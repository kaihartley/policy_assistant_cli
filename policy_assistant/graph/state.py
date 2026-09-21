""" State that will be used by every node in our graph """

from typing import TypedDict, Annotated
from langchain_core.documents import Document
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

from policy_assistant.graph.reducers import accumulate, merge_docs


class AgentState(TypedDict):

    # input
    messages: Annotated[list[AnyMessage], add_messages]

    # intake
    question: str

    # retrieval
    query: str
    queries: Annotated[list[str], accumulate]
    retrieved: Annotated[list[Document], merge_docs]
    attempts: int
    best_score: float
