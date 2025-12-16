#!/usr/bin/env python3
"""
ShadowBar Installation Test

This script verifies that ShadowBar is installed correctly and 
all core components are working.

Run: python test_installation.py
"""

import sys

def test_imports():
    """Test that all core modules can be imported."""
    print("Testing imports...")
    
    try:
        from shadowbar import Agent
        print("  [OK] Agent")
    except ImportError as e:
        print(f"  [FAIL] Agent: {e}")
        return False
    
    try:
        from shadowbar import LLM
        print("  [OK] LLM")
    except ImportError as e:
        print(f"  [FAIL] LLM: {e}")
        return False
    
    try:
        from shadowbar import llm_do
        print("  [OK] llm_do")
    except ImportError as e:
        print(f"  [FAIL] llm_do: {e}")
        return False
    
    try:
        from shadowbar import xray
        print("  [OK] xray")
    except ImportError as e:
        print(f"  [FAIL] xray: {e}")
        return False
    
    try:
        from shadowbar import Memory
        print("  [OK] Memory")
    except ImportError as e:
        print(f"  [FAIL] Memory: {e}")
        return False
    
    try:
        from shadowbar.llm import create_llm, MODEL_REGISTRY
        print("  [OK] create_llm, MODEL_REGISTRY")
    except ImportError as e:
        print(f"  [FAIL] create_llm: {e}")
        return False
    
    try:
        from shadowbar import connect
        print("  [OK] connect")
    except ImportError as e:
        print(f"  [FAIL] connect: {e}")
        return False
    
    return True


def test_anthropic_only():
    """Verify that only Anthropic models are supported."""
    print("\nTesting Anthropic-only restriction...")
    
    from shadowbar.llm import create_llm
    
    # Test that non-Claude models are rejected
    try:
        llm = create_llm("gpt-4o")
        print("  [FAIL] Should have rejected OpenAI model!")
        return False
    except ValueError as e:
        if "ShadowBar only supports Anthropic Claude models" in str(e):
            print("  [OK] OpenAI models correctly rejected")
        else:
            print(f"  [FAIL] Wrong error: {e}")
            return False
    
    try:
        llm = create_llm("gemini-2.5-pro")
        print("  [FAIL] Should have rejected Gemini model!")
        return False
    except ValueError as e:
        if "ShadowBar only supports Anthropic Claude models" in str(e):
            print("  [OK] Gemini models correctly rejected")
        else:
            print(f"  [FAIL] Wrong error: {e}")
            return False
    
    return True


def test_default_model():
    """Verify the default model is Claude."""
    print("\nTesting default model...")
    
    from shadowbar import Agent
    import inspect
    
    # Check Agent default
    sig = inspect.signature(Agent.__init__)
    model_default = sig.parameters['model'].default
    
    if model_default == "claude-3-5-sonnet-20241022":
        print(f"  [OK] Agent default model: {model_default}")
    else:
        print(f"  [FAIL] Agent default model should be claude-3-5-sonnet-20241022, got: {model_default}")
        return False
    
    from shadowbar import llm_do as llm_do_func
    sig = inspect.signature(llm_do_func)
    model_default = sig.parameters['model'].default
    
    if model_default == "claude-3-5-sonnet-20241022":
        print(f"  [OK] llm_do default model: {model_default}")
    else:
        print(f"  [FAIL] llm_do default model should be claude-3-5-sonnet-20241022, got: {model_default}")
        return False
    
    return True


def test_config_directory():
    """Verify .sb directory is used instead of .co."""
    print("\nTesting config directory (.sb)...")
    
    from shadowbar.logger import Logger
    import inspect
    
    # Check logger uses .sb paths
    source = inspect.getsource(Logger)
    
    if ".sb/logs" in source:
        print("  [OK] Logger uses .sb/logs")
    else:
        print("  [FAIL] Logger should use .sb/logs")
        return False
    
    if ".sb/sessions" in source:
        print("  [OK] Logger uses .sb/sessions")
    else:
        print("  [FAIL] Logger should use .sb/sessions")
        return False
    
    return True


def test_environment_variables():
    """Verify SHADOWBAR_ environment variables are used."""
    print("\nTesting environment variables...")
    
    from shadowbar import agent
    import inspect
    
    source = inspect.getsource(agent)
    
    if "SHADOWBAR_LOG" in source:
        print("  [OK] Uses SHADOWBAR_LOG")
    else:
        print("  [FAIL] Should use SHADOWBAR_LOG")
        return False
    
    if "SHADOWBAR_RELAY_URL" in source:
        print("  [OK] Uses SHADOWBAR_RELAY_URL")
    else:
        print("  [FAIL] Should use SHADOWBAR_RELAY_URL")
        return False
    
    return True


def test_cli():
    """Verify CLI is configured as 'sb'."""
    print("\nTesting CLI configuration...")
    
    try:
        from shadowbar.cli.main import cli, app
        print("  [OK] CLI module loads")
    except ImportError as e:
        print(f"  [FAIL] CLI module: {e}")
        return False
    
    return True


def main():
    print("=" * 60)
    print("ShadowBar Installation Test")
    print("=" * 60)
    
    all_passed = True
    
    all_passed &= test_imports()
    all_passed &= test_anthropic_only()
    all_passed &= test_default_model()
    all_passed &= test_config_directory()
    all_passed &= test_environment_variables()
    all_passed &= test_cli()
    
    print("\n" + "=" * 60)
    if all_passed:
        print("[OK] All tests passed! ShadowBar is correctly configured.")
        print("=" * 60)
        return 0
    else:
        print("[FAIL] Some tests failed. Please check the output above.")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())

