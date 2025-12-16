# Web Research Example

An agent that combines `WebFetch` and `Memory` to perform deep research.

```python
from shadowbar import Agent, WebFetch, Memory

web = WebFetch()
memory = Memory()

agent = Agent(
    name="researcher",
    tools=[web, memory],
    model="claude-opus-4-5",
    system_prompt="""
You are a deep researcher.
1. Search for information.
2. Store key facts in memory.
3. Synthesize a final report.
""",
)

agent.input("Research the history of the Python GIL.")
```
