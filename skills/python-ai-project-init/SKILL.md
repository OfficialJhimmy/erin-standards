---
name: python-ai-project-init
description: Scaffold a new Python project for AI/LLM development using uv, ruff, and pytest. Invoke with /python-ai-project-init when starting a new Python-based AI project (agents, API wrappers, RAG pipelines, evals).
---

# Python AI project init

## Before running anything

Confirm project name and what kind of AI project this is (API wrapper/agent script, FastAPI service, data/eval pipeline) if not already clear, the dependency set differs meaningfully between those.

## Steps

1. Check `uv` is installed (`uv --version`). If missing, tell the user to install it rather than silently falling back to pip, since the point of this skill is the uv-based workflow, not a generic one.

2. Scaffold with uv, using the package layout (`src/`) rather than a flat script layout unless this is genuinely a single-file tool:
   ```
   uv init <project-name> --package
   cd <project-name>
   ```

3. Pin a Python version floor appropriate for current tooling (3.11+) in `pyproject.toml`'s `requires-python` if `uv init` didn't already set one you're happy with.

4. Add dependencies based on what the project actually needs. Don't add all of these by default, ask or infer from what the user described:
   - Core: `uv add anthropic` (and `openai` only if actually using it)
   - Config/validation: `uv add pydantic python-dotenv`
   - If it's a service: `uv add fastapi uvicorn`
   - Dev only: `uv add --dev pytest ruff` (use `[dependency-groups]`, not the legacy `[tool.uv.dev-dependencies]` table)

5. Configure ruff in `pyproject.toml` (`[tool.ruff]`) for linting and formatting, replacing black/isort rather than running both.

6. Set up `.env` handling: `.env.example` with placeholder keys, `.env` in `.gitignore`, and confirm the code actually loads it (`load_dotenv()` if using `python-dotenv`, or document that the deployment platform injects env vars directly if this won't run locally against a `.env`).

7. Add a minimal `tests/` directory with one real passing test, not just an empty placeholder, so `uv run pytest` has something to prove the setup works.

8. Commit `uv.lock`, current uv guidance is to commit it for applications and services, not just libraries.

9. Write a project `CLAUDE.md` noting: use `uv run` for everything (never call `pytest`/`ruff` directly, since that bypasses the locked environment), `uv add`/`uv sync` instead of pip, and the actual commands for lint/test/run.

10. Report what was created, confirm `uv run pytest` passes, and stop there, don't scaffold CI, deployment, or Docker unless asked.
