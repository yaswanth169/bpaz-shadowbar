# CLI Reference

The `sb` command-line interface is your primary tool for managing ShadowBar agents.

## Commands

### `sb create <name>`

Scaffold a new agent project.

```bash
sb create my-agent
```

### `sb auth <provider>`

Authenticate with an integration provider.

```bash
sb auth microsoft
```

### `sb status`

Check your current ShadowBar configuration and keys.

```bash
sb status
```

### `sb doctor`

Run diagnostics against your environment (Python version, Anthropic connectivity, etc.).

```bash
sb doctor
```
