from app.adapters.base import BaseLLMAdapter
from app.adapters.claude import ClaudeAdapter
from app.adapters.openai import OpenAIAdapter
from app.schemas.harness import HarnessRequest, HarnessResponse, Provider, TokenUsage
from app.core.config import settings
from app.core.prompts import get_system_prompt


class Harness:
    """AI 에이전트를 감싸는 제어 실행 환경"""

    def _get_adapter(self, request: HarnessRequest) -> BaseLLMAdapter:
        """provider에 맞는 LLM 어댑터 반환"""
        if request.provider == Provider.claude:
            return ClaudeAdapter(
                api_key=settings.anthropic_api_key,
                model=request.model,
            )
        else:
            return OpenAIAdapter(
                api_key=settings.openai_api_key,
                model=request.model,
            )

    async def run(self, request: HarnessRequest) -> HarnessResponse:
        """하네스 실행 - LLM 1번 호출로 가드 + 답변 처리"""

        adapter = self._get_adapter(request)

        # context 있으면 RAG 프롬프트, 없으면 일반 프롬프트
        system_prompt = get_system_prompt(
            topic=request.topic,
            topic_desc=request.topic_desc,
            context=request.context,
        )

        # LLM 1번 호출로 가드 + 답변 동시 처리
        llm_response = await adapter.generate(
            system_prompt=system_prompt,
            user_prompt=request.query,
        )

        token_usage = TokenUsage(
            input_tokens=llm_response.input_tokens,
            output_tokens=llm_response.output_tokens,
            total_tokens=llm_response.total_tokens,
        )

        # BLOCKED 여부 체크
        content = llm_response.content.strip()
        if content.startswith("BLOCKED:"):
            reason = content.replace("BLOCKED:", "").strip()
            return HarnessResponse(
                success=False,
                provider=request.provider,
                topic=request.topic,
                query=request.query,
                blocked=True,
                blocked_reason=reason,
                token_usage=token_usage,
            )

        return HarnessResponse(
            success=True,
            provider=request.provider,
            topic=request.topic,
            query=request.query,
            answer=content,
            token_usage=token_usage,
        )