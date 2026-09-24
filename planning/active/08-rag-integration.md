# Task: Minimal RAG Integration

## Objective
Inject past interview weaknesses and feedback into the LLM prompt during new job analysis.

## Required Context
- docs/decisions/005-minimal-rag-for-feedback-loop.md

## Affected Areas
- `/backend/app/worker.py` (Fetch past feedbacks before LLM call)
- `/backend/app/services/llm_provider.py` (Update prompts to accept context)

## Constraints
- Do NOT use a Vector Database (ChromaDB). Just concatenate text from SQLite.

## Out of Scope
- Vector embeddings.

## Verification
- Provide mock feedback in DB and verify the prompt sent to the LLM includes it via logs or mock tests.

## Completion Criteria
- Worker fetches all past feedback from SQLite.
- `analyze_job` uses this context to generate better Prep Questions.

## Agent Execution Prompt
Update the worker and LLM prompt to enable In-Context Learning (Minimal RAG).
