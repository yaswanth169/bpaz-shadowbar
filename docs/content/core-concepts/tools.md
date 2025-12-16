# Tools

Tools are the hands and eyes of an agent. In ShadowBar, a tool is simply a Python function or a class with a specific structure.

## Function Tools

The simplest way to define a tool is a standard Python function with type hints and a docstring.

```python
def get_weather(location: str) -> str:
    """
    Get the current weather for a given location.
    
    Args:
        location: The city and state, e.g. "London, UK"
    """
    # Implementation here...
    return "Sunny, 15°C"
```

ShadowBar automatically parses the signature and docstring to generate the tool definition for Claude.

## Class Tools

For more complex tools that need state (like a database connection), you can use a class.

```python
class DatabaseTool:
    def __init__(self, connection_string: str):
        self.conn = connect(connection_string)

    def query(self, sql: str) -> list:
        """Run a SQL query."""
        return self.conn.execute(sql).fetchall()
```

## Best Practices

*   **Type Hints**: Always use type hints. Claude relies on them to know what arguments to pass.
*   **Docstrings**: Write clear, descriptive docstrings. This is the "prompt" for the tool.
*   **Idempotency**: Where possible, make tools safe to call multiple times.
*   **Error Handling**: Raise exceptions if something goes wrong. The agent will see the error message and can try to recover.
