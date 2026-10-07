import os
from dotenv import load_dotenv
load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine
from app import models
from app.worker import start_worker, job_queue
from app.api import jobs, profile

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

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Personal ATS Agent API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(jobs.router)
app.include_router(profile.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

