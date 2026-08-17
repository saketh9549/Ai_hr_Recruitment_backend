"""
Embedding service -- turns text into vectors for semantic comparison.

Uses sentence-transformers locally (free, no API cost per call) rather
than an embeddings API. Model loads once per process via functools.cache.
"""

from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app.config import settings


@lru_cache
def _get_model() -> SentenceTransformer:
    return SentenceTransformer(settings.EMBEDDING_MODEL)


def embed_text(text: str) -> list[float]:
    """Generate one embedding vector. Raises ValueError on empty input."""
    if not text or not text.strip():
        raise ValueError("Cannot embed empty text")
    vector = _get_model().encode(text, normalize_embeddings=True)
    return vector.tolist()


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Batch embedding -- faster than calling embed_text in a loop."""
    if not texts:
        return []
    vectors = _get_model().encode(texts, normalize_embeddings=True, batch_size=32)
    return [v.tolist() for v in vectors]


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """
    Manual cosine similarity (vectors are already normalized by embed_text,
    so this is just a dot product). Used by matcher.py to score resume-job
    similarity without needing a full vector DB round trip for a single pair.
    """
    return sum(a * b for a, b in zip(vec_a, vec_b))
