# Input

The `Input` component provides a robust way to get user input in the terminal.

## Features

*   **Validation**: Ensure the input matches a regex or custom function.
*   **Default Values**: Provide a default if the user just hits Enter.
*   **Password Mode**: Hide input for sensitive data.

## Example

```python
from shadowbar.tui import Input

password = Input("Enter API Key:", password=True).ask()
```
