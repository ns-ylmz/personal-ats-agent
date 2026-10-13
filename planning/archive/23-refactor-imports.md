# Task: Refactor Backend Imports and Resolve Circular Dependencies

## Objective

Eliminate inline (dynamic) imports from backend functions by restructuring the architecture to cleanly resolve circular dependencies. Standardize all file imports using a strict PEP-8 compliant format.

## Required Context

- .ai/guidelines/workflow.md
- backend/app/worker.py
- backend/app/api/jobs.py

## Affected Areas

- `backend/app/queue_manager.py` (New file to isolate the `job_queue` state)
- All Python files under `backend/app/` (Refactor imports to top of file and sort them)

## Constraints

- Isolate the `job_queue` variable from `worker.py` into a standalone module (e.g., `queue_manager.py`) so both `jobs.py` and `worker.py` can import it safely.
- No inline/dynamic imports are allowed within function scopes.
- Imports must be at the very top of each file, grouped sequentially:
  1. Standard Library Imports (e.g., `import os`, `import json`)
  2. Third-Party Imports (e.g., `from fastapi`, `import sqlalchemy`)
  3. Internal App Imports (e.g., `from app import models`)
- Within each group, imports must be sorted alphabetically.
- Execution of functions/logic must be strictly below all import blocks.

## Out of Scope

- Refactoring actual business logic or adding new LLM functionalities (handled in separate tasks).

## Verification

- Start the FastAPI server (`uvicorn app.main:app`) and trigger a job analysis.
- Ensure no circular import crashes occur during boot or runtime.
- Verify every backend `.py` file adheres strictly to the grouping and sorting constraint.

## Completion Criteria

- `worker.py` and other modules are completely free of inline imports.
- Global queue state is cleanly isolated.
- The entire backend is consistently sorted and strictly follows the import convention.

## Agent Execution Prompt

Execute task `planning/active/23-refactor-imports.md`.
