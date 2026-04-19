from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMResponse:
    """LLM 응답 + 토큰 사용량"""
    content: str
    input_tokens: int
    output_tokens: int
    total_tokens: int


class BaseLLMAdapter(ABC):
    """모든 LLM 어댑터의 추상 베이스 클래스"""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    @abstractmethod
    async def generate(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """LLM에 요청을 보내고 응답과 토큰 사용량 반환"""
        pass