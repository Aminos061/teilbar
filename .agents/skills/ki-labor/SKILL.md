---
name: ki-labor
description: Arbeitet mit dem KI-Labor (ai-lab/): Quellen sichten, Kandidaten, Hypothesen, Experimente, blinde Bewertung, Berichte. Verwenden zu Beginn einer Aufgabe (passt eine offene Hypothese?), wenn jemand ein Repo, Framework, Skill-Paket oder Tool ausprobieren oder sichten will, Kandidaten sehen, eine Hypothese anlegen, ein Experiment planen oder starten, Läufe bewerten, einen Befund festhalten, das Lab-Review durchführen oder einen Zwischenbericht erzeugen will, oder fragt, wie der Stand des Labors ist.
---

# KI-Labor

Das Team protokolliert seinen KI-Einsatz und prüft Hypothesen in kleinen, blind bewerteten Experimenten. Regeln: `docs/adr/0005` und `0006`. Begriffe: `GLOSSARY.md`. Lies nur die Unterdatei, die du gerade brauchst.

**Alle Daten sind JSONL in `ai-lab/daten/` und werden nur über `python ai-lab/tools/lab.py` geändert** (`vorlage`, `add`, `set`, `log`). Leg keine Markdown-Dateien an.

| Was | Unterdatei |
|---|---|
| Stand zeigen oder zu Beginn einer Aufgabe prüfen | hier unten |
| Repo, Framework, Tool oder Studie sichten und Kandidaten festhalten | [quelle.md](quelle.md) |
| Hypothese aus einem Kandidaten anlegen, Status ändern | [hypothese.md](hypothese.md) |
| Experiment planen, starten, Läufe festhalten, blind bewerten, Befund | [experiment.md](experiment.md) |
| Lab-Review im Wochenmeeting durchführen und Entscheidungen eintragen | [review.md](review.md) |
| Zwischenbericht erzeugen | [bericht.md](bericht.md) |
| Sitzung protokollieren | Skill `sitzung-protokollieren` |

## Stand und Beginn einer Aufgabe

1. `python ai-lab/tools/lab.py stand --issue <n>` (Issue der Aufgabe, falls bekannt).
2. Ist eine offene Hypothese als „passt zu dieser Aufgabe“ markiert, oder passt sie inhaltlich klar (gleiche Phase, gleiche Art von Aufgabe)? Dann stellst du **höchstens eine** kurze, konkrete Bitte. Beispiel: „H11 sucht Reviews durch ein anderes Modell. Magst du den Diff danach zusätzlich von Codex reviewen lassen? Dauert ca. 5 Minuten.“ Ein Nein wird akzeptiert und nicht wiederholt.
3. Einen Subagenten oder ein anderes Modell startest du nur nach ausdrücklicher Zustimmung und nie für mehr als die gefragte Wiederholung.
4. Am Ende der Aufgabe erinnerst du an „Sitzung protokollieren“.

## Regeln

- Höchstens 5 offene Hypothesen. Eine neue gibt es erst, wenn ein Platz frei ist.
- Wirkung behauptest du nur mit einem Befund, als „k von n“ mit Spannweite. Nie „signifikant“, nie „bewiesen“.
- Fremde Quellen nennst du mit URL, Lizenz und dem Harness, für den sie gebaut sind.
- Einträge liest du mit `lab.py zeige <id>`, Listen mit `lab.py liste <typ>` oder `lab.py kandidaten`.
