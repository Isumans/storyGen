from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime

class StoryOptionsSchema(BaseModel):
    text: str
    node_id: Optional[int] = None

class StoryNodeBase(BaseModel):
    content: str
    is_ending: bool = False
    is_wining_ending: bool = False

class completeStoryNodeResponse(StoryNodeBase):
    id: int
    options: List[StoryOptionsSchema] = []

    class Config:
        from_attribute = True

class StoryBase(BaseModel):
    title: str
    session_id: Optional[str] = None

    class Config:
            from_attribute = True

class CreateStoryRequest(BaseModel):
    theme: str

class completeStoryResponse(StoryBase):
    id: int
    created_at: datetime
    root_node: completeStoryNodeResponse
    all_nodes: Dict[int, completeStoryNodeResponse] = {}
    
    class Config:
        from_attribute = True