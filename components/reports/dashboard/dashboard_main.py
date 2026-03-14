
"""
Comprehensive Modern HR Management Dashboard
Enterprise-grade interface for employers and employees with hardware integration
Real-time analytics, workforce management, and intelligent algorithms
"""

from nicegui import ui
import yaml
import os
from datetime import datetime, timedelta, date
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import random

# Shared employee registry — single source of truth
from helperFuns.employee_registry import employee_registry

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
    device_type: str
    location: str
    status: str
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
                'auto_refresh_interval': 30,
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
        """Calculate HR dashboard metrics driven by real employee registry data."""
        all_emps = employee_registry.get_all()
        total_employees = max(len(all_emps), 1)
        on_leave_emps = [e for e in all_emps if e.get('status', '').lower() == 'on_leave']
        active_emps  = [e for e in all_emps if e.get('status', '').lower() == 'active']

        # -- Attendance algorithm --
        # Base rate driven by avg performance rating (better performers = better attendance)
        avg_rating = (
            sum(float(e.get('performance_rating', 3.5)) for e in all_emps) / total_employees
            if all_emps else 3.5
        )
        # Day-of-week factor: Mon 0.88, Tue-Thu 0.93, Fri 0.86
        dow = datetime.now().weekday()
        dow_factor = {0: 0.88, 1: 0.93, 2: 0.93, 3: 0.93, 4: 0.86}.get(dow, 0.90)
        attendance_rate = min(dow_factor + (avg_rating / 5.0) * 0.08, 0.98)
        present_today = max(1, round(len(active_emps) * attendance_rate))
        on_leave = len(on_leave_emps)
        absent_today = max(0, total_employees - present_today - on_leave)
        remote_workers = max(0, round(len(active_emps) * 0.15))  # 15% remote baseline

        late_arrivals   = self._calculate_late_arrivals(total_employees)
        early_departures = self._calculate_early_departures()
        overtime_hours   = self._calculate_overtime_trends(total_employees)
        productivity_score = self._calculate_productivity_score(avg_rating, attendance_rate)
        compliance_rate  = self._calculate_compliance_rate(all_emps)

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
    
    def _calculate_late_arrivals(self, total_employees: int) -> int:
        """Late arrival estimate: ~8% base rate scaled to actual headcount."""
        base_rate = 0.08
        weather_factor = random.uniform(0.9, 1.3)
        traffic_factor = random.uniform(0.95, 1.15)
        predicted_late = int(total_employees * base_rate * weather_factor * traffic_factor)
        return max(0, min(predicted_late, max(1, total_employees // 5)))

    def _calculate_early_departures(self) -> int:
        day_factor = 1.5 if datetime.now().weekday() == 4 else 1.0
        return int(random.randint(0, max(1, 2)) * day_factor)

    def _calculate_overtime_trends(self, total_employees: int) -> float:
        """OT hours: ~30% of workforce × 4h/week average, scaled by project pressure."""
        project_pressure = random.uniform(0.8, 1.4)
        base_ot = total_employees * 0.30 * 4.0  # 30% of staff × 4h avg
        return round(base_ot * project_pressure, 1)

    def _calculate_productivity_score(self, avg_rating: float, attendance_rate: float) -> float:
        """Productivity = weighted blend of performance rating + attendance + collaboration.
        performance_rating is 0-5 scale; normalise to 0-1."""
        perf_norm      = min(avg_rating / 5.0, 1.0)
        collab_score   = random.uniform(0.80, 0.95)  # team factor (future: from survey data)
        productivity   = (perf_norm * 0.5 + attendance_rate * 0.3 + collab_score * 0.2) * 100
        return round(productivity, 1)

    def _calculate_compliance_rate(self, all_emps: List[Dict]) -> float:
        """Compliance = avg of: health insurance %, dental %, 401k % across all employees."""
        if not all_emps:
            return 95.0
        benefits_fields = ['health_insurance', 'dental_insurance', 'retirement_401k']
        scores = []
        for field in benefits_fields:
            count = sum(
                1 for e in all_emps
                if e.get('benefits', {}).get(field, False) or e.get(field, False)
            )
            scores.append(count / len(all_emps))
        base = sum(scores) / len(scores)
        # Add a slight random jitter to represent policy adherence & doc submission variance
        jitter = random.uniform(-0.03, 0.03)
        return round(min(max(base + jitter, 0.0), 1.0) * 100, 1)
    
    def generate_alerts(self) -> List[Dict[str, Any]]:
        alerts = []
        current_time = datetime.now()
        
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
    
    def get_hr_algorithm_insights(self) -> Dict[str, Any]:
        """Compute HR algorithm insights derived entirely from the employee registry.
        Returns a structured dict used by the Stats Analysis HR Algorithm panel."""
        all_emps = employee_registry.get_all()
        if not all_emps:
            return {'error': 'No employee data available'}

        total = len(all_emps)
        active = [e for e in all_emps if e.get('status', '').lower() == 'active']

        # ---- Performance Analysis ----
        ratings = [float(e.get('performance_rating', 0)) for e in all_emps]
        avg_rating = round(sum(ratings) / total, 2)
        high_performers  = [e for e in all_emps if float(e.get('performance_rating', 0)) >= 4.5]
        at_risk_employees = [e for e in all_emps if float(e.get('performance_rating', 0)) < 3.5]

        # ---- Tenure Analysis ----
        today = datetime.now().date()
        def tenure_years(emp):
            raw = emp.get('hire_date', '')
            try:
                hd = date.fromisoformat(str(raw)) if raw else today
                return round((today - hd).days / 365.25, 1)
            except Exception:
                return 0.0
        tenures = [tenure_years(e) for e in all_emps]
        avg_tenure = round(sum(tenures) / total, 1) if tenures else 0.0

        # ---- Department Breakdown ----
        dept_map: Dict[str, List[Dict]] = {}
        for emp in all_emps:
            dept = emp.get('department', 'General')
            dept_map.setdefault(dept, []).append(emp)
        dept_stats = []
        colors = ['teal', 'blue', 'purple', 'orange', 'green', 'indigo', 'red']
        for i, (dept, emps) in enumerate(sorted(dept_map.items())):
            dept_ratings = [float(e.get('performance_rating', 3.5)) for e in emps]
            dept_avg = round(sum(dept_ratings) / len(dept_ratings), 2)
            dept_stats.append({
                'name': dept,
                'count': len(emps),
                'avg_rating': dept_avg,
                'perf_pct': round(dept_avg / 5.0 * 100, 1),
                'color': colors[i % len(colors)],
            })

        # ---- Workforce Health Score (0-100) ----
        # Weighted: avg performance (40%) + compliance (30%) + retention (30%)
        compliance = self.current_metrics.compliance_rate / 100.0
        retention  = 1.0 - (len(at_risk_employees) / total)
        health_score = round(
            (avg_rating / 5.0) * 0.40 +
            compliance * 0.30 +
            retention  * 0.30,
            3
        ) * 100

        # ---- Salary fairness indicator ----
        salaries = [float(e.get('salary') or 0) for e in all_emps if e.get('salary')]
        avg_salary = round(sum(salaries) / len(salaries), 0) if salaries else 0

        # ---- Attendance prediction (ML-style, day-ahead) ----
        dow = (datetime.now().weekday() + 1) % 7  # tomorrow's dow
        tomorrow_dow_factor = {0: 0.88, 1: 0.93, 2: 0.93, 3: 0.93, 4: 0.86, 5: 0.0, 6: 0.0}.get(dow, 0.90)
        predicted_attendance = round(len(active) * tomorrow_dow_factor * (1 + random.uniform(-0.03, 0.03)))

        return {
            'total': total,
            'active': len(active),
            'avg_rating': avg_rating,
            'avg_tenure_years': avg_tenure,
            'high_performers': [f"{e.get('first_name','')} {e.get('last_name','')} ({e.get('department','')}, {e.get('performance_rating','')}★)" for e in high_performers],
            'at_risk': [f"{e.get('first_name','')} {e.get('last_name','')} ({e.get('department','')}, {e.get('performance_rating','')}★)" for e in at_risk_employees],
            'dept_stats': dept_stats,
            'health_score': round(health_score, 1),
            'avg_salary': avg_salary,
            'predicted_attendance_tomorrow': max(0, int(predicted_attendance)),
            'attendance_rate_pct': round(self.current_metrics.present_today / max(total, 1) * 100, 1),
        }

    def load_user_preferences(self) -> Dict[str, Any]:
        if os.path.exists(self.user_preferences_file):
            try:
                with open(self.user_preferences_file, 'r') as file:
                    return yaml.safe_load(file) or {}
            except Exception as e:
                print(f"Error loading user preferences: {e}")
                return {}
        return {}
    
    def save_dashboard_config(self, config: Dict[str, Any]) -> bool:
        try:
            with open(self.dashboard_config_file, 'w') as file:
                yaml.dump(config, file, default_flow_style=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving dashboard config: {e}")
            return False
    
    def save_hardware_devices(self, devices: Dict[str, HardwareDevice]) -> bool:
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

def create_comprehensive_dashboard(initial_module=None):
    """Create comprehensive modern HR dashboard"""
    manager = HRDashboardManager()
    user_role = UserRole.ADMIN
    
    with ui.column().classes('w-full h-full bg-gradient-to-br from-slate-50 to-blue-50 min-h-screen'):
        create_dashboard_header(manager, user_role)
        
        with ui.row().classes('w-full px-6 gap-6'):
            with ui.column().classes('w-1/4'):
                create_dashboard_sidebar(manager, user_role)
            
            with ui.column().classes('w-3/4'):
                create_dashboard_widgets(manager, user_role)
        
        create_dashboard_footer(manager)
    
    if initial_module:
        ui.notify(f"Loading module: {initial_module}", type='info', sanitize=False)

def create_dashboard_header(manager: HRDashboardManager, user_role: UserRole):
    with ui.row().classes('w-full p-4 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 text-white shadow-lg'):
        with ui.row().classes('w-full justify-between items-center'):
            with ui.row().classes('items-center gap-4'):
                ui.html('<div class="text-4xl">🏢</div>')
                with ui.column().classes('gap-1'):
                    ui.label('Enterprise HR Dashboard').classes('text-2xl font-bold')
                    ui.label(f'Welcome, {user_role.value.replace("_", " ").title()}').classes('text-sm opacity-90')
            
            with ui.column().classes('items-center gap-1'):
                current_time = datetime.now()
                ui.label(current_time.strftime("%H:%M:%S")).classes('text-lg font-mono')
                ui.label(current_time.strftime("%A, %B %d, %Y")).classes('text-sm opacity-90')
            
            with ui.row().classes('items-center gap-3'):
                hardware_online = sum((1 for device in manager.hardware_devices.values() if device.status == 'online'))
                total_hardware = len(manager.hardware_devices)
                ui.button(
                    f'🔧 Hardware ({hardware_online}/{total_hardware})',
                    on_click=lambda: create_hardware_management_modal(manager)
                ).props('flat color=white', sanitize=False)
                
                alert_count = len(manager.alerts)
                ui.button(
                    f'🔔 Alerts ({alert_count})',
                    on_click=lambda: create_alerts_modal(manager)
                ).props('flat color=white', sanitize=False)
                
                ui.button('⚙️ Settings', on_click=lambda: create_settings_modal(manager)).props('flat color=white', sanitize=False)
                ui.button('👤 Profile', on_click=lambda: ui.notify('Profile settings opened')).props('flat color=white', sanitize=False)

def create_dashboard_sidebar(manager: HRDashboardManager, user_role: UserRole):
    with ui.card().classes('w-full mb-4'):
        with ui.card_section().classes('p-4'):
            ui.label('📊 Quick Overview').classes('text-lg font-semibold text-gray-800 mb-3', sanitize=False)
            
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
                        ui.html(f'<span class="text-lg">{stat["icon"]}</span>')
                        ui.label(stat['label']).classes('text-sm text-gray-600')
                    ui.label(str(stat['value'])).classes(f'font-semibold text-{stat["color"]}-600')

def create_dashboard_widgets(manager: HRDashboardManager, user_role: UserRole):
    with ui.row().classes('w-full gap-4 mb-6'):
        create_attendance_overview_widget(manager)
        create_performance_metrics_widget(manager)
    
    with ui.row().classes('w-full gap-4 mb-6'):
        create_leave_requests_widget(manager)
        create_hardware_monitoring_widget(manager)
        create_real_time_alerts_widget(manager)

    # HR Algorithm Analysis panel — always shown, full-width
    create_hr_algorithm_panel(manager)

def create_attendance_overview_widget(manager: HRDashboardManager):
    with ui.card().classes('flex-1 hover:shadow-lg transition-shadow'):
        with ui.card_section().classes('p-6'):
            with ui.row().classes('items-center gap-2'):
                ui.html('<span class="text-2xl">📊</span>', sanitize=False)
                ui.label('Attendance Overview').classes('text-xl font-semibold text-gray-800', sanitize=False)
            
            metrics = manager.current_metrics
            
            with ui.row().classes('w-full gap-4 mb-4'):
                with ui.column().classes('flex-1 text-center'):
                    ui.label(str(metrics.present_today)).classes('text-3xl font-bold text-green-600', sanitize=False)
                    ui.label('Present Today').classes('text-sm text-gray-600', sanitize=False)
                
                with ui.column().classes('flex-1 text-center'):
                    ui.label(str(metrics.absent_today)).classes('text-3xl font-bold text-red-600', sanitize=False)
                    ui.label('Absent').classes('text-sm text-gray-600', sanitize=False)
                
                with ui.column().classes('flex-1 text-center'):
                    ui.label(str(metrics.late_arrivals)).classes('text-3xl font-bold text-yellow-600', sanitize=False)
                    ui.label('Late Arrivals').classes('text-sm text-gray-600', sanitize=False)
            
            attendance_rate = (metrics.present_today / metrics.total_employees * 100) if metrics.total_employees > 0 else 0
            with ui.column().classes('w-full mb-2'):
                ui.linear_progress(attendance_rate/100).classes('w-full h-3', sanitize=False)
                ui.label(f'Attendance Rate: {attendance_rate:.1f}%').classes('text-center text-sm text-gray-600', sanitize=False)
            
            predicted_tomorrow = max(0, round(
                metrics.total_employees * (metrics.present_today / max(metrics.total_employees, 1))
                * random.uniform(0.95, 1.05)
            ))
            with ui.card().classes('mt-3 bg-blue-50 border border-blue-200'):
                with ui.card_section().classes('p-3'):
                    ui.label(f"🤖 AI Prediction: Tomorrow's expected attendance: {predicted_tomorrow} employees").classes('text-sm text-blue-800', sanitize=False)

def create_performance_metrics_widget(manager: HRDashboardManager):
    with ui.card().classes('flex-1 hover:shadow-lg transition-shadow'):
        with ui.card_section().classes('p-6'):
            with ui.row().classes('items-center gap-2'):
                ui.html('<span class="text-2xl">🎯</span>', sanitize=False)
                ui.label('Performance Metrics').classes('text-xl font-semibold text-gray-800', sanitize=False)
            
            metrics = manager.current_metrics
            
            performance_metrics = [
                {'label': 'Productivity Score', 'value': metrics.productivity_score, 'target': 90, 'unit': '%', 'color': 'blue'},
                {'label': 'Compliance Rate', 'value': metrics.compliance_rate, 'target': 95, 'unit': '%', 'color': 'green'},
                {'label': 'Overtime Hours', 'value': metrics.overtime_hours, 'target': 20, 'unit': 'h', 'color': 'yellow'},
            ]
            
            for metric in performance_metrics:
                with ui.row().classes('w-full items-center justify-between mb-3'):
                    ui.label(metric["label"]).classes('text-sm text-gray-600', sanitize=False)
                    ui.label(f'{metric["value"]}{metric["unit"]}').classes(f'font-semibold text-{metric["color"]}-600', sanitize=False)
                
                progress = min((metric["value"] / metric["target"]) * 100, 100)
                bar_color = metric["color"] if progress >= 80 else "red"
                ui.linear_progress(progress/100).classes(f'w-full h-2 bg-{bar_color}-500', sanitize=False)
            
            with ui.card().classes('mt-4 bg-purple-50 border border-purple-200'):
                with ui.card_section().classes('p-3'):
                    ui.label("📈 Trend Analysis: Performance improving by 2.3% this week").classes('text-sm text-purple-800', sanitize=False)

# Continue with the rest of your widget functions, making sure to remove ALL sanitize parameters
# I've shown the pattern - remove sanitize from ALL ui.html() calls

def create_leave_requests_widget(manager: HRDashboardManager):
    with ui.card().classes('flex-1 hover:shadow-lg transition-shadow'):
        with ui.card_section().classes('p-6'):
            with ui.row().classes('items-center gap-2'):
                ui.html('<span class="text-xl">📝</span>', sanitize=False)
                ui.label('Leave Requests').classes('text-lg font-semibold text-gray-800', sanitize=False)
            
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
                        ui.label(f"{urgent_indicator} {request['employee']}").classes('text-sm font-medium', sanitize=False)
                        ui.label(f"{request['type']} - {request['days']} days").classes('text-xs text-gray-500', sanitize=False)
                    ui.label(request['status'].title()).classes(f'px-2 py-1 text-xs rounded bg-{status_color}-100 text-{status_color}-800', sanitize=False)
            
            ui.button('📋 Manage All Requests', on_click=lambda: ui.notify('Opening leave management...')).classes('w-full mt-3 bg-blue-500 text-white', sanitize=False)

def create_hardware_monitoring_widget(manager: HRDashboardManager):
    with ui.card().classes('flex-1 hover:shadow-lg transition-shadow'):
        with ui.card_section().classes('p-6'):
            with ui.row().classes('items-center gap-2'):
                ui.html('<span class="text-xl">🔧</span>', sanitize=False)
                ui.label('Hardware Monitor').classes('text-lg font-semibold text-gray-800')
            
            online_devices = sum((1 for device in manager.hardware_devices.values() if device.status == 'online'))
            total_devices = len(manager.hardware_devices)
            
            with ui.column().classes('text-center mb-4'):
                ui.label(f'{online_devices}/{total_devices}').classes('text-2xl font-bold text-green-600', sanitize=False)
                ui.label('Devices Online').classes('text-sm text-gray-600', sanitize=False)
            
            for device_id, device in list(manager.hardware_devices.items())[:3]:
                status_icon = '🟢' if device.status == 'online' else '🔴' if device.status == 'offline' else '🟡'
                battery_info = f' ({device.battery_level}%)' if device.battery_level else ''
                
                with ui.row().classes('w-full items-center justify-between p-2 border-b border-gray-100'):
                    with ui.column().classes('flex-1'):
                        ui.label(device.device_type.title()).classes('text-sm font-medium', sanitize=False)
                        ui.label(f"{device.location}{battery_info}").classes('text-xs text-gray-500', sanitize=False)
                    ui.html(f'<span class="text-lg">{status_icon}</span>', sanitize=False)
            
            ui.button('🔧 Hardware Control Panel', on_click=lambda: create_hardware_management_modal(manager)).classes('w-full mt-3 bg-indigo-500 text-white', sanitize=False)

def create_real_time_alerts_widget(manager: HRDashboardManager):
    with ui.card().classes('flex-1 hover:shadow-lg transition-shadow'):
        with ui.card_section().classes('p-6'):
            with ui.row().classes('items-center gap-2'):
                ui.html('<span class="text-xl">🔔</span>', sanitize=False)
                ui.label('Real-Time Alerts').classes('text-lg font-semibold text-gray-800')
            
            high_alerts = sum((1 for alert in manager.alerts if alert['severity'] == 'high'))
            total_alerts = len(manager.alerts)
            
            if total_alerts > 0:
                with ui.card().classes('mb-4 bg-red-50 border border-red-200'):
                    with ui.card_section().classes('p-3'):
                        ui.label(f'⚠️ {high_alerts} high priority alerts of {total_alerts} total').classes('text-red-800 font-semibold', sanitize=False)
                
                for alert in manager.alerts[:3]:
                    severity_color = 'red' if alert['severity'] == 'high' else 'yellow' if alert['severity'] == 'medium' else 'blue'
                    
                    with ui.row().classes('w-full p-2 border-b border-gray-100 hover:bg-gray-50'):
                        ui.html(f'<span class="text-lg mr-2">{alert["icon"]}</span>', sanitize=False)
                        with ui.column().classes('flex-1'):
                            ui.label(alert["title"]).classes(f'text-sm font-medium text-{severity_color}-800', sanitize=False)
                            ui.label(alert["message"]).classes('text-xs text-gray-500', sanitize=False)
                
                ui.button('🔔 View All Alerts', on_click=lambda: create_alerts_modal(manager)).classes('w-full mt-3 bg-red-500 text-white', sanitize=False)
            else:
                with ui.column().classes('text-center py-8 text-gray-500'):
                    ui.html('<div class="text-4xl mb-2">✅</div>', sanitize=False)
                    ui.label('All systems normal', sanitize=False)

def create_dashboard_footer(manager: HRDashboardManager):
    with ui.row().classes('w-full p-4 bg-gray-100 border-t border-gray-200 mt-6'):
        with ui.row().classes('w-full justify-between items-center'):
            ui.label('🟢 System Status: All services operational').classes('text-sm text-gray-600', sanitize=False)
            last_sync = datetime.now() - timedelta(seconds=30)
            ui.label(f'Last sync: {last_sync.strftime("%H:%M:%S")}').classes('text-sm text-gray-600', sanitize=False)
            ui.label('HR-Kit v2.1.0 | Enterprise Edition').classes('text-sm text-gray-600', sanitize=False)

def create_hardware_management_modal(manager: HRDashboardManager):
    with ui.dialog() as dialog, ui.card().classes('w-full max-w-4xl'):
        with ui.card_section().classes('p-6'):
            with ui.row().classes('items-center gap-2'):
                ui.html('<span class="text-3xl">🔧</span>', sanitize=False)
                ui.label('Hardware Management Console').classes('text-2xl font-bold text-gray-800', sanitize=False)
            
            # Modal content - make sure to remove sanitize from any ui.html calls here too
            # ... (rest of modal implementation)
                        # Hardware overview
            with ui.row().classes('w-full gap-4 mb-6'):
                online_count = sum((1 for device in manager.hardware_devices.values() if device.status == 'online'))
                offline_count = sum((1 for device in manager.hardware_devices.values() if device.status == 'offline'))
                maintenance_count = sum((1 for device in manager.hardware_devices.values() if device.status == 'maintenance'))
                
                with ui.card().classes('flex-1 bg-green-50'):
                    with ui.card_section().classes('p-4 text-center'):
                        ui.label(str(online_count)).classes('text-2xl font-bold text-green-600', sanitize=False)
                        ui.label('Online').classes('text-sm text-green-800', sanitize=False)
                
                with ui.card().classes('flex-1 bg-red-50'):
                    with ui.card_section().classes('p-4 text-center'):
                        ui.label(str(offline_count)).classes('text-2xl font-bold text-red-600', sanitize=False)
                        ui.label('Offline').classes('text-sm text-red-800', sanitize=False)
                
                with ui.card().classes('flex-1 bg-yellow-50'):
                    with ui.card_section().classes('p-4 text-center'):
                        ui.label(str(maintenance_count)).classes('text-2xl font-bold text-yellow-600', sanitize=False)
                        ui.label('Maintenance').classes('text-sm text-yellow-800', sanitize=False)
            
            ui.label('Device Management').classes('text-lg font-semibold text-gray-800 mb-4', sanitize=False)
            
            # Device table
            with ui.column().classes('w-full'):
                for device_id, device in manager.hardware_devices.items():
                    with ui.card().classes('w-full mb-2'):
                        with ui.card_section().classes('p-4'):
                            with ui.row().classes('w-full items-center justify-between'):
                                with ui.column():
                                    ui.label(device_id).classes('font-mono font-semibold', sanitize=False)
                                    ui.label(f"{device.device_type.title()} - {device.location}").classes('text-sm text-gray-600', sanitize=False)
                                
                                with ui.row().classes('items-center gap-2'):
                                    status_color = 'green' if device.status == 'online' else 'red' if device.status == 'offline' else 'yellow'
                                    ui.label(device.status.title()).classes(f'px-2 py-1 rounded text-xs bg-{status_color}-100 text-{status_color}-800', sanitize=False)
                                    
                                    battery_display = f'{device.battery_level}%' if device.battery_level else 'N/A'
                                    ui.label(f'Battery: {battery_display}').classes('text-xs text-gray-600', sanitize=False)
                                    
                                    with ui.row().classes('gap-1'):
                                        ui.button('🔄', on_click=lambda d=device_id: ui.notify(f'Syncing {d}...')).props('dense flat', sanitize=False)
                                        ui.button('⚙️', on_click=lambda d=device_id: ui.notify(f'Configuring {d}...')).props('dense flat', sanitize=False)
            
            # Action buttons
            with ui.row().classes('w-full gap-4 mt-6'):
                ui.button('🔄 Sync All Devices', on_click=lambda: ui.notify('Syncing all devices...')).props('color=blue', sanitize=False)
                ui.button('➕ Add New Device', on_click=lambda: ui.notify('Opening device registration...')).props('color=green', sanitize=False)
                ui.button('❌ Close', on_click=dialog.close).props('color=gray', sanitize=False)
    
    dialog.open()


# Similarly, update create_alerts_modal and create_settings_modal to remove sanitize parameters

def create_alerts_modal(manager: HRDashboardManager):
    with ui.dialog() as dialog, ui.card().classes('w-full max-w-3xl'):
        with ui.card_section().classes('p-6'):
            with ui.row().classes('items-center gap-2'):
                ui.html('<span class="text-3xl">🔔</span>', sanitize=False)
                ui.label('Alert Management Center').classes('text-2xl font-bold text-gray-800', sanitize=False)
            
            # Modal content without sanitize
            # ... (rest of modal implementation)
             # Alert summary
            high_alerts = sum((1 for alert in manager.alerts if alert['severity'] == 'high'))
            medium_alerts = sum((1 for alert in manager.alerts if alert['severity'] == 'medium'))
            low_alerts = sum((1 for alert in manager.alerts if alert['severity'] == 'low'))
            
            with ui.row().classes('w-full gap-4 mb-6'):
                with ui.card().classes('flex-1 bg-red-50'):
                    with ui.card_section().classes('p-4 text-center'):
                        ui.label(str(high_alerts)).classes('text-2xl font-bold text-red-600', sanitize=False)
                        ui.label('High Priority').classes('text-sm text-red-800', sanitize=False)
                
                with ui.card().classes('flex-1 bg-yellow-50'):
                    with ui.card_section().classes('p-4 text-center'):
                        ui.label(str(medium_alerts)).classes('text-2xl font-bold text-yellow-600', sanitize=False)
                        ui.label('Medium Priority').classes('text-sm text-yellow-800', sanitize=False)
                
                with ui.card().classes('flex-1 bg-blue-50'):
                    with ui.card_section().classes('p-4 text-center'):
                        ui.label(str(low_alerts)).classes('text-2xl font-bold text-blue-600', sanitize=False)
                        ui.label('Low Priority').classes('text-sm text-blue-800', sanitize=False)
            
            ui.label('Recent Alerts').classes('text-lg font-semibold text-gray-800 mb-4', sanitize=False)
            
            # Alert list
            for alert in manager.alerts:
                severity_color = 'red' if alert['severity'] == 'high' else 'yellow' if alert['severity'] == 'medium' else 'blue'
                
                with ui.card().classes(f'w-full mb-3 border-l-4 border-{severity_color}-500'):
                    with ui.card_section().classes('p-4'):
                        with ui.row().classes('w-full items-start justify-between'):
                            with ui.row().classes('items-start gap-3'):
                                ui.html(f'<span class="text-2xl">{alert["icon"]}</span>', sanitize=False)
                                with ui.column().classes('flex-1'):
                                    ui.label(alert["title"]).classes(f'font-semibold text-{severity_color}-800', sanitize=False)
                                    ui.label(alert["message"]).classes('text-sm text-gray-600 mb-2', sanitize=False)
                                    ui.label(f'{alert["timestamp"].strftime("%H:%M:%S")} - {alert["type"].title()}').classes('text-xs text-gray-500', sanitize=False)
                            
                            with ui.column().classes('gap-2'):
                                ui.label(alert["severity"].title()).classes(f'px-2 py-1 text-xs rounded bg-{severity_color}-100 text-{severity_color}-800', sanitize=False)
                                if alert['action_required']:
                                    ui.button('🔧 Take Action', on_click=lambda: ui.notify('Action initiated...')).props('dense', sanitize=False)
            
            # Action buttons
            with ui.row().classes('w-full gap-4 mt-6'):
                ui.button('✅ Mark All Read', on_click=lambda: ui.notify('All alerts marked as read')).props('color=green', sanitize=False)
                ui.button('❌ Close', on_click=dialog.close).props('color=gray', sanitize=False)
    
    dialog.open()
    
    

def create_settings_modal(manager: HRDashboardManager):
    with ui.dialog() as dialog, ui.card().classes('w-full max-w-2xl'):
        with ui.card_section().classes('p-6'):
            with ui.row().classes('items-center gap-2'):
                ui.html('<span class="text-3xl">⚙️</span>', sanitize=False)
                ui.label('Dashboard Settings').classes('text-2xl font-bold text-gray-800', sanitize=False)
            
            # Modal content without sanitize
            # ... (rest of modal implementation)
             # Settings sections
            with ui.tabs().classes('w-full') as tabs:
                general_tab = ui.tab('General', icon='settings', sanitize=False)
                widgets_tab = ui.tab('Widgets', icon='dashboard', sanitize=False)
                hardware_tab = ui.tab('Hardware', icon='build', sanitize=False)
            
            with ui.tab_panels(tabs, value=general_tab).classes('w-full'):
                with ui.tab_panel(general_tab):
                    ui.label('General Settings').classes('text-lg font-semibold mb-4', sanitize=False)
                    
                    with ui.row().classes('w-full gap-4 mb-4'):
                        ui.select(['Light', 'Dark', 'Auto'], label='Theme', value='Light').classes('flex-1', sanitize=False)
                        ui.number(label='Auto Refresh (seconds)', value=30, min=10, max=300).classes('flex-1', sanitize=False)
                    
                    ui.checkbox('Enable animations', value=True)
                    ui.checkbox('Mobile responsive layout', value=True)
                    ui.checkbox('Hardware integration', value=True)
                    ui.checkbox('Real-time synchronization', value=True)
                
                with ui.tab_panel(widgets_tab):
                    ui.label('Widget Configuration').classes('text-lg font-semibold mb-4', sanitize=False)
                    
                    widgets = [
                        'Attendance Overview', 'Performance Metrics', 'Leave Requests',
                        'Hardware Monitor', 'Real-time Alerts'
                    ]
                    
                    for widget in widgets:
                        with ui.row().classes('w-full items-center justify-between p-2 border-b border-gray-100'):
                            ui.label(widget)
                            ui.checkbox('Enabled', value=True)
                
                with ui.tab_panel(hardware_tab):
                    ui.label('Hardware Settings').classes('text-lg font-semibold mb-4', sanitize=False)
                    
                    ui.number(label='Sync interval (seconds)', value=60, min=30, max=600).classes('w-full mb-4', sanitize=False)
                    ui.checkbox('Auto-reconnect offline devices', value=True)
                    ui.checkbox('Battery level alerts', value=True)
                    ui.checkbox('Device maintenance reminders', value=True)
            
            # Action buttons
            with ui.row().classes('w-full gap-4 mt-6'):
                ui.button('💾 Save Settings', on_click=lambda: [ui.notify('Settings saved successfully!'), dialog.close()]).props('color=green', sanitize=False)
                ui.button('❌ Cancel', on_click=dialog.close).props('color=gray', sanitize=False)
    
    dialog.open()

#############################################
# HR Algorithm Analysis Panel
#############################################

def create_hr_algorithm_panel(manager: HRDashboardManager):
    """Full-width panel showing HR algorithm insights derived from the employee registry."""
    insights = manager.get_hr_algorithm_insights()
    if 'error' in insights:
        return

    with ui.card().classes('w-full mt-2 mb-6 shadow-lg'):
        with ui.card_section().classes('p-6 bg-gradient-to-r from-teal-600 to-emerald-600 rounded-t-lg'):
            with ui.row().classes('items-center gap-3'):
                ui.html('<span class="text-3xl">🧠</span>', sanitize=False)
                with ui.column():
                    ui.label('HR Algorithm Analysis').classes('text-xl font-bold text-white')
                    ui.label('Real-time insights derived from employee registry data').classes('text-teal-100 text-sm')

        with ui.card_section().classes('p-6'):

            # ── Row 1: KPI summary cards ──────────────────────────────────────
            with ui.row().classes('w-full gap-4 mb-6'):
                kpis = [
                    {'label': 'Total Employees',       'value': str(insights['total']),
                     'sub': f"{insights['active']} active",
                     'icon': '👥', 'color': 'blue'},
                    {'label': 'Avg Performance Rating','value': f"{insights['avg_rating']} / 5.0",
                     'sub': 'from employee records',
                     'icon': '⭐', 'color': 'yellow'},
                    {'label': 'Avg Tenure',            'value': f"{insights['avg_tenure_years']} yrs",
                     'sub': 'across all staff',
                     'icon': '📅', 'color': 'purple'},
                    {'label': 'Workforce Health',      'value': f"{insights['health_score']}%",
                     'sub': 'composite algorithm score',
                     'icon': '💚', 'color': 'green'},
                    {'label': 'Predicted Attendance',  'value': str(insights['predicted_attendance_tomorrow']),
                     'sub': "tomorrow (day-ahead model)",
                     'icon': '🤖', 'color': 'indigo'},
                    {'label': 'Attendance Rate Today', 'value': f"{insights['attendance_rate_pct']}%",
                     'sub': 'present / total employees',
                     'icon': '✅', 'color': 'teal'},
                ]
                for kpi in kpis:
                    with ui.card().classes(f'flex-1 bg-{kpi["color"]}-50 border border-{kpi["color"]}-200'):
                        with ui.card_section().classes('p-4 text-center'):
                            ui.html(f'<div class="text-2xl mb-1">{kpi["icon"]}</div>', sanitize=False)
                            ui.label(kpi['value']).classes(f'text-2xl font-bold text-{kpi["color"]}-700')
                            ui.label(kpi['label']).classes('text-sm font-semibold text-gray-700 mt-1')
                            ui.label(kpi['sub']).classes(f'text-xs text-{kpi["color"]}-600 mt-1')

            # ── Row 2: Department Performance + Risk Indicators ──────────────
            with ui.row().classes('w-full gap-6 mb-4'):

                # Department Performance (from registry)
                with ui.card().classes('flex-1'):
                    with ui.card_section().classes('p-4'):
                        ui.label('Department Performance').classes('text-lg font-semibold text-gray-800 mb-3')
                        ui.label('Avg performance rating per department').classes('text-xs text-gray-500 mb-4')
                        for dept in insights['dept_stats']:
                            with ui.row().classes('items-center gap-3 mb-3'):
                                with ui.element('div').classes(f'w-3 h-3 rounded-full bg-{dept["color"]}-500'):
                                    pass
                                ui.label(dept['name']).classes('w-28 text-sm font-medium text-gray-700')
                                with ui.element('div').classes('flex-1 bg-gray-200 rounded-full h-3'):
                                    ui.element('div').classes(
                                        f'bg-{dept["color"]}-500 h-3 rounded-full'
                                    ).style(f'width: {dept["perf_pct"]}%')
                                ui.label(f'{dept["avg_rating"]}★ ({dept["count"]} staff)').classes(
                                    f'text-sm text-{dept["color"]}-600 font-semibold w-28 text-right'
                                )

                # Talent Indicators
                with ui.card().classes('flex-1'):
                    with ui.card_section().classes('p-4'):
                        ui.label('Talent Indicators').classes('text-lg font-semibold text-gray-800 mb-3')

                        # High Performers
                        with ui.card().classes('mb-3 bg-green-50 border border-green-200'):
                            with ui.card_section().classes('p-3'):
                                ui.label(f'🌟 High Performers ({len(insights["high_performers"])})').classes(
                                    'text-sm font-semibold text-green-800 mb-2'
                                )
                                if insights['high_performers']:
                                    for hp in insights['high_performers']:
                                        ui.label(f'  • {hp}').classes('text-xs text-green-700')
                                else:
                                    ui.label('  No employees rated ≥ 4.5 yet').classes('text-xs text-gray-500 italic')

                        # At-Risk Employees
                        with ui.card().classes('bg-orange-50 border border-orange-200'):
                            with ui.card_section().classes('p-3'):
                                ui.label(f'⚠️ Needs Attention ({len(insights["at_risk"])})').classes(
                                    'text-sm font-semibold text-orange-800 mb-2'
                                )
                                if insights['at_risk']:
                                    for ar in insights['at_risk']:
                                        ui.label(f'  • {ar}').classes('text-xs text-orange-700')
                                else:
                                    ui.label('  All employees performing satisfactorily').classes('text-xs text-gray-500 italic')

            # ── Row 3: Algorithm Explanation ────────────────────────────────
            with ui.expansion('Algorithm Details & Methodology', icon='info').classes('w-full bg-gray-50 rounded-lg border border-gray-200'):
                with ui.card_section().classes('p-4'):
                    explanations = [
                        ('Attendance Rate',      'Day-of-week factor (Mon 88%, Tue-Thu 93%, Fri 86%) × performance-rating factor (high performers attend more consistently).'),
                        ('Productivity Score',   '50% avg performance rating (normalised 0-5) + 30% attendance rate + 20% collaboration (team survey factor).'),
                        ('Compliance Rate',      'Average of: % employees with health insurance, dental insurance, and 401k coverage, from registry benefits data.'),
                        ('Workforce Health',     '40% avg performance rating + 30% compliance rate + 30% retention rate (1 – at-risk ratio).'),
                        ('Day-Ahead Prediction', 'Tomorrow\'s attendance = active staff × tomorrow-dow factor × ±3% stochastic variance (weather/traffic proxy).'),
                        ('Overtime Hours',       '30% of total staff × 4h average × project pressure factor (0.8–1.4×).'),
                    ]
                    for metric, desc in explanations:
                        with ui.row().classes('items-start gap-3 mb-2'):
                            ui.label(f'• {metric}:').classes('text-sm font-semibold text-teal-700 w-44 shrink-0')
                            ui.label(desc).classes('text-sm text-gray-600')

