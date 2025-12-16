---
hide:
  - navigation
  - toc
---

# ShadowBar Documentation (Barclays Internal)

<div class="grid" markdown>

<div class="card" markdown>
### 🚀 **Simple & Powerful**

Build complex AI agents with just a few lines of Python. ShadowBar handles the heavy lifting of state management, tool execution, and LLM communication.

[Get Started](quickstart.md){ .md-button .md-button--primary }
</div>

<div class="card" markdown>
### 🛡️ **Secure by Design**

Built for the enterprise. Features strict trust levels, comprehensive audit logging, and secure credential management via `sb auth`.

[Learn about Trust](concepts/trust.md){ .md-button }
</div>

<div class="card" markdown>
### 🔍 **Full Transparency**

Debug with confidence using `@xray`. Inspect every thought, tool call, and state change in real-time. No more black boxes.

[Debugging Guide](concepts/debugging.md){ .md-button }
</div>

<div class="card" markdown>
### 🏢 **Microsoft Integrated**

Seamlessly connects with the Barclays ecosystem. Native support for Outlook, Teams, Calendar, and SharePoint via Microsoft Graph.

[View Integrations](integrations/microsoft.md){ .md-button }
</div>

</div>

## Why ShadowBar?

ShadowBar is the standard framework for building AI agents at Barclays. It is optimized for **Anthropic Claude** models and provides a robust, secure environment for deploying autonomous agents.

!!! note "Internal Use Only"
    This documentation and the ShadowBar framework are for internal Barclays use only. Please do not share credentials or code outside the organization.

## Quick Example

```python title="agent.py"
from shadowbar import Agent
from shadowbar.tools import Outlook

# Initialize an agent with Outlook capabilities
agent = Agent(
    name="email-assistant",
    tools=[Outlook()],
    model="claude-3-5-sonnet-20241022",
    trust="tested"
)

# Run the agent
response = agent.input("Find the email from John about the 'Project X' meeting")
print(response)
```
