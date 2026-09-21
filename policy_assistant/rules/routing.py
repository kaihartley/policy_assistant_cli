""" Routing decisions. Pure functions of the state """

from typing import Literal

from langchain_core.messages import HumanMessage

from policy_assistant.config import DEFAULT_RETRIEVER_THRESHOLD, MAX_ATTEMPTS
from policy_assistant.graph.state import AgentState


def route_after_intake(state: AgentState) -> Literal["condense", "retrieve"]:
    """ Follow-up questions are made standalone before searching """
    user_turns = sum(isinstance(m, HumanMessage) for m in state["messages"])
    return "condense" if user_turns > 1 else "retrieve"


def route_after_retrieve(state: AgentState) -> Literal["generate", "reframe", "refuse"]:
    """ Good results answer; weak results retry until MAX_ATTEMPTS, then refuse """
    if state["best_score"] >= DEFAULT_RETRIEVER_THRESHOLD:
        return "generate"
    if state["attempts"] < MAX_ATTEMPTS:
        return "reframe"
    return "refuse"
