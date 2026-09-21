from functools import lru_cache
from policy_assistant.config import MODEL_REGION, CHAT_MODEL_ID, DEFAULT_MAX_TOKENS
from langchain_core.language_models import BaseChatModel
from langchain_aws import ChatBedrockConverse

@lru_cache(maxsize=1)
def get_chat_model(
    *,
    temperature: float = 0.0,
    max_tokens: int | None = None
) -> BaseChatModel:
    return ChatBedrockConverse(
        model=CHAT_MODEL_ID,
        region_name=MODEL_REGION,
        temperature=temperature,
        max_tokens=max_tokens or DEFAULT_MAX_TOKENS
    )
    
