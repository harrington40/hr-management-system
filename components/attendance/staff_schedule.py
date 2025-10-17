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

    # Initialize manager
    manager = ModernStaffScheduleManager()

    # Main container with modern design
    with ui.column().classes('w-full min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 p-6 gap-6'):

        # Header Section with Metrics
        with ui.row().classes('w-full justify-between items-start mb-6'):
            # Title and description
            with ui.column().classes('gap-2'):
                ui.html('<div class="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">📅 Staff Schedule</div>', sanitize=False)
                ui.html('<div class="text-lg text-slate-600 font-medium">Intelligent workforce planning and optimization</div>', sanitize=False)

            # Quick Stats Cards
            with ui.row().classes('gap-4'):
                # Coverage Card
                with ui.card().classes('bg-gradient-to-r from-green-500 to-emerald-600 text-white shadow-lg hover:shadow-xl transition-shadow duration-300'):
                    with ui.card_section().classes('p-4'):
                        with ui.row().classes('items-center gap-3'):
                            ui.html('<div class="text-2xl">📊</div>', sanitize=False)
                            with ui.column():
                                ui.html(f'<div class="text-2xl font-bold">{manager.metrics.coverage_percentage:.1f}%</div>', sanitize=False)
                                ui.html('<div class="text-sm opacity-90">Coverage Rate</div>', sanitize=False)

                # Pending Requests Card
                with ui.card().classes('bg-gradient-to-r from-orange-500 to-red-500 text-white shadow-lg hover:shadow-xl transition-shadow duration-300'):
                    with ui.card_section().classes('p-4'):
                        with ui.row().classes('items-center gap-3'):
                            ui.html('<div class="text-2xl">⏳</div>', sanitize=False)
                            with ui.column():
                                ui.html(f'<div class="text-2xl font-bold">{manager.metrics.pending_requests}</div>', sanitize=False)
                                ui.html('<div class="text-sm opacity-90">Pending Requests</div>', sanitize=False)

                # Total Shifts Card
                with ui.card().classes('bg-gradient-to-r from-blue-500 to-indigo-600 text-white shadow-lg hover:shadow-xl transition-shadow duration-300'):
                    with ui.card_section().classes('p-4'):
                        with ui.row().classes('items-center gap-3'):
                            ui.html('<div class="text-2xl">👥</div>', sanitize=False)
                            with ui.column():
                                ui.html(f'<div class="text-2xl font-bold">{manager.metrics.total_shifts}</div>', sanitize=False)
                                ui.html('<div class="text-sm opacity-90">Active Shifts</div>', sanitize=False)

        # AI Optimization Banner
        optimization_data = manager.optimize_schedule()
        if optimization_data['recommendations']:
            with ui.card().classes('w-full bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 shadow-md'):
                with ui.card_section().classes('p-4'):
                    with ui.row().classes('items-center gap-4 w-full'):
                        ui.html('<div class="text-2xl">🤖</div>', sanitize=False)
                        with ui.column().classes('flex-1'):
                            ui.html('<div class="text-lg font-semibold text-purple-800">AI Schedule Optimization Available</div>', sanitize=False)
                            ui.html('<div class="text-sm text-purple-600">Intelligent recommendations to improve coverage and fairness</div>', sanitize=False)

                        with ui.row().classes('gap-2'):
                            for rec in optimization_data['recommendations'][:2]:  # Show top 2 recommendations
                                priority_color = 'bg-red-100 text-red-800' if rec['priority'] == 'high' else 'bg-yellow-100 text-yellow-800'
                                ui.badge(rec['type'].title()).classes(f'{priority_color} text-xs')

                            ui.button('View Recommendations',
                                    on_click=lambda: ui.notify('Optimization recommendations would open here', type='info')
                                    ).classes('bg-purple-600 text-white hover:bg-purple-700 px-4 py-2 rounded-lg text-sm font-medium')

        # Main Content Grid
        with ui.grid(columns='1fr 350px').classes('w-full gap-6'):

            # Left Panel - Schedule Views
            with ui.card().classes('bg-white shadow-xl border-0 overflow-hidden'):
                with ui.card_section().classes('p-0'):

                    # View Selector Tabs
                    view_tabs = ui.tabs().classes('w-full bg-slate-50 border-b border-slate-200')
                    with view_tabs:
                        weekly_tab = ui.tab('Weekly View', icon='calendar_view_week')
                        monthly_tab = ui.tab('Monthly Overview', icon='calendar_month')
                        shifts_tab = ui.tab('Shift Templates', icon='schedule')
                        analytics_tab = ui.tab('Analytics', icon='analytics')

                    # Tab Panels
                    with ui.tab_panels(view_tabs, value=weekly_tab).classes('p-0'):

                        # Weekly View Panel
                        with ui.tab_panel(weekly_tab).classes('p-6'):
                            create_modern_weekly_schedule(manager)

                        # Monthly Overview Panel
                        with ui.tab_panel(monthly_tab).classes('p-6'):
                            create_modern_monthly_overview(manager)

                        # Shift Templates Panel
                        with ui.tab_panel(shifts_tab).classes('p-6'):
                            create_modern_shift_templates(manager)

                        # Analytics Panel
                        with ui.tab_panel(analytics_tab).classes('p-6'):
                            create_modern_analytics_dashboard(manager, optimization_data)

            # Right Panel - Quick Actions & Info
            with ui.column().classes('gap-4'):

                # Quick Actions Card
                with ui.card().classes('bg-white shadow-lg border-0'):
                    with ui.card_section().classes('p-4'):
                        ui.html('<div class="text-lg font-semibold text-slate-800 mb-4">⚡ Quick Actions</div>', sanitize=False)

                        with ui.column().classes('gap-3'):
                            ui.button('➕ Add New Shift',
                                    on_click=lambda: ui.notify('Add shift functionality', type='info')
                                    ).classes('w-full justify-start bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200')

                            ui.button('🔄 Optimize Schedule',
                                    on_click=lambda: ui.notify('AI optimization would run here', type='info')
                                    ).classes('w-full justify-start bg-purple-50 hover:bg-purple-100 text-purple-700 border border-purple-200')

                            ui.button('📋 Review Requests',
                                    on_click=lambda: ui.notify('Schedule requests panel', type='info')
                                    ).classes('w-full justify-start bg-green-50 hover:bg-green-100 text-green-700 border border-green-200')

                            ui.button('📊 Export Schedule',
                                    on_click=lambda: ui.notify('Export functionality', type='info')
                                    ).classes('w-full justify-start bg-orange-50 hover:bg-orange-100 text-orange-700 border border-orange-200')

                # Schedule Health Card
                with ui.card().classes('bg-white shadow-lg border-0'):
                    with ui.card_section().classes('p-4'):
                        ui.html('<div class="text-lg font-semibold text-slate-800 mb-4">🏥 Schedule Health</div>', sanitize=False)

                        # Health indicators
                        health_items = [
                            {'label': 'Coverage Rate', 'value': f"{manager.metrics.coverage_percentage:.1f}%", 'status': 'good' if manager.metrics.coverage_percentage > 80 else 'warning'},
                            {'label': 'Understaffed Days', 'value': str(manager.metrics.understaffed_days), 'status': 'bad' if manager.metrics.understaffed_days > 0 else 'good'},
                            {'label': 'Pending Requests', 'value': str(manager.metrics.pending_requests), 'status': 'warning' if manager.metrics.pending_requests > 0 else 'good'},
                        ]

                        for item in health_items:
                            status_color = {
                                'good': 'text-green-600 bg-green-50',
                                'warning': 'text-yellow-600 bg-yellow-50',
                                'bad': 'text-red-600 bg-red-50'
                            }[item['status']]

                            with ui.row().classes('justify-between items-center p-2 rounded-lg mb-2'):
                                ui.html(f'<div class="text-sm font-medium text-slate-700">{item["label"]}</div>', sanitize=False)
                                ui.html(f'<div class="text-sm font-bold px-2 py-1 rounded {status_color}">{item["value"]}</div>', sanitize=False)

                # Recent Activity Card
                with ui.card().classes('bg-white shadow-lg border-0'):
                    with ui.card_section().classes('p-4'):
                        ui.html('<div class="text-lg font-semibold text-slate-800 mb-4">📝 Recent Activity</div>', sanitize=False)

                        activities = [
                            {'time': '2 hours ago', 'action': 'Schedule optimized', 'user': 'AI System'},
                            {'time': '4 hours ago', 'action': 'Shift request approved', 'user': 'Sarah Johnson'},
                            {'time': '6 hours ago', 'action': 'New shift template added', 'user': 'John Smith'},
                        ]

                        for activity in activities:
                            with ui.row().classes('items-start gap-3 p-2 hover:bg-slate-50 rounded-lg cursor-pointer'):
                                with ui.column().classes('flex-1'):
                                    ui.html(f'<div class="text-sm font-medium text-slate-800">{activity["action"]}</div>', sanitize=False)
                                    ui.html(f'<div class="text-xs text-slate-500">{activity["user"]} • {activity["time"]}</div>', sanitize=False)

def create_modern_weekly_schedule(manager):
    """Create modern weekly schedule view with interactive calendar"""

    # Week navigation
    with ui.row().classes('items-center justify-between mb-6'):
        ui.button('⬅️ Previous Week',
                 on_click=lambda: ui.notify('Previous week navigation', type='info')
                 ).classes('bg-slate-100 hover:bg-slate-200 text-slate-700 px-4 py-2 rounded-lg')

        current_week = manager.schedule_data.get('weekly_schedule', {}).get('week_of', 'Current Week')
        ui.html(f'<div class="text-xl font-bold text-slate-800">Week of {current_week}</div>', sanitize=False)

        ui.button('Next Week ➡️',
                 on_click=lambda: ui.notify('Next week navigation', type='info')
                 ).classes('bg-slate-100 hover:bg-slate-200 text-slate-700 px-4 py-2 rounded-lg')

    # Schedule Grid
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    assignments = manager.schedule_data.get('weekly_schedule', {}).get('assignments', {})

    # Header row
    with ui.grid(columns='200px repeat(7, 1fr)').classes('gap-2 mb-4'):
        ui.html('<div class="font-bold text-slate-700 p-3"></div>', sanitize=False)  # Empty corner
        for day in days:
            day_short = day[:3]
            ui.html(f'<div class="font-bold text-slate-700 p-3 text-center bg-slate-100 rounded-lg">{day_short}</div>', sanitize=False)

        # Employee rows
        for emp_id, emp_data in assignments.items():
            emp_name = emp_data.get('name', emp_id)
            emp_dept = emp_data.get('department', 'Unknown')

            # Employee info cell
            with ui.column().classes('p-3 bg-blue-50 rounded-lg border border-blue-200'):
                ui.html(f'<div class="font-semibold text-blue-800">{emp_name}</div>', sanitize=False)
                ui.html(f'<div class="text-xs text-blue-600">{emp_dept}</div>', sanitize=False)

            # Day cells
            for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                day_data = emp_data.get(day, {})
                shift = day_data.get('shift', 'off')
                status = day_data.get('status', 'off')

                if shift == 'off':
                    bg_color = 'bg-gray-100 text-gray-500'
                    shift_text = 'OFF'
                else:
                    shift_templates = manager.schedule_data.get('shift_templates', {})
                    shift_info = shift_templates.get(shift, {})
                    shift_name = shift_info.get('name', shift.title())
                    color = shift_info.get('color', '#6B7280')
                    bg_color = f'bg-[{color}] text-white'
                    shift_text = shift_name.split()[0]  # First word only

                ui.html(f'<div class="p-2 text-center text-xs font-medium rounded-lg {bg_color} border cursor-pointer hover:opacity-80 transition-opacity" onclick="console.log(\'{emp_id} {day}\')">{shift_text}</div>', sanitize=False)

def create_modern_monthly_overview(manager):
    """Create modern monthly overview with calendar visualization"""
    with ui.card().classes('w-full bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-200'):
        with ui.card_section().classes('p-6'):
            ui.html('<div class="text-2xl font-bold text-indigo-800 mb-4">📊 Monthly Schedule Overview</div>', sanitize=False)
            ui.html('<div class="text-indigo-600 mb-6">Comprehensive monthly view with coverage analysis</div>', sanitize=False)

            # Month selector
            with ui.row().classes('items-center gap-4 mb-6'):
                ui.button('⬅️', on_click=lambda: ui.notify('Previous month', type='info')).classes('bg-indigo-100 hover:bg-indigo-200 text-indigo-700 px-3 py-2 rounded-lg')
                ui.html('<div class="text-xl font-bold text-indigo-800">October 2025</div>', sanitize=False)
                ui.button('➡️', on_click=lambda: ui.notify('Next month', type='info')).classes('bg-indigo-100 hover:bg-indigo-200 text-indigo-700 px-3 py-2 rounded-lg')

            ui.html('<div class="text-center text-slate-500 py-8">Monthly calendar view would be implemented here with interactive date selection and coverage visualization.</div>', sanitize=False)

def create_modern_shift_templates(manager):
    """Create modern shift templates management"""
    shift_templates = manager.schedule_data.get('shift_templates', {})

    with ui.column().classes('gap-4'):
        ui.html('<div class="text-xl font-bold text-slate-800 mb-4">⚙️ Shift Templates</div>', sanitize=False)

        for shift_id, shift_data in shift_templates.items():
            with ui.card().classes('bg-white border border-slate-200 hover:shadow-md transition-shadow'):
                with ui.card_section().classes('p-4'):
                    with ui.row().classes('items-center justify-between w-full'):
                        with ui.row().classes('items-center gap-3'):
                            # Color indicator
                            color = shift_data.get('color', '#6B7280')
                            ui.html(f'<div class="w-4 h-4 rounded-full" style="background-color: {color}"></div>', sanitize=False)

                            with ui.column():
                                ui.html(f'<div class="font-semibold text-slate-800">{shift_data.get("name", shift_id.title())}</div>', sanitize=False)
                                ui.html(f'<div class="text-sm text-slate-600">{shift_data.get("start_time", "N/A")} - {shift_data.get("end_time", "N/A")}</div>', sanitize=False)

                        ui.button('Edit',
                                 on_click=lambda s=shift_id: ui.notify(f'Edit {s} shift', type='info')
                                 ).classes('bg-blue-50 hover:bg-blue-100 text-blue-700 px-3 py-1 rounded text-sm')

def create_modern_analytics_dashboard(manager, optimization_data):
    """Create modern analytics dashboard with charts and insights"""
    with ui.column().classes('gap-6'):

        # Key Metrics Row
        with ui.grid(columns='repeat(auto-fit, minmax(200px, 1fr))').classes('gap-4 mb-6'):
            metrics = [
                {'title': 'Efficiency Score', 'value': f"{optimization_data.get('efficiency_score', 0):.1f}%", 'icon': '📈', 'color': 'from-green-500 to-emerald-600'},
                {'title': 'Workload Balance', 'value': 'Good', 'icon': '⚖️', 'color': 'from-blue-500 to-indigo-600'},
                {'title': 'Schedule Conflicts', 'value': '2', 'icon': '⚠️', 'color': 'from-orange-500 to-red-500'},
                {'title': 'Auto-Optimizations', 'value': '12', 'icon': '🤖', 'color': 'from-purple-500 to-pink-600'},
            ]

            for metric in metrics:
                with ui.card().classes(f'bg-gradient-to-r {metric["color"]} text-white shadow-lg'):
                    with ui.card_section().classes('p-4'):
                        with ui.row().classes('items-center justify-between'):
                            ui.html(f'<div class="text-2xl">{metric["icon"]}</div>', sanitize=False)
                            ui.html(f'<div class="text-2xl font-bold">{metric["value"]}</div>', sanitize=False)
                        ui.html(f'<div class="text-sm opacity-90">{metric["title"]}</div>', sanitize=False)

        # Charts and Visualizations
        with ui.grid(columns='1fr 1fr').classes('gap-6'):

            # Coverage Chart
            with ui.card().classes('bg-white shadow-lg border-0'):
                with ui.card_section().classes('p-4'):
                    ui.html('<div class="text-lg font-semibold text-slate-800 mb-4">📊 Weekly Coverage</div>', sanitize=False)
                    ui.html('<div class="text-center text-slate-500 py-8">Interactive coverage chart would be displayed here showing optimal/adequate/understaffed days.</div>', sanitize=False)

            # Shift Distribution
            with ui.card().classes('bg-white shadow-lg border-0'):
                with ui.card_section().classes('p-4'):
                    ui.html('<div class="text-lg font-semibold text-slate-800 mb-4">🔄 Shift Distribution</div>', sanitize=False)
                    ui.html('<div class="text-center text-slate-500 py-8">Pie chart showing distribution of morning/afternoon/evening/night shifts.</div>', sanitize=False)

        # AI Recommendations
        with ui.card().classes('bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 shadow-md'):
            with ui.card_section().classes('p-4'):
                ui.html('<div class="text-lg font-semibold text-purple-800 mb-4">🤖 AI Recommendations</div>', sanitize=False)

                recommendations = optimization_data.get('recommendations', [])
                if recommendations:
                    for rec in recommendations:
                        with ui.row().classes('items-start gap-3 p-3 bg-white/50 rounded-lg mb-3'):
                            priority_icon = '🔴' if rec['priority'] == 'high' else '🟡'
                            ui.html(f'<div class="text-lg">{priority_icon}</div>', sanitize=False)
                            with ui.column().classes('flex-1'):
                                ui.html(f'<div class="font-medium text-purple-800">{rec["message"]}</div>', sanitize=False)
                                ui.html(f'<div class="text-sm text-purple-600">{rec.get("action", "").replace("_", " ").title()}</div>', sanitize=False)
                else:
                    ui.html('<div class="text-purple-600">✅ All schedules are optimally configured!</div>', sanitize=False)

def create_modern_weekly_schedule(manager):
    """Create modern weekly schedule view with interactive calendar"""

    # Week navigation
    with ui.row().classes('items-center justify-between mb-6'):
        ui.button('⬅️ Previous Week',
                 on_click=lambda: ui.notify('Previous week navigation', type='info')
                 ).classes('bg-slate-100 hover:bg-slate-200 text-slate-700 px-4 py-2 rounded-lg')

        current_week = manager.schedule_data.get('weekly_schedule', {}).get('week_of', 'Current Week')
        ui.html(f'<div class="text-xl font-bold text-slate-800">Week of {current_week}</div>', sanitize=False)

        ui.button('Next Week ➡️',
                 on_click=lambda: ui.notify('Next week navigation', type='info')
                 ).classes('bg-slate-100 hover:bg-slate-200 text-slate-700 px-4 py-2 rounded-lg')

    # Schedule Grid
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    assignments = manager.schedule_data.get('weekly_schedule', {}).get('assignments', {})

    def save_schedule(self, schedule_data: Dict[str, Any]) -> bool:
        """Save schedule data to YAML file"""
        try:
            with open(self.schedule_file, 'w') as file:
                yaml.dump(schedule_data, file, default_flow_style=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving schedule: {e}")
            return False

# Legacy function - redirects to modern implementation
def create_staff_schedule_page():
    """Legacy function that redirects to the modern implementation"""
    return create_modern_staff_schedule_page()
