""" The retry step: a weak search gets a reworded query """

from policy_assistant.chains import build_reframe_chain
from policy_assistant.graph.state import AgentState


def reframe(state: AgentState) -> dict:
    """ Ask the model for a broader query, telling it what has already failed. """
    new_query = build_reframe_chain().invoke({
        "question": state["question"],
        "tried": "; ".join(state["queries"]),
    })
    return {"query": new_query.strip()}
