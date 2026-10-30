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

- **Windows/macOS (empfohlen):** In VS Code `F1` → „Dev Containers: Clone Repository in Container Volume…“ → `https://github.com/Aminos061/teilbar`. Das ist deutlich schneller als ein Ordner auf der Windows-Festplatte und vermeidet Zeilenende-Probleme.
- **Linux, oder wenn du lieber lokal klonst:** `git clone`, Ordner in VS Code öffnen, „Reopen in Container“.

Der erste Start dauert einige Minuten (`.devcontainer/install-clis.sh` installiert alle Agenten-CLIs in festen Versionen). Danach im Container-Terminal prüfen:

```bash
bash .devcontainer/check-env.sh
```

## 4. Bei deinen Werkzeugen einloggen (einmal, bleibt über Rebuilds erhalten)

| Werkzeug | Wer | Login im Container |
|---|---|---|
| Claude Code | Amin, Sirat, Matias | `claude` → Link im Browser öffnen → Code ins Terminal einfügen |
| Codex | Amin | `codex login --device-auth` (Device-Code muss in den ChatGPT-Sicherheitseinstellungen erlaubt sein) |
| Copilot CLI | Can (Student-Abo) | `copilot` → `/login` → Code auf github.com/login/device eingeben |
| Qwen Code | alle | kein Login; nutzt `LITE_LLM_*` (Konfiguration wird beim ersten Start angelegt) |
| opencode | alle | kein Login für Uni-Qwen; `opencode.json` im Repo verweist auf die Env-Variablen |
| Goose, OpenHands | optional, für Experimente | `goose configure` bzw. `openhands` und dort den Uni-LiteLLM als OpenAI-kompatiblen Endpunkt eintragen |
| GitHub (`gh`) | alle | `gh auth login` (oder VS Code reicht deine Git-Anmeldung durch) |

Gemini CLI funktioniert mit dem Gemini-Plus-Studentenpaket nicht (das Paket gilt nur für die Gemini-App, nicht für die API). Gemini nutzt ihr im Browser; Sitzungen dort protokolliert ihr mit dem Prompt aus `ai-lab/README.md#ohne-skill`.

## 5. Fertig. Was jetzt?

- Wie wir zusammenarbeiten: [CONTRIBUTING.md](../CONTRIBUTING.md)
- KI-Labor: [ai-lab/README.md](../ai-lab/README.md)

## Probleme

| Symptom | Lösung |
|---|---|
| `bash\r: bad interpreter` | Repo wurde mit Windows-Zeilenenden geklont. In einem Container-Volume neu klonen (Schritt 3) oder `git add --renormalize .` |
| Qwen: `401` oder „No api key“ | Variable fehlt im Container: `echo $LITE_LLM_LOCAL_API_KEY` (zeigt den Key, also nicht bei Bildschirmfreigabe). Nach `setx` VS Code komplett neu starten, Container neu bauen |
| Qwen: Timeout | VPN an? Test: `curl -s http://141.19.140.104:4000/v1/models -H "Authorization: Bearer $LITE_LLM_LOCAL_API_KEY" \| head` |
| Login-Seite leitet auf `localhost` um und scheitert | URL aus dem Terminal kopieren, im Browser öffnen, den angezeigten Code zurück ins Terminal einfügen |
| Commit wird von gitleaks blockiert | Da steht vermutlich wirklich ein Key. Entfernen. Echter Fehlalarm: Zeile mit `gitleaks:allow` markieren |
