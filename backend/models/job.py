from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from backend.db.database import Base

class StoryJob(Base):
    __tablename__ = "story_jobs"

    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, nullable=True)
    session_id = Column(String, nullable=True)
    job_id = Column(String, index=True)
    theme = Column(String)
    status = Column(String)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_job = Column(DateTime(timezone=True), nullable=True)