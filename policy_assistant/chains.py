""" The LLM steps as small chains: prompt | model (| parser).

    Each builder takes an optional chat model. Leave it out to use Bedrock;
    pass a stub in tests so nothing touches AWS.
"""

from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable

from policy_assistant.prompts import ANSWER_PROMPT, CONDENSE_PROMPT, REFRAME_PROMPT
from policy_assistant.models.chat import get_chat_model
from policy_assistant.schemas.answer import Answer


def build_condense_chain(model: BaseChatModel | None = None) -> Runnable:
    """ input: {"history": [messages]}  ->  standalone question (str) """
    prompt = ChatPromptTemplate.from_messages([
        ("system", CONDENSE_PROMPT),
        MessagesPlaceholder("history"),
    ])
    return prompt | (model or get_chat_model()) | StrOutputParser()


def build_reframe_chain(model: BaseChatModel | None = None) -> Runnable:
    """ input: {"question": str, "tried": str}  ->  new search query (str) """
    prompt = ChatPromptTemplate.from_messages([
        ("system", REFRAME_PROMPT),
        ("human", "Question: {question}\nQueries already tried: {tried}"),
    ])
    return prompt | (model or get_chat_model()) | StrOutputParser()


def build_answer_chain(model: BaseChatModel | None = None) -> Runnable:
    """ input: {"context": str, "question": str}  ->  Answer """
    prompt = ChatPromptTemplate.from_messages([
        ("system", ANSWER_PROMPT),
        ("human", "{question}"),
    ])

    structured_model = (model or get_chat_model()).with_structured_output(Answer)
    return prompt | structured_model
