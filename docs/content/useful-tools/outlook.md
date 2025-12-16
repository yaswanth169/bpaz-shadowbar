# Outlook

The `Outlook` tool integrates with Microsoft 365 to allow agents to send and receive emails.

## Usage

```python
from shadowbar import Agent, Outlook

outlook = Outlook()

agent = Agent(
    name="mail-agent",
    tools=[outlook],
)
```

## Features

*   `send_email(to, subject, body)`: Send an email.
*   `read_emails(limit=5)`: Read recent emails.
*   `search_emails(query)`: Search for specific emails.

## Authentication

Requires Microsoft 365 authentication. Run:

```bash
sb auth microsoft
```

Then follow the [Microsoft Integration](/integrations/microsoft) guide for environment variables and scopes.
