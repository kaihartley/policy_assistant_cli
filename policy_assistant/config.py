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
# A best score below this counts as a weak search
DEFAULT_RETRIEVER_THRESHOLD = 0.30
# Searches allowed per question (the first try plus retries)
MAX_ATTEMPTS = 3

REFUSAL_MESSAGE = (
    "I don't know. I couldn't find anything in the policy documents that answers that question."
)
