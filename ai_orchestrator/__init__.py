"""
AI Orchestrator package.

Heavy agent imports (openai SDK etc.) are deferred so that importing
ai_orchestrator.config at startup does not trigger the full dependency chain.
"""

from .config import get_deepai_key, get_deepseek_key, get_deepseek_model, keys_configured


def _lazy_imports():
    """Import the orchestrator and agents only when needed."""
    from .orchestrator import AIOrchestrator, TaskType, OrchestratorTask, OrchestratorResult  # noqa: F401
    from .agents.deepai_agent import DeepAIReasoningAgent  # noqa: F401
    from .agents.deepseeker_agent import DeepSeekerAgent  # noqa: F401


# Re-export for callers who do `from ai_orchestrator import AIOrchestrator`
def __getattr__(name):
    _heavy = {
        "AIOrchestrator", "TaskType", "OrchestratorTask", "OrchestratorResult",
        "DeepAIReasoningAgent", "DeepSeekerAgent",
    }
    if name in _heavy:
        _lazy_imports()
        import sys
        return getattr(sys.modules[__name__], name)
    raise AttributeError(f"module 'ai_orchestrator' has no attribute {name!r}")


__all__ = [
    "AIOrchestrator",
    "TaskType",
    "OrchestratorTask",
    "OrchestratorResult",
    "DeepAIReasoningAgent",
    "DeepSeekerAgent",
    "get_deepai_key",
    "get_deepseek_key",
    "get_deepseek_model",
    "keys_configured",
]
