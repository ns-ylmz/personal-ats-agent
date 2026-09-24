# Task: Implement Core Job Endpoints

## Objective
Create the FastAPI REST endpoints to submit a job application and retrieve its status.

## Required Context
- .ai/guidelines/architecture.md
- docs/01-architecture-overview.md

## Affected Areas
- `/backend/app/api/jobs.py`
- `/backend/app/schemas.py`
- `/backend/app/main.py` (router inclusion)

## Constraints
- Endpoints must be asynchronous (`async def`).
- Follow RESTful principles (`POST /jobs`, `GET /jobs/{id}`).

## Out of Scope
- Frontend UI.
- Real URL scraping (accept raw text for now).

## Verification
- Submit a mock POST request via Swagger UI.
- Verify it returns `202 Accepted` and enqueues the job.
- Verify GET request returns the generated LLM data once the worker completes.

## Completion Criteria
- `POST /jobs/analyze` accepts raw CV text and Job text, enqueues the task.
- `GET /jobs/{id}` retrieves the job status and final JSON result from SQLite.

## Agent Execution Prompt
Implement the endpoints tying together the Database, Worker, and LLMProvider layers.
