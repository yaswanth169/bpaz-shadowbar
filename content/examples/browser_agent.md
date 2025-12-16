# Browser Agent Example

This example demonstrates how to build an agent that can navigate the web, extract information, and take screenshots.

## Prerequisites

*   `playwright` installed (`pip install playwright`)
*   `playwright install` run

## The Code

```python title="browser_agent.py"
from shadowbar import Agent
from shadowbar.tools import Browser

# Initialize the browser tool
browser = Browser()

# Create the agent
agent = Agent(
    name="researcher",
    system_prompt="You are a web researcher. Use the browser to find information.",
    tools=[browser],
    model="claude-3-5-sonnet-20241022"
)

# Run a task
task = "Go to news.ycombinator.com and tell me the top story."
response = agent.input(task)

print(f"Result: {response}")

# Clean up
browser.close()
```

## How it Works

1.  **Browser Tool**: The `Browser` class manages a headless Chromium instance.
2.  **Navigation**: The agent calls `browser.navigate(url)`.
3.  **Extraction**: The agent uses `browser.get_content()` to read the page text.
4.  **Reasoning**: Claude analyzes the text to find the "top story".
