# Anthropic Integration

ShadowBar is optimized for Anthropic's Claude models, which offer superior reasoning and coding capabilities.

## Supported Models

| Model | ID | Best For |
| :--- | :--- | :--- |
| **Claude 3.5 Sonnet** | `claude-3-5-sonnet-20241022` | The default. Best balance of speed and intelligence. |
| **Claude 3 Haiku** | `claude-3-haiku-20240307` | Extremely fast and cheap. Good for simple tasks. |
| **Claude 3 Opus** | `claude-3-opus-20240229` | Maximum intelligence for complex reasoning. |

## Configuration

You can set the model globally via environment variables or per-agent.

### Environment Variable

```bash
export SHADOWBAR_MODEL="claude-3-haiku-20240307"
```

### Per-Agent

```python
agent = Agent(model="claude-3-opus-20240229")
```

## API Keys

ShadowBar looks for `ANTHROPIC_API_KEY` in your environment.

```bash
# .env file
ANTHROPIC_API_KEY=sk-ant-api03-...
```

You can also use `sb auth anthropic` to set this interactively.
