import os
from .llm_provider import LLMProvider

def get_llm_provider() -> LLMProvider:
    provider = os.getenv("LLM_PROVIDER", "GEMINI").upper()
    
    if provider == "GEMINI":
        from .gemini_provider import GeminiProvider
        return GeminiProvider()
    elif provider == "OLLAMA":
        raise NotImplementedError("OllamaProvider is not yet implemented.")
    else:
        raise ValueError(f"Unknown LLM_PROVIDER: {provider}")
