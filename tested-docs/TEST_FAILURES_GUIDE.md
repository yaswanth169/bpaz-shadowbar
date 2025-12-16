# ShadowBar Test Failures - Troubleshooting Guide

## Common Test Failures and Fixes

### 1. Import Errors

**Error**: `ModuleNotFoundError: No module named 'shadowbar'`

**Fix**:
```bash
# Install in development mode
cd shadowbar
pip install -e .
```

### 2. API Key Not Set

**Error**: `ANTHROPIC_API_KEY not set`

**Fix**:
```bash
# Windows PowerShell
$env:ANTHROPIC_API_KEY="your-key"

# Windows CMD
set ANTHROPIC_API_KEY=your-key

# Unix/Mac
export ANTHROPIC_API_KEY=your-key
```

### 3. Model Not Found

**Error**: `anthropic.NotFoundError: model: claude-haiku-4-5`

**Fix**: 
- Verify your API key has access to Claude 4.5 models
- Try using `claude-sonnet-4-5` instead
- Check Anthropic console for model availability

### 4. Shell Tool Method Error

**Error**: `'Shell' object has no attribute 'execute'`

**Fix**: Use `.run()` instead of `.execute()`
```python
shell = Shell()
result = shell.run("echo test")  # Correct
# NOT: shell.execute("echo test")  # Wrong
```

### 5. WebFetch Method Error

**Error**: `'WebFetch' object has no attribute 'web_fetch'`

**Fix**: Use `.fetch()` method
```python
web = WebFetch()
result = web.fetch("https://example.com")  # Correct
```

### 6. TodoList Method Error

**Error**: `add() missing 1 required positional argument: 'active_form'`

**Fix**: TodoList.add() requires both `content` and `active_form`
```python
todos = TodoList()
result = todos.add("Test task", "Testing task")  # Correct
# NOT: todos.add("Test task")  # Wrong
```

### 7. Event System Error

**Error**: `'Agent' object has no attribute '_event_handlers'`

**Fix**: Use public `.events` attribute
```python
agent.events['after_llm'].append(handler)  # Correct
# NOT: agent._event_handlers['after_llm'].append(handler)  # Wrong
```

### 8. Playwright Not Installed

**Error**: `ImportError: cannot import name 'sync_playwright'`

**Fix**:
```bash
pip install playwright
playwright install chromium
```

### 9. Microsoft Services Auth

**Error**: `ValueError: Microsoft OAuth not configured`

**Fix**: This is expected if `MICROSOFT_ACCESS_TOKEN` is not set
- Tests will pass (verifying class exists)
- For actual functionality: `sb auth microsoft`

### 10. DiffWriter Read Error

**Error**: `'DiffWriter' object has no attribute 'read_file'`

**Fix**: Use `.read()` method
```python
diff_writer = DiffWriter()
content = diff_writer.read(file_path)  # Correct
# NOT: diff_writer.read_file(file_path)  # Wrong
```

## Test Execution Tips

### Run Individual Tests

You can modify the test file to run only specific tests:

```python
# Comment out tests you don't want to run
# print_header("TEST 16: Browser Agent")
# ... test code ...
```

### Skip Live LLM Calls

To save API costs, you can skip actual LLM calls:

```python
if os.environ.get('ANTHROPIC_API_KEY') and os.environ.get('RUN_LIVE_TESTS'):
    result = agent.input("What is 5 + 3?")
    # ... test ...
else:
    test_result("Agent tool execution", True, "Skipped (set RUN_LIVE_TESTS=1 to enable)")
```

### Verbose Output

Add more debugging:

```python
import traceback
try:
    # test code
except Exception as e:
    test_result("Test Name", False, str(e))
    traceback.print_exc()  # Full stack trace
```

## Expected Test Results

### All Tests Should Pass If:
- ✅ ShadowBar installed (`pip install -e .`)
- ✅ `ANTHROPIC_API_KEY` set
- ✅ Python 3.8+
- ✅ Internet connection (for WebFetch, Browser tests)

### Some Tests May Skip If:
- ⚠️ Playwright not installed (Browser test)
- ⚠️ Microsoft auth not configured (Outlook/Calendar tests)
- ⚠️ Network issues (WebFetch test)

### Tests That Require Live API Calls:
- Agent tool execution
- llm_do calls
- Event system execution
- Browser agent with LLM

## Quick Diagnostic

Run this to check your setup:

```python
import sys
print(f"Python: {sys.version}")

try:
    import shadowbar
    print(f"✅ ShadowBar: {shadowbar.__version__}")
except ImportError as e:
    print(f"❌ ShadowBar: {e}")

import os
if os.environ.get('ANTHROPIC_API_KEY'):
    print("✅ ANTHROPIC_API_KEY: Set")
else:
    print("❌ ANTHROPIC_API_KEY: Not set")

try:
    from playwright.sync_api import sync_playwright
    print("✅ Playwright: Installed")
except ImportError:
    print("⚠️ Playwright: Not installed (optional)")

if os.environ.get('MICROSOFT_ACCESS_TOKEN'):
    print("✅ MICROSOFT_ACCESS_TOKEN: Set")
else:
    print("⚠️ MICROSOFT_ACCESS_TOKEN: Not set (optional)")
```

## Still Having Issues?

1. Check the full error traceback
2. Verify all imports work: `python -c "import shadowbar; print('OK')"`
3. Test individual components:
   ```python
   from shadowbar import Agent, Shell, Memory
   shell = Shell()
   print(shell.run("echo test"))
   ```
4. Check ShadowBar version: `python -c "import shadowbar; print(shadowbar.__version__)"`
5. Review `.sb/logs/` for detailed error logs


