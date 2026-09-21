""" The way out when the documents do not cover the question """

from langchain_core.messages import AIMessage

from policy_assistant.config import REFUSAL_MESSAGE
from policy_assistant.graph.state import AgentState


def refuse(state: AgentState) -> dict:
    return {"messages": [AIMessage(content=REFUSAL_MESSAGE)]}
