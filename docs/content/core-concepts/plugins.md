# Plugin System

Plugins allow you to package and share ShadowBar functionality. A plugin can contain tools, event handlers, and system prompts.

## Using Plugins

To use a plugin, simply import it and pass it to the agent.

```python
from shadowbar.plugins import gitlab_plugin

agent = Agent(
    # ...
    plugins=[gitlab_plugin]
)
```

## Creating a Plugin

A plugin is just a Python module or class that exposes a `register` function.

```python
# my_plugin.py

def register(agent):
    agent.add_tool(my_custom_tool)
    agent.on("tool_error", my_error_handler)
```

## Standard Plugins

ShadowBar comes with several built-in plugins:

*   `shell_approval`: Requires human approval for shell commands.
*   `gmail_plugin`: Tools for reading/sending email.
*   `calendar_plugin`: Tools for calendar management.
