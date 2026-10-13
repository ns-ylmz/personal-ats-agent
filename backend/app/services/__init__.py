import logging
import os

from .fallback_provider import FallbackLLMProvider
from .gemini_provider import GeminiProvider
from .llm_provider import LLMProvider
from .ollama_provider import OllamaProvider
from .openai_provider import OpenAIProvider

logger = logging.getLogger(__name__)


def get_llm_provider() -> LLMProvider:
    primary_name = os.getenv("LLM_PROVIDER", "GEMINI").upper()
    enable_fallback = os.getenv("ENABLE_FALLBACK", "true").lower() in ("true", "1", "yes")

    providers = []

    # 1. Initialize primary provider
    try:
        if primary_name == "GEMINI":
            providers.append(GeminiProvider())
        elif primary_name == "OPENAI":
            providers.append(OpenAIProvider())
        elif primary_name == "OLLAMA":
            providers.append(OllamaProvider())
        else:
            logger.warning(f"Unknown primary LLM_PROVIDER: {primary_name}")
    except Exception as e:
        logger.warning(f"Could not initialize primary provider '{primary_name}': {e}")

    # 2. Add fallback provider (Ollama) if enabled and primary is not already Ollama
    if enable_fallback and primary_name != "OLLAMA":
        try:
            providers.append(OllamaProvider())
        except Exception as e:
            logger.warning(f"Could not initialize fallback OllamaProvider: {e}")

    if not providers:
        raise RuntimeError("No LLM providers could be initialized. Please check your configuration.")

    if len(providers) == 1:
        return providers[0]

    return FallbackLLMProvider(providers)
