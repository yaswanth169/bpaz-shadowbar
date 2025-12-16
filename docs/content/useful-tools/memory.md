# Memory

The `Memory` tool gives agents a persistent key-value store. This allows them to remember information across sessions.

## Usage

```python
from shadowbar import Agent, Memory

memory = Memory()  # defaults to a markdown file under ./.sb/

agent = Agent(
    name="assistant-with-memory",
    tools=[memory],
)
```

## How it Works

By default, `Memory` persists to a markdown file in the `.sb` directory. It exposes simple read/write/search helpers that the agent can call:

*   `write_memory(key, value)`: Store or update a value.
*   `read_memory(key)`: Retrieve a value.
*   `list_memories()`: List all stored keys.
*   `search_memory(query)`: Search for matching entries.

## Use Cases

*   Storing user preferences.
*   Keeping track of task progress.
*   Caching expensive API results.
