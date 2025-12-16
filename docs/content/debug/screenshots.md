# Browser Screenshots

When using the `Browser` tool, it can be helpful to see what the agent sees.

## Automatic Screenshots

You can configure the agent to take a screenshot on every navigation event.

```python
agent = Agent(
    # ...
    browser_config={"screenshot_on_nav": True}
)
```

Screenshots are saved to `.sb/screenshots/`.
