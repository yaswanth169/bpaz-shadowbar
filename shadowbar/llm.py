"""
Purpose: Anthropic Claude LLM provider for ShadowBar framework
LLM-Note:
  Dependencies: imports from [abc, typing, dataclasses, json, os, anthropic, pydantic] | imported by [agent.py, llm_do.py] | tested by [tests/test_llm.py]
  Data flow: Agent/llm_do calls create_llm(model, api_key) → returns AnthropicLLM → Agent calls complete(messages, tools) OR structured_complete(messages, output_schema) → provider converts to native format → calls API → parses response → returns LLMResponse(content, tool_calls, raw_response) OR Pydantic model instance
  State/Effects: reads ANTHROPIC_API_KEY environment variable | makes HTTP requests to Anthropic API | no caching or persistence
  Integration: exposes create_llm(model, api_key), LLM abstract base class, AnthropicLLM, LLMResponse, ToolCall dataclasses | OpenAI message format is lingua franca | tool calling uses OpenAI schema converted for Anthropic
  Performance: stateless (no caching) | synchronous (no streaming) | default max_tokens=8192 for Anthropic (required) | each call hits API
  Errors: raises ValueError for missing API keys, non-Claude models | Anthropic API errors bubble up | Pydantic ValidationError for invalid structured output

ShadowBar LLM Provider - Anthropic Claude Only

This module provides the LLM interface for ShadowBar, supporting only Anthropic Claude models
as per Barclays internal requirements.

Supported Models:
  - claude-sonnet-4-5 (default, recommended)
  - claude-haiku-4-5
  - claude-opus-4-5
  - claude-3-5-sonnet-20241022 (legacy)
  - claude-3-5-haiku-20241022 (legacy)
  - claude-3-opus-20240229 (legacy)

Environment Variables:
  - ANTHROPIC_API_KEY: Required for API access

Example Usage:
    >>> from shadowbar.llm import create_llm
    >>> llm = create_llm(model="claude-sonnet-4-5")
    >>> response = llm.complete([{"role": "user", "content": "Hello"}])
    >>> print(response.content)
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Type
from dataclasses import dataclass
import json
import os
import anthropic
from pydantic import BaseModel


@dataclass
class ToolCall:
    """Represents a tool call from the LLM.

    Attributes:
        name: The function name to call
        arguments: Dict of arguments to pass to the function
        id: Unique identifier for this tool call
        extra_content: Provider-specific metadata (reserved for future use)
    """
    name: str
    arguments: Dict[str, Any]
    id: str
    extra_content: Optional[Dict[str, Any]] = None


# Import TokenUsage from usage module
from .usage import TokenUsage, calculate_cost


@dataclass
class LLMResponse:
    """Response from LLM including content and tool calls."""
    content: Optional[str]
    tool_calls: List[ToolCall]
    raw_response: Any
    usage: Optional[TokenUsage] = None


class LLM(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def complete(self, messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]] = None) -> LLMResponse:
        """Complete a conversation with optional tool support."""
        pass

    @abstractmethod
    def structured_complete(self, messages: List[Dict], output_schema: Type[BaseModel]) -> BaseModel:
        """Get structured Pydantic output matching the schema.

        Args:
            messages: Conversation messages in OpenAI format
            output_schema: Pydantic model class defining the expected output structure

        Returns:
            Instance of output_schema with parsed and validated data

        Raises:
            ValueError: If the LLM fails to generate valid structured output
        """
        pass


class AnthropicLLM(LLM):
    """Anthropic Claude LLM implementation - the only provider for ShadowBar."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-5", max_tokens: int = 8192, **kwargs):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key required.\n"
                "Set ANTHROPIC_API_KEY environment variable or pass api_key parameter.\n"
                "Get your key from: https://console.anthropic.com/"
            )

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model
        self.max_tokens = max_tokens  # Anthropic requires max_tokens (default 8192)
    
    def complete(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None, **kwargs) -> LLMResponse:
        """Complete a conversation with optional tool support."""
        # Convert messages to Anthropic format
        anthropic_messages = self._convert_messages(messages)

        api_kwargs = {
            "model": self.model,
            "messages": anthropic_messages,
            "max_tokens": self.max_tokens,  # Required by Anthropic
            **kwargs  # User can override max_tokens via kwargs
        }

        # Add tools if provided
        if tools:
            api_kwargs["tools"] = self._convert_tools(tools)

        response = self.client.messages.create(**api_kwargs)
        
        # Parse tool calls if present
        tool_calls = []
        content = ""
        
        for block in response.content:
            if block.type == "text":
                content += block.text
            elif block.type == "tool_use":
                tool_calls.append(ToolCall(
                    name=block.name,
                    arguments=block.input,
                    id=block.id
                ))

        # Extract token usage - Anthropic uses input_tokens/output_tokens
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        cached_tokens = getattr(response.usage, 'cache_read_input_tokens', 0) or 0
        cache_write_tokens = getattr(response.usage, 'cache_creation_input_tokens', 0) or 0
        cost = calculate_cost(self.model, input_tokens, output_tokens, cached_tokens, cache_write_tokens)

        return LLMResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            raw_response=response,
            usage=TokenUsage(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cached_tokens=cached_tokens,
                cache_write_tokens=cache_write_tokens,
                cost=cost,
            ),
        )

    def structured_complete(self, messages: List[Dict], output_schema: Type[BaseModel], **kwargs) -> BaseModel:
        """Get structured Pydantic output using tool calling method.

        Anthropic doesn't have native Pydantic support yet, so we use a tool calling
        workaround: create a dummy tool with the Pydantic schema and force its use.
        """
        # Convert messages to Anthropic format
        anthropic_messages = self._convert_messages(messages)

        # Create a tool with the Pydantic schema as input_schema
        tool = {
            "name": "return_structured_output",
            "description": "Returns the structured output based on the user's request",
            "input_schema": output_schema.model_json_schema()
        }

        # Set max_tokens with safe default
        api_kwargs = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": anthropic_messages,
            "tools": [tool],
            "tool_choice": {"type": "tool", "name": "return_structured_output"},
            **kwargs  # User can override max_tokens, temperature, etc.
        }

        # Force the model to use this tool
        response = self.client.messages.create(**api_kwargs)

        # Extract structured data from tool call
        for block in response.content:
            if block.type == "tool_use" and block.name == "return_structured_output":
                # Validate and return as Pydantic model
                return output_schema.model_validate(block.input)

        raise ValueError("No structured output received from Claude")

    def _convert_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert OpenAI-style messages to Anthropic format."""
        anthropic_messages = []
        i = 0
        
        while i < len(messages):
            msg = messages[i]
            
            # Skip system messages (will be handled separately)
            if msg["role"] == "system":
                i += 1
                continue
            
            # Handle assistant messages with tool calls
            if msg["role"] == "assistant" and msg.get("tool_calls"):
                content_blocks = []
                if msg.get("content"):
                    content_blocks.append({
                        "type": "text",
                        "text": msg["content"]
                    })
                
                for tc in msg["tool_calls"]:
                    content_blocks.append({
                        "type": "tool_use",
                        "id": tc["id"],
                        "name": tc["function"]["name"],
                        "input": json.loads(tc["function"]["arguments"]) if isinstance(tc["function"]["arguments"], str) else tc["function"]["arguments"]
                    })
                
                anthropic_messages.append({
                    "role": "assistant",
                    "content": content_blocks
                })
                
                # Now collect all the tool responses that follow immediately
                i += 1
                tool_results = []
                while i < len(messages) and messages[i]["role"] == "tool":
                    tool_msg = messages[i]
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_msg["tool_call_id"],
                        "content": tool_msg["content"]
                    })
                    i += 1
                
                # Add all tool results in a single user message
                if tool_results:
                    anthropic_messages.append({
                        "role": "user",
                        "content": tool_results
                    })
            
            # Handle tool role messages that aren't immediately after assistant tool calls
            elif msg["role"] == "tool":
                # This shouldn't happen in normal flow, but handle it just in case
                anthropic_messages.append({
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": msg["tool_call_id"],
                        "content": msg["content"]
                    }]
                })
                i += 1
            
            # Handle user messages
            elif msg["role"] == "user":
                if isinstance(msg.get("content"), list):
                    # This is already a structured message
                    anthropic_msg = {
                        "role": "user",
                        "content": []
                    }
                    for item in msg["content"]:
                        if item.get("type") == "tool_result":
                            anthropic_msg["content"].append({
                                "type": "tool_result",
                                "tool_use_id": item["tool_call_id"],
                                "content": item["content"]
                            })
                    anthropic_messages.append(anthropic_msg)
                else:
                    # Regular text message
                    anthropic_messages.append({
                        "role": "user",
                        "content": msg["content"]
                    })
                i += 1
            
            # Handle regular assistant messages
            elif msg["role"] == "assistant":
                anthropic_messages.append({
                    "role": "assistant",
                    "content": msg["content"]
                })
                i += 1
            
            else:
                i += 1
        
        return anthropic_messages
    
    def _convert_tools(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert OpenAI-style tools to Anthropic format."""
        anthropic_tools = []
        
        for tool in tools:
            # Tools already in our internal format
            anthropic_tool = {
                "name": tool["name"],
                "description": tool.get("description", ""),
                "input_schema": tool.get("parameters", {
                    "type": "object",
                    "properties": {},
                    "required": []
                })
            }
            anthropic_tools.append(anthropic_tool)
        
        return anthropic_tools


# Model registry - Anthropic Claude models only
MODEL_REGISTRY = {
    # Claude 4.5 models (latest, recommended)
    "claude-sonnet-4-5": "anthropic",
    "claude-sonnet-4-5-20250929": "anthropic",
    "claude-haiku-4-5": "anthropic",
    "claude-haiku-4-5-20251001": "anthropic",
    "claude-opus-4-5": "anthropic",
    "claude-opus-4-5-20251101": "anthropic",
    
    # Claude 3.5 models (legacy)
    "claude-3-5-sonnet": "anthropic",
    "claude-3-5-sonnet-20241022": "anthropic",
    "claude-3-5-sonnet-latest": "anthropic",
    "claude-3-5-haiku": "anthropic",
    "claude-3-5-haiku-20241022": "anthropic",
    "claude-3-5-haiku-latest": "anthropic",
    
    # Claude 3 models
    "claude-3-haiku-20240307": "anthropic",
    "claude-3-opus-20240229": "anthropic",
    "claude-3-opus-latest": "anthropic",
    "claude-3-sonnet-20240229": "anthropic",
    
    # Claude 4 models (newer)
    "claude-opus-4.1": "anthropic",
    "claude-opus-4-1-20250805": "anthropic",
    "claude-opus-4-1": "anthropic",
    "claude-opus-4": "anthropic",
    "claude-opus-4-20250514": "anthropic",
    "claude-opus-4-0": "anthropic",
    "claude-sonnet-4": "anthropic",
    "claude-sonnet-4-20250514": "anthropic",
    "claude-sonnet-4-0": "anthropic",
    
    # Claude 3.7 models
    "claude-3-7-sonnet-latest": "anthropic",
    "claude-3-7-sonnet-20250219": "anthropic",
    
    # Claude 4.5 models
    "claude-sonnet-4-5": "anthropic",
}


def create_llm(model: str, api_key: Optional[str] = None, **kwargs) -> LLM:
    """Factory function to create Anthropic LLM.
    
    ShadowBar only supports Anthropic Claude models as per Barclays requirements.
    
    Args:
        model: The Claude model name (e.g., "claude-sonnet-4-5")
        api_key: Optional API key to override ANTHROPIC_API_KEY environment variable
        **kwargs: Additional arguments (max_tokens, temperature, etc.)
    
    Returns:
        AnthropicLLM instance
    
    Raises:
        ValueError: If the model is not a Claude model
    
    Example:
        >>> llm = create_llm("claude-sonnet-4-5")
        >>> response = llm.complete([{"role": "user", "content": "Hello"}])
    """
    # Validate it's a Claude model
    if not model.startswith("claude"):
        raise ValueError(
            f"ShadowBar only supports Anthropic Claude models.\n"
            f"Got: '{model}'\n"
            f"Supported models include:\n"
            f"  - claude-sonnet-4-5 (recommended, default)\n"
            f"  - claude-haiku-4-5\n"
            f"  - claude-opus-4-5\n"
            f"  - claude-3-5-sonnet-20241022 (legacy)\n"
            f"See full list in MODEL_REGISTRY."
        )
    
    return AnthropicLLM(api_key=api_key, model=model, **kwargs)


