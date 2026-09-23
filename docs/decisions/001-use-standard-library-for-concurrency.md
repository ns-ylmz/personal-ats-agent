# 001: Use Python Standard Library for Background Concurrency

## Context
The application requires asynchronous processing to handle long-running LLM API calls and web scraping without blocking the FastAPI event loop. Traditional solutions involve external message brokers (Redis/RabbitMQ) and workers (Celery).

## Decision
We will use Python's built-in `threading` and `queue.Queue` to manage background tasks. 

## Consequences
- **Positive:** Zero external dependencies; easy local setup; perfect for learning core concurrency concepts.
- **Negative:** Not distributed; if the server crashes, in-memory queue jobs are lost. This is acceptable for a personal ATS.
