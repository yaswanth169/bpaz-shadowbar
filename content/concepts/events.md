# Events System

ShadowBar's event system allows you to hook into the agent's lifecycle. This is powerful for logging, monitoring, or modifying behavior dynamically.

## Hook Types

### `after_user_input`
Fired immediately after the user sends a message, before the LLM sees it.
*   **Use case**: PII redaction, logging.

### `before_llm`
Fired right before the request is sent to Anthropic.
*   **Use case**: Modifying the prompt, adding context.

### `after_llm`
Fired after the LLM responds.
*   **Use case**: Logging costs, analyzing sentiment.

### `before_each_tool`
Fired before a tool is executed.
*   **Use case**: Approval workflows, rate limiting.

## Creating a Plugin

A plugin is just a class with methods named after the hooks.

```python
class LoggerPlugin:
    def before_llm(self, messages):
        print(f"Sending {len(messages)} messages to LLM...")

    def on_error(self, error):
        print(f"Something went wrong: {error}")

agent = Agent(plugins=[LoggerPlugin()])
```
