# Atlas Deck

Portable iPad + Raspberry Pi command deck for homelab, AI, productivity, and secure remote admin.

## Purpose

Atlas Deck turns an iPad Pro, Raspberry Pi Zero 2 W, Raspberry Pi 5, Orange Pi Zero 3, and a Windows laptop into one connected mobile workstation.

## Hardware Roles

| Device | Role |
| --- | --- |
| iPad Pro + keyboard | Main mobile interface |
| Raspberry Pi Zero 2 W | Portable Linux node |
| Raspberry Pi 5 | Home server, AI, Docker, storage |
| Orange Pi Zero 3 | DNS, VPN, monitoring |
| Windows laptop | Development and testing workstation |

## Features v0.1

- One-command base install
- Terminal dashboard
- Homelab shortcuts
- Pi 5 SSH shortcut
- Orange Pi admin shortcut
- Notes folder
- Tailscale setup guide
- Market brief placeholder
- Nexus project menu placeholder

## Quick Start

```bash
git clone https://github.com/dnoel230/atlas-deck.git
cd atlas-deck
chmod +x install.sh atlas-menu.sh scripts/*.sh
./install.sh
./atlas-menu.sh
```

## Recommended iPad Apps

- Blink Shell
- Termius
- Tailscale
- Working Copy
- GitHub
- Files
- Obsidian or Apple Notes

## Security Note

Keep private IPs, SSH keys, API keys, client data, and internal business documents out of this public repo.
