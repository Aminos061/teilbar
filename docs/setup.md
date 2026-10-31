# Einrichtung (einmal pro Person, ca. 30 Minuten)

Ziel: Alle arbeiten im selben Devcontainer mit denselben Werkzeugversionen. Logins bleiben auf deinem Rechner (Docker-Volumes) und landen nie im Repo.

## 1. Auf deinem Rechner installieren

| Was | Windows | macOS | Linux |
|---|---|---|---|
| Docker | Docker Desktop (mit WSL2) | Docker Desktop oder OrbStack | Docker Engine |
| VS Code + Erweiterung „Dev Containers“ | ja | ja | ja |
| Git | Git for Windows | Xcode-Tools oder Homebrew | Paketmanager |
| VPN der Hochschule | nur für die Uni-Qwen-Modelle nötig | | |

## 2. Uni-Qwen-Keys als Umgebungsvariablen setzen

Die Keys bekommst du vom Kurs. Sie gehören **nie** in eine Datei im Repo.

Windows (PowerShell), danach VS Code komplett schließen und neu öffnen:

```powershell
setx LITE_LLM_LOCAL_API_KEY "<dein-key>"
setx LITE_LLM_ACADEMIC_CLOUD_API_KEY "<dein-key>"
```

macOS/Linux: dieselben zwei Zeilen als `export …` in `~/.zshrc` bzw. `~/.bashrc`, dann VS Code aus dem Terminal mit `code .` starten (sonst sieht VS Code die Variablen nicht).

**Wichtig:** Der LiteLLM-Server (`141.19.140.104:4000`) ist nur im Hochschulnetz oder mit VPN erreichbar. Ohne VPN funktionieren Qwen Code, opencode usw. mit Uni-Qwen nicht. Claude Code, Codex und Copilot laufen über eure Abos und brauchen kein VPN.

## 3. Repo im Container öffnen

Wähle einen der zwei Wege:

| Weg | So geht's | Gut für |
|---|---|---|
| **A: Container-Volume** | VS Code: `F1` → „Dev Containers: Clone Repository in Container Volume…“ → `https://github.com/Aminos061/teilbar` | Du arbeitest nur im Container. Am schnellsten, keine Zeilenende-Probleme. Der Code liegt in einem Docker-Volume, nicht in einem Ordner auf deinem Rechner. |
| **B: Lokaler Ordner** | `git clone https://github.com/Aminos061/teilbar.git` (z. B. nach `C:\Projects\teilbar`), Ordner in VS Code öffnen, `F1` → „Dev Containers: Reopen in Container“ | Du nutzt zusätzlich eine Desktop-App auf deinem Rechner (z. B. Claude Desktop). Container und Rechner arbeiten im selben Ordner: Was ein Agent im Container anlegt, siehst du sofort im Explorer und in der App, und umgekehrt. Dateizugriffe sind unter Windows etwas langsamer. |

### Agenten auf dem Rechner und im Container mischen (Weg B)

Desktop-Apps laufen auf deinem Rechner, nicht im Container. Beispiel Amin: Claude Code über die Claude-Desktop-App unter Windows, opencode mit Uni-Qwen im Container, beide auf `C:\Projects\teilbar`.

- Sitzungen in der App protokollierst du mit `environment: host`. Die Container-Werkzeuge (AgentsView, ccusage) gibt es dort nicht.
- `lab.py` läuft auch auf dem Rechner, wenn Python 3.12 da ist: `pip install -r ai-lab/tools/requirements.txt`.
- Der Container aktiviert die Git-Hooks für den ganzen Ordner. Committest du auch unter Windows, installier dort gitleaks (z. B. über winget), sonst prüft der Hook dort nicht auf Secrets. Die CI prüft jeden PR trotzdem.

Der erste Start dauert einige Minuten (`.devcontainer/install-clis.sh` installiert alle Agenten-CLIs in festen Versionen). Danach im Container-Terminal prüfen:

```bash
bash .devcontainer/check-env.sh
```

## 4. Bei deinen Werkzeugen einloggen (einmal, bleibt über Rebuilds erhalten)

| Werkzeug | Wer | Login im Container |
|---|---|---|
| Claude Code | Sirat, Matias (Amin über die Desktop-App, siehe oben) | `claude` → Link im Browser öffnen → Code ins Terminal einfügen |
| Codex | optional, für Experimente | `codex login --device-auth` (Device-Code muss in den ChatGPT-Sicherheitseinstellungen erlaubt sein) |
| Copilot CLI | Can (Student-Abo) | `copilot` → `/login` → Code auf github.com/login/device eingeben |
| Qwen Code | alle | kein Login; nutzt `LITE_LLM_*` (Konfiguration wird beim ersten Start angelegt) |
| opencode | alle | kein Login für Uni-Qwen; `opencode.json` im Repo verweist auf die Env-Variablen |
| Goose, OpenHands | optional, für Experimente | `goose configure` bzw. `openhands` und dort den Uni-LiteLLM als OpenAI-kompatiblen Endpunkt eintragen |
| GitHub (`gh`) | alle | `gh auth login` (oder VS Code reicht deine Git-Anmeldung durch) |
| Supabase (Cloud) | alle | kein Login im Container: Einladung per E-Mail annehmen (siehe Schritt 6) |

Gemini CLI funktioniert mit dem Gemini-Plus-Studentenpaket nicht (das Paket gilt nur für die Gemini-App, nicht für die API). Gemini nutzt ihr im Browser; Sitzungen dort protokolliert ihr mit dem Prompt aus `ai-lab/README.md#ohne-skill`.

## 5. Prüfen, ob alles läuft

Der Container hat beim ersten Start `npm ci` in `web/` ausgeführt und Docker-in-Docker bereitgestellt. Prüfen:

```bash
bash .devcontainer/check-env.sh    # zeigt auch Docker und die Supabase CLI
docker version                     # Client und Server müssen antworten
```

## 6. App und Supabase

Wie du die App und die lokale Datenbank startest, steht in der [README](../README.md#app-starten). Hier die Einrichtung dahinter.

**Speicher.** Die lokale Supabase startet mehrere Container (Datenbank, Anmeldung, Storage, Studio, Mailpit). Plane für Docker mindestens **8 GB Arbeitsspeicher** ein. Unter Windows stellst du das in `%UserProfile%\.wslconfig` ein (`[wsl2]` → `memory=8GB`, danach `wsl --shutdown`), in Docker Desktop unter *Settings → Resources*. Die Dienste `analytics` und `edge_runtime` sind in `web/supabase/config.toml` aus, um Speicher zu sparen.

**Docker-in-Docker.** Die Supabase CLI braucht Docker. Der Container bringt dafür ein eigenes Docker mit (privilegiert, Images liegen in einem Docker-Volume). Das erste `npm run db:start` lädt einige GB, danach geht es schnell. Nach einer Änderung an `.devcontainer/` den Container neu bauen: `F1` → „Dev Containers: Rebuild Container“.

**Cloud-Projekt.** Das gemeinsame Supabase-Projekt (kostenloser Tarif, EU-Region) gehört einer Organisation, in die dich eine Person mit Owner-Rolle per E-Mail einlädt:

1. Der Owner öffnet im Supabase-Dashboard die Organisation → *Team* → *Invite* und trägt deine E-Mail-Adresse ein. Rolle für uns: *Developer*.
2. Du nimmst die Einladung in der E-Mail an. Sie gilt **24 Stunden**; danach lässt der Owner sie erneut senden.
3. Project URL und Publishable Key stehen im Dashboard unter *Project Settings → API*. Kopiere `web/.env.example` nach `web/.env.local` und trage sie ein.

Zugriff aufs Projekt zeigt auch die geheimen Keys. Gib sie nie weiter und committe nie eine `.env.local`. Migrationen laufen nur nach dem Merge auf `main` gegen die Cloud (ADR 0007). Keys für die CI oder ein Deployment kommen als GitHub-Secrets, sobald das Hosting entschieden ist.

## 7. Fertig. Was jetzt?

- Wie wir zusammenarbeiten: [CONTRIBUTING.md](../CONTRIBUTING.md)
- KI-Labor: [ai-lab/README.md](../ai-lab/README.md)

## Probleme

| Symptom | Lösung |
|---|---|
| `bash\r: bad interpreter` | Repo wurde mit Windows-Zeilenenden geklont. Im Ordner `git add --renormalize .` ausführen oder Weg A nehmen (Schritt 3) |
| Qwen: `401` oder „No api key“ | Variable fehlt im Container: `echo $LITE_LLM_LOCAL_API_KEY` (zeigt den Key, also nicht bei Bildschirmfreigabe). Nach `setx` VS Code komplett neu starten, Container neu bauen |
| Qwen: Timeout | VPN an? Test: `curl -s http://141.19.140.104:4000/v1/models -H "Authorization: Bearer $LITE_LLM_LOCAL_API_KEY" \| head` |
| Login-Seite leitet auf `localhost` um und scheitert | URL aus dem Terminal kopieren, im Browser öffnen, den angezeigten Code zurück ins Terminal einfügen |
| Commit wird von gitleaks blockiert | Da steht vermutlich wirklich ein Key. Entfernen. Echter Fehlalarm: Zeile mit `gitleaks:allow` markieren |
| `docker version` meldet „Cannot connect“ im Container | Docker-in-Docker läuft nicht. Container neu bauen („Dev Containers: Rebuild Container“). Läuft Docker Desktop nicht oder ist „privileged“ gesperrt, startet das Feature nicht |
| `npm run db:start` bricht ab oder hängt | Meist zu wenig Speicher (Schritt 6) oder ein Port ist belegt (54321–54324). `npm run db:stop`, Speicher erhöhen, noch einmal starten |
| App meldet „NEXT_PUBLIC_SUPABASE_URL … fehlen“ | `web/.env.local` fehlt oder ist leer. `cp web/.env.example web/.env.local` und Werte aus `npm run db:status` eintragen |
| `docker compose up` erreicht die Datenbank nicht | `npm run db:start` in `web/` zuerst ausführen. `network_mode: host` gilt nur im Devcontainer, nicht auf dem Host unter Windows oder macOS |
