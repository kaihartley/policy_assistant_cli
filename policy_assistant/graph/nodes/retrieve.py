""" Search the document index """

from policy_assistant.config import DEFAULT_RETRIEVER_K, DEFAULT_RETRIEVER_THRESHOLD
from policy_assistant.graph.state import AgentState
from policy_assistant.models.retriever import search


def retrieve(state: AgentState) -> dict:
    """ One search. Uses search() rather than the retriever because the routing needs the scores. """
    hits = search(state["query"], k=DEFAULT_RETRIEVER_K)

    return {
        "queries": [state["query"]],
        # only chunks that clear the threshold count as evidence
        "retrieved": [doc for doc, score in hits if score >= DEFAULT_RETRIEVER_THRESHOLD],
        "attempts": state["attempts"] + 1,
        "best_score": hits[0][1] if hits else 0.0,
    }
