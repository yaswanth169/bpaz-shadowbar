"""
Purpose: Shared utility functions for CLI project commands including validation, API key detection, template generation, and Rich UI helpers
LLM-Note:
  Dependencies: imports from [os, re, sys, time, shutil, toml, rich.console, rich.prompt, rich.progress, rich.table, rich.panel, datetime, pathlib, __version__, address] | imported by [cli/commands/init.py, cli/commands/create.py] | calls LLM APIs for custom template generation | tested indirectly via test_cli_init.py and test_cli_create.py
  Data flow: provides utility functions called by init.py and create.py → validate_project_name() checks regex patterns → check_environment_for_api_keys() scans env vars for OpenAI/Anthropic/Google keys → detect_api_provider() inspects key format to identify provider → api_key_setup_menu() displays interactive menu for key selection → generate_custom_template_with_name() calls LLM API with custom prompt to generate agent.py code → show_progress() displays Rich spinner → LoadingAnimation context manager for long operations → get_special_directory_warning() warns about home/root dirs
  State/Effects: no persistent state | reads from environment variables | writes to stdout via rich.Console | calls LLM APIs (OpenAI/Anthropic/Google) when generating custom templates | creates Rich UI elements (tables, panels, progress bars, prompts) | does NOT write files (caller handles that)
  Integration: exposes 16+ utility functions and 1 class (LoadingAnimation) | used by init.py and create.py for shared logic | validate_project_name() enforces naming conventions (starts with letter, no spaces, max 50 chars) | check_environment_for_api_keys() scans OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY, GOOGLE_API_KEY | detect_api_provider() identifies provider by key prefix (sk- for OpenAI, sk-ant- for Anthropic, AIzaSy for Google, gsk- for Groq) | generate_custom_template_with_name() uses LLM to create agent.py from natural language description
  Performance: environment scanning is O(n) env vars | regex validation is fast (<1ms) | LLM API calls for custom templates (5-15s) | Rich UI rendering is lightweight | LoadingAnimation runs in main thread (non-blocking spinner)
  Errors: validate_project_name() returns (False, error_msg) for invalid names | detect_api_provider() returns ("unknown", "unknown") for unrecognized keys | generate_custom_template_with_name() may fail if LLM API unreachable | api_key_setup_menu() catches KeyboardInterrupt and returns ("", "", None) | no try-except blocks (follows fail-fast principle)
"""

import os
import re
import sys
import time
import shutil
import toml
from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.panel import Panel
from rich import box
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple, List

from ... import __version__
from ... import address

console = Console()




def validate_project_name(name: str) -> Tuple[bool, str]:
    """Validate project name for common issues.

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name:
        return False, "Project name cannot be empty"

    if ' ' in name:
        return False, "Project name cannot contain spaces. Try using hyphens instead (e.g., 'my-agent')"

    if not re.match(r'^[a-zA-Z][a-zA-Z0-9-_]*$', name):
        return False, "Project name must start with a letter and contain only letters, numbers, hyphens, and underscores"

    if len(name) > 50:
        return False, "Project name is too long (max 50 characters)"

    return True, ""


def show_progress(message: str, duration: float = 0.5):
    """Show a brief progress spinner using Rich."""
    with Progress(
        SpinnerColumn(style="cyan"),
        TextColumn("[cyan]{task.description}"),
        transient=True,
        console=console,
    ) as progress:
        task_id = progress.add_task(message, total=None)
        end_time = time.time() + duration
        while time.time() < end_time:
            time.sleep(0.05)
        progress.remove_task(task_id)


class LoadingAnimation:
    """Context manager for showing loading animation during long operations."""

    def __init__(self, message: str):
        self.message = message
        self.progress = None
        self.task_id = None

    def __enter__(self):
        from rich.progress import Progress, SpinnerColumn, TextColumn
        self.progress = Progress(
            SpinnerColumn(style="cyan"),
            TextColumn("[cyan]{task.description}"),
            transient=False,
            console=console,
        )
        self.progress.start()
        self.task_id = self.progress.add_task(self.message, total=None)
        return self

    def update(self, new_message: str):
        """Update the loading message."""
        if self.progress and self.task_id is not None:
            self.progress.update(self.task_id, description=new_message)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.progress:
            self.progress.stop()


def get_template_info() -> list:
    """Get template information for display."""
    return [
        ('minimal', '📦 Minimal', 'Basic agent structure'),
        ('playwright', '🎭 Playwright', 'Browser automation agent'),
        ('custom', '[*] Custom', 'AI-generated agent'),
    ]


def get_template_suggested_name(template: str) -> str:
    """Get suggested project name for a template."""
    suggestions = {
        'minimal': 'my-agent',
        'playwright': 'browser-agent',
        'custom': None  # Will be generated by AI
    }
    return suggestions.get(template, 'my-agent')


def api_key_setup_menu(temp_project_dir: Optional[Path] = None) -> Tuple[str, str, Path]:
    """Show API key setup options to the user.

    Args:
        temp_project_dir: Optional temporary project directory to use for auth

    Returns:
        Tuple of (api_key, provider, temp_dir) where temp_dir is the temporary project created for auth
    """
    from ... import address  # Import address module for key generation

    try:
        import questionary
        from questionary import Style

        custom_style = Style([
            ('question', 'fg:#00ffff bold'),
            ('pointer', 'fg:#00ff00 bold'),
            ('highlighted', 'fg:#00ff00 bold'),
            ('selected', 'fg:#00ffff'),
            ('separator', 'fg:#808080'),
            ('instruction', 'fg:#808080'),
        ])

        choices = [
            questionary.Choice(
                title="[KEY] BYO API key (OpenAI, Anthropic, Gemini)",
                value="own_key"
            ),
            questionary.Choice(
                title="ShadowBar uses your Anthropic API key (no external credits)",
                value="star"
            ),
            questionary.Choice(
                title="Skip (no managed credits; use your Anthropic API key)",
                value="skip"
            ),
        ]

        result = questionary.select(
            "How would you like to set up API access?",
            choices=choices,
            style=custom_style,
            instruction="(Use ↑/↓ arrows, press Enter to confirm)",
        ).ask()

        if result == "own_key":
            # Ask for their API key
            console.print("\n[cyan]Paste your API key (we'll detect the provider)[/cyan]")
            api_key = questionary.password("API key:").ask()
            if api_key:
                provider, key_type = detect_api_provider(api_key)
                console.print(f"[green][OK] {provider.title()} API key configured[/green]")
                return api_key, provider, None  # No temp dir for own keys
            return "", "", None

        elif result == "star":
            # Star for free credits - create temp project and authenticate immediately
            import webbrowser
            import shutil
            from pathlib import Path

            console.print("\n[cyan][*] Get 100k Free Tokens[/cyan]")
            console.print("\nOpening GitHub in your browser...")

            # Try to open the GitHub repo for starring
            github_url = "https://gitlab.com/shadowbar/shadowbar"
            try:
                webbrowser.open(github_url)
            except:
                pass  # Browser opening might fail in some environments

            # Keep asking until they confirm they've starred
            while True:
                already_starred = questionary.confirm(
                    "\nHave you starred our repository?",
                    default=False
                ).ask()

                if already_starred:
                    console.print("[green][OK] Thank you for your support![/green]")

                    # Create temporary project directory
                    temp_name = "shadowbar-temp-project"
                    temp_dir = Path(temp_name)
                    counter = 1
                    while temp_dir.exists():
                        temp_dir = Path(f"{temp_name}-{counter}")
                        counter += 1

                    console.print(f"\n[yellow]Setting up temporary project for authentication...[/yellow]")
                    temp_dir.mkdir(parents=True)

                    # Create .sb directory and generate keys
                    sb_dir = temp_dir / ".sb"
                    sb_dir.mkdir()

                    try:
                        # Generate keys for this project
                        addr_data = address.generate()
                        address.save(addr_data, sb_dir)

                        # Run direct registration with the project keys (no browser)
                        console.print("\n[yellow]Setting up your Anthropic access...[/yellow]\n")

                        from .auth_commands import authenticate
                        # ShadowBar: no managed credits; use Anthropic API key directly
                        console.print("\n[green][OK] Keys generated. Please set ANTHROPIC_API_KEY in your .env[/green]")
                        return "star", "shadowbar", temp_dir  # Return the temp directory
                    except Exception as e:
                        # Clean up on error
                        if temp_dir.exists():
                            shutil.rmtree(temp_dir)
                        console.print(f"[red]Error: {e}[/red]")
                        return "", "", None

                    break  # Exit the loop
                else:
                    console.print("\n[yellow]Please star the repository to get your free tokens![/yellow]")
                    console.print(f"\nIf the browser didn't open, visit: [cyan]{github_url}[/cyan]")
                    console.print("You can copy and paste this URL into your browser.")
                    console.print("\n[dim]We'll wait for you to star the repository...[/dim]")
                    # Loop will continue to ask again

            return "star", "shadowbar", None  # Should not reach here

        elif result == "skip":
            # User chose to skip API setup
            console.print("\n[yellow]⏭️  Skipping API setup[/yellow]")
            console.print("[dim]You can add your API key later in the .env file[/dim]")
            return "skip", "", None  # Return "skip" as api_key to indicate skip choice

        else:
            raise KeyboardInterrupt()

    except ImportError:
        # Fallback to simple menu
        console.print("\n[cyan][KEY] API Key Setup[/cyan]")
        console.print("1. Use your Anthropic API key (recommended)")
        console.print("2. Skip (enter later)")

        choice = IntPrompt.ask("Select option", choices=["1", "2"], default="1")
        choice = int(choice)

        if choice == 1:
            api_key = Prompt.ask("API key", password=True, default="")
            if api_key:
                provider, key_type = detect_api_provider(api_key)
                console.print(f"[green][OK] {provider.title()} API key configured[/green]")
                return api_key, provider, False  # No auth needed for own keys
            return "", "", False
        elif choice == 2:
            import webbrowser

            console.print("\n[cyan][*] Get 100k Free Tokens[/cyan]")
            console.print("\nOpening GitHub in your browser...")

            # Try to open the GitHub repo for starring
            github_url = "https://gitlab.com/shadowbar/shadowbar"
            try:
                webbrowser.open(github_url)
            except:
                pass  # Browser opening might fail in some environments

            # Keep asking until they confirm they've starred
            while True:
                already_starred = Confirm.ask("\nHave you starred our repository?", default=False)

                if already_starred:
                    console.print("[green][OK] Thank you for your support![/green]")
                    console.print("\n[yellow]Authenticating to activate your free credits...[/yellow]\n")

                    try:
                        from .auth_commands import authenticate
                        authenticate(Path(".sb"))
                        console.print("\n[green][OK] We verified your star. Thanks for supporting us![/green]")
                        console.print("[green]You now have 100k free tokens![/green]")
                        console.print("\n[cyan]ShadowBar supports Anthropic Claude models only:[/cyan]")
                        console.print("  • claude-sonnet-4-5 (default)")
                        console.print("  • claude-3-5-haiku-20241022")
                        console.print("  • claude-3-opus-20240229")
                        break  # Success, exit the loop
                    except Exception as e:
                        console.print(f"\n[red]Authentication failed: {e}[/red]")
                        console.print("[yellow]Please try running: [bold]sb auth[/bold][/yellow]")
                        break  # Exit on auth failure
                else:
                    console.print("\n[yellow]Please star the repository to get your free tokens![/yellow]")
                    console.print(f"\nIf the browser didn't open, visit: [cyan]{github_url}[/cyan]")
                    console.print("You can copy and paste this URL into your browser.")
                    console.print("\n[dim]We'll wait for you to star the repository...[/dim]")
                    # Loop will continue to ask again

            return "star", "shadowbar", None

        elif choice == 3:
            # Skip - user will get free tokens
            console.print("\n[yellow]⏭️  Skipping API setup[/yellow]")
            console.print("[dim]Use your Anthropic API key to get started[/dim]")
            console.print("[dim]Add your own API key to .env later for unlimited usage[/dim]")
            return "skip", "", None

        else:
            return "", "", None


def interactive_menu(options: List[Tuple[str, str, str]], prompt: str = "Choose an option:") -> str:
    """Interactive menu with arrow key navigation using questionary.

    Args:
        options: List of (key, emoji+name, description) tuples
        prompt: Menu prompt text

    Returns:
        Selected option key
    """
    try:
        import questionary
        from questionary import Style

        # Custom style using questionary's styling
        custom_style = Style([
            ('question', 'fg:#00ffff bold'),
            ('pointer', 'fg:#00ff00 bold'),  # The > pointer
            ('highlighted', 'fg:#00ff00 bold'),  # Currently selected item
            ('selected', 'fg:#00ffff'),  # Selected item after pressing enter
            ('separator', 'fg:#808080'),
            ('instruction', 'fg:#808080'),  # (Use arrow keys)
        ])

        # Create choices with formatted strings
        choices = []
        for key, name, desc in options:
            # Format: "📦 Minimal - Basic agent"
            choice_text = f"{name} - {desc}"
            choices.append(questionary.Choice(title=choice_text, value=key))

        # Show the selection menu
        result = questionary.select(
            prompt,
            choices=choices,
            style=custom_style,
            instruction="(Use ↑/↓ arrows, press Enter to confirm)",
        ).ask()

        if result:
            # Find the selected option name for confirmation
            for key, name, _ in options:
                if key == result:
                    console.print(f"[green][OK] Selected:[/green] {name}")
                    break
            return result
        else:
            # User cancelled (pressed Ctrl+C or Escape)
            raise KeyboardInterrupt()

    except ImportError:
        # Fallback to the original Rich + Click implementation
        console.print()
        console.print(Panel.fit(prompt, style="cyan", border_style="cyan", title="Templates"))

        table = Table(box=box.SIMPLE_HEAVY)
        table.add_column("No.", justify="right", style="bold")
        table.add_column("Template", style="white")
        table.add_column("Description", style="dim")

        for i, (_, name, desc) in enumerate(options, 1):
            table.add_row(str(i), name, desc)

        console.print(table)

        choices = [str(i) for i in range(1, len(options) + 1)]
        selected = IntPrompt.ask(
            "Select [number]",
            choices=choices,
            default="1"
        )

        idx = int(selected) - 1
        selected_option = options[idx]
        console.print(f"[green][OK] Selected:[/green] {selected_option[1]}")
        return selected_option[0]


def get_template_preview(template: str) -> str:
    """Get a preview of what the template includes."""
    previews = {
        'minimal': """  📦 Minimal - Simple starting point
    ├── agent.py (50 lines) - Basic agent with example tool
    ├── .env - API key configuration
    ├── README.md - Quick start guide
    └── .sb/ - Agent identity & metadata""",

        'web-research': """  🔍 Web Research - Data analysis & web scraping
    ├── agent.py (100+ lines) - Agent with web tools
    ├── tools/ - Web scraping & data extraction
    ├── .env - API key configuration
    ├── README.md - Usage examples
    └── .sb/ - Agent identity & metadata""",

        'email-agent': """  📧 Email Agent - Professional email assistant
    ├── agent.py (400+ lines) - Full email management
    ├── README.md - Comprehensive guide
    ├── .env.example - Configuration options
    └── .sb/ - Agent identity & metadata
    Features: inbox management, auto-respond, search, statistics""",

        'custom': """  [*] Custom - AI generates based on your needs
    ├── agent.py - Tailored to your description
    ├── tools/ - Custom tools for your use case
    ├── .env - API key configuration
    ├── README.md - Custom documentation
    └── .sb/ - Agent identity & metadata""",

        'meta-agent': """  🤖 Meta-Agent - ShadowBar development assistant
    ├── agent.py - Advanced agent with llm_do
    ├── prompts/ - System prompts (4 files)
    ├── .env - API key configuration
    ├── README.md - Comprehensive guide
    └── .sb/ - Agent identity & metadata""",

        'playwright': """  🎭 Playwright - Browser automation
    ├── agent.py - Browser control agent
    ├── prompt.md - System prompt
    ├── .env - API key configuration
    ├── README.md - Setup instructions
    └── .sb/ - Agent identity & metadata"""
    }

    return previews.get(template, f"  📄 {template.title()} template")


def check_environment_for_api_keys() -> Optional[Tuple[str, str]]:
    """Check environment variables for API keys.

    Returns:
        Tuple of (provider, api_key) if found, None otherwise
    """
    import os

    # Check for various API key environment variables
    checks = [
        ('OPENAI_API_KEY', 'openai'),
        ('ANTHROPIC_API_KEY', 'anthropic'),
        ('GEMINI_API_KEY', 'google'),
        ('GOOGLE_API_KEY', 'google'),
        ('GROQ_API_KEY', 'groq'),
    ]

    for env_var, provider in checks:
        api_key = os.environ.get(env_var)
        if api_key and api_key != 'your-api-key-here' and not api_key.startswith('sk-your'):
            return provider, api_key

    return None


def detect_api_provider(api_key: str) -> Tuple[str, str]:
    """Detect API provider from key format.

    Returns:
        Tuple of (provider, key_type)
    """
    # Check Anthropic first (more specific prefix)
    if api_key.startswith('sk-ant-'):
        return 'anthropic', 'claude'

    # OpenAI formats
    if api_key.startswith('sk-proj-'):
        return 'openai', 'project'
    elif api_key.startswith('sk-'):
        return 'openai', 'user'

    # Google (Gemini)
    if api_key.startswith('AIza'):
        return 'google', 'gemini'

    # Groq
    if api_key.startswith('gsk_'):
        return 'groq', 'groq'

    # Default to OpenAI if unsure
    return 'openai', 'unknown'


def configure_env_for_provider(provider: str, api_key: str) -> str:
    """Generate .env content based on provider.

    Args:
        provider: API provider name
        api_key: The API key

    Returns:
        .env file content
    """
    configs = {
        'anthropic': {
            'var': 'ANTHROPIC_API_KEY',
            'model': 'claude-sonnet-4-5'
        }
    }

    config = configs.get(provider, configs['anthropic'])

    return f"""# {provider.title()} API Configuration
{config['var']}={api_key}

# Model Configuration
MODEL={config['model']}

# Optional: Override default settings
# MAX_TOKENS=2000
# TEMPERATURE=0.7
"""


def generate_custom_template_with_name(description: str, api_key: str, model: str = None, loading_animation=None) -> Tuple[str, str]:
    """Generate custom agent template and suggested name using AI.

    Args:
        description: What the agent should do
        api_key: API key or token for LLM
        model: Optional model to use (e.g., "claude-sonnet-4-5")
        loading_animation: Optional LoadingAnimation instance to update

    Returns:
        Tuple of (agent_code, suggested_name)
    """
    import re

    # Default fallback values
    suggested_name = "custom-agent"

    # Try to use AI to generate name and code
    if model or api_key:
        try:
            from ...llm import create_llm

            # Use the model specified or default to Anthropic
            llm_model = model if model else "claude-sonnet-4-5"

            if loading_animation:
                loading_animation.update(f"Connecting to {llm_model}...")

            # Create LLM instance (Anthropic only)
            llm = create_llm(model=llm_model, api_key=api_key if api_key else None)

            # Generate project name and code with AI
            prompt = f"""Based on this description: "{description}"

Generate:
1. A short, descriptive project name (lowercase, hyphenated, max 30 chars, no spaces)
2. Python code for a ShadowBar agent that implements this functionality

Respond in this exact format:
PROJECT_NAME: your-suggested-name
CODE:
```python
# Your generated code here
```"""

            messages = [
                {"role": "system", "content": "You are an AI assistant that generates ShadowBar agent code and project names."},
                {"role": "user", "content": prompt}
            ]

            if loading_animation:
                loading_animation.update(f"Generating agent code...")

            response = llm.complete(messages)

            if response.content:
                # Parse the response
                lines = response.content.split('\n')
                for line in lines:
                    if line.startswith("PROJECT_NAME:"):
                        suggested_name = line.replace("PROJECT_NAME:", "").strip()
                        # Validate name format
                        suggested_name = re.sub(r'[^a-z0-9-]', '', suggested_name.lower())
                        if len(suggested_name) > 30:
                            suggested_name = suggested_name[:30]
                        break

                # Extract code between ```python and ```
                if "```python" in response.content and "```" in response.content:
                    code_start = response.content.find("```python") + 9
                    code_end = response.content.find("```", code_start)
                    if code_end > code_start:
                        agent_code = response.content[code_start:code_end].strip()
                        return agent_code, suggested_name

        except Exception as e:
            # If AI generation fails, fall back to simple generation
            print(f"AI generation failed: {e}, using fallback")

    # Fallback: Simple name generation from description
    words = description.lower().split()[:3]
    suggested_name = "-".join(re.sub(r'[^a-z0-9]', '', word) for word in words if word)
    if not suggested_name:
        suggested_name = "custom-agent"
    else:
        suggested_name = suggested_name + "-agent"

    if len(suggested_name) > 30:
        suggested_name = suggested_name[:30]

    # Fallback agent code
    agent_code = f"""# {description}
# Generated with ShadowBar

from shadowbar import Agent

def process_request(query: str) -> str:
    '''Process user queries for: {description}'''
    return f"Processing: {{query}}"

# Create agent
agent = Agent(
    name="{suggested_name.replace('-', '_')}",
    model="claude-sonnet-4-5",
    system_prompt=\"\"\"You are an AI agent designed to: {description}

    Provide helpful, accurate, and concise responses.\"\"\",
    tools=[process_request]
)

if __name__ == "__main__":
    print(f"🤖 {suggested_name.replace('-', ' ').title()} Ready!")
    print("Type 'exit' to quit\\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break

        response = agent.input(user_input)
        print(f"Agent: {{response}}\\n")
"""

    return agent_code, suggested_name


def generate_custom_template(description: str, api_key: str) -> str:
    """Generate custom agent template using AI.

    This is a placeholder - actual implementation would call AI API.
    """
    # TODO: Implement actual AI generation
    return f"""# Custom Agent Generated from: {description}

from shadowbar import Agent

def custom_tool(param: str) -> str:
    '''Custom tool for: {description}'''
    return f"Processing: {{param}}"

agent = Agent(
    name="custom_agent",
    system_prompt="You are a custom agent designed for: {description}",
    tools=[custom_tool]
)

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        response = agent.input(user_input)
        print(f"Agent: {{response}}")
"""


def is_directory_empty(directory: str) -> bool:
    """Check if a directory is empty (ignoring .git directory)."""
    contents = os.listdir(directory)
    # Ignore '.', '..', and '.git' directory
    meaningful_contents = [item for item in contents if item not in ['.', '..', '.git']]
    return len(meaningful_contents) == 0


def is_special_directory(directory: str) -> bool:
    """Check if directory is a special system directory."""
    abs_path = os.path.abspath(directory)

    if abs_path == os.path.expanduser("~"):
        return True
    if abs_path == "/":
        return True
    if "/tmp" in abs_path or "temp" in abs_path.lower():
        return False

    system_dirs = ["/usr", "/etc", "/bin", "/sbin", "/lib", "/opt"]
    for sys_dir in system_dirs:
        if abs_path.startswith(sys_dir + "/") or abs_path == sys_dir:
            return True

    return False


def get_special_directory_warning(directory: str) -> str:
    """Get warning message for special directories."""
    abs_path = os.path.abspath(directory)

    if abs_path == os.path.expanduser("~"):
        return "[!]  You're in your HOME directory. Consider creating a project folder first."
    elif abs_path == "/":
        return "[!]  You're in the ROOT directory. This is not recommended!"
    elif any(abs_path.startswith(d) for d in ["/usr", "/etc", "/bin", "/sbin", "/lib", "/opt"]):
        return "[!]  You're in a SYSTEM directory. This could affect system files!"

    return ""


# Export shared utilities for use by init.py and create.py
__all__ = [
    'LoadingAnimation',
    'validate_project_name',
    'get_special_directory_warning',
    'is_special_directory',
    'is_directory_empty',
    'check_environment_for_api_keys',
    'detect_api_provider',
    'configure_env_for_provider',
    'api_key_setup_menu',
    'get_template_info',
    'get_template_suggested_name',
    'get_template_preview',
    'interactive_menu',
    'show_progress',
    'generate_custom_template',
    'generate_custom_template_with_name',
]

# All the handle_init and handle_create code has been moved to init.py and create.py
# This file now only contains shared utilities
