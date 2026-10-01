from pydantic import BaseModel
from typing import Optional, List

class JobAnalyzeRequest(BaseModel):
    cv_text: str
    job_description: str

class JobStatusResponse(BaseModel):
    id: int
    status: str
    match_score: Optional[int] = None
    cover_letter: Optional[str] = None
    prep_questions: Optional[List[str]] = None

    class Config:
        from_attributes = True

class JobStatusUpdate(BaseModel):
    status: str

class InterviewFeedbackCreate(BaseModel):
    feedback_text: str

class InterviewFeedbackResponse(BaseModel):
    id: int
    job_id: int
    feedback_text: str

    class Config:
        from_attributes = True
