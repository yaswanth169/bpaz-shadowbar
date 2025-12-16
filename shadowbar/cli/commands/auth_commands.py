"""
ShadowBar authentication (Anthropic-only, no external backend).

- Uses local Ed25519 identity stored in ~/.sb/keys (sb_dir)
- No managed keys or external auth; you supply ANTHROPIC_API_KEY
- Writes AGENT_CONFIG_PATH, AGENT_ADDRESS, AGENT_EMAIL to keys.env and project .env
- Ready for future internal/Barclays auth without external dependencies
"""

from pathlib import Path
from rich.console import Console

from ... import address

console = Console()


def _save_identity_to_env(env_file: Path, agent_address: str, agent_email: str) -> None:
    """Ensure AGENT_CONFIG_PATH, AGENT_ADDRESS, AGENT_EMAIL are present in env_file."""
    lines = []
    found_addr = found_email = found_config = False

    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("AGENT_CONFIG_PATH="):
                    lines.append(line)
                    found_config = True
                elif line.strip().startswith("AGENT_ADDRESS="):
                    lines.append(f"AGENT_ADDRESS={agent_address}\n")
                    found_addr = True
                elif line.strip().startswith("AGENT_EMAIL="):
                    lines.append(f"AGENT_EMAIL={agent_email}\n")
                    found_email = True
                else:
                    lines.append(line)

    if not found_config:
        lines.insert(0, f"AGENT_CONFIG_PATH={env_file.parent / '.sb'}\n")
    if not found_addr:
        lines.append(f"AGENT_ADDRESS={agent_address}\n")
    if not found_email:
        lines.append(f"AGENT_EMAIL={agent_email}\n")

    if lines and not lines[-1].endswith("\n"):
        lines.append("\n")

    with open(env_file, "w", encoding="utf-8") as f:
        f.writelines(lines)


def authenticate(sb_dir: Path, save_to_project: bool = True, quiet: bool = False) -> bool:
    """
    ShadowBar Anthropic-only: no external auth.
    Loads local identity and records it in keys.env and project .env.
    """
    try:
        addr_data = address.load(sb_dir)
    except Exception:
        addr_data = None

    if not addr_data:
        if not quiet:
            console.print("[red][X] No agent keys found in ~/.sb/keys. Run sb init/create first.[/red]")
        return False

    agent_address = addr_data["address"]
    agent_email = f"{agent_address[:10]}@mail.shadowbar.ai"

    # Update global keys.env
    keys_env = sb_dir / "keys.env"
    _save_identity_to_env(keys_env, agent_address, agent_email)

    # Optionally update project .env (sibling of .sb)
    if save_to_project:
        project_env = sb_dir.parent / ".env"
        _save_identity_to_env(project_env, agent_address, agent_email)

    if not quiet:
        console.print("[green]Identity loaded. No external authentication required.[/green]")
        console.print("[yellow]Set ANTHROPIC_API_KEY in your environment or project .env.[/yellow]")

    return True
