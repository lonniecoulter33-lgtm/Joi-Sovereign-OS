"""
Browser Automation -- Selenium web control

REQUIRES: pip install selenium webdriver-manager
"""
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    HAVE_SELENIUM = True
except ImportError:
    HAVE_SELENIUM = False
    print("  WARNING: Selenium not installed. Run: pip install selenium webdriver-manager")

import time

# Global browser instance (persistent across calls)
_browser = None

def _get_browser():
    global _browser
    if _browser is None:
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # Comment out next line if you want to SEE the browser window
        # options.add_argument('--headless')
        service = Service(ChromeDriverManager().install())
        _browser = webdriver.Chrome(service=service, options=options)
    return _browser

def open_url(url: str):
    if not HAVE_SELENIUM:
        return {"ok": False, "error": "Selenium not installed"}
    try:
        browser = _get_browser()
        browser.get(url)
        time.sleep(2)
        return {"ok": True, "message": f"Opened {url}", "title": browser.title}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def click_element(selector: str, by_type: str = "css"):
    if not HAVE_SELENIUM:
        return {"ok": False, "error": "Selenium not installed"}
    try:
        browser = _get_browser()
        by_map = {"css": By.CSS_SELECTOR, "xpath": By.XPATH, "id": By.ID}
        by_val = by_map.get(by_type, By.CSS_SELECTOR)
        elem = browser.find_element(by_val, selector)
        elem.click()
        time.sleep(1)
        return {"ok": True, "message": f"Clicked element: {selector}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def fill_input(selector: str, text: str, by_type: str = "css"):
    if not HAVE_SELENIUM:
        return {"ok": False, "error": "Selenium not installed"}
    try:
        browser = _get_browser()
        by_map = {"css": By.CSS_SELECTOR, "xpath": By.XPATH, "id": By.ID}
        by_val = by_map.get(by_type, By.CSS_SELECTOR)
        elem = browser.find_element(by_val, selector)
        elem.clear()
        elem.send_keys(text)
        return {"ok": True, "message": f"Filled '{selector}' with '{text[:50]}'"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def extract_text(selector: str, by_type: str = "css"):
    if not HAVE_SELENIUM:
        return {"ok": False, "error": "Selenium not installed"}
    try:
        browser = _get_browser()
        by_map = {"css": By.CSS_SELECTOR, "xpath": By.XPATH, "id": By.ID}
        by_val = by_map.get(by_type, By.CSS_SELECTOR)
        elem = browser.find_element(by_val, selector)
        return {"ok": True, "text": elem.text}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def take_screenshot():
    if not HAVE_SELENIUM:
        return {"ok": False, "error": "Selenium not installed"}
    try:
        browser = _get_browser()
        png = browser.get_screenshot_as_png()
        import base64
        b64 = base64.b64encode(png).decode('utf-8')
        return {"ok": True, "message": "Screenshot taken", "data": f"data:image/png;base64,{b64}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def execute_js(script: str):
    if not HAVE_SELENIUM:
        return {"ok": False, "error": "Selenium not installed"}
    try:
        browser = _get_browser()
        result = browser.execute_script(script)
        return {"ok": True, "result": result}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def wait_for_element(selector: str, timeout: int = 10, by_type: str = "css"):
    if not HAVE_SELENIUM:
        return {"ok": False, "error": "Selenium not installed"}
    try:
        browser = _get_browser()
        by_map = {"css": By.CSS_SELECTOR, "xpath": By.XPATH, "id": By.ID}
        by_val = by_map.get(by_type, By.CSS_SELECTOR)
        WebDriverWait(browser, timeout).until(EC.presence_of_element_located((by_val, selector)))
        return {"ok": True, "message": f"Element '{selector}' appeared"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

# Register tools
import joi_companion

if HAVE_SELENIUM:
    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "open_url",
            "description": "Open a URL in the browser (websites, YouTube, any link). Use when the user asks to open a site, open YouTube, open a video, open a webpage, or go to a URL. Required for 'open youtube', 'play a video on youtube', 'open this site'.",
            "parameters": {"type": "object", "properties": {
                "url": {"type": "string", "description": "Full URL to open (e.g. https://youtube.com, https://www.youtube.com/watch?v=...)"}
            }, "required": ["url"]}
        }},
        open_url
    )
    
    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "click_element",
            "description": "Click a page element by CSS selector, XPath, or ID",
            "parameters": {"type": "object", "properties": {
                "selector": {"type": "string"},
                "by_type": {"type": "string", "enum": ["css", "xpath", "id"], "default": "css"}
            }, "required": ["selector"]}
        }},
        click_element
    )
    
    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "fill_input",
            "description": "Fill a form input field",
            "parameters": {"type": "object", "properties": {
                "selector": {"type": "string"},
                "text": {"type": "string"},
                "by_type": {"type": "string", "enum": ["css", "xpath", "id"], "default": "css"}
            }, "required": ["selector", "text"]}
        }},
        fill_input
    )
    
    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "extract_text",
            "description": "Extract text from a page element",
            "parameters": {"type": "object", "properties": {
                "selector": {"type": "string"},
                "by_type": {"type": "string", "enum": ["css", "xpath", "id"], "default": "css"}
            }, "required": ["selector"]}
        }},
        extract_text
    )
    
    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "browser_screenshot",
            "description": "Take a screenshot of the current browser page",
            "parameters": {"type": "object", "properties": {}}
        }},
        take_screenshot
    )
    
    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "execute_js",
            "description": "Execute JavaScript in the browser",
            "parameters": {"type": "object", "properties": {
                "script": {"type": "string"}
            }, "required": ["script"]}
        }},
        execute_js
    )
    
    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "wait_for_element",
            "description": "Wait for an element to appear on page",
            "parameters": {"type": "object", "properties": {
                "selector": {"type": "string"},
                "timeout": {"type": "integer", "default": 10},
                "by_type": {"type": "string", "enum": ["css", "xpath", "id"], "default": "css"}
            }, "required": ["selector"]}
        }},
        wait_for_element
    )
