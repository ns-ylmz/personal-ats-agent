# Task: Implement LLM Fallback Mechanism

## Objective

Enhance the LLM service factory to support automatic fallback from cloud providers (Gemini/OpenAI) to a local provider (Ollama) upon failure.

## Required Context

- .ai/guidelines/workflow.md
- backend/app/services/__init__.py
- backend/app/worker.py

## Affected Areas

- `backend/app/services/__init__.py` (Implement fallback wrapper or logic)
- `backend/app/worker.py` (Update error handling)

## Constraints

- The fallback chain should gracefully catch `ValueError`, API limit errors, or connection errors from the primary provider.
- If the primary provider fails, it must automatically retry the same methods on the secondary provider.

## Out of Scope

- Modifying the internals of the specific providers (`gemini_provider.py`, `ollama_provider.py`).

## Verification

- Submit a job with an intentionally invalid `GEMINI_API_KEY`. Verify backend logs display the failure, but the job still completes via Ollama.

## Completion Criteria

- Fallback chain is successfully implemented and logs clear warnings when falling back.

## Agent Execution Prompt

Execute task `planning/active/21-llm-fallback.md`.
