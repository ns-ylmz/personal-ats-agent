from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import List

class JobAnalysisResult(BaseModel):
    match_score: int = Field(description="Score out of 100 indicating how well the CV matches the job.")
    cover_letter: str = Field(description="A professional cover letter written for this job.")
    prep_questions: List[str] = Field(description="Interview preparation questions based on the job and CV.")

class LLMProvider(ABC):
    @abstractmethod
    def analyze_job(self, cv_text: str, job_description: str) -> JobAnalysisResult:
        """Analyzes a job description against a CV and returns structured results."""
        pass
