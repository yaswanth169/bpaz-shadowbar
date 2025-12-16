# WebFetch

`WebFetch` allows agents to retrieve content from the internet. It is designed to be safe and efficient, stripping away HTML boilerplate to return clean Markdown.

## Usage

```python
from shadowbar import Agent, WebFetch

web = WebFetch()

agent = Agent(
    name="web-agent",
    tools=[web],
)
```

## Features

*   **Markdown Conversion**: Automatically converts HTML to readable Markdown.
*   **Proxy Support**: Configured to work with Barclays internal proxies.
*   **Rate Limiting**: Prevents agents from spamming requests.

## Security Note

Access to external websites is subject to Barclays network policies. Some domains may be blocked.
