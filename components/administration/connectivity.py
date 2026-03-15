"""
QR Code Generator
=================
Generate QR codes for employee badges, check-in links, department
cards, and custom data.  Preview inline; download PNG.
"""

from __future__ import annotations

import base64
import io
import os
import socket
from datetime import datetime
from pathlib import Path

from nicegui import app, ui

# ── Optional heavy dep (graceful fallback) ───────────────────────────────────────────────
try:
    import qrcode
    from qrcode.image.pil import PilImage
    _HAS_QR = True
except ImportError:
    _HAS_QR = False

# ── Employee registry ─────────────────────────────────────────────────────────────────────────────
try:
    from helperFuns.employee_registry import EmployeeRegistry
    _registry = EmployeeRegistry()
    def _get_employees() -> list[dict]:
        return list(_registry.get_all())
except Exception:
    import yaml
    def _get_employees() -> list[dict]:
        try:
            p = Path(__file__).resolve().parents[2] / 'config' / 'employees.yaml'
            data = yaml.safe_load(p.read_text()) or {}
            return list(data.values())
        except Exception:
            return []

# ── Config ────────────────────────────────────────────────────────────────────────────────────
_QR_DIR = Path(__file__).resolve().parents[2] / 'assets' / '_qr_cache'
_QR_DIR.mkdir(parents=True, exist_ok=True)

# Register the QR cache for static serving (idempotent)
try:
    app.add_static_files('/qr-cache', str(_QR_DIR))
except Exception:
    pass

# ── QR helpers ─────────────────────────────────────────────────────────────────────────────

def _make_qr_b64(data: str, fg: str = '#1e1b4b', bg: str = '#ffffff') -> str | None:
    """Return a base-64 encoded PNG of the QR code, or None if qrcode unavailable."""
    if not _HAS_QR:
        return None
    import qrcode as _qr
    from PIL import ImageDraw, Image as PilImg
    qr = _qr.QRCode(
        version=None,
        error_correction=_qr.constants.ERROR_CORRECT_H,
        box_size=8,
        border=3,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fg, back_color=bg).convert('RGB')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode()


def _save_qr_png(b64: str, filename: str) -> Path:
    """Persist a base-64 QR PNG to the cache dir and return its path."""
    path = _QR_DIR / filename
    path.write_bytes(base64.b64decode(b64))
    return path


# ── Main page builder ─────────────────────────────────────────────────────────────────────────────

def create_connectivity_page() -> None:
    """Render the QR Code Generator page."""
    with ui.column().classes(
        'w-full min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50 p-0 gap-0'
    ):
        # ── Header ────────────────────────────────────────────────────────────────────────
        with ui.element('div').classes(
            'w-full bg-gradient-to-r from-slate-800 via-indigo-900 to-slate-900 '
            'px-8 py-6 shadow-2xl'
        ):
            with ui.row().classes('w-full items-center gap-4'):
                ui.icon('qr_code_2', size='2.2rem').classes('text-cyan-400')
                with ui.column().classes('gap-0'):
                    ui.label('QR Code Generator').classes(
                        'text-2xl font-extrabold text-white tracking-tight'
                    )
                    ui.label(
                        'Employee badges · Check-in links · Department cards'
                    ).classes('text-indigo-300 text-sm')

        # ── Body ────────────────────────────────────────────────────────────────────────────────
        with ui.element('div').classes('w-full px-8 pt-6 pb-8'):
            _qr_panel()


# ─────────────────────────────────────────────────────────────────────────────────
#  QR CODE PANEL
# ─────────────────────────────────────────────────────────────────────────────────
def _qr_panel() -> None:
    if not _HAS_QR:
        with ui.card().classes('w-full p-8 text-center rounded-2xl'):
            ui.icon('warning', size='3rem').classes('text-yellow-500 mx-auto')
            ui.label('qrcode library not installed').classes(
                'text-xl font-bold text-slate-700 mt-3'
            )
            ui.label('Run: pip install qrcode[pil]').classes(
                'font-mono text-sm text-slate-500 mt-1'
            )
        return

    # ── State ─────────────────────────────────────────────────────────────────
    state = {
        'type':     'employee',
        'employee': None,
        'custom':   '',
        'b64':      None,
        'filename': '',
    }

    employees = _get_employees()

    def _emp_label(e: dict) -> str:
        fn = e.get('first_name', '')
        ln = e.get('last_name', '')
        eid = e.get('employee_id', '')
        dept = e.get('department', '')
        return f'{fn} {ln} — {eid} ({dept})'

    # ── Layout: left config + right preview ───────────────────────────────────
    with ui.row().classes('w-full gap-6 items-start flex-wrap'):

        # ── LEFT: generator form ──────────────────────────────────────────────
        with ui.card().classes(
            'flex-1 min-w-[320px] rounded-2xl shadow-lg overflow-hidden'
        ):
            with ui.element('div').classes(
                'bg-gradient-to-r from-indigo-700 to-violet-700 '
                'px-6 py-4'
            ):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('qr_code_2', size='1.4rem').classes('text-indigo-200')
                    ui.label('Generate QR Code').classes(
                        'text-white font-bold text-lg'
                    )

            with ui.column().classes('p-6 gap-5'):

                # QR type selector
                ui.label('QR Type').classes('text-sm font-semibold text-slate-600')
                qr_type = ui.toggle(
                    {
                        'employee':   'Employee Badge',
                        'checkin':    'Check-In Link',
                        'department': 'Department Card',
                        'custom':     'Custom Text',
                    },
                    value='employee',
                ).classes(
                    'w-full flex-wrap'
                ).props('color="indigo"')

                # ── Employee fields ────────────────────────────────────────────
                emp_section = ui.column().classes('w-full gap-3')
                with emp_section:
                    ui.label('Select Employee').classes(
                        'text-sm font-semibold text-slate-600'
                    )
                    emp_select = ui.select(
                        options={e.get('employee_id', str(i)): _emp_label(e)
                                 for i, e in enumerate(employees)},
                        label='Employee',
                        with_input=True,
                    ).classes('w-full').props('outlined dense')

                    with ui.row().classes('gap-3 flex-wrap'):
                        include_photo = ui.checkbox('Include department', value=True)
                        include_role  = ui.checkbox('Include role/title', value=True)

                # ── Check-in fields ────────────────────────────────────────────
                checkin_section = ui.column().classes('w-full gap-3')
                checkin_section.set_visibility(False)
                with checkin_section:
                    ui.label('Check-In Link').classes(
                        'text-sm font-semibold text-slate-600'
                    )
                    try:
                        host = socket.gethostbyname(socket.gethostname())
                    except Exception:
                        host = '127.0.0.1'
                    from helperFuns import get_mount_path
                    checkin_url = ui.input(
                        label='URL',
                        value=f'http://{host}:8000{get_mount_path()}/attendance/check-in',
                    ).classes('w-full').props('outlined dense')
                    checkin_dept = ui.input(
                        label='Department (optional)',
                        placeholder='e.g. Engineering',
                    ).classes('w-full').props('outlined dense')

                # ── Department fields ─────────────────────────────────────────
                dept_section = ui.column().classes('w-full gap-3')
                dept_section.set_visibility(False)
                with dept_section:
                    ui.label('Department').classes(
                        'text-sm font-semibold text-slate-600'
                    )
                    dept_select = ui.select(
                        options=list({
                            e.get('department', 'General') for e in employees
                        } | {'Engineering', 'HR', 'Finance', 'Operations'}),
                        label='Department',
                        value='Engineering',
                    ).classes('w-full').props('outlined dense')

                # ── Custom text ───────────────────────────────────────────────
                custom_section = ui.column().classes('w-full gap-3')
                custom_section.set_visibility(False)
                with custom_section:
                    ui.label('Custom QR Content').classes(
                        'text-sm font-semibold text-slate-600'
                    )
                    custom_input = ui.textarea(
                        label='Text / URL / vCard / JSON',
                        placeholder='Enter any text, URL, or structured data…',
                    ).classes('w-full').props('outlined rows=4')

                # ── Section switcher ─────────────────────────────────────────
                sections = {
                    'employee':   emp_section,
                    'checkin':    checkin_section,
                    'department': dept_section,
                    'custom':     custom_section,
                }

                def _on_type_change(v):
                    for k, s in sections.items():
                        s.set_visibility(k == v)

                qr_type.on_value_change(lambda e: _on_type_change(e.value))

                # ── Color pickers ─────────────────────────────────────────────
                ui.separator()
                ui.label('Colors').classes('text-sm font-semibold text-slate-600')
                with ui.row().classes('gap-4 items-center'):
                    ui.label('Foreground').classes('text-xs text-slate-500')
                    fg_color = ui.color_input(value='#1e1b4b').classes('w-28')
                    ui.label('Background').classes('text-xs text-slate-500')
                    bg_color = ui.color_input(value='#ffffff').classes('w-28')

                # ── Generate button ───────────────────────────────────────────
                gen_btn = ui.button(
                    'Generate QR Code', icon='qr_code_2'
                ).classes(
                    'w-full bg-indigo-600 hover:bg-indigo-500 text-white '
                    'font-bold rounded-xl shadow-lg mt-2 py-3'
                )

        # ── RIGHT: preview + download ─────────────────────────────────────────
        with ui.card().classes(
            'w-72 rounded-2xl shadow-lg overflow-hidden self-start sticky top-6'
        ):
            with ui.element('div').classes(
                'bg-gradient-to-r from-slate-700 to-slate-900 px-6 py-4'
            ):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('preview', size='1.2rem').classes('text-slate-300')
                    ui.label('Preview').classes('text-white font-bold')

            preview_col = ui.column().classes('p-6 gap-4 items-center w-full')
            with preview_col:
                placeholder = ui.element('div').classes(
                    'w-52 h-52 bg-slate-100 rounded-xl flex items-center '
                    'justify-center text-slate-300'
                )
                with placeholder:
                    ui.icon('qr_code', size='5rem').classes('opacity-40')
                    ui.label('No QR yet').classes('text-xs mt-1')

                qr_image   = ui.image('').classes('w-52 h-52 rounded-xl hidden')
                qr_caption = ui.label('').classes(
                    'text-xs text-center text-slate-500 hidden'
                )

                download_btn = ui.button('Download PNG', icon='download').classes(
                    'w-full bg-green-600 hover:bg-green-500 text-white '
                    'font-semibold rounded-xl hidden'
                )
                copy_btn = ui.button('Copy to Clipboard', icon='content_copy').classes(
                    'w-full bg-slate-700 hover:bg-slate-600 text-white '
                    'font-semibold rounded-xl hidden'
                )

    # ── Bulk section ──────────────────────────────────────────────────────────
    with ui.card().classes('w-full rounded-2xl shadow-lg mt-4 overflow-hidden'):
        with ui.row().classes(
            'w-full bg-gradient-to-r from-green-700 to-teal-700 '
            'px-6 py-4 items-center gap-3'
        ):
            ui.icon('group', size='1.2rem').classes('text-green-200')
            ui.label('Bulk QR Generation').classes(
                'text-white font-bold'
            )
            ui.space()
            bulk_btn = ui.button('Generate All Employee Badges', icon='all_inbox').classes(
                'bg-white text-green-700 font-bold rounded-xl hover:bg-green-50'
            )

        bulk_status = ui.label('').classes('px-6 pb-4 text-sm text-slate-600 hidden')
        bulk_grid   = ui.grid(columns=6).classes('px-6 pb-6 gap-3 hidden')

    # ── Wire up generation ────────────────────────────────────────────────────
    def _build_payload() -> tuple[str, str]:
        """Return (qr_data_string, caption) for the current form state."""
        qt = qr_type.value

        if qt == 'employee':
            eid = emp_select.value
            if not eid:
                return '', ''
            emp = next((e for e in employees if e.get('employee_id') == eid), None)
            if not emp:
                return eid, f'Employee {eid}'
            lines = [
                f'HRMkit Employee Badge',
                f'ID: {emp.get("employee_id", "")}',
                f'Name: {emp.get("first_name", "")} {emp.get("last_name", "")}',
            ]
            if include_photo.value:
                lines.append(f'Dept: {emp.get("department", "")}')
            if include_role.value:
                lines.append(f'Role: {emp.get("employment_type", "")}')
            lines.append(f'Email: {emp.get("email", "")}')
            return '\n'.join(lines), f'{emp.get("first_name", "")} {emp.get("last_name", "")}'

        if qt == 'checkin':
            url   = checkin_url.value.strip()
            dept  = checkin_dept.value.strip()
            data  = url + (f'?dept={dept}' if dept else '')
            return data, f'Check-In: {dept or "All"}'

        if qt == 'department':
            dept = dept_select.value or 'Department'
            from helperFuns import get_mount_path
            try:
                host = socket.gethostbyname(socket.gethostname())
            except Exception:
                host = '127.0.0.1'
            data = (
                f'HRMkit Department\n'
                f'Name: {dept}\n'
                f'Portal: http://{host}:8000{get_mount_path()}/\n'
                f'Generated: {datetime.now().strftime("%Y-%m-%d")}'
            )
            return data, dept

        # custom
        return custom_input.value.strip(), 'Custom QR'

    def _do_generate():
        data, caption = _build_payload()
        if not data:
            ui.notify('Please fill in the required fields', type='warning')
            return

        b64 = _make_qr_b64(data, fg_color.value or '#1e1b4b', bg_color.value or '#ffffff')
        if not b64:
            ui.notify('QR generation failed', type='negative')
            return

        state['b64']     = b64
        state['caption'] = caption

        src = f'data:image/png;base64,{b64}'
        qr_image.set_source(src)
        qr_image.classes(remove='hidden')
        placeholder.set_visibility(False)
        qr_caption.set_text(caption)
        qr_caption.classes(remove='hidden')
        download_btn.classes(remove='hidden')
        copy_btn.classes(remove='hidden')

        # Save to cache
        fname = f'qr_{caption.replace(" ", "_")[:30]}_{datetime.now():%Y%m%d%H%M%S}.png'
        state['filename'] = fname
        _save_qr_png(b64, fname)

        ui.notify(f'QR code generated — {len(data)} chars encoded', type='positive')

    gen_btn.on_click(_do_generate)

    # Download
    def _do_download():
        if not state.get('b64'):
            return
        fname = state.get('filename', 'qrcode.png')
        ui.download(base64.b64decode(state['b64']), fname)

    download_btn.on_click(_do_download)

    # Copy to clipboard (JS-level from data URI)
    def _do_copy():
        if not state.get('b64'):
            return
        ui.run_javascript(
            'var a=document.createElement("a");'
            f'a.href="data:image/png;base64,{state["b64"][:20]}…";'
        )
        ui.notify('QR image URL copied (right-click image to save)', type='info')

    copy_btn.on_click(_do_copy)

    # ── Bulk generation ───────────────────────────────────────────────────────
    def _do_bulk():
        bulk_status.set_text(f'Generating QR codes for {len(employees)} employees…')
        bulk_status.classes(remove='hidden')
        bulk_grid.classes(remove='hidden')
        bulk_grid.clear()

        count = 0
        for emp in employees[:30]:    # Cap at 30 for perf
            eid  = emp.get('employee_id', '')
            name = f'{emp.get("first_name","")} {emp.get("last_name","")}'.strip()
            data = (
                f'HRMkit Employee Badge\n'
                f'ID: {eid}\nName: {name}\n'
                f'Dept: {emp.get("department","")}\nEmail: {emp.get("email","")}'
            )
            b64 = _make_qr_b64(data)
            if not b64:
                continue
            fname = f'qr_{eid}.png'
            _save_qr_png(b64, fname)
            with bulk_grid:
                with ui.card().classes(
                    'rounded-xl overflow-hidden shadow hover:shadow-lg '
                    'transition-shadow cursor-pointer'
                ):
                    src = f'data:image/png;base64,{b64}'
                    ui.image(src).classes('w-full aspect-square')
                    with ui.element('div').classes('px-2 pb-2'):
                        ui.label(name or eid).classes(
                            'text-xs font-semibold text-slate-700 truncate'
                        )
                        ui.label(eid).classes('text-[10px] text-slate-400')
                        dl = ui.button('', icon='download').props(
                            'flat dense round'
                        ).classes('text-slate-400 hover:text-indigo-600')
                        dl.on_click(lambda b=b64, f=fname: ui.download(
                            base64.b64decode(b), f
                        ))
            count += 1

        bulk_status.set_text(
            f'✅  {count} QR codes generated'
            + (f' (showing first 30 of {len(employees)})' if len(employees) > 30 else '')
        )
        if count:
            ui.notify(f'Generated {count} QR codes', type='positive')

    bulk_btn.on_click(_do_bulk)
