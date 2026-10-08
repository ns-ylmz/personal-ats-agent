import os
import json
import ollama
from .llm_provider import LLMProvider, JobAnalysisResult, MasterProfile

class OllamaProvider(LLMProvider):
    def __init__(self, model: str = "llama3"):
        self.model = os.getenv("OLLAMA_MODEL", model)

    def analyze_job(self, cv_text: str, job_description: str, past_feedback: str = "") -> JobAnalysisResult:
        feedback_section = ""
        if past_feedback:
            feedback_section = f"""
Past Interview Feedback Context:
Focus on addressing these past interview weaknesses and areas of improvement when generating prep questions.
{past_feedback}
"""

        schema = JobAnalysisResult.schema_json()

        prompt = f"""
You are an expert ATS (Applicant Tracking System) and career coach.
Analyze the following CV against the given job description.

{feedback_section}

CV:
{cv_text}

Job Description:
{job_description}

You must respond in strictly valid JSON format matching this schema:
{schema}
"""
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            format='json'
        )
        
        if not response or 'response' not in response:
            raise ValueError("Empty response from Ollama API.")
            
        return JobAnalysisResult.model_validate_json(response['response'])

    def extract_master_profile(self, cv_text: str) -> MasterProfile:
        schema = MasterProfile.schema_json()
        
        prompt = f"""
Extract the core professional profile from the following CV.

CV:
{cv_text}

You must respond in strictly valid JSON format matching this schema:
{schema}
"""
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            format='json'
        )
        
        if not response or 'response' not in response:
            raise ValueError("Empty response from Ollama API.")
            
        return MasterProfile.model_validate_json(response['response'])

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
        response = ollama.generate(
            model=self.model,
            prompt=prompt
        )
        
        if not response or 'response' not in response:
            return raw_text # Fallback
            
        return response['response']
