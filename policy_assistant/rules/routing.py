""" Routing decisions. Pure functions of the state """

from typing import Literal

from langchain_core.messages import HumanMessage

from policy_assistant.config import DEFAULT_RETRIEVER_THRESHOLD, MAX_ATTEMPTS
from policy_assistant.graph.state import AgentState


def route_after_intake(state: AgentState) -> Literal["condense", "retrieve"]:
    """ A follow-up (not the first user turn) has to be made standalone before searching. """
    user_turns = sum(isinstance(m, HumanMessage) for m in state["messages"])
    return "condense" if user_turns > 1 else "retrieve"


def route_after_retrieve(state: AgentState) -> Literal["generate", "reframe", "refuse"]:
    """ results -> answer. Weak results -> retry while attempts remain, otherwise refuse.

        This is what bounds the retry cycle: attempts only goes up to MAX_ATTEMPTS.
    """
    if state["best_score"] >= DEFAULT_RETRIEVER_THRESHOLD:
        return "generate"
    if state["attempts"] < MAX_ATTEMPTS:
        return "reframe"
    return "refuse"
