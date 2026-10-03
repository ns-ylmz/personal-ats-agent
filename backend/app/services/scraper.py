from playwright.sync_api import sync_playwright
import logging

logger = logging.getLogger(__name__)

def scrape_job_description(url: str) -> str:
    """
    Scrapes a webpage to extract readable text content.
    Useful for extracting job descriptions from URLs.
    """
    logger.info(f"Scraping URL: {url}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            # Set a normal user agent to avoid basic blocks
            page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            })
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            # Basic attempt to get readable text
            text_content = page.evaluate("document.body.innerText")
            return text_content.strip()
        except Exception as e:
            logger.error(f"Failed to scrape {url}: {e}")
            raise ValueError(f"Could not extract text from {url}: {e}")
        finally:
            browser.close()
