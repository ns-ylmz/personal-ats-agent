# Task: Implement Ollama Provider

## Objective
Add local LLM support via Ollama.

## Required Context
- docs/decisions/002-dual-llm-provider-strategy.md
- docs/05-environment-configuration.md

## Affected Areas
- `/backend/app/services/ollama_provider.py`
- `/backend/app/services/llm_provider.py` (Factory logic)

## Constraints
- Must use Ollama REST API or Python client.
- Must enforce the same Structured JSON Output as Gemini.

## Verification
- Set `LLM_PROVIDER=OLLAMA` and verify the worker routes the request to Ollama.

## Completion Criteria
- `OllamaProvider` class successfully generates Cover Letters and Prep Questions.

## Agent Execution Prompt
Implement the local LLM Strategy using Ollama, ensuring JSON schema compliance.
