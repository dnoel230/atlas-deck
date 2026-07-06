# Atlas Deck Plugins

Plugins are small modules that add features to Atlas Deck.

Each plugin should live in its own folder:

```text
plugins/example-plugin/
├── plugin.json
├── README.md
└── run.sh
```

## Manifest Example

```json
{
  "name": "example-plugin",
  "version": "0.1.0",
  "description": "Example Atlas Deck plugin",
  "entrypoint": "run.sh"
}
```

## Rules

- Keep plugins simple.
- Include setup instructions.
- Do not commit secrets.
- Do not include private data.
- Only manage systems you own or are allowed to manage.
