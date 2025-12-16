# Microsoft 365 Integration

ShadowBar is designed to work seamlessly within the Barclays ecosystem, which relies heavily on Microsoft 365. We provide first-class integrations for Outlook, Teams, and Calendar via the Microsoft Graph API.

## Authentication

Before using Microsoft tools, you must authenticate.

```bash
sb auth microsoft
```

This will open a browser window for you to log in with your Barclays credentials. The token is stored securely in `~/.sb/credentials`.

## Outlook

The `Outlook` tool allows agents to read, search, and send emails.

```python
from shadowbar.tools import Outlook

outlook = Outlook()

# Search for emails
emails = outlook.search("subject:Project X")

# Send an email
outlook.send(
    to="jane.doe@barclays.com",
    subject="Update",
    body="Here is the latest status..."
)
```

### Capabilities
*   `send_email(to, subject, body)`
*   `reply_to_email(id, body)`
*   `search_emails(query)`
*   `get_unread_emails()`

## Calendar

Manage your schedule programmatically.

```python
from shadowbar.tools import Calendar

calendar = Calendar()

# List today's events
events = calendar.list_events(date="today")

# Schedule a meeting
calendar.create_event(
    subject="Sync",
    start="2023-10-27T10:00:00",
    end="2023-10-27T10:30:00",
    attendees=["jane.doe@barclays.com"]
)
```

## Teams

Send messages to chats and channels.

```python
from shadowbar.tools import Teams

teams = Teams()
teams.send_message(chat_id="...", message="Hello team!")
```
