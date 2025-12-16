"""
Purpose: Token usage tracking and cost calculation for LLM calls
LLM-Note:
  Dependencies: none | imported by [llm.py, agent.py]
  Data flow: receives model name + token counts → returns cost in USD
  Integration: exposes TokenUsage, MODEL_PRICING, MODEL_CONTEXT_LIMITS, calculate_cost(), get_context_limit()

ShadowBar Usage - Token tracking and cost calculation.

This module provides utilities for tracking token usage and calculating costs
for Anthropic Claude models (the only LLM provider supported by ShadowBar).
"""

from dataclasses import dataclass


@dataclass
class TokenUsage:
    """Token usage from a single LLM call."""
    input_tokens: int = 0
    output_tokens: int = 0
    cached_tokens: int = 0      # Tokens read from cache (subset of input_tokens)
    cache_write_tokens: int = 0  # Tokens written to cache (Anthropic only)
    cost: float = 0.0           # USD cost for this call


# Pricing per 1M tokens (USD) - Anthropic Claude models only
# Format: {"input": $, "output": $, "cached": $, "cache_write": $}
MODEL_PRICING = {
    # Anthropic Claude models - cached = 10% of input, cache_write = 125% of input
    "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00, "cached": 0.30, "cache_write": 3.75},
    "claude-3-5-sonnet-latest": {"input": 3.00, "output": 15.00, "cached": 0.30, "cache_write": 3.75},
    "claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.00, "cached": 0.08, "cache_write": 1.00},
    "claude-3-5-haiku-latest": {"input": 0.80, "output": 4.00, "cached": 0.08, "cache_write": 1.00},
    "claude-3-opus-20240229": {"input": 15.00, "output": 75.00, "cached": 1.50, "cache_write": 18.75},
    "claude-3-opus-latest": {"input": 15.00, "output": 75.00, "cached": 1.50, "cache_write": 18.75},
    "claude-3-sonnet-20240229": {"input": 3.00, "output": 15.00, "cached": 0.30, "cache_write": 3.75},
    "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25, "cached": 0.025, "cache_write": 0.3125},

    # Claude 4 models
    "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00, "cached": 0.30, "cache_write": 3.75},
    "claude-sonnet-4": {"input": 3.00, "output": 15.00, "cached": 0.30, "cache_write": 3.75},
    "claude-sonnet-4-0": {"input": 3.00, "output": 15.00, "cached": 0.30, "cache_write": 3.75},
    "claude-opus-4-20250514": {"input": 15.00, "output": 75.00, "cached": 1.50, "cache_write": 18.75},
    "claude-opus-4": {"input": 15.00, "output": 75.00, "cached": 1.50, "cache_write": 18.75},
    "claude-opus-4-0": {"input": 15.00, "output": 75.00, "cached": 1.50, "cache_write": 18.75},
    "claude-opus-4-1": {"input": 15.00, "output": 75.00, "cached": 1.50, "cache_write": 18.75},
    "claude-opus-4-1-20250805": {"input": 15.00, "output": 75.00, "cached": 1.50, "cache_write": 18.75},

    # Claude 3.7 models
    "claude-3-7-sonnet-latest": {"input": 3.00, "output": 15.00, "cached": 0.30, "cache_write": 3.75},
    "claude-3-7-sonnet-20250219": {"input": 3.00, "output": 15.00, "cached": 0.30, "cache_write": 3.75},
    
    # Claude 4.5 models
    "claude-sonnet-4-5": {"input": 3.00, "output": 15.00, "cached": 0.30, "cache_write": 3.75},
}

# Context window limits (tokens) - Anthropic Claude models only
MODEL_CONTEXT_LIMITS = {
    # Anthropic Claude models
    "claude-3-5-sonnet-20241022": 200000,
    "claude-3-5-sonnet-latest": 200000,
    "claude-3-5-haiku-20241022": 200000,
    "claude-3-5-haiku-latest": 200000,
    "claude-3-opus-20240229": 200000,
    "claude-3-opus-latest": 200000,
    "claude-3-sonnet-20240229": 200000,
    "claude-3-haiku-20240307": 200000,
    "claude-sonnet-4-20250514": 200000,
    "claude-sonnet-4": 200000,
    "claude-sonnet-4-0": 200000,
    "claude-opus-4-20250514": 200000,
    "claude-opus-4": 200000,
    "claude-opus-4-0": 200000,
    "claude-opus-4-1": 200000,
    "claude-opus-4-1-20250805": 200000,
    "claude-3-7-sonnet-latest": 200000,
    "claude-3-7-sonnet-20250219": 200000,
    "claude-sonnet-4-5": 200000,
}

# Default values for unknown models (assuming Claude-like)
DEFAULT_PRICING = {"input": 3.00, "output": 15.00, "cached": 0.30, "cache_write": 3.75}
DEFAULT_CONTEXT_LIMIT = 200000


def get_pricing(model: str) -> dict:
    """Get pricing for a model, with fallback to default."""
    # Try exact match
    if model in MODEL_PRICING:
        return MODEL_PRICING[model]

    # Try prefix match (e.g., "claude-3-5-sonnet-2024" -> "claude-3-5-sonnet-20241022")
    for known_model in MODEL_PRICING:
        if model.startswith(known_model.rsplit('-', 1)[0]):
            return MODEL_PRICING[known_model]

    return DEFAULT_PRICING


def get_context_limit(model: str) -> int:
    """Get context limit for a model, with fallback to default."""
    if model in MODEL_CONTEXT_LIMITS:
        return MODEL_CONTEXT_LIMITS[model]

    for known_model in MODEL_CONTEXT_LIMITS:
        if model.startswith(known_model.rsplit('-', 1)[0]):
            return MODEL_CONTEXT_LIMITS[known_model]

    return DEFAULT_CONTEXT_LIMIT


def calculate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    cached_tokens: int = 0,
    cache_write_tokens: int = 0,
) -> float:
    """Calculate USD cost for token usage.

    Args:
        model: Model name
        input_tokens: Total input tokens (includes cached)
        output_tokens: Output/completion tokens
        cached_tokens: Tokens read from cache (subset of input_tokens)
        cache_write_tokens: Tokens written to cache (Anthropic)

    Returns:
        Cost in USD
    """
    pricing = get_pricing(model)

    # Non-cached input tokens = total input - cached
    non_cached_input = max(0, input_tokens - cached_tokens)

    # Calculate costs (pricing is per 1M tokens)
    input_cost = (non_cached_input / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]
    cached_cost = (cached_tokens / 1_000_000) * pricing.get("cached", pricing["input"] * 0.1)

    # Cache write cost (Anthropic)
    cache_write_cost = 0.0
    if cache_write_tokens > 0 and "cache_write" in pricing:
        cache_write_cost = (cache_write_tokens / 1_000_000) * pricing["cache_write"]

    return input_cost + output_cost + cached_cost + cache_write_cost


