# Project Roadmap: AI Job Hunter & Personal ATS

This roadmap outlines the iterative development phases for the Personal ATS Agent, moving from a foundational MVP to a fully autonomous, RAG-enabled background processor.

## Phase 1: Core MVP (Text-in, JSON-out)
**Goal**: Establish the foundational async architecture and LLM integration.
- Set up FastAPI and SQLAlchemy with SQLite.
- Implement the background worker queue using Python's standard `threading` and `queue.Queue`.
- Integrate Google Gemini API (via `google-genai` SDK) utilizing the Strategy Pattern (`LLMProvider`).
- Create basic endpoints to submit raw CV text and raw Job Description text (no scraping or file parsing yet).
- Generate and store AI outputs (Match Score, Cover Letter, Interview Questions) as Structured JSON.

## Phase 2: User Onboarding & File Processing
**Goal**: Automate the creation of the "Master Profile" from a CV document. *(Supports User Scenario 1)*
- Integrate `PyPDF2` (or similar) for document parsing.
- Create the `/api/profile/upload` endpoint.
- Parse the uploaded PDF and use the LLM to extract a structured Master Profile (Skills, Experience, Education).
- Persist the Master Profile in the database to prevent redundant parsing during future job analyses.

## Phase 3: Minimal RAG & Interview Feedback Loop
**Goal**: Implement the continuous learning feedback loop. *(Supports User Scenarios 3 & 4)*
- Add the `interview_feedbacks` table and `recruitment_status` tracking.
- Create endpoints to update job status and submit post-interview feedback.
- Implement In-Context Learning (Minimal RAG): Fetch past interview weaknesses/notes from SQLite and inject them into the LLM prompt when preparing the user for new job interviews.

## Phase 4: Autonomous Scraping & Advanced AI
**Goal**: Achieve full autonomy with URLs and upgrade the AI architecture. *(Supports User Scenario 2)*
- Integrate `Playwright` to autonomously scrape Job Descriptions directly from LinkedIn/Glassdoor URLs, bypassing anti-bot measures.
- Implement batch processing to handle an array of URLs concurrently.
- Include support for local LLMs (`OllamaProvider`) for offline processing.
- *(Optional)* Migrate Minimal RAG to a local Vector Database (`ChromaDB`) for scalable semantic search over extensive interview history and CV chunks.

## Phase 5: Frontend Dashboard Integration
**Goal**: Build the interactive User Interface.
- Scaffold a Next.js App Router project with Tailwind CSS and `shadcn/ui`.
- Implement the Job Tracker Kanban Board (Analyzed, Applied, Interviewing).
- Implement the Job Detail View displaying the original listing alongside the AI-generated Cover Letter and Prep Studio.
