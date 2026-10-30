#!/usr/bin/env python3
"""Werkzeug des KI-Labors. Alle Daten liegen als JSONL in ai-lab/daten/ (ADR 0005).
Ändere sie nur über diese Befehle, nie von Hand und nie mit neuen Markdown-Dateien.

  check                          Daten, Verweise und Markdown-Regel prüfen (läuft auch in der CI)
  stand [--issue N]              offene Hypothesen, laufende Experimente, neue Kandidaten, letzte Sitzungen
  kandidaten [--alle]            Kandidaten aus Sichtungen und Sitzungen
  liste TYP                      alle Einträge eines Typs als Tabelle
  zeige ID                       einen Eintrag lesbar anzeigen
  vorlage TYP [--person P --harness H --model M --issue N --slug S]
                                 leeren Eintrag als JSON ausgeben, zum Ausfüllen
  add TYP DATEI|-                Eintrag (oder Liste von Einträgen) aus JSON prüfen und speichern
  set ID feld=wert [...]         Felder ändern; wert als JSON, sonst Text; verschachtelt mit Punkt (tokens.output=5)
  log ID "Text"                  Hypothese: Zeile im Stand-Log ergänzen
  tokens --harness H [--session ID]
                                 Tokens einer Sitzung (claude-code, codex)
  experiment start E<n> [--dry-run]
                                 Worktrees, Blind-Kennungen und Läufe anlegen
  bericht                        Zwischenbericht nach ai-lab/berichte/<datum>.md
  sync-skills [--check]          .agents/skills nach .claude/skills kopieren

TYP: sitzung, sichtung, kandidat, hypothese, experiment, lauf
Braucht PyYAML und jsonschema (im Devcontainer installiert; sonst: pip install -r ai-lab/tools/requirements.txt).
"""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import filecmp
import fnmatch
import json
import os
import random
import re
import shutil
import statistics
import string
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML fehlt: pip install -r ai-lab/tools/requirements.txt")

ROOT = Path(__file__).resolve().parents[2]
LAB = ROOT / "ai-lab"
DATA = LAB / "daten"
SCHEMA = LAB / "schema"
OPEN_STATES = {"offen", "geplant", "pilot", "getestet"}
MAX_OPEN = 5  # ADR 0006
PERSONS = ("amin", "matias", "sirat", "can")

# Wo jeder Typ liegt. Sitzungen: eine Datei pro Person, damit sich parallele PRs selten berühren.
FILES = {
    "sitzung": "sitzungen/{person}.jsonl",
    "sichtung": "sichtungen.jsonl",
    "kandidat": "kandidaten.jsonl",
    "hypothese": "hypothesen.jsonl",
    "experiment": "experimente.jsonl",
    "lauf": "laeufe.jsonl",
}

# Einzige erlaubte Markdown-Dateien im Repo (ADR 0004). Neue Dateiart = PR, der diese Liste und den Index in AGENTS.md ändert.
ALLOWED_MD = [
    "README.md", "AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md", "GLOSSARY.md",
    "docs/setup.md", "docs/adr/[0-9][0-9][0-9][0-9]-*.md",
    "ai-lab/README.md", "ai-lab/berichte/*.md", "ai-lab/skill-kandidaten/*",
    ".agents/skills/*", ".claude/skills/*", ".github/*",
]

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# ---------- Daten lesen und schreiben ----------

def paths(typ: str) -> list[Path]:
    pattern = FILES[typ].replace("{person}", "*")
    return sorted(DATA.glob(pattern))


def read_lines(path: Path) -> list[dict]:
    out = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValueError(f"{path.relative_to(ROOT).as_posix()}:{n}: kein gültiges JSON ({e.msg})") from e
    return out


def records(typ: str) -> list[dict]:
    return [r for p in paths(typ) for r in read_lines(p)]


def write_lines(path: Path, recs: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in recs), encoding="utf-8", newline="\n")


def target(typ: str, rec: dict) -> Path:
    return DATA / FILES[typ].replace("{person}", rec.get("person", "unbekannt"))


def find(rid: str) -> tuple[str, Path, list[dict], int]:
    for typ in FILES:
        for p in paths(typ):
            recs = read_lines(p)
            for i, r in enumerate(recs):
                if r.get("id") == rid:
                    return typ, p, recs, i
    raise KeyError(f"keinen Eintrag mit id {rid!r} gefunden")


def today() -> str:
    return dt.date.today().isoformat()


def git(*a: str) -> str:
    try:
        return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    except Exception:  # noqa: BLE001
        return ""


# ---------- Schemas ----------

_validators: dict = {}


def validator(typ: str):
    if typ not in _validators:
        from jsonschema import Draft202012Validator, FormatChecker
        from referencing import Registry, Resource

        registry = Registry()
        for f in SCHEMA.glob("*.schema.json"):
            res = Resource.from_contents(json.loads(f.read_text(encoding="utf-8")))
            registry = registry.with_resource(f.name, res).with_resource(res.id(), res)
        schema = json.loads((SCHEMA / f"{typ}.schema.json").read_text(encoding="utf-8"))
        _validators[typ] = Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())
    return _validators[typ]


def schema_errors(typ: str, rec: dict) -> list[str]:
    return [f"{'/'.join(map(str, e.path)) or '(oben)'}: {e.message}"
            for e in sorted(validator(typ).iter_errors(rec), key=lambda e: list(e.path))]


# ---------- Schattenpreis ----------

def shadow_price(tokens: dict | None, model: str | None) -> float | None:
    prices = yaml.safe_load((LAB / "preise.yaml").read_text(encoding="utf-8"))["models"]
    p = prices.get(model or "")
    if p is None or not tokens or tokens.get("source") == "unbekannt":
        return None
    usd = sum((tokens.get(k) or 0) * (p.get(k) or 0) for k in ("input", "output", "cache_read", "cache_write"))
    return round(usd / 1_000_000, 4)


def model_of(typ: str, rec: dict) -> str | None:
    if typ == "sitzung":
        return (rec.get("config") or {}).get("model")
    if typ == "lauf":
        exp = next((e for e in records("experiment") if e["id"] == rec.get("experiment")), {})
        return ((exp.get("configs") or {}).get(rec.get("config")) or {}).get("model")
    return None


def derive(typ: str, rec: dict) -> None:
    """Felder, die lab.py selbst setzt."""
    if typ in ("sitzung", "lauf") and rec.get("tokens"):
        rec["shadow_price_usd"] = shadow_price(rec["tokens"], model_of(typ, rec))
    if typ == "lauf" and rec.get("experiment") and rec.get("run"):
        rec["id"] = f"{rec['experiment']}/{rec['run']}"


# ---------- check ----------

def cmd_check(_args) -> int:
    errors: list[str] = []
    data: dict[str, list[dict]] = {}
    for typ in FILES:
        data[typ] = []
        for p in paths(typ):
            rel = p.relative_to(ROOT).as_posix()
            try:
                recs = read_lines(p)
            except ValueError as e:
                errors.append(str(e))
                continue
            for r in recs:
                where = f"{rel} [{r.get('id', '?')}]"
                errors += [f"{where}: {e}" for e in schema_errors(typ, r)]
                if typ == "sitzung" and r.get("person") != p.stem:
                    errors.append(f"{where}: Sitzung von {r.get('person')} steht in der Datei von {p.stem}")
            data[typ] += recs
        dup = [k for k, v in Counter(r.get("id") for r in data[typ]).items() if v > 1]
        errors += [f"{typ} {d}: id doppelt (oft nach einem Merge): eine der Zeilen löschen" for d in dup]

    ids = {t: {r.get("id") for r in data[t]} for t in FILES}
    for k in data["kandidat"]:
        if k.get("origin") not in ids["sitzung"] | ids["sichtung"]:
            errors.append(f"kandidat {k.get('id')}: origin {k.get('origin')} ist weder Sitzung noch Sichtung")
        if k.get("status") in ("zurueckgestellt", "verworfen") and not k.get("reason"):
            errors.append(f"kandidat {k.get('id')}: braucht einen Grund (reason)")
    for h in data["hypothese"]:
        if h.get("candidate") and h["candidate"] not in ids["kandidat"]:
            errors.append(f"hypothese {h.get('id')}: candidate {h['candidate']} gibt es nicht")
        errors += [f"hypothese {h.get('id')}: Experiment {e} gibt es nicht" for e in h.get("experiments", []) if e not in ids["experiment"]]
    for e in data["experiment"]:
        if e.get("hypothesis") not in ids["hypothese"]:
            errors.append(f"experiment {e.get('id')}: Hypothese {e.get('hypothesis')} gibt es nicht")
        if e.get("owner") == e.get("rater"):
            errors.append(f"experiment {e.get('id')}: rater darf nicht owner sein (blinde Bewertung)")
    for lf in data["lauf"]:
        if lf.get("experiment") not in ids["experiment"]:
            errors.append(f"lauf {lf.get('id')}: Experiment {lf.get('experiment')} gibt es nicht")
    n_open = sum(h.get("status") in OPEN_STATES for h in data["hypothese"])
    if n_open > MAX_OPEN:
        errors.append(f"{n_open} offene Hypothesen, erlaubt sind {MAX_OPEN}")

    errors += markdown_violations()
    errors += sync_differences()
    total = sum(len(v) for v in data.values())
    if errors:
        print(f"✗ {len(errors)} Problem(e):")
        for e in errors:
            print("  -", e)
        return 1
    print(f"✓ {total} Einträge geprüft ({', '.join(f'{len(v)} {k}' for k, v in data.items())}); Markdown-Regel eingehalten; Skills synchron")
    return 0


def markdown_violations() -> list[str]:
    listed = git("ls-files", "--cached", "--others", "--exclude-standard", "--", "*.md")
    bad = [f for f in listed.splitlines() if f and not any(fnmatch.fnmatch(f, pat) for pat in ALLOWED_MD)]
    return [f"{f}: Markdown-Datei ist hier nicht vorgesehen. Daten gehören in ai-lab/daten/ (lab.py add), "
            f"Entscheidungen in docs/adr/, Aufgaben in ein Issue. Siehe Index in AGENTS.md" for f in bad]


# ---------- Ansichten ----------

def candidates() -> list[dict]:
    taken = {h["candidate"]: h["id"] for h in records("hypothese") if h.get("candidate")}
    out = []
    for k in records("kandidat"):
        k = dict(k)
        if k["id"] in taken:
            k["status"] = f"übernommen ({taken[k['id']]})"
        out.append(k)
    return out


def cmd_kandidaten(args) -> int:
    rows = candidates()
    shown = rows if args.alle else [c for c in rows if c["status"] == "neu"]
    print(f"Kandidaten: {sum(c['status'] == 'neu' for c in rows)} neu, {len(rows)} insgesamt" + ("" if args.alle else "  (alle: --alle)"))
    origin = None
    for c in shown:
        if c["origin"] != origin:
            origin = c["origin"]
            print(f"\n{origin}")
        extra = " · ".join(x for x in (c.get("effort"), c["status"] if c["status"] != "neu" else "", c.get("note") or "") if x)
        print(f"  #{c['id'].rsplit('#', 1)[1]:<3} {c['title']}" + (f"  [{extra}]" if extra else ""))
        print(f"       {c['statement']}")
    return 0


def cmd_stand(args) -> int:
    hyps = records("hypothese")
    open_h = [h for h in hyps if h.get("status") in OPEN_STATES]
    print(f"Offene Hypothesen: {len(open_h)} von max. {MAX_OPEN}")
    for h in open_h:
        mark = "  ◄ passt zu dieser Aufgabe" if args.issue and h.get("test_task") == args.issue else ""
        print(f"  {h['id']:<5} {h['status']:<9} {h['owner']:<7} {h['title']}{mark}")
        print(f"        {h['statement']}")
        if mark:
            print(f"        Messung: {h.get('measure', '—')}")
    running = [e for e in records("experiment") if e.get("status") in {"geplant", "laeuft", "bewertung"}]
    print(f"Laufende Experimente: {len(running)}")
    for e in running:
        print(f"  {e['id']:<5} {e['status']:<10} zu {e['hypothesis']}, bewertet von {e['rater']}")
    print(f"Neue Kandidaten: {sum(c['status'] == 'neu' for c in candidates())} (lab.py kandidaten)")
    sessions = sorted(records("sitzung"), key=lambda s: s["id"])
    by_person = Counter(s["person"] for s in sessions)
    print(f"Sitzungen: {len(sessions)} ({', '.join(f'{k} {v}' for k, v in sorted(by_person.items())) or '—'})")
    for s in sessions[-5:]:
        print(f"  {s['id']}")
    return 0


COLUMNS = {
    "sitzung": ["id", "outcome", "first_try", "shadow_price_usd"],
    "sichtung": ["id", "source.ref"],
    "kandidat": ["id", "status", "title"],
    "hypothese": ["id", "status", "evidence", "owner", "title"],
    "experiment": ["id", "hypothesis", "status", "owner", "rater"],
    "lauf": ["id", "blind_label", "failed", "rating.quality"],
}


def dig(rec: dict, dotted: str):
    for k in dotted.split("."):
        rec = rec.get(k) if isinstance(rec, dict) else None
    return rec


def cmd_liste(args) -> int:
    rows = candidates() if args.typ == "kandidat" else records(args.typ)
    cols = COLUMNS[args.typ]
    print(" | ".join(cols))
    for r in rows:
        print(" | ".join("—" if dig(r, c) is None else str(dig(r, c)) for c in cols))
    return 0


def cmd_zeige(args) -> int:
    try:
        typ, _p, recs, i = find(args.id)
    except KeyError as e:
        print(e)
        return 1
    print(f"# {typ} {args.id}")
    print(yaml.safe_dump(recs[i], allow_unicode=True, sort_keys=False, width=110))
    if typ in ("sichtung", "sitzung"):
        ks = [k for k in candidates() if k["origin"] == args.id]
        if ks:
            print("Kandidaten:")
            for k in ks:
                print(f"  {k['id']}  [{k['status']}]  {k['title']}")
    return 0


# ---------- Schreiben ----------

TEMPLATES = {
    "sitzung": {
        "id": "JJJJ-MM-TT_person_harness_issue-kurzname", "date": "JJJJ-MM-TT", "person": "amin",
        "task": {"issue": None, "title": "", "branch": None, "pr": None, "commits": []},
        "phases": ["Implementierung"],
        "config": {"harness": "claude-code", "harness_version": None, "interface": "cli", "environment": "devcontainer",
                   "model": "", "effort": None, "skills": [], "mcp": [], "subagents": [], "tools": []},
        "work_mode": "iterativ", "outcome": "erfolgreich", "first_try": "ja", "self_rating": None,
        "minutes": {"agent": None, "human": None, "rework": None},
        "tokens": {"input": None, "output": None, "cache_read": None, "cache_write": None, "source": "unbekannt", "how": ""},
        "goal": "", "prompts": [""], "agent_plan": [], "result": "", "went_well": [], "went_badly": [],
        "hypotheses": [], "experiment": None, "redacted": False,
    },
    "sichtung": {
        "id": "JJJJ-MM-TT_person_quelle", "date": "JJJJ-MM-TT", "person": "amin",
        "source": {"type": "open-source-repo", "ref": "", "version": None, "license": None, "harness_binding": None},
        "goal": "", "parts": [{"name": "", "promise": None, "cost": None, "portable": None, "chosen": False}],
        "not_adopted": [{"part": "", "reason": ""}], "notes": [],
    },
    "kandidat": {
        "origin": "ID der Sichtung oder Sitzung", "person": "amin", "date": "JJJJ-MM-TT", "title": "",
        "claim": None, "source_ref": None, "statement": "Wenn …, dann …, weil …", "variable": "mit vs. ohne …",
        "phases": ["Implementierung"], "measure": "", "test_idea": None, "harness_binding": None, "effort": "S",
        "status": "neu", "reason": None, "note": None,
    },
    "hypothese": {
        "id": "H<issue>", "title": "", "statement": "Wenn …, dann …, weil …", "status": "offen", "evidence": 0,
        "owner": "amin", "candidate": None, "source": None, "phases": ["Implementierung"], "measure": "",
        "decision_rule": "", "test_task": None, "experiments": [], "created": "JJJJ-MM-TT", "decided": None, "log": [],
    },
    "experiment": {
        "id": "E<issue>", "hypothesis": "H<n>", "status": "geplant", "owner": "amin", "rater": "sirat", "second_rater": None,
        "variable": "", "configs": {"A": {"harness": "claude-code", "model": "", "environment": "devcontainer", "effort": None,
                                          "skills": []},
                                    "B": {"harness": "claude-code", "model": "", "environment": "devcontainer", "effort": None,
                                          "skills": []}},
        "runs_per_config": 3, "base_commit": "", "task": {"title": "", "prompt": "", "checklist": [""], "time_limit_min": 30},
        "decision_rule": "", "noise_probe": None, "created": "JJJJ-MM-TT", "finding": None,
    },
    "lauf": {
        "experiment": "E<n>", "run": "A1", "config": "A", "blind_label": "abcd", "branch": "", "session": None, "failed": False,
        "tokens": None, "minutes": None, "objective": None, "rating": None, "notes": None,
    },
}


def slug(s: str) -> str:
    s = s.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:40]


def cmd_vorlage(args) -> int:
    rec = copy.deepcopy(TEMPLATES[args.typ])
    for k in ("date", "created"):
        if k in rec:
            rec[k] = today()
    if args.person and "person" in rec:
        rec["person"] = args.person
    if args.typ == "sitzung":
        if args.harness:
            rec["config"]["harness"] = args.harness
        if args.model:
            rec["config"]["model"] = args.model
        rec["task"]["issue"] = args.issue
        rec["task"]["branch"] = git("rev-parse", "--abbrev-ref", "HEAD") or None
        if args.person and args.harness and args.slug:
            rec["id"] = f"{today()}_{args.person}_{args.harness}_{args.issue or 0}-{slug(args.slug)}"
    if args.typ == "experiment":
        rec["base_commit"] = git("rev-parse", "--short", "HEAD")
    print(json.dumps(rec, ensure_ascii=False, indent=2))
    return 0


def cmd_add(args) -> int:
    raw = sys.stdin.read() if args.datei == "-" else Path(args.datei).read_text(encoding="utf-8")
    new = json.loads(raw)
    new = new if isinstance(new, list) else [new]
    existing = {r["id"] for r in records(args.typ)}
    errors, prepared = [], []
    for rec in new:
        rec.setdefault("date", today()) if args.typ in ("sitzung", "sichtung", "kandidat") else None
        if args.typ == "kandidat" and not rec.get("id"):
            used = [int(r["id"].rsplit("#", 1)[1]) for r in records("kandidat") + prepared if r["origin"] == rec.get("origin")]
            rec["id"] = f"{rec.get('origin')}#{max(used, default=0) + 1}"
        derive(args.typ, rec)
        errs = schema_errors(args.typ, rec)
        if rec.get("id") in existing:
            errs.append(f"id {rec['id']} gibt es schon (ändern: lab.py set)")
        if errs:
            errors += [f"[{rec.get('id', '?')}] {e}" for e in errs]
        prepared.append(rec)
        existing.add(rec.get("id"))
    if errors:
        print("✗ nichts gespeichert:")
        for e in errors:
            print("  -", e)
        return 1
    for rec in prepared:
        p = target(args.typ, rec)
        write_lines(p, (read_lines(p) if p.exists() else []) + [rec])
        print(f"✓ {args.typ} {rec['id']} → {p.relative_to(ROOT).as_posix()}"
              + (f"  (Schattenpreis {rec['shadow_price_usd']} $)" if rec.get("shadow_price_usd") is not None else ""))
    print("Weiter: python ai-lab/tools/lab.py check")
    return 0


def parse_value(v: str):
    try:
        return json.loads(v)
    except json.JSONDecodeError:
        return v


def cmd_set(args) -> int:
    try:
        typ, p, recs, i = find(args.id)
    except KeyError as e:
        print(e)
        return 1
    rec = copy.deepcopy(recs[i])
    for a in args.zuweisungen:
        key, sep, val = a.partition("=")
        if not sep:
            print(f"✗ {a!r}: erwartet feld=wert")
            return 1
        node, parts = rec, key.split(".")
        for k in parts[:-1]:
            node = node.setdefault(k, {}) if isinstance(node.get(k), dict) or node.get(k) is None else node[k]
        node[parts[-1]] = parse_value(val)
    derive(typ, rec)
    errs = schema_errors(typ, rec)
    if errs:
        print("✗ nicht gespeichert:")
        for e in errs:
            print("  -", e)
        return 1
    recs[i] = rec
    write_lines(p, recs)
    print(f"✓ {typ} {args.id} geändert")
    return 0


def cmd_log(args) -> int:
    typ, p, recs, i = find(args.id)
    if typ != "hypothese":
        print("log gibt es nur für Hypothesen")
        return 1
    recs[i].setdefault("log", []).append({"date": today(), "text": args.text})
    write_lines(p, recs)
    print(f"✓ {args.id}: Stand ergänzt")
    return 0


# ---------- tokens ----------

def claude_tokens(session: str | None) -> dict:
    base = Path(os.environ.get("CLAUDE_CONFIG_DIR", Path.home() / ".claude")) / "projects"
    project = base / re.sub(r"[^A-Za-z0-9]", "-", str(Path.cwd()))
    if session:  # Sitzungs-ID ist eindeutig, auch wenn die Sitzung in einem anderen Ordner lief
        files = sorted(base.glob(f"*/{session}.jsonl"))
    else:
        files = sorted(project.glob("*.jsonl"), key=lambda p: p.stat().st_mtime)
    if not files:
        raise FileNotFoundError(f"kein Transkript unter {project if not session else base}")
    tot, models = _claude_usage([files[-1]])
    # Subagenten liegen in <sitzung>/subagents/ und werden getrennt ausgewiesen (oft anderes Modell).
    sub_tot, sub_models = _claude_usage(sorted((files[-1].with_suffix("") / "subagents").glob("*.jsonl")))
    return {**tot, "source": "gemessen", "how": "lab.py tokens (Claude-Code-Transkript)",
            "subagents": {**sub_tot, "models": dict(sub_models)} if sub_models else None,
            "_model": models.most_common(1)[0][0] if models else None, "_session": files[-1].stem}


def _claude_usage(files: list[Path]) -> tuple[Counter, Counter]:
    tot, models = Counter(), Counter()
    for f in files:
        seen = set()
        for line in f.read_text(encoding="utf-8").splitlines():
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = rec.get("message") or {}
            usage, mid = msg.get("usage"), msg.get("id")
            if not usage or mid in seen:
                continue
            seen.add(mid)
            models[msg.get("model", "?")] += 1
            tot["input"] += usage.get("input_tokens", 0)
            tot["output"] += usage.get("output_tokens", 0)
            tot["cache_read"] += usage.get("cache_read_input_tokens", 0)
            tot["cache_write"] += usage.get("cache_creation_input_tokens", 0)
    return tot, models


def codex_tokens(session: str | None) -> dict:
    base = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "sessions"
    files = sorted(base.rglob("rollout-*.jsonl"), key=lambda p: p.stat().st_mtime)
    if session:
        files = [p for p in files if session in p.stem]
    if not files:
        raise FileNotFoundError(f"kein Rollout unter {base}")
    last, model = None, None
    for line in files[-1].read_text(encoding="utf-8").splitlines():
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        p = rec.get("payload") or {}
        model = p.get("model") or model
        if p.get("type") == "token_count" and (p.get("info") or {}).get("total_token_usage"):
            last = p["info"]["total_token_usage"]
    if not last:
        raise ValueError("keine token_count-Einträge im Rollout")
    cached = last.get("cached_input_tokens", 0)
    return {"input": last.get("input_tokens", 0) - cached, "cache_read": cached, "cache_write": 0,
            "output": last.get("output_tokens", 0), "source": "gemessen",
            "how": "lab.py tokens (Codex-Rollout, Format nicht offiziell dokumentiert)",
            "_model": model, "_session": files[-1].stem}


def cmd_tokens(args) -> int:
    readers = {"claude-code": claude_tokens, "codex": codex_tokens}
    if args.harness not in readers:
        print(f"Für {args.harness} liest lab.py keine Tokens selbst. Nimm (im Container installiert):\n"
              "  agentsview session usage <id> --format json   oder   ccusage session --json\n"
              "  opencode: `opencode stats` · qwen-code: `/stats model` · copilot-cli: `/usage` · goose/openhands: agentsview\n"
              "Kein Wert verfügbar → tokens.source: unbekannt.")
        return 2
    try:
        print(json.dumps(readers[args.harness](args.session), indent=2))
    except (FileNotFoundError, ValueError) as e:
        print(f"{e}. Mit --session <id> eine bestimmte Sitzung wählen, sonst tokens.source: unbekannt.")
        return 1
    print("Felder ohne _ als `tokens` übernehmen.")
    return 0


# ---------- experiment ----------

def cmd_experiment(args) -> int:
    try:
        typ, p, recs, i = find(args.id)
    except KeyError as e:
        print(e)
        return 1
    exp = recs[i]
    if any(lf["experiment"] == args.id for lf in records("lauf")):
        print(f"{args.id} hat schon Läufe: lab.py liste lauf")
        return 1
    runs = [f"{c}{n}" for n in range(1, exp["runs_per_config"] + 1) for c in sorted(exp["configs"])]
    random.shuffle(runs)  # Konfigurationen abwechselnd, Reihenfolge zufällig
    wt_root = ROOT.parent / f"{ROOT.name}-exp" / args.id
    labels: set[str] = set()
    new = []
    print(f"Reihenfolge der Läufe (so ausführen): {' → '.join(runs)}")
    for run in runs:
        label = "".join(random.choices(string.ascii_lowercase, k=4))
        while label in labels:
            label = "".join(random.choices(string.ascii_lowercase, k=4))
        labels.add(label)
        branch = f"exp/{args.id}/{label}"
        wt = wt_root / label
        if not args.dry_run:
            subprocess.run(["git", "worktree", "add", "-b", branch, str(wt), exp["base_commit"]], cwd=ROOT, check=True)
        new.append({"id": f"{args.id}/{run}", "experiment": args.id, "run": run, "config": run[0], "blind_label": label,
                    "branch": branch, "session": None, "failed": False, "tokens": None, "minutes": None,
                    "objective": None, "rating": None, "notes": None})
        print(f"  {run}: {wt}  (Branch {branch})")
    if args.dry_run:
        print("Probelauf: nichts gespeichert.")
        return 0
    lp = DATA / FILES["lauf"]
    write_lines(lp, (read_lines(lp) if lp.exists() else []) + new)
    exp["status"] = "laeuft"
    write_lines(p, recs)
    print("Die bewertende Person bekommt nur die Branch-Namen exp/…/<kennung>.")
    return 0


# ---------- bericht ----------

def spread(values: list) -> str:
    v = [x for x in values if x is not None]
    if not v:
        return "—"
    med = statistics.median(v)
    return f"{med:g} ({min(v):g}–{max(v):g})"


def cmd_bericht(_args) -> int:
    sessions = records("sitzung")
    hyps, exps, runs = records("hypothese"), records("experiment"), records("lauf")
    out = [f"# KI-Labor · Zwischenbericht {today()}", "",
           f"Erzeugt mit `lab.py bericht` aus {len(sessions)} Sitzungen, {len(records('kandidat'))} Kandidaten, "
           f"{len(hyps)} Hypothesen und {len(exps)} Experimenten. Stand des Repos: `{git('rev-parse', '--short', 'HEAD') or '?'}`.", "",
           "Die Sitzungs-Tabellen sind Rohzahlen ohne Kontrolle. Wirkungsaussagen stehen nur bei den Experimenten.", ""]

    def table(title, key):
        rows = defaultdict(Counter)
        for s in sessions:
            vals = s.get(key) if isinstance(s.get(key), list) else [(s.get("config") or {}).get(key) if key in ("harness", "model") else s.get(key)]
            for k in vals:
                r = rows[k]
                r["n"] += 1
                r["ok"] += s.get("first_try") == "ja"
                r["usd"] += s.get("shadow_price_usd") or 0
                for m in ("human", "rework"):
                    v = (s.get("minutes") or {}).get(m)
                    if v is not None:
                        r[m] += v
                        r[m + "_n"] += 1

        def mins(r, m):  # fehlende Angaben nicht als 0 ausgeben
            if not r[m + "_n"]:
                return "—"
            return f"{r[m]:.0f}" + ("" if r[m + "_n"] == r["n"] else f" ({r[m + '_n']} von {r['n']} erfasst)")

        out.extend([f"## {title}", "", "| | Sitzungen | beim ersten Mal gepasst | Schattenpreis $ | Menschenzeit min | Nacharbeit min |",
                    "|---|---|---|---|---|---|"])
        for k, r in sorted(rows.items(), key=lambda kv: -kv[1]["n"]):
            out.append(f"| {k} | {r['n']} | {r['ok']} von {r['n']} | {r['usd']:.2f} | {mins(r, 'human')} | {mins(r, 'rework')} |")
        out.append("")

    table("Nach Phase", "phases")
    table("Nach Harness", "harness")
    table("Nach Modell", "model")
    table("Nach Arbeitsweise (Ziel vorgeben vs. gemeinsam iterieren)", "work_mode")

    out.extend(["## Hypothesen", "", "| ID | Status | Belegstufe | Verantwortlich | Aussage |", "|---|---|---|---|---|"])
    for h in sorted(hyps, key=lambda h: int(h["id"][1:])):
        out.append(f"| {h['id']} | {h['status']} | {h['evidence']} | {h['owner']} | {h['statement']} |")
    out.append("")

    out.extend(["## Experimente", ""])
    for e in sorted(exps, key=lambda e: int(e["id"][1:])):
        out.append(f"### {e['id']} zu {e['hypothesis']}: {e['variable']} ({e['status']})")
        out.append("")
        out.append("| Konfiguration | Läufe | gescheitert | Tests grün | Checkliste erfüllt | Qualität | Nacharbeit min | Schattenpreis $ |")
        out.append("|---|---|---|---|---|---|---|---|")
        n_check = len(e["task"]["checklist"])
        for c, cfg in sorted(e["configs"].items()):
            rs = [r for r in runs if r["experiment"] == e["id"] and r["config"] == c]
            ob = [r.get("objective") or {} for r in rs]
            rt = [r.get("rating") or {} for r in rs]
            tests = sum(o.get("tests_pass") is True for o in ob)
            label = f"{cfg['harness']}/{cfg['model']}/{cfg.get('effort') or '-'}"
            if cfg.get("skills"):
                label += " + " + ", ".join(cfg["skills"])
            out.append(f"| {c}: {label} | {len(rs)} | "
                       f"{sum(r.get('failed', False) for r in rs)} | {tests} von {len(rs)} | "
                       f"{spread([o.get('checklist_met') for o in ob])} von {n_check} | {spread([r.get('quality') for r in rt])} | "
                       f"{spread([r.get('rework_min') for r in rt])} | {spread([r.get('shadow_price_usd') for r in rs])} |")
        f = e.get("finding")
        out.append("")
        out.append(f"Entscheidungsregel: {e['decision_rule']}")
        out.append(f"Befund: {f['decision']}. {f['summary']}" + (f". Grenzen: {f['limits']}" if f.get("limits") else "") if f else "Befund: noch keiner.")
        out.append("")

    path = LAB / "berichte" / f"{today()}.md"
    path.parent.mkdir(exist_ok=True)
    path.write_text("\n".join(out) + "\n\n## Einordnung\n\n(von Hand ergänzen: Skill ki-labor, bericht.md)\n", encoding="utf-8", newline="\n")
    print(path.relative_to(ROOT).as_posix())
    print(f"Einfrieren: git tag lab-{today()} && git push origin lab-{today()}")
    return 0


# ---------- sync-skills ----------

SRC, DST = ROOT / ".agents" / "skills", ROOT / ".claude" / "skills"


def sync_differences() -> list[str]:
    if not SRC.exists():
        return []
    if not DST.exists():
        return [".claude/skills fehlt: python ai-lab/tools/lab.py sync-skills"]
    diffs: list[str] = []

    def walk(c, prefix=""):
        for n in c.left_only + c.right_only + c.diff_files:
            diffs.append(f"Skill-Kopie weicht ab: {prefix}{n} (python ai-lab/tools/lab.py sync-skills)")
        for name, sub in c.subdirs.items():
            walk(sub, f"{prefix}{name}/")
    walk(filecmp.dircmp(SRC, DST))
    return diffs


def cmd_sync(args) -> int:
    if args.check:
        d = sync_differences()
        print("\n".join(d) or "✓ Skills synchron")
        return 1 if d else 0
    if DST.exists():
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST)
    print(f"✓ {SRC.relative_to(ROOT).as_posix()} → {DST.relative_to(ROOT).as_posix()}")
    return 0


# ---------- main ----------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    typ = dict(choices=list(FILES))
    sub.add_parser("check").set_defaults(fn=cmd_check)
    s = sub.add_parser("stand"); s.add_argument("--issue", type=int); s.set_defaults(fn=cmd_stand)
    s = sub.add_parser("kandidaten"); s.add_argument("--alle", action="store_true"); s.set_defaults(fn=cmd_kandidaten)
    s = sub.add_parser("liste"); s.add_argument("typ", **typ); s.set_defaults(fn=cmd_liste)
    s = sub.add_parser("zeige"); s.add_argument("id"); s.set_defaults(fn=cmd_zeige)
    s = sub.add_parser("vorlage"); s.add_argument("typ", **typ)
    for k in ("person", "harness", "model", "slug"):
        s.add_argument(f"--{k}")
    s.add_argument("--issue", type=int); s.set_defaults(fn=cmd_vorlage)
    s = sub.add_parser("add"); s.add_argument("typ", **typ); s.add_argument("datei"); s.set_defaults(fn=cmd_add)
    s = sub.add_parser("set"); s.add_argument("id"); s.add_argument("zuweisungen", nargs="+"); s.set_defaults(fn=cmd_set)
    s = sub.add_parser("log"); s.add_argument("id"); s.add_argument("text"); s.set_defaults(fn=cmd_log)
    s = sub.add_parser("tokens"); s.add_argument("--harness", required=True); s.add_argument("--session"); s.set_defaults(fn=cmd_tokens)
    s = sub.add_parser("experiment"); s.add_argument("aktion", choices=["start"]); s.add_argument("id")
    s.add_argument("--dry-run", action="store_true"); s.set_defaults(fn=cmd_experiment)
    sub.add_parser("bericht").set_defaults(fn=cmd_bericht)
    s = sub.add_parser("sync-skills"); s.add_argument("--check", action="store_true"); s.set_defaults(fn=cmd_sync)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
