# 0006 Vom Kandidaten zum Befund

Status: angenommen · 2026-10-30

## Kontext

Repos wie Superpowers, Cookbooks oder Skill-Sammlungen enthalten Behauptungen, die für andere Projekte und Modelle aufgestellt wurden. Mit vier Personen in einem Semester sind große A/B-Tests nicht machbar, reines Beobachten liefert aber keine belegten Aussagen.

## Entscheidung

- **Kandidaten** entstehen aus eigenen Sitzungen und aus **Sichtungen** fremder Quellen. Eine Sichtung läuft so: Ziel klären, Quelle nur lesen (nichts installieren), Bestandteile zeigen, höchstens 3 auswählen, Kandidaten formulieren, von der Person bestätigen lassen. Was nicht übernommen wird, bleibt mit Grund stehen.
- **Auswahl:** Das wöchentliche Lab-Review macht Kandidaten zu Hypothesen (Issue + Datensatz mit `candidate`). Höchstens 5 sind gleichzeitig offen. Ist ein Platz frei, darf die sichtende Person direkt eine anlegen.
- **Experimente:** genau eine Variable. Die Entscheidungsregel steht vor dem ersten Lauf fest. Alle Läufe starten am selben Commit im eigenen Worktree (`lab.py experiment start`), in zufälliger Reihenfolge. Fehlschläge zählen mit. Einmal pro Aufgabentyp gibt es eine A/A-Rauschprobe. Ein getesteter Fremd-Skill wird nur im Worktree der Läufe installiert.
- **Bewertung:** blind durch eine andere Person. Objektiv: Tests, Lint, Checkliste. Subjektiv 1–5: Qualität und Verständlichkeit. Dazu Nacharbeit, Schattenpreis und Laufzeit. Etwa 20 % der Läufe bewertet eine zweite Person.
- **Lebenszyklus:** offen → geplant → pilot → getestet → gestützt / nicht gestützt / unklar → repliziert → Regel, jederzeit veraltet oder verworfen. Belegstufen: 0 Beobachtung, 1 ein Experiment, 2 auf mindestens 2 Aufgaben repliziert, 3 zusätzlich durch eine Studie gestützt. Do's und Don'ts im Bericht gibt es erst ab Stufe 2. Ergebnisse stehen als „k von n“ mit Spannweite da, nie als „signifikant“.
- **Berichte:** `lab.py bericht` monatlich und zu jeder Abgabe, jeweils mit Git-Tag `lab-<datum>`. Im Januar 2027 folgt der Abschlussbericht mit einem Kapitel „Was nicht funktioniert hat“.
- **Werkzeuge:** eigenes Skript für Worktrees und Blind-Kennungen. `claude plugin eval` nur für Skill-Hypothesen in Claude Code. promptfoo, Inspect AI und Terminal-Bench vergleichen keine Harness-Konfigurationen und sind zu groß.
- **Start:** Die erste Sichtung (Recherche vom 30.10.) schlägt 5 Start-Hypothesen vor: kurze AGENTS.md, Effort nach Phase, Fremd-Review, Routine mit Uni-Qwen, erst fragen, dann coden.

## Folgen

Wissen entsteht nur aus Befunden, nicht aus gesammelten Empfehlungen. Ein begründetes „nicht gestützt“ ist ein vollwertiges Ergebnis.

## Quellen

- Statistik bei Modell-Evals: https://anthropic.com/research/statistical-approach-to-model-evals
- Streuung identischer Agenten-Läufe: https://arxiv.org/abs/2602.07150
- Superpowers: https://github.com/obra/superpowers · mattpocock/skills: https://github.com/mattpocock/skills
