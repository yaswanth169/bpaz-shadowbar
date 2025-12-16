# Quick Start

Get up and running with ShadowBar in minutes.

## Prerequisites

*   Python 3.10 or higher
*   Access to Barclays internal network
*   An Anthropic API Key (provisioned via the internal AI portal)

## Installation

Install ShadowBar using `pip`:

```bash
pip install shadowbar
```

## Configuration

Set your Anthropic API key as an environment variable. You can do this in your shell or via a `.env` file.

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Creating Your First Agent

Use the `sb` CLI to scaffold a new agent project.

```bash
sb create my-first-agent
cd my-first-agent
```

This will create a directory with a basic agent structure.

## Running the Agent

You can run your agent directly with Python from inside the project directory:

```bash
python agent.py
```

## Example Code

Here is a minimal example of a ShadowBar agent:

```python
from shadowbar import Agent, llm_do

def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

agent = Agent(
    name="calculator",
    tools=[add],
    model="claude-sonnet-4-5",
    system_prompt="You are a helpful calculator assistant."
)

print(agent.input("What is 5 + 3?"))
```

## Next Steps

*   Explore [Core Concepts](/core-concepts/agent) to understand how agents work.
*   Check out [Useful Tools](/useful-tools/shell) to see what's available out of the box.
*   Learn about [Integrations](/integrations/microsoft) to connect with Microsoft 365.
