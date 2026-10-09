from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    cv_text = Column(Text, nullable=False)
    job_description = Column(Text, nullable=False)
    status = Column(String, default="PENDING", index=True)  # PENDING, COMPLETED, FAILED, INTERVIEWING, REJECTED, OFFER
    
    # Results (populated when COMPLETED)
    match_score = Column(Integer, nullable=True)
    cover_letter = Column(Text, nullable=True)
    prep_questions = Column(Text, nullable=True)  # Stored as JSON string

    # Relationships
    feedbacks = relationship("InterviewFeedback", back_populates="job", cascade="all, delete-orphan")

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    raw_cv_text = Column(Text, nullable=True) # Full text extracted from PDF
    skills = Column(Text, nullable=False)  # Stored as JSON string
    experience_summary = Column(Text, nullable=False)

class InterviewFeedback(Base):
    __tablename__ = "interview_feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    feedback_text = Column(Text, nullable=False)
    
    job = relationship("Job", back_populates="feedbacks")

