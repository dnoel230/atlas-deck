           iPad Pro
               │
        Atlas Dashboard
               │
      Raspberry Pi Zero 2 W
               │
     ┌─────────┴─────────┐
     │                   │
 Raspberry Pi 5      Orange Pi
 AI • Docker          Network
     │                   │
     └─────────┬─────────┘
               │
        Your Home Network

README Introduction

Atlas Deck

Atlas Deck is an open-source, modular platform for building a private, AI-powered workspace using hardware you already own.

Whether you’re managing a homelab, developing software, learning Linux, or running local AI models, Atlas Deck provides a unified interface to connect your devices, automate workflows, and stay in control of your data.

Instead of replacing your hardware, Atlas Deck extends it.

It supports Raspberry Pi, Orange Pi, Windows, Linux, macOS, and iPad-based workflows while remaining privacy-first and self-hosted by design.

Vision

Our goal is simple:

Build a private, modular operating platform for personal infrastructure.

Atlas Deck connects your devices into one ecosystem where AI, automation, networking, storage, and development tools work together through a common interface.

Core Principles

* Privacy First
* Local AI
* Self-Hosted
* Modular Plugins
* Hardware Agnostic
* Open Source
* Community Driven

Current Features

* Terminal dashboard
* Raspberry Pi support
* Homelab management
* Tailscale integration
* SSH management
* Plugin architecture (in development)
* Automated installation
* GitHub-based development workflow

Planned Features

* Web dashboard optimized for iPad
* Plugin marketplace
* Local AI integration
* Docker management
* Home Assistant integration
* Documentation server
* Mobile-first interface
* Cross-platform support

Supported Hardware

* Raspberry Pi Zero 2 W
* Raspberry Pi 5
* Orange Pi
* Windows PCs
* Linux
* macOS
* iPad Pro (primary mobile interface)

Why Atlas Deck?

Many tools solve one problem well—home automation, containers, remote access, or local AI—but they often exist in separate ecosystems.

Atlas Deck aims to bring these capabilities together into a cohesive, extensible platform. It gives you one place to manage your devices, services, and workflows while keeping your data under your control.

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
