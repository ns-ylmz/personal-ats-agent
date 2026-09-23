# Personal ATS Agent

Your personal AI Applicant Tracking System. An autonomous AI agent built with FastAPI and Next.js that analyzes job descriptions, scores CV matches, and generates personalized cover letters & interview prep using LLMs.

## Overview

This project is an AI-powered pipeline designed to automate the tedious parts of job hunting:
- **CV Parsing**: Automatically extracts your "Master Profile" from a PDF CV.
- **Job Analysis**: Scrapes job descriptions directly from URLs (e.g., LinkedIn, Glassdoor).
- **Match Scoring**: Evaluates how well your profile fits the target role.
- **Preparation Studio**: Generates custom Cover Letters, CV tweak suggestions, and mock interview questions.
- **Continuous Learning (RAG)**: Learns from your post-interview feedback to better prepare you for future applications.

For a detailed breakdown of the development phases, see [ROADMAP.md](ROADMAP.md).

## Architecture & Tech Stack

- **Backend**: Python 3.12+ (FastAPI, SQLAlchemy, SQLite, `threading` for background queues, `playwright` for scraping)
- **Frontend**: Node.js (Next.js App Router, Tailwind CSS, shadcn/ui)
- **AI Integration**: Dual Provider Strategy (Google Gemini API for cloud, Ollama for local offline execution).

See `docs/01-architecture-overview.md` for a deeper dive into the system shape and data flow.

## AI Engineering Workflow

This repository utilizes a strict Agentic Workflow to maintain architectural coherence and deterministic task execution. If you are an AI assistant (like Claude Code, Antigravity, or Cursor) collaborating on this codebase, **you must read `AGENTS.md` and `.ai/README.md` before making changes.**

### Workspace Structure
- `docs/`: Architecture reasoning, ADRs (`docs/decisions/`), and high-level structural documentation.
- `planning/`: Bounded task plans and their lifecycle (`active/`, `archive/`). All implementation is driven by tasks defined here.
- `.ai/`: The canonical knowledge base for AI behavior (guidelines, prompt templates, guardrail hooks, and skills).
- `backend/`: *(To be created)* The Python FastAPI application and worker.
- `frontend/`: *(To be created)* The Next.js web application.
