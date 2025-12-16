# Trust & Security

Security is paramount at Barclays. ShadowBar implements a "Trust Level" system to control what agents can do.

## Trust Levels

### `open`
*   **Behavior**: The agent can execute any tool without confirmation.
*   **Use Case**: Read-only agents, development, local sandboxes.

### `tested`
*   **Behavior**: The agent can execute *safe* (read-only) tools freely, but requires user confirmation for *sensitive* (write/delete) actions.
*   **Use Case**: Most internal tools, email assistants.

### `strict`
*   **Behavior**: The agent requires confirmation for *every* tool execution.
*   **Use Case**: Production systems, high-risk operations.

## Configuring Trust

Set the trust level when initializing the agent.

```python
agent = Agent(trust="tested")
```

## Defining Sensitive Tools

You can mark specific tools as sensitive.

```python
@tool(sensitive=True)
def delete_database():
    ...
```

ShadowBar's built-in `Outlook.send` and `File.write` are marked sensitive by default.
