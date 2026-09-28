import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Response, exceptions, Cookie, responses, BackgroundTasks
from datetime import datetime
from sqlalchemy.orm import Session

from backend.db.database import get_db, SessionLocal
from backend.models import job
from backend.models.job import StoryJob
from backend.schemas.job import StoryJobResponse

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)

@router.get("/{job_id}", response_model=job.StoryJobResponse)
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()
    if not job:
        raise exceptions.HTTPException(status_code=404, detail="Job not found")
    return job