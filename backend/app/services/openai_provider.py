import os
from typing import Optional

from openai import OpenAI

from .llm_provider import JobAnalysisResult, LLMProvider, MasterProfile
from .prompts import (
    OPENAI_ATS_SYSTEM_PROMPT,
    OPENAI_CLEAN_TEXT_SYSTEM_PROMPT,
    OPENAI_PROFILE_SYSTEM_PROMPT,
    get_analyze_job_prompt,
    get_clean_raw_job_text_prompt,
    get_extract_master_profile_prompt,
)


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not set.")
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"

    def analyze_job(self, cv_text: str, job_description: str, past_feedback: str = "") -> JobAnalysisResult:
        prompt = get_analyze_job_prompt(cv_text, job_description, past_feedback)

        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": OPENAI_ATS_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            response_format=JobAnalysisResult,
            temperature=0.2,
        )

        return completion.choices[0].message.parsed

    def extract_master_profile(self, cv_text: str) -> MasterProfile:
        prompt = get_extract_master_profile_prompt(cv_text)
        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": OPENAI_PROFILE_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            response_format=MasterProfile,
            temperature=0.1,
        )

        return completion.choices[0].message.parsed

    def clean_raw_job_text(self, raw_text: str) -> str:
        prompt = get_clean_raw_job_text_prompt(raw_text)
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": OPENAI_CLEAN_TEXT_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
        )

        return completion.choices[0].message.content or raw_text
