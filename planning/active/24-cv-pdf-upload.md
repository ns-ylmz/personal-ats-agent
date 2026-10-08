# Task: Profile Management & PDF CV Upload

## Objective

Allow the user to upload their CV in PDF format, extract its raw text, use the LLM to generate a `MasterProfile` (skills and experience summary), and use this real CV data for all future job analyses instead of hardcoded text.

## Required Context

- .ai/guidelines/workflow.md
- backend/app/models.py
- backend/app/api/jobs.py
- frontend/src/app/page.tsx

## Affected Areas

- `backend/app/models.py` (Create `UserProfile` table to store `raw_cv_text`, `skills`, and `experience_summary`)
- `backend/app/api/profile.py` (New router for `POST /profile/upload` and `GET /profile`)
- `backend/app/main.py` (Include the new profile router)
- `backend/requirements.txt` (Add a PDF parsing library like `PyPDF2` or `pdfplumber` and `python-multipart` for file uploads)
- `backend/app/worker.py` (Query `UserProfile` to fetch the real `cv_text` for LLM analysis instead of trusting the frontend payload)
- `frontend/src/app/page.tsx` (Remove hardcoded `cv_text` from the analyze payload. Add a minimal "Upload CV" button or redirect to a profile page)
- `frontend/src/app/profile/page.tsx` (New page: Upload PDF, display extracted skills/experience)

## Constraints

- Only `.pdf` files need to be supported initially.
- The `UserProfile` should act as a singleton (e.g., just updating the row with `id=1` or taking the latest created row) to keep things simple for a personal ATS.
- The extraction of `MasterProfile` from the raw text must use the existing `provider.extract_master_profile()` method.

## Out of Scope

- Handling DOCX or other complex file formats.
- Multiple separate user accounts (it is a personal, single-user system).

## Verification

- Upload a real CV PDF via the frontend.
- Verify the backend successfully extracts text and LLM generates a valid `MasterProfile` JSON.
- Submit a new Job Analysis.
- Check the database/logs to confirm the LLM used the newly uploaded CV text instead of "Default Profile CV used."

## Completion Criteria

- `UserProfile` database model is created.
- PDF extraction works.
- Frontend allows file selection and upload.
- Job analysis dynamically uses the real CV text.

## Agent Execution Prompt

Execute task `planning/active/24-cv-pdf-upload.md`.
