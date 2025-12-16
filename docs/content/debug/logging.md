# Logging

ShadowBar uses a structured logging system.

## Log Levels

*   `DEBUG`: Detailed information for debugging.
*   `INFO`: General operational events.
*   `WARNING`: Something unexpected happened, but execution continues.
*   `ERROR`: A serious problem.

## Configuration

You can configure the log level via the `SB_LOG_LEVEL` environment variable.

```bash
export SB_LOG_LEVEL=DEBUG
```
