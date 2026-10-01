import json

from sqlalchemy.orm import Session
from core.models import StoryLLMResponse, StoryNodeLLM
from core.config import settings

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from core.prompts import STORY_PROMPT
from models.story import Story, StoryNode
class StoryGenerator:

    @classmethod
    def _get_llm(cls):
        api_key = settings.GROQ_API_KEY or settings.OPENAI_API_KEY
        if not api_key:
            raise RuntimeError("Set GROQ_API_KEY to generate stories")

        return ChatOpenAI(
            model=settings.GROQ_MODEL,
            api_key=api_key,
            base_url=settings.GROQ_BASE_URL,
            max_tokens=settings.GROQ_MAX_TOKENS,
        )

    @classmethod
    def generate_story(cls, db: Session, session_id:str, theme:str) -> Story:
        llm = cls._get_llm()
        story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)


        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    STORY_PROMPT
                ),
                (
                    "human",
                    f"Create a story based on the theme: {theme}"
                )
            ]
        ).partial(format_instructions=story_parser.get_format_instructions())

        raw_response = llm.bind(
            response_format={"type": "json_object"}
        ).invoke(prompt.invoke({}))

        response_text = raw_response
        if hasattr(raw_response, "content"):
            response_text = raw_response.content

        if isinstance(response_text, list):
            response_text = "".join(
                item.get("text", "") if isinstance(item, dict) else str(item)
                for item in response_text
            )

        if not isinstance(response_text, str):
            raise ValueError("The model returned an unsupported response format")

        story_structure = StoryLLMResponse.model_validate(json.loads(response_text))

        story_db = Story(title=story_structure.title, session_id=session_id)
        db.add(story_db)
        db.flush()

        root_node_data = story_structure.rootNode
        if isinstance(root_node_data, dict):
            root_node_data = StoryNodeLLM.model_validate(root_node_data)

        cls._process_story_node(db, story_db.id, root_node_data, is_root=True)

        db.commit()
        return story_db

    @classmethod
    def _process_story_node(cls, db: Session, story_id: int, node_data: StoryNodeLLM, is_root: bool = False)->StoryNode:
        node = StoryNode(
            story_id=story_id,
            content=node_data.content if hasattr(node_data, "content") else node_data["content"],
            is_ending=node_data.isEnding if hasattr(node_data, "isEnding") else node_data["isEnding"],
            is_winning_ending=node_data.isWinningEnding if hasattr(node_data, "isWinningEnding") else node_data["isWinningEnding"],
            is_root=is_root,
            options=[]
        )
        db.add(node)
        db.flush()

        if not node.is_ending and (hasattr(node_data, "options")and node_data.options):
            options_list = []
            for option_data in node_data.options:
                next_node = option_data.nextNode

                if isinstance(next_node, dict):
                    next_node = StoryNodeLLM.model_validate(next_node)

                child_node = cls._process_story_node(db, story_id, next_node, is_root=False)

                options_list.append({
                    "text": option_data.text,
                    "node_id": child_node.id
                })

            node.options = options_list

        db.flush()
        return node