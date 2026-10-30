#!/usr/bin/env bash
# Zeigt, welche Werkzeuge im Container laufen und ob der Uni-LiteLLM erreichbar ist.
export PATH="$HOME/.local/bin:$PATH"

for cmd in "claude --version" "codex --version" "opencode --version" "qwen --version" \
           "copilot --version" "goose --version" "openhands --version" "agentsview --version" \
           "ccusage --version" "gitleaks version" "gh --version" "node -v" "python3 -V"; do
  out=$($cmd 2>/dev/null | head -1)
  printf '%-22s %s\n' "${cmd%% *}" "${out:-FEHLT}"
done

echo
for var in LITE_LLM_LOCAL_API_KEY LITE_LLM_ACADEMIC_CLOUD_API_KEY; do
  if [ -n "${!var:-}" ]; then echo "$var gesetzt"; else echo "$var FEHLT (docs/setup.md, Schritt 2)"; fi
done

code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 \
  -H "Authorization: Bearer ${LITE_LLM_LOCAL_API_KEY:-}" "${LITE_LLM_BASE_URL:-http://141.19.140.104:4000/v1}/models")
case $code in
  200) echo "Uni-LiteLLM erreichbar" ;;
  000) echo "Uni-LiteLLM nicht erreichbar: VPN an?" ;;
  *)   echo "Uni-LiteLLM antwortet mit HTTP $code: Key prüfen" ;;
esac

echo
echo "Git-Hooks: $(git config core.hooksPath || echo 'nicht gesetzt (git config core.hooksPath .githooks)')"
