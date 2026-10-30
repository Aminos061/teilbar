# Felder des Sitzungsprotokolls

Schema: `ai-lab/schema/sitzung.schema.json`. Feldnamen sind Englisch, Inhalte Deutsch (ADR 0005). Eine leere Vorlage gibt `lab.py vorlage sitzung` aus.

## Werte mit fester Liste

| Feld | Werte |
|---|---|
| `person` | amin · matias · sirat · can |
| `phases` | Recherche · Anforderung · Design · Planung · Implementierung · Test · Review · Deployment · Doku · Organisation (mehrere möglich) |
| `config.harness` | claude-code · codex · opencode · qwen-code · copilot-cli · goose · openhands · gemini-cli · jcode · cline · claude-web · chatgpt-web · gemini-web · andere |
| `config.environment` | devcontainer (Standard) · host (z. B. Claude-Desktop-App) · web |
| `work_mode` | `autonom` = Ziel vorgegeben, Agent arbeitet allein · `iterativ` = gemeinsam geplant, viele kleine Schritte · `gemischt` |
| `outcome` | erfolgreich · teilweise · gescheitert · abgebrochen |
| `first_try` | `ja` · `nachgebessert` (Person oder Agent musste korrigieren) · `verworfen` |

## Modell, Effort und Tokens je Harness

| Harness | Modell und Effort | Tokens |
|---|---|---|
| claude-code | Modell steht in deinem Kontext bzw. in `/model`; Effort in `/effort` | `lab.py tokens --harness claude-code` (liest das Transkript der neuesten Sitzung im Projekt) |
| codex | `/status`; Effort = `model_reasoning_effort` | `lab.py tokens --harness codex` (liest den neuesten Rollout) |
| opencode | Modell in der Statuszeile bzw. `opencode.json` | `opencode stats` oder `agentsview session usage <id> --format json` |
| qwen-code | `/model` | `/stats model` (die Person kopiert die Zahlen) |
| copilot-cli | `/model` (Student-Abo: oft automatisch, dann „auto“) | `/usage` (Tokens je Modell) |
| goose, openhands | Konfiguration bzw. Umgebungsvariablen (`GOOSE_MODEL`, `LLM_MODEL`) | `agentsview session usage <id> --format json` |
| Web-Chats | was die Oberfläche anzeigt | `source: unbekannt` |

Gegenprobe: `ccusage session --json` für Claude Code, Codex, opencode, Copilot, Goose und Qwen Code. Weichen die Zahlen deutlich ab, notier das im Text.

## Zeiten

- `minutes.agent`: wie lange der Agent ungefähr gearbeitet hat
- `minutes.human`: Zeit der Person für Prompts, Warten und Prüfen
- `minutes.rework`: Nacharbeit von Hand, auch nach der Sitzung (gegebenenfalls später nachtragen)

## Textfelder

| Feld | Inhalt |
|---|---|
| `goal` | Ziel und Kontext in 2–4 Sätzen. Projektkontext nur, wenn er für die Bewertung zählt („erste Datei im leeren Repo“) |
| `prompts` | die 1–3 entscheidenden Prompts wörtlich; nur wenn nicht mehr bekannt mit „sinngemäß:“ davor |
| `agent_plan` | deine Schrittliste, wie sie war; Abweichungen markieren |
| `result` | was herauskam, was nachgebessert oder verworfen wurde |
| `went_well`, `went_badly` | konkrete Belege („Test X schlug fehl, weil …“) statt Bewertungen |
