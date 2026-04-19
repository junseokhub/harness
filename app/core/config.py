import yaml
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import List


def _load_config() -> dict:
    config_file = os.getenv("CONFIG_FILE", "config.yaml")
    config_path = Path(__file__).parent.parent.parent / config_file
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


_config = _load_config()


def get_model(provider: str, model_type: str = "default") -> str:
    """모델명 반환 (model_type: default or guard)"""
    return _config["models"][provider][model_type]


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    config_file: str = "config.yaml"

    class Config:
        env_file = ".env"

settings = Settings()