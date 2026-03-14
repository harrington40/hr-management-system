"""
DeepSeek Implementation & Debugging Agent
Calls the DeepSeek API directly via httpx (no openai SDK needed).
DeepSeek exposes an OpenAI-compatible /v1/chat/completions endpoint so
the request/response shape is identical — we just skip the heavy SDK.
API base: https://api.deepseek.com
"""

import logging
import httpx
from .base_agent import BaseAgent, AgentResponse

logger = logging.getLogger(__name__)

DEEPSEEK_CHAT_URL = "https://api.deepseek.com/v1/chat/completions"
DEFAULT_MODEL = "deepseek-chat"
CODER_MODEL   = "deepseek-coder"


class DeepSeekerAgent(BaseAgent):
    """
    Calls the DeepSeek chat-completions endpoint over plain httpx.
    Best suited for: implementation, debugging, test generation, code review.
    """

    name = "DeepSeeker-Coder"
    model = DEFAULT_MODEL

    def __init__(
        self,
        api_key: str,
        model: str = DEFAULT_MODEL,
        max_tokens: int = 4096,
        temperature: float = 0.2,
        timeout: int = 120,
    ):
        super().__init__(api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout

    async def invoke(
        self,
        prompt: str,
        system_prompt: str = "",
        use_coder_model: bool = False,
        **kwargs,
    ) -> AgentResponse:
        target_model = CODER_MODEL if use_coder_model else self.model
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": target_model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
        # Pass through optional extras (top_p, etc.)
        for key in ("top_p",):
            if key in kwargs:
                payload[key] = kwargs[key]

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(DEEPSEEK_CHAT_URL, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()

            choice = data["choices"][0]
            content = choice["message"]["content"] or ""
            usage = data.get("usage", {})

            return AgentResponse(
                content=content,
                agent_name=self.name,
                model=target_model,
                success=True,
                tokens_used=usage.get("total_tokens", 0),
                metadata={
                    "prompt_tokens": usage.get("prompt_tokens", 0),
                    "completion_tokens": usage.get("completion_tokens", 0),
                    "finish_reason": choice.get("finish_reason", ""),
                },
            )

        except httpx.HTTPStatusError as exc:
            msg = f"DeepSeek HTTP {exc.response.status_code}: {exc.response.text[:300]}"
            logger.error(msg)
            return self._error_response(msg)
        except httpx.RequestError as exc:
            msg = f"DeepSeek request error: {exc}"
            logger.error(msg)
            return self._error_response(msg)
        except Exception as exc:
            msg = f"DeepSeeker unexpected error: {exc}"
            logger.exception(msg)
            return self._error_response(msg)
