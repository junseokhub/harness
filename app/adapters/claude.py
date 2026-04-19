import anthropic
from app.adapters.base import BaseLLMAdapter, LLMResponse


class ClaudeAdapter(BaseLLMAdapter):
    """Anthropic Claude LLM 어댑터"""

    def __init__(self, api_key: str, model: str):
        super().__init__(api_key, model)
        self.client = anthropic.AsyncAnthropic(api_key=api_key)

    async def generate(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        message = await self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return LLMResponse(
            content=message.content[0].text,
            input_tokens=message.usage.input_tokens,
            output_tokens=message.usage.output_tokens,
            total_tokens=message.usage.input_tokens + message.usage.output_tokens,
        )