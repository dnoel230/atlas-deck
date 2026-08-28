#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$BASE_DIR/configs/homelab.env"

clear
echo "ATLAS CONNECTED ENERGY"
echo "-----------------------"

if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
fi

if [[ -z "${HA_URL:-}" || -z "${HA_TOKEN:-}" ]]; then
  echo "Home Assistant is not configured yet."
  echo
  echo "1. cp configs/homelab.env.example configs/homelab.env"
  echo "2. Edit configs/homelab.env and set HA_URL and HA_TOKEN"
  echo "   (HA_TOKEN is a Home Assistant long-lived access token)"
  echo "3. Optionally set HA_ENERGY_ENTITIES to a comma-separated"
  echo "   list of entity IDs to control what shows up here"
  echo
  read -rp "Press Enter to return..."
  exit 0
fi

if ! command -v curl >/dev/null 2>&1 || ! command -v jq >/dev/null 2>&1; then
  echo "This dashboard needs curl and jq. Run ./install.sh first."
  read -rp "Press Enter to return..."
  exit 0
fi

if ! STATES_JSON="$(curl -fsS \
  -H "Authorization: Bearer ${HA_TOKEN}" \
  -H "Content-Type: application/json" \
  "${HA_URL%/}/api/states" 2>/dev/null)"; then
  echo "Could not reach Home Assistant at ${HA_URL}."
  echo "Check that HA_URL and HA_TOKEN in configs/homelab.env are correct"
  echo "and that the host is reachable from this device."
  read -rp "Press Enter to return..."
  exit 0
fi

if [[ -n "${HA_ENERGY_ENTITIES:-}" ]]; then
  IDS_JSON="$(printf '%s\n' "$HA_ENERGY_ENTITIES" | tr ',' '\n' | jq -R . | jq -s .)"
  # shellcheck disable=SC2016
  FILTER='.[] | select(.entity_id as $id | $ids | index($id))'
  ROWS="$(echo "$STATES_JSON" | jq -r --argjson ids "$IDS_JSON" \
    "$FILTER | [.attributes.friendly_name // .entity_id, .state, (.attributes.unit_of_measurement // \"\")] | @tsv")"
else
  FILTER='.[] | select(.attributes.device_class == "power" or .attributes.device_class == "energy")'
  ROWS="$(echo "$STATES_JSON" | jq -r \
    "$FILTER | [.attributes.friendly_name // .entity_id, .state, (.attributes.unit_of_measurement // \"\")] | @tsv")"
fi

if [[ -z "$ROWS" ]]; then
  echo "Connected to Home Assistant, but no power/energy sensors were found."
  echo "Set HA_ENERGY_ENTITIES in configs/homelab.env to choose entities manually."
  read -rp "Press Enter to return..."
  exit 0
fi

printf "%-32s %12s %8s\n" "DEVICE" "READING" "UNIT"
printf "%-32s %12s %8s\n" "------" "-------" "----"

TOTAL_WATTS="0"
while IFS=$'\t' read -r name state unit; do
  printf "%-32s %12s %8s\n" "$name" "$state" "$unit"
  if [[ "$unit" == "W" && "$state" =~ ^-?[0-9]+([.][0-9]+)?$ ]]; then
    TOTAL_WATTS="$(awk -v t="$TOTAL_WATTS" -v s="$state" 'BEGIN { printf "%.2f", t + s }')"
  fi
done <<< "$ROWS"

echo
echo "Total live power draw: ${TOTAL_WATTS} W"
echo
read -rp "Press Enter to return..."
