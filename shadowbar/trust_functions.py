"""
Purpose: Provide tool functions for trust agents to verify other agents
LLM-Note:
  Dependencies: imports from [pathlib, typing] | imported by [trust.py] | tested by [tests/test_trust.py]
  Data flow: create_trust_agent() calls get_trust_verification_tools() → returns list of verification functions → these become tools for trust Agent
  State/Effects: check_whitelist() reads ~/.shadowbar/trusted.txt file if exists | supports wildcard patterns with *

ShadowBar Trust Functions - Verification tools for trust agents.

This module provides tool functions that trust agents use to verify other agents:
- check_whitelist: Check if an agent is on the trusted list
- test_capability: Test an agent's claimed capabilities
- verify_agent: General agent verification
"""

from pathlib import Path
from typing import List, Callable


def check_whitelist(agent_id: str) -> str:
    """
    Check if an agent is on the whitelist.
    
    Args:
        agent_id: Identifier of the agent to check
        
    Returns:
        String indicating if agent is whitelisted or not
    """
    whitelist_path = Path.home() / ".shadowbar" / "trusted.txt"
    if whitelist_path.exists():
        try:
            whitelist = whitelist_path.read_text(encoding='utf-8')
            lines = whitelist.strip().split('\n')
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if line == agent_id:
                    return f"{agent_id} is on the whitelist"
                # Simple wildcard support
                if '*' in line:
                    pattern = line.replace('*', '')
                    if pattern in agent_id:
                        return f"{agent_id} matches whitelist pattern: {line}"
            return f"{agent_id} is NOT on the whitelist"
        except Exception as e:
            return f"Error reading whitelist: {e}"
    return "No whitelist file found at ~/.shadowbar/trusted.txt"


def test_capability(agent_id: str, test: str, expected: str) -> str:
    """
    Test an agent's capability with a specific test.
    
    Args:
        agent_id: Identifier of the agent to test
        test: The test to perform
        expected: The expected result
        
    Returns:
        Test description for the trust agent to evaluate
    """
    return f"Testing {agent_id} with: {test}, expecting: {expected}"


def verify_agent(agent_id: str, agent_info: str = "") -> str:
    """
    General verification of an agent.
    
    Args:
        agent_id: Identifier of the agent
        agent_info: Additional information about the agent
        
    Returns:
        Verification context for the trust agent
    """
    return f"Verifying agent: {agent_id}. Info: {agent_info}"


def get_trust_verification_tools() -> List[Callable]:
    """
    Get the list of trust verification tools.
    
    Returns:
        List of trust verification functions
    """
    return [
        check_whitelist,
        test_capability,
        verify_agent
    ]


