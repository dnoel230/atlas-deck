#!/usr/bin/env bash
set -euo pipefail

while true; do
  clear
  echo "ATLAS HOMELAB"
  echo "-------------"
  echo "1. SSH to Raspberry Pi 5"
  echo "2. SSH to Orange Pi Zero 3"
  echo "3. Open Home Assistant URL note"
  echo "4. Open Pi-hole URL note"
  echo "5. Show local network info"
  echo "0. Back"
  echo
  read -rp "Choose: " choice

  case "$choice" in
    1) ssh pi5 || true ;;
    2) ssh orangepi || true ;;
    3) echo "Set your Home Assistant URL in configs/homelab.env"; read -rp "Press Enter..." ;;
    4) echo "Set your Pi-hole URL in configs/homelab.env"; read -rp "Press Enter..." ;;
    5) ip route; echo; ip -brief addr; read -rp "Press Enter..." ;;
    0) exit 0 ;;
    *) echo "Invalid option"; sleep 1 ;;
  esac
done
