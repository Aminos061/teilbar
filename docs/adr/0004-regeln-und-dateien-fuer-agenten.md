# 0004 Regeln und Dateien für Agenten

Status: angenommen · 2026-10-30

## Kontext

Vier Personen arbeiten mit mehreren Harnesses. Jeder Agent legt gern neue Markdown-Dateien an. Ohne Regel entsteht ein Dokumentensalat, den weder Menschen noch Agenten überblicken. Lange Regeldateien helfen Agenten laut Studie nicht und kosten Tokens.

## Entscheidung

- `AGENTS.md` ist die einzige Regeldatei. Sie ist kurz und enthält den **Index aller Dateien**: Zweck, wer sie ändert und wann. `CLAUDE.md` importiert sie nur.
- **Erlaubte Markdown-Dateien** sind nur die im Index. `lab.py check` (auch in der CI) lehnt jede andere `.md`-Datei ab. Eine neue Dateiart braucht einen PR, der den Index und die Liste in `lab.py` ändert.
- Daten des Labors sind JSONL, keine Dokumente (ADR 0005). Entscheidungen sind ADRs in `docs/adr/`. Aufgaben und Pläne sind Issues.
- Skills liegen in `.agents/skills/` im Agent-Skills-Format. `lab.py sync-skills` kopiert sie nach `.claude/skills/` (Symlinks sind unter Windows unzuverlässig). Skills sind klein: kurze `SKILL.md`, Details in Unterdateien, die erst bei Bedarf gelesen werden.
- Fremde Skills und Regeln kommen nicht direkt ins Repo, sondern über eine Sichtung (ADR 0006).

## Folgen

Wer etwas festhalten will, muss sich entscheiden: Datensatz, ADR, Issue oder Änderung an einer bestehenden Datei. Das ist gewollt.

## Quellen

- ETH-Studie zu Kontextdateien: https://arxiv.org/abs/2602.11988
- AGENTS.md: https://agents.md · Agent Skills: https://agentskills.io
