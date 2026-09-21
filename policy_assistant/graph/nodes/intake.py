""" Take in the user's question """

from langchain_core.messages import HumanMessage

from policy_assistant.graph.state import AgentState


def intake(state: AgentState) -> dict:
    last_user = next(m for m in reversed(state["messages"]) if isinstance(m, HumanMessage))
    question = last_user.content if isinstance(last_user.content, str) else str(last_user.content)

    # None clears the accumulating fields
    return {
        "question": question,
        "query": question,
        "queries": None,
        "retrieved": None,
        "attempts": 0,
        "best_score": 0.0,
    }
