import os
from .llm_provider import LLMProvider, JobAnalysisResult
from google import genai
from google.genai import types

class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        self.client = genai.Client(api_key=self.api_key)

    def analyze_job(self, cv_text: str, job_description: str) -> JobAnalysisResult:
        prompt = f"""
Analyze the following CV against the given job description.

CV:
{cv_text}

Job Description:
{job_description}
"""
        
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
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
