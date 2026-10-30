#!/usr/bin/env bash
# Installiert die Agenten-CLIs in festen Versionen (Begründung: docs/adr/0003-ein-devcontainer.md).
# Neue Version = Pull Request, der nur diese Zeilen ändert. Ein fehlgeschlagenes Werkzeug bricht den Rest nicht ab.
set -u

CLAUDE_CODE=2.1.314
CODEX=0.166.0
OPENCODE=1.19.5
QWEN_CODE=0.26.4
COPILOT=1.0.105
CCUSAGE=20.0.45
GOOSE=v1.57.0
OPENHANDS=1.16.0
GITLEAKS=8.30.1

failed=()
step() { local name=$1; shift; echo "==> $name"; "$@" || failed+=("$name"); }

case "$(uname -m)" in
  x86_64)  GL_ARCH=x64;   GOOSE_ARCH=x86_64 ;;
  aarch64|arm64) GL_ARCH=arm64; GOOSE_ARCH=aarch64 ;;
  *) echo "Unbekannte Architektur $(uname -m)"; GL_ARCH=x64; GOOSE_ARCH=x86_64 ;;
esac

# Volumes gehören beim ersten Anlegen root.
sudo chown -R "$(id -u):$(id -g)" ~/.claude ~/.codex ~/.copilot ~/.qwen ~/.openhands \
  ~/.local/share/opencode ~/.config/goose ~/.agentsview 2>/dev/null || true

step "npm-CLIs" npm install -g \
  "@anthropic-ai/claude-code@$CLAUDE_CODE" \
  "@openai/codex@$CODEX" \
  "opencode-ai@$OPENCODE" \
  "@qwen-code/qwen-code@$QWEN_CODE" \
  "@github/copilot@$COPILOT" \
  "ccusage@$CCUSAGE"

step "uv" bash -c 'command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh'
export PATH="$HOME/.local/bin:$PATH"
step "OpenHands" uv tool install "openhands==$OPENHANDS" --python 3.12

step "Goose" bash -c "curl -fsSL https://github.com/aaif-goose/goose/releases/download/$GOOSE/goose-$GOOSE_ARCH-unknown-linux-gnu.tar.gz \
  | tar -xz -C /tmp && install -m 755 \$(find /tmp -maxdepth 2 -name goose -type f | head -1) $HOME/.local/bin/goose"

step "gitleaks" bash -c "curl -fsSL https://github.com/gitleaks/gitleaks/releases/download/v$GITLEAKS/gitleaks_${GITLEAKS}_linux_$GL_ARCH.tar.gz \
  | tar -xz -C /tmp gitleaks && install -m 755 /tmp/gitleaks $HOME/.local/bin/gitleaks"

# AgentsView bietet nur ein Installskript ohne Versions-Pin (Stand 2026-10-30). Telemetrie ist per containerEnv aus.
step "AgentsView" bash -c 'curl -fsSL https://agentsview.io/install.sh | bash'

step "Python-Pakete (ai-lab)" python3 -m pip install --user -q -r ai-lab/tools/requirements.txt

# Qwen Code auf den Uni-LiteLLM einstellen, falls noch keine eigene Konfiguration existiert.
if [ ! -f ~/.qwen/settings.json ]; then
  mkdir -p ~/.qwen
  cat > ~/.qwen/settings.json <<'JSON'
{
  "modelProviders": {
    "openai": [
      { "id": "qwen3.8:27b", "name": "Qwen3.8 27B (Uni, lokal)",
        "envKey": "LITE_LLM_LOCAL_API_KEY", "baseUrl": "http://141.19.140.104:4000/v1" },
      { "id": "qwen3.8:27b-academic", "name": "Qwen3.8 27B (Uni, academic cloud)",
        "envKey": "LITE_LLM_ACADEMIC_CLOUD_API_KEY", "baseUrl": "http://141.19.140.104:4000/v1" }
    ]
  },
  "security": { "auth": { "selectedType": "openai" } },
  "model": { "name": "qwen3.8:27b" }
}
JSON
fi

git config core.hooksPath .githooks

echo
if [ ${#failed[@]} -eq 0 ]; then
  echo "Alles installiert. Test: bash .devcontainer/check-env.sh"
else
  echo "Fehlgeschlagen: ${failed[*]}. Container läuft trotzdem; bitte im Team melden."
fi
