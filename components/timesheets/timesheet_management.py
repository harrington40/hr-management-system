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
    total_hours = sum(e.total_hours for e in timesheets)
    avg_hours = total_hours / len(timesheets) if timesheets else 0
    overtime_hours = sum(e.overtime_hours for e in timesheets)
    remote_days = sum(1 for e in timesheets if e.remote_hours > 0)
    anomalies = sum(1 for e in timesheets if e.anomaly_detected)
    
    # Main layout
    with ui.column().classes('w-full bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen p-6'):
        
        # Header
        with ui.card().classes('w-full bg-white shadow-lg'):
            with ui.card_section().classes('p-8'):
                with ui.row().classes('w-full items-center justify-between'):
                    with ui.column().classes('gap-2'):
                        ui.label('⏰ Timesheet Management').classes('text-3xl font-bold text-blue-700')
                        ui.label('AI-powered time tracking and analytics').classes('text-gray-600')
                    
                    if is_hr:
                        ui.button('Export', icon='download').props('flat color=blue')
                        ui.button('Sync', icon='refresh').props('flat color=blue')
        
        # Analytics Cards
        with ui.card().classes('w-full bg-white shadow-lg'):
            with ui.card_section().classes('p-6'):
                with ui.row().classes('gap-4 w-full'):
                    # Total Hours Card
                    with ui.card().classes('flex-1 bg-gradient-to-br from-green-500 to-green-700 text-white shadow-md'):
                        with ui.card_section().classes('p-4 text-center'):
                            ui.label('Total Hours').classes('text-sm opacity-90')
                            ui.label(f'{total_hours:.1f}h').classes('text-3xl font-bold mt-2')
                    
                    # Avg Hours Card
                    with ui.card().classes('flex-1 bg-gradient-to-br from-blue-500 to-blue-700 text-white shadow-md'):
                        with ui.card_section().classes('p-4 text-center'):
                            ui.label('Avg Daily Hours').classes('text-sm opacity-90')
                            ui.label(f'{avg_hours:.1f}h').classes('text-3xl font-bold mt-2')
                    
                    # Overtime Card
                    with ui.card().classes('flex-1 bg-gradient-to-br from-orange-500 to-orange-700 text-white shadow-md'):
                        with ui.card_section().classes('p-4 text-center'):
                            ui.label('Overtime').classes('text-sm opacity-90')
                            ui.label(f'{overtime_hours:.1f}h').classes('text-3xl font-bold mt-2')
                    
                    # Remote Days Card
                    with ui.card().classes('flex-1 bg-gradient-to-br from-purple-500 to-purple-700 text-white shadow-md'):
                        with ui.card_section().classes('p-4 text-center'):
                            ui.label('Remote Days').classes('text-sm opacity-90')
                            ui.label(f'{remote_days}').classes('text-3xl font-bold mt-2')
                    
                    # Anomalies Card
                    with ui.card().classes('flex-1 bg-gradient-to-br from-red-500 to-red-700 text-white shadow-md'):
                        with ui.card_section().classes('p-4 text-center'):
                            ui.label('Anomalies').classes('text-sm opacity-90')
                            ui.label(f'{anomalies}').classes('text-3xl font-bold mt-2')
        
        # Timesheet Table
        with ui.card().classes('w-full bg-white shadow-lg'):
            with ui.card_section().classes('p-6'):
                ui.label('Recent Timesheets').classes('text-xl font-bold mb-4 block')
                
                # Create table rows programmatically
                with ui.element('div').classes('overflow-x-auto'):
                    with ui.element('table').classes('w-full border-collapse'):
                        # Header
                        with ui.element('thead'):
                            with ui.element('tr').classes('bg-gray-100 border-b-2 border-gray-300'):
                                headers = ['Employee', 'Date', 'Clock In', 'Clock Out', 'Total Hrs', 'Overtime', 'Remote', 'Status', 'Actions']
                                for header in headers:
                                    with ui.element('th').classes('p-3 text-left font-semibold text-gray-700'):
                                        ui.label(header)
                        
                        # Body
                        with ui.element('tbody'):
                            for idx, entry in enumerate(timesheets[:10]):  # Limit to 10 for performance
                                row_class = 'bg-red-50' if entry.anomaly_detected else 'hover:bg-gray-50'
                                with ui.element('tr').classes(f'border-b border-gray-200 {row_class}'):
                                    # Employee
                                    with ui.element('td').classes('p-3'):
                                        ui.label(entry.employee_id).classes('font-medium')
                                    
                                    # Date
                                    with ui.element('td').classes('p-3'):
                                        ui.label(entry.date)
                                    
                                    # Clock In
                                    with ui.element('td').classes('p-3'):
                                        ui.label(entry.clock_in)
                                    
                                    # Clock Out
                                    with ui.element('td').classes('p-3'):
                                        ui.label(entry.clock_out)
                                    
                                    # Total Hours
                                    with ui.element('td').classes('p-3'):
                                        ui.label(f'{entry.total_hours:.1f}h').classes('font-bold')
                                    
                                    # Overtime
                                    with ui.element('td').classes('p-3'):
                                        color = 'text-red-600 font-bold' if entry.overtime_hours > 0 else 'text-gray-600'
                                        ui.label(f'{entry.overtime_hours:.1f}h').classes(color)
                                    
                                    # Remote
                                    with ui.element('td').classes('p-3'):
                                        if entry.remote_hours > 0:
                                            ui.label(f'{entry.remote_hours}h').classes('text-blue-600')
                                        else:
                                            ui.label('On-site').classes('text-gray-600')
                                    
                                    # Status
                                    with ui.element('td').classes('p-3'):
                                        status_colors = {
                                            'approved': 'bg-green-100 text-green-800',
                                            'pending': 'bg-yellow-100 text-yellow-800',
                                            'rejected': 'bg-red-100 text-red-800',
                                            'draft': 'bg-gray-100 text-gray-800',
                                            'submitted': 'bg-blue-100 text-blue-800',
                                            'in_review': 'bg-indigo-100 text-indigo-800',
                                            'locked': 'bg-purple-100 text-purple-800',
                                        }
                                        color_class = status_colors.get(entry.status.value, 'bg-gray-100')
                                        ui.label(entry.status.value.replace('_', ' ').title()).classes(f'{color_class} px-3 py-1 rounded-full text-sm font-semibold')
                                    
                                    # Actions
                                    with ui.element('td').classes('p-3'):
                                        with ui.row().classes('gap-2'):
                                            if is_hr:
                                                ui.button('View', icon='visibility').props('flat size=sm')
                                                ui.button('Edit', icon='edit').props('flat size=sm color=blue')
                                            else:
                                                ui.button('View', icon='visibility').props('flat size=sm')
        
        # Footer info
        with ui.card().classes('w-full bg-white shadow-lg'):
            with ui.card_section().classes('p-4 text-center'):
                ui.label('Timesheet data is AI-enhanced. Only HR roles can edit entries.').classes('text-sm text-gray-600')


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
