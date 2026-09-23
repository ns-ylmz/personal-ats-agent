# 003: Use SQLite and SQLAlchemy

## Context
We need to persist the user's master profile, job application statuses, and interview feedback.

## Decision
We will use SQLite as the relational database, interfaced via SQLAlchemy 2.0 ORM.

## Consequences
- **Positive:** No database server setup required; single file portability (`app.db`). Using SQLAlchemy ensures that migrating to PostgreSQL in the future requires minimal code changes.
- **Negative:** Limited concurrency for write operations, which is acceptable for a single-user personal tool.
