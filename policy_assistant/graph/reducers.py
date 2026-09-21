""" How state fields combine old and new values """

from typing import Optional
from langchain_core.documents import Document


def accumulate(old: list, new: Optional[list]) -> list:
    """ Append new items; None clears the list """
    if new is None:
        return []
    return old + new


def merge_docs(old: list[Document], new: Optional[list[Document]]) -> list[Document]:
    """ Like accumulate, without duplicate chunks """
    if new is None:
        return []
    seen = {(d.metadata.get("source"), d.page_content) for d in old}
    merged = list(old)
    for doc in new:
        key = (doc.metadata.get("source"), doc.page_content)
        if key not in seen:
            seen.add(key)
            merged.append(doc)
    return merged
