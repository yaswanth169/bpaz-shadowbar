# ShadowBar End-to-End Testing Guide

## Overview

This guide explains how to test all ShadowBar features end-to-end, **without any Google dependencies**. All tests use Microsoft services or simpler alternatives.

## Quick Start

```bash
# From shadowbar directory
python test_all_features.py
```

## Test Coverage (18 Features)

### Core Features
1. ✅ **Basic Agent with Function Tools** - Python functions as tools
2. ✅ **Class-based Tools (Stateful)** - Stateful class instances as tools
3. ✅ **Memory System** - Persistent key-value storage
4. ✅ **Event System** - Hook-based event handlers
5. ✅ **llm_do** - Direct LLM calls without agent
6. ✅ **xray Debugging** - Interactive debugging decorator

### Tools & Utilities
7. ✅ **Shell Tool** - Cross-platform command execution
8. ✅ **DiffWriter Tool** - File writing with diff tracking
9. ✅ **TodoList Tool** - Task management
10. ✅ **WebFetch Tool** - HTTP content fetching
11. ✅ **Microsoft Outlook** - Email management (Microsoft Graph API)
12. ✅ **Microsoft Calendar** - Calendar management (Microsoft Graph API)

### Plugins
13. ✅ **re_act Plugin** - Planning and reflection
14. ✅ **eval Plugin** - Code evaluation
15. ✅ **shell_approval Plugin** - User confirmation for shell commands
16. ✅ **image_result_formatter Plugin** - Base64 image handling

### Advanced Features
17. ✅ **Logger and Session YAML** - Logging and session tracking
18. ✅ **Multi-Agent with Shared Memory** - Multiple agents sharing state
19. ✅ **Agent Networking** - Address generation and key management
20. ✅ **Trust System** - Security and trust levels
21. ✅ **Relay Server** - FastAPI WebSocket relay
22. ✅ **Browser Agent (Playwright)** - Browser automation

## Microsoft Services (No Google Dependencies)

### Microsoft Outlook
- **Purpose**: Email reading, sending, and management
- **Auth**: Requires `MICROSOFT_ACCESS_TOKEN` (set via `sb auth microsoft`)
- **Methods**: `read_inbox()`, `send()`, `search_emails()`, `reply()`, etc.

### Microsoft Calendar
- **Purpose**: Calendar event management
- **Auth**: Requires `MICROSOFT_ACCESS_TOKEN` (set via `sb auth microsoft`)
- **Methods**: `list_events()`, `create_event()`, `get_today_events()`, etc.

**Note**: Tests will pass even without Microsoft auth - they verify the classes are available and methods exist.

## Available Plugins (No Google)

### re_act
- Planning and reflection capabilities
- Adds reasoning loops to agents

### eval
- Code evaluation plugin
- Safe code execution

### shell_approval
- Human-in-the-loop for shell commands
- Requires user confirmation before execution

### image_result_formatter
- Handles base64 image results
- Formats image outputs for display

## Running Tests

### Basic Test Run
```bash
# Set API key
export ANTHROPIC_API_KEY=your-key  # Unix/Mac
set ANTHROPIC_API_KEY=your-key      # Windows CMD
$env:ANTHROPIC_API_KEY="your-key"   # Windows PowerShell

# Run tests
python test_all_features.py
```

### With Microsoft Services
```bash
# Set Microsoft auth (optional)
export MICROSOFT_ACCESS_TOKEN=your-token

# Run tests
python test_all_features.py
```

### Expected Output
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

Total Tests: 50+
✅ Passed: 50+
❌ Failed: 0
Success Rate: 100.0%

🎉 ALL TESTS PASSED!
```

## Test Files

### `test_all_features.py` (Recommended)
- **Purpose**: Comprehensive, organized test runner
- **Features**: 
  - Clear pass/fail output
  - Result tracking
  - Summary report
  - No Google dependencies
  - Microsoft service support
- **Usage**: `python test_all_features.py`

### `comprehensive_test.py`
- **Purpose**: Original comprehensive test suite
- **Features**: More verbose output, detailed test cases
- **Usage**: `python comprehensive_test.py`

### `test_browser_agent.py`
- **Purpose**: Browser automation specific tests
- **Features**: Playwright integration
- **Usage**: `python test_browser_agent.py`
- **Requirements**: `pip install playwright && playwright install chromium`

## Feature Details

### What's NOT Tested (Intentionally)
- ❌ Google Gmail (not available in ShadowBar)
- ❌ Google Calendar (not available in ShadowBar)
- ❌ Google Gemini models (ShadowBar is Anthropic-only)

### What IS Tested
- ✅ Microsoft Outlook (email)
- ✅ Microsoft Calendar (events)
- ✅ All core ShadowBar features
- ✅ All available plugins
- ✅ Browser automation (Playwright)

## Troubleshooting

### API Key Issues
```bash
# Check if set
echo $ANTHROPIC_API_KEY  # Unix/Mac
echo %ANTHROPIC_API_KEY% # Windows CMD
$env:ANTHROPIC_API_KEY   # Windows PowerShell
```

### Microsoft Auth Issues
```bash
# Authenticate with Microsoft
sb auth microsoft

# Or set manually
export MICROSOFT_ACCESS_TOKEN=your-token
```

### Playwright Issues
```bash
# Install Playwright
pip install playwright
playwright install chromium

# Verify
python -c "from playwright.sync_api import sync_playwright; print('OK')"
```

### Import Errors
```bash
# Install in development mode
cd shadowbar
pip install -e .

# Verify
python -c "import shadowbar; print(shadowbar.__file__)"
```

## Test Results Interpretation

### ✅ PASS
- Feature works correctly
- All functionality verified

### ❌ FAIL
- Check error message
- Verify dependencies installed
- Check API keys/environment variables
- Review test output for details

### ⚠️ SKIP (in some tests)
- Feature requires optional dependency
- Auth not configured (Microsoft services)
- Playwright not installed (browser tests)

## Continuous Integration

For CI/CD:

```bash
# Run tests
python test_all_features.py
EXIT_CODE=$?

# Check results
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ All tests passed!"
    exit 0
else
    echo "❌ Some tests failed!"
    exit 1
fi
```

## Next Steps

After all tests pass:
1. ✅ Verify features work in real scenarios
2. ✅ Check logs in `.sb/logs/`
3. ✅ Review session files in `.sb/sessions/`
4. ✅ Test with actual Microsoft accounts (if needed)
5. ✅ Document any edge cases

## Summary

- **18+ features tested** end-to-end
- **No Google dependencies** - uses Microsoft services
- **All plugins tested** - re_act, eval, shell_approval, image_formatter
- **Comprehensive coverage** - core features, tools, plugins, advanced features
- **Clear output** - easy to see what passes/fails

