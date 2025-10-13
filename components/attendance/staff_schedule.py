"""
Staff Schedule Management Component
Provides weekly/monthly schedule management, shift planning, and schedule visualization
"""

from nicegui import ui
import yaml
import os
from datetime import datetime, timedelta, date
import json
from typing import Dict, List, Any
import calendar

class StaffScheduleManager:
    """Manager class for staff schedule and shift planning"""
    
    def __init__(self):
        self.config_dir = "config"
        self.schedule_file = os.path.join(self.config_dir, "staff_schedule.yaml")
        self.ensure_config_directory()
        self.schedule_data = self.load_schedule()
    
    def ensure_config_directory(self):
        """Ensure config directory exists"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
    
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
        """Get default schedule configuration"""
        current_date = datetime.now()
        week_start = current_date - timedelta(days=current_date.weekday())
        
        return {
            'schedule_settings': {
                'week_start_day': 'monday',
                'default_shift_duration': 8,
                'max_hours_per_week': 40,
                'min_rest_hours': 12,
                'shift_change_notice_hours': 24,
                'overtime_threshold': 8
            },
            'shift_templates': {
                'morning': {
                    'name': 'Morning Shift',
                    'start_time': '09:00',
                    'end_time': '17:00',
                    'break_duration': 60,
                    'color': '#3B82F6'
                },
                'afternoon': {
                    'name': 'Afternoon Shift',
                    'start_time': '13:00',
                    'end_time': '21:00',
                    'break_duration': 60,
                    'color': '#F59E0B'
                },
                'evening': {
                    'name': 'Evening Shift',
                    'start_time': '17:00',
                    'end_time': '01:00',
                    'break_duration': 60,
                    'color': '#8B5CF6'
                },
                'night': {
                    'name': 'Night Shift',
                    'start_time': '23:00',
                    'end_time': '07:00',
                    'break_duration': 60,
                    'color': '#1F2937'
                }
            },
            'weekly_schedule': {
                'week_of': week_start.strftime('%Y-%m-%d'),
                'assignments': {
                    'EMP001': {
                        'monday': {'shift': 'morning', 'status': 'scheduled'},
                        'tuesday': {'shift': 'morning', 'status': 'scheduled'},
                        'wednesday': {'shift': 'morning', 'status': 'scheduled'},
                        'thursday': {'shift': 'morning', 'status': 'scheduled'},
                        'friday': {'shift': 'morning', 'status': 'scheduled'},
                        'saturday': {'shift': 'off', 'status': 'off'},
                        'sunday': {'shift': 'off', 'status': 'off'}
                    },
                    'EMP002': {
                        'monday': {'shift': 'afternoon', 'status': 'scheduled'},
                        'tuesday': {'shift': 'afternoon', 'status': 'scheduled'},
                        'wednesday': {'shift': 'afternoon', 'status': 'scheduled'},
                        'thursday': {'shift': 'afternoon', 'status': 'scheduled'},
                        'friday': {'shift': 'afternoon', 'status': 'scheduled'},
                        'saturday': {'shift': 'off', 'status': 'off'},
                        'sunday': {'shift': 'off', 'status': 'off'}
                    },
                    'EMP003': {
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
                    'submitted_date': '2025-10-10'
                },
                {
                    'id': 'REQ002',
                    'employee_id': 'EMP002',
                    'employee_name': 'Sarah Johnson',
                    'request_type': 'time_off',
                    'requested_date': '2025-10-18',
                    'reason': 'Personal appointment',
                    'status': 'approved',
                    'submitted_date': '2025-10-08'
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
    
    def save_schedule(self, schedule_data: Dict[str, Any]) -> bool:
        """Save schedule data to YAML file"""
        try:
            with open(self.schedule_file, 'w') as file:
                yaml.dump(schedule_data, file, default_flow_style=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving schedule: {e}")
            return False

def create_staff_schedule_page():
    """Create the main staff schedule page"""
    manager = StaffScheduleManager()
    
    with ui.column().classes('w-full h-full bg-gradient-to-br from-green-50 to-blue-100 min-h-screen'):
        # Header Section
        with ui.row().classes('w-full p-6'):
            with ui.card().classes('w-full bg-gradient-to-r from-green-600 to-blue-600 text-white'):
                with ui.card_section().classes('p-6'):
                    with ui.row().classes('w-full justify-between items-center'):
                        ui.html('<h1 class="text-3xl font-bold flex items-center gap-3"><span class="text-4xl">📅</span>Staff Schedule Management</h1>', sanitize=False).classes('mb-2')
                        with ui.row().classes('gap-4'):
                            ui.button('📊 Generate Schedule', on_click=lambda: ui.notify('Generating schedule...')).classes('bg-white text-green-600 hover:bg-gray-100')
                            ui.button('📝 Schedule Requests', on_click=lambda: ui.notify('Opening requests...')).classes('bg-white text-green-600 hover:bg-gray-100')
                            ui.button('📤 Export Schedule', on_click=lambda: ui.notify('Exporting schedule...')).classes('bg-white text-green-600 hover:bg-gray-100')

        # Main Content Area
        with ui.row().classes('w-full px-6 gap-6'):
            # Left Sidebar - Navigation
            with ui.column().classes('w-1/4'):
                with ui.card().classes('w-full'):
                    with ui.card_section().classes('p-4'):
                        ui.html('<h3 class="text-lg font-semibold text-gray-800 mb-4">📋 Schedule Views</h3>', sanitize=False)
                        
                        view_options = [
                            {'id': 'weekly', 'name': 'Weekly Schedule', 'icon': '📅', 'color': 'blue'},
                            {'id': 'monthly', 'name': 'Monthly Overview', 'icon': '🗓️', 'color': 'green'},
                            {'id': 'shifts', 'name': 'Shift Templates', 'icon': '⏰', 'color': 'purple'},
                            {'id': 'assignments', 'name': 'Staff Assignments', 'icon': '👥', 'color': 'indigo'},
                            {'id': 'requests', 'name': 'Schedule Requests', 'icon': '📝', 'color': 'yellow'},
                            {'id': 'coverage', 'name': 'Coverage Analysis', 'icon': '📊', 'color': 'red'},
                            {'id': 'settings', 'name': 'Schedule Settings', 'icon': '⚙️', 'color': 'gray'},
                        ]
                        
                        # Simple state management without ui.state()
                        class ViewState:
                            def __init__(self):
                                self.current = 'weekly'
                                self.panels = {}
                        
                        state = ViewState()
                        
                        def switch_view(view_id):
                            state.current = view_id
                            # Hide all panels
                            for panel in state.panels.values():
                                panel.set_visibility(False)
                            # Show selected panel
                            if view_id in state.panels:
                                state.panels[view_id].set_visibility(True)
                        
                        for option in view_options:
                            with ui.row().classes('w-full mb-2'):
                                ui.button(f"{option['icon']} {option['name']}", 
                                         on_click=lambda opt=option['id']: switch_view(opt)
                                ).classes(f'w-full justify-start text-left p-3 rounded-lg transition-all bg-gray-100 hover:bg-gray-200 text-gray-700')

            # Right Panel - Content
            with ui.column().classes('w-3/4'):
                with ui.card().classes('w-full'):
                    with ui.card_section().classes('p-6'):
                        
                        # Create panels and store references
                        state.panels['weekly'] = ui.column().classes('w-full')
                        with state.panels['weekly']:
                            create_weekly_schedule_panel(manager)
                        
                        state.panels['monthly'] = ui.column().classes('w-full')
                        with state.panels['monthly']:
                            create_monthly_overview_panel(manager)
                        state.panels['monthly'].set_visibility(False)
                            
                        state.panels['shifts'] = ui.column().classes('w-full')
                        with state.panels['shifts']:
                            create_shift_templates_panel(manager)
                        state.panels['shifts'].set_visibility(False)
                            
                        state.panels['assignments'] = ui.column().classes('w-full')
                        with state.panels['assignments']:
                            create_staff_assignments_panel(manager)
                        state.panels['assignments'].set_visibility(False)
                            
                        state.panels['requests'] = ui.column().classes('w-full')
                        with state.panels['requests']:
                            create_schedule_requests_panel(manager)
                        state.panels['requests'].set_visibility(False)
                            
                        state.panels['coverage'] = ui.column().classes('w-full')
                        with state.panels['coverage']:
                            create_coverage_analysis_panel(manager)
                        state.panels['coverage'].set_visibility(False)
                            
                        state.panels['settings'] = ui.column().classes('w-full')
                        with state.panels['settings']:
                            create_schedule_settings_panel(manager)
                        state.panels['settings'].set_visibility(False)

def create_weekly_schedule_panel(manager: StaffScheduleManager):
    """Create weekly schedule view panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">📅 Weekly Schedule</h2>', sanitize=False)
    
    # Week navigation
    current_week = manager.schedule_data['weekly_schedule']['week_of']
    with ui.row().classes('w-full gap-4 mb-4 items-center'):
        ui.button('◀ Previous Week', on_click=lambda: ui.notify('Loading previous week...')).classes('bg-blue-500 text-white')
        ui.html(f'<h3 class="text-lg font-semibold">Week of {current_week}</h3>', sanitize=False)
        ui.button('Next Week ▶', on_click=lambda: ui.notify('Loading next week...')).classes('bg-blue-500 text-white')
        ui.button('📅 Today', on_click=lambda: ui.notify('Jumping to current week...')).classes('bg-green-500 text-white')
    
    # Weekly schedule grid
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    assignments = manager.schedule_data['weekly_schedule']['assignments']
    
    with ui.card().classes('w-full'):
        with ui.card_section().classes('p-0'):
            # Header row
            with ui.row().classes('w-full bg-gray-50 border-b'):
                ui.html('<div class="w-32 p-3 font-semibold">Employee</div>', sanitize=False)
                for day in days:
                    ui.html(f'<div class="flex-1 p-3 text-center font-semibold">{day}</div>', sanitize=False)
            
            # Schedule rows
            for emp_id, schedule in assignments.items():
                with ui.row().classes('w-full border-b hover:bg-gray-50'):
                    # Employee name
                    emp_names = {'EMP001': 'John Smith', 'EMP002': 'Sarah Johnson', 'EMP003': 'Mike Davis'}
                    ui.html(f'<div class="w-32 p-3"><strong>{emp_names.get(emp_id, emp_id)}</strong></div>', sanitize=False)
                    
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
                            ui.html(f'<div class="text-center p-2 rounded {color_class}"><div class="text-xs font-medium">{shift_name.title()}</div><div class="text-xs">{status}</div></div>', sanitize=False)

def create_monthly_overview_panel(manager: StaffScheduleManager):
    """Create monthly overview panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">🗓️ Monthly Overview</h2>', sanitize=False)
    
    # Month navigation
    current_date = datetime.now()
    with ui.row().classes('w-full gap-4 mb-4 items-center'):
        ui.button('◀ Previous Month', on_click=lambda: ui.notify('Loading previous month...')).classes('bg-blue-500 text-white')
        ui.html(f'<h3 class="text-lg font-semibold">{current_date.strftime("%B %Y")}</h3>', sanitize=False)
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
                    ui.html(f'<div class="text-2xl">{stat["icon"]}</div>', sanitize=False)
                    ui.html(f'<div class="text-xl font-bold text-{stat["color"]}-600">{stat["value"]}</div>', sanitize=False)
                    ui.html(f'<div class="text-sm text-gray-600">{stat["title"]}</div>', sanitize=False)
    
    # Calendar view placeholder
    with ui.card().classes('w-full'):
        with ui.card_section().classes('p-4'):
            ui.html('<h3 class="text-lg font-semibold mb-3">📅 Calendar View</h3>', sanitize=False)
            ui.html('<div class="h-64 bg-gray-100 rounded flex items-center justify-center text-gray-500">Monthly calendar grid will be implemented here</div>', sanitize=False)

def create_shift_templates_panel(manager: StaffScheduleManager):
    """Create shift templates panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">⏰ Shift Templates</h2>', sanitize=False)
    
    # Add new shift button
    ui.button('➕ Add New Shift Template', on_click=lambda: ui.notify('Opening new shift dialog...')).classes('bg-green-500 text-white mb-4')
    
    # Shift templates grid
    shifts = manager.schedule_data['shift_templates']
    
    with ui.row().classes('w-full gap-4 flex-wrap'):
        for shift_id, shift_info in shifts.items():
            with ui.card().classes('w-64 hover:shadow-lg transition-shadow'):
                with ui.card_section().classes('p-4'):
                    # Shift header with color
                    ui.html(f'<div class="w-full h-3 rounded-t" style="background-color: {shift_info["color"]}"></div>', sanitize=False)
                    ui.html(f'<h3 class="text-lg font-semibold mt-3 mb-2">{shift_info["name"]}</h3>', sanitize=False)
                    
                    # Shift details
                    ui.html(f'<div class="mb-2">🕐 <strong>Start:</strong> {shift_info["start_time"]}</div>', sanitize=False)
                    ui.html(f'<div class="mb-2">🕐 <strong>End:</strong> {shift_info["end_time"]}</div>', sanitize=False)
                    ui.html(f'<div class="mb-3">☕ <strong>Break:</strong> {shift_info["break_duration"]} min</div>', sanitize=False)
                    
                    # Action buttons
                    with ui.row().classes('w-full gap-2'):
                        ui.button('✏️', on_click=lambda s=shift_id: ui.notify(f'Editing {s}')).classes('text-xs bg-blue-500 text-white')
                        ui.button('👥', on_click=lambda s=shift_id: ui.notify(f'Assigning {s}')).classes('text-xs bg-green-500 text-white')
                        ui.button('🗑️', on_click=lambda s=shift_id: ui.notify(f'Deleting {s}')).classes('text-xs bg-red-500 text-white')

def create_staff_assignments_panel(manager: StaffScheduleManager):
    """Create staff assignments panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">👥 Staff Assignments</h2>', sanitize=False)
    
    # Assignment controls
    with ui.row().classes('w-full gap-4 mb-4'):
        ui.select(['All Employees', 'Engineering', 'HR', 'Sales', 'Finance'], value='All Employees').classes('w-48')
        ui.select(['This Week', 'Next Week', 'This Month'], value='This Week').classes('w-48')
        ui.button('🔄 Auto-Assign', on_click=lambda: ui.notify('Auto-assigning shifts...')).classes('bg-blue-500 text-white')
        ui.button('📋 Bulk Edit', on_click=lambda: ui.notify('Opening bulk edit...')).classes('bg-green-500 text-white')
    
    # Assignment summary
    with ui.card().classes('w-full mb-4'):
        with ui.card_section().classes('p-4'):
            ui.html('<h3 class="text-lg font-semibold mb-3">📊 Assignment Summary</h3>', sanitize=False)
            with ui.row().classes('w-full gap-4'):
                summary_stats = [
                    {'label': 'Total Assignments', 'value': '25', 'color': 'blue'},
                    {'label': 'Pending Assignments', 'value': '5', 'color': 'yellow'},
                    {'label': 'Conflicts', 'value': '2', 'color': 'red'},
                    {'label': 'Coverage Rate', 'value': '92%', 'color': 'green'},
                ]
                
                for stat in summary_stats:
                    ui.html(f'<div class="flex-1 text-center"><div class="text-lg font-bold text-{stat["color"]}-600">{stat["value"]}</div><div class="text-sm text-gray-600">{stat["label"]}</div></div>', sanitize=False)

def create_schedule_requests_panel(manager: StaffScheduleManager):
    """Create schedule requests panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">📝 Schedule Requests</h2>', sanitize=False)
    
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
                ui.html('<div class="w-32 font-semibold">Employee</div>', sanitize=False)
                ui.html('<div class="w-32 font-semibold">Type</div>', sanitize=False)
                ui.html('<div class="w-32 font-semibold">Date</div>', sanitize=False)
                ui.html('<div class="flex-1 font-semibold">Details</div>', sanitize=False)
                ui.html('<div class="w-24 font-semibold">Status</div>', sanitize=False)
                ui.html('<div class="w-32 font-semibold">Actions</div>', sanitize=False)
            
            # Request rows
            for request in requests:
                with ui.row().classes('w-full p-4 border-b hover:bg-gray-50'):
                    ui.html(f'<div class="w-32">{request["employee_name"]}</div>', sanitize=False)
                    ui.html(f'<div class="w-32">{request["request_type"].replace("_", " ").title()}</div>', sanitize=False)
                    ui.html(f'<div class="w-32">{request["requested_date"]}</div>', sanitize=False)
                    ui.html(f'<div class="flex-1 text-sm">{request["reason"]}</div>', sanitize=False)
                    
                    # Status badge
                    status_colors = {
                        'pending': 'bg-yellow-100 text-yellow-800',
                        'approved': 'bg-green-100 text-green-800',
                        'denied': 'bg-red-100 text-red-800'
                    }
                    ui.html(f'<div class="w-24"><span class="px-2 py-1 rounded text-xs {status_colors.get(request["status"], "bg-gray-100 text-gray-800")}">{request["status"].title()}</span></div>', sanitize=False)
                    
                    # Action buttons
                    with ui.row().classes('w-32 gap-1'):
                        if request['status'] == 'pending':
                            ui.button('✅', on_click=lambda r=request['id']: ui.notify(f'Approving {r}')).classes('text-xs bg-green-500 text-white')
                            ui.button('❌', on_click=lambda r=request['id']: ui.notify(f'Denying {r}')).classes('text-xs bg-red-500 text-white')
                        ui.button('👁️', on_click=lambda r=request['id']: ui.notify(f'Viewing {r}')).classes('text-xs bg-blue-500 text-white')

def create_coverage_analysis_panel(manager: StaffScheduleManager):
    """Create coverage analysis panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">📊 Coverage Analysis</h2>', sanitize=False)
    
    # Coverage overview
    coverage = manager.schedule_data['coverage_analysis']
    
    with ui.card().classes('w-full mb-4'):
        with ui.card_section().classes('p-4'):
            ui.html('<h3 class="text-lg font-semibold mb-3">📈 Weekly Coverage Status</h3>', sanitize=False)
            
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
                            ui.html(f'<div class="font-semibold text-sm">{day.title()}</div>', sanitize=False)
                            ui.html(f'<div class="text-xs">{data["scheduled"]}/{data["required"]}</div>', sanitize=False)
                            ui.html(f'<div class="text-xs">{coverage_percent:.0f}%</div>', sanitize=False)
    
    # Detailed analysis
    with ui.row().classes('w-full gap-4'):
        # Understaffed alerts
        with ui.card().classes('flex-1'):
            with ui.card_section().classes('p-4'):
                ui.html('<h3 class="text-lg font-semibold mb-3 text-red-600">🚨 Understaffed Days</h3>', sanitize=False)
                understaffed_days = [day for day, data in coverage.items() if data['status'] == 'understaffed']
                
                if understaffed_days:
                    for day in understaffed_days:
                        data = coverage[day]
                        shortfall = data['required'] - data['scheduled']
                        ui.html(f'<div class="p-2 bg-red-50 rounded mb-2"><strong>{day.title()}:</strong> {shortfall} staff short</div>', sanitize=False)
                else:
                    ui.html('<div class="text-gray-500 text-center">No understaffed days</div>', sanitize=False)
        
        # Optimization suggestions
        with ui.card().classes('flex-1'):
            with ui.card_section().classes('p-4'):
                ui.html('<h3 class="text-lg font-semibold mb-3 text-blue-600">💡 Suggestions</h3>', sanitize=False)
                suggestions = [
                    'Consider hiring 2 additional part-time staff',
                    'Review Friday scheduling - consistently understaffed',
                    'Offer overtime incentives for Monday coverage',
                    'Cross-train employees for weekend shifts'
                ]
                
                for suggestion in suggestions:
                    ui.html(f'<div class="p-2 bg-blue-50 rounded mb-2 text-sm">• {suggestion}</div>', sanitize=False)

def create_schedule_settings_panel(manager: StaffScheduleManager):
    """Create schedule settings panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">⚙️ Schedule Settings</h2>', sanitize=False)
    
    settings = manager.schedule_data['schedule_settings']
    
    # General settings
    with ui.card().classes('w-full mb-4'):
        with ui.card_section().classes('p-4'):
            ui.html('<h3 class="text-lg font-semibold mb-3">🔧 General Settings</h3>', sanitize=False)
            
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
            ui.html('<h3 class="text-lg font-semibold mb-3">🔔 Notification Settings</h3>', sanitize=False)
            
            with ui.column().classes('w-full gap-2'):
                ui.checkbox('Email notifications for schedule changes', value=True)
                ui.checkbox('SMS reminders for shift start', value=False)
                ui.checkbox('Alert managers for coverage gaps', value=True)
                ui.checkbox('Notify employees of approved requests', value=True)
    
    # Save settings button
    ui.button('💾 Save Settings', on_click=lambda: ui.notify('Settings saved successfully!')).classes('bg-green-500 text-white')