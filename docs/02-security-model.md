# Security Model

## Authentication & Authorization
As a "Personal ATS", this system is designed for single-user local deployment.
-   **V1-V4**: No authentication required for local `localhost` usage. 
-   **V5 (Future Cloud Deployment)**: If deployed to the web, a simple Bearer Token or HTTP Basic Auth mechanism will be implemented to protect personal CV data.

## Secrets & Configuration
-   **LLM API Keys**: Credentials like `GEMINI_API_KEY` are strictly confidential. They must reside in a `.env` file at the root of the `/backend` workspace.
-   **Git Guardrails**: The project's `.ai/hooks/guard-git.sh` must remain active to prevent accidental commits of `.env` files or SQLite databases (`app.db`).
