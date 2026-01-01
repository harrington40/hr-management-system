"""
Enterprise Staff Status & Attendance Management System
Comprehensive real-time tracking of staff attendance, performance metrics, and workforce analytics
Integrated with HR Holiday & Vacation Management System
"""

from nicegui import ui
import yaml
import os
from datetime import datetime, timedelta, date
import json
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

# Import employee data manager for real-time statistics
from components.administration.enroll_staff import employee_data_manager

class StaffStatus(Enum):
    ON_DUTY = "on_duty"
    OFF_DUTY = "off_duty"
    ON_BREAK = "on_break"
    IN_MEETING = "in_meeting"
    ON_LEAVE = "on_leave"
    REMOTE_WORK = "remote_work"
    EMERGENCY_LEAVE = "emergency_leave"
    SICK_LEAVE = "sick_leave"
    VACATION = "vacation"
    TRAINING = "training"

class AttendanceMode(Enum):
    CLOCK_IN = "clock_in"
    CLOCK_OUT = "clock_out"
    BREAK_START = "break_start"
    BREAK_END = "break_end"
    LUNCH_START = "lunch_start"
    LUNCH_END = "lunch_end"

@dataclass
class StaffMember:
    employee_id: str
    name: str
    department: str
    position: str
    email: str
    phone: str
    current_status: StaffStatus
    shift_start: str
    shift_end: str
    last_activity: datetime
    attendance_score: float = 0.0
    performance_rating: str = "Good"

@dataclass
class AttendanceRecord:
    employee_id: str
    timestamp: datetime
    action: AttendanceMode
    location: str
    notes: str = ""

class StaffStatusManager:
    """Enterprise Staff Status and Attendance Management System"""
    
    def __init__(self):
        self.config_dir = "config"
        self.staff_status_file = os.path.join(self.config_dir, "staff_status.yaml")
        self.staff_data_file = os.path.join(self.config_dir, "staff_data.yaml")
        self.attendance_records_file = os.path.join(self.config_dir, "attendance_records.yaml")
        self.performance_metrics_file = os.path.join(self.config_dir, "performance_metrics.yaml")
        
        self.ensure_config_directory()
        self.staff_status = self.load_staff_status()
        self.staff_data = self.load_staff_data()
        self.attendance_records = self.load_attendance_records()
        self.performance_metrics = self.load_performance_metrics()
    
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
    
    def load_attendance_records(self) -> Dict[str, Any]:
        """Load attendance records from YAML file"""
        if os.path.exists(self.attendance_records_file):
            try:
                with open(self.attendance_records_file, 'r') as file:
                    return yaml.safe_load(file) or {}
            except Exception as e:
                print(f"Error loading attendance records: {e}")
                return self.get_default_attendance_records()
        else:
            default_records = self.get_default_attendance_records()
            self.save_attendance_records(default_records)
            return default_records
    
    def load_performance_metrics(self) -> Dict[str, Any]:
        """Load performance metrics from YAML file"""
        if os.path.exists(self.performance_metrics_file):
            try:
                with open(self.performance_metrics_file, 'r') as file:
                    return yaml.safe_load(file) or {}
            except Exception as e:
                print(f"Error loading performance metrics: {e}")
                return self.get_default_performance_metrics()
        else:
            default_metrics = self.get_default_performance_metrics()
            self.save_performance_metrics(default_metrics)
            return default_metrics
    
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
        """Generate comprehensive default staff data"""
        current_time = datetime.now()
        return {
            'staff_members': {
                'SM001': {
                    'employee_id': 'SM001',
                    'first_name': 'John',
                    'last_name': 'Smith',
                    'email': 'john.smith@company.com',
                    'phone': '+1-555-0101',
                    'department': 'Engineering',
                    'position': 'Senior Software Engineer',
                    'manager_id': 'SM005',
                    'hire_date': '2023-01-15',
                    'status': 'active',
                    'shift_pattern': 'standard',
                    'location': 'Main Office - Floor 3',
                    'current_status': 'on_duty',
                    'last_status_update': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'check_in_time': '09:15',
                    'expected_check_out': '17:00',
                    'break_start': None,
                    'total_hours_today': 4.5,
                    'emergency_contact': {
                        'name': 'Jane Smith',
                        'phone': '+1-555-0102',
                        'relationship': 'Spouse'
                    }
                },
                'SM002': {
                    'employee_id': 'SM002',
                    'first_name': 'Sarah',
                    'last_name': 'Johnson',
                    'email': 'sarah.johnson@company.com',
                    'phone': '+1-555-0103',
                    'department': 'Marketing',
                    'position': 'Marketing Manager',
                    'manager_id': 'SM006',
                    'hire_date': '2022-11-08',
                    'status': 'active',
                    'shift_pattern': 'flexible',
                    'location': 'Main Office - Floor 2',
                    'current_status': 'on_break',
                    'last_status_update': (current_time - timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S'),
                    'check_in_time': '08:45',
                    'expected_check_out': '17:00',
                    'break_start': (current_time - timedelta(minutes=15)).strftime('%H:%M'),
                    'total_hours_today': 3.75,
                    'emergency_contact': {
                        'name': 'Michael Johnson',
                        'phone': '+1-555-0104',
                        'relationship': 'Partner'
                    }
                },
                'SM003': {
                    'employee_id': 'SM003',
                    'first_name': 'David',
                    'last_name': 'Wilson',
                    'email': 'david.wilson@company.com',
                    'phone': '+1-555-0105',
                    'department': 'Sales',
                    'position': 'Sales Representative',
                    'manager_id': 'SM007',
                    'hire_date': '2023-03-22',
                    'status': 'active',
                    'shift_pattern': 'standard',
                    'location': 'Regional Office - West',
                    'current_status': 'remote_work',
                    'last_status_update': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'check_in_time': '09:00',
                    'expected_check_out': '17:00',
                    'break_start': None,
                    'total_hours_today': 4.0,
                    'emergency_contact': {
                        'name': 'Lisa Wilson',
                        'phone': '+1-555-0106',
                        'relationship': 'Spouse'
                    }
                },
                'SM004': {
                    'employee_id': 'SM004',
                    'first_name': 'Emily',
                    'last_name': 'Brown',
                    'email': 'emily.brown@company.com',
                    'phone': '+1-555-0107',
                    'department': 'Human Resources',
                    'position': 'HR Specialist',
                    'manager_id': 'SM008',
                    'hire_date': '2023-02-10',
                    'status': 'active',
                    'shift_pattern': 'standard',
                    'location': 'Main Office - Floor 1',
                    'current_status': 'on_leave',
                    'last_status_update': (current_time - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
                    'check_in_time': None,
                    'expected_check_out': None,
                    'break_start': None,
                    'total_hours_today': 0,
                    'emergency_contact': {
                        'name': 'Robert Brown',
                        'phone': '+1-555-0108',
                        'relationship': 'Father'
                    }
                },
                'SM005': {
                    'employee_id': 'SM005',
                    'first_name': 'Michael',
                    'last_name': 'Davis',
                    'email': 'michael.davis@company.com',
                    'phone': '+1-555-0109',
                    'department': 'Engineering',
                    'position': 'Engineering Manager',
                    'manager_id': None,
                    'hire_date': '2021-07-20',
                    'status': 'active',
                    'shift_pattern': 'executive',
                    'location': 'Main Office - Floor 3',
                    'current_status': 'on_duty',
                    'last_status_update': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'check_in_time': '08:30',
                    'expected_check_out': '18:00',
                    'break_start': None,
                    'total_hours_today': 5.5,
                    'emergency_contact': {
                        'name': 'Jennifer Davis',
                        'phone': '+1-555-0110',
                        'relationship': 'Spouse'
                    }
                }
            },
            'departments': {
                'Engineering': {
                    'name': 'Engineering',
                    'manager_id': 'SM005',
                    'total_staff': 25,
                    'on_duty': 20,
                    'on_break': 3,
                    'remote_work': 2,
                    'budget': 2500000,
                    'location': 'Main Office - Floor 3'
                },
                'Marketing': {
                    'name': 'Marketing',
                    'manager_id': 'SM006',
                    'total_staff': 12,
                    'on_duty': 9,
                    'on_break': 2,
                    'remote_work': 1,
                    'budget': 800000,
                    'location': 'Main Office - Floor 2'
                },
                'Sales': {
                    'name': 'Sales',
                    'manager_id': 'SM007',
                    'total_staff': 18,
                    'on_duty': 14,
                    'on_break': 1,
                    'remote_work': 3,
                    'budget': 1200000,
                    'location': 'Multiple Locations'
                },
                'Human Resources': {
                    'name': 'Human Resources',
                    'manager_id': 'SM008',
                    'total_staff': 8,
                    'on_duty': 6,
                    'on_break': 1,
                    'on_leave': 1,
                    'budget': 600000,
                    'location': 'Main Office - Floor 1'
                }
            },
            'shift_patterns': {
                'standard': {
                    'name': 'Standard Business Hours',
                    'start_time': '09:00',
                    'end_time': '17:00',
                    'break_duration': 60,
                    'flexible_minutes': 15
                },
                'flexible': {
                    'name': 'Flexible Hours',
                    'core_start': '10:00',
                    'core_end': '15:00',
                    'earliest_start': '07:00',
                    'latest_end': '19:00',
                    'daily_hours': 8
                },
                'executive': {
                    'name': 'Executive Schedule',
                    'flexible': True,
                    'minimum_hours': 8,
                    'overtime_exempt': True
                }
            },
            'real_time_stats': {
                'total_employees': len(employee_data_manager.employees),
                'currently_on_duty': max(1, int(len(employee_data_manager.employees) * 0.75)),  # Assume 75% on duty
                'on_break': max(0, int(len(employee_data_manager.employees) * 0.10)),  # Assume 10% on break
                'remote_workers': max(0, int(len(employee_data_manager.employees) * 0.15)),  # Assume 15% remote
                'on_leave': max(0, int(len(employee_data_manager.employees) * 0.05)),  # Assume 5% on leave
                'off_duty': max(0, len(employee_data_manager.employees) - int(len(employee_data_manager.employees) * 0.75) - int(len(employee_data_manager.employees) * 0.10) - int(len(employee_data_manager.employees) * 0.15) - int(len(employee_data_manager.employees) * 0.05)),
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
    
    def update_attendance_calculations(self):
        """Update attendance calculations based on current rules"""
        try:
            # Load current attendance rules
            from components.attendance.attendance_rules import AttendanceRulesManager
            rules_manager = AttendanceRulesManager()
            rules = rules_manager.rules_data.get('attendance_rules', {})
            
            # Recalculate attendance metrics for all employees
            for emp_id, emp_data in self.staff_data.get('employees', {}).items():
                # Apply current rules to calculate attendance score
                attendance_score = self._calculate_employee_attendance_score(emp_id, rules)
                emp_data['attendance_score'] = attendance_score
                
                # Update performance rating based on score
                emp_data['performance_rating'] = self._get_performance_rating(attendance_score)
            
            # Save updated calculations
            self.save_staff_data(self.staff_data)
            print(f"✅ Attendance calculations updated for {len(self.staff_data.get('employees', {}))} employees")
            
        except Exception as e:
            print(f"Error updating attendance calculations: {e}")
    
    def _calculate_employee_attendance_score(self, emp_id: str, rules: Dict[str, Any]) -> float:
        """Calculate attendance score for an employee based on current rules"""
        # This is a simplified calculation - in a real system this would be more complex
        base_score = 85.0  # Base attendance score
        
        # Apply rule-based adjustments
        core_settings = rules.get('core_settings', {})
        grace_period = core_settings.get('grace_period_minutes', 15)
        
        # Simulate some rule-based adjustments
        if grace_period > 20:
            base_score += 2.0  # More lenient grace period
        elif grace_period < 10:
            base_score -= 2.0  # Stricter grace period
        
        working_days = core_settings.get('working_days_per_week', 5)
        if working_days == 6:
            base_score -= 1.0  # 6-day week is more demanding
        
        # Random variation to simulate real attendance data
        import random
        variation = random.uniform(-5.0, 5.0)
        
        return max(0.0, min(100.0, base_score + variation))
    
    def _get_performance_rating(self, score: float) -> str:
        """Get performance rating based on attendance score"""
        if score >= 95:
            return "Excellent"
        elif score >= 85:
            return "Good"
        elif score >= 75:
            return "Satisfactory"
        elif score >= 65:
            return "Needs Improvement"
        else:
            return "Poor"
    
    def get_default_attendance_records(self) -> Dict[str, Any]:
        """Generate default attendance records"""
        from datetime import datetime, timedelta
        
        today = datetime.now()
        records = {}
        
        # Generate sample attendance for the last 7 days
        for days_back in range(7):
            date = (today - timedelta(days=days_back)).strftime('%Y-%m-%d')
            records[date] = {}
            
            for emp_id in ['SM001', 'SM002', 'SM003', 'SM004', 'SM005']:
                if days_back < 5:  # Weekdays
                    records[date][emp_id] = {
                        'check_in': '09:00:00',
                        'check_out': '17:00:00',
                        'break_start': '12:00:00',
                        'break_end': '13:00:00',
                        'total_hours': 7.0,
                        'status': 'present',
                        'notes': ''
                    }
        
        return {'daily_records': records}
    
    def get_default_performance_metrics(self) -> Dict[str, Any]:
        """Generate default performance metrics"""
        return {
            'attendance_rates': {
                'SM001': {'rate': 98.5, 'days_present': 197, 'days_total': 200},
                'SM002': {'rate': 96.8, 'days_present': 194, 'days_total': 200},
                'SM003': {'rate': 99.2, 'days_present': 198, 'days_total': 200},
                'SM004': {'rate': 97.1, 'days_present': 194, 'days_total': 200},
                'SM005': {'rate': 95.5, 'days_present': 191, 'days_total': 200}
            },
            'overtime_hours': {
                'SM001': {'monthly': 8.5, 'yearly': 102},
                'SM002': {'monthly': 4.2, 'yearly': 50},
                'SM003': {'monthly': 12.1, 'yearly': 145},
                'SM004': {'monthly': 6.8, 'yearly': 82},
                'SM005': {'monthly': 15.5, 'yearly': 186}
            },
            'productivity_scores': {
                'SM001': 87.5,
                'SM002': 92.1,
                'SM003': 84.8,
                'SM004': 89.6,
                'SM005': 94.2
            }
        }
    
    def save_attendance_records(self, records: Dict[str, Any]) -> bool:
        """Save attendance records to YAML file"""
        try:
            with open(self.attendance_records_file, 'w') as file:
                yaml.dump(records, file, default_flow_style=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving attendance records: {e}")
            return False
    
    def save_performance_metrics(self, metrics: Dict[str, Any]) -> bool:
        """Save performance metrics to YAML file"""
        try:
            with open(self.performance_metrics_file, 'w') as file:
                yaml.dump(metrics, file, default_flow_style=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving performance metrics: {e}")
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
                        # Create a simple avatar-like element with initials
                        with ui.element('div').classes('w-10 h-10 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-bold mr-3'):
                            ui.label(employee['name'][:2].upper())
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
                        # Create a simple avatar-like element with initials for break status
                        with ui.element('div').classes('w-10 h-10 bg-yellow-500 text-white rounded-full flex items-center justify-center text-sm font-bold mr-4'):
                            ui.label(employee['name'][:2].upper())
                        with ui.column().classes('flex-1'):
                            ui.html(f'<div class="font-semibold">{employee["name"]}</div>', sanitize=False)
                            ui.html(f'<div class="text-sm text-gray-600">Started break at {employee.get("break_start", "N/A")}</div>', sanitize=False)
                        ui.button('Return from Break', on_click=lambda e=emp_id: manager.update_employee_status(e, 'on_duty')).classes('bg-green-500 text-white')

def create_attendance_log_panel(manager: StaffStatusManager):
    """Create attendance log panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">📅 Attendance Log</h2>', sanitize=False)
    
    # Date range selector
    with ui.row().classes('w-full gap-4 mb-4'):
        with ui.input('From Date').classes('w-48') as from_date:
            from_date.props('type=date')
            from_date.value = datetime.now().strftime('%Y-%m-%d')
        with ui.input('To Date').classes('w-48') as to_date:
            to_date.props('type=date')
            to_date.value = datetime.now().strftime('%Y-%m-%d')
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