from __future__ import annotations

import os
from pathlib import Path

from pydantic import BaseModel


class Settings(BaseModel):
    """Runtime settings loaded from environment variables."""

    project_root: Path = Path("D:/codex_project/Domain-Adaptive Agentic GraphRAG Platform")
    data_dir: Path = Path("D:/codex_project/Domain-Adaptive Agentic GraphRAG Platform/data")
    cache_dir: Path = Path("D:/codex_project/Domain-Adaptive Agentic GraphRAG Platform/.cache")
    model_cache_dir: Path = Path("D:/codex_project/Domain-Adaptive Agentic GraphRAG Platform/.models")
    sqlite_path: Path = Path("D:/codex_project/Domain-Adaptive Agentic GraphRAG Platform/data/sqlite/app.db")
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "please_change_me"
    llm_provider: str = "mock"
    llm_base_url: str = ""
    llm_api_key: str = ""
    llm_model: str = "mock"
    embedding_provider: str = "hashing"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"


def get_settings() -> Settings:
    """Read settings from environment variables with D-drive defaults."""

    return Settings(
        project_root=Path(os.getenv("PROJECT_ROOT", Settings.model_fields["project_root"].default)),
        data_dir=Path(os.getenv("DATA_DIR", Settings.model_fields["data_dir"].default)),
        cache_dir=Path(os.getenv("CACHE_DIR", Settings.model_fields["cache_dir"].default)),
        model_cache_dir=Path(os.getenv("MODEL_CACHE_DIR", Settings.model_fields["model_cache_dir"].default)),
        sqlite_path=Path(os.getenv("SQLITE_PATH", Settings.model_fields["sqlite_path"].default)),
        qdrant_host=os.getenv("QDRANT_HOST", "localhost"),
        qdrant_port=int(os.getenv("QDRANT_PORT", "6333")),
        neo4j_uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        neo4j_user=os.getenv("NEO4J_USER", "neo4j"),
        neo4j_password=os.getenv("NEO4J_PASSWORD", "please_change_me"),
        llm_provider=os.getenv("LLM_PROVIDER", "mock"),
        llm_base_url=os.getenv("LLM_BASE_URL", ""),
        llm_api_key=os.getenv("LLM_API_KEY", ""),
        llm_model=os.getenv("LLM_MODEL", "mock"),
        embedding_provider=os.getenv("EMBEDDING_PROVIDER", "hashing"),
        embedding_model=os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"),
    )
