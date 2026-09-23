# 002: Dual LLM Provider Strategy

## Context
We need to generate cover letters and score CVs using an LLM. Vendor lock-in is a risk, and we want to allow for offline/local processing if desired.

## Decision
We will use the Strategy Pattern to abstract LLM interactions behind an `LLMProvider` interface. The initial implementations will be `GeminiProvider` (using Google AI Studio free tier) and `OllamaProvider` (for local, open-source models).

## Consequences
- **Positive:** High flexibility; future-proof; demonstrates solid OOP principles.
- **Negative:** Slight overhead in prompt management to ensure compatibility across different models.
