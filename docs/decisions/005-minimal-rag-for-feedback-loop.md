# 005: Minimal RAG (In-Context Learning)

## Context
We want the AI to learn from past interview experiences (e.g., weaknesses, asked questions) to better prepare the user for future interviews (RAG).

## Decision
Instead of deploying a dedicated Vector Database (like ChromaDB), we will use "Minimal RAG". We will query past feedback directly from SQLite and inject it as plain text into the LLM prompt.

## Consequences
- **Positive:** Eliminates the complexity of maintaining a vector database; utilizes the large context windows of modern LLMs (like Gemini 1.5).
- **Negative:** Not scalable for thousands of documents, though highly sufficient for a single user's interview history.
