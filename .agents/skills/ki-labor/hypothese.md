# Hypothese anlegen oder ändern

## Anlegen

1. **Platz prüfen:** `lab.py stand`. Sind schon 5 offen, legst du keine an. Die Idee bleibt Kandidat, und das Lab-Review entscheidet.
2. **Kandidat wählen:** `lab.py kandidaten`. Eine Hypothese stammt normalerweise aus einem Kandidaten. Ohne passenden Kandidaten legst du erst einen an (Sitzung oder [quelle.md](quelle.md)).
3. **Issue anlegen** mit der Vorlage „Hypothese“, z. B. `gh issue create --template hypothese.yml`. Die Issue-Nummer ist die ID (`H<n>`).
4. **Datensatz:** `lab.py vorlage hypothese`, ausfüllen und speichern mit `lab.py add hypothese <datei>`. Dabei:
   - `candidate` = ID des Kandidaten. Damit gilt er als übernommen.
   - `statement` als „Wenn …, dann …, weil …“ mit genau einer änderbaren Variable
   - `measure` und `decision_rule` (wann gilt sie als gestützt?)
   - `status: offen`, `evidence: 0`
5. `lab.py check`, dann `ai-lab/daten/` committen.

## Status ändern

```bash
python ai-lab/tools/lab.py set H12 status=geplant experiments='["E15"]'
python ai-lab/tools/lab.py log H12 "Experiment E15 geplant, Rater sirat"
```

Lebenszyklus:
1. `offen`
2. `geplant`: Das Experiment ist angelegt, die Entscheidungsregel steht.
3. `pilot`: 1 Lauf je Konfiguration. Zählt nicht als Beleg.
4. `getestet`
5. Ergebnis: `gestuetzt`, `nicht-gestuetzt` oder `unklar`
6. `repliziert`: gestützt und auf einer zweiten Aufgabe wiederholt (`evidence: 2`)
7. `regel`: geht als Do oder Don't in den Bericht

Jederzeit möglich sind `veraltet` (neue Modellversion) und `verworfen` (mit Grund im Log). Zu jeder Statusänderung gehört ein `log`-Eintrag.

Belegstufe (`evidence`):

| Stufe | Bedeutung |
|---|---|
| 0 | Beobachtung |
| 1 | ein Experiment auf einer Aufgabe |
| 2 | auf mindestens 2 Aufgaben repliziert |
| 3 | zusätzlich durch eine publizierte Studie gestützt |

## Skill aus einem Befund

Wenn ein Befund eine Hypothese stützt und sich das Vorgehen als Skill fassen lässt:
1. Leg den Skill in `ai-lab/skill-kandidaten/<name>/SKILL.md` an, mit Herkunft (Hypothese, Quelle, Lizenz).
2. Plan ein Experiment mit und ohne den Skill. Für Claude Code geht auch `claude plugin eval`.
3. Erst ab Belegstufe 2 und nach PR-Review kommt er nach `.agents/skills/`, danach `lab.py sync-skills`.
