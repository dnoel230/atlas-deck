# Atlas Deck

> **Private AI. Modular Infrastructure. Your Hardware.**

Atlas Deck is an open-source platform for building a private, AI-powered workspace using the hardware you already own.

Instead of replacing your devices, Atlas Deck connects them into one secure, modular ecosystem where you can manage infrastructure, automate workflows, develop software, and run local AI—all while keeping your data under your control.

Whether you're a homelab enthusiast, developer, student, or privacy-conscious user, Atlas Deck gives you a foundation to build on.

---

# Vision

Atlas Deck aims to become the operating platform for personal infrastructure.

Imagine connecting your Raspberry Pi, desktop, NAS, edge devices, and tablet into one cohesive workspace that is:

- Privacy-first
- AI-native
- Self-hosted
- Modular
- Cross-platform
- Community-driven

No vendor lock-in.

No required cloud services.

Your hardware. Your data. Your rules.

---

# Why Atlas Deck?

Today's tools solve individual problems.

- One application manages Docker.
- Another manages Home Assistant.
- Another provides remote access.
- Another hosts local AI.

Atlas Deck brings these capabilities together into a single extensible platform.

Instead of managing separate tools, Atlas provides one interface for your personal infrastructure.

---

# Core Principles

- Privacy First
- Local AI
- Self-Hosted by Default
- Modular Plugin Architecture
- Hardware Agnostic
- Open Source
- Community Driven

---

# Current Features

- Terminal dashboard
- Automated installation
- Raspberry Pi support
- Homelab management
- Secure SSH workflows
- Tailscale integration
- Plugin framework (in development)
- GitHub-based development workflow

---

# Roadmap

### v0.1
- Terminal interface
- Installer
- System monitoring
- SSH management
- Homelab utilities

### v0.2
- Plugin manager
- Hardware detection
- Configuration system

### v0.3
- Web dashboard
- iPad-optimized interface
- Mobile-first design

### v0.4
- Docker management
- Service monitoring
- Plugin marketplace

### v1.0
- Stable releases
- Complete documentation
- Cross-platform support
- Community plugin ecosystem

---

# Supported Hardware

Atlas Deck is designed to run on inexpensive, commonly available hardware.

Current targets include:

- Raspberry Pi Zero 2 W
- Raspberry Pi 5
- Orange Pi
- Windows
- Linux
- macOS

Primary mobile interface:

- iPad Pro
- External keyboard support

Future hardware support will continue expanding while maintaining a common user experience.

---

# Project Architecture

```
                iPad / Tablet
                       │
                Atlas Dashboard
                       │
              Edge Computing Node
             (Pi Zero / Mini PC)
                       │
        ┌──────────────┼──────────────┐
        │              │              │
    AI Services     Home Lab      Automation
        │              │              │
        └──────────────┼──────────────┘
                       │
              Private Infrastructure
```

---

# Quick Start

```bash
git clone https://github.com/dnoel230/atlas-deck.git

cd atlas-deck

chmod +x install.sh atlas-menu.sh scripts/*.sh

./install.sh

./atlas-menu.sh
```

---

# Contributing

Atlas Deck is an open-source community project.

Whether you write code, improve documentation, test hardware, design interfaces, or build plugins, contributions are welcome.

See:

- CONTRIBUTING.md
- SECURITY.md
- CODE_OF_CONDUCT.md

---

# Security

Atlas Deck is designed for systems you own or are authorized to manage.

Please never commit:

- API keys
- Passwords
- SSH keys
- Client information
- Sensitive business data

---

# License

License to be announced before the first stable release.

---

# Join the Project

Atlas Deck is just getting started.

If you're interested in privacy, Raspberry Pi, edge computing, homelabs, local AI, or open-source infrastructure, we'd love your help.

⭐ Star the repository

🐛 Report issues

💡 Suggest ideas

🔧 Build plugins

🚀 Help shape the future of Atlas Deck.