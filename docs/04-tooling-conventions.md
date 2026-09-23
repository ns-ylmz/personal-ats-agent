# Tooling Conventions

The reasoning behind the tooling setup for the Personal ATS project.

## Tech-Stack
-   **Backend**: Python 3.12+ 
-   **Frontend**: Node.js (Next.js)

## Lint & Format
Formatting and linting should be automated and non-debatable.

-   **Backend (Python)**: We use **Ruff** for blazingly fast linting and formatting. It replaces `flake8`, `black`, and `isort`.
-   **Frontend (TypeScript)**: We use **Prettier** + **ESLint**.

Enforcement should run at two levels:
| Level          | Mechanism                                            | Bypassable                       |
| -------------- | ---------------------------------------------------- | -------------------------------- |
| At commit time | `pre-commit` framework (`.pre-commit-config.yaml`)   | Yes (`--no-verify`)              |
| On every PR    | `.github/workflows/ci.yml`                           | No — the enforcement that counts |

## Dependency Management
-   Backend: `requirements.txt` (kept simple for MVP, may migrate to `poetry` or `uv` later).
-   Frontend: `npm` or `pnpm`.
