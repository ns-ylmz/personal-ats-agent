from fastapi import FastAPI
from app.database import engine
from app import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal ATS Agent API")

@app.get("/health")
def health_check():
    return {"status": "ok"}
