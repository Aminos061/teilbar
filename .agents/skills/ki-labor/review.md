# Lab-Review

Einmal pro Woche im Teammeeting: 10 Minuten, das erste etwa 30. Der Lab-Lead teilt den Bildschirm mit dieser Sitzung. Du führst durch die Punkte und trägst jede Entscheidung sofort ein. Es gibt kein Protokoll und keine Meeting-Notizen. Am Ende steht alles in Issues, in den Labordaten oder in einem ADR.

**Deine Rolle:** Du entscheidest nicht mit und stimmst nicht ab. Du wiederholst jede Entscheidung in einem Satz und trägst sie dann ein. Hinweisen darfst du nur, wenn eine Regel verletzt wäre, z. B. zwei Variablen, Bewerter = Verantwortlicher oder mehr als 5 offene Hypothesen.

## Vorbereiten

1. `git switch main && git pull`, dann `git switch -c lab-review-<JJJJ-MM-TT>`. Das Review wiederholt sich jede Woche und hat deshalb kein eigenes Issue.
2. `python ai-lab/tools/lab.py stand` und `python ai-lab/tools/lab.py kandidaten` ausführen und auf dem Bildschirm lassen.

## Ablauf

1. **Stand** (2 Min.): laufende Experimente und neue Befunde nennen. Befunde trägt die verantwortliche Person selbst ein ([experiment.md](experiment.md)), nicht das Review.
2. **Ideen** (3–10 Min.): Wer hat neue Kandidaten aus Sitzungen oder Sichtungen? Wer will eine Quelle sichten (Repo, Tool, Studie)?
3. **Auswahl** (nur wenn weniger als 5 Hypothesen offen sind): Für jeden Kandidaten, über den gesprochen wird, fragst du die vier Kriterien ab:
   - mit einer Variable testbar?
   - in 1–2 Wochen machbar?
   - passt zu einer Aufgabe, die bald ansteht?
   - wichtig für den Bericht?

   Bei Gleichstand entscheidet der Lab-Lead.
4. **Festlegen**, für jede neue Hypothese: wer verantwortlich ist, wer blind bewertet (eine andere Person) und an welcher echten Aufgabe getestet wird.
5. **Abschluss**: Fass alle Entscheidungen in einer Liste zusammen, dann folgen die Schritte unter „Am Ende“.

## Eintragen

| Entscheidung | Befehl |
|---|---|
| Kandidat wird Hypothese | wie in [hypothese.md](hypothese.md): Issue anlegen, dann `lab.py add hypothese` mit `candidate` |
| Kandidat später testen | `lab.py set <id> status=zurueckgestellt reason="…"` |
| Kandidat nicht testen | `lab.py set <id> status=verworfen reason="…"` (Material für „Was nicht funktioniert hat“) |
| Hypothese ändert sich (Status, Bewerter, Testaufgabe) | `lab.py set H<n> …` und `lab.py log H<n> "Lab-Review <datum>: …"` |
| Person sichtet eine Quelle | `gh issue create --title "[Aufgabe] Sichtung: <Quelle>" --assignee <login> --body "…"` |
| Eine Regel des Labors ändert sich | neues ADR in `docs/adr/` |

GitHub-Logins: amin `Aminos061`, matias `Matias5521`, sirat `siratjan`, can `candemirdoegen`.

## Am Ende

1. `python ai-lab/tools/lab.py check`.
2. Committen: `git add ai-lab/daten docs/adr && git commit -m "ai-lab: Lab-Review <JJJJ-MM-TT>"`.
3. Nach dem Okay des Lab-Leads pushen und einen PR „Lab-Review <JJJJ-MM-TT>“ öffnen. In die Beschreibung kommt die Liste der Entscheidungen mit Links zu den neuen Issues.
4. Jemand aus der Runde gibt den PR noch im Meeting frei. Danach mergen.
