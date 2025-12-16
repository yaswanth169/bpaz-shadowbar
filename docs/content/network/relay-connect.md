# Relay Server & Connect

ShadowBar includes a lightweight **Relay Server** and a `connect()` helper so that agents can talk to each other across machines and environments.

This section explains how to:

1. Start the relay server.
2. Serve an agent so it can receive requests.
3. Call that agent from another process using `connect()`.

---

## 1. Start the Relay Server

Run the relay server in a terminal:

```bash
uvicorn shadowbar.relay_server:app --host 0.0.0.0 --port 8000
```

You should see logs indicating the server is listening on `http://0.0.0.0:8000` and the WebSocket endpoint `ws://localhost:8000/ws/announce`.

You can verify it is running by visiting:

```bash
curl http://localhost:8000/
```

You should see a JSON health response:

```json
{
  "service": "ShadowBar Relay Server",
  "status": "running",
  "agents_online": 0,
  "pending_requests": 0
}
```

---

## 2. Serve an Agent

Any `Agent` can be made network‑accessible via the `.serve()` method. This method:

- Loads or generates an Ed25519 keypair in `.sb/keys/`.
- Connects to the relay via WebSocket.
- Announces the agent’s **address** (its public key).
- Listens for incoming tasks until you stop it (Ctrl‑C).

```python
from shadowbar import Agent

def greet(name: str) -> str:
    return f"Hello {name}, welcome to ShadowBar!"

agent = Agent(
    name="greeter",
    tools=[greet],
    system_prompt="You are a friendly greeter for Barclays colleagues.",
)

agent.serve()  # blocks and listens on the relay
```

By default, `.serve()` uses the `SHADOWBAR_RELAY_URL` environment variable if set, otherwise it falls back to `ws://localhost:8000/ws/announce`.

```bash
export SHADOWBAR_RELAY_URL="ws://relay.internal.barclays:8000/ws/announce"
python agent.py
```

When the agent starts, you will see its **address** printed in the logs, e.g.:

```text
Address: 0x3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c
```

Keep this value – it is how other processes will reach your agent.

---

## 3. Call a Remote Agent with `connect()`

From another Python process (or another machine that can reach the relay), you can call the served agent as if it were local:

```python
from shadowbar import connect

REMOTE_ADDRESS = "0x3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c"

greeter = connect(REMOTE_ADDRESS)  # uses SHADOWBAR_RELAY_URL if set

response = greeter.input("Say hello to Yaswanth from Team BPAZ")
print(response)
```

Under the hood, `connect()`:

- Opens a WebSocket connection to the relay’s `/ws/input` endpoint.
- Sends an `INPUT` message addressed to the remote agent.
- Waits for the `OUTPUT` response and returns the text content.

You can also use `input_async()` from async code:

```python
import asyncio
from shadowbar import connect

async def main():
    remote = connect(REMOTE_ADDRESS)
    reply = await remote.input_async("Give me a one‑line status update.")
    print(reply)

asyncio.run(main())
```

---

## When to Use the Relay

Use the relay and `connect()` when:

- You want to expose a “platform agent” (e.g., a central research or compliance agent) that many teams can call.
- You want to separate concerns: one process handles UI, another runs long‑lived agents.
- You are building **agent networks** where one agent delegates work to another.

For single‑process scripts that don’t need remote calls, you can ignore the relay and call `.input()` directly on your agents.


