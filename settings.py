from functools import lru_cache
from pathlib import Path
from pydantic import BaseSettings

IMAGE_DIR = str(Path(__file__).resolve().parent / 'images')


class Settings(BaseSettings):
    open_ai_key: str

    host: str
    port: int

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache
def get_settings() -> Settings:
    return Settings()
