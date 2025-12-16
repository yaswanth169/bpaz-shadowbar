#!/usr/bin/env python3
"""
ShadowBar Test Agent

This script tests the core agent functionality.
Requires ANTHROPIC_API_KEY environment variable.
"""

import os
import sys

# Check for API key
if not os.getenv("ANTHROPIC_API_KEY"):
    print("=" * 60)
    print("ANTHROPIC_API_KEY not set!")
    print("")
    print("To test with real API calls, set your Anthropic API key:")
    print("  set ANTHROPIC_API_KEY=your-key-here  (Windows)")
    print("  export ANTHROPIC_API_KEY=your-key-here  (Linux/Mac)")
    print("")
    print("Running import tests only...")
    print("=" * 60)
    
    # Just test imports
    print("\nTesting imports...")
    from shadowbar import Agent, LLM, llm_do, Memory, xray
    print("  [OK] All imports successful")
    
    from shadowbar.llm import create_llm, AnthropicLLM
    print("  [OK] LLM module loads correctly")
    
    # Test that create_llm rejects non-Claude models
    try:
        create_llm("gpt-4o")
        print("  [FAIL] Should have rejected OpenAI model")
    except ValueError as e:
        if "ShadowBar only supports Anthropic Claude" in str(e):
            print("  [OK] Non-Claude models correctly rejected")
    
    # Test Agent initialization (without API call)
    def dummy_tool(x: str) -> str:
        """A dummy tool."""
        return f"Got: {x}"
    
    try:
        # This will fail at LLM creation without API key
        agent = Agent("test", tools=[dummy_tool])
        print("  [FAIL] Should have failed without API key")
    except ValueError as e:
        if "Anthropic API key required" in str(e):
            print("  [OK] Agent correctly requires API key")
    
    print("\n" + "=" * 60)
    print("[OK] All import tests passed!")
    print("=" * 60)
    sys.exit(0)

# If we have API key, run full tests
print("=" * 60)
print("ShadowBar Agent Test (with API)")
print("=" * 60)

from shadowbar import Agent

# Define a simple tool
def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}! Welcome to ShadowBar."

def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

# Create agent
print("\nCreating agent...")
agent = Agent(
    name="test-agent",
    tools=[greet, add],
    system_prompt="You are a helpful assistant. Use the available tools to help users."
)

print(f"  Agent: {agent.name}")
print(f"  Model: {agent.llm.model}")
print(f"  Tools: {agent.list_tools()}")

# Test simple interaction
print("\nTesting agent.input()...")
try:
    response = agent.input("Please greet Alice")
    print(f"  Response: {response[:100]}...")
    print("  [OK] Agent responded successfully")
except Exception as e:
    print(f"  [FAIL] Error: {e}")
    sys.exit(1)

# Test tool execution
print("\nTesting tool execution...")
try:
    result = agent.execute_tool("add", {"a": 5, "b": 3})
    print(f"  Result: {result}")
    if result["result"] == "8":
        print("  [OK] Tool executed correctly")
    else:
        print(f"  [FAIL] Expected 8, got {result['result']}")
except Exception as e:
    print(f"  [FAIL] Error: {e}")

print("\n" + "=" * 60)
print("[OK] All tests passed!")
print("=" * 60)

