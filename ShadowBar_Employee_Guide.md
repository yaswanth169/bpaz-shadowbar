# ShadowBar Employee Guide (Team BPAZ)

An internal Python framework for building and running AI agents at Barclays. Built and maintained by Platform Engineering, Team BPAZ. This guide shows what ShadowBar does and how to use it end to end.

---

## What ShadowBar Provides
- Anthropic-only LLMs (Claude 4.5 family) baked in.
- Function/class tools turn into agent capabilities automatically.
- Plugins for ReAct reasoning, eval, shell approval, image formatting.
- Event hooks across the agent lifecycle.
- Persistent memory, logging, YAML sessions in `.sb/`.
- Multi-agent networking via the relay server + connect API.
- Browser automation tool (Playwright wrapper).
- Microsoft Outlook/Calendar tools (auth required).

---

## Install and Setup
```bash
pip install -e .
# Set API key
export ANTHROPIC_API_KEY="your-key"
```

---

## Quick Start: Minimal Agent
```python
from shadowbar import Agent

def add(a: float, b: float) -> float:
    return a + b

agent = Agent(
    name="calculator",
    tools=[add],
    system_prompt="You are a helpful calculator."
)

print(agent.input("What is 5 + 3?"))
```

---

## CLI Basics
```bash
# Create a project from templates (meta-agent by default)
sb create my-agent
cd my-agent
sb init           # set up config
sb status         # check config and keys
sb doctor         # sanity checks (Anthropic connectivity)
```

---

## Templates (ready-to-use)
- `meta-agent`: Development assistant.
- `minimal`: Smallest starter agent.
- `playwright`: Browser automation with Playwright.
- `web-research`: Web research starter.

Use:
```bash
sb init --template playwright
```

---

## Core Features with Examples

### 1) Tools (functions & classes)
```python
from shadowbar import Agent

def search(q: str) -> str:
    return f"Results for {q}"

class Todo:
    def __init__(self):
        self.items = []
    def add(self, text: str):
        self.items.append(text)
        return f"Added: {text}"
    def list(self):
        return self.items

todo = Todo()

agent = Agent("helper", tools=[search, todo])
agent.input("Add 'finish report' to my todo, then list todos.")
```

### 2) Memory
```python
from shadowbar import Agent, Memory
mem = Memory("notes.md")
agent = Agent("memo", tools=[mem])
agent.input("Remember: release is Friday")
agent.input("What did I say about release?")
```

### 3) Events
```python
from shadowbar import Agent, after_llm, after_each_tool

log = []

@after_llm
def track_llm(agent): log.append("llm")

@after_each_tool
def track_tool(agent): log.append("tool")

def ping(): return "pong"

agent = Agent("events", tools=[ping], on_events=[track_llm, track_tool])
agent.input("say hi")
print(log)  # ['llm', 'tool', ...]
```

### 4) Plugins
```python
from shadowbar import Agent
from shadowbar.useful_plugins import re_act, eval, shell_approval, image_result_formatter
agent = Agent("plugin-agent", plugins=[re_act, eval, shell_approval, image_result_formatter])
```

### 5) Logging & Sessions
- Logs: `.sb/logs/{agent}.log`
- Sessions (YAML): `.sb/sessions/{agent}.yaml`

### 6) Relay Server & Networking
Start relay:
```bash
uvicorn shadowbar.relay_server:app --host 0.0.0.0 --port 8000
```

Serve an agent:
```python
agent.serve(relay_url="ws://localhost:8000/ws/announce")
```

Connect to a remote agent:
```python
from shadowbar import connect
remote = connect("0x...agent_public_key...", relay_url="ws://localhost:8000/ws/announce")
print(remote.input("Say hello"))
```

### 7) Browser Automation (Playwright)
```python
from shadowbar import Agent, Browser

browser = Browser()
agent = Agent("web", tools=[browser])
agent.input("Open https://example.com and tell me the title.")
```

### 8) Microsoft Outlook / Calendar
- Tools: `Outlook`, `MicrosoftCalendar`
- Require Microsoft auth token (`MICROSOFT_ACCESS_TOKEN` or `sb auth microsoft`)

```python
from shadowbar import Agent, Outlook
mail = Outlook()
agent = Agent("mail", tools=[mail])
# agent.input("List my last 5 emails")  # requires token
```

---

## Testing
Key test scripts are in `tested-files/`:
- `test_all_features.py` — full feature sweep (Anthropic-only).
- `test_relay_integration.py` — relay + agent-to-agent networking.
- Others: `test_agent.py`, `test_browser_agent.py`, `test_installation.py`, `test_realtime.py`, `comprehensive_test.py`.

Reports in `tested-docs/`:
- `COMPREHENSIVE_TEST_REPORT.md`
- `RELAY_INTEGRATION_TEST_REPORT.md`
- `V1_LAUNCH_READINESS_REPORT.md`
- `FINAL_READINESS_REPORT.md`
- `TESTING_GUIDE.md`, `TESTING_DOCUMENTATION.md`, `TEST_FAILURES_GUIDE.md`, `UPDATE_VERIFICATION_REPORT.md`

Run a full sweep:
```bash
cd shadowbar
export ANTHROPIC_API_KEY="your-key"
python tested-files/test_all_features.py
```

Run relay integration:
```bash
python tested-files/test_relay_integration.py
```

---

## Operational Notes
- Default model: Claude 4.5 (set via `AnthropicLLM(model="claude-haiku-4-5")` or similar).
- Logging and sessions write under `.sb/`; ensure write permissions.
- Outlook/Calendar tests are expected to skip/fail without Microsoft auth.
- Browser tool requires Playwright installed and browsers set up (`pip install playwright && playwright install chromium`).

---

## Who Owns This
Platform Engineering, Team BPAZ. For support or escalations, reach out to the BPAZ team contacts.

