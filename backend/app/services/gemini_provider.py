import os
from typing import Optional

from google import genai
from google.genai import types

from .llm_provider import JobAnalysisResult, LLMProvider, MasterProfile
from .prompts import (
    get_analyze_job_prompt,
    get_clean_raw_job_text_prompt,
    get_extract_master_profile_prompt,
)


class GeminiProvider(LLMProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        self.client = genai.Client(api_key=self.api_key)

    def analyze_job(self, cv_text: str, job_description: str, past_feedback: str = "") -> JobAnalysisResult:
        prompt = get_analyze_job_prompt(cv_text, job_description, past_feedback)

        response = self.client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=JobAnalysisResult,
                temperature=0.2,
            ),
        )

        if not response.text:
            raise ValueError("Empty response from Gemini API.")

        return JobAnalysisResult.model_validate_json(response.text)

    def extract_master_profile(self, cv_text: str) -> MasterProfile:
        prompt = get_extract_master_profile_prompt(cv_text)
        response = self.client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=MasterProfile,
                temperature=0.1,
            ),
        )

        if not response.text:
            raise ValueError("Empty response from Gemini API.")

        return MasterProfile.model_validate_json(response.text)

    def clean_raw_job_text(self, raw_text: str) -> str:
        prompt = get_clean_raw_job_text_prompt(raw_text)
        response = self.client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
        )

        if not response.text:
            return raw_text  # Fallback to raw text if it fails

        return response.text
