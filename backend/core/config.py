from typing import Annotated, List
from pydantic_settings import BaseSettings, NoDecode
from pydantic import field_validator

class Settings(BaseSettings):
    DATABASE_URL: str
    API_PREFIX: str = "/api"
    DEBUG: bool = True
    ALLOWED_ORIGINS: Annotated[List[str], NoDecode] = []
    OPENAI_API_KEY: str

    @field_validator("ALLOWED_ORIGINS", mode="before")
    def parse_allowed_origins(cls,v:str) -> List[str]:
        return v.split(",") if v else []

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()