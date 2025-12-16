# Browser

The `Browser` tool is a headless browser wrapper (based on Playwright) that allows agents to interact with modern web applications.

## Usage

```python
from shadowbar import Agent, Browser

browser = Browser()

agent = Agent(
    name="browser-agent",
    tools=[browser],
)
```

## Capabilities

*   `navigate(url)`: Go to a page.
*   `click(selector)`: Click an element.
*   `type(selector, text)`: Type into a field.
*   `screenshot()`: Take a screenshot (useful for debugging).

## Requirements

Requires Playwright to be installed:

```bash
pip install playwright
playwright install chromium
```
