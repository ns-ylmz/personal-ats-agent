import os
from typing import Optional
from .llm_provider import LLMProvider, JobAnalysisResult, MasterProfile
from google import genai
from google.genai import types

class GeminiProvider(LLMProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        self.client = genai.Client(api_key=self.api_key)

    def analyze_job(self, cv_text: str, job_description: str, past_feedback: str = "") -> JobAnalysisResult:
        feedback_section = ""
        if past_feedback:
            feedback_section = f"""
Past Interview Feedback Context:
Focus on addressing these past interview weaknesses and areas of improvement when generating prep questions.
{past_feedback}
"""

        prompt = f"""
Analyze the following CV against the given job description.

{feedback_section}

CV:
{cv_text}

Job Description:
{job_description}
"""
        
        response = self.client.models.generate_content(
            model='gemini-3.8-flash',
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
        prompt = f"""
Extract the core professional profile from the following CV.

CV:
{cv_text}
"""
        response = self.client.models.generate_content(
            model='gemini-3.8-flash',
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
        prompt = f"""
You are an expert recruiter. The following text is scraped from a job board website.
It contains a lot of noise (footers, similar jobs, cookie policies, company boilerplate, etc.).

Your task is to extract ONLY the relevant information about the job itself:
- Job Title and Location
- Job Definition / Role Summary
- Key Responsibilities
- Requirements / Qualifications
- Cultural Fit / Perks (if highly relevant)

Do NOT include:
- "Similar Jobs" or "People also viewed"
- Website navigation menus, footers, or legal boilerplate
- Irrelevant company marketing fluff

Return the cleaned text formatted clearly. Do not use JSON, just return plain readable text.

Raw Text:
{raw_text}
"""
        response = self.client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt,
        )
        
        if not response.text:
            return raw_text # Fallback to raw text if it fails
            
        return response.text
