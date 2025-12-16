# Diff Writer

The `DiffWriter` tool allows agents to make precise edits to files. Instead of rewriting an entire file, the agent sends a unified diff or a search-and-replace block.

## Why DiffWriter?

*   **Efficiency**: Saves tokens by not outputting the whole file.
*   **Safety**: Reduces the risk of accidental deletion or truncation.
*   **Context**: The agent can see the context of the change.

## Usage

```python
from shadowbar import Agent, DiffWriter

writer = DiffWriter()  # or DiffWriter(auto_approve=True) for automation

agent = Agent(
    name="editor",
    tools=[writer],
)
```

## Supported Operations

`DiffWriter` focuses on three core operations:

*   `write(path, content)`: Apply a full-file update with an interactive diff/approval flow.
*   `diff(path, content)`: Show the diff without writing (preview mode).
*   `read(path)`: Read the current file contents.
