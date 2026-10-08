# Task: Implement job deletion functionality

## Objective

Allow users to permanently delete failed or unwanted job analyses from both the database and the UI.

## Required Context

- .ai/guidelines/workflow.md
- backend/app/api/jobs.py
- frontend/src/app/page.tsx

## Affected Areas

- `backend/app/api/jobs.py` (Add `DELETE /jobs/{id}` endpoint)
- `frontend/src/app/page.tsx` (Add delete button to Kanban cards)
- `frontend/src/app/jobs/[id]/page.tsx` (Add delete button to detail view)

## Constraints

- Ensure the delete operation cleanly cascades or removes associated DB rows if any relations exist.
- Do not introduce complex state management; simply refetch or filter the local state on successful deletion.

## Out of Scope

- Archiving features or soft-deletes (hard delete is preferred based on user constraints).
- Bulk deletion mechanisms.

## Verification

- Submit a deletion request and verify the row disappears from SQLite.
- Ensure the UI updates immediately and the job is no longer listed.

## Completion Criteria

- `DELETE /jobs/{id}` endpoint is functional and returns 204.
- Trash icon/button is present on the frontend.
- Clicking the trash button permanently removes the job.

## Agent Execution Prompt

Execute task `planning/active/17-delete-job.md`.
