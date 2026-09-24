# Task: Integrate Playwright Scraper

## Objective
Autonomously extract Job Description text from LinkedIn/Glassdoor URLs using Playwright.

## Required Context
- docs/decisions/004-playwright-for-web-scraping.md

## Affected Areas
- `/backend/app/services/scraper.py`
- `/backend/app/worker.py` (Replace raw text with scraped text)

## Constraints
- Use Playwright in headless mode.
- Must not block the FastAPI event loop.

## Out of Scope
- Handling captchas.

## Verification
- Write a script to scrape a public test URL and verify text extraction.

## Completion Criteria
- Given a URL, `scraper.py` returns the readable page text.
- Worker uses this scraper if a URL is provided instead of raw text.

## Agent Execution Prompt
Implement the web scraper service using Playwright and wire it into the worker thread.
