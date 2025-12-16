# The Agent

The `Agent` class is the central component of ShadowBar. It acts as the brain, orchestrating tools, managing memory, and communicating with the LLM to accomplish tasks.

## Initialization

To create an agent, you simply instantiate the `Agent` class.

```python
from shadowbar import Agent

agent = Agent(
    name="my-assistant",
    system_prompt="You are a helpful assistant.",
    tools=[...],
    model="claude-3-5-sonnet-20241022",
    max_iterations=15
)
```

### Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| `name` | `str` | Unique identifier for the agent. Used for logging and memory. | Required |
| `system_prompt` | `str` | The persona and instructions for the agent. Can be a string or path to a markdown file. | `"You are a helpful assistant."` |
| `tools` | `list` | A list of functions or class instances the agent can use. | `[]` |
| `model` | `str` | The LLM model to use. | `"claude-3-5-sonnet-20241022"` |
| `max_iterations` | `int` | Maximum number of thought/action loops allowed per request. | `15` |
| `trust` | `str` | Trust level (`open`, `tested`, `strict`). | `"open"` |

## The Input Loop

The primary way to interact with an agent is via the `input()` method.

```python
response = agent.input("What is the weather in London?")
```

When you call `input()`:
1.  **Context Loading**: The agent loads its memory and conversation history.
2.  **Reasoning**: It sends the history + new input to the LLM.
3.  **Tool Execution**: If the LLM decides to use a tool, the agent executes it.
4.  **Loop**: Steps 2-3 repeat until the task is done or `max_iterations` is reached.
5.  **Response**: The final answer is returned to you.

## System Prompts

ShadowBar supports loading system prompts from files, which is best practice for complex agents.

```python
agent = Agent(
    name="coder",
    system_prompt="prompts/coder.md"
)
```

The file can be Markdown, YAML, or JSON. ShadowBar auto-detects the format.
