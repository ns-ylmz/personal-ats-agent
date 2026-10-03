import threading
import queue
import time
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

job_queue = queue.Queue()

def worker_loop():
    logger.info("Worker thread started.")
    from app.database import SessionLocal
    from app import models
    from app.services import get_llm_provider
    import json
    
    while True:
        try:
            job_id = job_queue.get()
            if job_id is None:  # Poison pill to stop the thread
                logger.info("Worker thread stopping.")
                break
            
            logger.info(f"Processing job_id: {job_id}")
            
            # Fetch job from db
            db = SessionLocal()
            try:
                job = db.query(models.Job).filter(models.Job.id == job_id).first()
                if job:
                    # Fetch all past interview feedback to inject as minimal RAG
                    feedbacks = db.query(models.InterviewFeedback).all()
                    past_feedback_text = "\n".join([f"- {f.feedback_text}" for f in feedbacks])
                    
                    # Resolve job description (scrape if URL)
                    job_desc_text = job.job_description
                    if job_desc_text.startswith("http://") or job_desc_text.startswith("https://"):
                        from app.services.scraper import scrape_job_description
                        logger.info(f"Job description is a URL. Scraping: {job_desc_text}")
                        job_desc_text = scrape_job_description(job_desc_text)
                    
                    # Process with LLM
                    provider = get_llm_provider()
                    result = provider.analyze_job(job.cv_text, job_desc_text, past_feedback=past_feedback_text)
                    
                    # Update job
                    job.match_score = result.match_score
                    job.cover_letter = result.cover_letter
                    job.prep_questions = json.dumps(result.prep_questions)
                    job.status = "COMPLETED"
                    db.commit()
                    logger.info(f"Job {job_id} processed successfully.")
                else:
                    logger.error(f"Job {job_id} not found in database.")
            except Exception as inner_e:
                logger.error(f"Error executing LLM for job {job_id}: {inner_e}")
                if 'job' in locals() and job:
                    job.status = "FAILED"
                    db.commit()
            finally:
                db.close()
            
            job_queue.task_done()
        except Exception as e:
            logger.error(f"Error processing job queue: {e}")

def start_worker():
    thread = threading.Thread(target=worker_loop, daemon=True)
    thread.start()
    return thread
