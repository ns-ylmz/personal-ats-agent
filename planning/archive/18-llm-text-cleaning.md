# Task: Implement LLM-based pre-cleaning for scraped job descriptions

## Objective

Extract only the relevant parts (Job Definition, Requirements, Qualifications, Cultural Fit) from the raw HTML text using an LLM step before saving to the database.

## Required Context

- .ai/guidelines/workflow.md
- backend/app/services/llm_provider.py
- backend/app/worker.py

## Affected Areas

- `backend/app/services/llm_provider.py` (Add abstract `clean_raw_job_text` method)
- `backend/app/services/gemini_provider.py` (Implement extraction prompt)
- `backend/app/services/ollama_provider.py` (Implement extraction prompt)
- `backend/app/worker.py` (Call the cleaning step right after Playwright scraping and before DB commit)

## Constraints

- The cleaning prompt must explicitly instruct the model to discard "similar jobs", "footers", "cookie policies", etc.
- Must support both Gemini and Ollama providers dynamically.
- Keep the prompt concise to save tokens and time.

## Out of Scope

- RegEx or heuristic-based text cleaning (we agreed on Option A: AI-based).
- Altering the existing Match Score analysis logic.

## Verification

- Start a job analysis. Check SQLite database (`app.db`) to ensure `job_description` contains only a well-formatted summary, not raw footer text.

## Completion Criteria

- `clean_raw_job_text` method is implemented across providers.
- Worker updates `job.job_description` with the cleaned text before moving to the `analyze_job` phase.

## Agent Execution Prompt

Execute task `planning/active/18-llm-text-cleaning.md`.
