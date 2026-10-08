from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import List

class JobAnalysisResult(BaseModel):
    match_score: int = Field(description="Score out of 100 indicating how well the CV matches the job.")
    cover_letter: str = Field(description="A professional cover letter written for this job.")
    prep_questions: List[str] = Field(description="Interview preparation questions based on the job and CV.")

class MasterProfile(BaseModel):
    skills: List[str] = Field(description="List of professional skills extracted from the CV.")
    experience_summary: str = Field(description="A brief summary of the candidate's professional experience.")

class LLMProvider(ABC):
    @abstractmethod
    def analyze_job(self, cv_text: str, job_description: str, past_feedback: str = "") -> JobAnalysisResult:
        """Analyzes a job description against a CV and returns structured results."""
        pass
    
    @abstractmethod
    def extract_master_profile(self, cv_text: str) -> MasterProfile:
        """Extracts structured Master Profile (skills, experience) from a raw CV text."""
        pass
        
    @abstractmethod
    def clean_raw_job_text(self, raw_text: str) -> str:
        """Cleans raw scraped HTML text to extract only Job Definition, Requirements, and Cultural Fit."""
        pass
