# Task: Interview Feedback Database Schema

## Objective
Add database tables and endpoints to record interview feedback and status updates.

## Required Context
- docs/01-architecture-overview.md
- ROADMAP.md (Phase 3)

## Affected Areas
- `/backend/app/models.py` (Add InterviewFeedback)
- `/backend/app/api/jobs.py` (Add status update & feedback endpoints)

## Constraints
- Feedback must relate to a specific Job Application via Foreign Key.

## Out of Scope
- Actually utilizing the feedback in prompts (RAG).

## Verification
- Run a test to create a Job, then attach a Feedback record to it.

## Completion Criteria
- `POST /api/jobs/{id}/feedback` endpoint exists.
- `PATCH /api/jobs/{id}/status` endpoint exists.

## Agent Execution Prompt
Implement the CRUD operations for Interview Feedback in SQLAlchemy and FastAPI.
