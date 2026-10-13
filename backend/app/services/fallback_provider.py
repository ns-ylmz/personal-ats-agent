import logging
from typing import List

from .llm_provider import JobAnalysisResult, LLMProvider, MasterProfile

logger = logging.getLogger(__name__)


class FallbackLLMProvider(LLMProvider):
    def __init__(self, providers: List[LLMProvider]):
        if not providers:
            raise ValueError("FallbackLLMProvider requires at least one provider.")
        self.providers = providers

    def analyze_job(self, cv_text: str, job_description: str, past_feedback: str = "") -> JobAnalysisResult:
        last_error = None
        for provider in self.providers:
            try:
                return provider.analyze_job(cv_text, job_description, past_feedback)
            except Exception as e:
                logger.warning(
                    f"Provider '{provider.__class__.__name__}' failed during analyze_job: {e}. "
                    "Attempting fallback to next provider..."
                )
                last_error = e
        raise RuntimeError(f"All LLM providers failed in analyze_job. Last error: {last_error}")

    def extract_master_profile(self, cv_text: str) -> MasterProfile:
        last_error = None
        for provider in self.providers:
            try:
                return provider.extract_master_profile(cv_text)
            except Exception as e:
                logger.warning(
                    f"Provider '{provider.__class__.__name__}' failed during extract_master_profile: {e}. "
                    "Attempting fallback to next provider..."
                )
                last_error = e
        raise RuntimeError(f"All LLM providers failed in extract_master_profile. Last error: {last_error}")

    def clean_raw_job_text(self, raw_text: str) -> str:
        last_error = None
        for provider in self.providers:
            try:
                return provider.clean_raw_job_text(raw_text)
            except Exception as e:
                logger.warning(
                    f"Provider '{provider.__class__.__name__}' failed during clean_raw_job_text: {e}. "
                    "Attempting fallback to next provider..."
                )
                last_error = e
        raise RuntimeError(f"All LLM providers failed in clean_raw_job_text. Last error: {last_error}")
