"""Build the in-memory vector index from the document files.

    The index is built when the program starts and disappears when it stops.
"""
from functools import lru_cache
from pathlib import Path

from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore

from policy_assistant.config import DOCS_DIR
from policy_assistant.ingest.loader import load_chunks
from policy_assistant.models.embed import get_embed_model


def build_store(
    embeddings: Embeddings | None = None,
    docs_dir: Path = DOCS_DIR,
) -> InMemoryVectorStore:
    """Load, split and embed the documents into a fresh in-memory store.

    Pass fake `embeddings` in tests so nothing touches AWS.
    """
    store = InMemoryVectorStore(embedding=embeddings or get_embed_model())
    store.add_documents(load_chunks(docs_dir))
    return store


@lru_cache(maxsize=1)
def get_local_store() -> InMemoryVectorStore:
    """The process-wide index. Built on first use, gone when the program exits."""
    return build_store()
