# Calendar

The `Calendar` tool integrates with Microsoft 365 to manage your schedule.

## Usage

```python
from shadowbar import Agent, MicrosoftCalendar

calendar = MicrosoftCalendar()

agent = Agent(
    name="calendar-agent",
    tools=[calendar],
)
```

## Features

*   `list_events(day)`: See what's on the calendar.
*   `create_event(subject, start, end)`: Schedule a meeting.
*   `check_availability(users, time)`: Check if colleagues are free.

## Authentication

Requires Microsoft 365 authentication. See the [Integrations](/integrations/microsoft) guide for setup instructions.
