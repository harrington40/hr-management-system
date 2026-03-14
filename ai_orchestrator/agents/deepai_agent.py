"""
DeepAI Reasoning Agent
Uses the DeepAI text-generation API as the reasoning / planning brain.
API docs: https://deepai.org/machine-learning-model/text-generator
"""

import logging
import httpx
from .base_agent import BaseAgent, AgentResponse

logger = logging.getLogger(__name__)

DEEPAI_API_URL = "https://api.deepai.org/api/text-generator"


class DeepAIReasoningAgent(BaseAgent):
    """
    Calls the DeepAI text-generator endpoint.
    Best suited for: reasoning, high-level planning, summarisation, analysis.
    """

    name = "DeepAI-Reasoning"
    model = "deepai/text-generator"

    def __init__(self, api_key: str, timeout: int = 60):
        super().__init__(api_key)
        self.timeout = timeout

    async def invoke(self, prompt: str, system_prompt: str = "", **kwargs) -> AgentResponse:
        full_prompt = f"{system_prompt}\n\n{prompt}".strip() if system_prompt else prompt
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    DEEPAI_API_URL,
                    headers={"api-key": self.api_key},
                    data={"text": full_prompt},
                )
                response.raise_for_status()
                data = response.json()

            output = data.get("output", "")
            if not output:
                return self._error_response("DeepAI returned an empty output.")

            return AgentResponse(
                content=output,
                agent_name=self.name,
                model=self.model,
                success=True,
                metadata={"url": data.get("output_url", ""), "id": data.get("id", "")},
            )

        except httpx.HTTPStatusError as exc:
            msg = f"DeepAI HTTP {exc.response.status_code}: {exc.response.text[:300]}"
            logger.error(msg)
            return self._error_response(msg)
        except httpx.RequestError as exc:
            msg = f"DeepAI request error: {exc}"
            logger.error(msg)
            return self._error_response(msg)
        except Exception as exc:
            msg = f"DeepAI unexpected error: {exc}"
            logger.exception(msg)
            return self._error_response(msg)
