#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGINS_DIR="$BASE_DIR/plugins"

if ! command -v jq >/dev/null 2>&1; then
  echo "The plugin menu needs jq. Run ./install.sh first."
  read -rp "Press Enter to return..."
  exit 0
fi

mapfile -t MANIFESTS < <(find "$PLUGINS_DIR" -mindepth 2 -maxdepth 2 -name "plugin.json" | sort)

if [[ ${#MANIFESTS[@]} -eq 0 ]]; then
  echo "No plugins found under plugins/."
  read -rp "Press Enter to return..."
  exit 0
fi

while true; do
  clear
  echo "ATLAS PLUGINS"
  echo "-------------"
  for i in "${!MANIFESTS[@]}"; do
    name="$(jq -r '.name' "${MANIFESTS[$i]}")"
    description="$(jq -r '.description' "${MANIFESTS[$i]}")"
    printf "%d. %s - %s\n" "$((i + 1))" "$name" "$description"
  done
  echo "0. Back"
  echo
  read -rp "Choose: " choice

  if [[ "$choice" == "0" ]]; then
    exit 0
  fi

  if [[ "$choice" =~ ^[0-9]+$ ]] && (( choice >= 1 && choice <= ${#MANIFESTS[@]} )); then
    manifest="${MANIFESTS[$((choice - 1))]}"
    plugin_dir="$(dirname "$manifest")"
    entrypoint="$(jq -r '.entrypoint' "$manifest")"
    entry_path="$plugin_dir/$entrypoint"
    if [[ -x "$entry_path" ]]; then
      "$entry_path"
    elif [[ -f "$entry_path" ]]; then
      bash "$entry_path"
    else
      echo "Entrypoint not found: $entry_path"
      read -rp "Press Enter..."
    fi
  else
    echo "Invalid option"
    sleep 1
  fi
done
