from datetime import datetime

from pydantic import BaseModel


class StoryJobBase(BaseModel):
    theme: str

class StoryJobResponse(BaseModel):
    story_id: int | None = None
    job_id: str
    status: str
    completed_at: datetime | None = None
    error: str | None = None

    class Config:
        from_attributes = True

class StoryJobCreate(StoryJobBase):
    pass

