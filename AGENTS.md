# Teilbar · Regeln für Agenten

Kurz gehalten mit Absicht (`docs/adr/0004`). Hier steht nur, was nicht offensichtlich ist, und wo was hingehört.

## Arbeitsweise

- Jede Aufgabe ist ein GitHub-Issue. Gearbeitet wird auf dem Branch `<issue-nr>-<kurzname>`, nie direkt auf `main`. Merge nur über einen PR mit Review durch eine andere Person.
- Arbeite im Devcontainer (`.devcontainer/`). Läuft die Sitzung auf dem Host, vermerkst du das im Sitzungsprotokoll.
- Keine Keys, Tokens oder privaten Daten in Dateien, Commits oder PR-Texte. Das Repo ist öffentlich.
- Begriffe der App und des KI-Labors: `GLOSSARY.md`. Verwende sie so, wie sie dort stehen.

## Wohin mit etwas Neuem

**Leg keine neuen Markdown-Dateien an.** `lab.py check` (auch in der CI) lehnt jede `.md` ab, die nicht im Index unten steht. Was festgehalten werden soll, gehört an genau eine dieser Stellen:

| Du willst festhalten … | Dann |
|---|---|
| eine Sitzung mit einem Agenten | Skill `sitzung-protokollieren`, landet als Datensatz in `ai-lab/daten/sitzungen/` |
| eine Idee, die sich testen ließe | Kandidat: `python ai-lab/tools/lab.py add kandidat` (Skill `ki-labor`) |
| was eine fremde Quelle (Repo, Framework, Studie) taugt | Sichtung mit Kandidaten (Skill `ki-labor` → `quelle.md`). URLs stehen im Datensatz. Recherche-Dateien gibt es nicht. |
| Hypothese, Experiment, Lauf, Bewertung, Befund | `lab.py vorlage` / `add` / `set` / `log` (Skill `ki-labor`) |
| eine Entscheidung, deren Begründung bleiben soll | neues ADR `docs/adr/NNNN-titel.md` (nächste Nummer, Aufbau wie die bestehenden). Ein altes ADR schreibst du nicht um, sondern ersetzt es durch ein neues und setzt beim alten `Status: ersetzt durch NNNN`. |
| eine Aufgabe, einen Plan, ein Meeting-Ergebnis | GitHub-Issue oder Kommentar im Issue |
| einen neuen oder geänderten Begriff | `GLOSSARY.md`, im selben PR wie die Änderung, die ihn braucht |

Eine neue Art von Datei braucht einen PR, der diesen Index und `ALLOWED_MD` in `ai-lab/tools/lab.py` ändert.

## Index

| Datei / Ordner | Zweck | Ändern wann und wie |
|---|---|---|
| `AGENTS.md` | Regeln und dieser Index, für alle Agenten | wenn eine Regel, Datei oder Dateiart dazukommt oder wegfällt. Kurz halten. |
| `CLAUDE.md` | enthält nur `@AGENTS.md` | nie |
| `README.md` | für Menschen: was Teilbar ist, wie man die App startet, Einstieg ins Team-Setup | wenn sich App oder Start ändern |
| `CONTRIBUTING.md` | Ablauf Issue → Branch → PR → Review, Rollen, Lab-Review | wenn sich der Ablauf ändert, zusammen mit einem ADR |
| `GLOSSARY.md` | Begriffe der App und des Labors | siehe oben |
| `docs/setup.md` | Einrichtung: Container, CLIs, Logins | wenn sich ein Werkzeug, eine Version oder ein Login ändert, zusammen mit `.devcontainer/` |
| `docs/adr/NNNN-*.md` | Entscheidungen mit Kontext, Folgen und Quellen | neue Datei je Entscheidung, bestehende nur beim Status |
| `ai-lab/README.md` | für Menschen: wie man das Labor benutzt | wenn sich Befehle oder Ablauf ändern |
| `ai-lab/daten/*.jsonl`, `ai-lab/daten/sitzungen/<person>.jsonl` | alle Datensätze des Labors, einer pro Zeile | **nur über `lab.py`**. Nie von Hand umformatieren oder sortieren. |
| `ai-lab/schema/*.schema.json` | Felder und erlaubte Werte der Datensätze | wenn ein Feld dazukommt; danach `lab.py check` auf allen Daten. Bei Bedeutungsänderung ein ADR. |
| `ai-lab/preise.yaml` | Preise für den Schattenpreis | wenn ein Modell dazukommt oder sich ein Preis ändert, mit Quelle und Datum |
| `ai-lab/tools/lab.py` | einziges Werkzeug für die Daten | per PR; `check` muss grün bleiben |
| `ai-lab/berichte/<datum>.md` | Zwischen- und Abschlussberichte | nur `lab.py bericht` plus Einordnung. Nach dem Tag `lab-<datum>` nicht mehr ändern. |
| `ai-lab/skill-kandidaten/<name>/` | Skills aus Befunden, noch im Test | Skill `ki-labor` → `hypothese.md` |
| `.agents/skills/` | Skills (Original) | wenn sich ein Ablauf ändert; danach `python ai-lab/tools/lab.py sync-skills` |
| `.claude/skills/` | Kopie für Claude Code | nie von Hand |
| `opencode.json` | OpenCode mit dem Uni-LiteLLM | wenn sich Modell oder Endpunkt ändern |
| `.devcontainer/` | gemeinsame Umgebung mit festen Versionen | Versionen nur hier pinnen |
| `.githooks/`, `.gitleaks.toml` | Secret-Scan vor dem Commit, Erinnerung vor dem Push | selten |
| `.github/` | Issue- und PR-Vorlagen, CI | wenn sich Ablauf oder Prüfungen ändern |
| `.gitattributes` | Zeilenenden, `merge=union` für die JSONL-Daten | selten |
| `index.html`, `img/`, `fonts/` | App-Prototyp | über Aufgaben-Issues |

## KI-Labor

- **Zu Beginn einer Aufgabe:** `python ai-lab/tools/lab.py stand --issue <n>`. Passt eine offene Hypothese, darfst du **eine** kurze Bitte für einen Test stellen (Skill `ki-labor`). Ein Nein gilt.
- **Am Ende einer Aufgabe**, oder wenn die Person sich verabschiedet: Erinnere an „Sitzung protokollieren“ (Skill `sitzung-protokollieren`), falls es in dieser Sitzung noch kein Protokoll gibt.
- Starte keinen Subagenten und kein anderes Modell für Vergleiche ohne ausdrückliche Zustimmung.
- Vor jedem Commit unter `ai-lab/` oder an einer `.md`-Datei: `python ai-lab/tools/lab.py check`.
