# Shell Tool

The Shell tool allows agents to execute system commands. This is a powerful capability that is strictly controlled by the Trust system.

## Usage

```python
from shadowbar import Agent, Shell

shell = Shell()

agent = Agent(
    name="ops-agent",
    tools=[shell],
)
```

## Security

By default, you should combine `Shell` with the `shell_approval` plugin so that every command is reviewed by a human before execution.

When an agent attempts to run a command with `shell_approval` enabled:
1.  The command is intercepted.
2.  The user is prompted (via TUI) to approve the command.
3.  If approved, the command runs and output is returned to the agent.
4.  If denied, the agent receives an error message.

## Best Practices

*   **Sandboxing**: Always run agents with Shell access in a containerized environment where possible.
*   **Least Privilege**: Only give Shell access if absolutely necessary.
