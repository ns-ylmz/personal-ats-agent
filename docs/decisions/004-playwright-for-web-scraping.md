# 004: Playwright for Web Scraping

## Context
The system needs to extract job descriptions from URLs (LinkedIn, Glassdoor). These sites heavily use JavaScript rendering and basic anti-bot protections.

## Decision
We will use Playwright for web scraping instead of `requests` and `BeautifulSoup`.

## Consequences
- **Positive:** Can execute JavaScript and wait for dynamic content; significantly better at bypassing simple bot detections.
- **Negative:** Higher resource consumption (runs a headless browser); slower execution time per URL compared to raw HTTP requests.
