from pydantic import BaseModel, Field


class Answer(BaseModel):
    """ A policy answer grounded in the reference passages provided.

        Answer ONLY from the passages. The passages are the company's policy;
        your general knowledge is NOT a source and must not fill a gap.

        If the passages do not cover the situation, say so by setting
        `grounded` to false rather than producing a plausible answer.
    """

    grounded: bool = Field(
        description=(
            "True only if the passages directly support the answer. "
            "False if the question is not covered or you would have to guess."
        )
    )

    answer: str = Field(
        default="",
        description=(
            "The answer, quoting figures (days, percentages, prices) exactly as written, "
            "with the source file in square brackets after each claim, e.g. [refund-policy.md]. "
            "Empty when grounded is false."
        )
    )

    sources: list[str] = Field(
        description=(
            "The exact file names you used, copied from the 'source:' line of each passage. "
            "If you used none, return an empty list. Ex: []"
        )
    )
