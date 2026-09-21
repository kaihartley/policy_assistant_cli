"""Load the document files and split them into chunks"""
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter

from policy_assistant.config import DOCS_DIR


def load_documents(docs_dir: Path = DOCS_DIR) -> list[Document]:
    docs_dir = Path(docs_dir)
    
    if not docs_dir.is_dir():
        raise FileNotFoundError(f"Documents directory not found: {docs_dir}")
    paths = sorted(p for p in docs_dir.iterdir() if p.suffix in {".md", ".txt"})
    return [
        Document(page_content=p.read_text(encoding="utf-8"), metadata={"source": p.name})
        for p in paths
    ]


def split_documents(docs: list[Document]) -> list[Document]:
    """Split each document by its headings, one chunk per section"""
    splitter = MarkdownHeaderTextSplitter(
        [("#", "title"), ("##", "section")],
        strip_headers=False,
    )

    chunks: list[Document] = []
    for doc in docs:
        for chunk in splitter.split_text(doc.page_content):
            chunk.metadata["source"] = doc.metadata["source"]
            chunks.append(chunk)
    return chunks


def load_chunks(docs_dir: Path = DOCS_DIR) -> list[Document]:
    return split_documents(load_documents(docs_dir))
