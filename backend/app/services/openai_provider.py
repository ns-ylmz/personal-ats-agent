import os
from typing import Optional
from .llm_provider import LLMProvider, JobAnalysisResult, MasterProfile
from openai import OpenAI

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not set.")
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"

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
        
        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert ATS and career coach. Please output JSON according to the schema."},
                {"role": "user", "content": prompt}
            ],
            response_format=JobAnalysisResult,
            temperature=0.2,
        )
        
        return completion.choices[0].message.parsed

    def extract_master_profile(self, cv_text: str) -> MasterProfile:
        prompt = f"""
Extract the core professional profile from the following CV.

CV:
{cv_text}
"""
        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert recruiter parsing a CV into a structured master profile."},
                {"role": "user", "content": prompt}
            ],
            response_format=MasterProfile,
            temperature=0.1,
        )
        
        return completion.choices[0].message.parsed

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
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert recruiter cleaning up scraped HTML text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
        )
        
        return completion.choices[0].message.content or raw_text
