from functools import lru_cache
from policy_assistant.config import EMBED_MODEL_ID, MODEL_REGION
from langchain_core.embeddings import Embeddings
from langchain_aws import BedrockEmbeddings


@lru_cache(maxsize=1)
def get_embed_model() -> Embeddings:
    if not EMBED_MODEL_ID or not MODEL_REGION:
        raise RuntimeError("Set AWS_REGION and EMBED_MODEL_ID in your environment (see .env.example).")
    return BedrockEmbeddings(
        model_id=EMBED_MODEL_ID,
        region_name=MODEL_REGION,
    )
