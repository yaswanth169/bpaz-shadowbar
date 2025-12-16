#!/usr/bin/env python3
"""Real-time test with Anthropic API."""
import os

# Direct LLM test
print("=" * 60)
print("ShadowBar Real-Time API Test")
print("=" * 60)

from shadowbar.llm import AnthropicLLM

# Test 1: Direct LLM call
print("\n[Test 1] Direct LLM call...")
llm = AnthropicLLM(model='claude-3-haiku-20240307', max_tokens=1024)
print(f"  Model: {llm.model}")

response = llm.complete([
    {'role': 'user', 'content': 'Say hello in one sentence.'}
])
print(f"  Response: {response.content}")
print(f"  Tokens: {response.usage.input_tokens} in, {response.usage.output_tokens} out")
print(f"  Cost: ${response.usage.cost:.6f}")
print("  [OK] Direct LLM working!")

# Test 2: Agent with tool
print("\n[Test 2] Agent with tools...")
from shadowbar import Agent

def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}! Welcome to ShadowBar."

def calculate(expression: str) -> str:
    """Calculate a math expression."""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except:
        return "Error: Could not calculate"

# Use haiku with lower max_tokens
from shadowbar.llm import AnthropicLLM
llm = AnthropicLLM(model='claude-3-haiku-20240307', max_tokens=1024)

agent = Agent(
    name="test-agent",
    llm=llm,
    tools=[greet, calculate],
    system_prompt="You are a helpful assistant. Use tools when appropriate."
)
print(f"  Agent: {agent.name}")
print(f"  Tools: {agent.list_tools()}")

print("\n  Sending: 'Please greet Alice'")
response = agent.input("Please greet Alice")
print(f"  Response: {response[:200]}...")
print("  [OK] Agent with tools working!")

# Test 3: llm_do one-shot
print("\n[Test 3] llm_do one-shot...")
from shadowbar import llm_do
from pydantic import BaseModel

class Sentiment(BaseModel):
    mood: str
    score: float

result = llm_do(
    "I love this product! It's amazing!",
    output=Sentiment,
    model="claude-3-haiku-20240307",
    max_tokens=1024
)
print(f"  Mood: {result.mood}")
print(f"  Score: {result.score}")
print("  [OK] Structured output working!")

print("\n" + "=" * 60)
print("[OK] All real-time tests passed!")
print("=" * 60)

