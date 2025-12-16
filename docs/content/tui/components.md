# TUI Components

ShadowBar includes a set of Terminal User Interface (TUI) components to build rich interactive agents.

## Components

### `pick`

Select an item from a list.

```python
from shadowbar.tui import pick

choice = pick(["Option A", "Option B"], title="Choose one:")
```

### `Input`

Get text input from the user with validation.

```python
from shadowbar.tui import Input

name = Input("What is your name?").ask()
```

### `StatusBar`

Display a persistent status bar at the bottom of the screen.

```python
from shadowbar.tui import StatusBar

with StatusBar("Processing..."):
    # do work
    pass
```
