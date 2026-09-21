from policy_assistant.config import DOCS_DIR
from policy_assistant.loader import load_chunks, load_documents


def test_documents_load_from_files():
    docs = load_documents(DOCS_DIR)
    names = {d.metadata["source"] for d in docs}
    assert {"refund-policy.md", "shipping-policy.md", "account-and-billing.md", "known-issues.md"} <= names
    assert all(d.page_content.strip() for d in docs)


def test_documents_split_into_sections():
    chunks = load_chunks(DOCS_DIR)
    refund_sections = {c.metadata.get("section") for c in chunks if c.metadata["source"] == "refund-policy.md"}
    assert {"Standard return window", "Restocking fee", "Refund timing"} <= refund_sections


def test_every_chunk_has_a_source_and_text():
    chunks = load_chunks(DOCS_DIR)
    assert len(chunks) > 10
    assert all(c.metadata["source"].endswith(".md") and c.page_content.strip() for c in chunks)
