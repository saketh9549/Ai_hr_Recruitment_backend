"""
ChromaDB wrapper -- stores and searches resume/job embeddings.
"""

from functools import lru_cache

import chromadb

from app.config import settings


@lru_cache
def _get_client() -> chromadb.ClientAPI:
    return chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)


@lru_cache
def _get_collection():
    client = _get_client()
    return client.get_or_create_collection(name=settings.CHROMA_COLLECTION_NAME)


def upsert_resume_embedding(resume_id: int, embedding: list[float], metadata: dict) -> None:
    collection = _get_collection()
    collection.upsert(
        ids=[str(resume_id)],
        embeddings=[embedding],
        metadatas=[metadata],
    )


def query_similar_resumes(query_embedding: list[float], top_k: int = 10) -> list[dict]:
    collection = _get_collection()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    matches = []
    ids = results.get("ids", [[]])[0]
    distances = results.get("distances", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    for i, resume_id in enumerate(ids):
        matches.append({
            "id": int(resume_id),
            "distance": distances[i],
            "metadata": metadatas[i],
        })
    return matches


def delete_resume_embedding(resume_id: int) -> None:
    collection = _get_collection()
    collection.delete(ids=[str(resume_id)])
