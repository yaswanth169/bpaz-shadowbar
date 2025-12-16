# Event System

ShadowBar is built on an event-driven architecture. This allows you to hook into the agent's lifecycle to add logging, monitoring, or custom behaviors.

## The `on_event` Decorator

You can register handlers for specific events using the `@on_event` decorator.

```python
from shadowbar import Agent, on_event

@on_event("tool_start")
def log_tool_usage(event):
    print(f"Tool started: {event.tool_name}")

agent = Agent(...)
```

## Common Events

*   `agent_start`: Fired when the agent begins processing an input.
*   `llm_request`: Fired before sending a request to Claude.
*   `llm_response`: Fired when a response is received.
*   `tool_start`: Fired before a tool is executed.
*   `tool_end`: Fired after a tool completes.
*   `agent_end`: Fired when the agent finishes its task.

## Use Cases

*   **Audit Logging**: Record every action to a compliance database.
*   **Real-time UI**: Update a frontend as the agent thinks.
*   **Metrics**: Track token usage and latency.
