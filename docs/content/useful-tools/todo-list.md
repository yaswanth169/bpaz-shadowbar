# Todo List

A simple task management tool for agents. This helps agents break down complex goals into manageable steps.

## Usage

```python
from shadowbar import Agent, TodoList

todos = TodoList()

agent = Agent(
    name="planner",
    tools=[todos],
)
```

## Features

The `TodoList` tool is designed around natural-language task names:

*   `add(content, active_form)`: Add a new task (e.g., `"Fix auth bug"`, `"Fixing auth bug"`).
*   `start(content)`: Mark a task as in progress.
*   `complete(content)`: Mark a task as done.
*   `list()`: Render the current todo list as formatted text.

The agent is encouraged to use this tool to "think out loud" and plan its work step by step.
