---
name: sitzung-protokollieren
description: Hält am Ende einer Sitzung das Sitzungsprotokoll des KI-Labors als Datensatz in ai-lab/daten/sitzungen/ fest. Verwenden, wenn die Person "Sitzung protokollieren", "protokolliere die Sitzung" oder /sitzung-protokollieren sagt, oder wenn eine Aufgabe fertig ist und diese Sitzung noch kein Protokoll hat.
---

# Sitzung protokollieren

Du protokollierst **diese** Sitzung aus deinem eigenen Kontext, als ein Datensatz. Du schreibst keine Markdown-Datei. Begriffe: `GLOSSARY.md`. Feldwerte und Token-Quellen je Harness: [felder.md](felder.md). Ziel: höchstens 2 Minuten Aufwand für die Person.

## Ablauf

1. **Sammeln, was du schon weißt:**
   - Aufgabe, Issue und Phasen
   - deine Konfiguration: Harness, Modell, Effort, Skills, MCPs, Subagenten, Werkzeuge
   - deine Schrittliste und die wichtigsten Prompts im Wortlaut
   - Ergebnis, Commits und was nachgebessert wurde

   Erfinde nichts. Was du nicht weißt, ist `null`.
2. **Einmal nachfragen, alles in einer Nachricht**, jeweils mit deinem Vorschlag, sodass ein „ok“ genügt:
   - Person, falls du sie nicht kennst
   - Ergebnis, „beim ersten Mal gepasst?“ und Arbeitsweise
   - Menschenzeit und Nacharbeit in Minuten, Zufriedenheit 1–5
   - Kandidaten: Beobachtungen, die sich als „Wenn …, dann …, weil …“ testen ließen
3. **Vorlage holen:** `python ai-lab/tools/lab.py vorlage sitzung --person <p> --harness <h> --model <m> --issue <n> --slug <kurzname>`
4. **Tokens:** `python ai-lab/tools/lab.py tokens --harness <h>` (für `claude-code` und `codex`, sonst siehe [felder.md](felder.md)). Die Felder ohne `_` übernimmst du als `tokens`.
5. **Ausfüllen und schwärzen:** Füll die Vorlage aus und speichere sie als temporäre Datei außerhalb des Repos. Die Texte sind Deutsch, knapp und mit Beleg. Keys, Tokens (`sk-…`, `ghp_…`, `Bearer …`), Passwörter, private Kontaktdaten, Matrikelnummern und Namen Dritter ersetzt du durch `[GESCHWÄRZT]` und setzt `redacted: true`, denn das Repo ist öffentlich.
6. **Speichern:** `python ai-lab/tools/lab.py add sitzung <datei>`. Den Schattenpreis rechnet `lab.py` selbst. Bei Fehlern korrigierst du und rufst den Befehl erneut auf. Danach löschst du die temporäre Datei.
7. **Kandidaten** (falls die Person welche bestätigt hat): `python ai-lab/tools/lab.py vorlage kandidat`, `origin` auf die ID der Sitzung setzen, dann `lab.py add kandidat <datei>`. Mehrere Kandidaten gehen auch als JSON-Liste in einer Datei.
8. **Prüfen und committen:** `python ai-lab/tools/lab.py check`, dann nur `ai-lab/daten/` committen: `git add ai-lab/daten && git commit -m "ai-lab: Sitzung <id>"`. Nicht auf `main`, und pushen entscheidet die Person.

Nachträglich ändern, zum Beispiel die Nacharbeit: `python ai-lab/tools/lab.py set <id> minutes.rework=20`.

## Ohne Shell (Web-Chat)

Gib den Datensatz als einen JSON-Codeblock nach `ai-lab/schema/sitzung.schema.json` aus. Die Person speichert ihn als Datei und führt `lab.py add sitzung <datei>` aus.
