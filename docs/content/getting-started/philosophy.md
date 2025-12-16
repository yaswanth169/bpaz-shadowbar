# Philosophy

How ShadowBar thinks about agents, tools, and the developer experience.

## Design Principles

ShadowBar is built for engineers who ship real systems inside a regulated bank. Our philosophy is:

- **One mental model**: an `Agent`, a small set of `tools`, and a clear `system_prompt`. You shouldn’t need a diagram of flows and graphs to understand what your agent is doing.
- **Strong defaults, no magic**: sensible configuration out of the box, but everything important is explicit in code and config.
- **Production before prototypes**: every feature exists because it can be operated and supported in production, not just in a demo notebook.

## Scaling With Confidence

While it is easy to start, ShadowBar is designed to grow with your use case:

- **Type‑aware tools**: Python type hints drive tool schemas so Claude calls your functions correctly.
- **Deep observability**: logs, sessions, and traces make it obvious *what* happened and *why*.
- **Trust everywhere**: the trust layer is built into the `Agent` and networking stack so you can reason about blast radius up front.

## The "Barclays Way"

ShadowBar reflects how Barclays thinks about AI in production:

1. **Anthropic‑first**: we commit to Claude and integrate deeply with its capabilities instead of chasing every provider.
2. **Least privilege by default**: agents see only the tools, data, and networks you explicitly grant.
3. **Humans in control**: sensitive actions always have a human approval path (for example the `shell_approval` plugin or change‑review flows).

## Flow Over Friction

We aim to keep you in flow: ShadowBar handles plumbing—retry logic, logging, session storage, relay wiring—so you can focus on the intent of your agent, the user journeys it supports, and the guardrails it must respect.
