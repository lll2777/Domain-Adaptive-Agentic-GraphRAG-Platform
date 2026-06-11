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

Phase 2 retrieval now reads persisted SQLite chunks.

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

### 0007 - Sample chunks persisted to SQLite

Date: 2026-06-11

Goal:
Persist chunk records from the sample ingestion pipeline so the retrieval layer has a durable local source of truth.

Files changed:
- app/storage/sqlite_store.py: added chunk table initialization plus chunk upsert, count, and list methods.
- app/ingestion/pipeline.py: changed sample ingestion to generate chunks and persist both documents and chunks.
- app/api/routes_ingest.py: extended `POST /ingest/sample` response with chunk counts.
- scripts/ingest_sample.py: updated output to report document and chunk writes.
- tests/test_chunk_sqlite_store.py: added SQLite chunk persistence regression tests.
- tests/test_sample_ingest_chunks.py: added end-to-end sample chunk ingestion test.
- AGENTS.md: updated Latest Agent Checkpoint.
- PROJECT_MEMORY.md: added this change log entry.

Implementation notes:
- Chunk data is now written to `data/sqlite/app.db` alongside documents.
- Chunk metadata keeps `doc_id` so later Qdrant and Neo4j linking can reuse the same IDs.
- The sample ingest route now reports both document and chunk write counts.

Commands run:
- `python -m pytest tests/test_chunk_sqlite_store.py tests/test_sample_ingest_chunks.py -q`
- `.\\.venv\\Scripts\\python -m pytest tests -q`
- `.\\.venv\\Scripts\\python -m compileall app scripts`
- `.\\.venv\\Scripts\\python -c "from app.api.routes_ingest import ingest_sample; print(ingest_sample()['chunks'])"`

Test results:
- Targeted chunk persistence tests: `3 passed`.
- Full test suite: `15 passed`.
- Compile check succeeded.
- API ingest smoke check returned `5` chunks.

Large files or caches generated:
- Path: `D:\codex_project\Domain-Adaptive Agentic GraphRAG Platform\data\sqlite\app.db`
- Size if known: small SQLite demo database, not measured
- Should be committed: no

Known issues:
- Qdrant and Neo4j integrations still need real persistence adapters.

Next steps:
- Add Qdrant indexing with graceful fallback.
- Add Neo4j graph writing with graceful fallback.

### 0008 - Qdrant indexing adapter added

Date: 2026-06-11

Goal:
Add a Qdrant vector indexing adapter for sample chunks while keeping ingestion usable when Qdrant is not running.

Files changed:
- app/retrieval/qdrant_retriever.py: implemented REST-based collection creation and chunk vector upsert using deterministic hashing embeddings.
- app/ingestion/pipeline.py: added optional Qdrant indexer injection and Qdrant status fields in sample ingest results.
- app/api/routes_ingest.py: wired `POST /ingest/sample` to attempt Qdrant indexing and report status.
- scripts/ingest_sample.py: added Qdrant status reporting.
- tests/test_qdrant_retriever.py: added request-shape and graceful-fallback tests for Qdrant indexing.
- tests/test_sample_ingest_qdrant.py: added sample ingest test for Qdrant status reporting.
- README.md: documented Qdrant indexing behavior and how to start Qdrant.
- AGENTS.md: updated Latest Agent Checkpoint.
- PROJECT_MEMORY.md: added this change log entry.

Implementation notes:
- The adapter uses Qdrant REST calls through `requests`, avoiding a new client dependency.
- Point IDs are deterministic integers derived from chunk IDs.
- If Qdrant is unavailable, ingestion returns `qdrant_status = unavailable` and keeps SQLite writes intact.
- The smoke check returned `unavailable` because Qdrant was not running in this environment.

Commands run:
- `python -m pytest tests/test_qdrant_retriever.py -q`
- `python -m pytest tests/test_sample_ingest_qdrant.py -q`
- `.\\.venv\\Scripts\\python -m pytest tests -q`
- `.\\.venv\\Scripts\\python -m compileall app scripts`
- `.\\.venv\\Scripts\\python -c "from app.api.routes_ingest import ingest_sample; print(ingest_sample()['qdrant_status'])"`

Test results:
- Qdrant adapter tests: `2 passed`.
- Sample ingest Qdrant test: `1 passed`.
- Full test suite: `18 passed`.
- Compile check succeeded.
- API ingest smoke check returned `unavailable`, which is the expected graceful fallback when Qdrant is not running.

Large files or caches generated:
- Path: `D:\codex_project\Domain-Adaptive Agentic GraphRAG Platform\data\sqlite\app.db`
- Size if known: small SQLite demo database, not measured
- Should be committed: no

Known issues:
- Qdrant service was not running during smoke check, so vector indexing could not be verified against a live server.
- Neo4j graph writing still needs a persistence adapter.

Next steps:
- Add Neo4j graph writing with graceful fallback.
- Use SQLite/Qdrant data in hybrid retrieval.

### 0009 - Neo4j graph writing adapter added

Date: 2026-06-11

Goal:
Add Neo4j graph writing for rule-based entities and relations while keeping sample ingestion usable when Neo4j is not running.

Files changed:
- app/graph/cypher_templates.py: changed Cypher templates to batch-merge entities and relations.
- app/graph/neo4j_client.py: implemented Neo4j transactional HTTP writer with graceful unavailable fallback.
- app/ingestion/pipeline.py: added optional Neo4j writer injection and graph status fields in sample ingest results.
- app/api/routes_ingest.py: wired `POST /ingest/sample` to attempt Neo4j graph writing and report graph counts/status.
- scripts/ingest_sample.py: added Neo4j status reporting.
- tests/test_neo4j_client.py: added request-shape and graceful-fallback tests for Neo4j graph writing.
- tests/test_sample_ingest_neo4j.py: added sample ingest test for Neo4j status reporting.
- README.md: documented Neo4j graph writing behavior and how to start Neo4j with Docker Compose.
- AGENTS.md: updated Latest Agent Checkpoint.
- PROJECT_MEMORY.md: added this change log entry.

Implementation notes:
- The adapter uses Neo4j's transactional HTTP endpoint at `/db/neo4j/tx/commit`.
- Rule-based entities and relations are built from sample documents via `build_graph_records`.
- If Neo4j is unavailable, ingestion returns `neo4j_status = unavailable` and keeps SQLite/Qdrant progress intact.
- The smoke check returned `unavailable` because Neo4j was not running in this environment.

Commands run:
- `python -m pytest tests/test_neo4j_client.py tests/test_sample_ingest_neo4j.py -q`
- `python -m pytest tests/test_qdrant_retriever.py tests/test_sample_ingest_qdrant.py -q`
- `.\\.venv\\Scripts\\python -m pytest tests -q`
- `.\\.venv\\Scripts\\python -m compileall app scripts`
- `.\\.venv\\Scripts\\python -c "from app.api.routes_ingest import ingest_sample; print(ingest_sample()['neo4j_status'])"`

Test results:
- Neo4j adapter tests: `3 passed`.
- Qdrant regression tests: `3 passed`.
- Full test suite: `21 passed`.
- Compile check succeeded.
- API ingest smoke check returned `unavailable`, which is the expected graceful fallback when Neo4j is not running.

Large files or caches generated:
- Path: `D:\codex_project\Domain-Adaptive Agentic GraphRAG Platform\data\sqlite\app.db`
- Size if known: small SQLite demo database, not measured
- Should be committed: no

Known issues:
- Neo4j service was not running during smoke check, so graph writing was verified with unit tests and graceful-fallback smoke check only.

Next steps:
- Use SQLite/Qdrant/Neo4j data in hybrid retrieval and graph retrieval.

### 0010 - Neo4j adapter push pending

Date: 2026-06-11

Goal:
Record that the Neo4j adapter work is committed locally but could not be pushed because GitHub connectivity is unavailable.

Files changed:
- AGENTS.md: updated Latest Agent Checkpoint to note push is pending.
- PROJECT_MEMORY.md: added this change log entry.

Implementation notes:
- Local commit `ada7519` contains the Neo4j graph writing adapter.
- `Test-NetConnection github.com -Port 443` returned `TcpTestSucceeded : False`.
- `git -c http.version=HTTP/1.1 push` failed with `Failed to connect to github.com port 443`.

Commands run:
- `git -c http.version=HTTP/1.1 push`
- `Test-NetConnection github.com -Port 443 | Format-List ComputerName,RemoteAddress,TcpTestSucceeded`
- `Start-Sleep -Seconds 20; Test-NetConnection github.com -Port 443 | Format-List ComputerName,RemoteAddress,TcpTestSucceeded; git -c http.version=HTTP/1.1 push`

Test results:
- No additional tests were needed for this documentation-only push status update.
- The Neo4j adapter change was already verified with `21 passed` before commit.

Large files or caches generated:
- None.

Known issues:
- GitHub is temporarily unreachable from this machine.

Next steps:
- Retry `git -c http.version=HTTP/1.1 push` after github.com:443 becomes reachable.

### 0011 - Query workflow uses SQLite chunks

Date: 2026-06-11

Goal:
Make query-time retrieval prefer persisted SQLite chunks instead of rebuilding from sample JSON every time.

Files changed:
- app/retrieval/query_service.py: added query service helpers to load persisted chunks, build a BM25-backed workflow, and run queries.
- app/api/routes_query.py: changed `POST /query` to use `SQLiteStore` and the query service, with sample fallback.
- tests/test_query_service.py: added tests proving stored chunks are used and sample data is used as fallback when the store is empty.
- README.md: documented the `/query` data-source behavior.
- AGENTS.md: updated Latest Agent Checkpoint.
- PROJECT_MEMORY.md: added this change log entry.

Implementation notes:
- Query retrieval now checks `SQLiteStore.count_chunks()` and uses `SQLiteStore.list_chunks()` when chunks exist.
- If no chunks exist, the service falls back to `data/samples/ai_papers.json`.
- This is the first hybrid retrieval plumbing step; Qdrant search and Neo4j graph retrieval still need to be added to the query path.

Commands run:
- `python -m pytest tests/test_query_service.py -q`
- `.\\.venv\\Scripts\\python -m pytest tests -q`
- `.\\.venv\\Scripts\\python -m compileall app scripts`
- `.\\.venv\\Scripts\\python -c "from app.api.routes_query import query, QueryRequest; print(query(QueryRequest(question='What is GraphRAG?', top_k=3))['query_type'])"`

Test results:
- Query service tests: `2 passed`.
- Full test suite: `23 passed`.
- Compile check succeeded.
- Query route smoke check returned `factual`.

Large files or caches generated:
- Path: `D:\codex_project\Domain-Adaptive Agentic GraphRAG Platform\data\sqlite\app.db`
- Size if known: small SQLite demo database from earlier smoke checks, not measured
- Should be committed: no

Known issues:
- Qdrant vector search and Neo4j graph retrieval are not yet included in the query path.

Next steps:
- Add live Qdrant search to query retrieval with graceful fallback.
- Add Neo4j-backed graph retrieval to query retrieval with graceful fallback.

### 0012 - Hybrid retrieval now merges SQLite, Qdrant, and Neo4j

Date: 2026-06-11

Goal:
Upgrade query-time retrieval to combine persisted SQLite chunks, live Qdrant search, and Neo4j graph retrieval into one hybrid path.

Files changed:
- app/retrieval/qdrant_retriever.py: implemented live Qdrant search over the REST API with graceful fallback.
- app/retrieval/graph_retriever.py: implemented live Neo4j graph search over the transactional HTTP API with graceful fallback.
- app/retrieval/hybrid_retriever.py: added source merging, de-duplication, simple score normalization, and graph context capture.
- app/retrieval/query_service.py: switched query construction to the hybrid retriever and passed through graph context and source scores.
- app/agent/workflow.py: allowed domain-aware search calls so Qdrant filters can receive the requested domain.
- tests/test_qdrant_search.py: added Qdrant search regression tests.
- tests/test_graph_retriever.py: added Neo4j graph retrieval regression tests.
- tests/test_hybrid_retriever.py: added hybrid merge/deduplication tests.
- tests/test_query_service.py: kept coverage for persisted chunk use and sample fallback.
- README.md: clarified that `/query` now merges SQLite, Qdrant, and Neo4j with graceful degradation.
- AGENTS.md: updated Latest Agent Checkpoint.
- PROJECT_MEMORY.md: added this change log entry.

Implementation notes:
- `/query` now prefers persisted SQLite chunks, then merges Qdrant vector hits and Neo4j graph evidence.
- Graph hits contribute both retrieved chunks and graph context for downstream UI and evaluation use.
- Domain-aware search is threaded toward Qdrant so the `domain` filter can be applied when available.
- The system still falls back to sample JSON and skip states when Qdrant or Neo4j are offline.

Commands run:
- `python -m pytest tests/test_qdrant_search.py tests/test_graph_retriever.py tests/test_hybrid_retriever.py tests/test_query_service.py -q`
- `.\\.venv\\Scripts\\python -m pytest tests -q`
- `python -m compileall app scripts`
- `.\\.venv\\Scripts\\python -c "from app.api.routes_query import query, QueryRequest; result=query(QueryRequest(question='What is GraphRAG?', top_k=3)); print(result['query_type']); print(result['scores'].keys())"`

Test results:
- New retrieval tests: `7 passed`.
- Full test suite: `28 passed`.
- Compile check succeeded.
- Query smoke check returned `factual` and included `top_score`, `bm25_score`, `qdrant_score`, and `graph_score`.

Large files or caches generated:
- Path: `D:\codex_project\Domain-Adaptive Agentic GraphRAG Platform\data\sqlite\app.db`
- Size if known: small SQLite demo database, not measured
- Should be committed: no

Known issues:
- Qdrant and Neo4j live services were not running during smoke check, so those branches were validated via unit tests and graceful-fallback behavior.

Next steps:
- Expose richer graph context and retrieved chunk details in the UI.
- Continue filling out evaluation and docs.

### 0013 - Hybrid retrieval push pending

Date: 2026-06-11

Goal:
Record that hybrid query retrieval is committed locally but could not be pushed because GitHub connectivity failed.

Files changed:
- AGENTS.md: updated Latest Agent Checkpoint to note push is pending.
- PROJECT_MEMORY.md: added this change log entry.

Implementation notes:
- Local commit `86b9cdb` contains the hybrid retrieval work.
- `git -c http.version=HTTP/1.1 push` failed with `RPC failed; curl 56 Recv failure: Connection was reset`.
- `git ls-remote origin refs/heads/main` then failed with `Failed to connect to github.com port 443`.
- The local branch is ahead of `origin/main`.

Commands run:
- `git -c http.version=HTTP/1.1 push`
- `git status --short --branch`
- `git log --oneline -5`
- `git ls-remote origin refs/heads/main`

Test results:
- No additional tests were needed for this documentation-only push status update.
- The hybrid retrieval work was already verified with `28 passed` before commit.

Large files or caches generated:
- None.

Known issues:
- GitHub is temporarily unreachable from this machine.

Next steps:
- Retry `git -c http.version=HTTP/1.1 push` after github.com:443 becomes reachable.
- Expose richer graph context and retrieved chunk details in the UI.

### 0014 - Streamlit exposes hybrid retrieval details

Date: 2026-06-11

Goal:
Make the beginner-facing Streamlit UI reflect the same persisted SQLite + BM25 + Qdrant + Neo4j query path used by the API.

Files changed:
- app/ui/streamlit_app.py: switched sample ingest to the persisted ingestion pipeline, switched Ask to `run_query`, added domain selection, and displayed evidence status, citations, source scores, retrieved chunks, and graph context.
- app/ui/view_models.py: added small formatting helpers for Streamlit score, chunk, graph, and evidence display.
- tests/test_ui_view_models.py: added regression tests for the Streamlit view model helpers.
- README.md: documented the richer Streamlit Ask page and current hybrid retrieval stack.
- AGENTS.md: updated Latest Agent Checkpoint.
- PROJECT_MEMORY.md: added this change log entry.

Implementation notes:
- The UI now reports persisted SQLite document/chunk counts on Home when data has been imported.
- The Ingest page writes SQLite first and then attempts Qdrant indexing and Neo4j graph writing, with graceful unavailable statuses.
- The Ask page uses the shared query service, so UI and API behavior stay aligned.
- Qdrant and Neo4j remain optional for local MVP use; if they are offline, UI tables still render with fallback/empty values.

Commands run:
- `python -m pytest tests/test_ui_view_models.py -q`
- `python -m pytest tests -q`
- `python -m compileall app scripts`

Test results:
- UI view model tests: `4 passed`.
- Full test suite: `32 passed`.
- Compile check succeeded.

Large files or caches generated:
- None from this UI update.

Known issues:
- Browser automation was not available in this session, so the Streamlit UI was verified by tests and import/compile checks rather than an in-app screenshot.
- GitHub push is still pending from earlier network failures.

Next steps:
- Commit this UI update.
- Retry `git -c http.version=HTTP/1.1 push` after github.com:443 becomes reachable.
- Continue filling out evaluation quality reporting and docs.

### 0015 - GitHub sync restored after UI update

Date: 2026-06-11

Goal:
Record that the pending local commits, including hybrid retrieval and Streamlit UI details, were successfully pushed to GitHub.

Files changed:
- AGENTS.md: updated Latest Agent Checkpoint to show GitHub sync is current.
- PROJECT_MEMORY.md: added this change log entry.

Implementation notes:
- `git -c http.version=HTTP/1.1 push` succeeded.
- GitHub `main` advanced from `a9768b9` to `0780634`.
- Earlier GitHub connectivity failures are no longer blocking the current local branch.

Commands run:
- `git status --short --branch`
- `git -c http.version=HTTP/1.1 push`

Test results:
- No new tests were needed for this documentation-only push status update.
- The UI update was already verified with `32 passed` and compile checks before commit.

Large files or caches generated:
- None.

Known issues:
- None for GitHub sync at this checkpoint.

Next steps:
- Continue filling out evaluation quality reporting and docs.

### 0016 - Evaluation dashboard uses hybrid retrieval

Date: 2026-06-11

Goal:
Make sample evaluation reflect the current retrieval pipeline and present the results more clearly in Streamlit.

Files changed:
- app/evaluation/evaluator.py: switched sample evaluation to a reused hybrid retriever/workflow, added per-question query metadata/source scores, and returned a summary with average proxy metrics.
- app/retrieval/qdrant_retriever.py: cached unavailable search state per retriever instance to avoid repeated offline waits.
- app/retrieval/graph_retriever.py: cached unavailable graph search state per retriever instance to avoid repeated offline waits.
- app/ui/view_models.py: added evaluation summary and per-question metric table helpers.
- app/ui/streamlit_app.py: changed Evaluation page from raw JSON to summary and per-question tables.
- tests/test_evaluator.py: added evaluation output regression coverage.
- tests/test_qdrant_search.py: added repeated-unavailable Qdrant search coverage.
- tests/test_graph_retriever.py: added repeated-unavailable Neo4j graph search coverage.
- tests/test_ui_view_models.py: added evaluation table helper coverage.
- README.md: documented that evaluation now uses the hybrid query path and shows summary/per-question metrics.
- AGENTS.md: updated Latest Agent Checkpoint.
- PROJECT_MEMORY.md: added this change log entry.

Implementation notes:
- Evaluation now builds one `HybridRetriever` and one `QueryWorkflow` per run instead of rebuilding them for every question.
- If Qdrant or Neo4j are offline, the first failed search marks that retriever instance unavailable so the remaining evaluation questions do not wait on repeated connection attempts.
- The API response shape still keeps `metrics` and now adds `summary`.

Commands run:
- `python -m pytest tests/test_evaluator.py -q`
- `python -m pytest tests/test_qdrant_search.py tests/test_graph_retriever.py -q`
- `python -m pytest tests/test_ui_view_models.py -q`

Test results:
- Initial evaluator test failed as expected before implementation because `summary` did not exist.
- Initial repeated-unavailable retriever tests failed as expected because each search retried the offline service.
- Evaluator test now passes in about 9 seconds instead of about 81 seconds.
- Qdrant/Neo4j retriever tests: `6 passed`.
- UI view model tests: `5 passed`.

Large files or caches generated:
- None from this evaluation update.

Known issues:
- Qdrant and Neo4j live services were not running during tests, so live service behavior remains covered by request-shape unit tests and graceful-fallback behavior.

Next steps:
- Run full test suite and compile check.
- Commit and push this evaluation dashboard update.
- Continue reviewing remaining prompt coverage.

### 0017 - Evaluation dashboard push pending

Date: 2026-06-11

Goal:
Record that the evaluation dashboard update is committed locally but could not be pushed because GitHub is unreachable from this machine.

Files changed:
- AGENTS.md: updated Latest Agent Checkpoint to note push is pending.
- PROJECT_MEMORY.md: added this change log entry.

Implementation notes:
- Local commit `41c1942` contains the evaluation dashboard update.
- `git -c http.version=HTTP/1.1 push` failed before sending because `github.com:443` could not be reached.
- The local branch is ahead of `origin/main`.

Commands run:
- `git -c http.version=HTTP/1.1 push`

Test results:
- No new tests were needed for this documentation-only push status update.
- The evaluation dashboard update was already verified with `36 passed` and compile checks before commit.

Large files or caches generated:
- None.

Known issues:
- GitHub is temporarily unreachable from this machine.

Next steps:
- Retry `git -c http.version=HTTP/1.1 push` after github.com:443 becomes reachable.
- Continue reviewing remaining prompt coverage.
