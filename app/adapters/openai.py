from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam
from app.adapters.base import BaseLLMAdapter, LLMResponse


class OpenAIAdapter(BaseLLMAdapter):
    """OpenAI GPT LLM 어댑터"""

    def __init__(self, api_key: str, model: str):
        super().__init__(api_key, model)
        self.client = AsyncOpenAI(api_key=api_key)

    async def generate(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        messages = [
            ChatCompletionSystemMessageParam(role="system", content=system_prompt),
            ChatCompletionUserMessageParam(role="user", content=user_prompt),
        ]
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        usage = response.usage
        return LLMResponse(
            content=response.choices[0].message.content,
            input_tokens=usage.prompt_tokens,
            output_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
        )