from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import json

from app import models, schemas
from app.database import get_db
from app.worker import job_queue

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/analyze", status_code=status.HTTP_202_ACCEPTED)
async def analyze_job(request: schemas.JobAnalyzeRequest, db: Session = Depends(get_db)):
    new_job = models.Job(
        cv_text=request.cv_text,
        job_description=request.job_description,
        status="PENDING"
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    
    # Enqueue the job ID
    job_queue.put(new_job.id)
    
    return {"message": "Job enqueued", "job_id": new_job.id}

@router.get("", response_model=list[schemas.JobStatusResponse])
async def get_all_jobs(db: Session = Depends(get_db)):
    jobs = db.query(models.Job).order_by(models.Job.id.desc()).all()
    results = []
    for job in jobs:
        prep_questions_list = None
        if job.prep_questions:
            try:
                prep_questions_list = json.loads(job.prep_questions)
            except:
                prep_questions_list = []
        results.append(schemas.JobStatusResponse(
            id=job.id,
            status=job.status,
            job_description=job.job_description,
            match_score=job.match_score,
            cover_letter=job.cover_letter,
            prep_questions=prep_questions_list
        ))
    return results

@router.get("/{job_id}", response_model=schemas.JobStatusResponse)
async def get_job_status(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Parse JSON list back for response if available
    prep_questions_list = None
    if job.prep_questions:
        try:
            prep_questions_list = json.loads(job.prep_questions)
        except:
            prep_questions_list = []

    return schemas.JobStatusResponse(
        id=job.id,
        status=job.status,
        job_description=job.job_description,
        match_score=job.match_score,
        cover_letter=job.cover_letter,
        prep_questions=prep_questions_list
    )

@router.patch("/{job_id}/status", response_model=schemas.JobStatusResponse)
async def update_job_status(job_id: int, request: schemas.JobStatusUpdate, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    job.status = request.status
    db.commit()
    db.refresh(job)
    
    prep_questions_list = None
    if job.prep_questions:
        try:
            prep_questions_list = json.loads(job.prep_questions)
        except:
            prep_questions_list = []
            
    return schemas.JobStatusResponse(
        id=job.id,
        status=job.status,
        job_description=job.job_description,
        match_score=job.match_score,
        cover_letter=job.cover_letter,
        prep_questions=prep_questions_list
    )

@router.post("/{job_id}/feedback", response_model=schemas.InterviewFeedbackResponse, status_code=status.HTTP_201_CREATED)
async def add_interview_feedback(job_id: int, request: schemas.InterviewFeedbackCreate, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    feedback = models.InterviewFeedback(
        job_id=job_id,
        feedback_text=request.feedback_text
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    
    return feedback
