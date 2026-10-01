from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime

class StoryOptionsSchema(BaseModel):
    text: str
    node_id: Optional[int] = None

class StoryNodeBase(BaseModel):
    content: str
    is_ending: bool = False
    is_winning_ending: bool = False

class completeStoryNodeResponse(StoryNodeBase):
    id: int
    options: List[StoryOptionsSchema] = []

    class Config:
        from_attributes = True

class StoryBase(BaseModel):
    title: str
    session_id: Optional[str] = None

    class Config:
            from_attributes = True

class CreateStoryRequest(BaseModel):
    theme: str

class completeStoryResponse(StoryBase):
    id: int
    created_at: datetime
    root_node: completeStoryNodeResponse
    all_nodes: Dict[int, completeStoryNodeResponse] = Field(default_factory=dict)
    
    class Config:
        from_attributes = True