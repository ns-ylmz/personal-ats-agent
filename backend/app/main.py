from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine
from app import models
from app.worker import start_worker, job_queue
from app.api import jobs

# Create database tables
models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start the worker thread
    thread = start_worker()
    yield
    # Shutdown: Stop the worker thread gracefully
    job_queue.put(None)
    thread.join(timeout=5)

app = FastAPI(title="Personal ATS Agent API", lifespan=lifespan)

app.include_router(jobs.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

