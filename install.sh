#!/usr/bin/env bash
set -euo pipefail

echo "Atlas Deck installer"
echo "--------------------"

sudo apt update
sudo apt upgrade -y

sudo apt install -y \
  git curl wget vim nano tmux htop btop \
  python3 python3-pip python3-venv \
  nmap dnsutils net-tools iproute2 \
  openssh-server ufw jq fzf ripgrep ranger \
  ca-certificates gnupg lsb-release

if ! command -v tailscale >/dev/null 2>&1; then
  curl -fsSL https://tailscale.com/install.sh | sh
fi

mkdir -p "$HOME/atlas-notes" "$HOME/atlas-backups"
chmod +x atlas-menu.sh scripts/*.sh 2>/dev/null || true

echo
echo "Base install complete."
echo "Next steps:"
echo "1. sudo tailscale up"
echo "2. ./atlas-menu.sh"
