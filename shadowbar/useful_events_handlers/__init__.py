"""
Useful event handlers for shadowbar agents.

Event handlers fire at specific points in the agent lifecycle.
Use on_events parameter to register them with your agent.

Usage:
    from shadowbar import Agent
    from shadowbar.useful_events_handlers import reflect

    agent = Agent("assistant", on_events=[reflect])
"""

from .reflect import reflect

__all__ = ['reflect']
