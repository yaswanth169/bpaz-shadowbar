"""
Purpose: Browser automation tool for ShadowBar using Playwright
LLM-Note:
  Dependencies: imports from [playwright.sync_api] (optional) | imported by [useful_tools/__init__.py] | requires playwright package
  Data flow: Agent calls Browser methods → methods use Playwright to control browser → returns results as strings
  State/Effects: stateful browser session (playwright, browser, page) | tracks visited_urls, screenshots | modifies filesystem with screenshots
  Integration: exposes Browser class with start_browser(), navigate(), scrape_content(), take_screenshot(), click(), etc. | used as agent tool via Agent(tools=[Browser()])
  Performance: browser launch overhead 1-3s | operations vary by page complexity
  Errors: graceful fallback if Playwright not installed | method-level error handling returns error strings
"""

import sys
from pathlib import Path
from typing import Optional, List, Dict
import json

# Check Playwright availability
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    sync_playwright = None

from ..xray import xray


class Browser:
    """Browser automation tool for ShadowBar - wraps Playwright functionality.
    
    This class provides a clean interface for browser automation that can be
    imported directly from shadowbar without dealing with Playwright imports.
    
    Example:
        >>> from shadowbar import Agent, Browser
        >>> browser = Browser()
        >>> agent = Agent("web_agent", tools=[browser])
        >>> agent.input("Open google.com and take a screenshot")
    """
    
    def __init__(self):
        """Initialize browser automation tool."""
        self.playwright = None
        self.browser = None
        self.page = None
        self.screenshots = []
        self.visited_urls = []
        self.downloads = []
    
    @xray
    def start_browser(self, headless: bool = True) -> str:
        """Start a browser instance.
        
        Args:
            headless: Run browser in headless mode (no UI). Set False to see browser.
        
        Returns:
            Success message or error if Playwright not installed
        """
        if not PLAYWRIGHT_AVAILABLE:
            return "[ERROR] Playwright not installed. Run: pip install playwright && playwright install chromium"
        
        if self.browser:
            return "[OK] Browser already running"
        
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=headless)
            self.page = self.browser.new_page()
            return f"[OK] Browser started (headless={headless})"
        except Exception as e:
            return f"[ERROR] Failed to start browser: {e}"
    
    @xray
    def navigate(self, url: str, wait_until: str = "networkidle") -> str:
        """Navigate to a URL.
        
        Args:
            url: The URL to navigate to (e.g., "https://example.com")
            wait_until: When to consider navigation done ('load', 'domcontentloaded', 'networkidle')
        
        Returns:
            Success message with page title or error message
        """
        if not PLAYWRIGHT_AVAILABLE:
            return "[ERROR] Playwright not installed. Run: pip install playwright && playwright install chromium"
        
        if not self.page:
            return "[ERROR] Browser not started. Call start_browser() first."
        
        try:
            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = f'https://{url}'
            
            self.page.goto(url, wait_until=wait_until, timeout=60000)
            self.visited_urls.append(url)
            title = self.page.title()
            return f"[OK] Navigated to {url}\nPage title: {title}"
        except Exception as e:
            return f"[ERROR] Navigation failed: {e}"
    
    @xray
    def take_screenshot(self, filename: Optional[str] = None, full_page: bool = False) -> str:
        """Take a screenshot of the current page.
        
        Args:
            filename: Name for the screenshot file (auto-generates if None)
            full_page: Capture full scrollable page (default: False)
        
        Returns:
            Success message with filename or error message
        """
        if not PLAYWRIGHT_AVAILABLE:
            return "[ERROR] Playwright not installed. Run: pip install playwright && playwright install chromium"
        
        if not self.page:
            return "[ERROR] No page loaded. Navigate to a URL first."
        
        if not filename:
            filename = f"screenshot_{len(self.screenshots) + 1}.png"
        
        try:
            # Ensure directory exists
            Path(filename).parent.mkdir(parents=True, exist_ok=True)
            self.page.screenshot(path=filename, full_page=full_page)
            self.screenshots.append(filename)
            return f"[OK] Screenshot saved as {filename}"
        except Exception as e:
            return f"[ERROR] Screenshot failed: {e}"
    
    @xray
    def scrape_content(self, selector: str = "body") -> str:
        """Extract text content from the page.
        
        Args:
            selector: CSS selector for the element to scrape (default: "body")
        
        Returns:
            Extracted text content or error message
        """
        if not PLAYWRIGHT_AVAILABLE:
            return "[ERROR] Playwright not installed. Run: pip install playwright && playwright install chromium"
        
        if not self.page:
            return "[ERROR] No page loaded. Navigate to a URL first."
        
        try:
            element = self.page.query_selector(selector)
            if element:
                text = element.inner_text()
                return text if text else "[WARNING] Element found but has no text content"
            else:
                return f"[ERROR] No element found matching selector: {selector}"
        except Exception as e:
            return f"[ERROR] Scraping failed: {e}"
    
    @xray
    def get_page_html(self) -> str:
        """Get the HTML content of the current page.
        
        Returns:
            HTML content or error message
        """
        if not PLAYWRIGHT_AVAILABLE:
            return "[ERROR] Playwright not installed. Run: pip install playwright && playwright install chromium"
        
        if not self.page:
            return "[ERROR] No page loaded. Navigate to a URL first."
        
        try:
            return self.page.content()
        except Exception as e:
            return f"[ERROR] Failed to get HTML: {e}"
    
    @xray
    def get_page_info(self) -> str:
        """Get information about the current page.
        
        Returns:
            Page information (URL, title) or error message
        """
        if not PLAYWRIGHT_AVAILABLE:
            return "[ERROR] Playwright not installed. Run: pip install playwright && playwright install chromium"
        
        if not self.page:
            return "[ERROR] No page loaded. Navigate to a URL first."
        
        try:
            info = {
                "url": self.page.url,
                "title": self.page.title(),
                "viewport": self.page.viewport_size,
            }
            return f"URL: {info['url']}\nTitle: {info['title']}\nViewport: {info['viewport']}"
        except Exception as e:
            return f"[ERROR] Failed to get page info: {e}"
    
    @xray
    def click(self, selector: str) -> str:
        """Click an element on the page.
        
        Args:
            selector: CSS selector for the element to click
        
        Returns:
            Success message or error message
        """
        if not PLAYWRIGHT_AVAILABLE:
            return "[ERROR] Playwright not installed. Run: pip install playwright && playwright install chromium"
        
        if not self.page:
            return "[ERROR] No page loaded. Navigate to a URL first."
        
        try:
            self.page.click(selector)
            # Wait a bit for any navigation
            self.page.wait_for_load_state("networkidle", timeout=5000)
            return f"[OK] Clicked element: {selector}\nCurrent URL: {self.page.url}"
        except Exception as e:
            return f"[ERROR] Click failed on {selector}: {e}"
    
    @xray
    def fill_form(self, form_data: str) -> str:
        """Fill form fields on the page.
        
        Args:
            form_data: JSON string with selector-value pairs, e.g., '{"#name": "John", "#email": "john@example.com"}'
        
        Returns:
            Success message or error message
        """
        if not PLAYWRIGHT_AVAILABLE:
            return "[ERROR] Playwright not installed. Run: pip install playwright && playwright install chromium"
        
        if not self.page:
            return "[ERROR] No page loaded. Navigate to a URL first."
        
        try:
            data = json.loads(form_data)
            filled = []
            
            for selector, value in data.items():
                self.page.fill(selector, str(value))
                filled.append(f"{selector} = {value}")
            
            return f"[OK] Form filled:\n" + "\n".join(filled)
        except json.JSONDecodeError:
            return "[ERROR] Invalid JSON format for form_data"
        except Exception as e:
            return f"[ERROR] Form filling failed: {e}"
    
    @xray
    def extract_links(self, filter_pattern: str = "") -> str:
        """Extract all links from the current page.
        
        Args:
            filter_pattern: Optional pattern to filter links
        
        Returns:
            List of links or error message
        """
        if not PLAYWRIGHT_AVAILABLE:
            return "[ERROR] Playwright not installed. Run: pip install playwright && playwright install chromium"
        
        if not self.page:
            return "[ERROR] No page loaded. Navigate to a URL first."
        
        try:
            links = self.page.eval_on_selector_all(
                'a[href]',
                'elements => elements.map(e => ({text: e.innerText, href: e.href}))'
            )
            
            if filter_pattern:
                links = [link for link in links if filter_pattern in link['href']]
            
            if not links:
                return "No links found" + (f" matching '{filter_pattern}'" if filter_pattern else "")
            
            result = f"[OK] Found {len(links)} links:\n"
            for link in links[:20]:  # Show first 20
                result += f"  - {link['text'][:50]}: {link['href']}\n"
            
            if len(links) > 20:
                result += f"  ... and {len(links) - 20} more"
            
            return result
        except Exception as e:
            return f"[ERROR] Link extraction failed: {e}"
    
    @xray
    def wait(self, seconds: float) -> str:
        """Wait for a specified number of seconds.
        
        Args:
            seconds: Number of seconds to wait
        
        Returns:
            Success message
        """
        if not PLAYWRIGHT_AVAILABLE:
            return "[ERROR] Playwright not installed. Run: pip install playwright && playwright install chromium"
        
        if not self.page:
            return "[ERROR] No page loaded. Navigate to a URL first."
        
        try:
            self.page.wait_for_timeout(int(seconds * 1000))  # Convert to milliseconds
            return f"[OK] Waited for {seconds} seconds"
        except Exception as e:
            return f"[ERROR] Wait failed: {e}"
    
    @xray
    def execute_javascript(self, script: str) -> str:
        """Execute JavaScript code on the page.
        
        Args:
            script: JavaScript code to execute
        
        Returns:
            Result of JavaScript execution or error message
        """
        if not PLAYWRIGHT_AVAILABLE:
            return "[ERROR] Playwright not installed. Run: pip install playwright && playwright install chromium"
        
        if not self.page:
            return "[ERROR] No page loaded. Navigate to a URL first."
        
        try:
            result = self.page.evaluate(script)
            return f"[OK] JavaScript executed. Result: {result}"
        except Exception as e:
            return f"[ERROR] JavaScript execution failed: {e}"
    
    @xray
    def close_browser(self) -> str:
        """Close the browser and clean up resources.
        
        Returns:
            Success message
        """
        try:
            if self.page:
                self.page.close()
                self.page = None
            if self.browser:
                self.browser.close()
                self.browser = None
            if self.playwright:
                self.playwright.stop()
                self.playwright = None
            
            return "[OK] Browser closed and resources cleaned up"
        except Exception as e:
            return f"[ERROR] Failed to close browser: {e}"
    
    def get_session_info(self) -> str:
        """Get information about the browser session.
        
        Returns:
            Session information as formatted string
        """
        info = {
            "browser_running": self.browser is not None,
            "current_url": self.page.url if self.page else None,
            "visited_urls": self.visited_urls,
            "screenshots_taken": len(self.screenshots),
            "screenshot_files": self.screenshots,
        }
        
        return f"[OK] Session info:\n" + json.dumps(info, indent=2)

