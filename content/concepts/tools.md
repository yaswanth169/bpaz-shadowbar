# Tools

Tools give your agent hands. They allow it to interact with the outside world—sending emails, browsing the web, querying databases, and more.

## Function-Based Tools

The simplest way to create a tool is a Python function. ShadowBar automatically parses the type hints and docstrings to create the tool schema for the LLM.

```python
def calculate_tax(amount: float, rate: float = 0.2) -> float:
    """
    Calculate the tax for a given amount.
    
    Args:
        amount: The base amount.
        rate: The tax rate (default 20%).
    """
    return amount * rate

agent = Agent(tools=[calculate_tax])
```

!!! tip "Docstrings Matter"
    The LLM reads your docstring to understand *when* and *how* to use the tool. Be descriptive!

## Class-Based Tools

For tools that need to maintain state (like a browser session or database connection), use a class.

```python
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item: str, price: float) -> str:
        """Add an item to the cart."""
        self.items.append({"item": item, "price": price})
        return f"Added {item} to cart."

    def checkout(self) -> str:
        """Calculate total and clear cart."""
        total = sum(i["price"] for i in self.items)
        self.items = []
        return f"Total: ${total}"

# Pass the INSTANCE to the agent
cart = ShoppingCart()
agent = Agent(tools=[cart])
```

When you pass a class instance, ShadowBar automatically converts all public methods (those not starting with `_`) into tools.

## The `@xray` Decorator

Use the `@xray` decorator to make your tools visible in the debug logs and to give them access to the agent's internal state.

```python
from shadowbar import xray

@xray
def complex_tool(query: str):
    """A tool that needs debugging visibility."""
    # ... logic ...
    return "Result"
```
