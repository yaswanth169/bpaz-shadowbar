"""
Purpose: Display account status including balance, usage, and email configuration without re-authenticating
LLM-Note:
  Dependencies: imports from [os, toml, requests, pathlib, rich.console, rich.panel, dotenv.load_dotenv, jwt, address] | imported by [cli/main.py via handle_status()] | calls Anthropic API directly | tested by [tests/cli/test_cli_status.py]
  Data flow: receives no args → _load_api_key() checks ANTHROPIC_API_KEY from env/local .env → displays agent info from config.toml → displays API key status
  State/Effects: no state modifications | reads from env vars, .env, config.toml | writes to stdout via rich.Console and rich.Panel | does NOT update any files
  Integration: exposes handle_status() for CLI | similar to authenticate() but read-only | relies on address module for signature generation | uses requests for HTTP calls | displays Rich panel with account info | checks SHADOWBAR_API_KEY in 3 locations (priority: env var > local .env > global ~/.sb/keys.env)
  Performance: network call to backend (1-2s) | signature generation is fast (<10ms) | file I/O for config and .env files
  Errors: fails gracefully if SHADOWBAR_API_KEY not found (prints message to run 'sb auth') | fails if keys missing in .sb/keys/ | fails if backend unreachable (prints HTTP error) | handles response errors with status code display
"""

import os
import toml
import requests
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv

console = Console()


def _load_api_key() -> str:
    """Load SHADOWBAR_API_KEY from environment.

    Checks in order:
    1. Environment variable
    2. Local .env file
    3. Global ~/.sb/keys.env file

    Returns:
        API key if found, None otherwise
    """
    # Check environment variable first
    api_key = os.getenv("SHADOWBAR_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        return api_key

    # Check local .env
    local_env = Path(".env")
    if local_env.exists():
        load_dotenv(local_env)
        api_key = os.getenv("SHADOWBAR_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        if api_key:
            return api_key

    # Check global ~/.sb/keys.env
    global_env = Path.home() / ".sb" / "keys.env"
    if global_env.exists():
        load_dotenv(global_env)
        api_key = os.getenv("SHADOWBAR_API_KEY")
        if api_key:
            return api_key

    return None


def _load_config() -> dict:
    """Load config from .sb/config.toml or ~/.sb/config.toml.

    Returns:
        Config dict if found, empty dict otherwise
    """
    # Check local .sb/config.toml first
    local_config = Path(".sb") / "config.toml"
    if local_config.exists():
        return toml.load(local_config)

    # Check global ~/.sb/config.toml
    global_config = Path.home() / ".sb" / "config.toml"
    if global_config.exists():
        return toml.load(global_config)

    return {}


def handle_status():
    """Check account status without re-authenticating.

    Shows:
    - Agent ID
    - Email address
    - Balance (remaining credits)
    - Total spent
    - Last seen
    - Warnings if balance is low
    """
    # Load API key
    api_key = _load_api_key()
    if not api_key:
        console.print("\n[X] [bold red]No API key found[/bold red]")
        console.print("\n[cyan]Authenticate first:[/cyan]")
        console.print("  [bold]sb init[/bold]     Initialize project and set API key\n")
        return

    # Load config for agent info
    config = _load_config()
    agent_info = config.get("agent", {})

    # Build info display
    api_key_display = f"{api_key[:20]}..." if len(api_key) > 20 else api_key

    info_lines = [
        f"[cyan]Agent Name:[/cyan] {agent_info.get('name', 'Not configured')}",
        f"[cyan]API Key:[/cyan] {api_key_display}",
        f"[cyan]Provider:[/cyan] Anthropic (Claude)",
    ]

    console.print("\n")
    console.print(Panel.fit(
        "\n".join(info_lines),
        title="📊 Account Status",
        border_style="cyan"
    ))

    console.print("\n[yellow][i] Tips:[/yellow]")
    console.print("   • ShadowBar uses your Anthropic API key directly")
    console.print("   • No external account management required\n")
