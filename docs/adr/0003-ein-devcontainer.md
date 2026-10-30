# 0003 Ein Devcontainer für alle

Status: angenommen · 2026-10-30

## Kontext

Vier Rechner (Windows, macOS), sieben Agenten-CLIs. Wenn wir Konfigurationen vergleichen, darf sich zwischen zwei Läufen nur die Konfiguration unterscheiden, nicht die Umgebung. Der Tech-Stack der App ist noch offen.

## Entscheidung

- Ein gemeinsamer Devcontainer (`.devcontainer/`): Ubuntu, Node 24, Python 3.12, alle Agenten-CLIs in festen Versionen (`install-clis.sh`), Auto-Update aus.
- Logins (Claude, Codex, Copilot) liegen in benannten Docker-Volumes auf dem eigenen Rechner. Uni-Qwen-Keys kommen als Host-Variablen mit den Kurs-Namen in den Container.
- `.gitattributes` mit `eol=lf`. Unter Windows wird das Repo per „Clone in Container Volume“ geöffnet.
- Vertrag für die App, egal welcher Stack: `docker compose up` startet sie, entwickelt wird im Devcontainer. Den Stack entscheidet ein eigenes ADR.
- Desktop-Apps auf dem Host sind erlaubt. Die Sitzung vermerkt dann `environment: host`.

## Folgen

Versionswechsel gehen nur per PR auf `install-clis.sh`. Der erste Containerstart dauert einige Minuten.

## Quellen

- Claude Code im Devcontainer: https://code.claude.com/docs/en/devcontainer
- Dev-Container-Performance unter Windows: https://code.visualstudio.com/remote/advancedcontainers/improve-performance
