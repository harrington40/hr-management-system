"""
Comprehensive Modern HR Management Dashboard
Enterprise-grade interface for employers and employees with hardware integration
Real-time analytics, workforce management, and intelligent algorithms
"""

from nicegui import ui
import yaml
import os
from datetime import datetime, timedelta, date
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import random

class UserRole(Enum):
    ADMIN = "admin"
    HR_MANAGER = "hr_manager"
    DEPARTMENT_MANAGER = "department_manager"
    EMPLOYEE = "employee"
    EXECUTIVE = "executive"

class DashboardWidget(Enum):
    ATTENDANCE_OVERVIEW = "attendance_overview"
    PERFORMANCE_METRICS = "performance_metrics"
    LEAVE_REQUESTS = "leave_requests"
    PAYROLL_SUMMARY = "payroll_summary"
    EMPLOYEE_DIRECTORY = "employee_directory"
    COMPLIANCE_STATUS = "compliance_status"
    HARDWARE_STATUS = "hardware_status"
    REAL_TIME_ALERTS = "real_time_alerts"

@dataclass
class HardwareDevice:
    device_id: str
    device_type: str  # biometric, card_reader, face_recognition, temperature_scanner
    location: str
    status: str  # online, offline, maintenance
    last_sync: datetime
    battery_level: Optional[int] = None
    connected_employees: List[str] = field(default_factory=list)

@dataclass
class DashboardMetrics:
    total_employees: int
    present_today: int
    absent_today: int
    on_leave: int
    remote_workers: int
    late_arrivals: int
    early_departures: int
    overtime_hours: float
    productivity_score: float
    compliance_rate: float

class HRDashboardManager:
    """Enterprise HR Dashboard Management System with Hardware Integration"""
    
    def __init__(self):
        self.config_dir = "config"
        self.dashboard_config_file = os.path.join(self.config_dir, "dashboard_config.yaml")
        self.hardware_config_file = os.path.join(self.config_dir, "hardware_devices.yaml")
        self.user_preferences_file = os.path.join(self.config_dir, "user_preferences.yaml")
        
        self.ensure_config_directory()
        self.dashboard_config = self.load_dashboard_config()
        self.hardware_devices = self.load_hardware_devices()
        self.user_preferences = self.load_user_preferences()
        
        # Initialize real-time data
        self.current_metrics = self.calculate_metrics()
        self.alerts = self.generate_alerts()
        
    def ensure_config_directory(self):
        """Ensure config directory exists"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
    
    def load_dashboard_config(self) -> Dict[str, Any]:
        """Load dashboard configuration"""
        if os.path.exists(self.dashboard_config_file):
            try:
                with open(self.dashboard_config_file, 'r') as file:
                    return yaml.safe_load(file) or {}
            except Exception as e:
                print(f"Error loading dashboard config: {e}")
                return self.get_default_dashboard_config()
        else:
            default_config = self.get_default_dashboard_config()
            self.save_dashboard_config(default_config)
            return default_config
    
    def get_default_dashboard_config(self) -> Dict[str, Any]:
        """Generate comprehensive default dashboard configuration"""
        return {
            'dashboard_settings': {
                'theme': 'modern_blue',
                'auto_refresh_interval': 30,  # seconds
                'show_animations': True,
                'hardware_integration': True,
                'real_time_sync': True,
                'mobile_responsive': True
            },
            'widgets_config': {
                'attendance_overview': {
                    'enabled': True,
                    'position': {'row': 1, 'col': 1, 'span': 2},
                    'refresh_rate': 15,
                    'show_charts': True
                },
                'performance_metrics': {
                    'enabled': True,
                    'position': {'row': 1, 'col': 3, 'span': 2},
                    'refresh_rate': 60,
                    'include_ai_insights': True
                },
                'leave_requests': {
                    'enabled': True,
                    'position': {'row': 2, 'col': 1, 'span': 1},
                    'show_pending_only': False,
                    'auto_approve_settings': True
                },
                'hardware_status': {
                    'enabled': True,
                    'position': {'row': 2, 'col': 2, 'span': 1},
                    'show_offline_devices': True,
                    'battery_alerts': True
                },
                'real_time_alerts': {
                    'enabled': True,
                    'position': {'row': 2, 'col': 3, 'span': 2},
                    'sound_notifications': True,
                    'priority_filtering': True
                }
            },
            'role_permissions': {
                'admin': ['all_widgets', 'system_config', 'user_management', 'hardware_control'],
                'hr_manager': ['attendance_overview', 'leave_requests', 'employee_directory', 'compliance_status'],
                'department_manager': ['team_performance', 'attendance_overview', 'leave_approvals'],
                'employee': ['personal_dashboard', 'leave_requests', 'attendance_history']
            },
            'algorithms': {
                'attendance_prediction': {
                    'enabled': True,
                    'model_type': 'time_series',
                    'accuracy_threshold': 0.85
                },
                'performance_analysis': {
                    'enabled': True,
                    'factors': ['attendance', 'productivity', 'collaboration', 'goals'],
                    'update_frequency': 'daily'
                },
                'anomaly_detection': {
                    'enabled': True,
                    'sensitivity': 'medium',
                    'alert_threshold': 0.7
                },
                'leave_optimization': {
                    'enabled': True,
                    'consider_workload': True,
                    'team_coverage_required': 0.75
                }
            }
        }
    
    def load_hardware_devices(self) -> Dict[str, HardwareDevice]:
        """Load hardware device configurations"""
        if os.path.exists(self.hardware_config_file):
            try:
                with open(self.hardware_config_file, 'r') as file:
                    data = yaml.safe_load(file) or {}
                    devices = {}
                    for device_id, device_data in data.get('devices', {}).items():
                        devices[device_id] = HardwareDevice(
                            device_id=device_id,
                            device_type=device_data['type'],
                            location=device_data['location'],
                            status=device_data['status'],
                            last_sync=datetime.fromisoformat(device_data['last_sync']),
                            battery_level=device_data.get('battery_level'),
                            connected_employees=device_data.get('connected_employees', [])
                        )
                    return devices
            except Exception as e:
                print(f"Error loading hardware devices: {e}")
                return self.get_default_hardware_devices()
        else:
            default_devices = self.get_default_hardware_devices()
            self.save_hardware_devices(default_devices)
            return default_devices
    
    def get_default_hardware_devices(self) -> Dict[str, HardwareDevice]:
        """Generate default hardware device configuration"""
        current_time = datetime.now()
        return {
            'BIO_001': HardwareDevice(
                device_id='BIO_001',
                device_type='biometric',
                location='Main Entrance',
                status='online',
                last_sync=current_time,
                battery_level=95,
                connected_employees=['SM001', 'SM002', 'SM003']
            ),
            'CARD_002': HardwareDevice(
                device_id='CARD_002',
                device_type='card_reader',
                location='Executive Floor',
                status='online',
                last_sync=current_time - timedelta(minutes=2),
                battery_level=None,
                connected_employees=['SM005']
            ),
            'FACE_003': HardwareDevice(
                device_id='FACE_003',
                device_type='face_recognition',
                location='R&D Lab',
                status='maintenance',
                last_sync=current_time - timedelta(hours=2),
                battery_level=78,
                connected_employees=[]
            ),
            'TEMP_004': HardwareDevice(
                device_id='TEMP_004',
                device_type='temperature_scanner',
                location='Health Check Station',
                status='online',
                last_sync=current_time - timedelta(seconds=30),
                battery_level=88,
                connected_employees=['SM001', 'SM004']
            )
        }
    
    def calculate_metrics(self) -> DashboardMetrics:
        """Calculate comprehensive dashboard metrics using AI algorithms"""
        # Simulate real-time calculation with intelligent algorithms
        current_time = datetime.now()
        
        # Base metrics from employee data
        total_employees = 63
        present_today = random.randint(52, 59)
        absent_today = total_employees - present_today
        on_leave = random.randint(2, 5)
        remote_workers = random.randint(8, 15)
        
        # Advanced algorithm calculations
        late_arrivals = self._calculate_late_arrivals()
        early_departures = self._calculate_early_departures()
        overtime_hours = self._calculate_overtime_trends()
        productivity_score = self._calculate_productivity_score()
        compliance_rate = self._calculate_compliance_rate()
        
        return DashboardMetrics(
            total_employees=total_employees,
            present_today=present_today,
            absent_today=absent_today,
            on_leave=on_leave,
            remote_workers=remote_workers,
            late_arrivals=late_arrivals,
            early_departures=early_departures,
            overtime_hours=overtime_hours,
            productivity_score=productivity_score,
            compliance_rate=compliance_rate
        )
    
    def _calculate_late_arrivals(self) -> int:
        """AI algorithm to predict and calculate late arrivals"""
        # Simulate intelligent late arrival calculation
        base_rate = 0.08  # 8% historical late rate
        weather_factor = random.uniform(0.9, 1.3)  # Weather impact
        traffic_factor = random.uniform(0.95, 1.15)  # Traffic impact
        
        predicted_late = int(63 * base_rate * weather_factor * traffic_factor)
        return max(0, min(predicted_late, 10))
    
    def _calculate_early_departures(self) -> int:
        """Calculate early departures with pattern recognition"""
        # Day of week factor (Friday higher early departure rate)
        day_factor = 1.5 if datetime.now().weekday() == 4 else 1.0
        return int(random.randint(2, 8) * day_factor)
    
    def _calculate_overtime_trends(self) -> float:
        """Calculate overtime hours with trending analysis"""
        # Project deadline factor simulation
        project_pressure = random.uniform(0.8, 1.4)
        base_overtime = 24.5  # Average weekly overtime hours
        return round(base_overtime * project_pressure, 1)
    
    def _calculate_productivity_score(self) -> float:
        """AI-driven productivity score calculation"""
        # Factors: attendance, task completion, collaboration, innovation
        attendance_factor = min(self.current_metrics.present_today / 63, 1.0) if hasattr(self, 'current_metrics') else 0.92
        task_completion = random.uniform(0.85, 0.98)
        collaboration_score = random.uniform(0.80, 0.95)
        
        productivity = (attendance_factor * 0.3 + task_completion * 0.4 + collaboration_score * 0.3) * 100
        return round(productivity, 1)
    
    def _calculate_compliance_rate(self) -> float:
        """Calculate compliance rate across all HR policies"""
        policy_adherence = random.uniform(0.92, 0.99)
        training_completion = random.uniform(0.88, 0.96)
        document_submission = random.uniform(0.90, 0.98)
        
        compliance = (policy_adherence * 0.4 + training_completion * 0.3 + document_submission * 0.3) * 100
        return round(compliance, 1)
    
    def generate_alerts(self) -> List[Dict[str, Any]]:
        """Generate real-time intelligent alerts"""
        alerts = []
        current_time = datetime.now()
        
        # Hardware alerts
        for device_id, device in self.hardware_devices.items():
            if device.status == 'offline':
                alerts.append({
                    'type': 'hardware',
                    'severity': 'high',
                    'title': f'Device Offline: {device_id}',
                    'message': f'{device.device_type.title()} at {device.location} is offline',
                    'timestamp': current_time,
                    'action_required': True,
                    'icon': '🔴'
                })
            elif device.battery_level and device.battery_level < 20:
                alerts.append({
                    'type': 'hardware',
                    'severity': 'medium',
                    'title': f'Low Battery: {device_id}',
                    'message': f'Battery level at {device.battery_level}%',
                    'timestamp': current_time,
                    'action_required': True,
                    'icon': '🔋'
                })
        
        # Attendance alerts
        if self.current_metrics.late_arrivals > 5:
            alerts.append({
                'type': 'attendance',
                'severity': 'medium',
                'title': 'High Late Arrivals',
                'message': f'{self.current_metrics.late_arrivals} employees arrived late today',
                'timestamp': current_time,
                'action_required': False,
                'icon': '⏰'
            })
        
        # Compliance alerts
        if self.current_metrics.compliance_rate < 95:
            alerts.append({
                'type': 'compliance',
                'severity': 'high',
                'title': 'Compliance Rate Below Target',
                'message': f'Current compliance rate: {self.current_metrics.compliance_rate}%',
                'timestamp': current_time,
                'action_required': True,
                'icon': '⚠️'
            })
        
        # Performance alerts
        if self.current_metrics.productivity_score < 85:
            alerts.append({
                'type': 'performance',
                'severity': 'low',
                'title': 'Productivity Below Average',
                'message': 'Consider team motivation initiatives',
                'timestamp': current_time,
                'action_required': False,
                'icon': '📊'
            })
        
        return sorted(alerts, key=lambda x: x['timestamp'], reverse=True)
    
    def load_user_preferences(self) -> Dict[str, Any]:
        """Load user dashboard preferences"""
        if os.path.exists(self.user_preferences_file):
            try:
                with open(self.user_preferences_file, 'r') as file:
                    return yaml.safe_load(file) or {}
            except Exception as e:
                print(f"Error loading user preferences: {e}")
                return {}
        return {}
    
    def save_dashboard_config(self, config: Dict[str, Any]) -> bool:
        """Save dashboard configuration"""
        try:
            with open(self.dashboard_config_file, 'w') as file:
                yaml.dump(config, file, default_flow_style=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving dashboard config: {e}")
            return False
    
    def save_hardware_devices(self, devices: Dict[str, HardwareDevice]) -> bool:
        """Save hardware device configurations"""
        try:
            data = {'devices': {}}
            for device_id, device in devices.items():
                data['devices'][device_id] = {
                    'type': device.device_type,
                    'location': device.location,
                    'status': device.status,
                    'last_sync': device.last_sync.isoformat(),
                    'battery_level': device.battery_level,
                    'connected_employees': device.connected_employees
                }
            
            with open(self.hardware_config_file, 'w') as file:
                yaml.dump(data, file, default_flow_style=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving hardware devices: {e}")
            return False

def create_main_dashboard(user_role: UserRole = UserRole.ADMIN):
    """Create comprehensive modern HR dashboard"""
    manager = HRDashboardManager()
    
    with ui.column().classes('w-full h-full bg-gradient-to-br from-slate-50 to-blue-50 min-h-screen'):
        # Top Navigation Bar
        create_dashboard_header(manager, user_role)
        
        # Main Dashboard Grid
        with ui.row().classes('w-full px-6 gap-6'):
            # Left Sidebar - Quick Actions & Navigation
            with ui.column().classes('w-1/4'):
                create_dashboard_sidebar(manager, user_role)
            
            # Main Content Area - Widgets Grid
            with ui.column().classes('w-3/4'):
                create_dashboard_widgets(manager, user_role)
        
        # Footer with Hardware Status
        create_dashboard_footer(manager)

def create_dashboard_header(manager: HRDashboardManager, user_role: UserRole):
    """Create comprehensive dashboard header"""
    with ui.row().classes('w-full p-4 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 text-white shadow-lg'):
        with ui.row().classes('w-full justify-between items-center'):
            # Left - Logo & Title
            with ui.row().classes('items-center gap-4'):
                ui.html('<div class="text-4xl">🏢</div>', sanitize=False)
                with ui.column().classes('gap-1'):
                    ui.html('<h1 class="text-2xl font-bold">Enterprise HR Dashboard</h1>', sanitize=False)
                    ui.html(f'<div class="text-sm opacity-90">Welcome, {user_role.value.replace("_", " ").title()}</div>', sanitize=False)
            
            # Center - Real-time Clock & Date
            with ui.column().classes('items-center gap-1'):
                current_time = datetime.now()
                ui.html(f'<div class="text-lg font-mono">{current_time.strftime("%H:%M:%S")}</div>', sanitize=False)
                ui.html(f'<div class="text-sm opacity-90">{current_time.strftime("%A, %B %d, %Y")}</div>', sanitize=False)
            
            # Right - Quick Actions & Settings
            with ui.row().classes('items-center gap-3'):
                # Hardware sync status
                hardware_online = sum(1 for device in manager.hardware_devices.values() if device.status == 'online')
                total_hardware = len(manager.hardware_devices)
                ui.button(
                    f'🔧 Hardware ({hardware_online}/{total_hardware})',
                    on_click=lambda: create_hardware_management_modal(manager)
                ).classes('bg-white bg-opacity-20 text-white border-white border hover:bg-opacity-30')
                
                # Alerts indicator
                alert_count = len(manager.alerts)
                ui.button(
                    f'🔔 Alerts ({alert_count})',
                    on_click=lambda: create_alerts_modal(manager)
                ).classes('bg-white bg-opacity-20 text-white border-white border hover:bg-opacity-30')
                
                # Settings
                ui.button(
                    '⚙️ Settings',
                    on_click=lambda: create_settings_modal(manager)
                ).classes('bg-white bg-opacity-20 text-white border-white border hover:bg-opacity-30')
                
                # Profile
                ui.button(
                    '👤 Profile',
                    on_click=lambda: ui.notify('Profile settings opened')
                ).classes('bg-white bg-opacity-20 text-white border-white border hover:bg-opacity-30')

def create_dashboard_sidebar(manager: HRDashboardManager, user_role: UserRole):
    """Create dashboard sidebar with navigation and quick actions"""
    # Quick Stats Card
    with ui.card().classes('w-full mb-4'):
        with ui.card_section().classes('p-4'):
            ui.html('<h3 class="text-lg font-semibold text-gray-800 mb-3">📊 Quick Overview</h3>', sanitize=False)
            
            metrics = manager.current_metrics
            quick_stats = [
                {'label': 'Present Today', 'value': metrics.present_today, 'icon': '✅', 'color': 'green'},
                {'label': 'Remote Workers', 'value': metrics.remote_workers, 'icon': '🏠', 'color': 'purple'},
                {'label': 'On Leave', 'value': metrics.on_leave, 'icon': '🏖️', 'color': 'blue'},
                {'label': 'Productivity', 'value': f'{metrics.productivity_score}%', 'icon': '📈', 'color': 'indigo'},
            ]
            
            for stat in quick_stats:
                with ui.row().classes('w-full items-center justify-between py-2 border-b border-gray-100 last:border-0'):
                    with ui.row().classes('items-center gap-2'):
                        ui.html(f'<span class="text-lg">{stat["icon"]}</span>', sanitize=False)
                        ui.html(f'<span class="text-sm text-gray-600">{stat["label"]}</span>', sanitize=False)
                    ui.html(f'<span class="font-semibold text-{stat["color"]}-600">{stat["value"]}</span>', sanitize=False)
    
    # Quick Actions Card
    with ui.card().classes('w-full mb-4'):
        with ui.card_section().classes('p-4'):
            ui.html('<h3 class="text-lg font-semibold text-gray-800 mb-3">⚡ Quick Actions</h3>', sanitize=False)
            
            quick_actions = [
                {'label': 'Clock In/Out', 'icon': '🕐', 'action': lambda: ui.notify('Opening clock interface...'), 'color': 'blue'},
                {'label': 'Leave Request', 'icon': '📝', 'action': lambda: ui.notify('Opening leave request...'), 'color': 'green'},
                {'label': 'View Payroll', 'icon': '💰', 'action': lambda: ui.notify('Opening payroll...'), 'color': 'yellow'},
                {'label': 'Team Schedule', 'icon': '📅', 'action': lambda: ui.notify('Opening schedule...'), 'color': 'purple'},
                {'label': 'Reports', 'icon': '📊', 'action': lambda: ui.notify('Opening reports...'), 'color': 'indigo'},
                {'label': 'Emergency', 'icon': '🚨', 'action': lambda: ui.notify('Emergency protocol activated!'), 'color': 'red'},
            ]
            
            for action in quick_actions:
                ui.button(
                    f"{action['icon']} {action['label']}",
                    on_click=action['action']
                ).classes(f'w-full justify-start mb-2 p-3 bg-{action["color"]}-50 text-{action["color"]}-700 hover:bg-{action["color"]}-100 border border-{action["color"]}-200')
    
    # Hardware Status Mini Panel
    with ui.card().classes('w-full'):
        with ui.card_section().classes('p-4'):
            ui.html('<h3 class="text-lg font-semibold text-gray-800 mb-3">🔧 Hardware Status</h3>', sanitize=False)
            
            for device_id, device in manager.hardware_devices.items():
                status_color = 'green' if device.status == 'online' else 'red' if device.status == 'offline' else 'yellow'
                status_icon = '🟢' if device.status == 'online' else '🔴' if device.status == 'offline' else '🟡'
                
                with ui.row().classes('w-full items-center justify-between py-1'):
                    with ui.column().classes('flex-1'):
                        ui.html(f'<div class="text-sm font-medium">{device.device_type.title()}</div>', sanitize=False)
                        ui.html(f'<div class="text-xs text-gray-500">{device.location}</div>', sanitize=False)
                    ui.html(f'<span class="text-sm">{status_icon}</span>', sanitize=False)

def create_dashboard_widgets(manager: HRDashboardManager, user_role: UserRole):
    """Create main dashboard widget grid"""
    
    # Top Row - Primary Metrics
    with ui.row().classes('w-full gap-4 mb-6'):
        create_attendance_overview_widget(manager)
        create_performance_metrics_widget(manager)
    
    # Middle Row - Secondary Widgets
    with ui.row().classes('w-full gap-4 mb-6'):
        create_leave_requests_widget(manager)
        create_hardware_monitoring_widget(manager)
        create_real_time_alerts_widget(manager)
    
    # Bottom Row - Analytics & Reports
    with ui.row().classes('w-full gap-4'):
        create_analytics_widget(manager)
        create_compliance_widget(manager)

def create_attendance_overview_widget(manager: HRDashboardManager):
    """Attendance overview with AI predictions"""
    with ui.card().classes('flex-1 hover:shadow-lg transition-shadow'):
        with ui.card_section().classes('p-6'):
            ui.html('<h3 class="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2"><span class="text-2xl">📊</span>Attendance Overview</h3>', sanitize=False)
            
            metrics = manager.current_metrics
            
            # Main attendance stats
            with ui.row().classes('w-full gap-4 mb-4'):
                with ui.column().classes('flex-1 text-center'):
                    ui.html(f'<div class="text-3xl font-bold text-green-600">{metrics.present_today}</div>', sanitize=False)
                    ui.html('<div class="text-sm text-gray-600">Present Today</div>', sanitize=False)
                
                with ui.column().classes('flex-1 text-center'):
                    ui.html(f'<div class="text-3xl font-bold text-red-600">{metrics.absent_today}</div>', sanitize=False)
                    ui.html('<div class="text-sm text-gray-600">Absent</div>', sanitize=False)
                
                with ui.column().classes('flex-1 text-center'):
                    ui.html(f'<div class="text-3xl font-bold text-yellow-600">{metrics.late_arrivals}</div>', sanitize=False)
                    ui.html('<div class="text-sm text-gray-600">Late Arrivals</div>', sanitize=False)
            
            # Attendance rate progress bar
            attendance_rate = (metrics.present_today / metrics.total_employees) * 100
            ui.html(f'<div class="w-full bg-gray-200 rounded-full h-3 mb-2"><div class="bg-green-500 h-3 rounded-full transition-all duration-500" style="width: {attendance_rate}%"></div></div>', sanitize=False)
            ui.html(f'<div class="text-center text-sm text-gray-600">Attendance Rate: {attendance_rate:.1f}%</div>', sanitize=False)
            
            # AI Prediction
            predicted_tomorrow = random.randint(50, 60)
            ui.html(f'<div class="mt-3 p-3 bg-blue-50 rounded-lg border border-blue-200"><div class="text-sm text-blue-800"><strong>🤖 AI Prediction:</strong> Tomorrow\'s expected attendance: {predicted_tomorrow} employees</div></div>', sanitize=False)

def create_performance_metrics_widget(manager: HRDashboardManager):
    """Performance metrics with intelligent analysis"""
    with ui.card().classes('flex-1 hover:shadow-lg transition-shadow'):
        with ui.card_section().classes('p-6'):
            ui.html('<h3 class="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2"><span class="text-2xl">🎯</span>Performance Metrics</h3>', sanitize=False)
            
            metrics = manager.current_metrics
            
            # Performance indicators
            performance_metrics = [
                {'label': 'Productivity Score', 'value': metrics.productivity_score, 'target': 90, 'unit': '%', 'color': 'blue'},
                {'label': 'Compliance Rate', 'value': metrics.compliance_rate, 'target': 95, 'unit': '%', 'color': 'green'},
                {'label': 'Overtime Hours', 'value': metrics.overtime_hours, 'target': 20, 'unit': 'h', 'color': 'yellow'},
            ]
            
            for metric in performance_metrics:
                with ui.row().classes('w-full items-center justify-between mb-3'):
                    ui.html(f'<span class="text-sm text-gray-600">{metric["label"]}</span>', sanitize=False)
                    ui.html(f'<span class="font-semibold text-{metric["color"]}-600">{metric["value"]}{metric["unit"]}</span>', sanitize=False)
                
                # Progress bar
                progress = min((metric["value"] / metric["target"]) * 100, 100)
                bar_color = metric["color"] if progress >= 80 else "red"
                ui.html(f'<div class="w-full bg-gray-200 rounded-full h-2 mb-3"><div class="bg-{bar_color}-500 h-2 rounded-full transition-all duration-500" style="width: {progress}%"></div></div>', sanitize=False)
            
            # Trend analysis
            ui.html('<div class="mt-4 p-3 bg-purple-50 rounded-lg border border-purple-200"><div class="text-sm text-purple-800"><strong>📈 Trend Analysis:</strong> Performance improving by 2.3% this week</div></div>', sanitize=False)

def create_leave_requests_widget(manager: HRDashboardManager):
    """Leave requests management"""
    with ui.card().classes('flex-1 hover:shadow-lg transition-shadow'):
        with ui.card_section().classes('p-6'):
            ui.html('<h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2"><span class="text-xl">📝</span>Leave Requests</h3>', sanitize=False)
            
            # Sample leave requests
            leave_requests = [
                {'employee': 'John Smith', 'type': 'Vacation', 'days': 5, 'status': 'pending', 'urgent': False},
                {'employee': 'Sarah Johnson', 'type': 'Sick Leave', 'days': 2, 'status': 'approved', 'urgent': True},
                {'employee': 'Mike Davis', 'type': 'Personal', 'days': 1, 'status': 'pending', 'urgent': False},
            ]
            
            for request in leave_requests:
                status_color = 'green' if request['status'] == 'approved' else 'yellow' if request['status'] == 'pending' else 'red'
                urgent_indicator = '🔴' if request['urgent'] else ''
                
                with ui.row().classes('w-full items-center justify-between p-2 border-b border-gray-100 hover:bg-gray-50'):
                    with ui.column().classes('flex-1'):
                        ui.html(f'<div class="text-sm font-medium">{urgent_indicator} {request["employee"]}</div>', sanitize=False)
                        ui.html(f'<div class="text-xs text-gray-500">{request["type"]} - {request["days"]} days</div>', sanitize=False)
                    ui.html(f'<span class="px-2 py-1 text-xs rounded bg-{status_color}-100 text-{status_color}-800">{request["status"].title()}</span>', sanitize=False)
            
            ui.button('📋 Manage All Requests', on_click=lambda: ui.notify('Opening leave management...')).classes('w-full mt-3 bg-blue-500 text-white')

def create_hardware_monitoring_widget(manager: HRDashboardManager):
    """Hardware monitoring and control"""
    with ui.card().classes('flex-1 hover:shadow-lg transition-shadow'):
        with ui.card_section().classes('p-6'):
            ui.html('<h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2"><span class="text-xl">🔧</span>Hardware Monitor</h3>', sanitize=False)
            
            # Hardware status summary
            online_devices = sum(1 for device in manager.hardware_devices.values() if device.status == 'online')
            total_devices = len(manager.hardware_devices)
            
            ui.html(f'<div class="text-center mb-4"><span class="text-2xl font-bold text-green-600">{online_devices}/{total_devices}</span><div class="text-sm text-gray-600">Devices Online</div></div>', sanitize=False)
            
            # Device list
            for device_id, device in list(manager.hardware_devices.items())[:3]:  # Show first 3 devices
                status_icon = '🟢' if device.status == 'online' else '🔴' if device.status == 'offline' else '🟡'
                battery_info = f' ({device.battery_level}%)' if device.battery_level else ''
                
                with ui.row().classes('w-full items-center justify-between p-2 border-b border-gray-100'):
                    with ui.column().classes('flex-1'):
                        ui.html(f'<div class="text-sm font-medium">{device.device_type.title()}</div>', sanitize=False)
                        ui.html(f'<div class="text-xs text-gray-500">{device.location}{battery_info}</div>', sanitize=False)
                    ui.html(f'<span class="text-lg">{status_icon}</span>', sanitize=False)
            
            ui.button('🔧 Hardware Control Panel', on_click=lambda: create_hardware_management_modal(manager)).classes('w-full mt-3 bg-indigo-500 text-white')

def create_real_time_alerts_widget(manager: HRDashboardManager):
    """Real-time alerts and notifications"""
    with ui.card().classes('flex-1 hover:shadow-lg transition-shadow'):
        with ui.card_section().classes('p-6'):
            ui.html('<h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2"><span class="text-xl">🔔</span>Real-Time Alerts</h3>', sanitize=False)
            
            # Alert summary
            high_alerts = sum(1 for alert in manager.alerts if alert['severity'] == 'high')
            total_alerts = len(manager.alerts)
            
            if total_alerts > 0:
                ui.html(f'<div class="mb-4 p-3 bg-red-50 rounded-lg border border-red-200"><span class="text-red-800 font-semibold">⚠️ {high_alerts} high priority alerts of {total_alerts} total</span></div>', sanitize=False)
                
                # Show recent alerts
                for alert in manager.alerts[:3]:  # Show first 3 alerts
                    severity_color = 'red' if alert['severity'] == 'high' else 'yellow' if alert['severity'] == 'medium' else 'blue'
                    
                    with ui.row().classes('w-full p-2 border-b border-gray-100 hover:bg-gray-50'):
                        ui.html(f'<span class="text-lg mr-2">{alert["icon"]}</span>', sanitize=False)
                        with ui.column().classes('flex-1'):
                            ui.html(f'<div class="text-sm font-medium text-{severity_color}-800">{alert["title"]}</div>', sanitize=False)
                            ui.html(f'<div class="text-xs text-gray-500">{alert["message"]}</div>', sanitize=False)
                
                ui.button('🔔 View All Alerts', on_click=lambda: create_alerts_modal(manager)).classes('w-full mt-3 bg-red-500 text-white')
            else:
                ui.html('<div class="text-center py-8 text-gray-500"><div class="text-4xl mb-2">✅</div><div>All systems normal</div></div>', sanitize=False)

def create_analytics_widget(manager: HRDashboardManager):
    """Analytics and insights widget"""
    with ui.card().classes('flex-1 hover:shadow-lg transition-shadow'):
        with ui.card_section().classes('p-6'):
            ui.html('<h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2"><span class="text-xl">📈</span>Analytics & Insights</h3>', sanitize=False)
            
            # Key insights
            insights = [
                {'title': 'Peak Hours', 'value': '9:00 - 11:00 AM', 'icon': '⏰', 'trend': '+5%'},
                {'title': 'Top Department', 'value': 'Engineering', 'icon': '🏆', 'trend': '92% attendance'},
                {'title': 'Remote Work Trend', 'value': '↗️ Increasing', 'icon': '🏠', 'trend': '+12% this month'},
            ]
            
            for insight in insights:
                with ui.row().classes('w-full items-center p-3 bg-gray-50 rounded-lg mb-2'):
                    ui.html(f'<span class="text-2xl mr-3">{insight["icon"]}</span>', sanitize=False)
                    with ui.column().classes('flex-1'):
                        ui.html(f'<div class="font-medium text-gray-800">{insight["title"]}</div>', sanitize=False)
                        ui.html(f'<div class="text-sm text-gray-600">{insight["value"]}</div>', sanitize=False)
                    ui.html(f'<span class="text-xs text-green-600 font-medium">{insight["trend"]}</span>', sanitize=False)
            
            ui.button('📊 Full Analytics Dashboard', on_click=lambda: ui.notify('Opening analytics...')).classes('w-full mt-3 bg-purple-500 text-white')

def create_compliance_widget(manager: HRDashboardManager):
    """Compliance monitoring widget"""
    with ui.card().classes('flex-1 hover:shadow-lg transition-shadow'):
        with ui.card_section().classes('p-6'):
            ui.html('<h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2"><span class="text-xl">✅</span>Compliance Status</h3>', sanitize=False)
            
            metrics = manager.current_metrics
            
            # Compliance score
            ui.html(f'<div class="text-center mb-4"><span class="text-3xl font-bold text-green-600">{metrics.compliance_rate}%</span><div class="text-sm text-gray-600">Overall Compliance</div></div>', sanitize=False)
            
            # Compliance areas
            compliance_areas = [
                {'area': 'Safety Training', 'score': 98, 'status': 'excellent'},
                {'area': 'Document Submission', 'score': 94, 'status': 'good'},
                {'area': 'Policy Adherence', 'score': 89, 'status': 'needs_attention'},
            ]
            
            for area in compliance_areas:
                status_color = 'green' if area['status'] == 'excellent' else 'yellow' if area['status'] == 'good' else 'red'
                status_icon = '✅' if area['status'] == 'excellent' else '⚠️' if area['status'] == 'good' else '❌'
                
                with ui.row().classes('w-full items-center justify-between p-2 border-b border-gray-100'):
                    with ui.column().classes('flex-1'):
                        ui.html(f'<div class="text-sm font-medium">{area["area"]}</div>', sanitize=False)
                        ui.html(f'<div class="text-xs text-gray-500">{area["score"]}% compliant</div>', sanitize=False)
                    ui.html(f'<span class="text-lg">{status_icon}</span>', sanitize=False)
            
            ui.button('📋 Compliance Reports', on_click=lambda: ui.notify('Opening compliance reports...')).classes('w-full mt-3 bg-green-500 text-white')

def create_dashboard_footer(manager: HRDashboardManager):
    """Create dashboard footer with system info"""
    with ui.row().classes('w-full p-4 bg-gray-100 border-t border-gray-200 mt-6'):
        with ui.row().classes('w-full justify-between items-center'):
            # System status
            ui.html('<div class="text-sm text-gray-600">🟢 System Status: All services operational</div>', sanitize=False)
            
            # Last sync info
            last_sync = datetime.now() - timedelta(seconds=30)
            ui.html(f'<div class="text-sm text-gray-600">Last sync: {last_sync.strftime("%H:%M:%S")}</div>', sanitize=False)
            
            # Version info
            ui.html('<div class="text-sm text-gray-600">HR-Kit v2.1.0 | Enterprise Edition</div>', sanitize=False)

def create_hardware_management_modal(manager: HRDashboardManager):
    """Create hardware management modal"""
    with ui.dialog().classes('w-full max-w-4xl') as dialog:
        with ui.card().classes('w-full'):
            with ui.card_section().classes('p-6'):
                ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2"><span class="text-3xl">🔧</span>Hardware Management Console</h2>', sanitize=False)
                
                # Hardware overview
                with ui.row().classes('w-full gap-4 mb-6'):
                    online_count = sum(1 for device in manager.hardware_devices.values() if device.status == 'online')
                    offline_count = sum(1 for device in manager.hardware_devices.values() if device.status == 'offline')
                    maintenance_count = sum(1 for device in manager.hardware_devices.values() if device.status == 'maintenance')
                    
                    with ui.card().classes('flex-1 bg-green-50'):
                        with ui.card_section().classes('p-4 text-center'):
                            ui.html(f'<div class="text-2xl font-bold text-green-600">{online_count}</div>', sanitize=False)
                            ui.html('<div class="text-sm text-green-800">Online</div>', sanitize=False)
                    
                    with ui.card().classes('flex-1 bg-red-50'):
                        with ui.card_section().classes('p-4 text-center'):
                            ui.html(f'<div class="text-2xl font-bold text-red-600">{offline_count}</div>', sanitize=False)
                            ui.html('<div class="text-sm text-red-800">Offline</div>', sanitize=False)
                    
                    with ui.card().classes('flex-1 bg-yellow-50'):
                        with ui.card_section().classes('p-4 text-center'):
                            ui.html(f'<div class="text-2xl font-bold text-yellow-600">{maintenance_count}</div>', sanitize=False)
                            ui.html('<div class="text-sm text-yellow-800">Maintenance</div>', sanitize=False)
                
                # Device management table
                ui.html('<h3 class="text-lg font-semibold text-gray-800 mb-4">Device Management</h3>', sanitize=False)
                
                with ui.element('div').classes('overflow-x-auto'):
                    with ui.element('table').classes('w-full table-auto border-collapse'):
                        # Header
                        with ui.element('thead'):
                            with ui.element('tr').classes('bg-gray-100'):
                                ui.html('<th class="border p-3 text-left font-semibold">Device ID</th>', sanitize=False)
                                ui.html('<th class="border p-3 text-left font-semibold">Type</th>', sanitize=False)
                                ui.html('<th class="border p-3 text-left font-semibold">Location</th>', sanitize=False)
                                ui.html('<th class="border p-3 text-left font-semibold">Status</th>', sanitize=False)
                                ui.html('<th class="border p-3 text-left font-semibold">Battery</th>', sanitize=False)
                                ui.html('<th class="border p-3 text-left font-semibold">Last Sync</th>', sanitize=False)
                                ui.html('<th class="border p-3 text-left font-semibold">Actions</th>', sanitize=False)
                        
                        # Body
                        with ui.element('tbody'):
                            for device_id, device in manager.hardware_devices.items():
                                with ui.element('tr').classes('hover:bg-gray-50'):
                                    ui.html(f'<td class="border p-3 font-mono">{device_id}</td>', sanitize=False)
                                    ui.html(f'<td class="border p-3">{device.device_type.title()}</td>', sanitize=False)
                                    ui.html(f'<td class="border p-3">{device.location}</td>', sanitize=False)
                                    
                                    # Status with color
                                    status_color = 'green' if device.status == 'online' else 'red' if device.status == 'offline' else 'yellow'
                                    ui.html(f'<td class="border p-3"><span class="px-2 py-1 rounded text-xs bg-{status_color}-100 text-{status_color}-800">{device.status.title()}</span></td>', sanitize=False)
                                    
                                    # Battery
                                    battery_display = f'{device.battery_level}%' if device.battery_level else 'N/A'
                                    battery_color = 'green' if device.battery_level and device.battery_level > 50 else 'yellow' if device.battery_level and device.battery_level > 20 else 'red'
                                    ui.html(f'<td class="border p-3"><span class="text-{battery_color}-600">{battery_display}</span></td>', sanitize=False)
                                    
                                    # Last sync
                                    sync_time = device.last_sync.strftime('%H:%M:%S')
                                    ui.html(f'<td class="border p-3 font-mono text-sm">{sync_time}</td>', sanitize=False)
                                    
                                    # Actions
                                    with ui.element('td').classes('border p-3'):
                                        with ui.row().classes('gap-1'):
                                            ui.button('🔄', on_click=lambda d=device_id: ui.notify(f'Syncing {d}...')).classes('p-1 text-xs bg-blue-100 text-blue-600 hover:bg-blue-200')
                                            ui.button('⚙️', on_click=lambda d=device_id: ui.notify(f'Configuring {d}...')).classes('p-1 text-xs bg-gray-100 text-gray-600 hover:bg-gray-200')
                                            ui.button('🔧', on_click=lambda d=device_id: ui.notify(f'Maintenance mode for {d}')).classes('p-1 text-xs bg-yellow-100 text-yellow-600 hover:bg-yellow-200')
                
                # Action buttons
                with ui.row().classes('w-full gap-4 mt-6'):
                    ui.button('🔄 Sync All Devices', on_click=lambda: ui.notify('Syncing all devices...')).classes('bg-blue-500 text-white')
                    ui.button('➕ Add New Device', on_click=lambda: ui.notify('Opening device registration...')).classes('bg-green-500 text-white')
                    ui.button('📊 Device Reports', on_click=lambda: ui.notify('Opening device reports...')).classes('bg-purple-500 text-white')
                    ui.button('❌ Close', on_click=dialog.close).classes('bg-gray-500 text-white')
    
    dialog.open()

def create_alerts_modal(manager: HRDashboardManager):
    """Create alerts management modal"""
    with ui.dialog().classes('w-full max-w-3xl') as dialog:
        with ui.card().classes('w-full'):
            with ui.card_section().classes('p-6'):
                ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2"><span class="text-3xl">🔔</span>Alert Management Center</h2>', sanitize=False)
                
                # Alert summary
                high_alerts = sum(1 for alert in manager.alerts if alert['severity'] == 'high')
                medium_alerts = sum(1 for alert in manager.alerts if alert['severity'] == 'medium')
                low_alerts = sum(1 for alert in manager.alerts if alert['severity'] == 'low')
                
                with ui.row().classes('w-full gap-4 mb-6'):
                    with ui.card().classes('flex-1 bg-red-50'):
                        with ui.card_section().classes('p-4 text-center'):
                            ui.html(f'<div class="text-2xl font-bold text-red-600">{high_alerts}</div>', sanitize=False)
                            ui.html('<div class="text-sm text-red-800">High Priority</div>', sanitize=False)
                    
                    with ui.card().classes('flex-1 bg-yellow-50'):
                        with ui.card_section().classes('p-4 text-center'):
                            ui.html(f'<div class="text-2xl font-bold text-yellow-600">{medium_alerts}</div>', sanitize=False)
                            ui.html('<div class="text-sm text-yellow-800">Medium Priority</div>', sanitize=False)
                    
                    with ui.card().classes('flex-1 bg-blue-50'):
                        with ui.card_section().classes('p-4 text-center'):
                            ui.html(f'<div class="text-2xl font-bold text-blue-600">{low_alerts}</div>', sanitize=False)
                            ui.html('<div class="text-sm text-blue-800">Low Priority</div>', sanitize=False)
                
                # Alert list
                ui.html('<h3 class="text-lg font-semibold text-gray-800 mb-4">Recent Alerts</h3>', sanitize=False)
                
                for alert in manager.alerts:
                    severity_color = 'red' if alert['severity'] == 'high' else 'yellow' if alert['severity'] == 'medium' else 'blue'
                    
                    with ui.card().classes(f'w-full mb-3 border-l-4 border-{severity_color}-500'):
                        with ui.card_section().classes('p-4'):
                            with ui.row().classes('w-full items-start justify-between'):
                                with ui.row().classes('items-start gap-3'):
                                    ui.html(f'<span class="text-2xl">{alert["icon"]}</span>', sanitize=False)
                                    with ui.column().classes('flex-1'):
                                        ui.html(f'<div class="font-semibold text-{severity_color}-800">{alert["title"]}</div>', sanitize=False)
                                        ui.html(f'<div class="text-sm text-gray-600 mb-2">{alert["message"]}</div>', sanitize=False)
                                        ui.html(f'<div class="text-xs text-gray-500">{alert["timestamp"].strftime("%H:%M:%S")} - {alert["type"].title()}</div>', sanitize=False)
                                
                                with ui.column().classes('gap-2'):
                                    ui.html(f'<span class="px-2 py-1 text-xs rounded bg-{severity_color}-100 text-{severity_color}-800">{alert["severity"].title()}</span>', sanitize=False)
                                    if alert['action_required']:
                                        ui.button('🔧 Take Action', on_click=lambda: ui.notify('Action initiated...')).classes('text-xs bg-blue-500 text-white')
                
                # Action buttons
                with ui.row().classes('w-full gap-4 mt-6'):
                    ui.button('✅ Mark All Read', on_click=lambda: ui.notify('All alerts marked as read')).classes('bg-green-500 text-white')
                    ui.button('🔔 Configure Alerts', on_click=lambda: ui.notify('Opening alert configuration...')).classes('bg-blue-500 text-white')
                    ui.button('❌ Close', on_click=dialog.close).classes('bg-gray-500 text-white')
    
    dialog.open()

def create_settings_modal(manager: HRDashboardManager):
    """Create settings management modal"""
    with ui.dialog().classes('w-full max-w-2xl') as dialog:
        with ui.card().classes('w-full'):
            with ui.card_section().classes('p-6'):
                ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2"><span class="text-3xl">⚙️</span>Dashboard Settings</h2>', sanitize=False)
                
                # Settings sections
                with ui.tabs().classes('w-full') as tabs:
                    ui.tab('general', '🎛️ General')
                    ui.tab('widgets', '📊 Widgets')
                    ui.tab('hardware', '🔧 Hardware')
                    ui.tab('notifications', '🔔 Notifications')
                
                with ui.tab_panels(tabs, value='general').classes('w-full'):
                    with ui.tab_panel('general'):
                        ui.html('<h3 class="text-lg font-semibold mb-4">General Settings</h3>', sanitize=False)
                        
                        with ui.row().classes('w-full gap-4 mb-4'):
                            ui.select(['Light', 'Dark', 'Auto'], label='Theme', value='Light').classes('flex-1')
                            ui.number('Auto Refresh (seconds)', value=30, min=10, max=300).classes('flex-1')
                        
                        ui.checkbox('Enable animations', value=True).classes('mb-2')
                        ui.checkbox('Mobile responsive layout', value=True).classes('mb-2')
                        ui.checkbox('Hardware integration', value=True).classes('mb-2')
                        ui.checkbox('Real-time synchronization', value=True)
                    
                    with ui.tab_panel('widgets'):
                        ui.html('<h3 class="text-lg font-semibold mb-4">Widget Configuration</h3>', sanitize=False)
                        
                        widgets = [
                            'Attendance Overview', 'Performance Metrics', 'Leave Requests',
                            'Hardware Monitor', 'Real-time Alerts', 'Analytics', 'Compliance'
                        ]
                        
                        for widget in widgets:
                            with ui.row().classes('w-full items-center justify-between p-2 border-b border-gray-100'):
                                ui.label(widget)
                                ui.checkbox('Enabled', value=True)
                    
                    with ui.tab_panel('hardware'):
                        ui.html('<h3 class="text-lg font-semibold mb-4">Hardware Settings</h3>', sanitize=False)
                        
                        ui.number('Sync interval (seconds)', value=60, min=30, max=600).classes('w-full mb-4')
                        ui.checkbox('Auto-reconnect offline devices', value=True).classes('mb-2')
                        ui.checkbox('Battery level alerts', value=True).classes('mb-2')
                        ui.checkbox('Device maintenance reminders', value=True)
                    
                    with ui.tab_panel('notifications'):
                        ui.html('<h3 class="text-lg font-semibold mb-4">Notification Settings</h3>', sanitize=False)
                        
                        ui.checkbox('Sound notifications', value=True).classes('mb-2')
                        ui.checkbox('Email alerts for high priority', value=True).classes('mb-2')
                        ui.checkbox('SMS notifications for emergencies', value=False).classes('mb-2')
                        ui.select(['All', 'High Priority Only', 'Critical Only'], label='Alert Level', value='High Priority Only').classes('w-full')
                
                # Action buttons
                with ui.row().classes('w-full gap-4 mt-6'):
                    ui.button('💾 Save Settings', on_click=lambda: [ui.notify('Settings saved successfully!'), dialog.close()]).classes('bg-green-500 text-white')
                    ui.button('🔄 Reset to Defaults', on_click=lambda: ui.notify('Settings reset to defaults')).classes('bg-yellow-500 text-white')
                    ui.button('❌ Cancel', on_click=dialog.close).classes('bg-gray-500 text-white')
    
    dialog.open()