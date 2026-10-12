# Task: Refactor and DRY LLM Prompts

## Objective

Extract duplicated prompt strings across different LLM providers into a central, shared constants module to prevent duplication and ensure consistency.

## Required Context

- .ai/guidelines/workflow.md
- backend/app/services/gemini_provider.py
- backend/app/services/ollama_provider.py
- backend/app/services/openai_provider.py (if exists)

## Affected Areas

- `backend/app/services/prompts.py` (New file for shared strings)
- `backend/app/services/gemini_provider.py`
- `backend/app/services/ollama_provider.py`
- `backend/app/services/openai_provider.py` (if exists)

## Constraints

- Use Python string formatting (e.g., `f-strings` or `.format()`) securely in the shared constants.
- The refactor must be strictly behavioral-preserving (no logic changes).

## Out of Scope

- Changing the context or behavior of the LLMs.
- Introducing new LLM providers.

## Verification

- Submit a job and ensure the output quality and format remain exactly the same as before.

## Completion Criteria

- `clean_raw_job_text`, `analyze_job`, and `extract_master_profile` prompts are imported from a single source of truth.

## Agent Execution Prompt

Execute task `planning/active/22-refactor-prompts.md`.
