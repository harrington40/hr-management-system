"""
Modern Timesheet Management System
Refactored for NiceGUI v2.23 compatibility
"""

from nicegui import ui
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Any, Optional
import random

# Enums for status
class TimesheetStatus(Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    LOCKED = "locked"

@dataclass
class TimesheetEntry:
    """Represents a single timesheet entry"""
    employee_id: str
    date: str
    clock_in: str
    clock_out: str
    total_hours: float
    overtime_hours: float
    remote_hours: float
    status: TimesheetStatus
    notes: str = ""
    ai_insights: List[str] = field(default_factory=list)
    anomaly_detected: bool = False

class ModernTimesheetManager:
    """Manages timesheet data and operations"""
    
    def __init__(self):
        self.timesheets: Dict[str, TimesheetEntry] = {}
        self.calculator = self
        self.ai_analyzer = self
        self.load_timesheets()
    
    def load_timesheets(self):
        """Load sample timesheets"""
        base_date = datetime.now()
        employees = ['EMP001', 'EMP002', 'EMP003', 'EMP004', 'EMP005']
        
        for i in range(14):
            current_date = base_date - timedelta(days=i)
            for emp in employees:
                key = f"{emp}_{current_date.strftime('%Y-%m-%d')}"
                hours = random.uniform(7, 10)
                overtime = max(0, hours - 8)
                remote = random.choice([0, 2, 4, 6, 8])
                
                self.timesheets[key] = TimesheetEntry(
                    employee_id=emp,
                    date=current_date.strftime('%Y-%m-%d'),
                    clock_in=f"{random.randint(8, 9):02d}:{random.randint(0, 59):02d}",
                    clock_out=f"{random.randint(17, 18):02d}:{random.randint(0, 59):02d}",
                    total_hours=round(hours, 1),
                    overtime_hours=round(overtime, 1),
                    remote_hours=remote,
                    status=random.choice(list(TimesheetStatus)),
                    ai_insights=['On-time arrival', 'Standard work hours'],
                    anomaly_detected=random.random() < 0.1
                )
    
    def get_timesheets(self):
        """Get all timesheets"""
        return list(self.timesheets.values())[-14:]


def create_modern_timesheet_interface():
    """Modern, refactored timesheet UI for NiceGUI v2.23"""
    manager = ModernTimesheetManager()
    timesheets = manager.get_timesheets()
    user_role = 'hr_admin'
    is_hr = user_role in ['hr_admin', 'payroll_admin', 'system_admin']

    # Calculate analytics
    total_hours    = sum(e.total_hours for e in timesheets)
    avg_hours      = total_hours / len(timesheets) if timesheets else 0
    overtime_hours = sum(e.overtime_hours for e in timesheets)
    remote_days    = sum(1 for e in timesheets if e.remote_hours > 0)
    anomalies      = sum(1 for e in timesheets if e.anomaly_detected)

    # ── KPI card helper ───────────────────────────────────────────────────────
    def kpi_card(icon: str, label: str, value: str, gradient: str, sub: str = ''):
        with ui.card().classes(
            f'flex-1 min-w-0 {gradient} text-white rounded-2xl shadow-lg '
            'transition-transform duration-200 hover:-translate-y-1 hover:shadow-2xl'
        ):
            with ui.card_section().classes('p-5 flex flex-col items-center gap-2 text-center'):
                ui.html(f'<div class="text-4xl mb-1">{icon}</div>')
                ui.html(f'<div class="text-3xl font-extrabold tracking-tight">{value}</div>')
                ui.html(f'<div class="text-sm font-semibold uppercase tracking-widest opacity-80">{label}</div>')
                if sub:
                    ui.html(f'<div class="text-xs opacity-60 mt-1">{sub}</div>')

    # ── Main layout ───────────────────────────────────────────────────────────
    with ui.column().classes('w-full bg-gradient-to-br from-slate-100 to-blue-50 min-h-screen p-6 gap-6'):

        # ── Header ────────────────────────────────────────────────────────────
        with ui.card().classes('w-full rounded-2xl shadow-md bg-gradient-to-r from-blue-700 to-indigo-700 text-white'):
            with ui.card_section().classes('px-8 py-6'):
                with ui.row().classes('w-full items-center justify-between'):
                    with ui.column().classes('gap-1'):
                        ui.html('<h1 class="text-3xl font-extrabold tracking-tight flex items-center gap-3">'
                                '⏰ Timesheet Management</h1>')
                        ui.html('<p class="text-blue-100 text-sm">AI-powered time tracking &amp; workforce analytics</p>')
                    with ui.row().classes('gap-3'):
                        if is_hr:
                            ui.button('Export', icon='download').props('outline color=white')
                            ui.button('Sync',   icon='refresh').props('outline color=white')

        # ── KPI Cards ─────────────────────────────────────────────────────────
        with ui.row().classes('w-full gap-4 flex-nowrap'):
            kpi_card('🕐', 'Total Hours',    f'{total_hours:.1f}h',    'bg-gradient-to-br from-emerald-500 to-emerald-700')
            kpi_card('📊', 'Avg Daily Hrs',  f'{avg_hours:.1f}h',      'bg-gradient-to-br from-blue-500 to-blue-700')
            kpi_card('⚡', 'Overtime',        f'{overtime_hours:.1f}h', 'bg-gradient-to-br from-orange-500 to-orange-700')
            kpi_card('🏠', 'Remote Days',     str(remote_days),         'bg-gradient-to-br from-purple-500 to-purple-700')
            kpi_card('🚨', 'Anomalies',       str(anomalies),           'bg-gradient-to-br from-rose-500 to-rose-700',
                     'Flagged entries')

        # ── Timesheet Table ───────────────────────────────────────────────────
        with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden'):
            with ui.card_section().classes('px-6 pt-6 pb-2'):
                with ui.row().classes('w-full justify-between items-center mb-4'):
                    ui.html('<h2 class="text-xl font-bold text-gray-800 flex items-center gap-2">'
                            '📋 Recent Timesheets</h2>')
                    ui.html(f'<span class="text-xs text-gray-400 bg-gray-100 px-3 py-1 rounded-full">'
                            f'Showing {min(10, len(timesheets))} entries</span>')

            # Scrollable full-width table
            with ui.element('div').classes('w-full overflow-x-auto px-2 pb-4'):
                with ui.element('table').classes('w-full min-w-full border-collapse'):

                    # ── Table header ──────────────────────────────────────────
                    with ui.element('thead'):
                        with ui.element('tr').classes(
                            'bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-sm'
                        ):
                            col_classes = 'px-4 py-3 text-left font-semibold tracking-wide uppercase whitespace-nowrap'
                            headers = [
                                ('👤', 'Employee'), ('📅', 'Date'), ('🟢', 'Clock In'),
                                ('🔴', 'Clock Out'), ('⏱', 'Total Hrs'), ('⚡', 'Overtime'),
                                ('🏠', 'Remote'),   ('🏷', 'Status'),   ('⚙', 'Actions'),
                            ]
                            for icon_h, text_h in headers:
                                with ui.element('th').classes(col_classes):
                                    ui.html(f'{icon_h} {text_h}')

                    # ── Table body ────────────────────────────────────────────
                    with ui.element('tbody'):
                        status_colors = {
                            'approved':      'bg-emerald-100 text-emerald-800',
                            'pending':       'bg-yellow-100 text-yellow-800',
                            'rejected':      'bg-red-100 text-red-800',
                            'draft':         'bg-slate-100 text-slate-700',
                            'submitted':     'bg-blue-100 text-blue-800',
                            'in_review':     'bg-indigo-100 text-indigo-800',
                            'locked':        'bg-purple-100 text-purple-800',
                        }
                        for idx, entry in enumerate(timesheets[:10]):
                            stripe = 'bg-slate-50' if idx % 2 == 0 else 'bg-white'
                            anomaly_ring = 'ring-2 ring-rose-400' if entry.anomaly_detected else ''
                            td = 'px-4 py-3 text-sm text-gray-700 whitespace-nowrap'

                            with ui.element('tr').classes(
                                f'{stripe} {anomaly_ring} border-b border-gray-100 '
                                'hover:bg-blue-50 transition-colors duration-150'
                            ):
                                # Employee
                                with ui.element('td').classes(td):
                                    ui.html(f'<span class="font-semibold text-blue-700">{entry.employee_id}</span>'
                                            + (' <span class="text-rose-500 text-xs">⚠</span>' if entry.anomaly_detected else ''))

                                # Date
                                with ui.element('td').classes(td):
                                    ui.label(entry.date)

                                # Clock In
                                with ui.element('td').classes(td):
                                    ui.html(f'<span class="text-emerald-600 font-medium">🟢 {entry.clock_in}</span>')

                                # Clock Out
                                with ui.element('td').classes(td):
                                    ui.html(f'<span class="text-rose-500 font-medium">🔴 {entry.clock_out}</span>')

                                # Total Hours
                                with ui.element('td').classes(td):
                                    ui.html(f'<span class="font-bold text-gray-900">{entry.total_hours:.1f}h</span>')

                                # Overtime
                                with ui.element('td').classes(td):
                                    if entry.overtime_hours > 0:
                                        ui.html(f'<span class="text-orange-600 font-bold">+{entry.overtime_hours:.1f}h</span>')
                                    else:
                                        ui.html('<span class="text-gray-400">—</span>')

                                # Remote
                                with ui.element('td').classes(td):
                                    if entry.remote_hours > 0:
                                        ui.html(f'<span class="text-purple-600 font-medium">🏠 {entry.remote_hours}h</span>')
                                    else:
                                        ui.html('<span class="text-gray-400 text-xs">On-site</span>')

                                # Status badge
                                with ui.element('td').classes(td):
                                    cls = status_colors.get(entry.status.value, 'bg-gray-100 text-gray-700')
                                    label_text = entry.status.value.replace('_', ' ').title()
                                    ui.html(f'<span class="{cls} px-3 py-1 rounded-full text-xs font-bold">{label_text}</span>')

                                # Actions
                                with ui.element('td').classes(td):
                                    with ui.row().classes('gap-1'):
                                        ui.button(icon='visibility').props('flat round dense color=blue size=sm')
                                        if is_hr:
                                            ui.button(icon='edit').props('flat round dense color=indigo size=sm')

        # ── Footer ────────────────────────────────────────────────────────────
        with ui.card().classes('w-full rounded-2xl shadow-sm bg-white'):
            with ui.card_section().classes('px-6 py-4'):
                with ui.row().classes('w-full justify-between items-center'):
                    ui.html('<p class="text-xs text-gray-400">🤖 AI-enhanced timesheet data — '
                            'HR roles can edit entries.</p>')
                    ui.html(f'<p class="text-xs text-gray-400">Last updated: '
                            f'{datetime.now().strftime("%d %b %Y, %H:%M")}</p>')


def create_modern_timesheet_management_page():
    """Main page function for modern timesheet management"""
    create_modern_timesheet_interface()


# Backward compatibility
def register_modern_timesheet_routes():
    """Register modern timesheet routes"""
    pass


def generate_sample_modern_data():
    """Generate sample modern timesheet data"""
    manager = ModernTimesheetManager()
    return manager.get_timesheets()
