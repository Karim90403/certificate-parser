import os
from functools import lru_cache

from dotenv import find_dotenv, load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv())


class ProjectConfig(BaseSettings):
    debug: bool = Field(default=False)
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    searched_id: list[int] = Field(default=[])
    product_name: str = Field(default="УВЭОС")
    max_response_size: int = Field(default=1000)
    token: str = Field(default="")

    @property
    def cookies(self):
        return {
            "_ym_uid": "1712313037677828500",
            "_ym_d": "1712313037",
            "_ym_isad": "2",
            "JSESSIONID": "DC362F4A51390945B72B0EABA3824421",
        }


class Settings(BaseSettings):
    project: ProjectConfig = ProjectConfig()


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
