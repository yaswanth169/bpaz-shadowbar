# Minimal ShadowBar Agent

The simplest way to get started with ShadowBar. A basic calculator agent that demonstrates:
- Creating an agent with a simple tool
- Interactive conversations
- Using both `agent.input()` and `llm_do()` functions

## Quick Start

```bash
# Initialize project (if not already done)
sb init --template minimal

# Run the agent
python agent.py
```

## What's Inside

**`agent.py`** - A minimal agent with:
- Simple calculator tool (add, subtract, multiply, divide)
- Interactive conversation loop
- Examples of both agent and direct LLM usage

## Example Interaction

```python
# The agent can use its calculator tool
agent.input("What is 25 * 4?")
# → The calculator will compute: 100

# Direct LLM call without tools
llm_do("What is ShadowBar?")
# → Quick response without agent overhead
```

## Environment Variables

The `.env` file is created automatically during `sb init`. It includes:

- `ANTHROPIC_API_KEY` - Anthropic API key (required)
- Or `ANTHROPIC_API_KEY` - Your Anthropic API key

## Next Steps

**Ready for more?** Try these templates:

- `sb init --template playwright` - Browser automation with Playwright
- `sb init --template web-research` - Web search and research tools
- `sb init --template meta-agent` - Multi-agent orchestration

## Learn More

- [Documentation](https://docs.shadowbar.com)
- [Examples](https://gitlab.com/shadowbar/shadowbar/-/tree/main/examples)
- [Discord Community](https://discord.gg/4xfD9k8AUF)
