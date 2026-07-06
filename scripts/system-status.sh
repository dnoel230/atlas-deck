#!/usr/bin/env bash
set -euo pipefail

clear
echo "ATLAS SYSTEM STATUS"
echo "-------------------"
echo "Host: $(hostname)"
echo "User: $(whoami)"
echo "Uptime: $(uptime -p 2>/dev/null || uptime)"
echo
echo "Disk:"
df -h / || true
echo
echo "Memory:"
free -h || true
echo
echo "Network:"
ip -brief addr || true
echo
echo "Tailscale:"
tailscale status 2>/dev/null || echo "Tailscale not connected or not installed."
echo
read -rp "Press Enter to return..."
