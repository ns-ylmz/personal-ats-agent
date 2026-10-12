import os
import json
import ollama
from .llm_provider import LLMProvider, JobAnalysisResult, MasterProfile
from .prompts import (
    get_analyze_job_prompt,
    get_clean_raw_job_text_prompt,
    get_extract_master_profile_prompt,
)

class OllamaProvider(LLMProvider):
    def __init__(self, model: str = "llama3"):
        self.model = os.getenv("OLLAMA_MODEL", model)

    def analyze_job(self, cv_text: str, job_description: str, past_feedback: str = "") -> JobAnalysisResult:
        prompt = get_analyze_job_prompt(
            cv_text,
            job_description,
            past_feedback,
            include_role_preamble=True,
            include_suffix_instructions=True,
        )
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            format=JobAnalysisResult.model_json_schema()
        )
        
        if not response or 'response' not in response:
            raise ValueError("Empty response from Ollama API.")
            
        return JobAnalysisResult.model_validate_json(response['response'])

    def extract_master_profile(self, cv_text: str) -> MasterProfile:
        prompt = get_extract_master_profile_prompt(cv_text, include_suffix_instructions=True)
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            format=MasterProfile.model_json_schema()
        )
        
        if not response or 'response' not in response:
            raise ValueError("Empty response from Ollama API.")
            
        return MasterProfile.model_validate_json(response['response'])

    def clean_raw_job_text(self, raw_text: str) -> str:
        prompt = get_clean_raw_job_text_prompt(raw_text)
        response = ollama.generate(
            model=self.model,
            prompt=prompt
        )
        
        if not response or 'response' not in response:
            return raw_text # Fallback
            
        return response['response']
