# Browser Automation Example

An agent that uses the `Browser` tool to extract data from a website.

```python
from shadowbar import Agent, Browser

browser = Browser()

agent = Agent(
    name="browser-agent",
    tools=[browser],
    model="claude-sonnet-4-5",
    system_prompt="You are a research assistant. Use the browser to find information."
)

agent.input("Go to https://news.ycombinator.com and tell me the top story.")
```
