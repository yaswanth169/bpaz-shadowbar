# ShadowBar End-to-End Feature Testing Guide

This guide explains how to test all ShadowBar features end-to-end.

## Quick Start

### Prerequisites
1. Install ShadowBar: `pip install -e .` (from shadowbar directory)
2. Set API key: `export ANTHROPIC_API_KEY=your-key` (or set in `.env`)
3. For browser tests: `pip install playwright && playwright install chromium`

### Run All Tests

```bash
# From shadowbar directory
python test_all_features.py
```

This will test all 16 features:
1. ✅ Basic Agent with Function Tools
2. ✅ Class-based Tools (Stateful)
3. ✅ Memory System
4. ✅ Event System
5. ✅ llm_do (Direct LLM Calls)
6. ✅ xray Debugging
7. ✅ Shell Tool
8. ✅ Plugins (re_act)
9. ✅ DiffWriter Tool
10. ✅ WebFetch Tool
11. ✅ Logger and Session YAML
12. ✅ Multi-Agent with Shared Memory
13. ✅ Agent Networking (Address & Config)
14. ✅ Trust System
15. ✅ Relay Server
16. ✅ Browser Agent (Playwright)

## Test Files

### `test_all_features.py` (Recommended)
- **Purpose**: Comprehensive, organized test runner
- **Features**: Clear output, result tracking, summary report
- **Usage**: `python test_all_features.py`
- **Output**: Detailed pass/fail for each feature

### `comprehensive_test.py`
- **Purpose**: Original comprehensive test suite
- **Features**: More verbose output, detailed test cases
- **Usage**: `python comprehensive_test.py`
- **Output**: Detailed execution logs

### `test_browser_agent.py`
- **Purpose**: Browser automation specific tests
- **Features**: Playwright integration, browser capabilities
- **Usage**: `python test_browser_agent.py`
- **Requirements**: Playwright installed

## Feature Testing Details

### 1. Basic Agent with Function Tools
Tests that Python functions are automatically converted to agent-callable tools.

**What's tested:**
- Agent creation with function tools
- Type hints for parameter schemas
- Docstrings as tool descriptions
- Agent tool execution

**Example:**
```python
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

agent = Agent(tools=[add])
result = agent.input("What is 5 + 3?")
```

### 2. Class-based Tools (Stateful)
Tests that class instances can be used as tools with stateful methods.

**What's tested:**
- Class instance as tool
- Method discovery
- State persistence

### 3. Memory System
Tests the persistent memory system for key-value storage.

**What's tested:**
- `write_memory(key, value)`
- `read_memory(key)`
- `list_memories()`
- `search_memory(query)`
- Automatic directory scaling

### 4. Event System
Tests the hook-based event system for extending agent behavior.

**What's tested:**
- `after_user_input`
- `before_llm`
- `after_llm`
- `before_each_tool`
- `after_each_tool`
- `on_complete`
- `on_error`

### 5. llm_do (Direct LLM Calls)
Tests direct LLM calls without agent framework.

**What's tested:**
- Basic `llm_do()` calls
- Structured output with Pydantic
- System prompts
- Model selection

### 6. xray Debugging
Tests the interactive debugging system.

**What's tested:**
- `@xray` decorator
- Message tracking
- State inspection

### 7. Shell Tool
Tests shell command execution.

**What's tested:**
- Command execution
- Cross-platform support (Windows/PowerShell, Unix/bash)
- Timeout handling
- Output capture

### 8. Plugins (re_act)
Tests the ReAct plugin for planning and reflection.

**What's tested:**
- Plugin application
- Planning capabilities
- Reflection loops

### 9. DiffWriter Tool
Tests file writing with diff tracking.

**What's tested:**
- `write(file, content)`
- `read(file)`
- Diff generation

### 10. WebFetch Tool
Tests web content fetching.

**What's tested:**
- HTTP GET requests
- Content extraction
- Error handling

### 11. Logger and Session YAML
Tests logging and session tracking.

**What's tested:**
- Console logging
- Text file logging
- YAML session files
- Log directory structure (`.sb/logs`, `.sb/sessions`)

### 12. Multi-Agent with Shared Memory
Tests multiple agents sharing the same memory.

**What's tested:**
- Multiple agent instances
- Shared memory tool
- Cross-agent communication

### 13. Agent Networking (Address & Config)
Tests agent identity and networking configuration.

**What's tested:**
- Ed25519 key generation
- Address generation (`0x...`)
- Email generation (`@mail.shadowbar.internal`)
- Key storage (`.sb/keys`)

### 14. Trust System
Tests the trust/security system.

**What's tested:**
- Trust level checking
- Trust agent creation
- Whitelist management (`~/.shadowbar/trusted.txt`)

### 15. Relay Server
Tests the FastAPI-based relay server.

**What's tested:**
- FastAPI app creation
- WebSocket endpoints (`/ws/announce`, `/ws/input`, `/ws/lookup`)
- HTTP endpoints (`/`, `/agents`)
- Agent registration

### 16. Browser Agent (Playwright)
Tests browser automation capabilities.

**What's tested:**
- Browser instance management
- Navigation (`navigate(url)`)
- Screenshots (`take_screenshot()`)
- Content scraping (`scrape_content(selector)`)
- Link extraction (`extract_links()`)
- Form filling (`fill_form(data)`)
- JavaScript execution (`execute_javascript(script)`)
- Page interaction (`click(selector)`)
- Session management

## Expected Output

### Successful Test Run
```
======================================================================
[TEST 1: Basic Agent with Function Tools]
======================================================================
  ✅ PASS: Agent creation
  ✅ PASS: Tools registration
  ✅ PASS: Agent tool execution

...

======================================================================
TEST SUMMARY
======================================================================

Total Tests: 48
✅ Passed: 48
❌ Failed: 0
Success Rate: 100.0%

🎉 ALL TESTS PASSED!
```

### Failed Test
```
  ❌ FAIL: Agent tool execution
      Error: ANTHROPIC_API_KEY not set
```

## Troubleshooting

### API Key Issues
- Ensure `ANTHROPIC_API_KEY` is set in environment
- Or create `.env` file with `ANTHROPIC_API_KEY=your-key`
- Test with: `echo $ANTHROPIC_API_KEY` (Unix) or `echo %ANTHROPIC_API_KEY%` (Windows)

### Playwright Issues
- Install: `pip install playwright`
- Install browsers: `playwright install chromium`
- Check: `python -c "from playwright.sync_api import sync_playwright; print('OK')"`

### Import Errors
- Ensure you're in the `shadowbar` directory
- Install in development mode: `pip install -e .`
- Check Python path: `python -c "import shadowbar; print(shadowbar.__file__)"`

### Model Errors
- Ensure using correct model names: `claude-sonnet-4-5`, `claude-haiku-4-5`, `claude-opus-4-5`
- Check API key has access to Claude 4.5 models
- Fallback to legacy models if needed: `claude-3-5-sonnet-20241022`

## Continuous Testing

For CI/CD integration:

```bash
# Run tests and capture exit code
python test_all_features.py
EXIT_CODE=$?

# Check results
if [ $EXIT_CODE -eq 0 ]; then
    echo "All tests passed!"
else
    echo "Some tests failed!"
    exit 1
fi
```

## Next Steps

After all tests pass:
1. ✅ Verify all features work as expected
2. ✅ Check logs in `.sb/logs/` for any warnings
3. ✅ Review session files in `.sb/sessions/`
4. ✅ Test with real-world use cases
5. ✅ Document any edge cases found

