# Task: Implement Server-Sent Events (SSE) for background job updates

## Objective

Notify the Next.js frontend in real-time when the background worker completes an analysis, removing the need for manual browser refreshes.

## Required Context

- .ai/guidelines/workflow.md
- backend/app/api/jobs.py
- frontend/src/app/page.tsx

## Affected Areas

- `backend/app/api/jobs.py` (Add `/jobs/events` or `/jobs/{id}/events` SSE endpoint using `StreamingResponse`)
- `backend/app/worker.py` (Push an event to an async queue or broadcast mechanism when job status changes)
- `frontend/src/app/page.tsx` (Use `EventSource` or custom hook to listen for status changes and auto-refresh the board)
- `frontend/src/app/jobs/[id]/page.tsx` (Auto-refresh detail page if user is waiting there)

## Constraints

- Use Server-Sent Events (SSE), do NOT use WebSockets.
- Must handle connection drops gracefully.
- Keep the notification payload small (e.g., just `{ "job_id": 1, "status": "COMPLETED" }`).

## Out of Scope

- Setting up Redis or RabbitMQ for pub/sub (use a simple in-memory `asyncio.Queue` or list of queues for a single-instance FastAPI).

## Verification

- Start a job analysis.
- Do NOT touch the keyboard or refresh the browser.
- Ensure the UI automatically updates to COMPLETED when the backend finishes.

## Completion Criteria

- SSE endpoint is functional.
- Frontend establishes `EventSource` connection on mount.
- Status updates propagate to the UI without manual intervention.

## Agent Execution Prompt

Execute task `planning/active/19-sse-notifications.md`.
