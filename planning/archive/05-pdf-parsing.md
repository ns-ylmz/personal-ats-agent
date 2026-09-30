# Task: Implement PDF Parsing for Master Profile

## Objective
Extract a structured "Master Profile" (skills, experience) from an uploaded CV (PDF) using PyPDF2 and LLM.

## Required Context
- .ai/guidelines/workflow.md
- docs/01-architecture-overview.md
- ROADMAP.md (Phase 2)

## Affected Areas
- `/backend/app/services/pdf_service.py`
- `/backend/app/services/llm_provider.py` (add profile extraction prompt)

## Constraints
- Use `PyPDF2` (or `pdfplumber`).
- Result must be a structured JSON (Master Profile).

## Out of Scope
- Frontend upload UI.
- Database persistence (handled in next task).

## Verification
- Write a unit test providing a dummy PDF, mocking the LLM, and ensuring JSON structure is returned.

## Completion Criteria
- Service can extract text from a PDF.
- LLMProvider has a method `extract_master_profile` that returns structured data.

## Agent Execution Prompt
Implement the PDF parsing and LLM extraction logic as a pure service layer function.
