# Contributing to Atlas Deck

Thanks for helping improve Atlas Deck.

## Project Goals

Atlas Deck is a portable operations platform for iPad + Raspberry Pi users. It focuses on:

- Mobile productivity
- Homelab management
- Secure remote admin
- AI workstation workflows
- Plugin-based expansion

## How to Contribute

1. Fork the repo.
2. Create a feature branch.
3. Keep changes small and focused.
4. Test scripts locally before opening a pull request.
5. Open a pull request with a clear summary.

## Good First Contributions

- Fix typos in docs
- Improve install instructions
- Add hardware notes
- Add safe homelab utilities
- Build new plugins
- Improve shell script reliability

## Safety Rules

Do not add tools or examples that target systems without permission.

Do not commit:

- SSH keys
- API keys
- Passwords
- Private IP maps
- Client data
- Internal business documents

## Plugin Standards

A plugin should include:

- `plugin.json`
- `README.md`
- One executable script or service entry point
- Clear setup instructions

## Script Style

Use:

```bash
#!/usr/bin/env bash
set -euo pipefail
```

Prefer simple, readable scripts over clever code.
