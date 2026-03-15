"""
Modern Staff Schedule Management Component
Provides advanced weekly/monthly schedule management, AI-powered shift planning,
real-time schedule visualization, and intelligent workforce optimization
"""

from nicegui import ui
import yaml
import os
from datetime import datetime, timedelta, date
import json
from typing import Dict, List, Any, Optional
import calendar
import random
from dataclasses import dataclass
from enum import Enum

class ShiftType(Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"
    OFF = "off"

@dataclass
class ScheduleMetrics:
    total_shifts: int = 0
    understaffed_days: int = 0
    overstaffed_days: int = 0
    pending_requests: int = 0
    coverage_percentage: float = 0.0

class ModernStaffScheduleManager:
    """Advanced manager class for staff schedule with AI-powered optimization"""

    def __init__(self):
        self.config_dir = "config"
        self.schedule_file = os.path.join(self.config_dir, "modern_staff_schedule.yaml")
        self.ensure_config_directory()
        self.schedule_data = self.load_schedule()
        self.metrics = self.calculate_metrics()

    def ensure_config_directory(self):
        """Ensure config directory exists"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

    def calculate_metrics(self) -> ScheduleMetrics:
        """Calculate real-time schedule metrics"""
        metrics = ScheduleMetrics()

        # Calculate coverage metrics
        coverage_data = self.schedule_data.get('coverage_analysis', {})
        total_days = len(coverage_data)
        optimal_days = sum(1 for day in coverage_data.values() if day.get('status') == 'optimal')

        metrics.coverage_percentage = (optimal_days / total_days * 100) if total_days > 0 else 0
        metrics.understaffed_days = sum(1 for day in coverage_data.values() if day.get('status') == 'understaffed')
        metrics.overstaffed_days = sum(1 for day in coverage_data.values() if day.get('status') == 'overstaffed')
        metrics.pending_requests = len([r for r in self.schedule_data.get('schedule_requests', []) if r.get('status') == 'pending'])

        # Calculate total shifts
        assignments = self.schedule_data.get('weekly_schedule', {}).get('assignments', {})
        metrics.total_shifts = sum(1 for emp in assignments.values()
                                 for day in emp.values()
                                 if isinstance(day, dict) and day.get('shift') != 'off')

        return metrics

    def optimize_schedule(self) -> Dict[str, Any]:
        """AI-powered schedule optimization algorithm"""
        assignments = self.schedule_data.get('weekly_schedule', {}).get('assignments', {})
        coverage_reqs = self.schedule_data.get('coverage_analysis', {})

        optimization_results = {
            'recommendations': [],
            'efficiency_score': 85.5,
            'workload_balance': {},
            'shift_distribution': {}
        }

        # Analyze workload balance
        employee_hours = {}
        for emp_id, schedule in assignments.items():
            total_hours = 0
            for day_data in schedule.values():
                if isinstance(day_data, dict) and day_data.get('shift') != 'off':
                    shift = day_data.get('shift')
                    if shift in self.schedule_data.get('shift_templates', {}):
                        duration = self.schedule_data['shift_templates'][shift].get('duration', 8)
                        total_hours += duration
            employee_hours[emp_id] = total_hours

        avg_hours = sum(employee_hours.values()) / len(employee_hours) if employee_hours else 0
        optimization_results['workload_balance'] = {
            emp_id: {'hours': hours, 'deviation': hours - avg_hours}
            for emp_id, hours in employee_hours.items()
        }

        # Generate recommendations
        if self.metrics.understaffed_days > 0:
            optimization_results['recommendations'].append({
                'type': 'coverage',
                'priority': 'high',
                'message': f"Address {self.metrics.understaffed_days} understaffed days",
                'action': 'redistribute_shifts'
            })

        if self.metrics.pending_requests > 0:
            optimization_results['recommendations'].append({
                'type': 'requests',
                'priority': 'medium',
                'message': f"Review {self.metrics.pending_requests} pending schedule requests",
                'action': 'review_requests'
            })

        return optimization_results

    def load_schedule(self) -> Dict[str, Any]:
        """Load staff schedule from YAML file"""
        if os.path.exists(self.schedule_file):
            try:
                with open(self.schedule_file, 'r') as file:
                    return yaml.safe_load(file) or {}
            except Exception as e:
                print(f"Error loading staff schedule: {e}")
                return self.get_default_schedule()
        else:
            default_schedule = self.get_default_schedule()
            self.save_schedule(default_schedule)
            return default_schedule

    def get_default_schedule(self) -> Dict[str, Any]:
        """Get enhanced default schedule configuration"""
        current_date = datetime.now()
        week_start = current_date - timedelta(days=current_date.weekday())

        return {
            'schedule_settings': {
                'week_start_day': 'monday',
                'default_shift_duration': 8,
                'max_hours_per_week': 40,
                'min_rest_hours': 12,
                'shift_change_notice_hours': 24,
                'overtime_threshold': 8,
                'auto_optimization': True,
                'fairness_weight': 0.7,
                'efficiency_weight': 0.3
            },
            'shift_templates': {
                'morning': {
                    'name': 'Morning Shift',
                    'start_time': '09:00',
                    'end_time': '17:00',
                    'break_duration': 60,
                    'color': '#3B82F6',
                    'duration': 8
                },
                'afternoon': {
                    'name': 'Afternoon Shift',
                    'start_time': '13:00',
                    'end_time': '21:00',
                    'break_duration': 60,
                    'color': '#F59E0B',
                    'duration': 8
                },
                'evening': {
                    'name': 'Evening Shift',
                    'start_time': '17:00',
                    'end_time': '01:00',
                    'break_duration': 60,
                    'color': '#8B5CF6',
                    'duration': 8
                },
                'night': {
                    'name': 'Night Shift',
                    'start_time': '23:00',
                    'end_time': '07:00',
                    'break_duration': 60,
                    'color': '#1F2937',
                    'duration': 8
                }
            },
            'weekly_schedule': {
                'week_of': week_start.strftime('%Y-%m-%d'),
                'assignments': {
                    'EMP001': {
                        'name': 'John Smith',
                        'department': 'IT',
                        'monday': {'shift': 'morning', 'status': 'scheduled'},
                        'tuesday': {'shift': 'morning', 'status': 'scheduled'},
                        'wednesday': {'shift': 'morning', 'status': 'scheduled'},
                        'thursday': {'shift': 'morning', 'status': 'scheduled'},
                        'friday': {'shift': 'morning', 'status': 'scheduled'},
                        'saturday': {'shift': 'off', 'status': 'off'},
                        'sunday': {'shift': 'off', 'status': 'off'}
                    },
                    'EMP002': {
                        'name': 'Sarah Johnson',
                        'department': 'HR',
                        'monday': {'shift': 'afternoon', 'status': 'scheduled'},
                        'tuesday': {'shift': 'afternoon', 'status': 'scheduled'},
                        'wednesday': {'shift': 'afternoon', 'status': 'scheduled'},
                        'thursday': {'shift': 'afternoon', 'status': 'scheduled'},
                        'friday': {'shift': 'afternoon', 'status': 'scheduled'},
                        'saturday': {'shift': 'off', 'status': 'off'},
                        'sunday': {'shift': 'off', 'status': 'off'}
                    },
                    'EMP003': {
                        'name': 'Mike Davis',
                        'department': 'Finance',
                        'monday': {'shift': 'morning', 'status': 'scheduled'},
                        'tuesday': {'shift': 'morning', 'status': 'scheduled'},
                        'wednesday': {'shift': 'off', 'status': 'off'},
                        'thursday': {'shift': 'morning', 'status': 'scheduled'},
                        'friday': {'shift': 'morning', 'status': 'scheduled'},
                        'saturday': {'shift': 'morning', 'status': 'scheduled'},
                        'sunday': {'shift': 'off', 'status': 'off'}
                    }
                }
            },
            'schedule_requests': [
                {
                    'id': 'REQ001',
                    'employee_id': 'EMP001',
                    'employee_name': 'John Smith',
                    'request_type': 'shift_change',
                    'requested_date': '2025-10-15',
                    'current_shift': 'morning',
                    'requested_shift': 'afternoon',
                    'reason': 'Doctor appointment in the morning',
                    'status': 'pending',
                    'submitted_date': '2025-10-10',
                    'priority': 'medium'
                },
                {
                    'id': 'REQ002',
                    'employee_id': 'EMP002',
                    'employee_name': 'Sarah Johnson',
                    'request_type': 'time_off',
                    'requested_date': '2025-10-18',
                    'reason': 'Personal appointment',
                    'status': 'approved',
                    'submitted_date': '2025-10-08',
                    'priority': 'high'
                }
            ],
            'coverage_analysis': {
                'monday': {'required': 10, 'scheduled': 8, 'status': 'understaffed'},
                'tuesday': {'required': 10, 'scheduled': 10, 'status': 'optimal'},
                'wednesday': {'required': 10, 'scheduled': 9, 'status': 'adequate'},
                'thursday': {'required': 10, 'scheduled': 10, 'status': 'optimal'},
                'friday': {'required': 10, 'scheduled': 8, 'status': 'understaffed'},
                'saturday': {'required': 6, 'scheduled': 5, 'status': 'adequate'},
                'sunday': {'required': 4, 'scheduled': 3, 'status': 'adequate'}
            }
        }

    def save_schedule(self, data: Dict[str, Any]):
        """Save staff schedule to YAML file"""
        try:
            with open(self.schedule_file, 'w') as file:
                yaml.dump(data, file, default_flow_style=False)
        except Exception as e:
            print(f"Error saving staff schedule: {e}")

def create_modern_staff_schedule_page():
    """Create a modern, comprehensive staff schedule management page"""
    manager = ModernStaffScheduleManager()
    optimization_data = manager.optimize_schedule()

    with ui.column().classes('w-full bg-gradient-to-br from-slate-100 to-blue-50 min-h-screen p-6 gap-6'):

        # ── Gradient Header ──────────────────────────────────────────────────
        with ui.card().classes('w-full rounded-2xl shadow-md text-white overflow-hidden') \
                .style('background: linear-gradient(135deg, #0284c7, #0891b2, #0d9488);'):
            with ui.card_section().classes('px-8 py-6'):
                ui.html('<p style="font-size:.75rem;opacity:.75;letter-spacing:.08em;'
                        'text-transform:uppercase;margin-bottom:.5rem;">Attendance &#8250; Staff Schedule</p>')
                with ui.row().classes('items-center gap-5 w-full justify-between'):
                    with ui.row().classes('items-center gap-5'):
                        ui.html('<div style="width:52px;height:52px;border-radius:.75rem;'
                                'background:rgba(255,255,255,.18);display:flex;align-items:center;'
                                'justify-content:center;font-size:1.6rem;flex-shrink:0;">📅</div>')
                        with ui.column().classes('gap-1'):
                            ui.html('<h1 style="font-size:1.6rem;font-weight:900;margin:0;'
                                    'letter-spacing:-.02em;">Staff Schedule Management</h1>')
                            ui.html('<p style="font-size:.9rem;opacity:.82;margin:0;">'
                                    'Intelligent workforce planning, shift templates &amp; AI-powered optimization</p>')
                    with ui.row().classes('gap-3'):
                        ui.button('➕ Add Shift',
                                 on_click=lambda: ui.notify('Add shift functionality', type='info')
                                 ).style('background:rgba(255,255,255,.18);color:#fff;'
                                        'border:1px solid rgba(255,255,255,.35);border-radius:.75rem;'
                                        'padding:.45rem 1.1rem;font-size:.85rem;font-weight:600;')
                        ui.button('🔄 Optimize',
                                 on_click=lambda: ui.notify('AI optimization running...', type='info')
                                 ).style('background:rgba(255,255,255,.18);color:#fff;'
                                        'border:1px solid rgba(255,255,255,.35);border-radius:.75rem;'
                                        'padding:.45rem 1.1rem;font-size:.85rem;font-weight:600;')
                        ui.button('📊 Export',
                                 on_click=lambda: ui.notify('Exporting schedule...', type='info')
                                 ).style('background:rgba(255,255,255,.18);color:#fff;'
                                        'border:1px solid rgba(255,255,255,.35);border-radius:.75rem;'
                                        'padding:.45rem 1.1rem;font-size:.85rem;font-weight:600;')

        # ── KPI flex cards ───────────────────────────────────────────────────
        _kpis = [
            {'icon': '📊', 'value': f'{manager.metrics.coverage_percentage:.1f}%', 'label': 'COVERAGE RATE',
             'sub': 'Staff coverage', 'f': '#0284c7', 't': '#0891b2'},
            {'icon': '⏳', 'value': str(manager.metrics.pending_requests), 'label': 'PENDING REQUESTS',
             'sub': 'Awaiting approval', 'f': '#f59e0b', 't': '#f97316'},
            {'icon': '👥', 'value': str(manager.metrics.total_shifts), 'label': 'ACTIVE SHIFTS',
             'sub': 'This week', 'f': '#0d9488', 't': '#059669'},
            {'icon': '📈', 'value': f'{optimization_data.get("efficiency_score", 0):.1f}%', 'label': 'EFFICIENCY SCORE',
             'sub': 'AI optimized', 'f': '#7c3aed', 't': '#8b5cf6'},
            {'icon': '⚠️', 'value': str(manager.metrics.understaffed_days), 'label': 'UNDERSTAFFED DAYS',
             'sub': 'Need attention', 'f': '#dc2626', 't': '#e11d48'},
        ]
        with ui.element('div').style('display:flex;flex-wrap:nowrap;gap:1rem;width:100%;'):
            for c in _kpis:
                ui.html(
                    f'<div style="flex:1 1 0%;background:linear-gradient(135deg,{c["f"]},{c["t"]});'
                    'border-radius:1.25rem;padding:1.4rem 1.5rem;color:#fff;position:relative;overflow:hidden;'
                    'box-shadow:0 8px 24px -6px rgba(0,0,0,0.28);transition:transform .2s,box-shadow .2s;"'
                    ' onmouseover="this.style.transform=\'translateY(-5px)\';this.style.boxShadow=\'0 14px 32px -6px rgba(0,0,0,0.35)\'"'
                    ' onmouseout="this.style.transform=\'\';this.style.boxShadow=\'0 8px 24px -6px rgba(0,0,0,0.28)\'">'
                    '<div style="position:absolute;top:-18px;right:-18px;width:90px;height:90px;border-radius:50%;background:rgba(255,255,255,.12);"></div>'
                    '<div style="position:absolute;bottom:-12px;left:-12px;width:64px;height:64px;border-radius:50%;background:rgba(255,255,255,.08);"></div>'
                    f'<div style="width:48px;height:48px;border-radius:.75rem;background:rgba(255,255,255,.18);'
                    f'display:flex;align-items:center;justify-content:center;font-size:1.4rem;margin-bottom:.75rem;">{c["icon"]}</div>'
                    f'<div style="font-size:2rem;font-weight:900;letter-spacing:-.03em;line-height:1;">{c["value"]}</div>'
                    f'<div style="font-size:.72rem;text-transform:uppercase;letter-spacing:.1em;opacity:.8;margin-top:.3rem;">{c["label"]}</div>'
                    f'<div style="font-size:.68rem;opacity:.6;margin-top:.15rem;">{c["sub"]}</div></div>'
                )

        # ── AI Banner (when recommendations exist) ───────────────────────────
        if optimization_data.get('recommendations'):
            with ui.card().classes('w-full rounded-2xl shadow-md overflow-hidden') \
                    .style('background:linear-gradient(135deg,#7c3aed11,#0891b211);border:1px solid #7c3aed33;'):
                with ui.card_section().classes('px-6 py-4'):
                    with ui.row().classes('items-center gap-4 w-full'):
                        ui.html('<div style="font-size:1.8rem;">🤖</div>')
                        with ui.column().classes('flex-1 gap-1'):
                            ui.html('<div style="font-size:1rem;font-weight:700;color:#5b21b6;">AI Schedule Optimization Available</div>')
                            ui.html('<div style="font-size:.85rem;color:#7c3aed;">Intelligent recommendations to improve coverage and fairness</div>')
                        with ui.row().classes('gap-2 items-center'):
                            for rec in optimization_data['recommendations'][:2]:
                                badge_cls = 'bg-red-100 text-red-800' if rec['priority'] == 'high' else 'bg-yellow-100 text-yellow-800'
                                ui.badge(rec['type'].title()).classes(f'{badge_cls} text-xs font-bold')
                            ui.button('View Recommendations',
                                     on_click=lambda: ui.notify('Recommendations panel', type='info')
                                     ).classes('bg-purple-600 text-white hover:bg-purple-700 px-4 py-2 rounded-lg text-sm font-semibold')

        # ── Main Tabs ────────────────────────────────────────────────────────
        with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden'):
            tabs = ui.tabs().classes('w-full border-b border-slate-200')
            with tabs:
                t_weekly    = ui.tab('Weekly View',       icon='calendar_view_week')
                t_monthly   = ui.tab('Monthly Overview',  icon='calendar_month')
                t_templates = ui.tab('Shift Templates',   icon='schedule')
                t_analytics = ui.tab('Analytics',         icon='analytics')

            with ui.tab_panels(tabs, value=t_weekly).classes('w-full'):
                with ui.tab_panel(t_weekly).classes('p-6'):
                    create_modern_weekly_schedule(manager)
                with ui.tab_panel(t_monthly).classes('p-6'):
                    create_modern_monthly_overview(manager)
                with ui.tab_panel(t_templates).classes('p-6'):
                    create_modern_shift_templates(manager)
                with ui.tab_panel(t_analytics).classes('p-6'):
                    create_modern_analytics_dashboard(manager, optimization_data)


def create_modern_weekly_schedule(manager):
    """Create full-width weekly schedule grid with colour-coded shifts"""
    current_week = manager.schedule_data.get('weekly_schedule', {}).get('week_of', 'Current Week')
    assignments  = manager.schedule_data.get('weekly_schedule', {}).get('assignments', {})
    shift_templates = manager.schedule_data.get('shift_templates', {})
    days_short  = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    days_full   = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    # ── Nav bar ──────────────────────────────────────────────────────────────
    with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden mb-4'):
        with ui.element('div').style('background:linear-gradient(90deg,#0284c7,#0891b2);padding:1rem 1.5rem;'):
            with ui.row().classes('items-center justify-between w-full'):
                ui.button('← Prev Week',
                         on_click=lambda: ui.notify('Previous week', type='info')
                         ).style('background:rgba(255,255,255,.18);color:#fff;border:1px solid rgba(255,255,255,.35);'
                                'border-radius:.6rem;padding:.35rem .9rem;font-size:.8rem;font-weight:600;')
                ui.html(f'<div style="font-size:1rem;font-weight:700;color:#fff;">📅 Week of {current_week}</div>')
                ui.button('Next Week →',
                         on_click=lambda: ui.notify('Next week', type='info')
                         ).style('background:rgba(255,255,255,.18);color:#fff;border:1px solid rgba(255,255,255,.35);'
                                'border-radius:.6rem;padding:.35rem .9rem;font-size:.8rem;font-weight:600;')

        with ui.element('div').classes('p-4'):
            if not assignments:
                ui.html('<div style="text-align:center;color:#94a3b8;padding:2rem;font-style:italic;">No schedule data configured</div>')
                return

            # Build legend row from shift templates
            legend_html = '<div style="display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:1rem;">'
            legend_html += '<span style="font-size:.75rem;font-weight:600;color:#475569;align-self:center;">Legend:</span>'
            for sid, sdata in shift_templates.items():
                color = sdata.get('color', '#6B7280')
                name  = sdata.get('name', sid.title())
                legend_html += (
                    f'<span style="display:inline-flex;align-items:center;gap:.3rem;padding:.2rem .6rem;'
                    f'border-radius:9999px;background:{color}22;border:1px solid {color}55;font-size:.72rem;font-weight:600;">'
                    f'<span style="width:8px;height:8px;border-radius:50%;background:{color};"></span>'
                    f'{name}</span>'
                )
            legend_html += '<span style="display:inline-flex;align-items:center;gap:.3rem;padding:.2rem .6rem;border-radius:9999px;background:#f1f5f999;border:1px solid #e2e8f0;font-size:.72rem;font-weight:600;"><span style="width:8px;height:8px;border-radius:50%;background:#94a3b8;"></span>OFF</span>'
            legend_html += '</div>'
            ui.html(legend_html)

            # Grid header
            header = (
                '<div style="display:grid;grid-template-columns:180px repeat(7,1fr);gap:.4rem;margin-bottom:.4rem;">'
                '<div style="padding:.5rem;background:#f1f5f9;border-radius:.5rem;"></div>'
            )
            for d in days_short:
                header += (
                    f'<div style="padding:.5rem;background:linear-gradient(135deg,#0284c7,#0891b2);'
                    f'border-radius:.5rem;text-align:center;font-weight:700;font-size:.8rem;color:#fff;">{d}</div>'
                )
            header += '</div>'
            ui.html(header)

            # Employee rows
            rows_html = '<div style="display:flex;flex-direction:column;gap:.4rem;">'
            for i, (emp_id, emp_data) in enumerate(assignments.items()):
                emp_name = emp_data.get('name', emp_id)
                emp_dept = emp_data.get('department', '')
                row_bg   = '#f8fafc' if i % 2 == 0 else '#fff'
                row_html = (
                    f'<div style="display:grid;grid-template-columns:180px repeat(7,1fr);gap:.4rem;">'
                    f'<div style="padding:.5rem .75rem;background:{row_bg};border-radius:.5rem;'
                    f'border-left:3px solid #0284c7;">'
                    f'<div style="font-weight:600;font-size:.82rem;color:#1e293b;">{emp_name}</div>'
                    f'<div style="font-size:.7rem;color:#94a3b8;">{emp_dept}</div></div>'
                )
                for day in days_full:
                    day_data  = emp_data.get(day, {})
                    shift_key = day_data.get('shift', 'off')
                    if shift_key == 'off':
                        cell = (
                            '<div style="padding:.4rem;text-align:center;font-size:.72rem;font-weight:600;'
                            'background:#f1f5f9;color:#94a3b8;border-radius:.5rem;">OFF</div>'
                        )
                    else:
                        sinfo  = shift_templates.get(shift_key, {})
                        sname  = sinfo.get('name', shift_key.title()).split()[0]
                        scolor = sinfo.get('color', '#6B7280')
                        sstart = sinfo.get('start_time', '')
                        sname_full = sinfo.get('name', shift_key)
                        cell = (
                            f'<div style="padding:.4rem;text-align:center;font-size:.72rem;font-weight:700;'
                            f'background:{scolor}22;color:{scolor};border:1px solid {scolor}44;border-radius:.5rem;'
                            f'cursor:pointer;" title="{sname_full} {sstart}">{sname}</div>'
                        )
                    row_html += cell
                row_html += '</div>'
                rows_html += row_html
            rows_html += '</div>'
            ui.html(rows_html)


def create_modern_monthly_overview(manager):
    """Create modern monthly overview with calendar visualization"""
    with ui.card().classes('w-full bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-200'):
        with ui.card_section().classes('p-6'):
            ui.html('<div class="text-2xl font-bold text-indigo-800 mb-4">📊 Monthly Schedule Overview</div>')
            ui.html('<div class="text-indigo-600 mb-6">Comprehensive monthly view with coverage analysis</div>')

            # Month selector
            with ui.row().classes('items-center gap-4 mb-6'):
                ui.button('⬅️', on_click=lambda: ui.notify('Previous month', type='info')).classes('bg-indigo-100 hover:bg-indigo-200 text-indigo-700 px-3 py-2 rounded-lg')
                ui.html('<div class="text-xl font-bold text-indigo-800">October 2025</div>')
                ui.button('➡️', on_click=lambda: ui.notify('Next month', type='info')).classes('bg-indigo-100 hover:bg-indigo-200 text-indigo-700 px-3 py-2 rounded-lg')

            ui.html('<div class="text-center text-slate-500 py-8">Monthly calendar view would be implemented here with interactive date selection and coverage visualization.</div>')

def create_modern_shift_templates(manager):
    """Create horizontal flex cards for shift templates"""
    shift_templates = manager.schedule_data.get('shift_templates', {})

    # ── Section header ───────────────────────────────────────────────────────
    with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden mb-4'):
        with ui.element('div').style('background:linear-gradient(90deg,#0284c7,#0891b2);padding:1rem 1.5rem;'):
            with ui.row().classes('items-center justify-between w-full'):
                ui.html('<h2 style="font-size:1rem;font-weight:700;color:#fff;margin:0;">⚙️ Shift Templates</h2>')
                ui.button('+ Add Template',
                         on_click=lambda: ui.notify('Add template dialog', type='info')
                         ).style('background:rgba(255,255,255,.18);color:#fff;border:1px solid rgba(255,255,255,.35);'
                                'border-radius:.6rem;padding:.3rem .8rem;font-size:.8rem;font-weight:600;')

    # ── Horizontal flex cards ────────────────────────────────────────────────
    if not shift_templates:
        ui.html('<div style="text-align:center;color:#94a3b8;padding:2rem;font-style:italic;">No shift templates configured</div>')
        return

    with ui.element('div').style('display:flex;flex-wrap:wrap;gap:1rem;width:100%;'):
        for shift_id, shift_data in shift_templates.items():
            color      = shift_data.get('color', '#6B7280')
            name       = shift_data.get('name', shift_id.title())
            start_time = shift_data.get('start_time', 'N/A')
            end_time   = shift_data.get('end_time', 'N/A')
            emp_count  = shift_data.get('min_staff', shift_data.get('required_staff', '—'))

            # Determine gradient from color
            ui.html(
                f'<div style="flex:1 1 220px;border-radius:1rem;overflow:hidden;'
                'box-shadow:0 4px 18px -4px rgba(0,0,0,0.12);background:#fff;'
                'transition:transform .2s,box-shadow .2s;"'
                ' onmouseover="this.style.transform=\'translateY(-4px)\';this.style.boxShadow=\'0 10px 28px -6px rgba(0,0,0,0.2)\'"'
                ' onmouseout="this.style.transform=\'\';this.style.boxShadow=\'0 4px 18px -4px rgba(0,0,0,0.12)\'">'
                f'<div style="height:5px;background:{color};"></div>'
                f'<div style="padding:1.1rem 1.2rem;">'
                f'<div style="display:flex;align-items:center;gap:.6rem;margin-bottom:.75rem;">'
                f'<div style="width:36px;height:36px;border-radius:.5rem;background:{color}22;'
                f'display:flex;align-items:center;justify-content:center;font-size:1.2rem;">🕐</div>'
                f'<div style="font-weight:700;font-size:.95rem;color:#1e293b;">{name}</div></div>'
                f'<div style="display:flex;flex-direction:column;gap:.35rem;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                f'<span style="font-size:.75rem;color:#94a3b8;">Start time</span>'
                f'<span style="font-size:.82rem;font-weight:600;color:#1e293b;">{start_time}</span></div>'
                f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                f'<span style="font-size:.75rem;color:#94a3b8;">End time</span>'
                f'<span style="font-size:.82rem;font-weight:600;color:#1e293b;">{end_time}</span></div>'
                f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                f'<span style="font-size:.75rem;color:#94a3b8;">Min staff</span>'
                f'<span style="font-size:.82rem;font-weight:600;color:{color};">{emp_count}</span></div></div>'
                f'<div style="margin-top:.9rem;display:flex;gap:.5rem;">'
                f'<span style="flex:1;padding:.3rem;border-radius:.5rem;background:{color}15;color:{color};'
                f'text-align:center;font-size:.75rem;font-weight:600;cursor:pointer;">Edit</span>'
                f'<span style="flex:1;padding:.3rem;border-radius:.5rem;background:#fee2e2;color:#dc2626;'
                f'text-align:center;font-size:.75rem;font-weight:600;cursor:pointer;">Delete</span>'
                f'</div></div></div>'
            )


def create_modern_analytics_dashboard(manager, optimization_data):
    """Create modern analytics dashboard with metric cards and AI recommendations"""

    # ── KPI Metric Cards ─────────────────────────────────────────────────────
    with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden mb-4'):
        with ui.element('div').style('background:linear-gradient(90deg,#0284c7,#0891b2);padding:1rem 1.5rem;'):
            ui.html('<h2 style="font-size:1rem;font-weight:700;color:#fff;margin:0;">📈 Analytics Overview</h2>')
        with ui.element('div').classes('p-4'):
            _metrics = [
                {'title': 'Efficiency Score',   'value': f"{optimization_data.get('efficiency_score', 0):.1f}%",
                 'icon': '📈', 'f': '#059669', 't': '#10b981'},
                {'title': 'Workload Balance',   'value': 'Good',
                 'icon': '⚖️', 'f': '#0284c7', 't': '#0891b2'},
                {'title': 'Schedule Conflicts', 'value': '2',
                 'icon': '⚠️', 'f': '#f59e0b', 't': '#f97316'},
                {'title': 'AI Optimizations',  'value': '12',
                 'icon': '🤖', 'f': '#7c3aed', 't': '#8b5cf6'},
            ]
            with ui.element('div').style('display:flex;flex-wrap:nowrap;gap:1rem;'):
                for m in _metrics:
                    ui.html(
                        f'<div style="flex:1 1 0%;background:linear-gradient(135deg,{m["f"]},{m["t"]});'
                        'border-radius:1rem;padding:1.2rem 1.3rem;color:#fff;position:relative;overflow:hidden;'
                        'box-shadow:0 6px 20px -5px rgba(0,0,0,0.22);">'
                        '<div style="position:absolute;top:-14px;right:-14px;width:64px;height:64px;border-radius:50%;background:rgba(255,255,255,.12);"></div>'
                        f'<div style="font-size:1.5rem;margin-bottom:.4rem;">{m["icon"]}</div>'
                        f'<div style="font-size:1.75rem;font-weight:900;line-height:1;">{m["value"]}</div>'
                        f'<div style="font-size:.75rem;font-weight:600;opacity:.85;margin-top:.25rem;">{m["title"]}</div>'
                        '</div>'
                    )

    # ── Coverage Chart placeholder ───────────────────────────────────────────
    with ui.element('div').style('display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem;'):
        with ui.card().classes('rounded-2xl shadow-md bg-white overflow-hidden'):
            with ui.element('div').style('background:linear-gradient(90deg,#0284c7,#0891b2);padding:.8rem 1.2rem;'):
                ui.html('<h3 style="font-size:.9rem;font-weight:700;color:#fff;margin:0;">📊 Weekly Coverage</h3>')
            with ui.element('div').classes('p-4'):
                days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                vals = [95, 88, 92, 78, 96, 65, 40]
                bars_html = '<div style="display:flex;gap:.4rem;align-items:flex-end;height:100px;">'
                for day, val in zip(days, vals):
                    color = '#059669' if val >= 90 else ('#f59e0b' if val >= 70 else '#dc2626')
                    bars_html += (
                        f'<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:.25rem;">'
                        f'<div style="font-size:.65rem;color:#475569;font-weight:600;">{val}%</div>'
                        f'<div style="width:100%;background:{color};border-radius:.25rem .25rem 0 0;height:{val}px;"></div>'
                        f'<div style="font-size:.65rem;color:#94a3b8;">{day}</div></div>'
                    )
                bars_html += '</div>'
                ui.html(bars_html)

        with ui.card().classes('rounded-2xl shadow-md bg-white overflow-hidden'):
            with ui.element('div').style('background:linear-gradient(90deg,#0891b2,#0d9488);padding:.8rem 1.2rem;'):
                ui.html('<h3 style="font-size:.9rem;font-weight:700;color:#fff;margin:0;">🔄 Shift Distribution</h3>')
            with ui.element('div').classes('p-4'):
                segments = [
                    {'label': 'Morning',   'pct': 40, 'color': '#f59e0b'},
                    {'label': 'Afternoon', 'pct': 30, 'color': '#0891b2'},
                    {'label': 'Evening',   'pct': 20, 'color': '#7c3aed'},
                    {'label': 'Night',     'pct': 10, 'color': '#1e293b'},
                ]
                dist_html = '<div style="display:flex;flex-direction:column;gap:.5rem;">'
                for s in segments:
                    dist_html += (
                        f'<div style="display:flex;align-items:center;gap:.6rem;">'
                        f'<div style="font-size:.75rem;color:#475569;width:60px;">{s["label"]}</div>'
                        f'<div style="flex:1;height:12px;background:#f1f5f9;border-radius:9999px;overflow:hidden;">'
                        f'<div style="width:{s["pct"]}%;height:100%;background:{s["color"]};border-radius:9999px;"></div></div>'
                        f'<div style="font-size:.75rem;color:#475569;font-weight:600;width:28px;">{s["pct"]}%</div></div>'
                    )
                dist_html += '</div>'
                ui.html(dist_html)

    # ── AI Recommendations ────────────────────────────────────────────────────
    with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden'):
        with ui.element('div').style('background:linear-gradient(90deg,#7c3aed,#8b5cf6);padding:1rem 1.5rem;'):
            ui.html('<h2 style="font-size:1rem;font-weight:700;color:#fff;margin:0;">🤖 AI Recommendations</h2>')
        with ui.element('div').classes('p-4'):
            recommendations = optimization_data.get('recommendations', [])
            if recommendations:
                with ui.element('div').style('display:flex;flex-wrap:wrap;gap:.75rem;'):
                    for rec in recommendations:
                        priority    = rec.get('priority', 'medium')
                        pri_color   = ('#dc2626', '#fee2e2') if priority == 'high' else ('#f59e0b', '#fef3c7')
                        pri_label   = '🔴 High' if priority == 'high' else '🟡 Medium'
                        action_text = rec.get('action', '').replace('_', ' ').title()
                        ui.html(
                            f'<div style="flex:1 1 280px;border-radius:.75rem;overflow:hidden;'
                            'box-shadow:0 3px 12px -3px rgba(0,0,0,0.1);background:#fff;">'
                            f'<div style="height:4px;background:{pri_color[0]};"></div>'
                            f'<div style="padding:.9rem 1rem;">'
                            f'<div style="display:flex;align-items:center;gap:.5rem;margin-bottom:.4rem;">'
                            f'<span style="font-size:.7rem;font-weight:700;padding:.15rem .5rem;border-radius:9999px;'
                            f'background:{pri_color[1]};color:{pri_color[0]};">{pri_label}</span>'
                            f'<span style="font-size:.72rem;color:#94a3b8;">{action_text}</span></div>'
                            f'<div style="font-size:.85rem;font-weight:600;color:#1e293b;">{rec.get("message","")}</div>'
                            f'</div></div>'
                        )
            else:
                ui.html('<div style="display:flex;align-items:center;gap:.6rem;padding:.75rem;background:#d1fae5;border-radius:.75rem;">'
                        '<span style="font-size:1.2rem;">✅</span>'
                        '<span style="font-size:.9rem;font-weight:600;color:#065f46;">All schedules are optimally configured!</span></div>')


# Legacy function - redirects to modern implementation
def create_staff_schedule_page():
    """Legacy function that redirects to the modern implementation"""
    return create_modern_staff_schedule_page()

def create_weekly_schedule_panel(manager: ModernStaffScheduleManager):
    """Create weekly schedule view panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">📅 Weekly Schedule</h2>')
    
    # Week navigation
    current_week = manager.schedule_data['weekly_schedule']['week_of']
    with ui.row().classes('w-full gap-4 mb-4 items-center'):
        ui.button('◀ Previous Week', on_click=lambda: ui.notify('Loading previous week...')).classes('bg-blue-500 text-white')
        ui.html(f'<h3 class="text-lg font-semibold">Week of {current_week}</h3>')
        ui.button('Next Week ▶', on_click=lambda: ui.notify('Loading next week...')).classes('bg-blue-500 text-white')
        ui.button('📅 Today', on_click=lambda: ui.notify('Jumping to current week...')).classes('bg-green-500 text-white')
    
    # Weekly schedule grid
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    assignments = manager.schedule_data['weekly_schedule']['assignments']
    
    with ui.card().classes('w-full'):
        with ui.card_section().classes('p-0'):
            # Header row
            with ui.row().classes('w-full bg-gray-50 border-b'):
                ui.html('<div class="w-32 p-3 font-semibold">Employee</div>')
                for day in days:
                    ui.html(f'<div class="flex-1 p-3 text-center font-semibold">{day}</div>')
            
            # Schedule rows
            for emp_id, schedule in assignments.items():
                with ui.row().classes('w-full border-b hover:bg-gray-50'):
                    # Employee name
                    emp_names = {'EMP001': 'John Smith', 'EMP002': 'Sarah Johnson', 'EMP003': 'Mike Davis'}
                    ui.html(f'<div class="w-32 p-3"><strong>{emp_names.get(emp_id, emp_id)}</strong></div>')
                    
                    # Daily assignments
                    for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                        day_info = schedule.get(day, {'shift': 'off', 'status': 'off'})
                        shift_name = day_info.get('shift', 'off')
                        status = day_info.get('status', 'off')
                        
                        # Color coding for shifts
                        if shift_name == 'off':
                            color_class = 'bg-gray-100 text-gray-600'
                        elif shift_name == 'morning':
                            color_class = 'bg-blue-100 text-blue-800'
                        elif shift_name == 'afternoon':
                            color_class = 'bg-yellow-100 text-yellow-800'
                        elif shift_name == 'evening':
                            color_class = 'bg-purple-100 text-purple-800'
                        else:
                            color_class = 'bg-green-100 text-green-800'
                        
                        with ui.column().classes('flex-1 p-2'):
                            ui.html(f'<div class="text-center p-2 rounded {color_class}"><div class="text-xs font-medium">{shift_name.title()}</div><div class="text-xs">{status}</div></div>')

def create_monthly_overview_panel(manager: ModernStaffScheduleManager):
    """Create monthly overview panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">🗓️ Monthly Overview</h2>')
    
    # Month navigation
    current_date = datetime.now()
    with ui.row().classes('w-full gap-4 mb-4 items-center'):
        ui.button('◀ Previous Month', on_click=lambda: ui.notify('Loading previous month...')).classes('bg-blue-500 text-white')
        ui.html(f'<h3 class="text-lg font-semibold">{current_date.strftime("%B %Y")}</h3>')
        ui.button('Next Month ▶', on_click=lambda: ui.notify('Loading next month...')).classes('bg-blue-500 text-white')
    
    # Monthly stats
    with ui.row().classes('w-full gap-4 mb-4'):
        stats = [
            {'title': 'Total Scheduled Hours', 'value': '1,280', 'icon': '⏰', 'color': 'blue'},
            {'title': 'Employees Scheduled', 'value': '25', 'icon': '👥', 'color': 'green'},
            {'title': 'Overtime Hours', 'value': '48', 'icon': '📈', 'color': 'yellow'},
            {'title': 'Time-off Requests', 'value': '12', 'icon': '🏖️', 'color': 'purple'},
        ]
        
        for stat in stats:
            with ui.card().classes('flex-1'):
                with ui.card_section().classes('p-4 text-center'):
                    ui.html(f'<div class="text-2xl">{stat["icon"]}</div>')
                    ui.html(f'<div class="text-xl font-bold text-{stat["color"]}-600">{stat["value"]}</div>')
                    ui.html(f'<div class="text-sm text-gray-600">{stat["title"]}</div>')
    
    # Calendar view placeholder
    with ui.card().classes('w-full'):
        with ui.card_section().classes('p-4'):
            ui.html('<h3 class="text-lg font-semibold mb-3">📅 Calendar View</h3>')
            ui.html('<div class="h-64 bg-gray-100 rounded flex items-center justify-center text-gray-500">Monthly calendar grid will be implemented here</div>')

def create_shift_templates_panel(manager: ModernStaffScheduleManager):
    """Create shift templates panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">⏰ Shift Templates</h2>')
    
    # Add new shift button
    ui.button('➕ Add New Shift Template', on_click=lambda: ui.notify('Opening new shift dialog...')).classes('bg-green-500 text-white mb-4')
    
    # Shift templates grid
    shifts = manager.schedule_data['shift_templates']
    
    with ui.row().classes('w-full gap-4 flex-wrap'):
        for shift_id, shift_info in shifts.items():
            with ui.card().classes('w-64 hover:shadow-lg transition-shadow'):
                with ui.card_section().classes('p-4'):
                    # Shift header with color
                    ui.html(f'<div class="w-full h-3 rounded-t" style="background-color: {shift_info["color"]}"></div>')
                    ui.html(f'<h3 class="text-lg font-semibold mt-3 mb-2">{shift_info["name"]}</h3>')
                    
                    # Shift details
                    ui.html(f'<div class="mb-2">🕐 <strong>Start:</strong> {shift_info["start_time"]}</div>')
                    ui.html(f'<div class="mb-2">🕐 <strong>End:</strong> {shift_info["end_time"]}</div>')
                    ui.html(f'<div class="mb-3">☕ <strong>Break:</strong> {shift_info["break_duration"]} min</div>')
                    
                    # Action buttons
                    with ui.row().classes('w-full gap-2'):
                        ui.button('✏️', on_click=lambda s=shift_id: ui.notify(f'Editing {s}')).classes('text-xs bg-blue-500 text-white')
                        ui.button('👥', on_click=lambda s=shift_id: ui.notify(f'Assigning {s}')).classes('text-xs bg-green-500 text-white')
                        ui.button('🗑️', on_click=lambda s=shift_id: ui.notify(f'Deleting {s}')).classes('text-xs bg-red-500 text-white')

def create_staff_assignments_panel(manager: ModernStaffScheduleManager):
    """Create staff assignments panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">👥 Staff Assignments</h2>')
    
    # Assignment controls
    with ui.row().classes('w-full gap-4 mb-4'):
        ui.select(['All Employees', 'Engineering', 'HR', 'Sales', 'Finance'], value='All Employees').classes('w-48')
        ui.select(['This Week', 'Next Week', 'This Month'], value='This Week').classes('w-48')
        ui.button('🔄 Auto-Assign', on_click=lambda: ui.notify('Auto-assigning shifts...')).classes('bg-blue-500 text-white')
        ui.button('📋 Bulk Edit', on_click=lambda: ui.notify('Opening bulk edit...')).classes('bg-green-500 text-white')
    
    # Assignment summary
    with ui.card().classes('w-full mb-4'):
        with ui.card_section().classes('p-4'):
            ui.html('<h3 class="text-lg font-semibold mb-3">📊 Assignment Summary</h3>')
            with ui.row().classes('w-full gap-4'):
                summary_stats = [
                    {'label': 'Total Assignments', 'value': '25', 'color': 'blue'},
                    {'label': 'Pending Assignments', 'value': '5', 'color': 'yellow'},
                    {'label': 'Conflicts', 'value': '2', 'color': 'red'},
                    {'label': 'Coverage Rate', 'value': '92%', 'color': 'green'},
                ]
                
                for stat in summary_stats:
                    ui.html(f'<div class="flex-1 text-center"><div class="text-lg font-bold text-{stat["color"]}-600">{stat["value"]}</div><div class="text-sm text-gray-600">{stat["label"]}</div></div>')

def create_schedule_requests_panel(manager: ModernStaffScheduleManager):
    """Create schedule requests panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">📝 Schedule Requests</h2>')
    
    # Request filters
    with ui.row().classes('w-full gap-4 mb-4'):
        ui.select(['All Requests', 'Pending', 'Approved', 'Denied'], value='All Requests').classes('w-48')
        ui.select(['All Types', 'Shift Change', 'Time Off', 'Overtime'], value='All Types').classes('w-48')
        ui.button('📝 New Request', on_click=lambda: ui.notify('Creating new request...')).classes('bg-green-500 text-white')
    
    # Requests table
    requests = manager.schedule_data['schedule_requests']
    
    with ui.card().classes('w-full'):
        with ui.card_section().classes('p-0'):
            # Table header
            with ui.row().classes('w-full p-4 bg-gray-50 border-b'):
                ui.html('<div class="w-32 font-semibold">Employee</div>')
                ui.html('<div class="w-32 font-semibold">Type</div>')
                ui.html('<div class="w-32 font-semibold">Date</div>')
                ui.html('<div class="flex-1 font-semibold">Details</div>')
                ui.html('<div class="w-24 font-semibold">Status</div>')
                ui.html('<div class="w-32 font-semibold">Actions</div>')
            
            # Request rows
            for request in requests:
                with ui.row().classes('w-full p-4 border-b hover:bg-gray-50'):
                    ui.html(f'<div class="w-32">{request["employee_name"]}</div>')
                    ui.html(f'<div class="w-32">{request["request_type"].replace("_", " ").title()}</div>')
                    ui.html(f'<div class="w-32">{request["requested_date"]}</div>')
                    ui.html(f'<div class="flex-1 text-sm">{request["reason"]}</div>')
                    
                    # Status badge
                    status_colors = {
                        'pending': 'bg-yellow-100 text-yellow-800',
                        'approved': 'bg-green-100 text-green-800',
                        'denied': 'bg-red-100 text-red-800'
                    }
                    ui.html(f'<div class="w-24"><span class="px-2 py-1 rounded text-xs {status_colors.get(request["status"], "bg-gray-100 text-gray-800")}">{request["status"].title()}</span></div>')
                    
                    # Action buttons
                    with ui.row().classes('w-32 gap-1'):
                        if request['status'] == 'pending':
                            ui.button('✅', on_click=lambda r=request['id']: ui.notify(f'Approving {r}')).classes('text-xs bg-green-500 text-white')
                            ui.button('❌', on_click=lambda r=request['id']: ui.notify(f'Denying {r}')).classes('text-xs bg-red-500 text-white')
                        ui.button('👁️', on_click=lambda r=request['id']: ui.notify(f'Viewing {r}')).classes('text-xs bg-blue-500 text-white')

def create_coverage_analysis_panel(manager: ModernStaffScheduleManager):
    """Create coverage analysis panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">📊 Coverage Analysis</h2>')
    
    # Coverage overview
    coverage = manager.schedule_data['coverage_analysis']
    
    with ui.card().classes('w-full mb-4'):
        with ui.card_section().classes('p-4'):
            ui.html('<h3 class="text-lg font-semibold mb-3">📈 Weekly Coverage Status</h3>')
            
            # Coverage grid
            with ui.row().classes('w-full gap-2'):
                for day, data in coverage.items():
                    coverage_percent = (data['scheduled'] / data['required']) * 100
                    
                    # Status color
                    if data['status'] == 'optimal':
                        color_class = 'bg-green-100 border-green-300 text-green-800'
                    elif data['status'] == 'adequate':
                        color_class = 'bg-yellow-100 border-yellow-300 text-yellow-800'
                    else:
                        color_class = 'bg-red-100 border-red-300 text-red-800'
                    
                    with ui.card().classes(f'flex-1 {color_class} border-2'):
                        with ui.card_section().classes('p-3 text-center'):
                            ui.html(f'<div class="font-semibold text-sm">{day.title()}</div>')
                            ui.html(f'<div class="text-xs">{data["scheduled"]}/{data["required"]}</div>')
                            ui.html(f'<div class="text-xs">{coverage_percent:.0f}%</div>')
    
    # Detailed analysis
    with ui.row().classes('w-full gap-4'):
        # Understaffed alerts
        with ui.card().classes('flex-1'):
            with ui.card_section().classes('p-4'):
                ui.html('<h3 class="text-lg font-semibold mb-3 text-red-600">🚨 Understaffed Days</h3>')
                understaffed_days = [day for day, data in coverage.items() if data['status'] == 'understaffed']
                
                if understaffed_days:
                    for day in understaffed_days:
                        data = coverage[day]
                        shortfall = data['required'] - data['scheduled']
                        ui.html(f'<div class="p-2 bg-red-50 rounded mb-2"><strong>{day.title()}:</strong> {shortfall} staff short</div>')
                else:
                    ui.html('<div class="text-gray-500 text-center">No understaffed days</div>')
        
        # Optimization suggestions
        with ui.card().classes('flex-1'):
            with ui.card_section().classes('p-4'):
                ui.html('<h3 class="text-lg font-semibold mb-3 text-blue-600">💡 Suggestions</h3>')
                suggestions = [
                    'Consider hiring 2 additional part-time staff',
                    'Review Friday scheduling - consistently understaffed',
                    'Offer overtime incentives for Monday coverage',
                    'Cross-train employees for weekend shifts'
                ]
                
                for suggestion in suggestions:
                    ui.html(f'<div class="p-2 bg-blue-50 rounded mb-2 text-sm">• {suggestion}</div>')

def create_schedule_settings_panel(manager: ModernStaffScheduleManager):
    """Create schedule settings panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">⚙️ Schedule Settings</h2>')
    
    settings = manager.schedule_data['schedule_settings']
    
    # General settings
    with ui.card().classes('w-full mb-4'):
        with ui.card_section().classes('p-4'):
            ui.html('<h3 class="text-lg font-semibold mb-3">🔧 General Settings</h3>')
            
            with ui.row().classes('w-full gap-4'):
                with ui.column().classes('flex-1'):
                    ui.select(['monday', 'sunday'], value=settings['week_start_day'], label='Week Start Day').classes('w-full')
                    ui.number('Default Shift Duration (hours)', value=settings['default_shift_duration']).classes('w-full')
                    ui.number('Max Hours Per Week', value=settings['max_hours_per_week']).classes('w-full')
                
                with ui.column().classes('flex-1'):
                    ui.number('Minimum Rest Hours', value=settings['min_rest_hours']).classes('w-full')
                    ui.number('Shift Change Notice (hours)', value=settings['shift_change_notice_hours']).classes('w-full')
                    ui.number('Overtime Threshold (hours)', value=settings['overtime_threshold']).classes('w-full')
    
    # Notification settings
    with ui.card().classes('w-full mb-4'):
        with ui.card_section().classes('p-4'):
            ui.html('<h3 class="text-lg font-semibold mb-3">🔔 Notification Settings</h3>')
            
            with ui.column().classes('w-full gap-2'):
                ui.checkbox('Email notifications for schedule changes', value=True)
                ui.checkbox('SMS reminders for shift start', value=False)
                ui.checkbox('Alert managers for coverage gaps', value=True)
                ui.checkbox('Notify employees of approved requests', value=True)
    
    # Save settings button
