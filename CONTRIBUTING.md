# Mitarbeiten an Teilbar

Für das Team (Amin, Matias, Sirat, Can). Einrichtung: [docs/setup.md](docs/setup.md). Begriffe: [GLOSSARY.md](GLOSSARY.md). Welche Datei wofür da ist: Index in [AGENTS.md](AGENTS.md).

## Werkzeuge

| Wofür | Werkzeug |
|---|---|
| Code, Reviews, Aufgaben, Board | GitHub: Repo, Issues, Projects, Pull Requests |
| Kurze Absprachen | WhatsApp-Gruppe |
| Meetings (einmal pro Woche, mit 10 Minuten Lab-Review; ein Agent trägt die Entscheidungen live ein) | Discord |
| Ergebnisse aus Meetings | keine Notizen: Aufgaben als Issue, Entscheidungen als ADR, Lab-Review direkt in den Daten |
| Entscheidungen | `docs/adr/NNNN-kurzname.md` (Kontext, Entscheidung, Folgen, Quellen) |
| KI-Einsatz dokumentieren | `ai-lab/` (siehe unten) |

Notion ist eingefroren und dient nur noch als Archiv.

## Ablauf einer Aufgabe (GitHub Flow)

1. **Issue** anlegen oder nehmen (Vorlage „Aufgabe“), sich selbst zuweisen, auf dem Board nach „In Arbeit“ ziehen.
2. **Branch** vom aktuellen `main`: `git switch main && git pull && git switch -c <issue-nr>-<kurzname>`.
3. **Arbeiten** mit dem Agenten deiner Wahl, im Devcontainer. Kleine Commits mit verständlichem Text.
4. **Sitzung protokollieren** am Ende jeder relevanten Agenten-Sitzung: dem Agenten „Sitzung protokollieren“ sagen. Er hängt einen Datensatz an `ai-lab/daten/sitzungen/<du>.jsonl` an und committet ihn auf deinem Branch.
5. **Pull Request** nach `main`: Vorlage ausfüllen, im Feld „Sitzungen“ die IDs der Protokolle eintragen, eine andere Person als Reviewer eintragen.
6. **Review:** Die andere Person prüft Code und Protokoll und gibt frei. Danach Squash-Merge, Branch löschen.

`main` ist geschützt: kein direkter Push, mindestens ein Review.

Konflikt in einer `ai-lab/daten/*.jsonl`? Auf GitHub nicht lösen, sondern lokal: `git merge main`. Git behält dank `merge=union` beide Zeilen; danach `python ai-lab/tools/lab.py check`.

## Mit KI arbeiten: unsere Regeln

- **Du bist verantwortlich**, nicht der Agent. Was du committest, hast du gelesen und verstanden.
- **Ein Protokoll pro relevanter Sitzung.** Relevant ist alles, was in Code, Doku, Design oder Entscheidungen einfließt. Kurze Fragen ohne Folgen brauchen keins.
- **Ehrlich protokollieren.** Ein begründetes „hat nicht funktioniert“ ist genauso wertvoll wie ein Erfolg.
- **Nichts Geheimes** in Prompts, die ins Protokoll kommen. Das Repo ist öffentlich. Der Agent schwärzt Keys und private Daten, prüf das trotzdem.
- **Experiment-Bitten des Agenten** sind freiwillig. Er fragt höchstens einmal pro Sitzung.
- **Neue Skills, Regeln oder Tools aus dem Internet** kommen nicht direkt ins Repo. Sag deinem Agenten „Ich will <Quelle> sichten“. Daraus entstehen Kandidaten, das Lab-Review wählt Hypothesen aus, und erst ein Experiment entscheidet, ob etwas bleibt.

## KI-Labor in 30 Sekunden

`ai-lab/` sammelt unsere Sitzungsprotokolle. Daraus entstehen Hypothesen („Wenn …, dann …, weil …“), die wir in kleinen Experimenten prüfen: dieselbe Aufgabe in zwei Konfigurationen, blind bewertet von einer anderen Person. Am Semesterende steht daraus der Bericht für die Projektabgabe. Einstieg: [ai-lab/README.md](ai-lab/README.md).
