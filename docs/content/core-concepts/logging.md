# Logging & Sessions

Observability is critical for AI agents. ShadowBar automatically logs all activity to the `.sb` directory.

## Session Logs

Every interaction with an agent creates a session. Sessions are stored in `.sb/sessions/`.

Each session file contains:
*   The full conversation history.
*   Tool inputs and outputs.
*   Token usage statistics.
*   Timestamps for every event.

## The `sb` CLI

You can inspect logs using the CLI:

```bash
# List recent sessions
sb logs list

# View a specific session
sb logs view <session_id>
```

## Structured Logging

ShadowBar uses `structlog` internally to produce machine-readable JSON logs. This makes it easy to ingest logs into Splunk or other monitoring tools used at Barclays.
