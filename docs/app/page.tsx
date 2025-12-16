 "use client";

import React from "react";
import { TerminalBlock } from "@/components/ui/TerminalBlock";
import { ComparisonView } from "@/components/ui/ComparisonView";
import { Step } from "@/components/ui/StepGuide";
import { ArrowRight, Gitlab, X } from "lucide-react";
import Link from "next/link";

export default function Home() {
  const [showContributionModal, setShowContributionModal] = React.useState(false);

  return (
    <div className="space-y-24">
      {/* Hero Section */}
      <section className="relative pt-12 text-center">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[300px] bg-purple-500/20 blur-[120px] rounded-full opacity-50 pointer-events-none" />

        <h1 className="relative text-5xl font-bold tracking-tight sm:text-7xl">
          Securely Automate,
          <br />
          <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            Intelligently Integrate
          </span>
        </h1>

        <p className="relative mt-6 text-lg text-gray-400 max-w-2xl mx-auto">
          The Barclays internal AI agent framework from Platform Engineering (Team BPAZ),
          built so every colleague can adopt agentic systems to accelerate their day‑to‑day work.
        </p>

        <div className="relative mt-10 flex justify-center gap-4">
          <Link
            href="/getting-started/quick-start"
            className="flex items-center gap-2 rounded-full bg-gradient-to-r from-purple-600 to-pink-600 px-6 py-3 font-semibold text-white transition-transform hover:scale-105"
          >
            Quick Start <ArrowRight className="h-4 w-4" />
          </Link>
          <Link
            href="https://gitlab.barclays.internal/shadowbar/shadowbar"
            className="flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-6 py-3 font-semibold text-white transition-colors hover:bg-white/10"
          >
            <Gitlab className="h-4 w-4" /> GitLab
          </Link>
        </div>

        <div className="mt-16 max-w-2xl mx-auto">
          <TerminalBlock
            command="pip install shadowbar (coming soon)"
            className="transform transition-all hover:scale-[1.01]"
          />
        </div>
      </section>

      {/* Comparison Section – Core Agent Simplicity */}
      <section>
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold">Type hints = automatic tools. No wrappers needed.</h2>
          <p className="text-gray-400 mt-2">
            Define normal Python functions with type hints and ShadowBar turns them into safe tools for Claude.
          </p>
        </div>

        <ComparisonView
          leftTitle="ShadowBar"
          rightTitle="LangChain"
          leftContent={
            <pre className="text-sm text-gray-300 overflow-x-auto">
              <code>{`from shadowbar import Agent

def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

agent = Agent(
    name="calc",
    tools=[add],
    model="claude-sonnet-4-5",
)

agent.input("What is 5 + 3?")`}</code>
            </pre>
          }
          rightContent={
            <pre className="text-sm text-gray-500 overflow-x-auto opacity-50">
              <code>{`from langchain.agents import Tool, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

def add(input_str):
    a, b = map(int, input_str.split(","))
    return a + b

tools = [
    Tool(
        name="Add",
        func=add,
        description="Add two numbers"
    )
]

prompt = PromptTemplate(...)
llm = ChatOpenAI(...)
# ... 20 more lines of setup ...`}</code>
            </pre>
          }
        />
      </section>

      {/* Browser Automation Section */}
      <section className="mt-24">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold">Browser Automation – just pass a class.</h2>
          <p className="text-gray-400 mt-2">
            Public methods become tools and <code>self</code> becomes shared state between calls.
          </p>
        </div>

        <ComparisonView
          leftTitle="ShadowBar"
          rightTitle="Generic SDK"
          leftContent={
            <pre className="text-sm text-gray-300 overflow-x-auto">
              <code>{`from shadowbar import Agent, Browser


class DocsBrowser(Browser):
    \"\"\"Simple wrapper around Playwright for internal docs.\"\"\"

    def open_docs(self, path: str) -> str:
        self.goto(f"https://shadowbar.barclays.internal{path}")
        return "Opened docs page"

    def screenshot(self, name: str) -> str:
        self.capture_screenshot(f"{name}.png")
        return f"Saved screenshot {name}.png"


browser = DocsBrowser()

agent = Agent(
    name="docs-helper",
    tools=[browser],
    model="claude-sonnet-4-5",
)

agent.input("Open the getting-started page and take a screenshot called 'onboarding'.")`}</code>
            </pre>
          }
          rightContent={
            <pre className="text-sm text-gray-500 overflow-x-auto opacity-50">
              <code>{`# Pseudocode using a generic SDK
from sdk.browser import launch_browser
from sdk.agents import Tool, Agent, Runner


browser = launch_browser(headless=True)

def open_docs(url: str) -> str:
    browser.goto(url)
    return "Opened docs page"

def screenshot(name: str) -> str:
    browser.screenshot(path=f"{name}.png")
    return f"Saved screenshot {name}.png"

tools = [
    Tool(name="open_docs", func=open_docs, description="Open a docs URL"),
    Tool(name="screenshot", func=screenshot, description="Take a screenshot"),
]

agent = Agent(
    instructions="Help with internal documentation.",
    tools=tools,
)

runner = Runner(agent)
runner.run("Open the getting-started page and take a screenshot called 'onboarding'.")`}</code>
            </pre>
          }
        />
      </section>

      {/* Memory System Section */}
      <section className="mt-24">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold">Memory is just a tool.</h2>
          <p className="text-gray-400 mt-2">
            No sessions or hidden state machines – memory is explicit and testable like any other tool.
          </p>
        </div>

        <ComparisonView
          leftTitle="ShadowBar"
          rightTitle="Heavyweight Memory Stacks"
          leftContent={
            <pre className="text-sm text-gray-300 overflow-x-auto">
              <code>{`from shadowbar import Agent, Memory


preferences = Memory()

agent = Agent(
    name="preference-helper",
    system_prompt="You remember user preferences and explain how they are used.",
    tools=[preferences],
    model="claude-sonnet-4-5",
)

agent.input("Remember that I prefer dark mode and weekly summaries.")
agent.input("What are my preferences and how will you use them?")`}</code>
            </pre>
          }
          rightContent={
            <pre className="text-sm text-gray-500 overflow-x-auto opacity-50">
              <code>{`# Pseudocode for a typical memory stack
from framework.memory import ConversationBufferMemory, SummaryMemory
from framework.prompts import PromptTemplate
from framework.chains import LLMChain


short_term = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
)

long_term = SummaryMemory(
    summary_key="summary",
    k=5,
)

template = PromptTemplate(
    input_variables=["chat_history", "summary", "input"],
    template=\"\"\"You are a preference assistant.

Summary so far: {summary}
Conversation:
{chat_history}

User: {input}
\"\"\",
)

chain = LLMChain(
    llm=...,
    prompt=template,
    memory=[short_term, long_term],
)`}</code>
            </pre>
          }
        />
      </section>

      {/* Event Hooks Section */}
      <section className="mt-24">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold">Event hooks with full agent context.</h2>
          <p className="text-gray-400 mt-2">
            Log, enforce policy, or add approvals – without forking the framework.
          </p>
        </div>

        <ComparisonView
          leftTitle="ShadowBar"
          rightTitle="Guardrails-only Systems"
          leftContent={
            <pre className="text-sm text-gray-300 overflow-x-auto">
              <code>{`from shadowbar import Agent
from shadowbar.events import after_llm, before_each_tool


def trace_llm(event):
    print("LLM tokens:", event.tokens_used)


def approve_tool(event):
    if event.tool_name == "Shell":
        raise PermissionError("Shell tool requires human approval.")


agent = Agent(
    name="audited-assistant",
    model="claude-sonnet-4-5",
    tools=[...],
    on_events=[
        after_llm(trace_llm),
        before_each_tool(approve_tool),
    ],
)

agent.input("Run a risky command on this server.")`}</code>
            </pre>
          }
          rightContent={
            <pre className="text-sm text-gray-500 overflow-x-auto opacity-50">
              <code>{`# Pseudocode for a guardrail-only system
from sdk import Agent, Guardrail, Runner


def check_output(text: str) -> None:
    if "rm -rf" in text:
        raise Guardrail("Blocked dangerous command text.")


guardrails = [Guardrail(check_output)]

agent = Agent(
    tools=[...],
    guardrails=guardrails,
)

runner = Runner(agent)
runner.run("Run a risky command on this server.")`}</code>
            </pre>
          }
        />
      </section>

      {/* Quick Start Section */}
      <section className="mt-24">
        <div className="mb-12">
          <h2 className="text-3xl font-bold">Quick Start Guide</h2>
          <p className="text-gray-400 mt-2">Get up and running in under 2 minutes.</p>
        </div>

        <div className="max-w-3xl">
          <Step number={1} title="Install ShadowBar">
            <p className="mb-4">Install the package via pip. Requires Python 3.10+.</p>
            <TerminalBlock command="pip install shadowbar" />
          </Step>

          <Step number={2} title="Authenticate">
            <p className="mb-4">Log in with your Barclays credentials to access managed LLMs.</p>
            <TerminalBlock command="sb auth microsoft" />
          </Step>

          <Step number={3} title="Create Your First Agent" isLast>
            <p className="mb-4">Use the CLI to scaffold a new agent.</p>
            <TerminalBlock command="sb create my-agent" output="Created agent in ./my-agent" />
          </Step>
        </div>
      </section>

      {/* Production Ready Section */}
      <section className="mt-24">
        <div className="text-center mb-10">
          <h2 className="text-3xl font-bold">Production ready from day one.</h2>
          <p className="text-gray-400 mt-2">
            Built for regulated environments: logging, plugins, approvals, and networking are first‑class.
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-4">
          <div className="rounded-2xl border border-white/10 bg-white/5 p-4 text-center">
            <div className="text-xs font-semibold text-purple-300 mb-1 tracking-wide">Auto Logs</div>
            <div className="text-sm text-gray-200">Every session is logged under <code>.sb/logs/</code>.</div>
          </div>
          <div className="rounded-2xl border border-white/10 bg-white/5 p-4 text-center">
            <div className="text-xs font-semibold text-purple-300 mb-1 tracking-wide">Plugins</div>
            <div className="text-sm text-gray-200">
              Drop in <code>re_act</code>, <code>eval</code>, <code>shell_approval</code>, and more.
            </div>
          </div>
          <div className="rounded-2xl border border-white/10 bg-white/5 p-4 text-center">
            <div className="text-xs font-semibold text-purple-300 mb-1 tracking-wide">Relay &amp; Connect</div>
            <div className="text-sm text-gray-200">Serve agents over WebSockets and call them from anywhere.</div>
          </div>
          <div className="rounded-2xl border border-white/10 bg-white/5 p-4 text-center">
            <div className="text-xs font-semibold text-purple-300 mb-1 tracking-wide">Human in the Loop</div>
            <div className="text-sm text-gray-200">
              Route sensitive actions through approvals and structured reviews.
            </div>
          </div>
        </div>
      </section>

      {/* Contribution & Adoption Section */}
      <section className="mt-24">
        <div className="mt-24 max-w-4xl mx-auto">
          <div className="relative overflow-hidden rounded-3xl border border-white/10 bg-white/5/10 bg-white/5 backdrop-blur-xl p-8 shadow-[0_0_40px_rgba(0,0,0,0.45)] transition-transform duration-200 hover:-translate-y-1 hover:shadow-[0_24px_80px_rgba(0,0,0,0.7)]">
            <div className="absolute inset-0 pointer-events-none bg-gradient-to-r from-purple-500/10 via-pink-500/10 to-blue-500/10 opacity-70" />
            <div className="relative space-y-4">
              <h2 className="text-2xl font-semibold">
                Make ShadowBar Yours – For Every Colleague, Tech and Non‑Tech
              </h2>
              <p className="text-gray-300">
                Our goal is simple: **every person in Barclays** should be able to lean on agentic systems to
                remove repetitive work and create new kinds of impact. ShadowBar is the foundation, but the
                real magic comes from the agents you and your teams build on top of it.
              </p>
              <p className="text-gray-400 text-sm leading-relaxed">
                If you want to contribute to the codebase, help shape the roadmap, or roll ShadowBar out to
                your area, please reach out. All <span className="font-semibold">codebase access and contribution requests</span> should go
                through{" "}
                <code className="bg-white/10 rounded px-1.5 py-0.5 text-xs">
                  devavarapu.yaswanth@barclays.com
                </code>{" "}
                (Team BPAZ) – via email or a direct message on Microsoft Teams. Idea initiated by{" "}
                <span className="font-semibold">Ninad Shete</span>, with the working team led by{" "}
                <span className="font-semibold">Yash &amp; Satya</span>.
              </p>
              <div className="flex flex-wrap items-center gap-3 pt-3">
                <button
                  type="button"
                  onClick={() => setShowContributionModal(true)}
                  className="inline-flex items-center gap-2 rounded-full bg-white/10 px-4 py-2 text-sm font-medium text-white hover:bg-white/20 transition-colors"
                >
                  <ArrowRight className="h-4 w-4" />
                  Request codebase access
                </button>
                <span className="text-xs text-gray-500">
                  When you request access, mention your team, primary use cases, and how you plan to help
                  colleagues create real‑world wins with ShadowBar.
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Contribution Modal */}
      {showContributionModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm">
          <div className="relative w-full max-w-xl rounded-3xl border border-white/15 bg-gradient-to-b from-black/90 via-zinc-900/95 to-black/90 p-6 shadow-[0_24px_80px_rgba(0,0,0,0.9)]">
            <div className="absolute inset-px pointer-events-none rounded-3xl bg-[radial-gradient(circle_at_top,_rgba(255,255,255,0.04),_transparent_55%)]" />
            <button
              type="button"
              onClick={() => setShowContributionModal(false)}
              className="relative ml-auto flex h-8 w-8 items-center justify-center rounded-full bg-black/40 text-gray-300 hover:text-white hover:bg-black/70 transition-colors"
              aria-label="Close"
            >
              <X className="h-4 w-4" />
            </button>
            <div className="relative mt-2 space-y-4 text-sm text-gray-200">
              <h3 className="text-lg font-semibold">ShadowBar Contribution &amp; Access</h3>
              {/* Q&A style terminal example – terminal-only answer */}
              <div className="mt-4 space-y-3">
                <TerminalBlock command={`shadowbar.input("How can I access ShadowBar or contribute to it?")`} />
                <TerminalBlock
                  command="bash"
                  output={[
                    "ShadowBar is an internal Barclays framework owned by Platform Engineering (Team BPAZ).",
                    "",
                    "To request access or contribute to the codebase:",
                    "  1. Email devavarapu.yaswanth@barclays.com (Team BPAZ), or",
                    "  2. Send a direct message on Microsoft Teams.",
                    "",
                    "In your message, include:",
                    "  • Your team and role.",
                    "  • 1–3 concrete use cases where ShadowBar will help colleagues.",
                    "  • Any systems or data sources your agents need to integrate with.",
                    "",
                    "Idea initiated by Ninad Shete; working team: Ninad Shete ,Yash & Satya (Team BPAZ).",
                  ].join("\n")}
                />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
