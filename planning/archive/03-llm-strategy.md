# Task: Implement LLM Provider Strategy

## Objective
Create the Strategy Pattern interface for LLMs and implement the `GeminiProvider`.

## Required Context
- .ai/guidelines/architecture.md
- docs/decisions/002-dual-llm-provider-strategy.md
- docs/05-environment-configuration.md

## Affected Areas
- `/backend/app/services/llm_provider.py`
- `/backend/app/services/gemini_provider.py`

## Constraints
- Must use `google-genai` SDK.
- Provider selection must be driven by `LLM_PROVIDER` env variable.
- Must use Structured JSON Output capabilities of Gemini.

## Out of Scope
- `OllamaProvider` implementation (deferred to later task).
- Web scraping.

## Verification
- Run a unit test that mocks the Gemini API and verifies the JSON output structure.

## Completion Criteria
- Abstract base class `LLMProvider` is defined with an `analyze_job` method.
- `GeminiProvider` implements this interface.
- Returns structured JSON containing Match Score, Cover Letter, and Prep Questions.

## Agent Execution Prompt
Execute this task emphasizing clean OOP principles. Ensure the output strictly enforces JSON schemas.
