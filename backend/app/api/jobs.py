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
        match_score=job.match_score,
        cover_letter=job.cover_letter,
        prep_questions=prep_questions_list
    )
