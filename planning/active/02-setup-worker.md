# Task: Implement Background Worker Queue

## Objective
Set up an embedded background worker using Python `threading` and `queue.Queue` to process async jobs.

## Required Context
- .ai/guidelines/workflow.md
- docs/01-architecture-overview.md
- docs/decisions/001-use-standard-library-for-concurrency.md

## Affected Areas
- `/backend/app/worker.py`
- `/backend/app/main.py` (to start/stop the worker on startup/shutdown events)

## Constraints
- Do NOT use Celery, Redis, or RabbitMQ.
- Must use standard library `threading` and `queue`.

## Out of Scope
- Actual scraping or LLM calls.
- Frontend implementation.

## Verification
- Add a dummy task to the queue from a test endpoint.
- Verify the worker thread processes it and prints a success log.

## Completion Criteria
- FastAPI startup event correctly spawns the worker daemon thread.
- Worker correctly listens to `queue.Queue` and processes jobs.

## Agent Execution Prompt
Execute this task by following the constraints. Ensure the worker starts automatically when FastAPI boots.
