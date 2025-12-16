# Trust Parameter

The `trust` parameter controls the network capabilities of an agent.

## Host Allowlist

You can restrict which hosts an agent can connect to.

```python
from shadowbar import Agent, Trust

trust = Trust(
    allowed_hosts=["api.barclays.internal", "google.com"]
)

agent = Agent(..., trust=trust)
```

If the agent tries to connect to a host not in the allowlist, the connection is blocked.
