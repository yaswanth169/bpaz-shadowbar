# Calculator Example

A minimal example showing how to define a tool and use it with an agent.

```python
from shadowbar import Agent

def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

agent = Agent(
    name="calc",
    tools=[add, multiply],
    model="claude-sonnet-4-5",
)

print(agent.input("What is (5 + 3) * 2?"))
```
