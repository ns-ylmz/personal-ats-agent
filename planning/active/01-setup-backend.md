# Task: Setup FastAPI and SQLite

## Objective
Initialize the Python backend workspace with FastAPI and SQLAlchemy connected to a local SQLite database.

## Required Context
- .ai/guidelines/workflow.md
- docs/01-architecture-overview.md
- docs/04-tooling-conventions.md

## Affected Areas
- `/backend/app/main.py`
- `/backend/app/database.py`
- `/backend/app/models.py`
- `/backend/requirements.txt`

## Constraints
- Use Python 3.12+ features.
- Database must be strictly SQLite.
- Do not add external databases like PostgreSQL.

## Out of Scope
- LLM integration.
- Background worker threads.
- Authentication.

## Verification
- Run `cd backend && uvicorn app.main:app --reload`.
- Ensure `/docs` loads successfully.
- Verify `app.db` file is created.

## Completion Criteria
- FastAPI application starts without errors.
- SQLAlchemy engine and declarative base are configured.
- A dummy `/health` endpoint returns `{"status": "ok"}`.

## Agent Execution Prompt
Execute this task by following the `docs/04-tooling-conventions.md` for Python. Ensure all constraints and verification steps pass.
