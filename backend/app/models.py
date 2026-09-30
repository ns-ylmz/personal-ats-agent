from sqlalchemy import Column, Integer, String, Text

from app.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    cv_text = Column(Text, nullable=False)
    job_description = Column(Text, nullable=False)
    status = Column(String, default="PENDING", index=True)  # PENDING, COMPLETED, FAILED
    
    # Results (populated when COMPLETED)
    match_score = Column(Integer, nullable=True)
    cover_letter = Column(Text, nullable=True)
    prep_questions = Column(Text, nullable=True)  # Stored as JSON string

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    skills = Column(Text, nullable=False)  # Stored as JSON string
    experience_summary = Column(Text, nullable=False)

