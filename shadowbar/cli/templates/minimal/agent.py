"""
Purpose: Minimal agent template demonstrating basic ShadowBar usage with a calculator tool
LLM-Note:
  Dependencies: imports from [shadowbar.Agent] | template file copied by [cli/commands/init.py, cli/commands/create.py] | default template for 'sb create' and 'sb init'
  Data flow: user query → Agent.input() → calculator tool called if math expression → eval() computes result → returns answer
  State/Effects: no persistent state | single Agent.input() call | uses Anthropic Claude model
  Integration: template for 'sb create --template minimal' | demonstrates function-as-tool pattern | shows system_prompt and model configuration
  Performance: single LLM call | eval() is fast
  Errors: [!] Security: uses eval() - for demo only, not production safe

Minimal ShadowBar agent with a simple calculator tool.
"""

from shadowbar import Agent
from shadowbar.llm import AnthropicLLM


def calculator(expression: str) -> float:
    """Simple calculator that evaluates arithmetic expressions.

    Args:
        expression: A mathematical expression (e.g., "5*5", "10+20")

    Returns:
        The result of the calculation
    """
    # Note: eval() is used for simplicity. For production, use a safer parser.
    return eval(expression)


# Create LLM with Anthropic Claude
llm = AnthropicLLM(model="claude-sonnet-4-5", max_tokens=2048)

# Create agent with calculator tool
agent = Agent(
    name="calculator-agent", 
    llm=llm,
    system_prompt="Please use the calculator tool to answer math questions", # you can also pass a markdown file like system_prompt="path/to/your_markdown_file.md"
    tools=[calculator], # tools can be python classes or functions
)

# Run the agent
result = agent.input("what is the result of 5*5")
print(result)
