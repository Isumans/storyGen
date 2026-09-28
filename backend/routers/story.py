import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Response, exceptions, Cookie, responses, BackgroundTasks
from datetime import datetime
from sqlalchemy.orm import Session

from backend.db.database import get_db, SessionLocal
from backend.models import job
from backend.models.story import Story, StoryNode
from backend.models.job import StoryJob
from backend.schemas.story import (
    completeStoryNodeResponse, completeStoryResponse, CreateStoryRequest
)
from backend.schemas.job import StoryJobResponse


router = APIRouter(
    prefix="/stories",
    tags=["stories"]
)

def get_session_id(session_id:Optional[str] = Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id

@router.post("/create", response_model=StoryJobResponse)
def create_story(
    request: CreateStoryRequest,
    background_tasks: BackgroundTasks,
    response: Response,
    session_id:str= Depends(get_session_id),
    db: Session= Depends(get_db)
):
    response.set_cookie(key="session_id", value=session_id, httponly=True)

    job_id = str(uuid.uuid4())

    job = StoryJob(
        job_id = job_id,
        session_id = session_id,
        theme = request.theme,
        status = "pending"
    )
    db.add(job)
    db.commit()


     #TODo: Add background task to process the story creation
    background_tasks.add_task(
         generate_story_task, 
         job_id=job_id, 
         theme=request.theme, 
         session_id=session_id
         )
    return job

def generate_story_task(job_id:str, theme:str, session_id:str):
    db = SessionLocal()
    try:
        job =db.query(StoryJob).filter(StoryJob.job_id == job_id).first()
        if not job:
            return

        try:
            job.status = "in_progress"
            db.commit()

            story = {} #todO: generate story

            job.story_id = 1 #todo: update story id
            job.status = "completed"
            job.completed_at = datetime.utcnow()
            db.commit()
        except Exception as e:
            job.status = "failed"
            job.completed_at = datetime.now()
            job.error = str(e)
            db.commit()
    finally:
        db.close()

@router.get("{story_id}/complete", response_model=completeStoryResponse)
def get_complete_story(story_id:int, db: Session= Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise exceptions.HTTPException(status_code=404, detail="Story not found")
    
    complete_story = build_complete_story_tree(db, story)
    return complete_story

def build_complete_story_tree(db: Session, story: Story) -> completeStoryResponse:
    pass