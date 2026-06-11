# Phase 1 Runnable Scaffold Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a runnable first-stage scaffold for the Domain-Adaptive Agentic GraphRAG Platform.

**Architecture:** The scaffold keeps domain models, configuration, ingestion adapters, retrieval, graph, agent workflow, storage, evaluation, API routes, scripts, and Streamlit UI in separate modules. First-stage implementations are lightweight and mock-friendly so the project starts without paid API keys, external model downloads, or database setup beyond optional Docker services.

**Tech Stack:** Python 3.11+, FastAPI, Pydantic, Uvicorn, Streamlit, PyYAML, pytest, requests, Qdrant/Neo4j via docker-compose.

---

### Task 1: Test-First Core Behavior

**Files:**
- Create: `tests/test_chunking.py`
- Create: `tests/test_schema.py`
- Create: `tests/test_bm25.py`
- Create: `tests/test_workflow.py`
- Create: `tests/test_citation.py`

- [ ] **Step 1: Write failing tests**

```python
def test_chunking_keeps_doc_id():
    from app.core.chunking import chunk_document
    from app.core.documents import Document

    doc = Document(doc_id="doc-1", title="Demo", text="alpha beta gamma", source="sample", domain="ai_paper")
    chunks = chunk_document(doc, chunk_size=2, overlap=0)
    assert chunks
    assert chunks[0].doc_id == "doc-1"
```

- [ ] **Step 2: Run RED**

Run: `python -m pytest tests -q`

Expected: failures because `app` modules are not implemented yet.

### Task 2: Implement Minimal Scaffold

**Files:**
- Create package directories under `app/`
- Create domain configs under `configs/domains/`
- Create scripts under `scripts/`
- Create sample data under `data/samples/` and `data/eval/`
- Create `requirements.txt`, `docker-compose.yml`, and `README.md`

- [ ] **Step 1: Create directories and module stubs**

Create every package named in the phase-1 project structure with `__init__.py` files where needed.

- [ ] **Step 2: Implement minimal tested core modules**

Implement `Document`, `Chunk`, `Entity`, `Relation`, `DomainSchema`, `chunk_document`, schema loading, `BM25Retriever`, `QueryClassifier`, `QueryWorkflow`, and `CitationChecker`.

- [ ] **Step 3: Implement runnable API and UI**

Implement FastAPI health/routes and Streamlit pages that start successfully and use mock/local behavior when services are unavailable.

- [ ] **Step 4: Run GREEN**

Run: `python -m pytest tests -q`

Expected: all tests pass.

### Task 3: Docs, Memory, Commit, Push

**Files:**
- Modify: `AGENTS.md`
- Modify: `PROJECT_MEMORY.md`
- Modify: `README.md`

- [ ] **Step 1: Update README**

Include beginner-friendly setup, D-drive cache rules, Docker commands, backend/frontend commands, sample ingest command, Mermaid diagrams, proxy metric explanation, migration notes, resume wording, and FAQ.

- [ ] **Step 2: Update memory files**

Record files touched, commands run, tests, large file status, and next steps.

- [ ] **Step 3: Verify and publish**

Run:

```powershell
python -m pytest tests -q
python -m compileall app scripts
git status --short --branch
git add .
git commit -m "feat: add runnable phase 1 scaffold"
git push
```
