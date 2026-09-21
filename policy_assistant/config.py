import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


MODEL_REGION = os.environ.get("AWS_REGION")
CHAT_MODEL_ID = os.environ.get("BEDROCK_MODEL_ID")
DEFAULT_MAX_TOKENS = int(os.environ.get("BEDROCK_MAX_TOKENS", "600"))
EMBED_MODEL_ID = os.environ.get("EMBED_MODEL_ID")

DOCS_DIR = Path(__file__).resolve().parents[1] / "kb-documents"

DEFAULT_RETRIEVER_K = 5
# Minimum cosine similarity for a chunk to count as relevant. Measured with Titan:
# covered questions scored 0.36-0.43 and the uncovered one 0.17, so 0.30 sits between them.
DEFAULT_RETRIEVER_THRESHOLD = 0.30
# Total searches allowed per user question (the first try plus retries).
MAX_ATTEMPTS = 3

REFUSAL_MESSAGE = (
    "I don't know. I couldn't find anything in the policy documents that answers that question."
)
