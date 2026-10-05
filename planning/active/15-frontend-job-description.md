# Task: Improve Job Description Display on Frontend

## Objective
Ensure the potentially massive raw scraped job description text is displayed nicely in the UI without breaking the layout.

## Required Context
- `frontend/src/app/jobs/[id]/page.tsx`

## Affected Areas
- `frontend/src/app/jobs/[id]/page.tsx`

## Constraints
- Minimal changes: just improve the visual presentation (e.g. adding a collapsible container or maintaining whitespace format).

## Out of Scope
- Backend logic modifications.
- LLM response changes.

## Verification
- Navigate to an analyzed job with a long description and verify the UI remains clean and readable.

## Completion Criteria
- Job Description section correctly handles long strings of raw text.

## Agent Execution Prompt
Implement the frontend UI enhancements to cleanly render large raw job description texts.
