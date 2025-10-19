"""
Modern Timesheet Management System
AI-powered time tracking with predictive analytics, smart scheduling,
and modern UI with real-time collaboration features
"""

from nicegui import ui
import yaml
import os
from datetime import datetime, timedelta, date, time
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import math
from decimal import Decimal, ROUND_HALF_UP
import statistics
import random

class ModernClockEventType(Enum):
    CLOCK_IN = "clock_in"
    CLOCK_OUT = "clock_out"
    BREAK_START = "break_start"
    BREAK_END = "break_end"
    REMOTE_START = "remote_start"
    REMOTE_END = "remote_end"
    MEETING_START = "meeting_start"
    MEETING_END = "meeting_end"

class ModernTimesheetStatus(Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    LOCKED = "locked"
    IN_REVIEW = "in_review"

class SmartPayrollStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    PAID = "paid"
    AUDIT_REQUIRED = "audit_required"

@dataclass
class SmartClockEvent:
    event_id: str
    employee_id: str
    timestamp: datetime
    event_type: ModernClockEventType
    location: str
    device_id: str
    biometric_verified: bool
    ip_address: str
    coordinates: Optional[Tuple[float, float]]
    confidence_score: float = 1.0
    ai_verified: bool = False
    notes: str = ""
    created_by: str = "AI_SYSTEM"
    created_at: str = ""

@dataclass
class ModernTimesheetEntry:
    entry_id: str
    employee_id: str
    date: str
    clock_in: Optional[str]
    clock_out: Optional[str]
    break_duration: float
    lunch_duration: float
    remote_hours: float
    meeting_hours: float
    regular_hours: float
    overtime_hours: float
    total_hours: float
    hourly_rate: float
    regular_pay: float
    overtime_pay: float
    remote_allowance: float
    total_pay: float
    status: ModernTimesheetStatus
    productivity_score: float = 0.0
    ai_insights: List[str] = None
    anomaly_detected: bool = False
    notes: str = ""
    approved_by: Optional[str] = None
    approved_at: Optional[str] = None
    last_modified_by: str = ""
    last_modified_at: str = ""

    def __post_init__(self):
        if self.ai_insights is None:
            self.ai_insights = []

class AITimesheetAnalyzer:
    """AI-powered analyzer for timesheet optimization and insights"""
    
    def __init__(self):
        self.anomaly_threshold = 0.7
    
    def detect_anomalies(self, entry: ModernTimesheetEntry, historical_data: List[ModernTimesheetEntry]) -> Dict[str, Any]:
        """Detect anomalies using statistical analysis and pattern recognition"""
        insights = []
        anomaly_score = 0.0
        
        # Check for excessive hours
        if entry.total_hours > 12:
            insights.append("⚠️ Extended work hours detected (>12 hours)")
            anomaly_score += 0.3
        
        # Check for high overtime
        if entry.overtime_hours > 4:
            insights.append("⚠️ High overtime usage detected")
            anomaly_score += 0.2
        
        # Check for unusual patterns
        if entry.clock_in and entry.clock_out:
            clock_in_time = datetime.strptime(entry.clock_in, '%H:%M').time()
            clock_out_time = datetime.strptime(entry.clock_out, '%H:%M').time()
            
            # Late night/early morning work
            if clock_in_time < time(6, 0) or clock_out_time > time(22, 0):
                insights.append("🌙 Late night/early morning work detected")
                anomaly_score += 0.2
            
            # Very short/long shifts
            if entry.total_hours < 2:
                insights.append("⏱️ Very short shift detected")
                anomaly_score += 0.1
            elif entry.total_hours > 10 and entry.break_duration + entry.lunch_duration < 30:
                insights.append("💡 Consider taking more breaks for productivity")
                anomaly_score += 0.1
        
        # Weekend work analysis
        entry_date = datetime.strptime(entry.date, '%Y-%m-%d')
        if entry_date.weekday() >= 5:
            insights.append("📅 Weekend work detected")
            anomaly_score += 0.1
        
        # Productivity scoring
        if entry.total_hours > 0:
            productivity = min(1.0, (entry.regular_hours / entry.total_hours) * 
                             (1 - (entry.overtime_hours / max(1, entry.total_hours))))
            entry.productivity_score = round(productivity, 2)
            
            if productivity < 0.5:
                insights.append("📊 Lower productivity pattern detected")
                anomaly_score += 0.1
        
        is_anomaly = anomaly_score > self.anomaly_threshold
        
        return {
            "anomaly_detected": is_anomaly,
            "anomaly_score": round(anomaly_score, 2),
            "insights": insights
        }
    
    def predict_optimal_schedule(self, employee_id: str, historical_data: List[ModernTimesheetEntry]) -> Dict[str, Any]:
        """Predict optimal work schedule based on historical patterns"""
        if not historical_data:
            return {
                "optimal_daily_hours": 8.0,
                "optimal_start_time": "09:00",
                "recommended_breaks": "15min morning, 30min lunch, 15min afternoon",
                "productivity_tip": "Maintain consistent work hours for better productivity"
            }
        
        # Analyze work patterns
        productive_entries = [entry for entry in historical_data if entry.productivity_score > 0.7]
        
        if productive_entries:
            # Find most common productive start time
            start_times = []
            for entry in productive_entries:
                if entry.clock_in:
                    start_times.append(datetime.strptime(entry.clock_in, '%H:%M').hour)
            
            optimal_start = statistics.median(start_times) if start_times else 9
        else:
            optimal_start = 9
        
        # Calculate optimal hours based on productivity
        total_hours = [entry.total_hours for entry in historical_data if entry.total_hours <= 10]
        optimal_hours = statistics.median(total_hours) if total_hours else 8.0
        
        tips = [
            "Schedule complex tasks for morning hours when focus is highest",
            "Take regular breaks to maintain productivity throughout the day",
            "Avoid back-to-back meetings to allow for deep work sessions",
            "Consider time blocking for different types of work"
        ]
        
        return {
            "optimal_daily_hours": round(min(8.0, optimal_hours), 2),
            "optimal_start_time": f"{int(optimal_start):02d}:00",
            "recommended_breaks": "15min morning, 30min lunch, 15min afternoon",
            "productivity_tip": random.choice(tips)
        }

class SmartTimesheetCalculator:
    """Advanced calculator with AI-enhanced features"""
    
    def __init__(self):
        self.overtime_threshold = 8.0
        self.overtime_multiplier = 1.5
        self.remote_allowance = 25.0  # Daily remote work allowance
        self.rounding_precision = 0.25
    
    def calculate_smart_hours(self, clock_in: datetime, clock_out: datetime, 
                            break_duration: float = 0, lunch_duration: float = 0,
                            remote_work: bool = False, meeting_hours: float = 0) -> Dict[str, float]:
        """Calculate work hours with smart features"""
        
        total_time = (clock_out - clock_in).total_seconds() / 3600.0
        total_break_time = (break_duration + lunch_duration) / 60.0
        worked_hours = total_time - total_break_time
        
        # Round to precision
        worked_hours = self.round_to_precision(worked_hours)
        
        # Calculate different hour types
        regular_hours = min(worked_hours, self.overtime_threshold)
        overtime_hours = max(0, worked_hours - self.overtime_threshold)
        remote_hours = worked_hours if remote_work else 0.0
        
        return {
            "total_hours": worked_hours,
            "regular_hours": regular_hours,
            "overtime_hours": overtime_hours,
            "remote_hours": remote_hours,
            "meeting_hours": meeting_hours,
            "break_time": total_break_time
        }
    
    def calculate_smart_pay(self, hours_data: Dict[str, float], hourly_rate: float, remote_work: bool = False) -> Dict[str, float]:
        """Calculate pay with smart allowances"""
        regular_pay = hours_data["regular_hours"] * hourly_rate
        overtime_pay = hours_data["overtime_hours"] * hourly_rate * self.overtime_multiplier
        remote_allowance = self.remote_allowance if remote_work and hours_data["remote_hours"] > 4 else 0.0
        total_pay = regular_pay + overtime_pay + remote_allowance
        
        return {
            "regular_pay": round(regular_pay, 2),
            "overtime_pay": round(overtime_pay, 2),
            "remote_allowance": round(remote_allowance, 2),
            "total_pay": round(total_pay, 2)
        }
    
    def round_to_precision(self, hours: float) -> float:
        """Round hours to specified precision"""
        return float(Decimal(str(hours / self.rounding_precision)).quantize(
            Decimal('1'), rounding=ROUND_HALF_UP) * Decimal(str(self.rounding_precision)))

class ModernTimesheetManager:
    """Modern Timesheet Management with AI Features"""
    
    def __init__(self):
        self.config_dir = "config"
        self.timesheets_file = os.path.join(self.config_dir, "modern_timesheets.yaml")
        self.clock_events_file = os.path.join(self.config_dir, "modern_clock_events.yaml")
        self.settings_file = os.path.join(self.config_dir, "modern_timesheet_settings.yaml")
        
        self.ensure_config_directory()
        self.timesheets = self.load_timesheets()
        self.clock_events = self.load_clock_events()
        self.settings = self.load_settings()
        
        self.calculator = SmartTimesheetCalculator()
        self.ai_analyzer = AITimesheetAnalyzer()
    
    def ensure_config_directory(self):
        """Ensure config directory exists"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
    
    def load_timesheets(self) -> Dict[str, ModernTimesheetEntry]:
        """Load modern timesheets"""
        if os.path.exists(self.timesheets_file):
            try:
                with open(self.timesheets_file, 'r') as file:
                    data = yaml.safe_load(file) or {}
                    timesheets = {}
                    for entry_id, entry_data in data.items():
                        entry_data['status'] = ModernTimesheetStatus(entry_data.get('status', 'draft'))
                        if entry_data.get('ai_insights') is None:
                            entry_data['ai_insights'] = []
                        timesheets[entry_id] = ModernTimesheetEntry(**entry_data)
                    return timesheets
            except Exception as e:
                print(f"Error loading modern timesheets: {e}")
                return self.get_sample_timesheets()
        else:
            sample_timesheets = self.get_sample_timesheets()
            self.save_timesheets(sample_timesheets)
            return sample_timesheets
    
    def get_sample_timesheets(self) -> Dict[str, ModernTimesheetEntry]:
        """Generate sample modern timesheet entries"""
        current_time = datetime.now()
        timesheets = {}
        
        for i in range(14):  # 2 weeks of sample data
            date_obj = current_time - timedelta(days=i)
            if date_obj.weekday() < 5:  # Weekdays only
                entry_id = f"MTS_{date_obj.strftime('%Y%m%d')}_EMP001001"
                
                # Varied sample data for realism
                start_hour = 8 + random.randint(0, 1)  # 8-9 AM start
                end_hour = 17 + random.randint(-1, 1)  # 4-6 PM end
                remote_work = random.choice([True, False, False])  # 33% remote
                
                clock_in = datetime.combine(date_obj.date(), time(start_hour, random.choice([0, 15, 30])))
                clock_out = datetime.combine(date_obj.date(), time(end_hour, random.choice([0, 15, 30])))
                
                hours_data = self.calculator.calculate_smart_hours(
                    clock_in, clock_out, 
                    break_duration=random.choice([10, 15, 20]),
                    lunch_duration=random.choice([30, 45, 60]),
                    remote_work=remote_work,
                    meeting_hours=random.uniform(0.5, 3.0)
                )
                
                pay_data = self.calculator.calculate_smart_pay(hours_data, 28.50, remote_work)
                
                # AI analysis
                historical = list(timesheets.values())[-5:] if timesheets else []
                ai_analysis = self.ai_analyzer.detect_anomalies(
                    ModernTimesheetEntry(
                        entry_id=entry_id,
                        employee_id="EMP001001",
                        date=date_obj.strftime('%Y-%m-%d'),
                        clock_in=clock_in.strftime('%H:%M'),
                        clock_out=clock_out.strftime('%H:%M'),
                        break_duration=hours_data.get('break_time', 0) * 60,
                        lunch_duration=0,
                        remote_hours=hours_data["remote_hours"],
                        meeting_hours=hours_data["meeting_hours"],
                        regular_hours=hours_data["regular_hours"],
                        overtime_hours=hours_data["overtime_hours"],
                        total_hours=hours_data["total_hours"],
                        hourly_rate=28.50,
                        regular_pay=pay_data["regular_pay"],
                        overtime_pay=pay_data["overtime_pay"],
                        remote_allowance=pay_data["remote_allowance"],
                        total_pay=pay_data["total_pay"],
                        status=ModernTimesheetStatus.APPROVED
                    ),
                    historical
                )
                
                entry = ModernTimesheetEntry(
                    entry_id=entry_id,
                    employee_id="EMP001001",
                    date=date_obj.strftime('%Y-%m-%d'),
                    clock_in=clock_in.strftime('%H:%M'),
                    clock_out=clock_out.strftime('%H:%M'),
                    break_duration=hours_data.get('break_time', 0) * 60,
                    lunch_duration=0,
                    remote_hours=hours_data["remote_hours"],
                    meeting_hours=hours_data["meeting_hours"],
                    regular_hours=hours_data["regular_hours"],
                    overtime_hours=hours_data["overtime_hours"],
                    total_hours=hours_data["total_hours"],
                    hourly_rate=28.50,
                    regular_pay=pay_data["regular_pay"],
                    overtime_pay=pay_data["overtime_pay"],
                    remote_allowance=pay_data["remote_allowance"],
                    total_pay=pay_data["total_pay"],
                    status=ModernTimesheetStatus.APPROVED,
                    productivity_score=ai_analysis.get('productivity_score', 0.8),
                    ai_insights=ai_analysis.get('insights', []),
                    anomaly_detected=ai_analysis.get('anomaly_detected', False),
                    last_modified_by="AI_SYSTEM",
                    last_modified_at=current_time.isoformat()
                )
                
                timesheets[entry_id] = entry
        
        return timesheets
    
    def save_timesheets(self, timesheets: Dict[str, ModernTimesheetEntry]) -> bool:
        """Save modern timesheets to YAML file"""
        try:
            data = {}
            for entry_id, entry in timesheets.items():
                entry_dict = asdict(entry)
                entry_dict['status'] = entry.status.value
                data[entry_id] = entry_dict
            
            with open(self.timesheets_file, 'w') as file:
                yaml.dump(data, file, default_flow_style=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving modern timesheets: {e}")
            return False
    
    def load_clock_events(self) -> List[SmartClockEvent]:
        """Load modern clock events"""
        if os.path.exists(self.clock_events_file):
            try:
                with open(self.clock_events_file, 'r') as file:
                    data = yaml.safe_load(file) or []
                    events = []
                    for event_data in data:
                        event_data['event_type'] = ModernClockEventType(event_data['event_type'])
                        event_data['timestamp'] = datetime.fromisoformat(event_data['timestamp'])
                        events.append(SmartClockEvent(**event_data))
                    return events
            except Exception as e:
                print(f"Error loading modern clock events: {e}")
                return []
        return []
    
    def load_settings(self) -> Dict[str, Any]:
        """Load modern timesheet settings"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as file:
                    return yaml.safe_load(file) or self.get_default_settings()
            except Exception as e:
                print(f"Error loading settings: {e}")
                return self.get_default_settings()
        else:
            default_settings = self.get_default_settings()
            self.save_settings(default_settings)
            return default_settings

    def get_default_settings(self) -> Dict[str, Any]:
        """Get default modern timesheet settings"""
        return {
            "ai_features": {
                "anomaly_detection": True,
                "productivity_scoring": True,
                "optimal_scheduling": True,
                "predictive_analytics": True
            },
            "work_modes": {
                "remote_work_enabled": True,
                "hybrid_scheduling": True,
                "flexible_hours": True
            },
            "overtime": {
                "daily_threshold": 8.0,
                "weekly_threshold": 40.0,
                "multiplier": 1.5,
                "auto_approval_limit": 2.0
            },
            "notifications": {
                "anomaly_alerts": True,
                "approval_reminders": True,
                "payroll_deadlines": True
            }
        }

    def save_settings(self, settings: Dict[str, Any]) -> bool:
        """Save modern timesheet settings"""
        try:
            with open(self.settings_file, 'w') as file:
                yaml.dump(settings, file, default_flow_style=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False

    def generate_ai_insights_report(self, employee_id: str, days: int = 30) -> Dict[str, Any]:
        """Generate AI-powered insights report for an employee"""
        recent_entries = [
            entry for entry in self.timesheets.values()
            if entry.employee_id == employee_id and 
            (datetime.now() - datetime.strptime(entry.date, '%Y-%m-%d')).days <= days
        ]
        
        if not recent_entries:
            return {"error": "No data available for analysis"}
        
        # Calculate statistics
        total_hours = sum(entry.total_hours for entry in recent_entries)
        avg_hours = total_hours / len(recent_entries)
        overtime_hours = sum(entry.overtime_hours for entry in recent_entries)
        remote_days = sum(1 for entry in recent_entries if entry.remote_hours > 0)
        
        # AI analysis
        optimal_schedule = self.ai_analyzer.predict_optimal_schedule(employee_id, recent_entries)
        
        # Productivity analysis
        productive_days = sum(1 for entry in recent_entries if entry.productivity_score > 0.7)
        productivity_rate = productive_days / len(recent_entries) if recent_entries else 0
        
        # Anomaly detection
        anomalies = sum(1 for entry in recent_entries if entry.anomaly_detected)
        
        return {
            "summary": {
                "period_days": len(recent_entries),
                "total_hours": round(total_hours, 2),
                "average_daily_hours": round(avg_hours, 2),
                "overtime_hours": round(overtime_hours, 2),
                "remote_days": remote_days,
                "productivity_rate": round(productivity_rate, 2),
                "anomalies_detected": anomalies
            },
            "recommendations": optimal_schedule,
            "trends": {
                "work_pattern": "Consistent" if avg_hours >= 7 and avg_hours <= 9 else "Variable",
                "overtime_trend": "High" if overtime_hours > 10 else "Moderate" if overtime_hours > 5 else "Low",
                "remote_adoption": "High" if remote_days / len(recent_entries) > 0.5 else "Moderate"
            }
        }

def create_modern_timesheet_interface():
    """Modern UI for Timesheet Management with advanced HR analytics and interactive table"""
    manager = ModernTimesheetManager()
    timesheets = list(manager.timesheets.values())[-14:]
    analyzer = manager.ai_analyzer
    calculator = manager.calculator
    user_role = 'hr_admin'  # Simulate HR role for demo
    is_hr = user_role in ['hr_admin', 'payroll_admin', 'system_admin']

    # State for row/column selection
    selected_row = {'index': None}
    selected_col = {'name': None}

    def handle_row_click(idx):
        selected_row['index'] = idx
        selected_col['name'] = None
        ui.notify(f"Row {idx+1} selected")

    def handle_col_click(col_name):
        selected_col['name'] = col_name
        selected_row['index'] = None
        ui.notify(f"Column '{col_name}' selected")

    def status_badge(status):
        color_map = {
            'Approved': 'bg-green-500',
            'Pending': 'bg-yellow-500',
            'Rejected': 'bg-red-500',
            'Draft': 'bg-gray-400',
            'Submitted': 'bg-blue-500',
            'Locked': 'bg-purple-500',
            'In Review': 'bg-indigo-500',
        }
        color = color_map.get(status, 'bg-gray-300')
        return f'<span class="px-3 py-1 rounded-full text-white {color}">{status}</span>'

    with ui.column().classes('w-full h-full bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen'):
        with ui.card().classes('w-full max-w-5xl mx-auto mt-10 bg-white shadow-2xl'):
            with ui.card_section().classes('p-8'):
                ui.html('<h1 class="text-3xl font-bold text-blue-700 mb-4 flex items-center gap-3"><span class="text-4xl">⏰</span>Modern Timesheet Management</h1>')
                ui.html('<p class="text-lg text-gray-700 mb-6">AI-powered time tracking, smart scheduling, and advanced analytics for HR. Only authorized HR can edit timesheets.</p>')
                # Analytics cards
                total_hours = sum(e.total_hours for e in timesheets)
                avg_hours = total_hours / len(timesheets) if timesheets else 0
                overtime_hours = sum(e.overtime_hours for e in timesheets)
                remote_days = sum(1 for e in timesheets if e.remote_hours > 0)
                anomalies = sum(1 for e in timesheets if e.anomaly_detected)
                with ui.row().classes('gap-6 mb-8'):
                        with ui.card().classes('flex-1 bg-gradient-to-br from-green-500 to-green-700 text-white p-4'):
                            ui.html(f'<div class="text-lg font-bold">Total Hours</div><div class="text-2xl">{total_hours:.1f}</div>')
                        with ui.card().classes('flex-1 bg-gradient-to-br from-blue-500 to-blue-700 text-white p-4'):
                            ui.html(f'<div class="text-lg font-bold">Avg Daily Hours</div><div class="text-2xl">{avg_hours:.1f}</div>')
                        with ui.card().classes('flex-1 bg-gradient-to-br from-orange-500 to-orange-700 text-white p-4'):
                            ui.html(f'<div class="text-lg font-bold">Overtime</div><div class="text-2xl">{overtime_hours:.1f}</div>')
                        with ui.card().classes('flex-1 bg-gradient-to-br from-purple-500 to-purple-700 text-white p-4'):
                            ui.html(f'<div class="text-lg font-bold">Remote Days</div><div class="text-2xl">{remote_days}</div>')
                        with ui.card().classes('flex-1 bg-gradient-to-br from-red-500 to-red-700 text-white p-4'):
                            ui.html(f'<div class="text-lg font-bold">Anomalies</div><div class="text-2xl">{anomalies}</div>')
                # Timesheet Table with avatars and interactive highlights
                columns = [
                    {'name': 'avatar', 'label': '', 'field': 'avatar'},
                    {'name': 'date', 'label': 'Date', 'field': 'date'},
                    {'name': 'clock_in', 'label': 'Clock In', 'field': 'clock_in'},
                    {'name': 'clock_out', 'label': 'Clock Out', 'field': 'clock_out'},
                    {'name': 'total_hours', 'label': 'Total Hours', 'field': 'total_hours'},
                    {'name': 'overtime_hours', 'label': 'Overtime', 'field': 'overtime_hours'},
                    {'name': 'remote_hours', 'label': 'Remote', 'field': 'remote_hours'},
                    {'name': 'status', 'label': 'Status', 'field': 'status'},
                    {'name': 'ai_insights', 'label': 'AI Insights', 'field': 'ai_insights'},
                    {'name': 'actions', 'label': 'Actions', 'field': 'actions'},
                ]
                rows = []
                for idx, entry in enumerate(timesheets):
                    insights = '<br>'.join(entry.ai_insights) if entry.ai_insights else ''
                    actions = ui.button('Edit', on_click=lambda e=entry: ui.notify('Edit only allowed for HR!'), disabled=not is_hr).classes('bg-blue-500 text-white px-2 py-1 rounded text-xs') if is_hr else ''
                    avatar_html = f'<div class="flex items-center justify-center"><img src="https://ui-avatars.com/api/?name={entry.employee_id}&background=0D8ABC&color=fff&size=32" class="rounded-full border-2 border-blue-400" /></div>'
                    row_style = 'bg-blue-100' if selected_row['index'] == idx else ''
                    rows.append({
                        'avatar': avatar_html,
                        'date': f'<div onclick="window.rowClick{idx}()" class="cursor-pointer {row_style}">{entry.date}</div>',
                        'clock_in': f'<div onclick="window.colClickClockIn{idx}()" class="cursor-pointer">{entry.clock_in}</div>',
                        'clock_out': f'<div onclick="window.colClickClockOut{idx}()" class="cursor-pointer">{entry.clock_out}</div>',
                        'total_hours': f'<div onclick="window.colClickTotalHours{idx}()" class="cursor-pointer">{entry.total_hours}</div>',
                        'overtime_hours': f'<div onclick="window.colClickOvertime{idx}()" class="cursor-pointer">{entry.overtime_hours}</div>',
                        'remote_hours': f'<div onclick="window.colClickRemote{idx}()" class="cursor-pointer">{entry.remote_hours}</div>',
                        'status': status_badge(entry.status.value.title()),
                        'ai_insights': insights,
                        'actions': actions
                    })
                    # Register JS click handlers for row/col highlight
                    ui.run_javascript(f"window.rowClick{idx} = function() {{ window.dispatchEvent(new CustomEvent('rowClick{idx}')); }};")
                    ui.run_javascript(f"window.colClickClockIn{idx} = function() {{ window.dispatchEvent(new CustomEvent('colClickClockIn{idx}')); }};")
                    ui.run_javascript(f"window.colClickClockOut{idx} = function() {{ window.dispatchEvent(new CustomEvent('colClickClockOut{idx}')); }};")
                    ui.run_javascript(f"window.colClickTotalHours{idx} = function() {{ window.dispatchEvent(new CustomEvent('colClickTotalHours{idx}')); }};")
                    ui.run_javascript(f"window.colClickOvertime{idx} = function() {{ window.dispatchEvent(new CustomEvent('colClickOvertime{idx}')); }};")
                    ui.run_javascript(f"window.colClickRemote{idx} = function() {{ window.dispatchEvent(new CustomEvent('colClickRemote{idx}')); }};")
                    ui.on_event(f'rowClick{idx}', lambda e=None, idx=idx: handle_row_click(idx))
                    ui.on_event(f'colClickClockIn{idx}', lambda e=None: handle_col_click('clock_in'))
                    ui.on_event(f'colClickClockOut{idx}', lambda e=None: handle_col_click('clock_out'))
                    ui.on_event(f'colClickTotalHours{idx}', lambda e=None: handle_col_click('total_hours'))
                    ui.on_event(f'colClickOvertime{idx}', lambda e=None: handle_col_click('overtime_hours'))
                    ui.on_event(f'colClickRemote{idx}', lambda e=None: handle_col_click('remote_hours'))
                ui.table(columns=columns, rows=rows).classes('w-full')
                # Trends and charts (simulated)
                ui.html('<div class="w-full h-64 bg-gray-100 rounded-lg flex items-center justify-center text-gray-500 mt-8">[Work Trends Chart]</div>')
                ui.html('<div class="mt-8 text-center text-gray-500 text-sm">Timesheet data is AI-enhanced and synced with clock and database. Editing is restricted to HR roles.</div>')

def create_modern_timesheet_management_page():
    """Main page function for modern timesheet management"""
    create_modern_timesheet_interface()

# Add the modern timesheet page to the frontend routes
def register_modern_timesheet_routes():
    """Register modern timesheet routes in the frontend"""
    # This function should be called from frontend.py to add the modern timesheet page
    pass

# Sample data generation for demonstration
def generate_sample_modern_data():
    """Generate sample modern timesheet data for demonstration"""
    manager = ModernTimesheetManager()
    return manager.get_sample_timesheets()


