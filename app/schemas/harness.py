from pydantic import BaseModel, model_validator
from typing import Optional
from enum import Enum
from app.core.config import get_model


class Provider(str, Enum):
    claude = "claude"
    openai = "openai"


class TokenUsage(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0


class HarnessRequest(BaseModel):
    provider: Provider = Provider.claude
    model: Optional[str] = None
    topic: str
    topic_desc: str
    query: str
    context: Optional[str] = None       # RAG 검색 결과 (없으면 LLM 자체 지식으로 답변)

    @model_validator(mode="after")
    def set_default_model(self) -> "HarnessRequest":
        if not self.model:
            self.model = get_model(self.provider, "default")
        return self


class HarnessResponse(BaseModel):
    success: bool
    provider: str
    topic: str
    query: str
    answer: Optional[str] = None
    blocked: bool = False
    blocked_reason: Optional[str] = None
    token_usage: Optional[TokenUsage] = None