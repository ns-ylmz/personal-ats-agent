from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import json

from app import models
from app.database import get_db
from app.services.pdf_service import extract_text_from_pdf
from app.services import get_llm_provider

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.post("/upload")
async def upload_master_profile(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        content = await file.read()
        cv_text = extract_text_from_pdf(content)
        
        provider = get_llm_provider()
        master_profile = provider.extract_master_profile(cv_text)
        
        # Assume single user, clear old profile if it exists or just update the first one
        profile_record = db.query(models.UserProfile).first()
        if not profile_record:
            profile_record = models.UserProfile()
            db.add(profile_record)
        
        profile_record.skills = json.dumps(master_profile.skills)
        profile_record.experience_summary = master_profile.experience_summary
        
        db.commit()
        db.refresh(profile_record)
        
        return {
            "message": "Master profile updated successfully",
            "skills": master_profile.skills,
            "experience_summary": master_profile.experience_summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_master_profile(db: Session = Depends(get_db)):
    profile_record = db.query(models.UserProfile).first()
    if not profile_record:
        raise HTTPException(status_code=404, detail="Master profile not found")
        
    skills = []
    if profile_record.skills:
        try:
            skills = json.loads(profile_record.skills)
        except:
            skills = []
            
    return {
        "skills": skills,
        "experience_summary": profile_record.experience_summary
    }
