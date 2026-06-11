# PROJECT_MEMORY.md

This file is the long-term memory for the project. It must be updated after every code change so future agents can continue even if chat history is lost.

## Project Overview

Project name: Domain-Adaptive Agentic GraphRAG Platform

Chinese name: 面向多领域知识库的自适应 Agentic GraphRAG 平台

Local project path:

`D:\codex_project\Domain-Adaptive Agentic GraphRAG Platform`

Primary domain: AI Research Papers

Long-term goal:
Build a resume-quality, domain-adaptive Agentic GraphRAG system that can later migrate to financial reports, biomedical literature, legal documents, enterprise knowledge bases, and code repositories.

## Current Architecture

To be updated as the project is implemented.

## Current Phase

Phase 2 data ingestion started.

## Environment Assumptions

- Windows environment
- Project should stay under D drive
- C drive space is limited
- Python 3.11+
- FastAPI backend
- Streamlit frontend
- Qdrant via Docker
- Neo4j via Docker
- SQLite for lightweight metadata storage
- Mock LLM mode must work without API keys

## D Drive Storage Rules

Project root:

`D:\codex_project\Domain-Adaptive Agentic GraphRAG Platform`

Large or generated project files should stay under:

- `.venv/`
- `.cache/`
- `.models/`
- `data/raw/`
- `data/cache/`
- `data/qdrant_storage/`
- `data/neo4j_data/`
- `data/neo4j_logs/`
- `data/sqlite/`

These paths must not be committed to Git.

If Docker Desktop itself stores WSL2 disk images on C drive, the user must manually set Docker Desktop disk image location to:

`D:\DockerData`

## Important Decisions

- The project must be beginner-friendly.
- The first working version must use sample AI paper data.
- Do not require paid API keys for the MVP.
- Keep advanced integrations as adapters if they are too heavy.
- Use AGENTS.md for agent instructions.
- Use PROJECT_MEMORY.md for detailed development memory.
- Protect C drive space by keeping project data, caches, databases, and models under the D drive project directory.

## Change Log

### 0001 - Repository setup

Date: 2026-06-11

Goal:
Initialize repository memory and agent rules.

Changes:
- Initialized Git repository.
- Created AGENTS.md.
- Created PROJECT_MEMORY.md.
- Created .gitignore.
- Created .env.example.
- Added D drive storage and C drive protection rules.

Files changed:
- AGENTS.md: added agent workflow, Git rules, memory rules, and D drive storage rules.
- PROJECT_MEMORY.md: added long-term project memory.
- .gitignore: added Python, AI, Docker, database, cache, and generated data ignores.
- .env.example: added D drive based environment variable examples.

Commands run:
- `cd "D:\codex_project\Domain-Adaptive Agentic GraphRAG Platform"`
- `git status --short --branch`
- `git remote -v`
- `git branch --show-current`
- `git init`
- `git branch -M main`
- `git add AGENTS.md PROJECT_MEMORY.md .gitignore .env.example`
- `git commit -m "chore: initialize repository memory and agent rules"`

Test results:
- Not applicable yet. Repository setup contains no executable project code.

Large files or caches generated:
- None.

GitHub push:
- Not pushed because `remote origin` is not configured.

Next steps:
- Configure GitHub remote if missing.
- Start project scaffold.

### 0002 - Configure GitHub remote

Date: 2026-06-11

Goal:
Connect the local repository to the user's GitHub repository and prepare for pushing the initialized project memory.

Files changed:
- AGENTS.md: updated Latest Agent Checkpoint to record the GitHub remote configuration.
- PROJECT_MEMORY.md: added this change log entry for remote setup.

Implementation notes:
- Configured `origin` as `https://github.com/lll2777/Domain-Adaptive-Agentic-GraphRAG-Platform.git`.
- No secrets, tokens, API keys, passwords, or private keys were written to repository files.

Commands run:
- `git status --short --branch`
- `git remote -v`
- `git branch --show-current`
- `git remote add origin https://github.com/lll2777/Domain-Adaptive-Agentic-GraphRAG-Platform.git`
- `git remote -v`

Test results:
- Not applicable. This was a repository configuration and documentation update.

Large files or caches generated:
- Path: None
- Size if known: 0
- Should be committed: no

Known issues:
- First `git push -u origin main` failed with `Recv failure: Connection was reset`.
- Network diagnostics showed `github.com:443` was reachable and `git ls-remote` could access the repository.
- A retry of `git push -u origin main` succeeded.

Next steps:
- Start the project scaffold.

### 0003 - Push repository to GitHub

Date: 2026-06-11

Goal:
Record the successful GitHub push after configuring the remote repository.

Files changed:
- AGENTS.md: updated Latest Agent Checkpoint to show that `main` was pushed to GitHub.
- PROJECT_MEMORY.md: recorded push diagnostics and the successful retry.

Implementation notes:
- The first push attempt failed because the HTTPS connection was reset.
- `Test-NetConnection github.com -Port 443` confirmed TCP connectivity.
- `git ls-remote https://github.com/lll2777/Domain-Adaptive-Agentic-GraphRAG-Platform.git` succeeded with empty output, consistent with an empty reachable repository.
- The second `git push -u origin main` succeeded and set `main` to track `origin/main`.

Commands run:
- `git push -u origin main`
- `git ls-remote https://github.com/lll2777/Domain-Adaptive-Agentic-GraphRAG-Platform.git`
- `Test-NetConnection github.com -Port 443`
- `git status --short --branch`
- `git log --oneline -2`
- `git push -u origin main`

Test results:
- Not applicable. This was a repository publishing and documentation update.

Large files or caches generated:
- Path: None
- Size if known: 0
- Should be committed: no

Known issues:
- None for repository setup.

Next steps:
- Start the project scaffold.

### 0004 - Phase 1 runnable scaffold

Date: 2026-06-11

Goal:
Build the first runnable scaffold for the Domain-Adaptive Agentic GraphRAG Platform.

Files changed:
- README.md: added beginner-friendly setup, Mermaid diagrams, D-drive guidance, Docker commands, API examples, evaluation explanation, migration notes, resume wording, and FAQ.
- requirements.txt: added FastAPI, Uvicorn, Pydantic, Streamlit, PyYAML, Requests, and Pytest.
- docker-compose.yml: added Qdrant and Neo4j services with D-drive bind mounts.
- app/: added core models, chunking, schema loading, embeddings fallback, LLM abstraction, retrieval, agent workflow, ingestion adapters, graph helpers, evaluation helpers, API routes, Streamlit UI, and storage boundary modules.
- configs/domains/: added ai_paper and financial_report YAML schemas.
- data/samples/ai_papers.json: added synthetic demo records.
- data/eval/sample_questions.json: added sample evaluation prompts.
- scripts/: added sample ingest, arXiv ingest, evaluation, and reset helpers.
- tests/: added chunking, schema, BM25, workflow, and citation regression tests.
- docs/superpowers/plans/2026-06-11-phase-1-runnable-scaffold.md: added the implementation plan for this stage.
- AGENTS.md: updated Latest Agent Checkpoint for phase 1.
- PROJECT_MEMORY.md: added this change log entry.

Implementation notes:
- Kept the first-stage implementation mock-friendly and offline-capable.
- BM25 is implemented locally; Qdrant and Neo4j are adapter skeletons for phase 2.
- Query workflow supports factual/comparison/multi_hop/trend_analysis/citation_trace/out_of_domain routing.
- Citation checking now rejects fabricated chunk IDs.
- Synthetic sample records are clearly marked via `metadata.is_synthetic = true`.

Commands run:
- `python -m pytest tests -q`
- `python -m compileall app scripts`
- `python -c "from app.main import app; print(app.title)"`
- `python -m venv .venv`
- `.\\.venv\\Scripts\\python -m pip install --upgrade pip`
- `.\\.venv\\Scripts\\python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn`
- `.\\.venv\\Scripts\\python -m pytest tests -q`
- `.\\.venv\\Scripts\\python -c "from app.main import app; print(app.title)"`
- `.\\.venv\\Scripts\\python -c "import streamlit, uvicorn; print(streamlit.__version__)"`

Test results:
- `9 passed` with the system Python.
- `9 passed` with the project `.venv`.
- `python -c "from app.main import app; print(app.title)"` succeeded in `.venv`.

Large files or caches generated:
- Path: `D:\codex_project\Domain-Adaptive Agentic GraphRAG Platform\.venv`
- Size if known: not measured, but expected to be sizable
- Should be committed: no
- Path: `D:\codex_project\Domain-Adaptive Agentic GraphRAG Platform\.cache\pip`
- Size if known: not measured
- Should be committed: no

Known issues:
- The first default PyPI install attempt failed with SSL EOF errors, but the mirror-based retry succeeded.
- `.venv` and `.cache` exist only for local execution and remain ignored.

Next steps:
- Start phase 2 data persistence and retrieval plumbing.

### 0005 - Phase 1 push pending

Date: 2026-06-11

Goal:
Record that the phase 1 scaffold is complete locally but GitHub push is temporarily blocked by network connectivity.

Files changed:
- AGENTS.md: updated Latest Agent Checkpoint to note the push is pending because github.com:443 is unreachable.
- PROJECT_MEMORY.md: added this change log entry for the push failure state.

Implementation notes:
- Local commit `103ffae` contains the phase 1 scaffold.
- `Test-NetConnection github.com -Port 443` failed twice with `TcpTestSucceeded : False`.
- `git push` failed with `Failed to connect to github.com port 443 after 21088 ms`.
- The repository is currently one commit ahead of `origin/main`.

Commands run:
- `Test-NetConnection github.com -Port 443 | Format-List ComputerName,RemoteAddress,TcpTestSucceeded`
- `git push`
- `Start-Sleep -Seconds 20; Test-NetConnection github.com -Port 443 | Format-List ComputerName,RemoteAddress,TcpTestSucceeded; git push`

Test results:
- Project tests still pass in `.venv`: `9 passed`.

Large files or caches generated:
- None beyond the existing `.venv` and `.cache` from the stage.

Known issues:
- GitHub connectivity is temporarily unavailable from this machine.

Next steps:
- Retry `git push` after github.com:443 becomes reachable.
- Begin phase 2 data persistence and retrieval plumbing.

### 0006 - Sample documents persisted to SQLite

Date: 2026-06-11

Goal:
Start phase 2 by making sample ingestion persist documents to SQLite under the D-drive project data directory.

Files changed:
- app/storage/sqlite_store.py: added document upsert, count, and list methods with JSON metadata storage.
- app/ingestion/pipeline.py: added `ingest_sample_documents` to load bundled samples and persist them through `SQLiteStore`.
- app/api/routes_ingest.py: changed `POST /ingest/sample` to write sample documents to SQLite.
- scripts/ingest_sample.py: changed the script to write sample documents to SQLite and report the target path.
- tests/test_sqlite_store.py: added SQLite persistence regression tests.
- tests/test_sample_ingest.py: added sample ingestion persistence test.
- README.md: updated sample ingest docs and API examples.
- AGENTS.md: updated Latest Agent Checkpoint.
- PROJECT_MEMORY.md: added this change log entry.

Implementation notes:
- This step persists documents only. Chunk persistence, Qdrant vector indexing, and Neo4j graph writing remain next.
- SQLite path stays under `D:\codex_project\Domain-Adaptive Agentic GraphRAG Platform\data\sqlite\app.db`.
- The smoke test created `data/sqlite/app.db`; this path is ignored by Git and should not be committed.

Commands run:
- `python -m pytest tests/test_sqlite_store.py tests/test_sample_ingest.py -q`
- `.\\.venv\\Scripts\\python -m pytest tests -q`
- `.\\.venv\\Scripts\\python -m compileall app scripts`
- `.\\.venv\\Scripts\\python -c "from app.api.routes_ingest import ingest_sample; print(ingest_sample()['status'])"`

Test results:
- Targeted persistence tests: `3 passed`.
- Full test suite: `12 passed`.
- Compile check succeeded.
- API ingest route smoke check returned `ok`.

Large files or caches generated:
- Path: `D:\codex_project\Domain-Adaptive Agentic GraphRAG Platform\data\sqlite\app.db`
- Size if known: small SQLite demo database, not measured
- Should be committed: no

Known issues:
- Qdrant and Neo4j persistence are still adapter/skeleton level.

Next steps:
- Persist chunks in SQLite.
- Add Qdrant indexing with graceful fallback.
- Add Neo4j graph writing with graceful fallback.
