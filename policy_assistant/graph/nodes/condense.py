""" Turn a follow-up question into a standalone one """

from policy_assistant.chains import build_condense_chain
from policy_assistant.graph.state import AgentState


def condense(state: AgentState) -> dict:
    """ "is that the same for members?" -> "Is the 45-day return window the same for members?" """
    question = build_condense_chain().invoke({"history": state["messages"]}).strip()
    return {"question": question, "query": question}
