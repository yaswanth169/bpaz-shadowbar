# Email Agent Example

This example shows how to build an agent that manages your Outlook inbox, a common use case at Barclays.

## Prerequisites

*   Authenticated with Microsoft (`sb auth microsoft`)

## The Code

```python title="email_agent.py"
from shadowbar import Agent
from shadowbar.tools import Outlook

# Initialize Outlook tool
outlook = Outlook()

# Create the agent
agent = Agent(
    name="email-assistant",
    system_prompt="""
    You are an efficient email assistant.
    - Prioritize unread emails from 'Important' senders.
    - Draft replies but do not send without confirmation (trust=tested).
    """,
    tools=[outlook],
    model="claude-3-5-sonnet-20241022",
    trust="tested"  # Requires confirmation for sensitive actions
)

# Run the agent
print("Checking email...")
response = agent.input("Check my unread emails and summarize any from 'Project X'")
print(response)
```

## Key Concepts

*   **Trust Levels**: We set `trust="tested"`. If the agent tries to *send* an email, ShadowBar will pause and ask you for confirmation.
*   **System Prompt**: We give specific instructions on how to handle emails.
