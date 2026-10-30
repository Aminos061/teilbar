# 0002 Zusammenarbeit über GitHub

Status: angenommen · 2026-10-30

## Kontext

Aufgaben lagen in Notion ohne festen Prozess, Absprachen in WhatsApp und Discord. Agenten sollen Aufgaben lesen und verlinken können, und die Kette von der Aufgabe bis zum Merge soll nachvollziehbar sein.

## Entscheidung

- **Aufgaben** sind GitHub Issues auf einem GitHub Project. Notion wird nach dem Umzug eingefroren.
- **GitHub Flow:** `main` ist geschützt. Pro Aufgabe ein Branch `<issue-nr>-<kurzname>`, PR mit Review durch eine andere Person, Squash-Merge.
- **Repo** bleibt unter `Aminos061`, die anderen drei sind Collaborators. Keine Organisation, weil sich sonst die Pages-Adresse ändert und Links in der CA1 und der QR-Code brechen.
- **Rollen:** Amin ist Lab-Lead. Haupt-Konfigurationen: Amin Claude Code (korrigiert am 30.10.2026, Codex nutzt er nicht), Sirat Claude Code, Matias Claude Code, Can Qwen Code mit Uni-Qwen und Copilot CLI. Alle nutzen zusätzlich ihren Kurs-Harness mit Uni-Qwen (Amin opencode, Sirat OpenHands, Matias Goose). Gemini nur im Browser, die Gemini CLI geht mit dem Studentenpaket nicht.
- **Rhythmus:** ein Discord-Meeting pro Woche mit 10 Minuten Lab-Review. Ergebnisse landen dort, wo sie hingehören: Aufgaben als Issue, Entscheidungen als ADR, Laborstand über `lab.py`. Es gibt keine eigenen Meeting-Notizen.

## Folgen

Agenten erreichen Issues über `gh`. Die Haupt-Konfigurationen ergeben von selbst die Vergleiche Frontier gegen Open-Weight und Harness gegen Harness.
