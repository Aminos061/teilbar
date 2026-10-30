# Zwischenbericht

1. `python ai-lab/tools/lab.py check` muss grün sein.
2. `python ai-lab/tools/lab.py bericht` schreibt `ai-lab/berichte/<datum>.md` mit:
   - Sitzungen nach Phase, Harness, Modell und Arbeitsweise
   - Hypothesen mit Status und Belegstufe
   - je Experiment die Zahlen pro Konfiguration und den Befund
3. Ersetze den Platzhalter unter „Einordnung“ durch höchstens eine Seite auf Deutsch:
   - Was zeigen die Befunde (mit Belegstufe)?
   - Was sind nur Beobachtungen?
   - Was ist offen?
   - Was hat nicht funktioniert?

   Aus den Sitzungs-Tabellen leitest du keine Wirkung ab, sie sind Rohzahlen ohne Kontrolle.
4. Committen, dann einfrieren: `git tag lab-<datum>` und, nach Zustimmung, `git push origin lab-<datum>`.

Für den **Abschlussbericht** (Januar 2027):
- Do's und Don'ts nur ab Belegstufe 2, jeweils mit Experiment, n und Grenzen
- Kostenvergleich pro Phase und Konfiguration über den Schattenpreis
- ein eigenes Kapitel „Was nicht funktioniert hat“, auch mit den „Nicht übernommen“-Listen der Sichtungen
