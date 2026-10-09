# Task: Wire Profile Management & PDF CV Upload Frontend

## Objective

Leverage the existing backend profile endpoints (`api/profile.py`) to allow the user to upload their CV in PDF format via a new frontend UI, and wire `worker.py` to use the extracted CV context for all future job analyses instead of a hardcoded payload.

## Required Context

- .ai/guidelines/workflow.md
- backend/app/models.py
- backend/app/api/profile.py
- backend/app/worker.py
- frontend/src/app/page.tsx

## Affected Areas

- `backend/app/models.py` (Add `raw_cv_text` column to existing `UserProfile` table)
- `backend/app/api/profile.py` (Save the extracted raw text into the new `raw_cv_text` column)
- `backend/app/worker.py` (Query `UserProfile.raw_cv_text` to fetch the real CV context for LLM analysis, ignoring the frontend payload)
- `backend/app/schemas.py` (Make `cv_text` optional in `JobAnalyzeRequest`)
- `frontend/src/app/page.tsx` (Remove hardcoded `cv_text` from the analyze payload. Add a "My Profile" button in the header)
- `frontend/src/app/profile/page.tsx` (New page: UI to upload PDF and display the extracted `skills` and `experience_summary`)

## Constraints

- The backend already has `api/profile.py` and `pdf_service.py` implemented. Do not duplicate logic, just extend `UserProfile` to save the raw text.
- The `UserProfile` acts as a singleton.
- The frontend profile page should display the currently saved profile if it exists.

## Out of Scope

- Handling DOCX or other complex file formats.

## Verification

- Upload a real CV PDF via the frontend `/profile` page.
- Submit a new Job Analysis.
- Check the database/logs to confirm the LLM used the newly uploaded CV text instead of "Default Profile CV used."

## Completion Criteria

- `UserProfile` correctly stores `raw_cv_text`.
- Frontend `/profile` page allows file upload and displays the current profile.
- Job analysis dynamically uses the real CV text from the DB.

## Agent Execution Prompt

Execute task `planning/active/24-cv-pdf-upload.md`.
