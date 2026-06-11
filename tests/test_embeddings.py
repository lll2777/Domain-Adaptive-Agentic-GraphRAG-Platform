from app.core.embeddings import HashingEmbeddingModel, SentenceTransformerEmbeddingModel, build_embedding_model


def test_build_embedding_model_uses_hashing_fallback_when_sentence_transformer_unavailable(monkeypatch) -> None:
    def raise_import_error(*args, **kwargs):
        raise ImportError("not installed")

    monkeypatch.setattr("app.core.embeddings.SentenceTransformerEmbeddingModel", raise_import_error)

    model = build_embedding_model("sentence-transformers", dimensions=16)

    assert isinstance(model, HashingEmbeddingModel)
    assert len(model.embed("GraphRAG retrieval")) == 16


def test_sentence_transformer_adapter_normalizes_embedding_from_injected_model() -> None:
    class FakeModel:
        def encode(self, text: str):
            return [3.0, 4.0]

    model = SentenceTransformerEmbeddingModel(model=FakeModel())

    assert model.embed("GraphRAG") == [0.6, 0.8]
