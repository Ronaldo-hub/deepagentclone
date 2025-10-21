# TODO: Fix deepagentclone project (prioritized)

This TODO lists the minimal, prioritized steps to make the repository runnable and testable. Execute tasks in order; run tests and lint after each group.

1. Quick syntax fixes (high priority)
   - Remove any invalid `// filepath:` comment lines from Python files if present.

2. Consolidate module boundaries (high)
   - Use `backend.py` as the canonical implementation for core agent classes (AIAgent, WebSearchAgent, EmailAgent, DatabaseAgent, TaskQueue, Config).
   - Keep advanced/example features in `main.py` (AgentMemory, WorkflowEngine, PluginManager, etc.).

3. Fix tests and layout (high)
   - Move top-level tests into a `tests/` directory.
   - Update tests to import from `backend` (for core agent classes) and `main` (for advanced features).

4. Split/repair docker and dependency files (high)
   - If `docker-compose.yml` contains concatenated files, split into `docker-compose.yml`, `Dockerfile`, `requirements.txt`, and `.env.example`.

5. Fix dataclass defaults & import-time side effects (high)
   - Replace evaluated-at-import defaults like `datetime.now()` with `field(default_factory=...)`.
   - Guard any long-running examples behind `if __name__ == "__main__":`.

6. Worker / TaskQueue / imports (high)
   - Ensure `worker.py` (if present) imports `TaskQueue` from `backend` or move `TaskQueue` into `tasks.py` and update imports accordingly.

7. Async vs blocking I/O (medium)
   - Audit for blocking calls inside `async def` and wrap them in `asyncio.to_thread` or use async clients.

8. Frontend file fixes (medium)
   - Add proper extensions and placement for `ai_agent_dashboard` frontend files (e.g., `ai_agent_dashboard/src/...`).

9. Requirements & heavy dependencies (medium)
   - For local dev/tests use lightweight or mocked dependencies; defer heavy ML libs to a separate environment.

10. CI / Docker / run instructions (medium)
   - Add `scripts/` with bootstrap, run-dev, and test commands; update `README.md` and `setup_guide.md`.

11. Code quality & safety (low)
   - Add linters (`ruff`/`flake8`) and optional `mypy` type checks.

Verification steps after edits:
- Run `pytest -q` and fix remaining import/runtime errors.
- Run `python -m pyflakes <files>` or `ruff` for linting.

If you'd like, I can continue and apply additional changes (split docker files, wrap blocking calls, or add a small test harness). Reply with which next step to take.
