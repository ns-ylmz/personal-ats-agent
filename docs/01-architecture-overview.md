# Architecture Overview

## System Shape
The Personal ATS Agent is composed of two primary deployment units:
1.  **Backend API & Worker**: A monolithic Python service powered by FastAPI. It contains an asynchronous API layer and an embedded background worker thread pool (`queue.Queue`) for long-running LLM and scraping tasks.
2.  **Frontend Dashboard**: A Next.js (App Router) web application utilizing Tailwind CSS and `shadcn/ui` components for the user interface.

## Workspaces & Ownership
-   `/backend`: Owns data persistence (SQLite), business logic, web scraping, and LLM orchestration.
-   `/frontend`: Owns the UI, state management, and user interaction (Kanban boards, profile upload).

## High-Level Data Flow
**Core Job Analysis Flow:**
1.  **Frontend**: User pastes a Job URL and clicks "Analyze". Request sent to `/api/jobs/analyze`.
2.  **FastAPI (Transport)**: Validates request, creates a "PENDING" job in SQLite, and places the `job_id` into the in-memory `queue.Queue`. Instantly returns `202 Accepted` to the client.
3.  **Worker Thread (Orchestration)**:
    -   Pulls `job_id` from the queue.
    -   Calls `Playwright` to scrape the job description.
    -   Retrieves User's "Master Profile" and past "Interview Feedbacks" from SQLite.
    -   Calls the `LLMProvider` (Strategy: Gemini or Ollama) with the combined context.
4.  **Database (Persistence)**: Saves the generated Cover Letter, Match Score, and Prep Questions to SQLite and marks job as "COMPLETED".
5.  **Frontend**: Polls or fetches the completed data and displays it on the Dashboard.

## Runtime Contracts
-   The Frontend and Backend communicate strictly via REST JSON over HTTP.
-   The database schema is managed via SQLAlchemy ORM models.
-   LLM interactions are abstracted behind the `LLMProvider` interface to prevent vendor lock-in.
