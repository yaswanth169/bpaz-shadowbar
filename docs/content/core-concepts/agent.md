# Agent

The `Agent` class is the core building block of ShadowBar. It represents an autonomous entity capable of reasoning, using tools, and maintaining state.

## Basic Usage

```python
from shadowbar import Agent

agent = Agent(
    name="my-agent",
    model="claude-sonnet-4-5",
    system_prompt="You are a helpful assistant."
)

response = agent.input("Hello!")
```

## Key Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `name` | `str` | Unique identifier for the agent. Used for logging and addressing. |
| `model` | `str` | The Anthropic model to use (e.g., `claude-sonnet-4-5`). |
| `tools` | `list` | A list of functions or tool objects the agent can use. |
| `system_prompt` | `str` | The persona and instructions for the agent. |
| `trust` | `Trust` | Security configuration for the agent. |

## Lifecycle

1.  **Initialization**: The agent sets up its memory, logger, and tool definitions.
2.  **Input**: You send a message to the agent via `.input()`.
3.  **Reasoning**: The agent sends the history to Claude and decides what to do.
4.  **Tool Execution**: If Claude requests a tool call, the agent executes it (subject to trust checks).
5.  **Response**: The agent returns the final answer or asks for more information.

## Advanced: Sub-Agents

Agents can call other agents. This is handled via the `Network` layer.

```python
# In a complex setup, one agent might delegate to another
result = agent.input("Ask the research-agent to find the stock price of BARC.")
```
