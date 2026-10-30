# KI-Labor

Hier hält das Team fest, wie es KI-Agenten bei der Entwicklung von Teilbar einsetzt, und prüft in kleinen Experimenten, was davon wirklich hilft. Am Semesterende entsteht daraus ein Bericht mit belegten Do's und Don'ts. Warum es so aufgebaut ist: [ADR 0001](../docs/adr/0001-ki-labor-im-app-repo.md), [0005](../docs/adr/0005-daten-des-labors.md), [0006](../docs/adr/0006-vom-kandidaten-zum-befund.md). Begriffe: [GLOSSARY.md](../GLOSSARY.md).

## Ich will …

| … | So geht's |
|---|---|
| eine Sitzung protokollieren | Dem Agenten sagen: **„Sitzung protokollieren“**. In Claude Code geht auch `/sitzung-protokollieren`. Ohne Skill-Unterstützung: Prompt [unten](#ohne-skill) |
| wissen, was gerade offen ist | `python ai-lab/tools/lab.py stand` |
| ein Repo, Framework oder Tool ausprobieren | Dem Agenten sagen: **„Ich will <Quelle> sichten“**. Er klärt das Ziel, zeigt die Bestandteile und hält mit dir Kandidaten fest. Installiert wird erst im Experiment. |
| sehen, welche Ideen auf einen Test warten | `python ai-lab/tools/lab.py kandidaten` |
| einen Eintrag ansehen | `python ai-lab/tools/lab.py zeige H12` (oder eine Sitzungs-, Kandidaten-, Experiment-ID) |
| das Lab-Review im Meeting machen | Bildschirm mit einer Agenten-Sitzung teilen und sagen: **„Wir machen das Lab-Review“**. Der Agent führt durch die Punkte und trägt die Entscheidungen live ein. |
| eine Hypothese anlegen | Im Lab-Review aus einem Kandidaten auswählen, dann dem Agenten sagen: „Leg H<n> aus Kandidat … an“ |
| ein Experiment machen | Dem Agenten sagen: „Plane ein Experiment zu H<n>“ (Skill `ki-labor`) |
| einen Zwischenbericht | `python ai-lab/tools/lab.py bericht` |
| prüfen, ob alles gültig ist | `python ai-lab/tools/lab.py check` |

Einmal vorher: `pip install -r ai-lab/tools/requirements.txt` (im Devcontainer schon erledigt).

## Woher Hypothesen kommen

```text
Sitzung ───────────┐
  (Beobachtung)     │
                    ├─► Kandidat ──► Lab-Review wählt ──► Hypothese ──► Experiment ──► Befund
Sichtung einer ─────┘   neu           (max. 5 offen)        H<n>           E<n>          k von n
  Quelle (Repo, Studie)
```

Eine Quelle wie Superpowers oder ein Cookbook liefert Behauptungen. Wissen für unser Projekt wird daraus erst, wenn ein Experiment sie an unseren Aufgaben prüft. Das Lab-Review (10 Minuten im Wochenmeeting) entscheidet, was getestet wird. Die verantwortliche Person stellt das Experiment auf, eine andere Person bewertet blind.

## Was wo liegt

Alles ist Daten, keine Dokumente: ein JSON-Datensatz pro Zeile, geprüft gegen ein Schema.

| Datei | Inhalt |
|---|---|
| `daten/sitzungen/<person>.jsonl` | Sitzungsprotokolle, eine Datei pro Person |
| `daten/sichtungen.jsonl` | gesichtete Quellen: was sie versprechen, was wir nicht übernehmen |
| `daten/kandidaten.jsonl` | testbare Ideen aus Sitzungen und Sichtungen |
| `daten/hypothesen.jsonl` | Hypothesen `H<issue>` mit Status, Belegstufe und Log |
| `daten/experimente.jsonl` | Experimente `E<issue>`: Variable, Konfigurationen, Auftrag, Entscheidungsregel, Befund |
| `daten/laeufe.jsonl` | einzelne Läufe `E<n>/A1` mit Zahlen und blinder Bewertung |
| `schema/` | Felder und erlaubte Werte |
| `preise.yaml` | Preise für den Schattenpreis (was die Sitzung über die API gekostet hätte) |
| `tools/lab.py` | das einzige Werkzeug zum Lesen und Ändern |
| `berichte/` | erzeugte Berichte |

Ändern nur über `lab.py` (`vorlage`, `add`, `set`, `log`), damit Schema und Verweise stimmen. Bei einem Merge-Konflikt in einer `.jsonl`: `main` lokal in deinen Branch mergen, beide Zeilen behalten, `lab.py check`.

## Verwendete Fremdwerkzeuge

| Werkzeug | Wofür | Lizenz | Gebaut für |
|---|---|---|---|
| [AgentsView](https://github.com/wesm/agentsview) | Tokenzahlen aus lokalen Transkripten | MIT | alle unsere Harnesses |
| [ccusage](https://github.com/ryoppippi/ccusage) | Gegenprobe der Tokenzahlen | MIT | alle außer OpenHands |
| [gitleaks](https://github.com/gitleaks/gitleaks) | Secret-Scan vor Commit und in CI | MIT | unabhängig |
| [Agent Skills](https://agentskills.io) (Format) | Skills in `.agents/skills/` | offen | alle außer Claude Code (Kopie in `.claude/skills/`) |
| Ideen aus [mattpocock/skills](https://github.com/mattpocock/skills), [obra/superpowers](https://github.com/obra/superpowers) | nur als Kandidaten, nicht installiert | MIT | portabel |

## Ohne Skill

Für Web-Chats oder Harnesses ohne Skills diesen Prompt am Ende der Sitzung einfügen:

```text
Schreib ein Sitzungsprotokoll über diese Sitzung für unser KI-Labor, als EIN JSON-Objekt nach dem Schema
https://github.com/Aminos061/teilbar/blob/main/ai-lab/schema/sitzung.schema.json
Feldwerte laut https://github.com/Aminos061/teilbar/blob/main/.agents/skills/sitzung-protokollieren/felder.md.
Erfinde nichts; was du nicht weißt, ist null. Zitiere die wichtigsten Prompts wörtlich. Schwärze Keys, Tokens
und private Daten mit [GESCHWÄRZT]. Frag mich in EINER Nachricht nach Person, Ergebnis, Menschenzeit,
Nacharbeit und Zufriedenheit 1–5, jeweils mit deinem Vorschlag. Gib dann das JSON als einen Codeblock aus.
```

Das JSON als Datei speichern (außerhalb des Repos), dann `python ai-lab/tools/lab.py add sitzung <datei>` und `python ai-lab/tools/lab.py check`.
