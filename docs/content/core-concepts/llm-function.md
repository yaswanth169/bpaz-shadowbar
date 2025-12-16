# LLM Function (`llm_do`)

Sometimes you don't need a full agent. You just need to transform some text, extract data, or make a quick decision. For this, ShadowBar provides `llm_do`.

## Usage

`llm_do` is a functional wrapper around the LLM.

```python
from shadowbar import llm_do

# Simple text generation
summary = llm_do("Summarize this email: ...")

# Structured data extraction (returns JSON)
user_data = llm_do(
    "Extract the user's name and ID from this log: ...",
    output_schema={
        "name": "str",
        "id": "int"
    }
)
```

## When to use `llm_do` vs `Agent`

*   **Use `llm_do`** for stateless, single-turn tasks.
*   **Use `Agent`** when you need to maintain conversation history, use tools, or perform multi-step reasoning.
