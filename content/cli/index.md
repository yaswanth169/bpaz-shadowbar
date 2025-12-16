# CLI Reference

The `sb` (ShadowBar) command-line interface is your primary tool for managing agents, authentication, and environments.

## Installation

The CLI is installed automatically with the package.

```bash
pip install shadowbar
```

## Global Flags

*   `--verbose`, `-v`: Enable verbose logging.
*   `--help`: Show help message.

## Commands

### `sb init`

Initialize a new ShadowBar project in the current directory.

```bash
sb init
```

This creates a `.sb` directory and adds necessary configuration files without overwriting your existing code.

### `sb create`

Create a new agent from a template.

```bash
sb create my-agent
```

Options:
*   `--template`: Choose a specific template (default: `basic`).
*   `--interactive`: Run in interactive mode.

### `sb auth`

Manage authentication for various providers.

```bash
sb auth [PROVIDER]
```

See [Authentication](auth.md) for details.

### `sb browser`

Launch a standalone browser session for quick debugging or screenshots.

```bash
sb browser --url https://google.com
```
