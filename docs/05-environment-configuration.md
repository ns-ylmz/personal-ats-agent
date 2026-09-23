# Environment Configuration

## Environment Variables
The application relies on a `.env` file for runtime configuration. There should be a `.env.example` committed to the repository outlining required variables.

### Required Variables
-   `LLM_PROVIDER`: Defines the active AI strategy (`GEMINI` or `OLLAMA`). Default: `GEMINI`.
-   `GEMINI_API_KEY`: Required if provider is GEMINI.
-   `DATABASE_URL`: SQLAlchemy connection string. Default: `sqlite:///./app.db`.

## Per-Environment Behavior
-   **Development**: SQLite database resides locally. FastAPI runs with `--reload`.
-   **Production**: Ensure `CORS_ORIGINS` are tightly restricted. Ensure LLM_PROVIDER rate limits are respected if processing large batches.
