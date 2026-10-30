# 0005 Daten des Labors als JSONL

Status: angenommen · 2026-10-30 (ersetzt die erste Fassung mit einer Markdown-Datei pro Sitzung)

## Kontext

Wir arbeiten viel mit Agenten. Eine Markdown-Datei pro Sitzung, Hypothese und Experiment wäre nach wenigen Wochen unübersichtlich und schwer auszuwerten. Gleichzeitig dürfen vier Personen auf parallelen Branches keine ständigen Merge-Konflikte bekommen.

## Entscheidung

- **Ein Datensatz pro Zeile in JSONL-Dateien** unter `ai-lab/daten/`: `sitzungen/<person>.jsonl`, `sichtungen.jsonl`, `kandidaten.jsonl`, `hypothesen.jsonl`, `experimente.jsonl`, `laeufe.jsonl`. Jeder Typ hat ein JSON-Schema in `ai-lab/schema/`.
- **Nur über `lab.py`:** `vorlage`, `add`, `set`, `log`, `zeige`, `liste`. `check` prüft Schema, doppelte IDs und Verweise, auch in der CI.
- **Konflikte:** Sitzungen liegen pro Person, weil sie am häufigsten entstehen. Für alle JSONL-Dateien gilt `merge=union` in `.gitattributes`. Lokal führt Git parallele Zeilen dadurch zusammen. Meldet GitHub trotzdem einen Konflikt, mergt man `main` lokal. Danach findet `lab.py check` doppelte IDs.
- **Protokoll per Befehl:** Am Sitzungsende schreibt der Agent den Datensatz aus seinem eigenen Kontext. Hooks erinnern nur, sie schneiden nichts mit. Die wichtigsten Prompts stehen wörtlich drin. Das kostet die Person höchstens etwa 2 Minuten.
- **Feldnamen Englisch, Inhalte Deutsch.** Feste Phasen: Recherche, Anforderung, Design, Planung, Implementierung, Test, Review, Deployment, Doku, Organisation.
- **Kosten:** Tokens (gemessen mit `lab.py tokens`, AgentsView, ccusage) werden zum Listenpreis aus `ai-lab/preise.yaml` in einen Schattenpreis umgerechnet. Dazu kommen Agentenzeit, Menschenzeit und Nacharbeit. Uni-Qwen zählt mit 0 $.
- Nicht übernommen: Transkript-Exporter, Langfuse, OpenTelemetry. Sie ersetzen das kuratierte Protokoll nicht und sind für uns zu schwer.

## Folgen

Menschen lesen die Daten über `lab.py zeige`, `stand`, `kandidaten` und den erzeugten Bericht, nicht in der Rohdatei. Recherchen sind keine eigene Dateiart: Was daraus testbar ist, wird eine Sichtung mit Kandidaten, Fakten fürs Setup gehen in ein ADR oder `docs/setup.md`.

## Quellen

- AgentsView: https://github.com/wesm/agentsview · ccusage: https://ccusage.com/guide/
- Git `merge=union`: https://git-scm.com/docs/gitattributes#_built_in_merge_drivers
