"""
Purpose: One-shot LLM function for simple single-round calls without agent overhead
LLM-Note:
  Dependencies: imports from [typing, pathlib, pydantic, dotenv, prompts.py, llm.py] | imported by [debug_explainer/explain_context.py, user code, examples] | tested by [tests/test_llm_do.py]
  Data flow: user calls llm_do(input, output, system_prompt, model, api_key, **kwargs) → validates input non-empty → loads system_prompt via load_system_prompt() → builds messages [system, user] → calls create_llm(model, api_key) factory → calls llm.complete(messages, **kwargs) OR llm.structured_complete(messages, output, **kwargs) → returns string OR Pydantic model instance
  State/Effects: loads .env via dotenv.load_dotenv() | reads system_prompt files if Path provided | makes one LLM API request | no caching or persistence | stateless
  Integration: exposes llm_do(input, output, system_prompt, model, api_key, **kwargs) | default model="claude-3-5-sonnet-20241022" (ShadowBar default) | default temperature=0.1 | supports Anthropic Claude models only | **kwargs pass through to provider (max_tokens, temperature, etc.)
  Performance: minimal overhead (no agent loop, no tool calling, no conversation history) | one LLM call per invocation | no caching | synchronous blocking
  Errors: raises ValueError if input empty | provider errors from create_llm() and llm.complete() bubble up | Pydantic ValidationError if structured output doesn't match schema

One-shot LLM function for simple, single-round calls with optional structured output.

ShadowBar Version - Anthropic Claude Only

This module provides the `llm_do()` function - a simplified interface for making
one-shot LLM calls without the overhead of the full Agent system. Perfect for
simple tasks that don't require multi-step reasoning or tool calling.

Purpose
-------
`llm_do()` is designed for:
- Quick LLM calls without agent overhead
- Data extraction with Pydantic validation
- Simple Q&A and text generation
- Format conversion (text → JSON, etc.)
- One-shot analysis tasks

NOT designed for:
- Multi-step workflows (use Agent instead)
- Tool calling (use Agent instead)
- Iterative refinement (use Agent instead)
- Maintaining conversation history (use Agent instead)

Architecture
-----------
The function is a thin wrapper around the Anthropic LLM provider:

1. **Input Validation**: Ensures non-empty input
2. **System Prompt Loading**: Loads from string or file path
3. **Message Building**: Constructs OpenAI-format message list
4. **LLM Selection**: Uses create_llm() factory to get Anthropic provider
5. **Response Handling**: Routes to complete() or structured_complete()

Key Design Decisions
-------------------
- **Stateless**: No conversation history, each call is independent
- **Simple API**: Minimal parameters, sensible defaults
- **Default Model**: Uses "claude-sonnet-4-5" (Claude Sonnet 4.5)
- **Structured Output**: Native Pydantic support via forced tool calling
- **Flexible Parameters**: **kwargs pass through to underlying LLM (temperature, max_tokens, etc.)

Supported Models (Anthropic Only)
---------------------------------
- claude-sonnet-4-5 (default, recommended)
- claude-3-5-haiku-20241022 (faster, cheaper)
- claude-3-opus-20240229 (most capable)
- claude-sonnet-4, claude-opus-4 (newer versions)

Example Usage
-------------
    from shadowbar import llm_do
    from pydantic import BaseModel

    # Simple call
    answer = llm_do("What's 2+2?")

    # Structured output
    class Analysis(BaseModel):
        sentiment: str
        confidence: float
        keywords: list[str]

    result = llm_do(
        "I absolutely love this product! Best purchase ever!",
        output=Analysis
    )
    print(result.sentiment)    # "positive"
    print(result.confidence)   # 0.98
"""

from typing import Union, Type, Optional, TypeVar
from pathlib import Path
from pydantic import BaseModel
from .prompts import load_system_prompt
from .llm import create_llm

T = TypeVar('T', bound=BaseModel)


def llm_do(
    input: str,
    output: Optional[Type[T]] = None,
    system_prompt: Optional[Union[str, Path]] = None,
    model: str = "claude-sonnet-4-5",  # ShadowBar default: Claude Sonnet 4.5
    api_key: Optional[str] = None,
    **kwargs
) -> Union[str, T]:
    """
    Make a one-shot LLM call with optional structured output.

    ShadowBar uses Anthropic Claude models exclusively:
    - "claude-3-5-sonnet-20241022" (default, recommended)
    - "claude-3-5-haiku-20241022" (faster)
    - "claude-3-opus-20240229" (most capable)
    - "claude-sonnet-4" (newer)

    Args:
        input: The input text/question to send to the LLM
        output: Optional Pydantic model class for structured output
        system_prompt: Optional system prompt (string or file path)
        model: Model name (default: "claude-sonnet-4-5")
        api_key: Optional API key (uses ANTHROPIC_API_KEY env var if not provided)
        **kwargs: Additional parameters (temperature, max_tokens, etc.)

    Returns:
        Either a string response or an instance of the output model

    Examples:
        >>> # Simple string response with default model
        >>> answer = llm_do("What's 2+2?")
        >>> print(answer)  # "4"

        >>> # With Claude Haiku (faster)
        >>> answer = llm_do("Explain quantum physics", model="claude-3-5-haiku-20241022")

        >>> # With structured output
        >>> class Analysis(BaseModel):
        ...     sentiment: str
        ...     score: float
        >>>
        >>> result = llm_do("I love this!", output=Analysis)
        >>> print(result.sentiment)  # "positive"
    """
    # Validate input
    if not input or not input.strip():
        raise ValueError("Input cannot be empty")

    # Load system prompt
    if system_prompt:
        prompt_text = load_system_prompt(system_prompt)
    else:
        prompt_text = "You are a helpful assistant."

    # Build messages
    messages = [
        {"role": "system", "content": prompt_text},
        {"role": "user", "content": input}
    ]

    # Create LLM using factory (only pass api_key and initialization params)
    llm = create_llm(model=model, api_key=api_key)

    # Get response
    if output:
        # Structured output - use structured_complete()
        return llm.structured_complete(messages, output, **kwargs)
    else:
        # Plain text - use complete()
        # Pass through kwargs (max_tokens, temperature, etc.)
        response = llm.complete(messages, tools=None, **kwargs)
        return response.content


