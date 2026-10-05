# Task: Persistent Database

## Objective
Ensure the SQLite database file path is absolute so it persists consistently, regardless of which directory the backend is started from.

## Required Context
- `backend/app/database.py`

## Affected Areas
- `backend/app/database.py`

## Constraints
- Modify `SQLALCHEMY_DATABASE_URL` to dynamically resolve an absolute path relative to the script's location.

## Out of Scope
- Changing to a different database engine (e.g. Postgres).
- Data migrations.

## Verification
- Start the server from the root directory and from the `backend/` directory; both should write to the same `backend/app/app.db` file.

## Completion Criteria
- `SQLALCHEMY_DATABASE_URL` uses `os.path.abspath`.

## Agent Execution Prompt
Implement the database path fix to ensure SQLite is persistent.
