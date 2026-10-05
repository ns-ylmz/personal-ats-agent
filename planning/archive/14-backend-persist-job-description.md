# Task: Persist Scraped Job Description

## Objective
Ensure the raw scraped text from a job URL is saved back to the database, so it remains accessible even if the original job posting is taken down.

## Required Context
- `backend/app/worker.py`
- `backend/app/models.py`

## Affected Areas
- `backend/app/worker.py`

## Constraints
- Minimal changes: just assign the scraped text to `job.job_description` before `db.commit()`.
- Do not modify frontend or LLM prompt behavior in this task.

## Out of Scope
- Frontend UI modifications (will be handled in a separate task).
- Adding new database columns or migrating existing schema.

## Verification
- Submit a job with a valid URL. After completion, `GET /jobs/{id}` should return the actual text of the job description instead of the URL.

## Completion Criteria
- Worker correctly updates `job_description` with `job_desc_text`.
- The database correctly persists the large text blob.

## Agent Execution Prompt
Implement the backend persistence logic to store scraped text in the database.
