from typing import Any

from pydantic import BaseModel, Field


class StoryOptionLLM(BaseModel):
    text: str = Field(description="The text displayed for this story choice.")
    nextNode: dict[str, Any]= Field(description="The next node in the story, which can be another StoryNodeLLM or an ending node.")


class StoryNodeLLM(BaseModel):
    content: str = Field(description="The content of the story node.")
    isEnding: bool = Field(description="Indicates if this node is an ending node.")
    isWinningEnding: bool = Field(description="Indicates if this node is a winning ending.")
    options: list[StoryOptionLLM] = Field(description="A list of options leading to other nodes or endings.")

class StoryLLMResponse(BaseModel):
    title: str = Field(description="The title of the story.")
    rootNode: StoryNodeLLM = Field(description="The root node of the story, which contains the starting situation and options.")
    