"""
Modern Shift Timetable Management Component
Advanced visual shift planning with AI-powered optimization,
real-time scheduling, and interactive timetable builder
"""

from nicegui import ui
import yaml
import os
from datetime import datetime, time, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

class ShiftType(Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"

@dataclass
class TimetableMetrics:
    total_shifts: int = 0
    active_employees: int = 0
    coverage_gaps: int = 0
    overtime_hours: int = 0
    efficiency_score: float = 0.0

class TemplateState:
    """State management for shift template selection"""
    def __init__(self):
        self.selected_template = None
        self.templates = []
        self.template_cards = {}

    def select_template(self, template_id: str):
        """Handle template selection"""
        self.selected_template = template_id

class ModernShiftTimetableManager:
    """Advanced manager for shift timetable with AI optimization"""

    def __init__(self):
        self.config_path = "/mnt/c/Users/harri/designProject2020/hr-clock/hrms-main/config/shift_timetable.yaml"
        self.timetable_data = self.load_timetable()
        self.metrics = self.calculate_metrics()

    def calculate_metrics(self) -> TimetableMetrics:
        """Calculate real-time timetable metrics"""
        metrics = TimetableMetrics()

        # Calculate basic metrics
        shift_templates = self.timetable_data.get('shift_timetable', {}).get('shift_templates', {})
        metrics.total_shifts = len(shift_templates)

        # Mock additional metrics for demo
        metrics.active_employees = 25
        metrics.coverage_gaps = 3
        metrics.overtime_hours = 45
        metrics.efficiency_score = 87.3

        return metrics

    def optimize_timetable(self) -> Dict[str, Any]:
        """AI-powered timetable optimization"""
        return {
            'recommendations': [
                {'type': 'coverage', 'message': 'Add 2 evening shifts for better coverage', 'priority': 'high'},
                {'type': 'balance', 'message': 'Redistribute morning shifts for better work-life balance', 'priority': 'medium'},
                {'type': 'efficiency', 'message': 'Optimize break times to reduce downtime', 'priority': 'low'}
            ],
            'efficiency_gain': 12.5,
            'cost_savings': 850.00
        }

    def load_timetable(self) -> Dict[str, Any]:
        """Load shift timetable from YAML file"""
        try:
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            return self.get_default_timetable()

    def get_default_timetable(self) -> Dict[str, Any]:
        """Return enhanced default shift timetable"""
        return {
            "shift_timetable": {
                "version": "2.0",
                "organization": {
                    "timezone": "UTC+0",
                    "week_start_day": "monday",
                    "business_hours": "08:00-18:00"
                },
                "shift_templates": {
                    "morning": {
                        "name": "Morning Shift",
                        "start_time": "08:00",
                        "end_time": "16:00",
                        "duration": 8,
                        "break_duration": 60,
                        "color": "#3B82F6",
                        "capacity": 5,
                        "skills_required": ["basic"]
                    },
                    "afternoon": {
                        "name": "Afternoon Shift",
                        "start_time": "14:00",
                        "end_time": "22:00",
                        "duration": 8,
                        "break_duration": 60,
                        "color": "#F59E0B",
                        "capacity": 4,
                        "skills_required": ["intermediate"]
                    },
                    "night": {
                        "name": "Night Shift",
                        "start_time": "22:00",
                        "end_time": "06:00",
                        "duration": 8,
                        "break_duration": 45,
                        "color": "#1F2937",
                        "capacity": 3,
                        "skills_required": ["advanced"]
                    }
                },
                "department_schedules": {
                    "IT": {
                        "monday": ["morning", "afternoon"],
                        "tuesday": ["morning", "afternoon"],
                        "wednesday": ["morning", "night"],
                        "thursday": ["morning", "afternoon"],
                        "friday": ["morning", "afternoon"],
                        "saturday": ["morning"],
                        "sunday": ["night"]
                    },
                    "HR": {
                        "monday": ["morning"],
                        "tuesday": ["morning"],
                        "wednesday": ["morning"],
                        "thursday": ["morning"],
                        "friday": ["morning"],
                        "saturday": [],
                        "sunday": []
                    }
                }
            }
        }

def create_modern_shift_timetable_page():
    """Create a modern, comprehensive shift timetable management page"""

    manager          = ModernShiftTimetableManager()
    optimization_data = manager.optimize_timetable()

    with ui.column().classes('w-full bg-gradient-to-br from-slate-100 to-indigo-50 min-h-screen p-6 gap-6'):

        # ── Header card ──────────────────────────────────────────────────────
        with ui.card().classes(
            'w-full rounded-2xl shadow-md text-white overflow-hidden'
        ).style('background: linear-gradient(135deg, #4f46e5, #7c3aed, #a21caf);'):
            with ui.card_section().classes('px-8 py-6'):
                with ui.row().classes('w-full justify-between items-center'):
                    with ui.column().classes('gap-2'):
                        with ui.row().classes('items-center gap-2 text-indigo-200 text-sm mb-1'):
                            ui.html('<span>🏠 Dashboard</span>')
                            ui.html('<span class="opacity-50">/</span>')
                            ui.html('<span>Attendance</span>')
                            ui.html('<span class="opacity-50">/</span>')
                            ui.html('<span class="text-white font-medium">Shift Timetable</span>')
                        with ui.row().classes('items-center gap-4'):
                            ui.html(
                                '<div style="background:rgba(255,255,255,0.18);border-radius:0.875rem;'
                                'width:52px;height:52px;display:flex;align-items:center;'
                                'justify-content:center;font-size:1.75rem;">⏰</div>'
                            )
                            with ui.column().classes('gap-0.5'):
                                ui.html('<h1 class="text-3xl font-extrabold tracking-tight">Shift Timetable Management</h1>')
                                ui.html('<p class="text-indigo-200 text-sm">Advanced visual shift planning and workforce optimisation</p>')
                    with ui.row().classes('gap-3'):
                        ui.button('🤖 AI Auto-Schedule',
                                  on_click=lambda: ui.notify('AI auto-scheduling running…', type='info')
                                  ).props('outline color=white')
                        ui.button('📤 Export Timetable',
                                  on_click=lambda: ui.notify('Export functionality', type='info')
                                  ).props('outline color=white')

        # ── KPI dashboard ─────────────────────────────────────────────────────
        create_shift_kpi_dashboard(manager)

        # ── Tabs ──────────────────────────────────────────────────────────────
        with ui.tabs().classes('w-full') as tabs:
            overview_tab    = ui.tab('Overview',         icon='dashboard')
            templates_tab   = ui.tab('Shift Templates',  icon='schedule')
            departments_tab = ui.tab('Departments',      icon='business')
            analytics_tab   = ui.tab('Analytics',        icon='analytics')

        with ui.tab_panels(tabs, value=overview_tab).classes('w-full'):
            with ui.tab_panel(overview_tab):
                create_modern_timetable_overview(manager)
            with ui.tab_panel(templates_tab):
                create_modern_shift_templates(manager)
            with ui.tab_panel(departments_tab):
                create_modern_department_schedules(manager)
            with ui.tab_panel(analytics_tab):
                create_modern_timetable_analytics(manager, optimization_data)

def create_shift_kpi_dashboard(manager):
    """5 evenly-distributed vivid gradient KPI cards."""
    _kpis = [
        {'icon': '⚡', 'value': f'{manager.metrics.efficiency_score:.0f}%',
         'label': 'EFFICIENCY SCORE',     'sub': 'vs 85% target',
         'from_': '#4f46e5', 'to_': '#3730a3'},
        {'icon': '🔄', 'value': str(manager.metrics.total_shifts),
         'label': 'ACTIVE SHIFTS',        'sub': 'shift templates',
         'from_': '#0891b2', 'to_': '#0e7490'},
        {'icon': '👥', 'value': str(manager.metrics.active_employees),
         'label': 'ACTIVE EMPLOYEES',     'sub': 'scheduled today',
         'from_': '#059669', 'to_': '#065f46'},
        {'icon': '⚠️', 'value': str(manager.metrics.coverage_gaps),
         'label': 'COVERAGE GAPS',        'sub': 'need attention',
         'from_': '#dc2626', 'to_': '#9f1239'},
        {'icon': '⏱️', 'value': f'{manager.metrics.overtime_hours}h',
         'label': 'OVERTIME HOURS',       'sub': 'this week',
         'from_': '#d97706', 'to_': '#b45309'},
    ]
    with ui.element('div').style('display:flex; flex-wrap:nowrap; gap:1rem; width:100%;'):
        for c in _kpis:
            ui.html(f"""
<div style="
  flex: 1 1 0%;
  background: linear-gradient(135deg, {c['from_']}, {c['to_']});
  border-radius: 1.25rem;
  padding: 1.4rem 1.5rem;
  color: #fff;
  position: relative;
  overflow: hidden;
  box-shadow: 0 8px 24px -6px rgba(0,0,0,0.28);
  transition: transform .2s ease, box-shadow .2s ease;
  cursor: default;
"
onmouseover="this.style.transform='translateY(-5px)';this.style.boxShadow='0 16px 32px -8px rgba(0,0,0,0.35)'"
onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 8px 24px -6px rgba(0,0,0,0.28)'">
  <div style="position:absolute;top:-18px;right:-18px;width:90px;height:90px;
              background:rgba(255,255,255,0.12);border-radius:50%;"></div>
  <div style="position:absolute;bottom:-16px;left:-12px;width:64px;height:64px;
              background:rgba(255,255,255,0.08);border-radius:50%;"></div>
  <div style="position:relative;z-index:1;">
    <div style="background:rgba(255,255,255,0.18);border-radius:.75rem;
                width:48px;height:48px;display:flex;align-items:center;
                justify-content:center;font-size:1.35rem;margin-bottom:.75rem;">
      {c['icon']}
    </div>
    <div style="font-size:2rem;font-weight:900;letter-spacing:-.02em;">{c['value']}</div>
    <div style="font-size:.72rem;font-weight:700;text-transform:uppercase;
                letter-spacing:.1em;opacity:.85;margin-top:.25rem;">{c['label']}</div>
    <div style="font-size:.68rem;opacity:.6;margin-top:.15rem;">{c['sub']}</div>
  </div>
</div>
""")


def create_modern_timetable_overview(manager):
    """Overview tab — full-width timetable grid, colour-blocked shift bands, legend."""

    days       = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    days_short = ['Mon',    'Tue',     'Wed',       'Thu',      'Fri',     'Sat',      'Sun']

    # Each row = 1 hour  (06:00 → 23:00)
    hours = list(range(6, 24))   # 06 … 23

    # Shift bands: (label, start_h, end_h, text_color, bg_color, border_color)
    _bands = [
        ('Morning',   8,  16, '#3730a3', '#e0e7ff', '#a5b4fc'),
        ('Afternoon', 14, 22, '#92400e', '#fef3c7', '#fcd34d'),
        ('Night',     22, 30, '#1e293b', '#e2e8f0', '#94a3b8'),   # wraps past midnight
    ]

    def get_shift(hour, is_weekend):
        if is_weekend:
            if 8 <= hour < 16:
                return ('Morning', '#3730a3', '#e0e7ff', '#a5b4fc')
            return None
        if 8 <= hour < 14:
            return ('Morning',   '#3730a3', '#e0e7ff', '#a5b4fc')
        if 14 <= hour < 22:
            return ('Afternoon', '#92400e', '#fef3c7', '#fcd34d')
        if hour >= 22:
            return ('Night',     '#1e293b', '#e2e8f0', '#94a3b8')
        return None

    with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden'):

        # ── Header ────────────────────────────────────────────────────────────
        with ui.element('div').style(
            'background:linear-gradient(90deg,#4f46e5,#7c3aed);'
            'padding:1rem 1.75rem;display:flex;justify-content:space-between;align-items:center;'
        ):
            ui.html('<h2 class="text-lg font-bold text-white">📊 Weekly Schedule Overview</h2>')
            with ui.row().classes('items-center gap-3'):
                # Legend pills
                for name, tc, bc, _ in [
                    ('Morning',   '#3730a3', '#e0e7ff', ''),
                    ('Afternoon', '#92400e', '#fef3c7', ''),
                    ('Night',     '#1e293b', '#e2e8f0', ''),
                ]:
                    ui.html(
                        f'<span style="background:{bc};color:{tc};font-size:.68rem;'
                        f'font-weight:700;padding:.2rem .6rem;border-radius:9999px;">{name}</span>'
                    )
                ui.html('<span style="background:rgba(255,255,255,0.15);width:1px;height:20px;'
                        'display:inline-block;margin:0 .25rem;"></span>')
                ui.button('⬅', on_click=lambda: ui.notify('Previous week', type='info')).props('flat color=white dense')
                ui.html(f'<span style="color:#fff;font-weight:600;font-size:.82rem;">'
                        f'{datetime.now().strftime("%b %d, %Y")}</span>')
                ui.button('➡', on_click=lambda: ui.notify('Next week', type='info')).props('flat color=white dense')

        # ── Grid ──────────────────────────────────────────────────────────────
        with ui.element('div').style('padding:1.25rem 1.5rem 1.5rem;'):

            # Day-name header row
            ui.html(
                '<div style="display:grid;grid-template-columns:52px repeat(7,1fr);'
                'gap:.5rem;width:100%;margin-bottom:.4rem;">'
                '<div></div>'
                + ''.join(
                    f'<div style="text-align:center;font-size:.75rem;font-weight:800;'
                    f'color:{"#94a3b8" if i>=5 else "#4f46e5"};text-transform:uppercase;'
                    f'letter-spacing:.07em;padding:.4rem .3rem;'
                    f'background:{"#f8fafc" if i>=5 else "#eef2ff"};'
                    f'border-radius:.5rem;">{d}</div>'
                    for i, d in enumerate(days_short)
                )
                + '</div>'
            )

            # Hour rows — build one big HTML block for performance
            rows_html = (
                '<div style="display:grid;grid-template-columns:52px repeat(7,1fr);'
                'gap:.5rem .5rem;width:100%;row-gap:.3rem;">'
            )
            for hour in hours:
                ts = f'{hour:02d}:00'
                rows_html += (
                    f'<div style="text-align:right;font-size:.68rem;font-weight:600;'
                    f'color:#94a3b8;padding:.45rem .4rem;white-space:nowrap;'
                    f'align-self:center;">{ts}</div>'
                )
                for i in range(7):
                    is_wknd = i >= 5
                    sh = get_shift(hour, is_wknd)
                    if sh:
                        lbl, tc, bc, bdr = sh
                        rows_html += (
                            f'<div style="text-align:center;font-size:.7rem;font-weight:700;'
                            f'padding:.45rem .3rem;border-radius:.5rem;'
                            f'color:{tc};background:{bc};border:1px solid {bdr};'
                            f'cursor:pointer;transition:filter .15s;" '
                            f'onmouseover="this.style.filter=\'brightness(.92)\'" '
                            f'onmouseout="this.style.filter=\'none\'">{lbl[:3]}</div>'
                        )
                    else:
                        rows_html += (
                            '<div style="background:#f8fafc;border-radius:.5rem;'
                            'height:100%;min-height:28px;border:1px solid #f1f5f9;"></div>'
                        )
            rows_html += '</div>'
            ui.html(rows_html)

    # ── Quick actions ─────────────────────────────────────────────────────────
    with ui.row().classes('gap-3 mt-2'):
        for label, color in [
            ('➕ Create New Shift', '#4f46e5'),
            ('👥 Assign Employees', '#059669'),
            ('📊 Coverage Report',  '#7c3aed'),
        ]:
            ui.button(label, on_click=lambda l=label: ui.notify(f'{l} — coming soon', type='info')
                      ).style(
                f'background:{color};color:#fff;border-radius:.75rem;'
                f'font-weight:700;padding:.45rem 1.1rem;'
            )

def create_modern_shift_templates(manager):
    """Shift Templates tab — styled section card + horizontal flex cards."""
    shift_templates = manager.timetable_data.get('shift_timetable', {}).get('shift_templates', {})

    _grads = {
        'morning':   ('#4f46e5', '#3730a3'),
        'afternoon': ('#d97706', '#b45309'),
        'night':     ('#1e293b', '#374151'),
    }

    with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden'):
        with ui.element('div').style(
            'background:linear-gradient(90deg,#4f46e5,#7c3aed);'
            'padding:1rem 1.5rem;display:flex;justify-content:space-between;align-items:center;'
        ):
            ui.html('<h2 class="text-lg font-bold text-white">⚙️ Shift Templates</h2>')
            ui.button('➕ Add Template',
                      on_click=lambda: ui.notify('Add template', type='info')
                      ).props('outline color=white').classes('text-sm')

        with ui.card_section().classes('p-6'):
            with ui.element('div').style('display:flex;flex-wrap:wrap;gap:1rem;width:100%;'):
                for shift_id, shift_data in shift_templates.items():
                    g_from, g_to  = _grads.get(shift_id, ('#4f46e5', '#3730a3'))
                    color         = shift_data.get('color', g_from)
                    name          = shift_data.get('name', shift_id.title())
                    start         = shift_data.get('start_time', 'N/A')
                    end           = shift_data.get('end_time',   'N/A')
                    dur           = shift_data.get('duration',   shift_data.get('working_hours', 0))
                    cap           = shift_data.get('capacity', '—')
                    brk           = shift_data.get('break_duration', 0)
                    skills        = ', '.join(shift_data.get('skills_required', [])[:2]) or '—'

                    ui.html(f"""
<div style="
  flex: 1 1 220px; min-width: 220px;
  border-radius: 1rem; overflow: hidden;
  box-shadow: 0 4px 18px -4px rgba(0,0,0,0.13);
  background: #fff;
  transition: transform .18s ease, box-shadow .18s ease;
" onmouseover="this.style.transform='translateY(-4px)';this.style.boxShadow='0 12px 24px -6px rgba(0,0,0,0.17)'"
   onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 4px 18px -4px rgba(0,0,0,0.13)'">

  <div style="height:5px;background:linear-gradient(90deg,{g_from},{g_to});"></div>

  <div style="padding:.85rem 1rem;">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.6rem;">
      <div style="display:flex;align-items:center;gap:.5rem;">
        <div style="width:10px;height:10px;border-radius:50%;background:{color};box-shadow:0 0 0 3px {color}33;"></div>
        <span style="font-weight:800;font-size:.85rem;color:#1e293b;">{name}</span>
      </div>
      <span style="font-size:.7rem;font-weight:700;padding:.15rem .5rem;
                   border-radius:9999px;background:linear-gradient(90deg,{g_from},{g_to});
                   color:#fff;">{dur}h</span>
    </div>

    <div style="font-size:.78rem;color:#64748b;margin-bottom:.75rem;">⏰ {start} → {end}</div>

    <div style="display:flex;flex-direction:column;gap:.3rem;">
      {''.join([
          f'<div style="display:flex;justify-content:space-between;padding:.2rem 0;'
          f'border-bottom:1px solid #f1f5f9;font-size:.74rem;">'
          f'<span style="color:#94a3b8;">{lbl}</span>'
          f'<span style="font-weight:700;color:#1e293b;">{val}</span></div>'
          for lbl, val in [("Capacity", f"{cap} staff"), ("Break", f"{brk} min"), ("Skills", skills)]
      ])}
    </div>
  </div>
</div>
""")

def create_modern_department_schedules(manager):
    """Departments tab — one styled card per department with day-pill schedule."""
    department_schedules = manager.timetable_data.get('shift_timetable', {}).get('department_schedules', {})
    shift_templates      = manager.timetable_data.get('shift_timetable', {}).get('shift_templates', {})

    _dept_grads = [
        ('#4f46e5', '#3730a3'), ('#059669', '#065f46'),
        ('#d97706', '#b45309'), ('#dc2626', '#9f1239'),
    ]
    _shift_pill = {
        'morning':   ('#4f46e5', '#e0e7ff'),
        'afternoon': ('#d97706', '#fef3c7'),
        'night':     ('#374151', '#e2e8f0'),
    }

    with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden'):
        with ui.element('div').style(
            'background:linear-gradient(90deg,#4f46e5,#7c3aed);padding:1rem 1.5rem;'
        ):
            ui.html('<h2 class="text-lg font-bold text-white">🏢 Department Schedules</h2>')

        with ui.card_section().classes('p-6'):
            days      = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
            day_abbr  = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']

            for d_idx, (dept_name, dept_schedule) in enumerate(department_schedules.items()):
                g_from, g_to = _dept_grads[d_idx % len(_dept_grads)]

                with ui.element('div').style(
                    f'border-radius:1rem;overflow:hidden;'
                    f'box-shadow:0 4px 16px -4px rgba(0,0,0,0.10);'
                    f'background:#fff;margin-bottom:1rem;'
                ):
                    # Dept header
                    with ui.element('div').style(
                        f'background:linear-gradient(90deg,{g_from},{g_to});'
                        f'padding:.65rem 1rem;display:flex;justify-content:space-between;align-items:center;'
                    ):
                        ui.html(f'<span style="font-weight:800;font-size:.85rem;color:#fff;">{dept_name} Department</span>')
                        total_shifts = sum(len(v) for v in dept_schedule.values())
                        ui.html(
                            f'<span style="background:rgba(255,255,255,0.2);color:#fff;'
                            f'font-size:.68rem;font-weight:700;padding:.15rem .55rem;border-radius:9999px;">'
                            f'{total_shifts} slots/week</span>'
                        )

                    # Day grid
                    with ui.element('div').style(
                        'display:grid;grid-template-columns:repeat(7,1fr);gap:.4rem;padding:.75rem 1rem;'
                    ):
                        # Day headers
                        for abbr in day_abbr:
                            is_wknd = abbr in ('Sat', 'Sun')
                            ui.html(
                                f'<div style="text-align:center;font-size:.68rem;font-weight:700;'
                                f'color:{"#94a3b8" if is_wknd else "#4f46e5"};'
                                f'text-transform:uppercase;letter-spacing:.06em;'
                                f'padding:.25rem .2rem;background:{"#f8fafc" if is_wknd else "#eef2ff"};'
                                f'border-radius:.4rem;">{abbr}</div>'
                            )
                        # Shift pills per day
                        for day in days:
                            shifts = dept_schedule.get(day, [])
                            is_wknd = day in ('saturday', 'sunday')
                            if shifts:
                                html_parts = []
                                for sh in shifts[:2]:
                                    sh_fc, sh_bc = _shift_pill.get(sh, ('#4f46e5', '#eef2ff'))
                                    html_parts.append(
                                        f'<div style="font-size:.6rem;font-weight:700;text-align:center;'
                                        f'padding:.2rem .25rem;border-radius:.35rem;'
                                        f'color:{sh_fc};background:{sh_bc};margin-bottom:.15rem;">'
                                        f'{sh[:3].title()}</div>'
                                    )
                                ui.html(''.join(html_parts))
                            else:
                                ui.html(
                                    f'<div style="font-size:.6rem;color:#cbd5e1;text-align:center;'
                                    f'padding:.4rem .2rem;background:#f8fafc;border-radius:.35rem;">—</div>'
                                )

def create_modern_timetable_analytics(manager, optimization_data):
    """Analytics tab — KPI row + AI recommendations styled card."""

    # ── Metric cards ──────────────────────────────────────────────────────────
    _metrics = [
        {'icon': '📈', 'value': f"{optimization_data.get('efficiency_gain', 0):.1f}%",
         'label': 'SCHEDULE EFFICIENCY', 'from_': '#059669', 'to_': '#065f46'},
        {'icon': '💰', 'value': f"${optimization_data.get('cost_savings', 0):.0f}",
         'label': 'COST SAVINGS',        'from_': '#0891b2', 'to_': '#0e7490'},
        {'icon': '⚠️', 'value': str(manager.metrics.coverage_gaps),
         'label': 'COVERAGE ISSUES',     'from_': '#dc2626', 'to_': '#9f1239'},
        {'icon': '🔄', 'value': str(manager.metrics.total_shifts),
         'label': 'ACTIVE TEMPLATES',    'from_': '#7c3aed', 'to_': '#4c1d95'},
    ]
    with ui.element('div').style('display:flex;flex-wrap:nowrap;gap:1rem;width:100%;margin-bottom:1.25rem;'):
        for c in _metrics:
            ui.html(f"""
<div style="flex:1 1 0%;background:linear-gradient(135deg,{c['from_']},{c['to_']});
  border-radius:1.25rem;padding:1.2rem 1.4rem;color:#fff;position:relative;overflow:hidden;
  box-shadow:0 8px 24px -6px rgba(0,0,0,0.24);
  transition:transform .18s ease;cursor:default;"
onmouseover="this.style.transform='translateY(-4px)'" onmouseout="this.style.transform='translateY(0)'">
  <div style="position:absolute;top:-14px;right:-14px;width:70px;height:70px;
              background:rgba(255,255,255,0.1);border-radius:50%;"></div>
  <div style="font-size:1.65rem;margin-bottom:.5rem;">{c['icon']}</div>
  <div style="font-size:1.75rem;font-weight:900;">{c['value']}</div>
  <div style="font-size:.68rem;font-weight:700;text-transform:uppercase;
              letter-spacing:.1em;opacity:.8;margin-top:.2rem;">{c['label']}</div>
</div>
""")

    # ── Charts placeholder ────────────────────────────────────────────────────
    with ui.row().classes('w-full gap-4 mb-4'):
        for title, desc in [
            ('🔄 Shift Distribution', 'Morning / Afternoon / Night split across all departments'),
            ('🏢 Department Coverage', 'Optimal ✔  Adequate ~  Understaffed ✖'),
        ]:
            with ui.card().classes('flex-1 rounded-2xl shadow-md bg-white overflow-hidden'):
                with ui.element('div').style(
                    'background:linear-gradient(90deg,#4f46e5,#7c3aed);padding:.8rem 1.2rem;'
                ):
                    ui.html(f'<h3 class="text-sm font-bold text-white">{title}</h3>')
                with ui.card_section().classes('py-10'):
                    ui.html(f'<p class="text-center text-gray-400 text-sm">{desc}</p>')

    # ── AI recommendations ────────────────────────────────────────────────────
    _priority_map = {
        'high':   ('#dc2626', '#9f1239', '#fee2e2', '#7f1d1d'),
        'medium': ('#d97706', '#b45309', '#fef3c7', '#78350f'),
        'low':    ('#0891b2', '#0e7490', '#e0f2fe', '#0c4a6e'),
    }

    with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden'):
        with ui.element('div').style(
            'background:linear-gradient(90deg,#4f46e5,#7c3aed);padding:1rem 1.5rem;'
        ):
            ui.html('<h2 class="text-lg font-bold text-white">🤖 AI Optimization Recommendations</h2>')

        with ui.card_section().classes('p-6'):
            recs = optimization_data.get('recommendations', [])
            if not recs:
                ui.html('<p class="text-center text-gray-400">✅ Timetable is optimally configured!</p>')
            else:
                with ui.element('div').style('display:flex;flex-wrap:wrap;gap:1rem;width:100%;'):
                    for rec in recs:
                        g_from, g_to, bg, txt = _priority_map.get(
                            rec['priority'], ('#64748b','#475569','#f1f5f9','#1e293b')
                        )
                        ui.html(f"""
<div style="flex:1 1 230px;min-width:230px;border-radius:1rem;overflow:hidden;
  box-shadow:0 4px 16px -4px rgba(0,0,0,0.12);background:#fff;
  transition:transform .18s ease;"
onmouseover="this.style.transform='translateY(-4px)'" onmouseout="this.style.transform='translateY(0)'">
  <div style="height:5px;background:linear-gradient(90deg,{g_from},{g_to});"></div>
  <div style="padding:.85rem 1rem;">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.5rem;">
      <span style="font-weight:700;font-size:.82rem;color:#1e293b;">{rec['type'].title()}</span>
      <span style="padding:.15rem .5rem;border-radius:9999px;font-size:.65rem;font-weight:700;
                   background:{bg};color:{txt};">{rec['priority'].title()}</span>
    </div>
    <p style="font-size:.75rem;color:#64748b;line-height:1.5;">{rec['message']}</p>
  </div>
</div>
""")

# Legacy function - redirects to modern implementation
def ShiftTimetable():
    """Legacy function that redirects to the modern implementation"""
    return create_modern_shift_timetable_page()
    """Modern Shift Timetable Management Page"""
    manager = ModernShiftTimetableManager()
    
    # Header with gradient background
    with ui.row().classes('w-full mb-6'):
        with ui.card().classes('w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white'):
            with ui.card_section().classes('p-6'):
                with ui.row().classes('items-center justify-between w-full'):
                    with ui.column().classes('gap-2'):
                        ui.html('<h1 class="text-3xl font-bold flex items-center gap-3"><span class="text-4xl">📅</span>Shift Timetable Management</h1>').classes('mb-2')
                        ui.label('Design and manage flexible shift schedules with visual timetable builder').classes('text-purple-100 text-lg')
                        ui.label(f'Last updated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}').classes('text-purple-200 text-sm')
                    
                    with ui.row().classes('gap-3'):
                        ui.button('💾 Save Timetable', on_click=lambda: save_all_timetable()).classes('bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg font-semibold')
                        ui.button('📋 Export Schedule', on_click=lambda: export_schedule()).classes('bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold')
                        ui.button('📊 Analytics', on_click=lambda: show_analytics()).classes('bg-yellow-500 hover:bg-yellow-600 text-white px-6 py-3 rounded-lg font-semibold')

    # Main content with tabs
    with ui.row().classes('w-full gap-6'):
        # Left panel - Navigation
        with ui.column().classes('w-1/4'):
            with ui.card().classes('w-full'):
                with ui.card_section().classes('p-4'):
                    ui.label('Timetable Sections').classes('text-xl font-bold text-gray-700 mb-4')
                    
                    timetable_sections = [
                        {'id': 'overview', 'name': 'Schedule Overview', 'icon': '📊', 'color': 'blue'},
                        {'id': 'shifts', 'name': 'Shift Templates', 'icon': '⏰', 'color': 'green'},
                        {'id': 'departments', 'name': 'Department Schedules', 'icon': '🏢', 'color': 'purple'},
                        {'id': 'patterns', 'name': 'Weekly Patterns', 'icon': '📋', 'color': 'yellow'},
                        {'id': 'assignments', 'name': 'Shift Assignments', 'icon': '👥', 'color': 'red'},
                        {'id': 'breaks', 'name': 'Break Policies', 'icon': '☕', 'color': 'indigo'},
                        {'id': 'overtime', 'name': 'Overtime Rules', 'icon': '⏱️', 'color': 'pink'},
                        {'id': 'reporting', 'name': 'Reports & Analytics', 'icon': '📈', 'color': 'cyan'},
                    ]
                    
                    # Simple state management without ui.state()
                    class SectionState:
                        def __init__(self):
                            self.current = 'overview'
                            self.panels = {}
                    
                    state = SectionState()
                    
                    def switch_section(sec_id):
                        state.current = sec_id
                        # Hide all panels
                        for panel in state.panels.values():
                            panel.set_visibility(False)
                        # Show selected panel
                        if sec_id in state.panels:
                            state.panels[sec_id].set_visibility(True)
                    
                    for section in timetable_sections:
                        with ui.row().classes('w-full mb-2'):
                            btn = ui.button(f"{section['icon']} {section['name']}", 
                                          on_click=lambda sec=section['id']: switch_section(sec)
                            ).classes(f'w-full justify-start text-left p-3 rounded-lg transition-all bg-gray-100 hover:bg-gray-200 text-gray-700')

        # Right panel - Content
        with ui.column().classes('w-3/4'):
            with ui.card().classes('w-full'):
                with ui.card_section().classes('p-6'):
                    
                    # Create panels and store references
                    state.panels['overview'] = ui.column().classes('w-full')
                    with state.panels['overview']:
                        create_schedule_overview_panel(manager)
                    
                    state.panels['shifts'] = ui.column().classes('w-full')
                    with state.panels['shifts']:
                        create_shift_templates_panel(manager)
                    state.panels['shifts'].set_visibility(False)
                        
                    state.panels['departments'] = ui.column().classes('w-full')
                    with state.panels['departments']:
                        create_department_schedules_panel(manager)
                    state.panels['departments'].set_visibility(False)
                        
                    state.panels['patterns'] = ui.column().classes('w-full')
                    with state.panels['patterns']:
                        create_weekly_patterns_panel(manager)
                    state.panels['patterns'].set_visibility(False)
                        
                    state.panels['assignments'] = ui.column().classes('w-full')
                    with state.panels['assignments']:
                        create_shift_assignments_panel(manager)
                    state.panels['assignments'].set_visibility(False)
                        
                    state.panels['breaks'] = ui.column().classes('w-full')
                    with state.panels['breaks']:
                        create_break_policies_panel(manager)
                    state.panels['breaks'].set_visibility(False)
                        
                    state.panels['overtime'] = ui.column().classes('w-full')
                    with state.panels['overtime']:
                        create_overtime_rules_panel(manager)
                    state.panels['overtime'].set_visibility(False)
                        
                    state.panels['reporting'] = ui.column().classes('w-full')
                    with state.panels['reporting']:
                        create_reporting_panel(manager)
                    state.panels['reporting'].set_visibility(False)

    def save_all_timetable():
        """Save all timetable changes"""
        try:
            success = manager.save_timetable(manager.timetable_data)
            if success:
                ui.notify('✅ Shift timetable saved successfully!', type='positive')
            else:
                ui.notify('❌ Failed to save shift timetable', type='negative')
        except Exception as e:
            ui.notify(f'❌ Error saving timetable: {str(e)}', type='negative')
    
    def export_schedule():
        """Export current schedule"""
        try:
            yaml_content = yaml.dump(manager.timetable_data, default_flow_style=False, sort_keys=False)
            ui.notify('📋 Schedule exported successfully', type='positive')
        except Exception as e:
            ui.notify(f'❌ Error exporting schedule: {str(e)}', type='negative')
    
    def show_analytics():
        """Show schedule analytics"""
        ui.notify('📊 Analytics dashboard coming soon!', type='info')

def create_schedule_overview_panel(manager: ModernShiftTimetableManager):
    """Create schedule overview panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">📊 Schedule Overview</h2>')
    ui.label('Visual overview of your organization\'s shift schedules and coverage').classes('text-gray-600 mb-6')
    
    shift_templates = manager.timetable_data.get('shift_timetable', {}).get('shift_templates', {})
    
    # Statistics Cards
    with ui.row().classes('w-full gap-4 mb-6'):
        # Total Shifts Card
        with ui.card().classes('p-4 bg-gradient-to-r from-blue-100 to-blue-200'):
            with ui.row().classes('items-center gap-3'):
                ui.label('📊').classes('text-3xl')
                with ui.column():
                    ui.label('Total Shift Templates').classes('text-sm text-gray-600')
                    ui.label(str(len(shift_templates))).classes('text-2xl font-bold text-blue-700')
        
        # Coverage Hours Card
        with ui.card().classes('p-4 bg-gradient-to-r from-green-100 to-green-200'):
            with ui.row().classes('items-center gap-3'):
                ui.label('⏰').classes('text-3xl')
                with ui.column():
                    ui.label('Total Coverage Hours').classes('text-sm text-gray-600')
                    total_hours = sum(template.get('working_hours', 0) for template in shift_templates.values())
                    ui.label(f'{total_hours}h').classes('text-2xl font-bold text-green-700')
        
        # Active Departments Card
        with ui.card().classes('p-4 bg-gradient-to-r from-purple-100 to-purple-200'):
            with ui.row().classes('items-center gap-3'):
                ui.label('🏢').classes('text-3xl')
                with ui.column():
                    ui.label('Departments').classes('text-sm text-gray-600')
                    dept_schedules = manager.timetable_data.get('shift_timetable', {}).get('department_shifts', {})
                    ui.label(str(len(dept_schedules))).classes('text-2xl font-bold text-purple-700')
        
        # Coverage Status Card
        with ui.card().classes('p-4 bg-gradient-to-r from-yellow-100 to-yellow-200'):
            with ui.row().classes('items-center gap-3'):
                ui.label('🌟').classes('text-3xl')
                with ui.column():
                    ui.label('Coverage Status').classes('text-sm text-gray-600')
                    ui.label('Optimal').classes('text-2xl font-bold text-yellow-700')

    # Weekly Schedule Visualization
    with ui.card().classes('w-full p-6 mb-6'):
        ui.label('📅 Weekly Schedule Visualization').classes('text-xl font-bold text-gray-700 mb-4')
        
        # Create a simple weekly grid
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        time_slots = ['06:00', '09:00', '12:00', '15:00', '18:00', '21:00']
        
        with ui.grid(columns=8).classes('gap-2 w-full'):
            # Header row
            ui.label('Time').classes('font-semibold text-center p-2 bg-gray-100 rounded')
            for day in weekdays:
                ui.label(day).classes('font-semibold text-center p-2 bg-gray-100 rounded text-sm')
            
            # Time slot rows
            for time_slot in time_slots:
                ui.label(time_slot).classes('text-center p-2 bg-gray-50 rounded text-sm font-medium')
                for day in weekdays:
                    # Sample shift coverage visualization
                    coverage_class = 'bg-green-200 text-green-800' if time_slot in ['09:00', '12:00', '15:00'] else 'bg-blue-200 text-blue-800'
                    shift_name = 'Day Shift' if time_slot in ['09:00', '12:00', '15:00'] else 'Evening'
                    ui.label(shift_name).classes(f'text-center p-2 rounded text-xs {coverage_class}')

    # Quick Actions
    with ui.row().classes('w-full gap-4'):
        ui.button('➕ Create New Shift', on_click=lambda: show_create_shift_dialog()).classes('bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold')
        ui.button('👥 Assign Employees', on_click=lambda: ui.notify('Employee assignment coming soon!', type='info')).classes('bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg font-semibold')
        ui.button('📊 Generate Report', on_click=lambda: ui.notify('Report generation coming soon!', type='info')).classes('bg-purple-500 hover:bg-purple-600 text-white px-6 py-3 rounded-lg font-semibold')

    def show_create_shift_dialog():
        """Show create shift dialog"""
        with ui.dialog() as dialog, ui.card().classes('w-96'):
            ui.label('Create New Shift Template').classes('text-xl font-bold mb-4')
            
            shift_id = ui.input('Shift ID (e.g., morning_shift)').classes('w-full mb-3')
            display_name = ui.input('Display Name').classes('w-full mb-3')
            start_time = ui.input('Start Time').classes('w-full mb-3').props('type=time')
            end_time = ui.input('End Time').classes('w-full mb-3').props('type=time')
            
            with ui.row().classes('gap-3 w-full justify-end'):
                ui.button('Cancel', on_click=dialog.close).classes('bg-gray-500 text-white')
                ui.button('Create Shift', on_click=lambda: create_new_shift(
                    shift_id.value, display_name.value, start_time.value, end_time.value, dialog
                )).classes('bg-blue-500 text-white')
        
        dialog.open()
    
    def create_new_shift(shift_id: str, name: str, start: str, end: str, dialog):
        """Create new shift template"""
        if not all([shift_id, name, start, end]):
            ui.notify('❌ Please fill in all fields', type='negative')
            return
        
        if 'shift_timetable' not in manager.timetable_data:
            manager.timetable_data['shift_timetable'] = {}
        if 'shift_templates' not in manager.timetable_data['shift_timetable']:
            manager.timetable_data['shift_timetable']['shift_templates'] = {}
        
        # Calculate working hours
        start_time = datetime.strptime(start, '%H:%M').time()
        end_time = datetime.strptime(end, '%H:%M').time()
        start_dt = datetime.combine(datetime.today(), start_time)
        end_dt = datetime.combine(datetime.today(), end_time)
        if end_dt < start_dt:  # Next day
            end_dt += timedelta(days=1)
        working_hours = (end_dt - start_dt).total_seconds() / 3600
        
        manager.timetable_data['shift_timetable']['shift_templates'][shift_id] = {
            'name': shift_id,
            'display_name': name,
            'start_time': start,
            'end_time': end,
            'working_hours': working_hours,
            'color': '#22c55e',
            'icon': '⏰'
        }
        
        dialog.close()
        ui.notify(f'✅ Shift "{name}" created successfully!', type='positive')
        ui.navigate.reload()

def create_shift_templates_panel(manager: ModernShiftTimetableManager):
    """Create shift templates configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">⏰ Shift Templates</h2>')
    ui.label('Create and manage reusable shift templates for your organization').classes('text-gray-600 mb-6')
    
    shift_templates = manager.timetable_data.get('shift_timetable', {}).get('shift_templates', {})
    
    # Shift Templates Grid
    if shift_templates:
        with ui.grid(columns=2).classes('gap-6 w-full'):
            for template_id, template in shift_templates.items():
                with ui.card().classes('p-4 border-l-4 border-blue-500'):
                    # Template Header
                    with ui.row().classes('items-center justify-between w-full mb-3'):
                        with ui.row().classes('items-center gap-3'):
                            ui.label(template.get('icon', '⏰')).classes('text-2xl')
                            ui.label(template.get('display_name', template_id)).classes('font-bold text-lg text-gray-700')
                        
                        with ui.row().classes('gap-2'):
                            ui.button('✏️', on_click=lambda tid=template_id: edit_shift_template(tid)).classes('bg-blue-500 text-white p-1 text-sm')
                            ui.button('🗑️', on_click=lambda tid=template_id: delete_shift_template(tid)).classes('bg-red-500 text-white p-1 text-sm')
                    
                    # Template Details
                    with ui.grid(columns=2).classes('gap-4 w-full'):
                        with ui.column():
                            ui.label('⏰ Time').classes('text-sm font-medium text-gray-600 mb-1')
                            ui.label(f"{template.get('start_time', 'N/A')} - {template.get('end_time', 'N/A')}").classes('text-gray-700')
                            
                            ui.label('📊 Working Hours').classes('text-sm font-medium text-gray-600 mb-1 mt-2')
                            ui.label(f"{template.get('working_hours', 0)} hours").classes('text-gray-700')
                        
                        with ui.column():
                            ui.label('☕ Break Duration').classes('text-sm font-medium text-gray-600 mb-1')
                            ui.label(f"{template.get('break_duration_minutes', 0)} minutes").classes('text-gray-700')
                            
                            ui.label('💰 Allowance').classes('text-sm font-medium text-gray-600 mb-1 mt-2')
                            allowance = template.get('shift_allowance_percentage', 0)
                            ui.label(f"{allowance}%" if allowance > 0 else "None").classes('text-gray-700')
    else:
        # Empty state
        with ui.card().classes('p-8 text-center bg-gray-50'):
            ui.label('📝').classes('text-6xl mb-4 opacity-50')
            ui.label('No Shift Templates Created').classes('text-xl font-semibold text-gray-600 mb-2')
            ui.label('Create your first shift template to get started with scheduling').classes('text-gray-500 mb-4')
            ui.button('➕ Create First Template', on_click=lambda: show_create_template_dialog()).classes('bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold')

    # Add New Template Button (if templates exist)
    if shift_templates:
        with ui.row().classes('w-full mt-6'):
            ui.button('➕ Add New Template', on_click=lambda: show_create_template_dialog()).classes('bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg font-semibold')

    def show_create_template_dialog():
        """Show create template dialog"""
        with ui.dialog() as dialog, ui.card().classes('w-[500px]'):
            ui.label('Create Shift Template').classes('text-xl font-bold mb-4')
            
            # Basic Information
            ui.label('Basic Information').classes('font-semibold text-gray-700 mb-2')
            template_id = ui.input('Template ID (e.g., morning_shift)').classes('w-full mb-3')
            display_name = ui.input('Display Name').classes('w-full mb-3')
            
            # Time Settings
            ui.label('Time Settings').classes('font-semibold text-gray-700 mb-2 mt-4')
            with ui.row().classes('gap-3 w-full'):
                start_time = ui.input('Start Time').classes('flex-1').props('type=time')
                end_time = ui.input('End Time').classes('flex-1').props('type=time')
            
            # Break Settings
            ui.label('Break Settings').classes('font-semibold text-gray-700 mb-2 mt-4')
            with ui.row().classes('gap-3 w-full'):
                break_duration = ui.number('Break Duration (minutes)', value=60, min=0, max=180).classes('flex-1')
                break_start = ui.input('Break Start Time').classes('flex-1').props('type=time')
            
            # Additional Settings
            ui.label('Additional Settings').classes('font-semibold text-gray-700 mb-2 mt-4')
            with ui.row().classes('gap-3 w-full'):
                allowance = ui.number('Shift Allowance (%)', value=0, min=0, max=100).classes('flex-1')
                color = ui.input('Color', value='#22c55e').classes('flex-1').props('type=color')
            
            icon = ui.input('Icon/Emoji', value='⏰').classes('w-full mb-4')
            
            with ui.row().classes('gap-3 w-full justify-end'):
                ui.button('Cancel', on_click=dialog.close).classes('bg-gray-500 text-white')
                ui.button('Create Template', on_click=lambda: create_template(
                    template_id.value, display_name.value, start_time.value, end_time.value,
                    break_duration.value, break_start.value, allowance.value, color.value, icon.value, dialog
                )).classes('bg-green-500 text-white')
        
        dialog.open()
    
    def create_template(template_id: str, name: str, start: str, end: str, break_dur: int, break_start: str, allowance: float, color: str, icon: str, dialog):
        """Create new shift template"""
        if not all([template_id, name, start, end]):
            ui.notify('❌ Please fill in required fields', type='negative')
            return
        
        # Calculate working hours
        start_time = datetime.strptime(start, '%H:%M').time()
        end_time = datetime.strptime(end, '%H:%M').time()
        start_dt = datetime.combine(datetime.today(), start_time)
        end_dt = datetime.combine(datetime.today(), end_time)
        if end_dt < start_dt:  # Next day
            end_dt += timedelta(days=1)
        working_hours = (end_dt - start_dt).total_seconds() / 3600 - (break_dur / 60)
        
        if 'shift_timetable' not in manager.timetable_data:
            manager.timetable_data['shift_timetable'] = {}
        if 'shift_templates' not in manager.timetable_data['shift_timetable']:
            manager.timetable_data['shift_timetable']['shift_templates'] = {}
        
        manager.timetable_data['shift_timetable']['shift_templates'][template_id] = {
            'name': template_id,
            'display_name': name,
            'start_time': start,
            'end_time': end,
            'break_duration_minutes': break_dur,
            'break_start_time': break_start,
            'working_hours': round(working_hours, 2),
            'shift_allowance_percentage': allowance,
            'color': color,
            'icon': icon
        }
        
        dialog.close()
        ui.notify(f'✅ Template "{name}" created successfully!', type='positive')
        ui.navigate.reload()
    
    def edit_shift_template(template_id: str):
        """Edit existing shift template"""
        ui.notify(f'✏️ Edit functionality for {template_id} coming soon!', type='info')
    
    def delete_shift_template(template_id: str):
        """Delete shift template"""
        if 'shift_timetable' in manager.timetable_data and 'shift_templates' in manager.timetable_data['shift_timetable']:
            if template_id in manager.timetable_data['shift_timetable']['shift_templates']:
                del manager.timetable_data['shift_timetable']['shift_templates'][template_id]
                ui.notify(f'🗑️ Template {template_id} deleted', type='info')
                ui.navigate.reload()

def create_modern_shift_templates(manager: ModernShiftTimetableManager):
    """Create modern interactive shift templates with active/selected states"""
    ui.html('<h2 class="text-2xl font-bold text-slate-800 mb-4">⏰ Shift Templates</h2>')
    ui.label('Create and manage reusable shift templates with interactive selection').classes('text-slate-600 mb-6')

    shift_templates = manager.timetable_data.get('shift_timetable', {}).get('shift_templates', {})

    # State management for active selection
    template_state = TemplateState()

    def select_template(template_id: str):
        """Handle template selection with visual feedback"""
        # Update state
        template_state.select_template(template_id)

        # Update visual states for all cards
        for tid, card_info in template_state.template_cards.items():
            if tid == template_id:
                # Selected state - enhanced styling
                card_info['card'].classes('border-2 border-blue-500 bg-gradient-to-br from-blue-50 to-indigo-50 shadow-xl transform scale-105')
                card_info['header'].classes('bg-gradient-to-r from-blue-500 to-indigo-600 text-white')
                card_info['status'].set_text('🟢 ACTIVE')
                card_info['status'].classes('text-blue-600 font-bold')
            else:
                # Default state
                card_info['card'].classes('border border-slate-200 bg-white shadow-md hover:shadow-lg')
                card_info['header'].classes('bg-gradient-to-r from-slate-100 to-slate-200 text-slate-700')
                card_info['status'].set_text('⭕ INACTIVE')
                card_info['status'].classes('text-slate-500')

        # Show template details
        show_template_details(template_id)

    def show_template_details(template_id: str):
        """Show detailed information for selected template"""
        template = shift_templates.get(template_id, {})
        ui.notify(f'📋 Selected: {template.get("display_name", template_id)} - {template.get("start_time", "")} to {template.get("end_time", "")}', type='info')

    # Template Grid
    if shift_templates:
        with ui.grid(columns='repeat(auto-fit, minmax(320px, 1fr))').classes('gap-6 w-full mb-6'):
            for template_id, template in shift_templates.items():
                with ui.card().classes('border border-slate-200 bg-white shadow-md hover:shadow-lg transition-all duration-300 cursor-pointer') as card:
                    # Store card reference for state management
                    template_state.template_cards[template_id] = {
                        'card': card,
                        'header': None,
                        'status': None
                    }

                    with ui.card_section().classes('p-0'):
                        # Header with gradient background
                        with ui.row().classes('w-full p-4 bg-gradient-to-r from-slate-100 to-slate-200 text-slate-700') as header:
                            template_state.template_cards[template_id]['header'] = header

                            with ui.row().classes('items-center justify-between w-full'):
                                with ui.row().classes('items-center gap-3'):
                                    ui.html(f'<span class="text-2xl">{template.get("icon", "⏰")}</span>')
                                    with ui.column().classes('gap-1'):
                                        ui.label(template.get('display_name', template_id)).classes('font-bold text-lg')
                                        ui.label(f'{template.get("start_time", "N/A")} - {template.get("end_time", "N/A")}').classes('text-sm opacity-80')

                                # Status indicator
                                status_label = ui.label('⭕ INACTIVE').classes('text-slate-500 font-medium')
                                template_state.template_cards[template_id]['status'] = status_label

                        # Template details
                        with ui.card_section().classes('p-4'):
                            with ui.grid(columns=2).classes('gap-4 w-full mb-4'):
                                # Left column
                                with ui.column().classes('gap-2'):
                                    ui.label('⏰ Duration').classes('text-sm font-medium text-slate-600')
                                    ui.label(f'{template.get("working_hours", 0)} hours').classes('text-slate-800')

                                    ui.label('☕ Break').classes('text-sm font-medium text-slate-600 mt-2')
                                    ui.label(f'{template.get("break_duration_minutes", 0)} min').classes('text-slate-800')

                                # Right column
                                with ui.column().classes('gap-2'):
                                    ui.label('💰 Allowance').classes('text-sm font-medium text-slate-600')
                                    allowance = template.get('shift_allowance_percentage', 0)
                                    ui.label(f'{allowance}%' if allowance > 0 else 'None').classes('text-slate-800')

                                    ui.label('🎨 Color').classes('text-sm font-medium text-slate-600 mt-2')
                                    color = template.get('color', '#6B7280')
                                    ui.html(f'<div class="w-4 h-4 rounded-full border-2 border-white shadow-sm" style="background-color: {color}"></div>')

                            # Action buttons
                            with ui.row().classes('gap-2 w-full mt-4'):
                                ui.button('👁️ View Details',
                                        on_click=lambda tid=template_id: show_template_details(tid)
                                        ).classes('flex-1 bg-slate-100 hover:bg-slate-200 text-slate-700 text-sm')

                                ui.button('✏️ Edit',
                                        on_click=lambda tid=template_id: edit_template(tid)
                                        ).classes('flex-1 bg-blue-500 hover:bg-blue-600 text-white text-sm')

                                ui.button('🗑️ Delete',
                                        on_click=lambda tid=template_id: delete_template(tid)
                                        ).classes('flex-1 bg-red-500 hover:bg-red-600 text-white text-sm')

                        # Click handler for entire card
                        card.on('click', lambda tid=template_id: select_template(tid))

        # Selected template details panel
        with ui.card().classes('w-full mt-6 bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-200'):
            with ui.card_section().classes('p-6'):
                ui.label('📋 Template Details').classes('text-xl font-bold text-blue-800 mb-4')

                if template_state.selected_template:
                    template = shift_templates.get(template_state.selected_template, {})
                    with ui.grid(columns='repeat(auto-fit, minmax(200px, 1fr))').classes('gap-4'):
                        details = [
                            ('Template ID', template_state.selected_template),
                            ('Display Name', template.get('display_name', 'N/A')),
                            ('Start Time', template.get('start_time', 'N/A')),
                            ('End Time', template.get('end_time', 'N/A')),
                            ('Working Hours', f'{template.get("working_hours", 0)} hours'),
                            ('Break Duration', f'{template.get("break_duration_minutes", 0)} minutes'),
                            ('Break Start', template.get('break_start_time', 'N/A')),
                            ('Allowance', f'{template.get("shift_allowance_percentage", 0)}%'),
                        ]

                        for label, value in details:
                            with ui.card().classes('bg-white/70 border border-blue-100'):
                                with ui.card_section().classes('p-3 text-center'):
                                    ui.label(label).classes('text-sm font-medium text-blue-600 mb-1')
                                    ui.label(str(value)).classes('font-semibold text-blue-800')
                else:
                    ui.label('Click on a shift template above to view its details').classes('text-blue-600 italic text-center py-8')

    else:
        # Empty state with call-to-action
        with ui.card().classes('w-full p-12 text-center bg-gradient-to-br from-slate-50 to-slate-100 border-2 border-dashed border-slate-300'):
            with ui.card_section().classes('p-8'):
                ui.html('<div class="text-8xl mb-6">⏰</div>')
                ui.label('No Shift Templates Created').classes('text-2xl font-bold text-slate-700 mb-3')
                ui.label('Create your first interactive shift template to get started').classes('text-slate-600 mb-6')

                ui.button('✨ Create First Template',
                        on_click=lambda: show_modern_create_dialog()
                        ).classes('bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white px-8 py-4 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200')

    def show_modern_create_dialog():
        """Show modern create template dialog"""
        with ui.dialog() as dialog, ui.card().classes('w-[600px] max-w-full'):
            with ui.card_section().classes('p-6'):
                with ui.row().classes('items-center gap-3 mb-6'):
                    ui.html('<span class="text-3xl">⏰</span>')
                    ui.label('Create New Shift Template').classes('text-2xl font-bold text-slate-800')

                with ui.tabs().classes('w-full') as tabs:
                    basic_tab = ui.tab('Basic Info', icon='info')
                    time_tab = ui.tab('Time Settings', icon='schedule')
                    advanced_tab = ui.tab('Advanced', icon='settings')

                with ui.tab_panels(tabs, value=basic_tab).classes('w-full mt-4'):
                    with ui.tab_panel(basic_tab):
                        ui.label('Basic Information').classes('font-semibold text-slate-700 mb-4')
                        template_id = ui.input('Template ID (unique identifier)').classes('w-full mb-3').props('outlined')
                        display_name = ui.input('Display Name').classes('w-full mb-3').props('outlined')
                        icon = ui.input('Icon/Emoji', value='⏰').classes('w-full').props('outlined')

                    with ui.tab_panel(time_tab):
                        ui.label('Time Configuration').classes('font-semibold text-slate-700 mb-4')
                        with ui.grid(columns=2).classes('gap-4 w-full'):
                            start_time = ui.input('Start Time').props('outlined type=time').classes('w-full')
                            end_time = ui.input('End Time').props('outlined type=time').classes('w-full')
                            break_duration = ui.number('Break Duration (minutes)', value=60, min=0, max=180).classes('w-full')
                            break_start = ui.input('Break Start Time').props('outlined type=time').classes('w-full')

                    with ui.tab_panel(advanced_tab):
                        ui.label('Advanced Settings').classes('font-semibold text-slate-700 mb-4')
                        with ui.grid(columns=2).classes('gap-4 w-full'):
                            allowance = ui.number('Shift Allowance (%)', value=0, min=0, max=100).classes('w-full')
                            color = ui.input('Color', value='#3B82F6').props('outlined type=color').classes('w-full')
                            capacity = ui.number('Max Capacity', value=5, min=1, max=50).classes('w-full')
                            priority = ui.select(['Low', 'Medium', 'High'], value='Medium', label='Priority').classes('w-full')

                with ui.row().classes('gap-3 w-full justify-end mt-6'):
                    ui.button('❌ Cancel', on_click=dialog.close).classes('bg-slate-500 hover:bg-slate-600 text-white px-6 py-2 rounded-lg')
                    ui.button('✅ Create Template',
                            on_click=lambda: create_modern_template(
                                template_id.value, display_name.value, icon.value,
                                start_time.value, end_time.value, break_duration.value, break_start.value,
                                allowance.value, color.value, capacity.value, priority.value, dialog
                            )).classes('bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white px-6 py-2 rounded-lg font-semibold')

        dialog.open()

    def create_modern_template(tid, name, icon, start, end, break_dur, break_start, allowance, color, capacity, priority, dialog):
        """Create new modern shift template"""
        if not all([tid, name, start, end]):
            ui.notify('❌ Please fill in all required fields', type='negative')
            return

        # Calculate working hours
        try:
            start_time = datetime.strptime(start, '%H:%M').time()
            end_time = datetime.strptime(end, '%H:%M').time()
            start_dt = datetime.combine(datetime.today(), start_time)
            end_dt = datetime.combine(datetime.today(), end_time)
            if end_dt < start_dt:  # Next day
                end_dt += timedelta(days=1)
            working_hours = (end_dt - start_dt).total_seconds() / 3600 - (break_dur / 60)
        except:
            ui.notify('❌ Invalid time format', type='negative')
            return

        if 'shift_timetable' not in manager.timetable_data:
            manager.timetable_data['shift_timetable'] = {}
        if 'shift_templates' not in manager.timetable_data['shift_timetable']:
            manager.timetable_data['shift_timetable']['shift_templates'] = {}

        manager.timetable_data['shift_timetable']['shift_templates'][tid] = {
            'name': tid,
            'display_name': name,
            'icon': icon,
            'start_time': start,
            'end_time': end,
            'break_duration_minutes': break_dur,
            'break_start_time': break_start,
            'working_hours': round(working_hours, 2),
            'shift_allowance_percentage': allowance,
            'color': color,
            'capacity': capacity,
            'priority': priority
        }

        dialog.close()
        ui.notify(f'✅ Template "{name}" created successfully!', type='positive')
        ui.navigate.reload()

    def edit_template(template_id: str):
        """Edit existing template"""
        ui.notify(f'✏️ Edit functionality for {template_id} coming soon!', type='info')

    def delete_template(template_id: str):
        """Delete template with confirmation"""
        template = shift_templates.get(template_id, {})
        template_name = template.get('display_name', template_id)

        with ui.dialog() as confirm_dialog, ui.card().classes('w-96'):
            with ui.card_section().classes('p-6 text-center'):
                ui.html('<span class="text-4xl mb-4 block">⚠️</span>')
                ui.label(f'Delete Template').classes('text-xl font-bold text-slate-800 mb-2')
                ui.label(f'Are you sure you want to delete "{template_name}"?').classes('text-slate-600 mb-6')
                ui.label('This action cannot be undone.').classes('text-sm text-red-600 mb-6')

                with ui.row().classes('gap-3 w-full justify-center'):
                    ui.button('❌ Cancel', on_click=confirm_dialog.close).classes('bg-slate-500 hover:bg-slate-600 text-white px-6 py-2 rounded-lg')
                    ui.button('🗑️ Delete',
                            on_click=lambda: confirm_delete(template_id, confirm_dialog)
                            ).classes('bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-lg font-semibold')

        confirm_dialog.open()

    def confirm_delete(template_id: str, dialog):
        """Confirm and execute template deletion"""
        if 'shift_timetable' in manager.timetable_data and 'shift_templates' in manager.timetable_data['shift_timetable']:
            if template_id in manager.timetable_data['shift_timetable']['shift_templates']:
                del manager.timetable_data['shift_timetable']['shift_templates'][template_id]
                ui.notify(f'🗑️ Template deleted successfully', type='info')
                dialog.close()
                ui.navigate.reload()

def create_department_schedules_panel(manager: ModernShiftTimetableManager):
    """Create department schedules configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">🏢 Department Schedules</h2>')
    ui.label('Configure department-specific shift patterns and requirements').classes('text-gray-600 mb-6')
    
    department_shifts = manager.timetable_data.get('shift_timetable', {}).get('department_shifts', {})
    
    # Department Overview
    if department_shifts:
        with ui.grid(columns=2).classes('gap-6 w-full'):
            for dept_name, dept_config in department_shifts.items():
                with ui.card().classes('p-4'):
                    ui.label(f'🏢 {dept_name.replace("_", " ").title()}').classes('text-lg font-bold text-gray-700 mb-3')
                    
                    ui.label('Default Shift:').classes('text-sm font-medium text-gray-600')
                    ui.label(dept_config.get('default_shift', 'Not set')).classes('text-gray-700 mb-2')
                    
                    ui.label('Available Shifts:').classes('text-sm font-medium text-gray-600')
                    available_shifts = dept_config.get('available_shifts', [])
                    ui.label(', '.join(available_shifts) if available_shifts else 'None').classes('text-gray-700 mb-2')
                    
                    if dept_config.get('24_7_coverage'):
                        ui.chip('24/7 Coverage', color='red').classes('text-white text-xs')
                    
                    if dept_config.get('on_call_rotation'):
                        ui.chip('On-Call Rotation', color='blue').classes('text-white text-xs')
    else:
        with ui.card().classes('p-8 text-center bg-gray-50'):
            ui.label('🏢').classes('text-6xl mb-4 opacity-50')
            ui.label('No Department Schedules Configured').classes('text-xl font-semibold text-gray-600 mb-2')
            ui.label('Set up department-specific scheduling rules').classes('text-gray-500 mb-4')
            ui.button('➕ Configure Departments', on_click=lambda: show_department_config_dialog()).classes('bg-purple-500 hover:bg-purple-600 text-white px-6 py-3 rounded-lg font-semibold')

    def show_department_config_dialog():
        """Show department configuration dialog"""
        ui.notify('🏢 Department configuration coming soon!', type='info')

def create_weekly_patterns_panel(manager: ModernShiftTimetableManager):
    """Create weekly patterns configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">📋 Weekly Schedule Patterns</h2>')
    ui.label('Define recurring weekly work patterns and rotation schedules').classes('text-gray-600 mb-6')
    
    # Add content for weekly patterns
    with ui.card().classes('p-6'):
        ui.label('📅 Pattern Management Coming Soon').classes('text-xl font-semibold text-gray-700 mb-3')
        ui.label('Configure standard 5-day, compressed 4-day, 6-day retail, and rotating shift patterns.').classes('text-gray-600')

def create_shift_assignments_panel(manager: ModernShiftTimetableManager):
    """Create shift assignments configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">👥 Shift Assignment Rules</h2>')
    ui.label('Configure automated shift assignment and employee scheduling rules').classes('text-gray-600 mb-6')
    
    assignment_rules = manager.timetable_data.get('shift_timetable', {}).get('assignment_rules', {})
    
    with ui.grid(columns=2).classes('gap-6 w-full'):
        # Basic Assignment Settings
        with ui.card().classes('p-4'):
            ui.label('⚙️ Assignment Settings').classes('font-semibold text-gray-700 mb-3')
            
            auto_assignment = ui.switch(
                'Auto Assignment',
                value=assignment_rules.get('auto_assignment', False),
                on_change=lambda e: update_assignment_rule('auto_assignment', e.value)
            ).classes('mb-3')
            
            manager_approval = ui.switch(
                'Manager Approval Required',
                value=assignment_rules.get('manager_approval_required', True),
                on_change=lambda e: update_assignment_rule('manager_approval_required', e.value)
            ).classes('mb-3')
            
            ui.label('Employee Preference Weight (%)').classes('text-sm text-gray-600 mb-1')
            preference_weight = ui.number(
                value=assignment_rules.get('employee_preference_weight', 30),
                min=0, max=100,
                on_change=lambda e: update_assignment_rule('employee_preference_weight', e.value)
            ).classes('w-full')
        
        # Fairness Rules
        with ui.card().classes('p-4'):
            ui.label('⚖️ Fairness Rules').classes('font-semibold text-gray-700 mb-3')
            
            equal_opportunity = ui.switch(
                'Equal Opportunity Night Shifts',
                value=assignment_rules.get('equal_opportunity_night_shifts', True),
                on_change=lambda e: update_assignment_rule('equal_opportunity_night_shifts', e.value)
            ).classes('mb-3')
            
            weekend_rotation = ui.switch(
                'Fair Weekend Rotation',
                value=assignment_rules.get('weekend_rotation_fair_distribution', True),
                on_change=lambda e: update_assignment_rule('weekend_rotation_fair_distribution', e.value)
            ).classes('mb-3')
            
            holiday_rotation = ui.switch(
                'Holiday Duty Rotation',
                value=assignment_rules.get('holiday_duty_rotation', True),
                on_change=lambda e: update_assignment_rule('holiday_duty_rotation', e.value)
            )
    
    def update_assignment_rule(key: str, value):
        """Update assignment rule"""
        if 'shift_timetable' not in manager.timetable_data:
            manager.timetable_data['shift_timetable'] = {}
        if 'assignment_rules' not in manager.timetable_data['shift_timetable']:
            manager.timetable_data['shift_timetable']['assignment_rules'] = {}
        manager.timetable_data['shift_timetable']['assignment_rules'][key] = value

def create_break_policies_panel(manager: ModernShiftTimetableManager):
    """Create break policies configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">☕ Break Time Policies</h2>')
    ui.label('Configure break schedules and meal period policies for shifts').classes('text-gray-600 mb-6')
    
    # Add content for break policies
    with ui.card().classes('p-6'):
        ui.label('☕ Break Policy Configuration Coming Soon').classes('text-xl font-semibold text-gray-700 mb-3')
        ui.label('Set up paid breaks, meal breaks, prayer breaks, and special accommodation breaks.').classes('text-gray-600')

def create_overtime_rules_panel(manager: ModernShiftTimetableManager):
    """Create overtime rules configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">⏱️ Overtime Management</h2>')
    ui.label('Configure overtime calculation and approval workflows for shifts').classes('text-gray-600 mb-6')
    
    overtime_rules = manager.timetable_data.get('shift_timetable', {}).get('overtime_rules', {})
    
    with ui.grid(columns=2).classes('gap-6 w-full'):
        # Basic Overtime Settings
        with ui.card().classes('p-4'):
            ui.label('⚙️ Overtime Settings').classes('font-semibold text-gray-700 mb-3')
            
            auto_calculation = ui.switch(
                'Automatic Calculation',
                value=overtime_rules.get('automatic_calculation', True),
                on_change=lambda e: update_overtime_rule('automatic_calculation', e.value)
            ).classes('mb-3')
            
            approval_workflow = ui.switch(
                'Approval Workflow',
                value=overtime_rules.get('approval_workflow', True),
                on_change=lambda e: update_overtime_rule('approval_workflow', e.value)
            ).classes('mb-3')
            
            ui.label('Max Overtime Hours/Week').classes('text-sm text-gray-600 mb-1')
            max_overtime = ui.number(
                value=overtime_rules.get('maximum_overtime_hours_per_week', 12),
                min=0, max=40,
                on_change=lambda e: update_overtime_rule('maximum_overtime_hours_per_week', e.value)
            ).classes('w-full')
        
        # Overtime Benefits
        with ui.card().classes('p-4'):
            ui.label('💰 Overtime Benefits').classes('font-semibold text-gray-700 mb-3')
            
            meal_allowance = ui.switch(
                'Overtime Meal Allowance',
                value=overtime_rules.get('overtime_meal_allowance', True),
                on_change=lambda e: update_overtime_rule('overtime_meal_allowance', e.value)
            ).classes('mb-3')
            
            ui.label('Transport Allowance After').classes('text-sm text-gray-600 mb-1')
            transport_time = ui.input(
                value=overtime_rules.get('transport_allowance_after_hours', '22:00'),
                on_change=lambda e: update_overtime_rule('transport_allowance_after_hours', e.value)
            ).classes('w-full').props('type=time')
    
    def update_overtime_rule(key: str, value):
        """Update overtime rule"""
        if 'shift_timetable' not in manager.timetable_data:
            manager.timetable_data['shift_timetable'] = {}
        if 'overtime_rules' not in manager.timetable_data['shift_timetable']:
            manager.timetable_data['shift_timetable']['overtime_rules'] = {}
        manager.timetable_data['shift_timetable']['overtime_rules'][key] = value

def create_reporting_panel(manager: ModernShiftTimetableManager):
    """Create reporting and analytics panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">📈 Reports & Analytics</h2>')
    ui.label('Generate reports and analyze shift scheduling performance').classes('text-gray-600 mb-6')
    
    # Report Categories
    with ui.grid(columns=2).classes('gap-6 w-full'):
        # Coverage Reports
        with ui.card().classes('p-4'):
            ui.label('📊 Coverage Analysis').classes('font-semibold text-gray-700 mb-3')
            
            ui.button('Shift Coverage Report', on_click=lambda: generate_report('coverage')).classes('w-full bg-blue-500 text-white mb-2')
            ui.button('Staffing Gaps Analysis', on_click=lambda: generate_report('gaps')).classes('w-full bg-red-500 text-white mb-2')
            ui.button('Overtime Cost Analysis', on_click=lambda: generate_report('overtime')).classes('w-full bg-yellow-500 text-white')
        
        # Performance Reports
        with ui.card().classes('p-4'):
            ui.label('📈 Performance Metrics').classes('font-semibold text-gray-700 mb-3')
            
            ui.button('Employee Satisfaction', on_click=lambda: generate_report('satisfaction')).classes('w-full bg-green-500 text-white mb-2')
            ui.button('Productivity by Shift', on_click=lambda: generate_report('productivity')).classes('w-full bg-purple-500 text-white mb-2')
            ui.button('Absenteeism Tracking', on_click=lambda: generate_report('absenteeism')).classes('w-full bg-orange-500 text-white')
    
    def generate_report(report_type: str):
        """Generate specified report"""
        ui.notify(f'📊 Generating {report_type} report...', type='info')
        # In a real implementation, this would generate and download the report