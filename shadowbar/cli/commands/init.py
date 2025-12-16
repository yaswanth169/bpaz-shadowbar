"""
Purpose: Initialize ShadowBar project in current directory with template files, authentication, and configuration
LLM-Note:
  Dependencies: imports from [os, sys, shutil, subprocess, toml, datetime, pathlib, rich.console, rich.prompt, __version__, address, auth_commands.authenticate, project_cmd_lib] | imported by [cli/main.py via handle_init()] | uses templates from [cli/templates/{minimal,playwright}] | tested by [tests/cli/test_cli_init.py]
  Data flow: receives args (ai, key, template, description, yes, force) from CLI parser → ensure_global_config() creates ~/.sb/ with master keypair if needed → check_environment_for_api_keys() detects existing keys → api_key_setup_menu() or detect_api_provider() validates API key → generate_custom_template() if template='custom' → copy template files from cli/templates/{template}/ to current dir → create/update .env with API keys from ~/.sb/keys.env → create .sb/config.toml with project metadata and global identity → copy vibe coding docs to .sb/docs/ and project root → update .gitignore if git repo → display success message with next steps
  State/Effects: modifies ~/.sb/ (config.toml, keys.env, keys/, logs/) on first run | writes to current dir: .sb/config.toml, .env, agent.py (if template), .gitignore, sb-vibecoding-principles-docs-contexts-all-in-one.md | copies template files (agent.py, requirements.txt, etc.) | creates temp_project_dir during auth flow (cleaned up at end) | writes to stdout via rich.Console
  Integration: exposes handle_init(ai, key, template, description, yes, force) | calls ensure_global_config() to create global identity | calls authenticate(global_co_dir, save_to_project=False) for managed keys | uses template files from cli/templates/ | relies on project_cmd_lib for shared functions | uses address.generate() and address.save() for Ed25519 keypair | template options: 'minimal', 'playwright', 'custom', 'none' (default)
  Performance: authenticate() makes network call to backend (2-5s) | generate_custom_template() calls LLM API if template='custom' | template file copying is O(n) files | config/env file operations are I/O bound
  Errors: fails if cli/templates/{template}/ not found | fails if API key invalid during authenticate() | warns if directory not empty (requires --force or confirmation) | warns for special directories (home, root, system dirs) | skips duplicate .env keys (safe append) | creates temp_project_dir but cleans up on completion
"""

import os
import sys
import shutil
import subprocess
import toml
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.text import Text

from ... import __version__
from ... import address
from .auth_commands import authenticate

# Import shared functions from project_cmd_lib
from .project_cmd_lib import (
    get_special_directory_warning,
    is_directory_empty,
    check_environment_for_api_keys,
    api_key_setup_menu,
    detect_api_provider,
    get_template_info,
    interactive_menu,
    generate_custom_template,
    show_progress,
    configure_env_for_provider
)

console = Console()


def ensure_global_config() -> Dict[str, Any]:
    """Simple function to ensure ~/.sb/ exists with global identity."""
    global_dir = Path.home() / ".sb"
    config_path = global_dir / "config.toml"

    # If exists, just load and return
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return toml.load(f)

    # First time - create global config
    console.print(f"\n[>] Welcome to ShadowBar!")
    console.print(f"[*] Setting up global configuration...")

    # Create directories
    global_dir.mkdir(exist_ok=True)
    (global_dir / "keys").mkdir(exist_ok=True)
    (global_dir / "logs").mkdir(exist_ok=True)

    # Generate master keys - fail fast if libraries missing
    addr_data = address.generate()
    address.save(addr_data, global_dir)
    console.print(f"  [OK] Generated master keypair")
    console.print(f"  [OK] Your address: {addr_data['short_address']}")

    # Create config (simplified - address/email now in .env)
    config = {
        "shadowbar": {
            "framework_version": __version__,
            "created": datetime.now().isoformat(),
        },
        "cli": {
            "version": "1.0.0",
        },
        "agent": {
            "algorithm": "ed25519",
            "default_model": "claude-sonnet-4-5",
            "max_iterations": 10,
            "created_at": datetime.now().isoformat(),
        },
    }

    # Save config
    with open(config_path, 'w', encoding='utf-8') as f:
        toml.dump(config, f)
    console.print(f"  [OK] Created ~/.sb/config.toml")

    # Create keys.env with config path and agent address
    keys_env = global_dir / "keys.env"
    if not keys_env.exists():
        with open(keys_env, 'w', encoding='utf-8') as f:
            f.write(f"AGENT_CONFIG_PATH={global_dir}\n")
            f.write(f"AGENT_ADDRESS={addr_data['address']}\n")
            f.write("# Your agent address (Ed25519 public key) is used for:\n")
            f.write("#   - Secure agent communication (encrypt/decrypt with private key)\n")
            f.write("#   - Authentication with ShadowBar (Anthropic) provider\n")
            f.write(f"#   - Email address: {addr_data['address'][:10]}@mail.shadowbar.ai\n")
        if sys.platform != 'win32':
            os.chmod(keys_env, 0o600)  # Read/write for owner only (Unix/Mac only)
    else:
        # Append if not exists
        existing = keys_env.read_text()
        if 'AGENT_CONFIG_PATH=' not in existing:
            with open(keys_env, 'a', encoding='utf-8') as f:
                f.write(f"AGENT_CONFIG_PATH={global_dir}\n")
        if 'AGENT_ADDRESS=' not in existing:
            with open(keys_env, 'a', encoding='utf-8') as f:
                f.write(f"AGENT_ADDRESS={addr_data['address']}\n")
    console.print(f"  [OK] Created ~/.sb/keys.env")

    return config


def handle_init(ai: Optional[bool], key: Optional[str], template: Optional[str],
                description: Optional[str], yes: bool, force: bool):
    """Initialize a ShadowBar project in the current directory."""
    # Ensure global config exists first
    global_config = ensure_global_config()
    global_identity = global_config.get("agent", {})

    current_dir = os.getcwd()
    project_name = os.path.basename(current_dir) or "my-agent"

    # Track temp directory for cleanup
    temp_project_dir = None

    # Header removed for cleaner output

    # Check for special directories
    warning = get_special_directory_warning(current_dir)
    if warning:
        console.print(f"[yellow]{warning}[/yellow]")
        if not yes and not Confirm.ask("[yellow]Continue anyway?[/yellow]"):
            console.print("[yellow]Initialization cancelled.[/yellow]")
            return

    # Check if directory is empty
    if not is_directory_empty(current_dir) and not force:
        existing_files = os.listdir(current_dir)[:5]
        console.print("[yellow][!]  Directory not empty[/yellow]")
        console.print(f"[yellow]Existing files: {', '.join(existing_files[:5])}[/yellow]")
        if not yes and not Confirm.ask("\n[yellow]Add ShadowBar to existing project?[/yellow]"):
            console.print("[yellow]Initialization cancelled.[/yellow]")
            return

    # Auto-detect API keys from environment (no menu, just detect)
    detected_keys = {}
    provider = None

    # Check for API keys in environment
    env_api = check_environment_for_api_keys()
    if env_api:
        provider, env_key = env_api
        detected_keys[provider] = env_key
        if not yes:
            console.print(f"[green][OK] Detected {provider.title()} API key[/green]")

    # If --key provided via flag, use it
    if key:
        provider, key_type = detect_api_provider(key)
        detected_keys[provider] = key

    # Template selection - default to 'none' (just add .sb folder) unless --template provided
    if not template:
        # No --template flag provided, just add ShadowBar config
        template = 'none'
        if not yes:
            console.print("\n[green][OK] Adding ShadowBar config (.sb folder)[/green] (use --template <name> for full templates)")
    # else: template has a specific value from --template <name>

    # Handle custom template
    custom_code = None
    if template == 'custom':
        if not description and not yes:
            console.print("\n[cyan]🤖 Describe your agent:[/cyan]")
            description = Prompt.ask("  What should your agent do?")
        elif not description:
            description = "A general purpose agent"

        show_progress("Generating custom template with AI...", 2.0)
        # Use detected key or empty string (will use SHADOWBAR_API_KEY after auth)
        template_key = list(detected_keys.values())[0] if detected_keys else ""
        custom_code = generate_custom_template(description, template_key)

    # Start initialization
    show_progress("Initializing ShadowBar project...", 1.0)

    # Get template directory
    cli_dir = Path(__file__).parent.parent
    template_dir = cli_dir / "templates" / template if template != 'none' else None

    if template_dir and not template_dir.exists() and template not in ['custom', 'none']:
        console.print(f"[red][X] Template '{template}' not found![/red]")
        return

    # Copy template files
    files_created = []
    files_skipped = []

    if template not in ['custom', 'none'] and template_dir and template_dir.exists():
        for item in template_dir.iterdir():
            # Skip hidden files except .env.example
            if item.name.startswith('.') and item.name != '.env.example':
                continue

            dest_path = Path(current_dir) / item.name

            if item.is_dir():
                # Copy directory
                if dest_path.exists() and not force:
                    files_skipped.append(f"{item.name}/ (already exists)")
                else:
                    if dest_path.exists():
                        shutil.rmtree(dest_path)
                    shutil.copytree(item, dest_path)
                    files_created.append(f"{item.name}/")
            else:
                # Skip .env.example, we'll create .env directly
                if item.name == '.env.example':
                    continue
                # Copy file
                if dest_path.exists() and not force:
                    files_skipped.append(f"{item.name} (already exists)")
                else:
                    shutil.copy2(item, dest_path)
                    files_created.append(item.name)

    # Create custom agent.py if custom template
    if custom_code:
        agent_file = Path(current_dir) / "agent.py"
        agent_file.write_text(custom_code, encoding='utf-8')
        files_created.append("agent.py")

    # AUTHENTICATE FIRST - so we have SHADOWBAR_API_KEY to add to .env
    global_co_dir = Path.home() / ".sb"
    if not global_co_dir.exists():
        ensure_global_config()

    # Authenticate to get SHADOWBAR_API_KEY (always, for everyone)
    auth_success = authenticate(global_co_dir, save_to_project=False)

    # Handle .env file - append API keys from global config
    env_path = Path(current_dir) / ".env"
    global_dir = Path.home() / ".sb"
    global_keys_env = global_dir / "keys.env"

    # Read existing .env if it exists
    existing_env_content = ""
    existing_keys = set()
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            existing_env_content = f.read()
            # Parse existing keys
            for line in existing_env_content.split('\n'):
                if '=' in line and not line.strip().startswith('#'):
                    key = line.split('=')[0].strip()
                    existing_keys.add(key)

    # Read global keys (now includes SHADOWBAR_API_KEY from auth)
    keys_to_add = []
    if global_keys_env.exists():
        with open(global_keys_env, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key = line.split('=')[0].strip()
                    if key not in existing_keys:
                        keys_to_add.append(line)

    # Add agent address (from global keys.env)
    if global_keys_env.exists():
        # Load from global keys.env to get address
        with open(global_keys_env, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('AGENT_ADDRESS=') and 'AGENT_ADDRESS' not in existing_keys:
                    keys_to_add.append(line)

    # Add detected API keys
    if "anthropic" in detected_keys:
        key_value = detected_keys["anthropic"]
        if "ANTHROPIC_API_KEY" not in existing_keys:
            keys_to_add.append(f"ANTHROPIC_API_KEY={key_value}")

    # Write or append to .env
    if not env_path.exists():
        # Create new .env
        if keys_to_add:
            # Add global config path and default model comment
            env_content = f"AGENT_CONFIG_PATH={Path.home() / '.sb'}\n"
            env_content += "# Default model: claude-sonnet-4-5\n\n"
            env_content += '\n'.join(keys_to_add) + '\n'
            env_path.write_text(env_content, encoding='utf-8')
            console.print(f"[green][OK] Saved to {env_path}[/green]")
        else:
            # Fallback
            env_content = """# Add your Anthropic API key below
# ANTHROPIC_API_KEY=

# Optional: Override default model
# MODEL=claude-sonnet-4-5
"""
            env_path.write_text(env_content, encoding='utf-8')
        files_created.append(".env")
    elif keys_to_add:
        # Append missing keys to existing .env
        with open(env_path, 'a', encoding='utf-8') as f:
            if not existing_env_content.endswith('\n'):
                f.write('\n')
            f.write('\n# API Keys\n')
            f.write('\n'.join(keys_to_add) + '\n')
        console.print(f"[green][OK] Updated {env_path}[/green]")
        files_created.append(".env (updated)")
    else:
        console.print("[green][OK] .env already contains all necessary keys[/green]")

    # Create .sb directory with metadata
    sb_dir = Path(current_dir) / ".sb"
    sb_dir.mkdir(exist_ok=True)

    # Create docs directory and copy documentation (always overwrite for latest version)
    docs_dir = sb_dir / "docs"
    if docs_dir.exists():
        shutil.rmtree(docs_dir)
    docs_dir.mkdir(exist_ok=True)

    # Copy ShadowBar documentation
    cli_dir = Path(__file__).parent.parent

    # Always copy the vibe coding doc for all templates - it's the master reference doc
    master_doc = cli_dir / "docs" / "sb-vibecoding-principles-docs-contexts-all-in-one.md"

    if master_doc.exists():
        # Copy to .sb/docs/ (project metadata)
        target_doc = docs_dir / "sb-vibecoding-principles-docs-contexts-all-in-one.md"
        shutil.copy2(master_doc, target_doc)
        files_created.append(".sb/docs/sb-vibecoding-principles-docs-contexts-all-in-one.md")

        # ALSO copy to project root (always visible, easier to find)
        root_doc = Path(current_dir) / "sb-vibecoding-principles-docs-contexts-all-in-one.md"
        shutil.copy2(master_doc, root_doc)
        files_created.append("sb-vibecoding-principles-docs-contexts-all-in-one.md")
    else:
        console.print(f"[yellow][!]  Warning: Vibe coding documentation not found at {master_doc}[/yellow]")

    # Use global identity instead of generating project keys
    # NO PROJECT KEYS - we use global address/email
    # Reload global config to get updated email_active after authentication
    global_config = toml.load(global_co_dir / "config.toml") if (global_co_dir / "config.toml").exists() else global_config
    addr_data = global_config.get("agent", global_identity)  # Use updated global identity

    # Note: We're NOT creating project-specific keys anymore
    # If user wants project-specific keys, they'll use 'co address' command

    # Create config.toml (simplified - address/email now in .env)
    config = {
        "project": {
            "name": os.path.basename(current_dir) or "shadowbar-agent",
            "created": datetime.now().isoformat(),
            "framework_version": __version__,
            "secrets": ".env",  # Path to secrets file
        },
        "cli": {
            "version": "1.0.0",
            "command": "sb init",
            "template": template,
        },
        "agent": {
            "algorithm": "ed25519",
            "default_model": "claude-sonnet-4-5",
            "max_iterations": 10,
            "created_at": datetime.now().isoformat(),
        },
    }

    config_path = sb_dir / "config.toml"
    with open(config_path, "w", encoding='utf-8') as f:
        toml.dump(config, f)
    files_created.append(".sb/config.toml")

    # Handle .gitignore if in git repo
    if (Path(current_dir) / ".git").exists():
        gitignore_path = Path(current_dir) / ".gitignore"
        gitignore_content = """
# ShadowBar
.env
.sb/keys/
.sb/cache/
.sb/logs/
.sb/history/
sb-vibecoding-principles-docs-contexts-all-in-one.md
*.py[cod]
__pycache__/
todo.md
"""
        if gitignore_path.exists():
            with open(gitignore_path, "a", encoding='utf-8') as f:
                if "# ShadowBar" not in gitignore_path.read_text(encoding='utf-8'):
                    f.write(gitignore_content)
            files_created.append(".gitignore (updated)")
        else:
            gitignore_path.write_text(gitignore_content.lstrip(), encoding='utf-8')
            files_created.append(".gitignore")

    # Success message with Rich formatting
    console.print()
    console.print(f"[bold green]✅ Initialized ShadowBar in {project_name}[/bold green]")
    console.print()

    # Show different message based on whether agent.py exists
    if template != 'none' and (Path(current_dir) / "agent.py").exists():
        # Command with syntax highlighting - compact design
        command = "python agent.py"
        syntax = Syntax(
            command,
            "bash",
            theme="monokai",
            background_color="#272822",  # Monokai background color
            padding=(0, 1)  # Minimal padding for tight fit
        )
        console.print(syntax)
        console.print()

        # Vibe Coding hint - clean formatting with proper spacing
        console.print("[bold yellow][i] Vibe Coding:[/bold yellow] Use Claude/Cursor/Codex with")
        console.print(f"   [cyan]sb-vibecoding-principles-docs-contexts-all-in-one.md[/cyan]")
    else:
        # Vibe Coding hint for building from scratch
        console.print("[bold yellow][i] Vibe Coding:[/bold yellow] Use Claude/Cursor/Codex with")
        console.print(f"   [cyan]sb-vibecoding-principles-docs-contexts-all-in-one.md[/cyan]")
        console.print("   to build your agent")

    # Resources - clean format with arrows for better alignment
    console.print()
    console.print("[bold cyan]📚 Resources:[/bold cyan]")
    console.print(f"   Docs    [dim]→[/dim] [link=https://docs.shadowbar.com][blue]https://docs.shadowbar.com[/blue][/link]")
    console.print(f"   Discord [dim]→[/dim] [link=https://discord.gg/4xfD9k8AUF][blue]https://discord.gg/4xfD9k8AUF[/blue][/link]")
    console.print(f"   GitLab  [dim]→[/dim] [link=https://gitlab.com/shadowbar/shadowbar][blue]https://gitlab.com/shadowbar/shadowbar[/blue][/link] [dim]([*] star us!)[/dim]")
    console.print()

    # Clean up temporary project directory if created for authentication
    if temp_project_dir and temp_project_dir.exists():
        # Copy the auth token to the current project
        temp_config = temp_project_dir / ".sb" / "config.toml"
        current_config = Path(current_dir) / ".sb" / "config.toml"
        if temp_config.exists() and current_config.exists():
            temp_data = toml.load(temp_config)
            current_data = toml.load(current_config)
            if "auth" in temp_data:
                current_data["auth"] = temp_data["auth"]
                with open(current_config, "w", encoding='utf-8') as f:
                    toml.dump(current_data, f)

        # Remove the temp directory
        shutil.rmtree(temp_project_dir)
