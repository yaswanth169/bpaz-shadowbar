"""ShadowBar - Barclays Internal AI Agent Framework.

A Python framework for building collaborative AI agents with:
- Function-based tools that convert automatically
- Anthropic Claude LLM support
- Multi-agent networking via relay server
- Interactive debugging with @xray decorator
- Persistent memory and logging
"""

__version__ = "1.0.0"

# Auto-load .env files for the entire framework
from dotenv import load_dotenv
from pathlib import Path as _Path

# Load from current working directory (where user runs their script)
# NOT from the module's location (framework directory)
load_dotenv(_Path.cwd() / ".env")

from .agent import Agent
from .tool_factory import create_tool_from_function
from .llm import LLM
from .logger import Logger
from .llm_do import llm_do
from .prompts import load_system_prompt
from .xray import xray
from .decorators import replay, xray_replay
from .useful_tools import (
    Memory, Outlook, MicrosoftCalendar,
    WebFetch, Shell, DiffWriter, pick, yes_no, autocomplete,
    TodoList, SlashCommand
)

# Browser automation (optional - requires playwright)
try:
    from .useful_tools import Browser
except ImportError:
    Browser = None
from .auto_debug_exception import auto_debug_exception
from .connect import connect, RemoteAgent
from .events import (
    after_user_input,
    before_llm,
    after_llm,
    before_each_tool,
    before_tools,
    after_each_tool,
    after_tools,
    on_error,
    on_complete
)

__all__ = [
    "Agent",
    "LLM",
    "Logger",
    "create_tool_from_function",
    "llm_do",
    "load_system_prompt",
    "xray",
    "replay",
    "xray_replay",
    "Memory",
    "Outlook",
    "MicrosoftCalendar",
    "WebFetch",
    "Shell",
    "DiffWriter",
    "pick",
    "yes_no",
    "autocomplete",
    "TodoList",
    "SlashCommand",
    "auto_debug_exception",
    "connect",
    "RemoteAgent",
    "after_user_input",
    "before_llm",
    "after_llm",
    "before_each_tool",
    "before_tools",
    "after_each_tool",
    "after_tools",
    "on_error",
    "on_complete",
]

# Add Browser if available
if Browser is not None:
    __all__.append("Browser")


