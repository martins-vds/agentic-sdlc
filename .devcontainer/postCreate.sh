#!/usr/bin/env bash
set -euo pipefail

export PATH="$HOME/.local/bin:$PATH"

if ! command -v copilot >/dev/null 2>&1; then
  echo "Installing GitHub Copilot CLI..."
  curl -fsSL https://gh.io/copilot-install | PREFIX="$HOME/.local" bash
fi

copilot --version
python3 -m pip install --user --quiet -r requirements-dev.txt

if ! grep -q '# COPILOT_CLI_PATH' "$HOME/.bashrc"; then
  {
    echo
    echo '# COPILOT_CLI_PATH'
    echo 'export PATH="$HOME/.local/bin:$PATH"'
  } >> "$HOME/.bashrc"
fi

chmod +x scripts/validate_workshop.sh scripts/run_multi_agent.sh \
  scripts/project_pulse/validate_exercise.py
./scripts/validate_workshop.sh

cat <<'MESSAGE'

Workshop setup complete.
For the Project Pulse custom-agent lab, open:
  labs/04-multi-agent/project-pulse/README.md
Then start GitHub Copilot CLI with:
  copilot
MESSAGE
