# ShadowBar

**Barclays Internal AI Agent Framework**

ShadowBar is a Python framework for building collaborative AI agents, powered exclusively by **Anthropic Claude**.

## Quick Start

```bash
# Install
pip install -e .

# Create a new agent project
sb create my-agent
cd my-agent

# Set your Anthropic API key
export ANTHROPIC_API_KEY=your-key-here

# Run the agent
python agent.py
```

## Features

- **Anthropic Claude Integration**: Exclusively uses Claude models (3.5 Sonnet, Haiku, Opus)
- **Function-based Tools**: Python functions automatically become agent tools
- **Event System**: Hook into agent lifecycle (`before_llm`, `after_tool`, etc.)
- **Interactive Debugging**: `@xray` decorator for tool inspection
- **Persistent Memory**: Key-value storage in `.sb/` directory
- **Multi-Agent Networking**: Agents can discover and communicate via relay server

## Basic Usage

```python
from shadowbar import Agent

def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

agent = Agent(
    name="my-agent",
    tools=[search],
    model="claude-sonnet-4-5"  # Default model
)

response = agent.input("Search for Python tutorials")
print(response)
```

## Configuration

ShadowBar uses the `.sb/` directory for configuration:

```
.sb/
├── keys/           # Agent identity keys
│   ├── agent.key   # Ed25519 private key
│   └── recovery.txt # Seed phrase
├── logs/           # Agent logs
└── sessions/       # YAML session files
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Required: Your Anthropic API key |
| `SHADOWBAR_LOG` | Override log directory |
| `SHADOWBAR_RELAY_URL` | Relay server URL (default: `ws://localhost:8000/ws/announce`) |
| `SHADOWBAR_ENV` | Environment (development/staging/production) |

## Supported Models

ShadowBar is optimized for Anthropic Claude 4.5 models:

| Model | Description |
|-------|-------------|
| `claude-sonnet-4-5` | **Default** – Best balance of speed and quality for most agents |
| `claude-haiku-4-5` | Fastest and most cost‑effective; ideal for high‑volume workflows |
| `claude-opus-4-5` | Most capable model when you need maximum reasoning depth |

## Relay Server

ShadowBar includes a minimal relay server for agent-to-agent communication:

```bash
# Install relay dependencies
pip install shadowbar[relay-server]

# Start relay server
uvicorn shadowbar.relay_server:app --host 0.0.0.0 --port 8000
```

## CLI Commands

```bash
sb create <name>     # Create new project
sb init              # Initialize in current directory
sb auth              # Generate agent identity
sb doctor            # Diagnose installation
sb status            # Check agent status
```

## License

Proprietary - Barclays Internal Use Only


