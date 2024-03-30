from pydantic_settings import BaseSettings
from typing import Optional


class GlobalConfig(BaseSettings):
    HF_TOKEN: str

    class Config:
        env_file = ".env"


global_config = GlobalConfig()
