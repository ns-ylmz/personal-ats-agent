# Task: Master Profile DB and Endpoints

## Objective
Store the extracted Master Profile in SQLite and expose an upload endpoint.

## Required Context
- .ai/guidelines/architecture.md
- docs/01-architecture-overview.md

## Affected Areas
- `/backend/app/models.py` (Add UserProfile)
- `/backend/app/api/profile.py`
- `/backend/app/main.py`

## Constraints
- Store skills and experience as JSON strings or related tables in SQLite.

## Out of Scope
- Multiple users (assume single user environment).

## Verification
- Use Swagger UI to upload a sample PDF and verify it returns 200 OK.
- Check SQLite database to ensure the Master Profile row is created.

## Completion Criteria
- `POST /api/profile/upload` endpoint exists and accepts `UploadFile`.
- Endpoint uses `pdf_service` and saves results to DB.

## Agent Execution Prompt
Tie the PDF parsing service to the FastAPI endpoint and SQLAlchemy models.
