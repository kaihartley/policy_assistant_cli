""" Nodes for phase 1 of the graph: intake the user's question """

from langchain_core.messages import HumanMessage

from policy_assistant.graph.state import AgentState


def intake(state: AgentState) -> dict:
    """ Start of a question: take the latest user message and reset the per-question fields. """
    last_user = next(m for m in reversed(state["messages"]) if isinstance(m, HumanMessage))
    question = last_user.content if isinstance(last_user.content, str) else str(last_user.content)

    # None tells the accumulating fields to clear themselves
    return {
        "question": question,
        "query": question,
        "queries": None,
        "retrieved": None,
        "attempts": 0,
        "best_score": 0.0,
    }
