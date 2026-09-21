""" Reducers: how a state field combines its old value with what a node returns """

from typing import Optional
from langchain_core.documents import Document


def accumulate(old: list, new: Optional[list]) -> list:
    """ Reducer: append new items to the old ones instead of overwriting them.

        Passing None clears the list. The intake node does that once at the start
        of every question so evidence from a previous question does not leak in.
    """
    if new is None:
        return []
    return old + new


def merge_docs(old: list[Document], new: Optional[list[Document]]) -> list[Document]:
    """ Reducer: like accumulate, but a chunk found twice is only kept once. """
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
