# Task: Frontend Kanban Dashboard

## Objective
Build the Dashboard UI to track job statuses.

## Required Context
- docs/08-frontend-ui.md (Dashboard wireframe)

## Affected Areas
- `/frontend/app/page.tsx`
- `/frontend/components/`

## Constraints
- Fetch data from the FastAPI backend.
- UI must match the Applicant B2C focus (no B2B employer elements).

## Verification
- Render the page and ensure columns (Analyzed, Applied, Interviewing) map to job statuses.

## Completion Criteria
- Dashboard displays a URL input bar.
- Kanban board renders cards based on backend DB state.

## Agent Execution Prompt
Implement the Dashboard UI using shadcn components and integrate it with the backend API.
