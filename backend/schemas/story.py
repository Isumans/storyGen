from datetime import datetime

from pydantic import BaseModel, Field


class StoryOptionsSchema(BaseModel):
    text: str
    node_id: int | None = None

class StoryNodeBase(BaseModel):
    content: str
    is_ending: bool = False
    is_winning_ending: bool = False

class completeStoryNodeResponse(StoryNodeBase):
    id: int
    options: list[StoryOptionsSchema] = []

    class Config:
        from_attributes = True

class StoryBase(BaseModel):
    title: str
    session_id: str | None = None

    class Config:
            from_attributes = True

class CreateStoryRequest(BaseModel):
    theme: str

class completeStoryResponse(StoryBase):
    id: int
    created_at: datetime
    root_node: completeStoryNodeResponse
    all_nodes: dict[int, completeStoryNodeResponse] = Field(default_factory=dict)
    
    class Config:
        from_attributes = True