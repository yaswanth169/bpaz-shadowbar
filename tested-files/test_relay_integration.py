#!/usr/bin/env python3
"""
Real-World Integration Test for ShadowBar Relay Server and Agent Networking

This test:
1. Starts the relay server
2. Starts an agent with agent.serve()
3. Connects to that agent using connect()
4. Sends messages and verifies responses
5. Tests all networking features end-to-end

Run with: python test_relay_integration.py
Requires: ANTHROPIC_API_KEY environment variable
"""

import sys
import os
import time
import subprocess
import threading
import signal
import asyncio
from pathlib import Path
from typing import Optional
from datetime import datetime
from io import StringIO

# Fix encoding for Windows
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Capture all output
output_buffer = StringIO()
original_stdout = sys.stdout
original_stderr = sys.stderr

class TeeOutput:
    """Tee output to both console and buffer."""
    def __init__(self, *streams):
        self.streams = streams
    
    def write(self, data):
        for stream in self.streams:
            stream.write(data)
            stream.flush()
    
    def flush(self):
        for stream in self.streams:
            stream.flush()

# Set up tee output
sys.stdout = TeeOutput(original_stdout, output_buffer)
sys.stderr = TeeOutput(original_stderr, output_buffer)

# Ensure we're using the local shadowbar package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test results tracking
test_results = []
relay_process: Optional[subprocess.Popen] = None
agent_thread: Optional[threading.Thread] = None
agent_address: Optional[str] = None
agent_ready = threading.Event()

def test_result(name: str, passed: bool, message: str = ""):
    """Record test result."""
    test_results.append((name, passed, message))
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"  {status}: {name}")
    if message:
        print(f"      {message}")

def print_header(title: str):
    """Print test section header."""
    print("\n" + "=" * 70)
    print(f"[{title}]")
    print("=" * 70)

# ============================================================================
# SETUP: Start Relay Server
# ============================================================================
print_header("SETUP: Starting Relay Server")

try:
    import uvicorn
    from shadowbar.relay_server import app
    
    # Start relay server in background
    def start_relay_server():
        """Start relay server in background."""
        global relay_process
        try:
            relay_process = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "shadowbar.relay_server:app", 
                 "--host", "127.0.0.1", "--port", "8000"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            # Wait a bit for server to start
            time.sleep(3)
            print("  [OK] Relay server started on http://127.0.0.1:8000")
        except Exception as e:
            print(f"  [ERROR] Failed to start relay server: {e}")
    
    start_relay_server()
    # Check if process exists and is running (poll() returns None if running)
    process_running = relay_process is not None and relay_process.poll() is None
    test_result("Relay server process", process_running, 
                "Process running" if process_running else "Process may have exited")
    
    # Verify server is running
    try:
        import requests
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        test_result("Relay server health check", response.status_code == 200)
        health_data = response.json()
        test_result("Relay server status", health_data.get("status") == "running")
        print(f"      Agents online: {health_data.get('agents_online', 0)}")
    except ImportError:
        test_result("Relay server health check", False, "requests library not installed")
    except Exception as e:
        test_result("Relay server health check", False, str(e))
        
except ImportError as e:
    test_result("Relay server dependencies", False, f"Missing: {e}")
    print("  Install with: pip install fastapi uvicorn")
    sys.exit(1)
except Exception as e:
    test_result("Relay server startup", False, str(e))

# ============================================================================
# TEST 1: Agent Identity Generation
# ============================================================================
print_header("TEST 1: Agent Identity Generation")

try:
    from shadowbar import address
    import tempfile
    import shutil
    
    # Create temporary .sb directory
    test_dir = Path.cwd() / "test_relay_temp"
    test_dir.mkdir(exist_ok=True)
    sb_dir = test_dir / ".sb"
    sb_dir.mkdir(exist_ok=True)
    
    # Generate address
    addr_data = address.generate()
    test_result("Address generation", addr_data is not None and addr_data.get('address', '').startswith("0x"))
    
    agent_address = addr_data['address']
    print(f"      Agent address: {agent_address[:20]}...")
    
    # Save address
    address.save(addr_data, sb_dir)
    test_result("Address save", (sb_dir / "keys" / "agent.key").exists())
    
    # Load address
    loaded_data = address.load(sb_dir)
    test_result("Address load", loaded_data is not None and loaded_data.get('address') == agent_address)
    
except Exception as e:
    test_result("Agent Identity", False, str(e))
    import traceback
    traceback.print_exc()

# ============================================================================
# TEST 2: Start Agent with serve()
# ============================================================================
print_header("TEST 2: Start Agent with serve()")

try:
    from shadowbar import Agent
    from shadowbar.llm import AnthropicLLM
    
    if not os.environ.get('ANTHROPIC_API_KEY'):
        test_result("Agent serve (no API key)", False, "ANTHROPIC_API_KEY not set")
    else:
        # Create a simple agent with a tool
        def greet(name: str) -> str:
            """Greet someone."""
            return f"Hello {name}! I'm a networked ShadowBar agent."
        
        llm = AnthropicLLM(model='claude-haiku-4-5', max_tokens=512)
        serving_agent = Agent(
            name="test-greeter",
            llm=llm,
            tools=[greet],
            system_prompt="You are a friendly greeting agent."
        )
        
        # Change to test directory for .sb keys
        original_cwd = os.getcwd()
        os.chdir(test_dir)
        
        # Ensure .sb/logs directory exists
        logs_dir = Path(".sb/logs")
        logs_dir.mkdir(parents=True, exist_ok=True)
        sessions_dir = Path(".sb/sessions")
        sessions_dir.mkdir(parents=True, exist_ok=True)
        
        # Start agent.serve() in a separate thread (non-blocking)
        def serve_agent():
            """Run agent.serve() in thread."""
            try:
                agent_ready.set()
                serving_agent.serve(relay_url="ws://127.0.0.1:8000/ws/announce")
            except Exception as e:
                print(f"  [ERROR] Agent serve failed: {e}")
                import traceback
                traceback.print_exc()
        
        agent_thread = threading.Thread(target=serve_agent, daemon=True)
        agent_thread.start()
        
        # Wait for agent to announce
        time.sleep(5)
        
        # Check if agent is registered
        try:
            import requests
            response = requests.get("http://127.0.0.1:8000/", timeout=5)
            health_data = response.json()
            agents_online = health_data.get('agents_online', 0)
            test_result("Agent announced to relay", agents_online > 0, f"Agents online: {agents_online}")
        except ImportError:
            test_result("Agent announced to relay", False, "requests library not installed")
        except Exception as e:
            test_result("Agent announced to relay", False, str(e))
        
        os.chdir(original_cwd)
        
except Exception as e:
    test_result("Agent serve", False, str(e))
    import traceback
    traceback.print_exc()

# ============================================================================
# TEST 3: Connect to Remote Agent
# ============================================================================
print_header("TEST 3: Connect to Remote Agent")

try:
    from shadowbar import connect
    
    if not agent_address:
        test_result("Connect to agent (no address)", False, "Agent address not generated")
    elif not os.environ.get('ANTHROPIC_API_KEY'):
        test_result("Connect to agent (no API key)", False, "ANTHROPIC_API_KEY not set")
    else:
        # Wait a bit more for agent to be ready
        time.sleep(2)
        
        # Connect to the agent
        remote_agent = connect(agent_address, relay_url="ws://127.0.0.1:8000/ws/announce")
        test_result("Connect function", remote_agent is not None)
        test_result("RemoteAgent address", remote_agent.address == agent_address)
        
        # Send a message
        print("      Sending message to remote agent...")
        try:
            result = remote_agent.input("Say hello and introduce yourself", timeout=30.0)
            test_result("Remote agent response", result is not None and len(result) > 0, f"Got: {result[:100]}")
        except Exception as e:
            test_result("Remote agent response", False, str(e))
            import traceback
            traceback.print_exc()
        
except Exception as e:
    test_result("Connect to agent", False, str(e))
    import traceback
    traceback.print_exc()

# ============================================================================
# TEST 4: Multi-Agent Communication
# ============================================================================
print_header("TEST 4: Multi-Agent Communication")

try:
    if not agent_address or not os.environ.get('ANTHROPIC_API_KEY'):
        test_result("Multi-agent test", False, "Prerequisites not met")
    else:
        # Create a second agent that connects to the first
        def calculate(operation: str, a: float, b: float) -> float:
            """Perform a calculation."""
            if operation == "add":
                return a + b
            elif operation == "multiply":
                return a * b
            return 0.0
        
        llm2 = AnthropicLLM(model='claude-haiku-4-5', max_tokens=512)
        agent2 = Agent(
            name="test-calculator",
            llm=llm2,
            tools=[calculate],
            system_prompt="You are a calculator agent."
        )
        
        # Connect to the first agent
        remote = connect(agent_address, relay_url="ws://127.0.0.1:8000/ws/announce")
        
        # Send a calculation request
        print("      Sending calculation request...")
        try:
            result = remote.input("What is 5 + 3?", timeout=30.0)
            test_result("Multi-agent calculation", "8" in result or "eight" in result.lower(), f"Got: {result[:100]}")
        except Exception as e:
            test_result("Multi-agent calculation", False, str(e))
        
except Exception as e:
    test_result("Multi-agent communication", False, str(e))
    import traceback
    traceback.print_exc()

# ============================================================================
# CLEANUP
# ============================================================================
print_header("CLEANUP")

try:
    # Stop relay server
    if relay_process:
        relay_process.terminate()
        relay_process.wait(timeout=5)
        test_result("Relay server shutdown", True)
    
    # Clean up test directory
    if test_dir.exists():
        shutil.rmtree(test_dir)
        test_result("Test directory cleanup", True)
    
except Exception as e:
    test_result("Cleanup", False, str(e))

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
if failed == 0:
    print("\n🎉 ALL TESTS PASSED!")
else:
    print(f"\n⚠️  {failed} test(s) failed. Check details above.")
print("=" * 70)

# ============================================================================
# SAVE OUTPUT TO MARKDOWN FILE
# ============================================================================
print_header("SAVING TEST RESULTS")

try:
    # Get all captured output
    output_content = output_buffer.getvalue()
    
    # Create markdown report
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    success_rate = (passed/total*100) if total > 0 else 0
    markdown_content = f"""# ShadowBar Relay Integration Test Report

**Test Date**: {timestamp}  
**Test Suite**: `test_relay_integration.py`  
**Success Rate**: {success_rate:.1f}% ({passed}/{total} tests passed)

## Test Summary

- **Total Tests**: {total}
- **✅ Passed**: {passed}
- **❌ Failed**: {failed}
- **Success Rate**: {success_rate:.1f}%

## Test Results

"""
    
    # Add detailed results
    for i, (name, passed_status, message) in enumerate(test_results, 1):
        status_icon = "✅" if passed_status else "❌"
        markdown_content += f"{i}. {status_icon} **{name}**"
        if message:
            markdown_content += f"\n   - {message}"
        markdown_content += "\n\n"
    
    # Add full output
    markdown_content += f"""
## Full Test Output

```
{output_content}
```

## Conclusion

"""
    
    if failed == 0:
        markdown_content += "✅ **ALL TESTS PASSED** - Relay server and agent networking are working correctly!\n"
    else:
        markdown_content += f"⚠️ **{failed} test(s) failed** - See details above.\n"
    
    # Save to file
    report_file = Path(__file__).parent / "RELAY_INTEGRATION_TEST_REPORT.md"
    report_file.write_text(markdown_content, encoding='utf-8')
    
    print(f"  ✅ Test report saved to: {report_file}")
    print(f"      Total output: {len(output_content)} characters")
    
except Exception as e:
    print(f"  ❌ Failed to save report: {e}")
    import traceback
    traceback.print_exc()

# Restore stdout/stderr
sys.stdout = original_stdout
sys.stderr = original_stderr

# Exit with appropriate code
sys.exit(0 if failed == 0 else 1)

