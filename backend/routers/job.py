import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Response, exceptions, Cookie, responses, BackgroundTasks
from datetime import datetime
from sqlalchemy.orm import Session

from db.database import get_db, SessionLocal
from models import job
from models.job import StoryJob
from schemas.job import StoryJobResponse

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)

@router.get("/{job_id}", response_model=StoryJobResponse)
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()
    if not job:
        raise exceptions.HTTPException(status_code=404, detail="Job not found")
    return job