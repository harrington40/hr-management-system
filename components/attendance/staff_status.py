"""
Staff and On Duty Status Management Component
Provides real-time tracking of staff attendance status, on-duty personnel, and status management
"""

from nicegui import ui
import yaml
import os
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any

class StaffStatusManager:
    """Manager class for staff status and on-duty tracking"""
    
    def __init__(self):
        self.config_dir = "config"
        self.staff_status_file = os.path.join(self.config_dir, "staff_status.yaml")
        self.staff_data_file = os.path.join(self.config_dir, "staff_data.yaml")
        self.ensure_config_directory()
        self.staff_status = self.load_staff_status()
        self.staff_data = self.load_staff_data()
    
    def ensure_config_directory(self):
        """Ensure config directory exists"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
    
    def load_staff_status(self) -> Dict[str, Any]:
        """Load staff status configuration from YAML file"""
        if os.path.exists(self.staff_status_file):
            try:
                with open(self.staff_status_file, 'r') as file:
                    return yaml.safe_load(file) or {}
            except Exception as e:
                print(f"Error loading staff status config: {e}")
                return self.get_default_staff_status()
        else:
            default_config = self.get_default_staff_status()
            self.save_staff_status(default_config)
            return default_config
    
    def load_staff_data(self) -> Dict[str, Any]:
        """Load staff data from YAML file"""
        if os.path.exists(self.staff_data_file):
            try:
                with open(self.staff_data_file, 'r') as file:
                    return yaml.safe_load(file) or {}
            except Exception as e:
                print(f"Error loading staff data: {e}")
                return self.get_default_staff_data()
        else:
            default_data = self.get_default_staff_data()
            self.save_staff_data(default_data)
            return default_data
    
    def get_default_staff_status(self) -> Dict[str, Any]:
        """Get default staff status configuration"""
        return {
            'status_types': {
                'on_duty': {
                    'name': 'On Duty',
                    'color': 'green',
                    'icon': '✅',
                    'description': 'Currently working and available'
                },
                'off_duty': {
                    'name': 'Off Duty',
                    'color': 'gray',
                    'icon': '⭕',
                    'description': 'Not currently working'
                },
                'on_break': {
                    'name': 'On Break',
                    'color': 'yellow',
                    'icon': '☕',
                    'description': 'Currently on break'
                },
                'on_leave': {
                    'name': 'On Leave',
                    'color': 'blue',
                    'icon': '🏖️',
                    'description': 'On approved leave'
                },
                'sick_leave': {
                    'name': 'Sick Leave',
                    'color': 'red',
                    'icon': '🤒',
                    'description': 'On sick leave'
                },
                'remote_work': {
                    'name': 'Remote Work',
                    'color': 'purple',
                    'icon': '🏠',
                    'description': 'Working remotely'
                }
            },
            'settings': {
                'auto_status_update': True,
                'break_timeout_minutes': 30,
                'status_sync_interval': 5,
                'show_location': True,
                'enable_notifications': True
            },
            'shift_patterns': {
                'morning': {'start': '09:00', 'end': '17:00'},
                'evening': {'start': '17:00', 'end': '01:00'},
                'night': {'start': '01:00', 'end': '09:00'}
            }
        }
    
    def get_default_staff_data(self) -> Dict[str, Any]:
        """Get default staff data with sample employees"""
        current_time = datetime.now()
        return {
            'employees': {
                'EMP001': {
                    'name': 'John Smith',
                    'department': 'Engineering',
                    'position': 'Senior Developer',
                    'email': 'john.smith@company.com',
                    'phone': '+1-555-0101',
                    'shift': 'morning',
                    'location': 'Office Floor 3',
                    'current_status': 'on_duty',
                    'last_status_update': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'check_in_time': '09:15',
                    'expected_check_out': '17:00',
                    'break_start': None,
                    'total_hours_today': 0,
                    'profile_image': None
                },
                'EMP002': {
                    'name': 'Sarah Johnson',
                    'department': 'Human Resources',
                    'position': 'HR Manager',
                    'email': 'sarah.johnson@company.com',
                    'phone': '+1-555-0102',
                    'shift': 'morning',
                    'location': 'Office Floor 2',
                    'current_status': 'on_break',
                    'last_status_update': (current_time - timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S'),
                    'check_in_time': '08:45',
                    'expected_check_out': '17:00',
                    'break_start': (current_time - timedelta(minutes=15)).strftime('%H:%M'),
                    'total_hours_today': 3.75,
                    'profile_image': None
                },
                'EMP003': {
                    'name': 'Mike Davis',
                    'department': 'Sales',
                    'position': 'Sales Representative',
                    'email': 'mike.davis@company.com',
                    'phone': '+1-555-0103',
                    'shift': 'morning',
                    'location': 'Remote',
                    'current_status': 'remote_work',
                    'last_status_update': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'check_in_time': '09:00',
                    'expected_check_out': '17:00',
                    'break_start': None,
                    'total_hours_today': 4.0,
                    'profile_image': None
                },
                'EMP004': {
                    'name': 'Lisa Wilson',
                    'department': 'Finance',
                    'position': 'Financial Analyst',
                    'email': 'lisa.wilson@company.com',
                    'phone': '+1-555-0104',
                    'shift': 'morning',
                    'location': 'Office Floor 1',
                    'current_status': 'on_leave',
                    'last_status_update': (current_time - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
                    'check_in_time': None,
                    'expected_check_out': None,
                    'break_start': None,
                    'total_hours_today': 0,
                    'profile_image': None
                }
            },
            'departments': {
                'Engineering': {'total_staff': 15, 'on_duty': 12, 'on_break': 2, 'off_duty': 1},
                'Human Resources': {'total_staff': 5, 'on_duty': 3, 'on_break': 1, 'off_duty': 1},
                'Sales': {'total_staff': 10, 'on_duty': 7, 'on_break': 1, 'remote_work': 2},
                'Finance': {'total_staff': 8, 'on_duty': 6, 'on_leave': 1, 'off_duty': 1}
            },
            'real_time_stats': {
                'total_employees': 38,
                'currently_on_duty': 28,
                'on_break': 4,
                'remote_workers': 2,
                'on_leave': 2,
                'off_duty': 2,
                'last_updated': current_time.strftime('%Y-%m-%d %H:%M:%S')
            }
        }
    
    def save_staff_status(self, config: Dict[str, Any]) -> bool:
        """Save staff status configuration to YAML file"""
        try:
            with open(self.staff_status_file, 'w') as file:
                yaml.dump(config, file, default_flow_style=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving staff status config: {e}")
            return False
    
    def save_staff_data(self, data: Dict[str, Any]) -> bool:
        """Save staff data to YAML file"""
        try:
            with open(self.staff_data_file, 'w') as file:
                yaml.dump(data, file, default_flow_style=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving staff data: {e}")
            return False
    
    def update_employee_status(self, emp_id: str, new_status: str) -> bool:
        """Update employee status"""
        if emp_id in self.staff_data['employees']:
            self.staff_data['employees'][emp_id]['current_status'] = new_status
            self.staff_data['employees'][emp_id]['last_status_update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return self.save_staff_data(self.staff_data)
        return False

def create_staff_status_page():
    """Create the main staff and on duty status page"""
    manager = StaffStatusManager()
    
    with ui.column().classes('w-full h-full bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen'):
        # Header Section
        with ui.row().classes('w-full p-6'):
            with ui.card().classes('w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white'):
                with ui.card_section().classes('p-6'):
                    with ui.row().classes('w-full justify-between items-center'):
                        ui.html('<h1 class="text-3xl font-bold flex items-center gap-3"><span class="text-4xl">👥</span>Staff & On Duty Status</h1>', sanitize=False).classes('mb-2')
                        with ui.row().classes('gap-4'):
                            ui.button('🔄 Refresh Status', on_click=lambda: ui.notify('Status refreshed!')).classes('bg-white text-blue-600 hover:bg-gray-100')
                            ui.button('📊 Generate Report', on_click=lambda: ui.notify('Report generated!')).classes('bg-white text-blue-600 hover:bg-gray-100')
                            ui.button('⚙️ Settings', on_click=lambda: ui.notify('Opening settings...')).classes('bg-white text-blue-600 hover:bg-gray-100')

        # Main Content Area
        with ui.row().classes('w-full px-6 gap-6'):
            # Left Sidebar - Navigation
            with ui.column().classes('w-1/4'):
                with ui.card().classes('w-full'):
                    with ui.card_section().classes('p-4'):
                        ui.html('<h3 class="text-lg font-semibold text-gray-800 mb-4">📋 View Options</h3>', sanitize=False)
                        
                        view_options = [
                            {'id': 'dashboard', 'name': 'Status Dashboard', 'icon': '📊', 'color': 'blue'},
                            {'id': 'staff_list', 'name': 'Staff Directory', 'icon': '👥', 'color': 'green'},
                            {'id': 'on_duty', 'name': 'On Duty Personnel', 'icon': '✅', 'color': 'emerald'},
                            {'id': 'breaks', 'name': 'Break Management', 'icon': '☕', 'color': 'yellow'},
                            {'id': 'attendance', 'name': 'Attendance Log', 'icon': '📅', 'color': 'purple'},
                            {'id': 'departments', 'name': 'Department View', 'icon': '🏢', 'color': 'indigo'},
                            {'id': 'analytics', 'name': 'Analytics', 'icon': '📈', 'color': 'pink'},
                        ]
                        
                        # Simple state management without ui.state()
                        class ViewState:
                            def __init__(self):
                                self.current = 'dashboard'
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
                        state.panels['dashboard'] = ui.column().classes('w-full')
                        with state.panels['dashboard']:
                            create_status_dashboard_panel(manager)
                        
                        state.panels['staff_list'] = ui.column().classes('w-full')
                        with state.panels['staff_list']:
                            create_staff_directory_panel(manager)
                        state.panels['staff_list'].set_visibility(False)
                            
                        state.panels['on_duty'] = ui.column().classes('w-full')
                        with state.panels['on_duty']:
                            create_on_duty_panel(manager)
                        state.panels['on_duty'].set_visibility(False)
                            
                        state.panels['breaks'] = ui.column().classes('w-full')
                        with state.panels['breaks']:
                            create_break_management_panel(manager)
                        state.panels['breaks'].set_visibility(False)
                            
                        state.panels['attendance'] = ui.column().classes('w-full')
                        with state.panels['attendance']:
                            create_attendance_log_panel(manager)
                        state.panels['attendance'].set_visibility(False)
                            
                        state.panels['departments'] = ui.column().classes('w-full')
                        with state.panels['departments']:
                            create_department_view_panel(manager)
                        state.panels['departments'].set_visibility(False)
                            
                        state.panels['analytics'] = ui.column().classes('w-full')
                        with state.panels['analytics']:
                            create_analytics_panel(manager)
                        state.panels['analytics'].set_visibility(False)

def create_status_dashboard_panel(manager: StaffStatusManager):
    """Create the main status dashboard panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">📊 Real-Time Status Dashboard</h2>', sanitize=False)
    
    # Real-time stats cards
    with ui.row().classes('w-full gap-4 mb-6'):
        stats = manager.staff_data['real_time_stats']
        
        # Total Employees Card
        with ui.card().classes('flex-1 bg-gradient-to-r from-blue-500 to-blue-600 text-white'):
            with ui.card_section().classes('p-4 text-center'):
                ui.html('<div class="text-3xl font-bold">👥</div>', sanitize=False)
                ui.html(f'<div class="text-2xl font-bold">{stats["total_employees"]}</div>', sanitize=False)
                ui.html('<div class="text-sm opacity-90">Total Employees</div>', sanitize=False)
        
        # On Duty Card
        with ui.card().classes('flex-1 bg-gradient-to-r from-green-500 to-green-600 text-white'):
            with ui.card_section().classes('p-4 text-center'):
                ui.html('<div class="text-3xl font-bold">✅</div>', sanitize=False)
                ui.html(f'<div class="text-2xl font-bold">{stats["currently_on_duty"]}</div>', sanitize=False)
                ui.html('<div class="text-sm opacity-90">Currently On Duty</div>', sanitize=False)
        
        # On Break Card
        with ui.card().classes('flex-1 bg-gradient-to-r from-yellow-500 to-yellow-600 text-white'):
            with ui.card_section().classes('p-4 text-center'):
                ui.html('<div class="text-3xl font-bold">☕</div>', sanitize=False)
                ui.html(f'<div class="text-2xl font-bold">{stats["on_break"]}</div>', sanitize=False)
                ui.html('<div class="text-sm opacity-90">On Break</div>', sanitize=False)
        
        # Remote Workers Card
        with ui.card().classes('flex-1 bg-gradient-to-r from-purple-500 to-purple-600 text-white'):
            with ui.card_section().classes('p-4 text-center'):
                ui.html('<div class="text-3xl font-bold">🏠</div>', sanitize=False)
                ui.html(f'<div class="text-2xl font-bold">{stats["remote_workers"]}</div>', sanitize=False)
                ui.html('<div class="text-sm opacity-90">Remote Workers</div>', sanitize=False)
    
    # Live Status Feed
    ui.html('<h3 class="text-xl font-semibold text-gray-800 mb-4">🔴 Live Status Updates</h3>', sanitize=False)
    
    with ui.card().classes('w-full'):
        with ui.card_section().classes('p-4'):
            # Status timeline
            status_updates = [
                {'time': '13:45', 'employee': 'John Smith', 'action': 'Returned from break', 'status': 'on_duty'},
                {'time': '13:30', 'employee': 'Sarah Johnson', 'action': 'Started break', 'status': 'on_break'},
                {'time': '13:15', 'employee': 'Mike Davis', 'action': 'Checked in remotely', 'status': 'remote_work'},
                {'time': '13:00', 'employee': 'Lisa Wilson', 'action': 'Approved leave started', 'status': 'on_leave'},
            ]
            
            for update in status_updates:
                with ui.row().classes('w-full p-3 border-b border-gray-200 hover:bg-gray-50'):
                    ui.html(f'<div class="text-sm text-gray-500 w-16">{update["time"]}</div>', sanitize=False)
                    ui.html(f'<div class="flex-1 font-medium">{update["employee"]}</div>', sanitize=False)
                    ui.html(f'<div class="text-sm text-gray-600">{update["action"]}</div>', sanitize=False)
                    status_colors = {
                        'on_duty': 'bg-green-100 text-green-800',
                        'on_break': 'bg-yellow-100 text-yellow-800',
                        'remote_work': 'bg-purple-100 text-purple-800',
                        'on_leave': 'bg-blue-100 text-blue-800'
                    }
                    ui.html(f'<div class="px-2 py-1 rounded text-xs {status_colors.get(update["status"], "bg-gray-100 text-gray-800")}">{update["status"].replace("_", " ").title()}</div>', sanitize=False)

def create_staff_directory_panel(manager: StaffStatusManager):
    """Create staff directory panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">👥 Staff Directory</h2>', sanitize=False)
    
    # Search and filters
    with ui.row().classes('w-full gap-4 mb-4'):
        ui.input('Search employees...').classes('flex-1')
        ui.select(['All Departments', 'Engineering', 'HR', 'Sales', 'Finance'], value='All Departments').classes('w-48')
        ui.select(['All Status', 'On Duty', 'Off Duty', 'On Break', 'On Leave'], value='All Status').classes('w-48')
    
    # Employee cards grid
    with ui.row().classes('w-full gap-4 flex-wrap'):
        for emp_id, employee in manager.staff_data['employees'].items():
            with ui.card().classes('w-64 hover:shadow-lg transition-shadow'):
                with ui.card_section().classes('p-4'):
                    # Employee header
                    with ui.row().classes('w-full items-center mb-3'):
                        ui.avatar(text=employee['name'][:2], color='bg-blue-500').classes('mr-3')
                        with ui.column().classes('flex-1'):
                            ui.html(f'<div class="font-semibold">{employee["name"]}</div>', sanitize=False)
                            ui.html(f'<div class="text-sm text-gray-600">{employee["position"]}</div>', sanitize=False)
                    
                    # Status badge
                    status_info = manager.staff_status['status_types'].get(employee['current_status'], {})
                    status_color = status_info.get('color', 'gray')
                    status_icon = status_info.get('icon', '⚪')
                    ui.html(f'<div class="mb-3"><span class="px-2 py-1 rounded text-xs bg-{status_color}-100 text-{status_color}-800">{status_icon} {status_info.get("name", employee["current_status"])}</span></div>', sanitize=False)
                    
                    # Employee details
                    ui.html(f'<div class="text-sm text-gray-600 mb-1">📧 {employee["email"]}</div>', sanitize=False)
                    ui.html(f'<div class="text-sm text-gray-600 mb-1">🏢 {employee["department"]}</div>', sanitize=False)
                    ui.html(f'<div class="text-sm text-gray-600 mb-1">📍 {employee["location"]}</div>', sanitize=False)
                    
                    # Action buttons
                    with ui.row().classes('w-full gap-2 mt-3'):
                        ui.button('👁️', on_click=lambda e=emp_id: ui.notify(f'Viewing {e}')).classes('text-xs')
                        ui.button('✏️', on_click=lambda e=emp_id: ui.notify(f'Editing {e}')).classes('text-xs')
                        ui.button('📞', on_click=lambda e=emp_id: ui.notify(f'Calling {e}')).classes('text-xs')

def create_on_duty_panel(manager: StaffStatusManager):
    """Create on-duty personnel panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">✅ On Duty Personnel</h2>', sanitize=False)
    
    # On-duty summary
    on_duty_count = sum(1 for emp in manager.staff_data['employees'].values() if emp['current_status'] == 'on_duty')
    ui.html(f'<div class="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg"><span class="text-green-800 font-semibold">🟢 {on_duty_count} employees currently on duty</span></div>', sanitize=False)
    
    # On-duty staff table
    with ui.card().classes('w-full'):
        with ui.card_section().classes('p-0'):
            # Table header
            with ui.row().classes('w-full p-4 bg-gray-50 border-b'):
                ui.html('<div class="w-1/4 font-semibold">Employee</div>', sanitize=False)
                ui.html('<div class="w-1/4 font-semibold">Department</div>', sanitize=False)
                ui.html('<div class="w-1/4 font-semibold">Check-in Time</div>', sanitize=False)
                ui.html('<div class="w-1/4 font-semibold">Hours Today</div>', sanitize=False)
            
            # Table rows
            for emp_id, employee in manager.staff_data['employees'].items():
                if employee['current_status'] == 'on_duty':
                    with ui.row().classes('w-full p-4 border-b hover:bg-gray-50'):
                        ui.html(f'<div class="w-1/4"><strong>{employee["name"]}</strong><br><small>{employee["position"]}</small></div>', sanitize=False)
                        ui.html(f'<div class="w-1/4">{employee["department"]}</div>', sanitize=False)
                        ui.html(f'<div class="w-1/4">{employee.get("check_in_time", "N/A")}</div>', sanitize=False)
                        ui.html(f'<div class="w-1/4">{employee.get("total_hours_today", 0):.1f} hours</div>', sanitize=False)

def create_break_management_panel(manager: StaffStatusManager):
    """Create break management panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">☕ Break Management</h2>', sanitize=False)
    
    # Break summary
    on_break_count = sum(1 for emp in manager.staff_data['employees'].values() if emp['current_status'] == 'on_break')
    ui.html(f'<div class="mb-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg"><span class="text-yellow-800 font-semibold">☕ {on_break_count} employees currently on break</span></div>', sanitize=False)
    
    # Break policy settings
    with ui.card().classes('w-full mb-4'):
        with ui.card_section().classes('p-4'):
            ui.html('<h3 class="text-lg font-semibold mb-3">⚙️ Break Policy Settings</h3>', sanitize=False)
            with ui.row().classes('w-full gap-4'):
                ui.number('Break Duration (minutes)', value=30).classes('flex-1')
                ui.number('Maximum Daily Breaks', value=2).classes('flex-1')
                ui.checkbox('Auto-return from break', value=True)
    
    # Current breaks
    ui.html('<h3 class="text-lg font-semibold mb-3">🕐 Current Breaks</h3>', sanitize=False)
    
    with ui.card().classes('w-full'):
        with ui.card_section().classes('p-0'):
            for emp_id, employee in manager.staff_data['employees'].items():
                if employee['current_status'] == 'on_break':
                    with ui.row().classes('w-full p-4 border-b items-center'):
                        ui.avatar(text=employee['name'][:2], color='bg-yellow-500').classes('mr-4')
                        with ui.column().classes('flex-1'):
                            ui.html(f'<div class="font-semibold">{employee["name"]}</div>', sanitize=False)
                            ui.html(f'<div class="text-sm text-gray-600">Started break at {employee.get("break_start", "N/A")}</div>', sanitize=False)
                        ui.button('Return from Break', on_click=lambda e=emp_id: manager.update_employee_status(e, 'on_duty')).classes('bg-green-500 text-white')

def create_attendance_log_panel(manager: StaffStatusManager):
    """Create attendance log panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">📅 Attendance Log</h2>', sanitize=False)
    
    # Date range selector
    with ui.row().classes('w-full gap-4 mb-4'):
        ui.date('From Date', value=datetime.now().strftime('%Y-%m-%d')).classes('w-48')
        ui.date('To Date', value=datetime.now().strftime('%Y-%m-%d')).classes('w-48')
        ui.button('🔍 Filter', on_click=lambda: ui.notify('Filtering attendance...')).classes('bg-blue-500 text-white')
        ui.button('📊 Export', on_click=lambda: ui.notify('Exporting data...')).classes('bg-green-500 text-white')
    
    # Attendance summary
    with ui.row().classes('w-full gap-4 mb-4'):
        with ui.card().classes('flex-1'):
            with ui.card_section().classes('p-4 text-center'):
                ui.html('<div class="text-2xl font-bold text-green-600">95%</div>', sanitize=False)
                ui.html('<div class="text-sm text-gray-600">Attendance Rate</div>', sanitize=False)
        
        with ui.card().classes('flex-1'):
            with ui.card_section().classes('p-4 text-center'):
                ui.html('<div class="text-2xl font-bold text-blue-600">7.8</div>', sanitize=False)
                ui.html('<div class="text-sm text-gray-600">Avg Hours/Day</div>', sanitize=False)
        
        with ui.card().classes('flex-1'):
            with ui.card_section().classes('p-4 text-center'):
                ui.html('<div class="text-2xl font-bold text-yellow-600">12</div>', sanitize=False)
                ui.html('<div class="text-sm text-gray-600">Late Arrivals</div>', sanitize=False)

def create_department_view_panel(manager: StaffStatusManager):
    """Create department view panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">🏢 Department Overview</h2>', sanitize=False)
    
    # Department cards
    with ui.row().classes('w-full gap-4 flex-wrap'):
        for dept_name, dept_data in manager.staff_data['departments'].items():
            with ui.card().classes('w-64 hover:shadow-lg transition-shadow'):
                with ui.card_section().classes('p-4'):
                    ui.html(f'<h3 class="text-lg font-semibold mb-3">🏢 {dept_name}</h3>', sanitize=False)
                    
                    # Department stats
                    ui.html(f'<div class="mb-2">👥 Total Staff: <strong>{dept_data["total_staff"]}</strong></div>', sanitize=False)
                    ui.html(f'<div class="mb-2 text-green-600">✅ On Duty: <strong>{dept_data.get("on_duty", 0)}</strong></div>', sanitize=False)
                    ui.html(f'<div class="mb-2 text-yellow-600">☕ On Break: <strong>{dept_data.get("on_break", 0)}</strong></div>', sanitize=False)
                    ui.html(f'<div class="mb-2 text-gray-600">⭕ Off Duty: <strong>{dept_data.get("off_duty", 0)}</strong></div>', sanitize=False)
                    
                    # Progress bar
                    on_duty_percentage = (dept_data.get("on_duty", 0) / dept_data["total_staff"]) * 100
                    ui.html(f'<div class="w-full bg-gray-200 rounded-full h-2 mt-3"><div class="bg-green-500 h-2 rounded-full" style="width: {on_duty_percentage}%"></div></div>', sanitize=False)
                    ui.html(f'<div class="text-xs text-gray-600 mt-1">{on_duty_percentage:.0f}% Active</div>', sanitize=False)

def create_analytics_panel(manager: StaffStatusManager):
    """Create analytics panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">📈 Staff Analytics</h2>', sanitize=False)
    
    # Analytics cards
    with ui.row().classes('w-full gap-4 mb-6'):
        with ui.card().classes('flex-1'):
            with ui.card_section().classes('p-4'):
                ui.html('<h3 class="text-lg font-semibold mb-3">📊 Weekly Trends</h3>', sanitize=False)
                ui.html('<div class="h-48 bg-gray-100 rounded flex items-center justify-center text-gray-500">Weekly attendance chart placeholder</div>', sanitize=False)
        
        with ui.card().classes('flex-1'):
            with ui.card_section().classes('p-4'):
                ui.html('<h3 class="text-lg font-semibold mb-3">🕐 Peak Hours</h3>', sanitize=False)
                ui.html('<div class="h-48 bg-gray-100 rounded flex items-center justify-center text-gray-500">Peak hours chart placeholder</div>', sanitize=False)
    
    # Analytics metrics
    with ui.row().classes('w-full gap-4'):
        metrics = [
            {'title': 'Average Daily Attendance', 'value': '92%', 'trend': '+2.3%', 'color': 'green'},
            {'title': 'Average Break Duration', 'value': '28 min', 'trend': '-1.2%', 'color': 'blue'},
            {'title': 'Remote Work Rate', 'value': '15%', 'trend': '+5.1%', 'color': 'purple'},
            {'title': 'Overtime Hours', 'value': '124h', 'trend': '-8.5%', 'color': 'yellow'},
        ]
        
        for metric in metrics:
            with ui.card().classes('flex-1'):
                with ui.card_section().classes('p-4 text-center'):
                    ui.html(f'<div class="text-2xl font-bold text-{metric["color"]}-600">{metric["value"]}</div>', sanitize=False)
                    ui.html(f'<div class="text-sm text-gray-600 mb-1">{metric["title"]}</div>', sanitize=False)
                    ui.html(f'<div class="text-xs text-{metric["color"]}-600">{metric["trend"]}</div>', sanitize=False)