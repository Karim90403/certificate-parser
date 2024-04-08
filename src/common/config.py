import os
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class ProjectConfig(BaseSettings):
    debug: bool = Field(default=False)
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    column_search: str = Field(default="УВЭОС")


class Settings(BaseSettings):
    project: ProjectConfig = ProjectConfig()


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
