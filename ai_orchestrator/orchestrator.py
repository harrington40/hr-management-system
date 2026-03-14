"""
AI Orchestrator  — core routing, chaining, and execution engine.

Routing strategy
----------------
REASON      → DeepAI (analysis, planning, decision making)
IMPLEMENT   → DeepSeeker (code generation, feature building)
DEBUG       → DeepSeeker (bug analysis, fixes)
TEST        → DeepSeeker (unit/integration test generation)
ORCHESTRATE → DeepAI for reasoning plan  →  DeepSeeker for implementation
              (two-model chain: the reasoning output feeds the coder)
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Callable, Dict, List, Optional

from .agents.deepai_agent import DeepAIReasoningAgent
from .agents.deepseeker_agent import DeepSeekerAgent
from .agents.base_agent import AgentResponse
from .config import get_deepseek_model, get_deepseek_max_tokens

logger = logging.getLogger(__name__)


# ─────────────────────────────── Task Model ──────────────────────────────── #

class TaskType(str, Enum):
    REASON      = "reason"       # high-level reasoning / analysis  → DeepAI
    IMPLEMENT   = "implement"    # code generation / features        → DeepSeeker
    DEBUG       = "debug"        # debugging / bug fix               → DeepSeeker
    TEST        = "test"         # test generation                   → DeepSeeker
    ORCHESTRATE = "orchestrate"  # reason  →  implement (two-model chain)


class TaskStatus(str, Enum):
    PENDING    = "pending"
    RUNNING    = "running"
    COMPLETED  = "completed"
    FAILED     = "failed"


@dataclass
class OrchestratorTask:
    prompt: str
    task_type: TaskType
    task_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    context: str = ""           # optional extra context / system prompt
    created_at: datetime = field(default_factory=datetime.now)
    status: TaskStatus = TaskStatus.PENDING


@dataclass
class OrchestratorResult:
    task: OrchestratorTask
    primary_response: AgentResponse
    secondary_response: Optional[AgentResponse] = None   # used in ORCHESTRATE chain
    completed_at: datetime = field(default_factory=datetime.now)

    @property
    def success(self) -> bool:
        ok = self.primary_response.success
        if self.secondary_response:
            ok = ok and self.secondary_response.success
        return ok

    @property
    def final_output(self) -> str:
        """Returns the most relevant output for the task type."""
        if self.secondary_response and self.secondary_response.success:
            return self.secondary_response.content
        return self.primary_response.content

    @property
    def chain_summary(self) -> str:
        """For ORCHESTRATE tasks shows both stages."""
        if not self.secondary_response:
            return self.primary_response.content
        return (
            "### Reasoning Plan (DeepAI)\n"
            f"{self.primary_response.content}\n\n"
            "---\n\n"
            "### Implementation (DeepSeeker)\n"
            f"{self.secondary_response.content}"
        )


# ─────────────────────────────── Orchestrator ────────────────────────────── #

class AIOrchestrator:
    """
    Coordinates DeepAI (reason) and DeepSeeker (implement / debug / test).

    Usage
    -----
        orch = AIOrchestrator(deepai_key="...", deepseek_key="...")
        result = await orch.run(OrchestratorTask(
            prompt="Add a salary comparison feature to the HR dashboard",
            task_type=TaskType.ORCHESTRATE,
        ))
        print(result.chain_summary)
    """

    REASON_SYSTEM = (
        "You are a senior software architect and HR domain expert. "
        "Analyse the request thoroughly, identify edge cases, produce a clear "
        "step-by-step implementation plan and list any assumptions made."
    )

    IMPLEMENT_SYSTEM = (
        "You are an expert Python developer working on a NiceGUI / FastAPI HRMS "
        "application. Write clean, secure, production-ready code. "
        "Return only code and brief inline comments unless asked otherwise."
    )

    DEBUG_SYSTEM = (
        "You are a Python debugging specialist. Analyse the code or error "
        "provided, explain the root cause, then supply the corrected code."
    )

    TEST_SYSTEM = (
        "You are a QA engineer. Write comprehensive pytest unit and integration "
        "tests for the provided code. Cover happy paths, edge cases, and error "
        "conditions. Use mocking where external dependencies are involved."
    )

    # ── Construction ─────────────────────────────────────────────────────── #

    def __init__(
        self,
        deepai_key: str,
        deepseek_key: str,
        on_progress: Optional[Callable[[str], None]] = None,
    ):
        self._reason_agent  = DeepAIReasoningAgent(api_key=deepai_key)
        self._coder_agent   = DeepSeekerAgent(
            api_key=deepseek_key,
            model=get_deepseek_model(),
            max_tokens=get_deepseek_max_tokens(),
        )
        self._on_progress   = on_progress or (lambda msg: None)
        self._history: List[OrchestratorResult] = []

    # ── Public API ───────────────────────────────────────────────────────── #

    async def run(self, task: OrchestratorTask) -> OrchestratorResult:
        """Execute a task and store the result in history."""
        task.status = TaskStatus.RUNNING
        self._on_progress(f"[{task.task_id}] Starting {task.task_type.value} task…")

        try:
            result = await self._dispatch(task)
        except Exception as exc:
            logger.exception("Orchestrator dispatch failed")
            task.status = TaskStatus.FAILED
            err_resp = AgentResponse(
                content="", agent_name="orchestrator", model="n/a",
                success=False, error=str(exc),
            )
            result = OrchestratorResult(task=task, primary_response=err_resp)

        task.status = TaskStatus.COMPLETED if result.success else TaskStatus.FAILED
        self._history.append(result)
        self._on_progress(
            f"[{task.task_id}] {'Done ✓' if result.success else 'Failed ✗'}"
        )
        return result

    async def run_many(self, tasks: List[OrchestratorTask]) -> List[OrchestratorResult]:
        """Run tasks sequentially (preserves order, avoids rate-limit issues)."""
        results = []
        for task in tasks:
            results.append(await self.run(task))
        return results

    @property
    def history(self) -> List[OrchestratorResult]:
        return list(self._history)

    def clear_history(self) -> None:
        self._history.clear()

    # ── Internal dispatch ─────────────────────────────────────────────────── #

    async def _dispatch(self, task: OrchestratorTask) -> OrchestratorResult:
        tt = task.task_type

        if tt == TaskType.REASON:
            return await self._reason_task(task)

        if tt == TaskType.IMPLEMENT:
            return await self._implement_task(task)

        if tt == TaskType.DEBUG:
            return await self._debug_task(task)

        if tt == TaskType.TEST:
            return await self._test_task(task)

        if tt == TaskType.ORCHESTRATE:
            return await self._orchestrate_task(task)

        raise ValueError(f"Unknown task type: {tt}")

    # ── Task handlers ─────────────────────────────────────────────────────── #

    async def _reason_task(self, task: OrchestratorTask) -> OrchestratorResult:
        system = f"{self.REASON_SYSTEM}\n\n{task.context}".strip() if task.context else self.REASON_SYSTEM
        self._on_progress(f"[{task.task_id}] → DeepAI reasoning…")
        resp = await self._reason_agent.invoke(task.prompt, system_prompt=system)
        return OrchestratorResult(task=task, primary_response=resp)

    async def _implement_task(self, task: OrchestratorTask) -> OrchestratorResult:
        system = f"{self.IMPLEMENT_SYSTEM}\n\n{task.context}".strip() if task.context else self.IMPLEMENT_SYSTEM
        self._on_progress(f"[{task.task_id}] → DeepSeeker implementing…")
        resp = await self._coder_agent.invoke(task.prompt, system_prompt=system, use_coder_model=True)
        return OrchestratorResult(task=task, primary_response=resp)

    async def _debug_task(self, task: OrchestratorTask) -> OrchestratorResult:
        system = f"{self.DEBUG_SYSTEM}\n\n{task.context}".strip() if task.context else self.DEBUG_SYSTEM
        self._on_progress(f"[{task.task_id}] → DeepSeeker debugging…")
        resp = await self._coder_agent.invoke(task.prompt, system_prompt=system, use_coder_model=True)
        return OrchestratorResult(task=task, primary_response=resp)

    async def _test_task(self, task: OrchestratorTask) -> OrchestratorResult:
        system = f"{self.TEST_SYSTEM}\n\n{task.context}".strip() if task.context else self.TEST_SYSTEM
        self._on_progress(f"[{task.task_id}] → DeepSeeker generating tests…")
        resp = await self._coder_agent.invoke(task.prompt, system_prompt=system, use_coder_model=True)
        return OrchestratorResult(task=task, primary_response=resp)

    async def _orchestrate_task(self, task: OrchestratorTask) -> OrchestratorResult:
        """
        Two-model chain:
        1. DeepAI produces a reasoning plan.
        2. DeepSeeker uses that plan to produce the implementation.
        """
        # Stage 1 — reason
        reason_system = f"{self.REASON_SYSTEM}\n\n{task.context}".strip() if task.context else self.REASON_SYSTEM
        reason_prompt  = (
            f"Analyse and create a detailed implementation plan for the following request:\n\n"
            f"{task.prompt}"
        )
        self._on_progress(f"[{task.task_id}] Stage 1 → DeepAI reasoning…")
        reason_resp = await self._reason_agent.invoke(reason_prompt, system_prompt=reason_system)

        if not reason_resp.success:
            return OrchestratorResult(task=task, primary_response=reason_resp)

        # Stage 2 — implement using the plan
        impl_system = self.IMPLEMENT_SYSTEM
        impl_prompt = (
            f"Using the plan below, implement the solution in Python (NiceGUI / FastAPI HRMS).\n\n"
            f"## Plan\n{reason_resp.content}\n\n"
            f"## Original Request\n{task.prompt}"
        )
        self._on_progress(f"[{task.task_id}] Stage 2 → DeepSeeker implementing…")
        impl_resp = await self._coder_agent.invoke(impl_prompt, system_prompt=impl_system, use_coder_model=True)

        return OrchestratorResult(
            task=task,
            primary_response=reason_resp,
            secondary_response=impl_resp,
        )
