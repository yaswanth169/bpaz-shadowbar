"""
Purpose: Diagnose ShadowBar installation and configuration issues
LLM-Note:
  Dependencies: imports from [sys, os, shutil, pathlib, requests, rich.console, rich.panel, rich.table, __version__] | imported by [cli/main.py via handle_doctor()] | checks local files and backend connectivity
  Data flow: receives no args → checks system info → checks config files → checks API key → tests backend connectivity → displays results with [OK]/[X] indicators
  State/Effects: no state modifications | reads from filesystem | makes HTTP request | writes to stdout via rich.Console
  Integration: exposes handle_doctor() for CLI | helps users self-diagnose setup issues
  Performance: fast local checks (<100ms) | network check to backend (1-2s)
  Errors: lets errors crash naturally - no try-except unless absolutely needed
"""

import sys
import os
import shutil
from pathlib import Path
import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()


def handle_doctor():
    """Run comprehensive diagnostics on ShadowBar installation."""
    from ... import __version__

    console.print("\n[bold cyan]🔍 ShadowBar Diagnostics[/bold cyan]\n")

    # System checks
    system_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
    system_table.add_column("Check", style="cyan")
    system_table.add_column("Status")

    # Version
    system_table.add_row("Version", f"[green][OK][/green] {__version__}")

    # Python
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    python_path = sys.executable
    system_table.add_row("Python", f"[green][OK][/green] {python_version}")
    system_table.add_row("Python Path", f"[dim]{python_path}[/dim]")

    # Virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    venv_status = "[green][OK][/green] Virtual environment" if in_venv else "[yellow]○[/yellow] Global Python"
    system_table.add_row("Environment", venv_status)
    if in_venv:
        system_table.add_row("Venv Path", f"[dim]{sys.prefix}[/dim]")

    # Command location
    co_path = shutil.which('sb')
    if co_path:
        system_table.add_row("Command", f"[green][OK][/green] {co_path}")
    else:
        system_table.add_row("Command", "[red][X][/red] 'sb' not found in PATH")

    # Package location
    import shadowbar
    package_path = Path(shadowbar.__file__).parent
    system_table.add_row("Package", f"[dim]{package_path}[/dim]")

    console.print(Panel(system_table, title="[bold]System[/bold]", border_style="blue"))
    console.print()

    # Configuration checks
    config_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
    config_table.add_column("Check", style="cyan")
    config_table.add_column("Status")

    # Check for config.toml
    local_config = Path(".sb") / "config.toml"
    global_config = Path.home() / ".sb" / "config.toml"

    if local_config.exists():
        config_table.add_row("Config", f"[green][OK][/green] {local_config}")
        import toml
        config = toml.load(local_config)
        agent_name = config.get("agent", {}).get("name", "Not set")
        config_table.add_row("Agent Name", f"[dim]{agent_name}[/dim]")
    elif global_config.exists():
        config_table.add_row("Config", f"[green][OK][/green] {global_config}")
    else:
        config_table.add_row("Config", "[yellow]○[/yellow] Not found (optional)")

    # Check for keys
    local_keys = Path(".sb") / "keys" / "agent.key"
    global_keys = Path.home() / ".sb" / "keys" / "agent.key"

    if local_keys.exists():
        config_table.add_row("Keys", f"[green][OK][/green] {local_keys}")
    elif global_keys.exists():
        config_table.add_row("Keys", f"[green][OK][/green] {global_keys}")
    else:
        config_table.add_row("Keys", "[yellow]○[/yellow] Not found (run 'sb auth' to create)")

    # Check for API key
    api_key = os.getenv("SHADOWBAR_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        api_key_display = f"{api_key[:20]}..." if len(api_key) > 20 else api_key
        config_table.add_row("API Key", f"[green][OK][/green] Found in environment")
        config_table.add_row("Key Preview", f"[dim]{api_key_display}[/dim]")
    else:
        # Check .env files
        from dotenv import load_dotenv
        local_env = Path(".env")
        global_env = Path.home() / ".sb" / "keys.env"

        if local_env.exists():
            load_dotenv(local_env)
            api_key = os.getenv("SHADOWBAR_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
            if api_key:
                config_table.add_row("API Key", f"[green][OK][/green] Found in .env")

        if not api_key and global_env.exists():
            load_dotenv(global_env)
            api_key = os.getenv("SHADOWBAR_API_KEY")
            if api_key:
                config_table.add_row("API Key", f"[green][OK][/green] Found in ~/.sb/keys.env")

        if not api_key:
            config_table.add_row("API Key", "[yellow]○[/yellow] Not configured (run 'sb auth')")

    console.print(Panel(config_table, title="[bold]Configuration[/bold]", border_style="green"))
    console.print()

    # Connectivity checks (only if API key exists)
    # Connectivity checks (only if API key exists)
    if api_key:
        connectivity_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
        connectivity_table.add_column("Check", style="cyan")
        connectivity_table.add_column("Status")

        # Check Anthropic API reachability
        try:
            response = requests.get("https://api.anthropic.com", timeout=5)
            if response.status_code == 200:
                connectivity_table.add_row("Anthropic API", "[green][OK][/green] https://api.anthropic.com")
            else:
                connectivity_table.add_row("Anthropic API", f"[yellow]⚠[/yellow] Status {response.status_code}")
        except Exception as e:
            connectivity_table.add_row("Anthropic API", f"[red][X][/red] Unreachable: {e}")

        console.print(Panel(connectivity_table, title="[bold]Connectivity[/bold]", border_style="magenta"))
        console.print()

        console.print(Panel(connectivity_table, title="[bold]Connectivity[/bold]", border_style="magenta"))
        console.print()

    console.print("[bold green]✅ Diagnostics complete![/bold green]\n")
    console.print("[dim]Run 'sb auth' if you need to authenticate[/dim]\n")
