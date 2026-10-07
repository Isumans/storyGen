from typing import Annotated

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode


class Settings(BaseSettings):
    DATABASE_URL: str
    API_PREFIX: str = "/api"
    DEBUG: bool = True
    ALLOWED_ORIGINS: Annotated[list[str], NoDecode] = []
    GROQ_API_KEY: str | None = None
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"
    GROQ_MODEL: str = "openai/gpt-oss-20b"
    GROQ_MAX_TOKENS: int = 4096

    @field_validator("ALLOWED_ORIGINS", mode="before")
    def parse_allowed_origins(cls,v:str) -> list[str]:
        return v.split(",") if v else []

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()