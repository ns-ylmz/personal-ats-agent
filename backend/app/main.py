from contextlib import asynccontextmanager
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models
from app.api import jobs, profile
from app.database import engine
from app.queue_manager import job_queue
from app.worker import start_worker

load_dotenv()

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
