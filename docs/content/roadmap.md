# Roadmap

ShadowBar's internal roadmap for Barclays, maintained by **Platform Engineering – Team BPAZ**.

We treat v1.0.0 as the baseline for ShadowBar inside the bank and evolve from there.

---

## Current Milestones

### ShadowBar v1.0.0 Launch (Q4 2025)

Anthropic‑only agent framework, ready for internal adoption.

**Features (v1.0.0):**

- Core `Agent`/`tools` framework with type‑hinted tools.
- Anthropic Claude (Claude 4.5 family) integration via `AnthropicLLM`.
- Trust layer (`Trust` parameter) with host allow‑lists.
- Rich logging and session storage under `.sb/logs/`.
- Relay server (`shadowbar.relay_server`) and `connect()` helper for agent‑to‑agent calls.
- Browser automation tool (`Browser`) wrapping Playwright.
- Useful tools for Memory, Shell, WebFetch, DiffWriter, TodoList, Outlook, Microsoft Calendar.
- Plugin system (`re_act`, `eval`, `shell_approval`, `image_result_formatter`).
- CLI (`sb`) for `create`, `init`, `auth`, `status`, `doctor`.
- Next.js and MkDocs‑Material documentation sites.

Status: **Complete**

---

### Enterprise Network & Relay Hardening (Q1 2026)

Make the relay and networking story production‑grade for Barclays.

**Planned/ongoing work:**

- Harden relay server for production (timeouts, back‑pressure, metrics).
- Service discovery patterns for “platform agents” (central research/compliance agents).
- Operational playbooks for running the relay inside Barclays infrastructure.
- First‑class examples for multi‑agent topologies (orchestrator → specialist agents).

Status: **In Progress**

---

### Trust & Audit Expansion (Q1–Q2 2026)

Extend the trust layer beyond simple host allow‑lists so teams can reason about risk more explicitly.

**Planned features:**

- Per‑tool trust profiles (e.g., Shell, Browser, Outlook).
- Stronger logging for tool inputs/outputs with redaction hooks.
- Session‑level audit exports for model, prompt, tools, and network calls.
- Recommended “trust profiles” for common agent types (research agents, operations agents, automation agents).

Status: **Planned**

---

### Evaluation & Guardrails (Q2 2026)

Provide batteries‑included evaluation patterns so ShadowBar agents can be tested like any other service.

**Planned features:**

- Evaluation utilities for regression suites (prompt + tools + expected behaviour).
- Example tests in `tested-files/` plus guides in `tested-docs/`.
- Hooks for capturing structured traces that can feed internal eval systems.
- Opinionated examples for human‑in‑the‑loop review flows (using `shell_approval` and custom plugins).

Status: **Planned**

---

### Template & Example Library (Q2–Q3 2026)

Make it easy for any Barclays colleague (tech or non‑tech) to start from a proven pattern instead of a blank file.

**Planned features:**

- Expanded `sb create` templates: “operations assistant”, “compliance summariser”, “browser research”, etc.
- Library of tested examples in the docs (browser automation, Outlook triage, calendar coordination, research).
- Internal “recipes” for common use cases (team onboarding, reporting, ticket triage).

Status: **Planned**

---

### Platform & Tooling (2026+)

Longer‑term platform features that we may prioritise based on adoption.

- VS Code / internal IDE helpers for ShadowBar projects.
- Agent catalogue / registry for discovering reusable internal agents.
- Deeper integration with Barclays observability stack (logs, metrics, traces).
- Optional auto‑coding helpers built on ShadowBar itself (agents that refactor or scaffold code safely).

Status: **Exploratory**

---

## How to Influence the Roadmap

ShadowBar is an internal framework; there is no public GitHub or Discord. Instead:

- **Feature ideas / pain points**: email or message  
  `devavarapu.yaswanth@barclays.com` (Team BPAZ) on Microsoft Teams.
- **Concrete proposals**: share the use case, impact, and which teams would adopt it if we built it.
- **Pilot volunteers**: if your team wants to be an early adopter for a feature above, mention this so we can prioritise properly.

Our north star is simple: **every Barclays colleague should be able to lean on agentic systems to remove repetitive work and create new kinds of impact.** The roadmap will keep evolving to support that goal.


