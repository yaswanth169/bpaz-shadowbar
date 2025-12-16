"""
Purpose: Entry point for ShadowBar CLI application using Typer framework with Rich formatting

ShadowBar CLI - Barclays Internal AI Agent Framework

Commands:
  - sb create <name>   Create new agent project
  - sb init            Initialize in current directory
  - sb doctor          Diagnose installation
  - sb status          Check agent status
"""

import typer
from rich.console import Console
from typing import Optional

from .. import __version__

console = Console()
app = typer.Typer(add_completion=False, no_args_is_help=False)


def version_callback(value: bool):
    if value:
        console.print(f"sb {__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-v", callback=version_callback, is_eager=True),
    browser: Optional[str] = typer.Option(None, "-b", "--browser", help="Quick browser command"),
):
    """ShadowBar - Barclays Internal AI Agent Framework."""
    if browser:
        from .commands.browser_commands import handle_browser
        handle_browser(browser)
        raise typer.Exit()
    if ctx.invoked_subcommand is None:
        _show_help()


def _show_help():
    """Show help message."""
    console.print()
    console.print(f"[bold cyan]sb[/bold cyan] - ShadowBar v{__version__}")
    console.print()
    console.print("Barclays Internal AI Agent Framework - Powered by Anthropic Claude.")
    console.print()
    console.print("[bold]Quick Start:[/bold]")
    console.print("  [cyan]sb create my-agent[/cyan]                Create new agent project")
    console.print("  [cyan]cd my-agent && python agent.py[/cyan]   Run your agent")
    console.print()
    console.print("[bold]Commands:[/bold]")
    console.print("  [green]create[/green]  <name>     Create new project")
    console.print("  [green]init[/green]              Initialize in current directory")
    console.print("  [green]auth[/green]              Generate agent identity keys")
    console.print("  [green]status[/green]            Check agent status")
    console.print("  [green]doctor[/green]            Diagnose installation")
    console.print()
    console.print("[bold]Configuration:[/bold]")
    console.print("  Agent config:    .sb/")
    console.print("  Logs:            .sb/logs/")
    console.print("  Sessions:        .sb/sessions/")
    console.print()
    console.print("[bold]LLM Provider:[/bold] Anthropic Claude (claude-sonnet-4-5)")
    console.print()


@app.command()
def init(
    template: Optional[str] = typer.Option(None, "-t", "--template", help="Template: minimal, playwright, custom"),
    yes: bool = typer.Option(False, "-y", "--yes", help="Skip prompts"),
    key: Optional[str] = typer.Option(None, "--key", help="API key"),
    description: Optional[str] = typer.Option(None, "--description", help="Description for custom template"),
    force: bool = typer.Option(False, "--force", help="Overwrite existing files"),
):
    """Initialize project in current directory."""
    from .commands.init import handle_init
    handle_init(ai=None, key=key, template=template, description=description, yes=yes, force=force)


@app.command()
def create(
    name: Optional[str] = typer.Argument(None, help="Project name"),
    template: Optional[str] = typer.Option(None, "-t", "--template", help="Template: minimal, playwright, custom"),
    yes: bool = typer.Option(False, "-y", "--yes", help="Skip prompts"),
    key: Optional[str] = typer.Option(None, "--key", help="API key"),
    description: Optional[str] = typer.Option(None, "--description", help="Description for custom template"),
):
    """Create new project."""
    from .commands.create import handle_create
    handle_create(name=name, ai=None, key=key, template=template, description=description, yes=yes)


@app.command()
def auth(service: Optional[str] = typer.Argument(None, help="Service: google, microsoft")):
    """Generate or manage agent identity keys."""
    if service == "microsoft":
        from .commands.auth_commands import handle_microsoft_auth
        handle_microsoft_auth()
    else:
        from .commands.auth_commands import handle_auth
        handle_auth()


@app.command()
def status():
    """Check agent status."""
    from .commands.status_commands import handle_status
    handle_status()


@app.command()
def reset():
    """Reset agent identity (destructive)."""
    from .commands.reset_commands import handle_reset
    handle_reset()


@app.command()
def doctor():
    """Diagnose installation."""
    from .commands.doctor_commands import handle_doctor
    handle_doctor()


@app.command()
def browser(command: str = typer.Argument(..., help="Browser command")):
    """Browser automation."""
    from .commands.browser_commands import handle_browser
    handle_browser(command)


def cli():
    """Entry point."""
    app()


if __name__ == "__main__":
    cli()
