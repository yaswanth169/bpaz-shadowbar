# Trust

Security is the foundation of ShadowBar. The **Trust** system defines the boundaries of what an agent can do.

## Trust Levels

Every agent operates at a specific trust level.

| Level | Description |
| :--- | :--- |
| `untrusted` | No access to tools or network. Pure text generation only. |
| `read_only` | Can read files and access read-only tools. No network writes. |
| `standard` | (Default) Can use standard tools. Sensitive actions require approval. |
| `admin` | Full access to all tools and system commands. Use with caution. |

## Configuring Trust

You can set the trust level when initializing an agent:

```python
from shadowbar import Agent, Trust

agent = Agent(
    # ...
    trust=Trust(level="read_only")
)
```

## The Trust Agent

ShadowBar employs a "Trust Agent" pattern. Before executing any potentially dangerous action (like a shell command or API write), a separate, specialized agent reviews the action against the security policy. If the Trust Agent flags the action, it is blocked, and the main agent is notified.
