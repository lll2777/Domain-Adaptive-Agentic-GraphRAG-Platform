# AGENTS.md

This file contains mandatory instructions for AI coding agents working on this repository.

## Project Identity

Project name: Domain-Adaptive Agentic GraphRAG Platform

Chinese name: 面向多领域知识库的自适应 Agentic GraphRAG 平台

Local project path:

`D:\codex_project\Domain-Adaptive Agentic GraphRAG Platform`

Current primary domain: AI Research Papers

Goal: Build a resume-quality, domain-adaptive Agentic GraphRAG platform with hybrid retrieval, graph retrieval, citation checking, evaluation, and a beginner-friendly UI.

## Mandatory Workflow

Before making changes:
1. Read this AGENTS.md.
2. Read PROJECT_MEMORY.md.
3. Run `git status`.
4. Understand the current project phase and last checkpoint.
5. Confirm work is happening inside `D:\codex_project\Domain-Adaptive Agentic GraphRAG Platform`.

When making changes:
1. Keep changes small and staged by feature.
2. Do not overwrite user work without checking existing files.
3. Prefer a working MVP over over-engineered incomplete code.
4. Add or update tests when core logic changes.
5. Update README when commands, architecture, or behavior changes.
6. Never commit secrets, API keys, tokens, passwords, private keys, or `.env`.
7. Avoid writing large files to C drive.
8. Put project caches, models, databases, Qdrant storage, Neo4j data, SQLite files, and temporary downloads under the D drive project directory whenever possible.

After making changes:
1. Update PROJECT_MEMORY.md with what changed, why it changed, files touched, commands run, test results, generated large files or caches, and next steps.
2. Update the "Latest Agent Checkpoint" section in this AGENTS.md.
3. Run relevant tests or at least a syntax/import check.
4. Run `git status`.
5. Commit changes with a clear commit message.
6. Push to GitHub if remote origin and authentication are available.
7. If push fails, document the reason and tell the user exactly how to fix it.

## C Drive Space Protection

The user's C drive has limited free space.

Rules:
1. Prefer the D drive project directory for all project files.
2. Create `.venv` inside the project directory, not under C drive.
3. Put pip cache under `.cache/pip` inside the project directory.
4. Put Hugging Face, transformers, sentence-transformers, and model caches under `.cache` or `.models` inside the project directory.
5. Put Qdrant storage under `data/qdrant_storage`.
6. Put Neo4j data and logs under `data/neo4j_data` and `data/neo4j_logs`.
7. Put SQLite files under `data/sqlite`.
8. Do not commit large generated files, caches, database files, vector stores, model files, or Docker data.
9. If Docker Desktop stores WSL2 disk images on C drive, tell the user to manually change Docker Desktop disk image location to `D:\DockerData`.

Recommended PowerShell environment setup:

```powershell
cd "D:\codex_project\Domain-Adaptive Agentic GraphRAG Platform"

python -m venv .venv
.\.venv\Scripts\activate

$env:PIP_CACHE_DIR="D:\codex_project\Domain-Adaptive Agentic GraphRAG Platform\.cache\pip"
$env:HF_HOME="D:\codex_project\Domain-Adaptive Agentic GraphRAG Platform\.cache\huggingface"
$env:TRANSFORMERS_CACHE="D:\codex_project\Domain-Adaptive Agentic GraphRAG Platform\.cache\huggingface\transformers"
$env:SENTENCE_TRANSFORMERS_HOME="D:\codex_project\Domain-Adaptive Agentic GraphRAG Platform\.cache\sentence_transformers"
```

## Latest Agent Checkpoint

* Status: Phase 2 Qdrant indexing adapter added.
* Last updated by: Codex.
* Last update summary: Added Qdrant REST indexing adapter with deterministic fallback embeddings and wired sample ingest to report Qdrant indexing status while preserving SQLite progress.
* Current phase: Phase 2 data ingestion.
* Next step: Add Neo4j graph writing with graceful fallback, then use SQLite/Qdrant data in hybrid retrieval.

## Coding Standards

* Use Python 3.11+.
* Use type hints for important functions.
* Use Pydantic models for API schemas.
* Use pathlib for file paths.
* Use logging instead of print for backend code.
* Keep modules small and understandable.
* Write beginner-friendly comments only where useful.
* Do not hide failures; show clear error messages.
* Read paths from environment variables or config files when possible.
* Never hardcode C drive paths.

## Git Rules

* Commit after every meaningful development step.
* Use conventional commit style when possible:

  * `chore: initialize repository`
  * `feat: add sample ingestion pipeline`
  * `fix: handle qdrant connection failure`
  * `docs: update setup guide`
  * `test: add workflow tests`
* Never commit `.env`, database files, cache files, model files, vector stores, or large raw datasets.
* Always check `git status` before and after changes.

## Memory Rules

* PROJECT_MEMORY.md is the long-term memory file.
* Every code change must update PROJECT_MEMORY.md.
* Every code change must also update the "Latest Agent Checkpoint" section in this AGENTS.md.
* Keep AGENTS.md concise. Put detailed history in PROJECT_MEMORY.md.
* If context is unclear, rely on PROJECT_MEMORY.md before guessing.
* Record whether a stage generated large files, caches, database files, Docker volumes, or model downloads.

## Safety and Secrets

* Never ask the user to paste secrets into source files.
* Never store GitHub tokens in the repository.
* Use environment variables and `.env.example`.
* If authentication is needed, explain how the user can authenticate locally with GitHub CLI or Git credentials.

## Beginner-Friendly Requirement

Every completed phase must explain:

1. What was completed.
2. How to run it.
3. How to test it.
4. What files changed.
5. Whether files/caches were created on D drive.
6. What to do next.
