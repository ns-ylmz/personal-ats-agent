# Task: Implement OpenAI Provider

## Objective

Introduce a new `OpenAIProvider` to allow the system to use OpenAI models (like `gpt-4o-mini` or `gpt-4o`) for job analysis and profile extraction.

## Required Context

- .ai/guidelines/workflow.md
- backend/app/services/llm_provider.py

## Affected Areas

- `backend/app/services/openai_provider.py` (New file)
- `backend/app/services/__init__.py` (Add OpenAI logic to provider factory)
- `backend/requirements.txt` (Add `openai` SDK)
- `backend/.env.example` (Add `OPENAI_API_KEY`)

## Constraints

- `OpenAIProvider` must strictly inherit from `LLMProvider`.
- Must use OpenAI's native Structured Outputs (`response_format` / `beta.parse`) to guarantee exact Pydantic schema matches.

## Out of Scope

- Fallback logic (to be handled in a separate task).
- Refactoring existing prompts (to be handled in a separate task).

## Verification

- Set `LLM_PROVIDER=OPENAI` and `OPENAI_API_KEY`, submit a job via UI, and ensure a completed state with proper JSON structure.

## Completion Criteria

- `OpenAIProvider` is successfully wired into the factory and passes end-to-end tests.

## Agent Execution Prompt

Execute task `planning/active/20-openai-provider.md`.
