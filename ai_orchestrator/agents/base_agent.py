"""
Base agent interface for the AI Orchestrator.
All concrete agents must inherit from BaseAgent.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class AgentResponse:
    """Typed response returned by any agent."""
    content: str
    agent_name: str
    model: str
    success: bool
    error: Optional[str] = None
    tokens_used: int = 0
    metadata: dict = field(default_factory=dict)


class BaseAgent(ABC):
    """Abstract base class for all orchestrator agents."""

    name: str = "BaseAgent"
    model: str = "unknown"

    def __init__(self, api_key: str):
        if not api_key or not api_key.strip():
            raise ValueError(f"{self.name}: api_key must not be empty.")
        self.api_key = api_key.strip()

    @abstractmethod
    async def invoke(self, prompt: str, system_prompt: str = "", **kwargs) -> AgentResponse:
        """Send prompt to the underlying model and return a structured response."""

    def _error_response(self, error: str) -> AgentResponse:
        return AgentResponse(
            content="",
            agent_name=self.name,
            model=self.model,
            success=False,
            error=error,
        )
