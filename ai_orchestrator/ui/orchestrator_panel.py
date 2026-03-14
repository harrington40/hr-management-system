"""
AI Orchestrator NiceGUI panel.

Provides a full-page chat/task interface that lets users:
  • Enter API keys — pre-filled from .env (DEEPAI_API_KEY / DEEPSEEK_API_KEY)
    and saved in NiceGUI user storage as an override (never logged server-side)
  • Pick a task type (Reason / Implement / Debug / Test / Orchestrate)
  • Submit a prompt and see streaming progress + final result
  • Browse task history
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Optional

from nicegui import ui, app as nicegui_app

from ..orchestrator import AIOrchestrator, OrchestratorTask, OrchestratorResult, TaskType, TaskStatus
from ..config import get_deepai_key, get_deepseek_key, get_deepseek_model, get_deepseek_max_tokens, keys_configured

logger = logging.getLogger(__name__)

# ─── Storage keys (NiceGUI user storage — browser-scoped, not server logs) ── #
_KEY_DEEPAI  = "ai_orch_deepai_key"
_KEY_DEEPSK  = "ai_orch_deepseek_key"

TASK_TYPE_OPTIONS = {
    "🧠  Reason  (DeepAI)":                TaskType.REASON,
    "⚙️  Implement  (DeepSeeker)":         TaskType.IMPLEMENT,
    "🐛  Debug  (DeepSeeker)":             TaskType.DEBUG,
    "🧪  Test  (DeepSeeker)":              TaskType.TEST,
    "🚀  Orchestrate  (Reason → Implement)": TaskType.ORCHESTRATE,
}

BADGE_COLORS: dict[TaskType, str] = {
    TaskType.REASON:      "bg-blue-100 text-blue-800",
    TaskType.IMPLEMENT:   "bg-green-100 text-green-800",
    TaskType.DEBUG:       "bg-red-100 text-red-800",
    TaskType.TEST:        "bg-yellow-100 text-yellow-800",
    TaskType.ORCHESTRATE: "bg-purple-100 text-purple-800",
}


def create_ai_orchestrator_page() -> None:
    """Render the full AI Orchestrator page inside the existing NiceGUI layout."""

    # ── State ─────────────────────────────────────────────────────────────── #
    state = {
        "orchestrator": None,        # AIOrchestrator instance
        "running": False,
        "results": [],               # list[OrchestratorResult]
        "progress_log": [],          # list[str]
        "selected_task_type": TaskType.ORCHESTRATE,
    }

    # ── Load keys: prefer browser storage override, fall back to .env ─────── #
    storage = nicegui_app.storage.user
    env_deepai   = get_deepai_key()
    env_deepsk   = get_deepseek_key()
    saved_deepai = storage.get(_KEY_DEEPAI, "") or env_deepai
    saved_deepsk = storage.get(_KEY_DEEPSK, "") or env_deepsk
    env_keys_ok  = keys_configured()

    # ── Layout ────────────────────────────────────────────────────────────── #
    with ui.element("div").classes("min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 p-6"):

        # ── Title bar ─────────────────────────────────────────────────────── #
        with ui.row().classes("items-center gap-4 mb-6"):
            ui.html(
                '<div class="bg-gradient-to-r from-purple-600 to-indigo-600 text-white '
                'p-3 rounded-xl shadow-lg text-2xl">🤖</div>'
            )
            with ui.column():
                ui.html('<h1 class="text-3xl font-bold text-gray-800">AI Orchestrator</h1>')
                ui.html(
                    '<p class="text-gray-500">DeepAI Reasoning  ⟷  DeepSeeker Implementation & Debugging</p>'
                )
            # .env status badge
            if env_keys_ok:
                ui.html(
                    '<span class="ml-4 px-3 py-1 rounded-full text-xs font-medium '
                    'bg-green-100 text-green-800">✅ .env keys loaded</span>'
                )
            else:
                ui.html(
                    '<span class="ml-4 px-3 py-1 rounded-full text-xs font-medium '
                    'bg-yellow-100 text-yellow-800">⚠️ Enter API keys below</span>'
                )

        with ui.row().classes("w-full gap-6 items-start"):

            # ══════════════════════════════════════════════════════════════ #
            # LEFT PANEL — Config + Input
            # ══════════════════════════════════════════════════════════════ #
            with ui.card().classes("w-[420px] shrink-0 shadow-lg rounded-2xl p-6"):

                # ── API Keys ──────────────────────────────────────────── #
                ui.html('<h2 class="text-lg font-semibold text-gray-700 mb-3">🔑 API Keys</h2>')

                deepai_input = ui.input(
                    label="DeepAI API Key  (Reasoning brain)",
                    value=saved_deepai,
                    password=True,
                    password_toggle_button=True,
                ).classes("w-full mb-2").props('outlined dense')

                deepseek_input = ui.input(
                    label="DeepSeek API Key  (Coder brain)",
                    value=saved_deepsk,
                    password=True,
                    password_toggle_button=True,
                ).classes("w-full mb-1").props('outlined dense')

                # Source hint
                if env_keys_ok:
                    ui.html(
                        '<p class="text-xs text-green-600 mb-1">✅ Keys pre-loaded from <code>.env</code>. '
                        'Type here to override for this session.</p>'
                    )
                else:
                    ui.html(
                        '<p class="text-xs text-yellow-600 mb-1">⚠️ No keys found in <code>.env</code>. '
                        'Add <code>DEEPAI_API_KEY</code> and <code>DEEPSEEK_API_KEY</code> to your '
                        '<code>.env</code> file, or enter them manually below.</p>'
                    )
                ui.html(
                    '<p class="text-xs text-gray-400 mb-4">'
                    'Manual overrides are stored in your browser session only — never logged server-side.</p>'
                )

                ui.separator()

                # ── Task Type ─────────────────────────────────────────── #
                ui.html('<h2 class="text-lg font-semibold text-gray-700 mt-4 mb-3">⚡ Task Type</h2>')

                task_type_select = ui.select(
                    options=list(TASK_TYPE_OPTIONS.keys()),
                    value=list(TASK_TYPE_OPTIONS.keys())[-1],   # default = Orchestrate
                ).classes("w-full mb-4").props('outlined dense')

                def on_task_type_change(e):
                    state["selected_task_type"] = TASK_TYPE_OPTIONS[e.value]

                task_type_select.on_value_change(on_task_type_change)

                # ── Context (optional) ────────────────────────────────── #
                context_input = ui.textarea(
                    label="Context / System Instructions  (optional)",
                    placeholder="e.g. 'Focus on the attendance module. Use YAML config files.'",
                ).classes("w-full mb-4").props('outlined dense rows=3')

                # ── Prompt ────────────────────────────────────────────── #
                ui.html('<h2 class="text-lg font-semibold text-gray-700 mb-2">💬 Prompt</h2>')

                prompt_input = ui.textarea(
                    label="Describe your task…",
                    placeholder=(
                        "e.g. 'Add a salary comparison chart to the HR dashboard "
                        "using NiceGUI and the existing YAML employee config.'"
                    ),
                ).classes("w-full mb-4").props('outlined rows=6')

                # ── Run button ────────────────────────────────────────── #
                run_btn = ui.button(
                    "Run Task",
                    icon="play_arrow",
                ).classes(
                    "w-full bg-gradient-to-r from-purple-600 to-indigo-600 text-white "
                    "font-semibold py-3 rounded-xl hover:opacity-90 transition"
                ).props("unelevated")

                # ── Quick-example buttons ──────────────────────────────── #
                ui.html('<p class="text-xs text-gray-400 mt-4 mb-2">Quick examples:</p>')
                examples = [
                    ("Analyse attendance trends", TaskType.REASON,
                     "Analyse the current attendance module logic and summarise patterns and risks."),
                    ("Debug a bug", TaskType.DEBUG,
                     "Paste your traceback or buggy code snippet here and ask DeepSeeker to fix it."),
                    ("Generate tests", TaskType.TEST,
                     "Write pytest tests for the leave_rules module covering all edge cases."),
                ]
                for label, ttype, ex_prompt in examples:
                    def _fill(t=ttype, p=ex_prompt):
                        key = next(k for k, v in TASK_TYPE_OPTIONS.items() if v == t)
                        task_type_select.set_value(key)
                        state["selected_task_type"] = t
                        prompt_input.set_value(p)
                    ui.button(label, on_click=_fill).classes(
                        "w-full text-left text-xs text-gray-600 bg-gray-50 "
                        "hover:bg-gray-100 rounded-lg px-3 py-2 mb-1"
                    ).props("flat dense")

            # ══════════════════════════════════════════════════════════════ #
            # RIGHT PANEL — Progress log + Result
            # ══════════════════════════════════════════════════════════════ #
            with ui.column().classes("flex-1 gap-4"):

                # Progress log ──────────────────────────────────────────── #
                with ui.card().classes("w-full shadow rounded-2xl p-4"):
                    ui.html('<h2 class="text-lg font-semibold text-gray-700 mb-2">📡 Live Progress</h2>')
                    progress_area = ui.column().classes("gap-1 max-h-40 overflow-y-auto")

                # Result card ───────────────────────────────────────────── #
                result_card = ui.card().classes("w-full shadow rounded-2xl p-6")
                with result_card:
                    ui.html(
                        '<div id="result-placeholder" class="text-gray-400 text-sm italic">'
                        'Results will appear here after you run a task.</div>'
                    )

                # History ──────────────────────────────────────────────── #
                history_card = ui.card().classes("w-full shadow rounded-2xl p-4")
                with history_card:
                    ui.html('<h2 class="text-lg font-semibold text-gray-700 mb-3">🕘 Task History</h2>')
                    history_column = ui.column().classes("gap-2 max-h-80 overflow-y-auto")
                    with history_column:
                        ui.html('<p class="text-xs text-gray-400">No tasks run yet.</p>')

        # ── Helper: render a progress message ─────────────────────────────── #
        def add_progress(msg: str):
            state["progress_log"].append(msg)
            with progress_area:
                ts = datetime.now().strftime("%H:%M:%S")
                ui.html(
                    f'<div class="text-xs font-mono text-gray-600">'
                    f'<span class="text-gray-400">[{ts}]</span> {msg}</div>'
                )

        # ── Helper: render a result ────────────────────────────────────────── #
        def render_result(result: OrchestratorResult):
            result_card.clear()
            with result_card:
                ttype = result.task.task_type
                badge_cls = BADGE_COLORS.get(ttype, "bg-gray-100 text-gray-800")
                status_icon = "✅" if result.success else "❌"

                with ui.row().classes("items-center gap-3 mb-4"):
                    ui.html(
                        f'<span class="px-3 py-1 rounded-full text-sm font-medium {badge_cls}">'
                        f'{ttype.value.upper()}</span>'
                    )
                    ui.html(f'<span class="text-lg">{status_icon}</span>')
                    ui.html(
                        f'<span class="text-xs text-gray-400">'
                        f'Task ID: {result.task.task_id}  •  '
                        f'{result.completed_at.strftime("%H:%M:%S")}</span>'
                    )

                if not result.success:
                    err = (
                        result.primary_response.error
                        or (result.secondary_response.error if result.secondary_response else "Unknown error")
                    )
                    ui.html(
                        f'<div class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700 text-sm">'
                        f'<strong>Error:</strong> {err}</div>'
                    )
                    return

                # ORCHESTRATE shows two tabs; others show single output
                if ttype == TaskType.ORCHESTRATE and result.secondary_response:
                    with ui.tabs().classes("w-full") as tabs:
                        tab_impl   = ui.tab("Implementation",   icon="code")
                        tab_reason = ui.tab("Reasoning Plan",   icon="psychology")

                    with ui.tab_panels(tabs, value=tab_impl).classes("w-full mt-2"):
                        with ui.tab_panel(tab_impl):
                            _render_markdown_or_code(result.secondary_response.content)
                            _render_token_info(result.secondary_response)
                        with ui.tab_panel(tab_reason):
                            _render_markdown_or_code(result.primary_response.content)
                else:
                    resp = result.primary_response
                    _render_markdown_or_code(resp.content)
                    _render_token_info(resp)

        def _render_markdown_or_code(text: str):
            """Render content — code blocks get syntax highlighting via scrollable pre."""
            if "```" in text:
                ui.markdown(text).classes("text-sm leading-relaxed prose max-w-none")
            else:
                ui.html(
                    f'<div class="bg-gray-50 border border-gray-200 rounded-lg p-4 '
                    f'text-sm text-gray-800 leading-relaxed whitespace-pre-wrap overflow-x-auto">'
                    f'{text}</div>'
                )

        def _render_token_info(resp):
            if resp.tokens_used:
                ui.html(
                    f'<div class="mt-3 text-xs text-gray-400">'
                    f'Model: <strong>{resp.model}</strong>  •  '
                    f'Tokens used: <strong>{resp.tokens_used}</strong></div>'
                )

        def refresh_history():
            history_column.clear()
            if not state["results"]:
                with history_column:
                    ui.html('<p class="text-xs text-gray-400">No tasks run yet.</p>')
                return
            with history_column:
                for r in reversed(state["results"]):
                    ttype = r.task.task_type
                    badge_cls = BADGE_COLORS.get(ttype, "bg-gray-100 text-gray-800")
                    icon = "✅" if r.success else "❌"
                    snippet = (r.task.prompt[:80] + "…") if len(r.task.prompt) > 80 else r.task.prompt

                    def _show(result=r):
                        render_result(result)

                    with ui.row().classes(
                        "items-center gap-2 p-2 rounded-lg hover:bg-gray-50 cursor-pointer border"
                    ).on("click", _show):
                        ui.html(f'<span class="px-2 py-0.5 rounded-full text-xs {badge_cls}">{ttype.value}</span>')
                        ui.html(f'<span class="text-lg">{icon}</span>')
                        ui.html(f'<span class="text-xs text-gray-600 flex-1 truncate">{snippet}</span>')
                        ui.html(
                            f'<span class="text-xs text-gray-400">'
                            f'{r.completed_at.strftime("%H:%M")}</span>'
                        )

        # ── Main run handler ───────────────────────────────────────────────── #
        async def handle_run():
            if state["running"]:
                ui.notify("A task is already running. Please wait.", color="warning")
                return

            prompt = prompt_input.value.strip()
            if not prompt:
                ui.notify("Please enter a prompt.", color="negative")
                return

            deepai_key   = deepai_input.value.strip() or get_deepai_key()
            deepseek_key = deepseek_input.value.strip() or get_deepseek_key()

            # Validate keys — clear fallback to .env already applied above
            if not deepai_key:
                ui.notify("DeepAI API key is required. Add DEEPAI_API_KEY to .env or enter it above.", color="negative")
                return
            if not deepseek_key:
                ui.notify("DeepSeek API key is required. Add DEEPSEEK_API_KEY to .env or enter it above.", color="negative")
                return

            # Persist manual overrides in browser storage (env-sourced keys are not re-saved)
            if deepai_input.value.strip():
                storage[_KEY_DEEPAI] = deepai_key
            if deepseek_input.value.strip():
                storage[_KEY_DEEPSK] = deepseek_key

            # Build orchestrator (fresh each run so key/model changes are picked up)
            def _progress(msg: str):
                add_progress(msg)

            try:
                from ..agents.deepseeker_agent import DeepSeekerAgent
                from ..agents.deepai_agent import DeepAIReasoningAgent
                from ..orchestrator import AIOrchestrator as _Orch
                orchestrator = _Orch(
                    deepai_key=deepai_key,
                    deepseek_key=deepseek_key,
                    on_progress=_progress,
                )
                # Apply env model/token overrides
                orchestrator._coder_agent.model      = get_deepseek_model()
                orchestrator._coder_agent.max_tokens = get_deepseek_max_tokens()
            except ValueError as e:
                ui.notify(str(e), color="negative")
                return

            task = OrchestratorTask(
                prompt=prompt,
                task_type=state["selected_task_type"],
                context=context_input.value.strip(),
            )

            state["running"] = True
            run_btn.disable()
            run_btn.set_text("Running…")

            progress_area.clear()
            result_card.clear()
            with result_card:
                with ui.row().classes("items-center gap-3 text-gray-500"):
                    ui.spinner(size="lg", color="purple")
                    ui.html('<span class="text-sm">Processing your task…</span>')

            try:
                result = await orchestrator.run(task)
                state["results"].append(result)
                render_result(result)
                refresh_history()
                if result.success:
                    ui.notify("Task completed successfully!", color="positive")
                else:
                    err = result.primary_response.error or "Unknown error"
                    ui.notify(f"Task failed: {err[:100]}", color="negative")
            except Exception as exc:
                logger.exception("UI handler failed")
                ui.notify(f"Unexpected error: {exc}", color="negative")
            finally:
                state["running"] = False
                run_btn.enable()
                run_btn.set_text("Run Task")

        run_btn.on_click(handle_run)
