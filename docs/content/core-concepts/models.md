# Models

ShadowBar is optimized for the **Anthropic Claude** family of models. We believe Claude offers the best balance of reasoning, coding capability, and safety for enterprise use cases.

## Supported Models

| Model ID | Description | Best For |
| :--- | :--- | :--- |
| `claude-sonnet-4-5` | Default production model. | Complex reasoning, coding, tool use. |
| `claude-opus-4-5` | Highest capability. | Long-form writing, complex analysis, critical decisions. |
| `claude-haiku-4-5` | Fast and cost-effective. | Simple tasks, classification, high-volume workloads. |

## Configuration

You specify the model when creating an agent:

```python
agent = Agent(
    name="coder",
    model="claude-sonnet-4-5",
    # ...
)
```

## Why Anthropic Only?

By focusing on a single provider, we can:

1.  **Deeply Integrate**: We use specific features like prompt caching and precise tool definitions.
2.  **Simplify API**: We don't need a generic "LLM" abstraction layer that hides model-specific capabilities.
3.  **Ensure Compliance**: Anthropic's data retention and privacy policies align with Barclays' requirements.
