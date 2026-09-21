from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore

from policy_assistant.config import DEFAULT_RETRIEVER_K
from policy_assistant.ingest.index import get_local_store


def search(
    query: str,
    *,
    k: int = DEFAULT_RETRIEVER_K,
    store: InMemoryVectorStore | None = None,
) -> list[tuple[Document, float]]:
    """ Top-k (chunk, similarity) pairs, best first """
    store = store or get_local_store()
    return store.similarity_search_with_score(query, k=k)


if __name__ == "__main__":
    for q in [
        "How long does a customer have to return an item, and is there a fee?",
        "How long do I have to send something back?",
        "What is the company's parental leave policy?",
    ]:
        print(q)
        for doc, score in search(q, k=3):
            print(f"   {score:.3f}  {doc.metadata['source']} | {doc.metadata.get('section')}")
