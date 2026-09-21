""" Answer from the retrieved passages """

from langchain_core.messages import AIMessage

from policy_assistant.chains import build_answer_chain
from policy_assistant.config import REFUSAL_MESSAGE
from policy_assistant.graph.state import AgentState
from policy_assistant.rag import enforce_grounding, format_docs


def generate(state: AgentState) -> dict:
    """ Put the retrieved passages in the prompt. If the model is not grounded in them, refuse. """
    docs = state["retrieved"]

    answer = build_answer_chain().invoke({
        "context": format_docs(docs),
        "question": state["question"],
    })
    answer = enforce_grounding(answer, docs)

    if not answer.grounded:
        return {"messages": [AIMessage(content=REFUSAL_MESSAGE)]}

    text = f"{answer.answer}\n\nSources: {', '.join(answer.sources)}"
    return {"messages": [AIMessage(content=text)]}
