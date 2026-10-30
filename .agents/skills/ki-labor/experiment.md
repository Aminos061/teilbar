# Experiment

## Planen

1. Issue mit der Vorlage „Experiment“ anlegen. Die Nummer ist die ID (`E<n>`).
2. `lab.py vorlage experiment` (setzt `base_commit` auf den aktuellen Commit), ausfüllen, `lab.py add experiment <datei>`. Bevor ein Lauf startet, steht darin:
   - **genau eine Variable** (`variable`) und die Konfigurationen A, B (… C)
   - `runs_per_config`, meist 3
   - `rater` (nicht `owner`), optional `second_rater`
   - `task`: Titel, Auftrag (`prompt`, für alle Läufe wortgleich), Checkliste der Anforderungen, Zeitlimit
   - `decision_rule`
   - `noise_probe`: Gibt es für diesen Aufgabentyp schon eine A/A-Probe? Sonst Konfiguration A zusätzlich 3× laufen lassen.
3. Hypothese: `lab.py set H<n> status=geplant experiments='["E<n>"]'` und `lab.py log H<n> "…"`.
4. `lab.py check`, committen.

## Durchführen

1. `python ai-lab/tools/lab.py experiment start E<n>` legt Folgendes an:
   - pro Lauf einen Worktree unter `../teilbar-exp/E<n>/<kennung>` auf Branch `exp/E<n>/<kennung>`, vom `base_commit` aus
   - die Läufe in `laeufe.jsonl`
   - eine zufällige Reihenfolge
2. Jeder Lauf: im eigenen Worktree, im Devcontainer, in einer frischen Sitzung mit der Konfiguration aus dem Plan, Auftrag wortgleich aus `task.prompt`. Ein getesteter Fremd-Skill wird nur im Worktree der Läufe abgelegt, die ihn brauchen.
3. Nach dem Lauf:
   - Ergebnis auf dem Branch committen, ohne Hinweis auf Harness oder Modell in der Nachricht und ohne „Co-authored-by“-Zeilen (Blindheit)
   - Zahlen eintragen: `lab.py set E<n>/A1 tokens='{…}' minutes='{"agent":12,"human":3,"rework":null}' objective='{"tests_pass":true,"lint_clean":true,"checklist_met":4}'`
   - Fehlschläge (Timeout, leeres Ergebnis) mit `failed=true` festhalten. Nicht wiederholen, bis es klappt.

## Blind bewerten

1. Die bewertende Person bekommt nur die Branch-Namen `exp/E<n>/<kennung>`. Die Daten des Experiments sieht sie sich vorher nicht an.
2. In zufälliger Reihenfolge prüft sie Tests, Lint und Checkliste und misst die Nacharbeit bis „fertig“ mit der Stoppuhr. Dann vergibt sie zwei Noten, Qualität und Verständlichkeit:

   | Note | Bedeutung |
   |---|---|
   | 1 | unbrauchbar |
   | 2 | läuft, aber mit groben Mängeln |
   | 3 | lauffähig, die Struktur ist aber fremd oder umständlich |
   | 4 | gut, kleine Nacharbeit |
   | 5 | so würde ich es mergen |

3. Eintragen über die Kennung: Der Agent sucht den Lauf mit `lab.py liste lauf`, ohne der bewertenden Person die Konfiguration zu nennen, und setzt `rating='{"rater":"sirat","quality":4,"clarity":4,"rework_min":5,"note":"…"}'`.
4. Ca. 20 % der Läufe bewertet `second_rater` zusätzlich (`rating.second`). Weichen die Noten um mehr als 1 Punkt ab, wird das Raster geschärft, bevor es einen Befund gibt.

## Befund

1. `lab.py bericht` rechnet je Konfiguration „k von n“, Median und Spanne aus den Läufen.
2. Wende die Entscheidungsregel genau so an, wie sie vorab festgeschrieben war: `lab.py set E<n> status=abgeschlossen finding='{"date":"…","decision":"gestuetzt","summary":"B in 3 von 3 Läufen weniger Nacharbeit (Median 5 statt 20 min)","limits":"eine Aufgabe, n=3"}'`
3. Hypothese: Status, `evidence` und `log`. Bei `unklar` wird das Experiment erweitert oder stillgelegt, nicht umgedeutet.
4. Worktrees mit `git worktree remove` aufräumen. Die `exp/`-Branches bleiben als Beleg auf dem Remote.
