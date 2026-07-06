#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

run_script() {
  local script="$1"
  if [[ -x "$BASE_DIR/$script" ]]; then
    "$BASE_DIR/$script"
  else
    bash "$BASE_DIR/$script"
  fi
}

while true; do
  clear
  echo "=============================="
  echo "          ATLAS DECK"
  echo "=============================="
  echo "1. System Status"
  echo "2. Homelab"
  echo "3. AI Server / Pi 5"
  echo "4. Nexus Workspace"
  echo "5. Market Brief"
  echo "6. Notes"
  echo "7. Files"
  echo "8. Update Atlas Deck"
  echo "0. Exit"
  echo
  read -rp "Choose: " choice

  case "$choice" in
    1) run_script "scripts/system-status.sh" ;;
    2) run_script "scripts/homelab-menu.sh" ;;
    3) ssh pi5 || true ;;
    4) run_script "scripts/nexus-menu.sh" ;;
    5) run_script "scripts/market-brief.sh" ;;
    6) mkdir -p "$HOME/atlas-notes" && nano "$HOME/atlas-notes/today.md" ;;
    7) ranger "$HOME" || ls -la "$HOME" ; read -rp "Press Enter..." ;;
    8) git -C "$BASE_DIR" pull --ff-only || true ; read -rp "Press Enter..." ;;
    0) exit 0 ;;
    *) echo "Invalid option"; sleep 1 ;;
  esac
done
