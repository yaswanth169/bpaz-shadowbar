"""
Purpose: Export all useful tools and utilities for shadowbar agents (Microsoft-only)
LLM-Note:
  Dependencies: imports from [memory, outlook, microsoft_calendar, web_fetch, shell, diff_writer, tui.pick, terminal, todo_list, slash_command] | imported by [__init__.py main package] | re-exports tools for agent consumption
  Data flow: agent imports from useful_tools -> accesses tool functions/classes directly
  State/Effects: no state | pure re-exports | lazy loading for heavy dependencies
  Integration: exposes Memory, Outlook, MicrosoftCalendar, WebFetch, Shell, DiffWriter, TodoList (tool classes) | pick, yes_no, autocomplete (TUI helpers) | SlashCommand (extension point)
  Errors: ImportError if dependency not installed (e.g., httpx for Outlook/MicrosoftCalendar)
"""

from .memory import Memory
from .outlook import Outlook
from .microsoft_calendar import MicrosoftCalendar
from .web_fetch import WebFetch
from .shell import Shell
from .diff_writer import DiffWriter
from ..tui import pick
from .terminal import yes_no, autocomplete
from .todo_list import TodoList
from .slash_command import SlashCommand

# Browser automation (optional - requires playwright)
try:
    from .browser import Browser
    BROWSER_AVAILABLE = True
except ImportError:
    Browser = None
    BROWSER_AVAILABLE = False

__all__ = [
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
]

# Add Browser if available
if BROWSER_AVAILABLE:
    __all__.append("Browser")
