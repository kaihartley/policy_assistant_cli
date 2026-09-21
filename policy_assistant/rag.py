""" retrieved passages in the prompt and checking citations """

from langchain_core.documents import Document

from policy_assistant.schemas.answer import Answer


def format_docs(docs: list[Document]) -> str:
    """ Turn the retrieved docs into the passage text for the prompt, labelled by source """
    if not docs:
        return "(no passages were found)"

    blocks = []
    for doc in docs:
        meta = doc.metadata
        header = f"source: {meta.get('source', 'unknown')}"
        if meta.get("section"):
            header += f" | section: {meta['section']}"
        blocks.append(f"--- {header} ---\n{doc.page_content.strip()}")

    return "\n\n".join(blocks)


def enforce_grounding(answer: Answer, docs: list[Document]) -> Answer:
    """ Drop citations that were not retrieved; with none left, the answer is ungrounded """
    known = {doc.metadata.get("source") for doc in docs}
    valid_citations = [s for s in answer.sources if s in known]

    if not answer.grounded or not valid_citations:
        return answer.model_copy(update={"grounded": False, "answer": "", "sources": []})
    return answer.model_copy(update={"sources": valid_citations})
