# Testing Foundation

## Test Layers
1.  **Unit Tests (Backend)**: Located in `/backend/tests/unit/`.
    -   Focus: Testing LLM prompt generation logic, text chunking algorithms, and URL validation.
    -   Tooling: `pytest` with `unittest.mock` to mock LLM network calls.
2.  **Integration Tests (Backend)**: Located in `/backend/tests/integration/`.
    -   Focus: Verifying FastAPI endpoints, database CRUD operations, and worker queue processing using a test SQLite database.
    -   Tooling: `pytest`, `httpx` (FastAPI TestClient).

## Verification Commands
-   Backend Verification: `cd backend && pytest`
-   FastAPI Startup Check: `cd backend && uvicorn app.main:app --reload`
