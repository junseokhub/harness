import yaml
from pathlib import Path
from typing import Optional


def load_config() -> dict:
    config_path = Path(__file__).parent.parent.parent / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


_config = load_config()


def get_system_prompt(topic: str, topic_desc: str, context: Optional[str] = None) -> str:
    """시스템 프롬프트 반환 - context 있으면 RAG 프롬프트 사용"""
    if context:
        template = _config["prompts"]["system_with_context"]
        return template.format(topic=topic, topic_desc=topic_desc, context=context)
    else:
        template = _config["prompts"]["system"]
        return template.format(topic=topic, topic_desc=topic_desc)