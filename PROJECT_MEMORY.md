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

Repository setup.

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
