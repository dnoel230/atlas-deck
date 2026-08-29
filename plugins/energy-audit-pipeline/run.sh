#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$BASE_DIR/config.env"

if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "This plugin needs python3. Run ./install.sh first."
  read -rp "Press Enter to return..."
  exit 0
fi

exec python3 "$BASE_DIR/src/cli.py"
