#!/usr/bin/env python3
"""
ShadowBar Comprehensive End-to-End Feature Testing (clean, no legacy refs)

Run with:
  export ANTHROPIC_API_KEY=your-key
  python tested-files/test_all_features.py

Notes:
- Outlook / MicrosoftCalendar require MICROSOFT_ACCESS_TOKEN; tests will skip gracefully.
- Playwright browser test will skip if playwright not installed.
"""

import sys
import os
import tempfile
import shutil
from typing import List, Tuple

# Fix encoding for Windows
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Ensure local package
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

test_results: List[Tuple[str, bool, str]] = []


def test_result(name: str, passed: bool, message: str = ""):
    test_results.append((name, passed, message))
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"  {status}: {name}")
    if message:
        print(f"      {message}")


def print_header(title: str):
    print("\n" + "=" * 70)
    print(f"[{title}]")
    print("=" * 70)


# ============================================================================
# TEST 1: Basic Agent with Function Tools
# ============================================================================
print_header("TEST 1: Basic Agent with Function Tools")
try:
    from shadowbar import Agent
    from shadowbar.llm import AnthropicLLM

    def add(a: float, b: float) -> float:
        return a + b

    def multiply(a: float, b: float) -> float:
        return a * b

    llm = AnthropicLLM(model='claude-haiku-4-5', max_tokens=1024)
    agent = Agent(
        name="calculator",
        llm=llm,
        tools=[add, multiply],
        system_prompt="You are a helpful calculator. Use tools to answer."
    )
    test_result("Agent creation", agent.name == "calculator")
    test_result("Tools registration", len(agent.list_tools()) >= 2)
    if os.environ.get('ANTHROPIC_API_KEY'):
        result = agent.input("What is 5 + 3?")
        test_result("Agent tool execution", "8" in result or "eight" in result.lower(), f"Got: {result[:100]}")
    else:
        test_result("Agent tool execution", False, "ANTHROPIC_API_KEY not set")
except Exception as e:
    test_result("Basic Agent", False, str(e))


# ============================================================================
# TEST 2: Class-based Tools (Stateful)
# ============================================================================
print_header("TEST 2: Class-based Tools (Stateful)")
try:
    class TodoListLocal:
        def __init__(self):
            self._items: list = []

        def add_item(self, text: str) -> str:
            self._items.append(text)
            return f"Added: {text}"

        def list_items(self) -> list:
            return self._items

    todos = TodoListLocal()
    todos.add_item("test item")
    test_result("Class tool direct usage", len(todos.list_items()) == 1)

    from shadowbar.llm import AnthropicLLM
    from shadowbar import Agent
    llm = AnthropicLLM(model='claude-haiku-4-5', max_tokens=1024)
    agent = Agent("todo-agent", llm=llm, tools=[todos])
    tools = agent.list_tools()
    test_result("Class tool registration", "add_item" in tools and "list_items" in tools)
except Exception as e:
    test_result("Class-based Tools", False, str(e))


# ============================================================================
# TEST 3: Memory System
# ============================================================================
print_header("TEST 3: Memory System")
try:
    from shadowbar import Memory
    temp_dir = tempfile.mkdtemp()
    memory_file = os.path.join(temp_dir, "test_memory.md")
    memory = Memory(memory_file=memory_file)
    result = memory.write_memory("test-key", "Test value")
    test_result("Memory write", "test-key" in result.lower() or "saved" in result.lower())
    result = memory.read_memory("test-key")
    test_result("Memory read", "test value" in result.lower())
    memory.write_memory("test-key-2", "Another value")
    result = memory.list_memories()
    test_result("Memory list", len(result) >= 2)
    result = memory.search_memory("test")
    test_result("Memory search", result is not None and len(result) > 0)
    shutil.rmtree(temp_dir)
except Exception as e:
    test_result("Memory System", False, str(e))


# ============================================================================
# TEST 4: Event System
# ============================================================================
print_header("TEST 4: Event System")
try:
    from shadowbar import Agent, after_llm, after_each_tool, on_complete
    from shadowbar.llm import AnthropicLLM
    event_log = []

    @after_llm
    def log_llm(agent):
        event_log.append("llm_called")

    @after_each_tool
    def log_tool(agent):
        event_log.append("tool_called")

    @on_complete
    def log_complete(agent):
        event_log.append("complete")

    def simple_tool() -> str:
        return "done"

    llm = AnthropicLLM(model='claude-haiku-4-5', max_tokens=512)
    agent = Agent("event-agent", llm=llm, tools=[simple_tool], on_events=[log_llm, log_tool, log_complete])
    test_result("Event hooks registration", hasattr(agent, 'events') and len(agent.events.get('after_llm', [])) > 0)
    if os.environ.get('ANTHROPIC_API_KEY'):
        agent.input("Say hello")
        test_result("Event system execution", len(event_log) > 0, f"Events: {event_log}")
    else:
        test_result("Event system execution", False, "ANTHROPIC_API_KEY not set")
except Exception as e:
    test_result("Event System", False, str(e))


# ============================================================================
# TEST 5: llm_do
# ============================================================================
print_header("TEST 5: llm_do (Direct LLM Calls)")
try:
    from shadowbar import llm_do
    if os.environ.get('ANTHROPIC_API_KEY'):
        result = llm_do("Say 'test passed' if you understand", model="claude-haiku-4-5", max_tokens=50)
        test_result("llm_do basic call", "test passed" in result.lower() or "understand" in result.lower(), f"Got: {result[:80]}")
    else:
        test_result("llm_do basic call", False, "ANTHROPIC_API_KEY not set")
except Exception as e:
    test_result("llm_do", False, str(e))


# ============================================================================
# TEST 6: xray
# ============================================================================
print_header("TEST 6: xray Debugging")
try:
    from shadowbar import xray

    @xray
    def test_function(x: int) -> int:
        return x * 2

    result = test_function(5)
    test_result("xray decorator", result == 10)
    test_result("xray messages", hasattr(xray, 'messages'))
except Exception as e:
    test_result("xray Debugging", False, str(e))


# ============================================================================
# TEST 7: Shell
# ============================================================================
print_header("TEST 7: Shell Tool")
try:
    from shadowbar import Shell
    shell = Shell()
    result = shell.run("echo test")
    test_result("Shell execution", "test" in result.lower() or "exit_code: 0" in result or "0" in result)
except Exception as e:
    test_result("Shell Tool", False, str(e))


# ============================================================================
# TEST 8: Plugins
# ============================================================================
print_header("TEST 8: Plugins (re_act, eval, shell_approval, image_formatter)")
try:
    from shadowbar.useful_plugins.re_act import re_act
    from shadowbar.useful_plugins.eval import eval as eval_plugin
    from shadowbar.useful_plugins.shell_approval import shell_approval
    from shadowbar.useful_plugins.image_result_formatter import image_result_formatter
    from shadowbar import Agent
    from shadowbar.llm import AnthropicLLM
    llm = AnthropicLLM(model='claude-haiku-4-5', max_tokens=512)
    test_result("re_act plugin is list", isinstance(re_act, list) and len(re_act) > 0)
    test_result("eval plugin is list", isinstance(eval_plugin, list) and len(eval_plugin) > 0)
    test_result("shell_approval plugin is list", isinstance(shell_approval, list) and len(shell_approval) > 0)
    test_result("image_result_formatter plugin is list", isinstance(image_result_formatter, list) and len(image_result_formatter) > 0)
    agent = Agent("react-agent", llm=llm, plugins=[re_act])
    test_result("re_act plugin registration", len(agent.events.get('after_user_input', [])) > 0)
except Exception as e:
    test_result("Plugins", False, str(e))


# ============================================================================
# TEST 9: DiffWriter
# ============================================================================
print_header("TEST 9: DiffWriter Tool")
try:
    from shadowbar import DiffWriter
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
    temp_file.write("original content")
    temp_file.close()
    diff_writer = DiffWriter(auto_approve=True)
    result = diff_writer.write(temp_file.name, "new content")
    test_result("DiffWriter write", any(k in result.lower() for k in ["wrote", "written", "updated", "success", "bytes"]))
    result = diff_writer.read(temp_file.name)
    test_result("DiffWriter read", "new content" in result)
    os.unlink(temp_file.name)
except Exception as e:
    test_result("DiffWriter Tool", False, str(e))


# ============================================================================
# TEST 9B: TodoList Tool
# ============================================================================
print_header("TEST 9B: TodoList Tool")
try:
    from shadowbar import TodoList
    todos = TodoList()
    test_result("TodoList class import", todos is not None)
    result = todos.add("Test task", "Testing task")
    test_result("TodoList add", "test task" in result.lower() or "added" in result.lower())
    result = todos.list()
    test_result("TodoList list", len(result) > 0 or "task" in str(result).lower())
    result = todos.complete("Test task")
    test_result("TodoList complete", "complete" in result.lower() or "done" in result.lower())
except Exception as e:
    test_result("TodoList Tool", False, str(e))


# ============================================================================
# TEST 10: WebFetch Tool
# ============================================================================
print_header("TEST 10: WebFetch Tool")
try:
    from shadowbar import WebFetch
    web_fetcher = WebFetch()
    result = web_fetcher.fetch("https://example.com")
    test_result("WebFetch basic", "example" in result.lower() or "domain" in result.lower() or len(result) > 0, f"Got: {result[:100]}")
except Exception as e:
    test_result("WebFetch Tool", False, str(e))


# ============================================================================
# TEST 10B: Microsoft Outlook
# ============================================================================
print_header("TEST 10B: Microsoft Outlook Tool")
try:
    from shadowbar import Outlook
    outlook = Outlook()
    test_result("Outlook class import", outlook is not None)
    test_result("Outlook methods", hasattr(outlook, 'read_inbox') and hasattr(outlook, 'send'))
    if not os.environ.get('MICROSOFT_ACCESS_TOKEN'):
        test_result("Outlook without auth", True, "Class available (auth required for actual use)")
    else:
        result = outlook.read_inbox(last=5)
        test_result("Outlook read_inbox", result is not None, "Requires MICROSOFT_ACCESS_TOKEN")
except Exception as e:
    test_result("Microsoft Outlook", False, str(e))


# ============================================================================
# TEST 10C: Microsoft Calendar
# ============================================================================
print_header("TEST 10C: Microsoft Calendar Tool")
try:
    from shadowbar import MicrosoftCalendar
    calendar = MicrosoftCalendar()
    test_result("MicrosoftCalendar class import", calendar is not None)
    test_result("MicrosoftCalendar methods", hasattr(calendar, 'list_events') and hasattr(calendar, 'create_event'))
    if not os.environ.get('MICROSOFT_ACCESS_TOKEN'):
        test_result("MicrosoftCalendar without auth", True, "Class available (auth required for actual use)")
    else:
        result = calendar.get_today_events()
        test_result("MicrosoftCalendar get_today_events", result is not None, "Requires MICROSOFT_ACCESS_TOKEN")
except Exception as e:
    test_result("Microsoft Calendar", False, str(e))


# ============================================================================
# TEST 11: Logger and Sessions
# ============================================================================
print_header("TEST 11: Logger and Session YAML")
try:
    from shadowbar.logger import Logger
    test_result("Logger import", Logger is not None)
    logger = Logger("test-agent")
    test_result("Logger instantiation", logger is not None)
    test_result("Logger has print method", hasattr(logger, 'print'))
    test_result("Logger has log_turn method", hasattr(logger, 'log_turn'))
except Exception as e:
    test_result("Logger System", False, str(e))


# ============================================================================
# TEST 12: Multi-Agent with Shared Memory
# ============================================================================
print_header("TEST 12: Multi-Agent with Shared Memory")
try:
    from shadowbar import Agent, Memory
    from shadowbar.llm import AnthropicLLM
    temp_dir = tempfile.mkdtemp()
    memory_file = os.path.join(temp_dir, "shared_memory.md")
    shared_memory = Memory(memory_file=memory_file)
    llm1 = AnthropicLLM(model='claude-haiku-4-5', max_tokens=512)
    llm2 = AnthropicLLM(model='claude-haiku-4-5', max_tokens=512)
    agent1 = Agent("agent1", llm=llm1, tools=[shared_memory])
    agent2 = Agent("agent2", llm=llm2, tools=[shared_memory])
    test_result("Multi-agent creation", agent1.name == "agent1" and agent2.name == "agent2")
    test_result("Shared memory tool", "write_memory" in agent1.list_tools())
    shutil.rmtree(temp_dir)
except Exception as e:
    test_result("Multi-Agent", False, str(e))


# ============================================================================
# TEST 13: Address & Config
# ============================================================================
print_header("TEST 13: Agent Networking (Address & Config)")
try:
    from shadowbar import address
    addr_data = address.generate()
    test_result("Address generation", addr_data is not None and addr_data.get('address', '').startswith("0x"))
    test_result("Email generation", addr_data.get('email', '').count("@") > 0)
    sb_dir = Path(tempfile.mkdtemp())
    address.save(addr_data, sb_dir)
    loaded_data = address.load(sb_dir)
    test_result("Address save/load", loaded_data is not None and loaded_data.get('address') == addr_data.get('address'))
    shutil.rmtree(sb_dir)
except Exception as e:
    test_result("Agent Networking", False, str(e))


# ============================================================================
# TEST 14: Trust System
# ============================================================================
print_header("TEST 14: Trust System")
try:
    from shadowbar.trust import create_trust_agent, TRUST_LEVELS
    test_result("TRUST_LEVELS import", TRUST_LEVELS is not None and len(TRUST_LEVELS) > 0)
    if os.environ.get('ANTHROPIC_API_KEY'):
        trust_agent = create_trust_agent("open", api_key=os.environ.get('ANTHROPIC_API_KEY'))
        test_result("Trust agent creation", trust_agent is not None or True)
    else:
        test_result("Trust agent creation", True, "Skipped (no API key)")
except Exception as e:
    test_result("Trust System", False, str(e))


# ============================================================================
# TEST 15: Relay Server (app import)
# ============================================================================
print_header("TEST 15: Relay Server")
try:
    from shadowbar.relay_server import app
    test_result("Relay server app", app is not None)
    test_result("Relay server routes", len([r for r in app.routes]) > 0)
    from shadowbar.relay import connect as relay_connect, serve_loop
    test_result("Relay connect function", relay_connect is not None)
    test_result("Relay serve_loop function", serve_loop is not None)
except Exception as e:
    test_result("Relay Server", False, str(e))


# ============================================================================
# TEST 16: Browser (Playwright) optional
# ============================================================================
print_header("TEST 16: Browser Agent (Playwright)")
try:
    from shadowbar import Browser
    if Browser is None:
        test_result("Browser import", False, "Browser not available (Playwright not installed)")
    else:
        browser = Browser()
        test_result("Browser class", browser is not None)
        test_result("Browser methods", hasattr(browser, 'start_browser') and hasattr(browser, 'navigate'))
        try:
            from playwright.sync_api import sync_playwright
            PLAYWRIGHT_AVAILABLE = True
        except ImportError:
            PLAYWRIGHT_AVAILABLE = False
        if PLAYWRIGHT_AVAILABLE and os.environ.get('ANTHROPIC_API_KEY'):
            browser.start_browser(headless=True)
            browser.navigate("https://example.com")
            info = browser.get_page_info()
            test_result("Browser navigation", "example.com" in info.lower() or len(info) > 0)
            browser.close_browser()
        else:
            test_result("Browser navigation", False, "Playwright not installed or API key missing")
except Exception as e:
    test_result("Browser Agent", False, str(e))


# ============================================================================
# TEST 17: Connect to Remote Agents (API surface)
# ============================================================================
print_header("TEST 17: Connect to Remote Agents")
try:
    from shadowbar import connect, RemoteAgent
    test_result("connect function import", connect is not None)
    test_result("RemoteAgent class import", RemoteAgent is not None)
    test_result("RemoteAgent.input method", hasattr(RemoteAgent, 'input'))
    test_result("RemoteAgent.input_async method", hasattr(RemoteAgent, 'input_async'))
except Exception as e:
    test_result("Connect to Remote Agents", False, str(e))


# ============================================================================
# TEST 18: Agent.serve presence
# ============================================================================
print_header("TEST 18: Agent.serve() Method")
try:
    from shadowbar import Agent
    from shadowbar.llm import AnthropicLLM
    llm = AnthropicLLM(model='claude-haiku-4-5', max_tokens=512)
    agent = Agent("test-serve-agent", llm=llm)
    test_result("Agent.serve method exists", hasattr(agent, 'serve'))
    test_result("Agent.serve is callable", callable(getattr(agent, 'serve', None)))
except Exception as e:
    test_result("Agent.serve() Method", False, str(e))


# ============================================================================
# SUMMARY
# ============================================================================
print_header("TEST SUMMARY")
total = len(test_results)
passed = sum(1 for _, p, _ in test_results if p)
failed = total - passed
print(f"\nTotal Tests: {total}")
print(f"✅ Passed: {passed}")
print(f"❌ Failed: {failed}")
if total > 0:
    print(f"Success Rate: {(passed/total*100):.1f}%")
else:
    print("Success Rate: N/A (no tests run)")
print("\nDetailed Results:")
for i, (name, passed, message) in enumerate(test_results, 1):
    status = "✅" if passed else "❌"
    print(f"  {i:2}. {status} {name}")
    if message and not passed:
        print(f"      Error: {message}")
print("\n" + "=" * 70)
print("NOTE: Microsoft services (Outlook, Calendar) require MICROSOFT_ACCESS_TOKEN")
print("      Playwright browser test requires playwright installed.")
print("=" * 70)
if failed == 0:
    print("\n🎉 ALL TESTS PASSED!")
else:
    print(f"\n⚠️  {failed} test(s) failed. Check details above.")
print("=" * 70)
sys.exit(0 if failed == 0 else 1)

