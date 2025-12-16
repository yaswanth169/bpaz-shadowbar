# Interactive Debugging

ShadowBar provides an interactive debugger that lets you inspect the agent's state in real-time.

## Starting the Debugger

You can drop into the debugger at any point in your code:

```python
agent.debug()
```

Or run the agent with the `--debug` flag:

```bash
sb run agent.py --debug
```

## Commands

Inside the debugger, you can use the following commands:
*   `state`: View the current agent state (memory, history).
*   `tools`: List available tools.
*   `step`: Execute the next step.
*   `continue`: Resume normal execution.
