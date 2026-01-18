"""
Modern Employee Management System
Refactored for NiceGUI v2.23 with modern design and page connections
"""

from nicegui import ui
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional
import random

# Enums for employee status
class EmployeeStatus(Enum):
    ACTIVE = "active"
    ON_LEAVE = "on_leave"
    REMOTE = "remote"
    TERMINATED = "terminated"
    PENDING = "pending"

@dataclass
class Employee:
    """Represents an employee"""
    id: str
    first_name: str
    last_name: str
    email: str
    department: str
    position: str
    employment_type: str
    status: EmployeeStatus
    hire_date: str
    salary_range: str = ""
    direct_manager: str = ""
    phone: str = ""
    location: str = "On-site"

class EmployeeManager:
    """Manages employee data and operations"""
    
    def __init__(self):
        self.employees: Dict[str, Employee] = {}
        self.load_employees()
    
    def load_employees(self):
        """Load sample employees"""
        departments = ['Engineering', 'Sales', 'HR', 'Finance', 'Operations']
        positions = {
            'Engineering': ['Senior Developer', 'Developer', 'DevOps Engineer'],
            'Sales': ['Sales Manager', 'Sales Executive', 'Account Manager'],
            'HR': ['HR Manager', 'Recruiter', 'HR Analyst'],
            'Finance': ['CFO', 'Accountant', 'Financial Analyst'],
            'Operations': ['Operations Manager', 'Coordinator', 'Analyst']
        }
        employment_types = ['Full-time', 'Part-time', 'Contract', 'Intern']
        
        employees_data = [
            ('Alice Johnson', 'Engineering', 'Senior Developer'),
            ('Bob Smith', 'Sales', 'Sales Manager'),
            ('Carol White', 'HR', 'HR Manager'),
            ('David Brown', 'Finance', 'Accountant'),
            ('Emma Davis', 'Operations', 'Operations Manager'),
            ('Frank Miller', 'Engineering', 'Developer'),
            ('Grace Lee', 'Sales', 'Sales Executive'),
            ('Henry Wilson', 'Engineering', 'DevOps Engineer'),
            ('Iris Anderson', 'Finance', 'Financial Analyst'),
            ('Jack Taylor', 'Operations', 'Coordinator'),
        ]
        
        for idx, (name, dept, pos) in enumerate(employees_data):
            first, last = name.split()
            emp_id = f"EMP{1000 + idx}"
            email = f"{first.lower()}.{last.lower()}@company.com"
            
            self.employees[emp_id] = Employee(
                id=emp_id,
                first_name=first,
                last_name=last,
                email=email,
                department=dept,
                position=pos,
                employment_type=random.choice(employment_types),
                status=random.choice(list(EmployeeStatus)),
                hire_date=f"2021-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                salary_range=f"${random.randint(50, 150)}K - ${random.randint(150, 200)}K",
                direct_manager="John Doe" if idx > 0 else "CEO",
                phone=f"+1-555-{random.randint(1000, 9999)}",
                location=random.choice(['On-site', 'Remote', 'Hybrid'])
            )
    
    def get_employees(self):
        """Get all employees"""
        return list(self.employees.values())


def create_modern_employee_interface():
    """Modern, refactored employee management UI for NiceGUI v2.23"""
    manager = EmployeeManager()
    employees = manager.get_employees()
    
    # Calculate statistics
    total = len(employees)
    active = sum(1 for e in employees if e.status == EmployeeStatus.ACTIVE)
    on_leave = sum(1 for e in employees if e.status == EmployeeStatus.ON_LEAVE)
    remote = sum(1 for e in employees if e.location == 'Remote')
    
    # State for filtering and search
    selected_employee = {'data': None}
    
    # Main layout
    with ui.column().classes('w-full bg-gradient-to-br from-slate-50 to-blue-50 min-h-screen p-6'):
        
        # Header with navigation buttons
        with ui.card().classes('w-full bg-white shadow-lg'):
            with ui.card_section().classes('p-8'):
                with ui.row().classes('w-full items-center justify-between'):
                    with ui.column().classes('gap-2'):
                        ui.label('👥 Employee Management').classes('text-4xl font-bold text-blue-800')
                        ui.label('Manage team members, track performance, and organize company structure').classes('text-gray-600 text-lg')
                    
                    with ui.row().classes('gap-3'):
                        ui.button('Add Employee', icon='person_add').props('color=green')
                        ui.button('Import', icon='upload').props('flat')
                        ui.button('Export', icon='download').props('flat')
        
        # Statistics Cards
        with ui.card().classes('w-full bg-white shadow-lg'):
            with ui.card_section().classes('p-6'):
                with ui.row().classes('gap-4 w-full'):
                    # Total Employees
                    with ui.card().classes('flex-1 bg-gradient-to-br from-blue-500 to-blue-700 text-white shadow-md'):
                        with ui.card_section().classes('p-4 text-center'):
                            ui.label('Total Employees').classes('text-sm opacity-90')
                            ui.label(f'{total}').classes('text-3xl font-bold mt-2')
                    
                    # Active Employees
                    with ui.card().classes('flex-1 bg-gradient-to-br from-green-500 to-green-700 text-white shadow-md'):
                        with ui.card_section().classes('p-4 text-center'):
                            ui.label('Active').classes('text-sm opacity-90')
                            ui.label(f'{active}').classes('text-3xl font-bold mt-2')
                    
                    # On Leave
                    with ui.card().classes('flex-1 bg-gradient-to-br from-orange-500 to-orange-700 text-white shadow-md'):
                        with ui.card_section().classes('p-4 text-center'):
                            ui.label('On Leave').classes('text-sm opacity-90')
                            ui.label(f'{on_leave}').classes('text-3xl font-bold mt-2')
                    
                    # Remote Workers
                    with ui.card().classes('flex-1 bg-gradient-to-br from-purple-500 to-purple-700 text-white shadow-md'):
                        with ui.card_section().classes('p-4 text-center'):
                            ui.label('Remote').classes('text-sm opacity-90')
                            ui.label(f'{remote}').classes('text-3xl font-bold mt-2')
        
        # Search and Filter Bar
        with ui.card().classes('w-full bg-white shadow-lg'):
            with ui.card_section().classes('p-6'):
                with ui.row().classes('w-full gap-4'):
                    search_input = ui.input(placeholder='🔍 Search by name or email').classes('flex-1')
                    department_select = ui.select(
                        label='Department',
                        value='All',
                        options=['All', 'Engineering', 'Sales', 'HR', 'Finance', 'Operations']
                    ).classes('w-48')
                    status_select = ui.select(
                        label='Status',
                        value='All',
                        options=['All', 'Active', 'On Leave', 'Remote', 'Pending']
                    ).classes('w-48')
        
        # Employee Table
        with ui.card().classes('w-full bg-white shadow-lg'):
            with ui.card_section().classes('p-6'):
                ui.label('Employee Directory').classes('text-xl font-bold mb-4 block')
                
                with ui.element('div').classes('overflow-x-auto'):
                    with ui.element('table').classes('w-full border-collapse'):
                        # Table Header
                        with ui.element('thead'):
                            with ui.element('tr').classes('bg-gradient-to-r from-blue-100 to-blue-50 border-b-2 border-blue-300'):
                                headers = ['', 'Name', 'ID', 'Department', 'Position', 'Status', 'Location', 'Hire Date', 'Actions']
                                for header in headers:
                                    with ui.element('th').classes('p-4 text-left font-semibold text-blue-800'):
                                        ui.label(header).classes('text-sm')
                        
                        # Table Body
                        with ui.element('tbody'):
                            for idx, emp in enumerate(employees):
                                row_class = 'hover:bg-blue-50 border-b border-gray-200'
                                with ui.element('tr').classes(row_class):
                                    # Avatar
                                    with ui.element('td').classes('p-4'):
                                        initials = f"{emp.first_name[0]}{emp.last_name[0]}".upper()
                                        with ui.element('div').classes('w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-700 text-white rounded-full flex items-center justify-center font-bold'):
                                            ui.label(initials).classes('text-white text-sm')
                                    
                                    # Name
                                    with ui.element('td').classes('p-4'):
                                        ui.label(f'{emp.first_name} {emp.last_name}').classes('font-semibold text-gray-800')
                                    
                                    # ID
                                    with ui.element('td').classes('p-4'):
                                        ui.label(emp.id).classes('font-mono text-gray-600 text-sm')
                                    
                                    # Department
                                    with ui.element('td').classes('p-4'):
                                        ui.label(emp.department).classes('text-gray-700')
                                    
                                    # Position
                                    with ui.element('td').classes('p-4'):
                                        ui.label(emp.position).classes('text-gray-700')
                                    
                                    # Status Badge
                                    with ui.element('td').classes('p-4'):
                                        status_colors = {
                                            'active': 'bg-green-100 text-green-800',
                                            'on_leave': 'bg-orange-100 text-orange-800',
                                            'remote': 'bg-purple-100 text-purple-800',
                                            'pending': 'bg-yellow-100 text-yellow-800',
                                            'terminated': 'bg-red-100 text-red-800',
                                        }
                                        color = status_colors.get(emp.status.value, 'bg-gray-100 text-gray-800')
                                        ui.label(emp.status.value.replace('_', ' ').title()).classes(f'{color} px-3 py-1 rounded-full text-xs font-semibold')
                                    
                                    # Location
                                    with ui.element('td').classes('p-4'):
                                        location_icon = {'On-site': '🏢', 'Remote': '🏠', 'Hybrid': '🔄'}.get(emp.location, '📍')
                                        ui.label(f'{location_icon} {emp.location}').classes('text-gray-700 text-sm')
                                    
                                    # Hire Date
                                    with ui.element('td').classes('p-4'):
                                        ui.label(emp.hire_date).classes('text-gray-600 text-sm')
                                    
                                    # Actions
                                    with ui.element('td').classes('p-4'):
                                        with ui.row().classes('gap-2'):
                                            ui.button(icon='visibility').props('flat size=sm') \
                                                .on_click(lambda emp=emp: show_employee_details(emp, selected_employee))
                                            ui.button(icon='edit').props('flat size=sm color=blue') \
                                                .on_click(lambda emp=emp: show_edit_employee(emp))
                                            ui.button(icon='more_vert').props('flat size=sm')
        
        # Employee Details Card (shown when selected)
        details_container = ui.card().classes('w-full bg-white shadow-lg')
        
        def show_employee_details(emp, selected_emp):
            """Display employee details"""
            selected_emp['data'] = emp
            details_container.clear()
            with details_container:
                with ui.card_section().classes('p-6'):
                    with ui.row().classes('w-full gap-6'):
                        # Left: Profile Info
                        with ui.column().classes('flex-1 gap-4'):
                            ui.label(f'{emp.first_name} {emp.last_name}').classes('text-2xl font-bold text-gray-800')
                            ui.label(emp.position).classes('text-lg text-blue-600 font-semibold')
                            ui.label(f'📧 {emp.email}').classes('text-gray-600')
                            ui.label(f'📞 {emp.phone}').classes('text-gray-600')
                            ui.label(f'🏢 {emp.department} | {emp.employment_type}').classes('text-gray-600')
                        
                        # Right: Details Grid
                        with ui.column().classes('flex-1 gap-4'):
                            with ui.row().classes('w-full gap-4'):
                                with ui.column().classes('flex-1'):
                                    ui.label('Employee ID').classes('text-xs font-semibold text-gray-500 uppercase')
                                    ui.label(emp.id).classes('text-lg font-semibold text-gray-800')
                                
                                with ui.column().classes('flex-1'):
                                    ui.label('Hire Date').classes('text-xs font-semibold text-gray-500 uppercase')
                                    ui.label(emp.hire_date).classes('text-lg font-semibold text-gray-800')
                            
                            with ui.row().classes('w-full gap-4'):
                                with ui.column().classes('flex-1'):
                                    ui.label('Location').classes('text-xs font-semibold text-gray-500 uppercase')
                                    ui.label(emp.location).classes('text-lg font-semibold text-gray-800')
                                
                                with ui.column().classes('flex-1'):
                                    ui.label('Salary Range').classes('text-xs font-semibold text-gray-500 uppercase')
                                    ui.label(emp.salary_range).classes('text-lg font-semibold text-gray-800')
                            
                            with ui.row().classes('w-full gap-4'):
                                with ui.column().classes('flex-1'):
                                    ui.label('Direct Manager').classes('text-xs font-semibold text-gray-500 uppercase')
                                    ui.label(emp.direct_manager).classes('text-lg font-semibold text-gray-800')
                        
                        # Right: Action Buttons
                        with ui.column().classes('flex-shrink-0 gap-2'):
                            ui.button('View Timesheet', icon='schedule').props('flat color=blue') \
                                .on_click(lambda: ui.navigate('/hrmkit/reporting/employees/timesheet'))
                            ui.button('View Leave', icon='event_busy').props('flat color=orange')
                            ui.button('Edit Info', icon='edit').props('flat color=green')
                            ui.button('Send Message', icon='mail').props('flat')
        
        def show_edit_employee(emp):
            """Show edit employee dialog"""
            with ui.dialog() as dialog:
                with ui.card().classes('w-full'):
                    with ui.card_section().classes('p-6'):
                        ui.label(f'Edit {emp.first_name} {emp.last_name}').classes('text-xl font-bold')
                        
                        with ui.column().classes('gap-4 w-96'):
                            ui.input(label='First Name', value=emp.first_name)
                            ui.input(label='Last Name', value=emp.last_name)
                            ui.input(label='Email', value=emp.email)
                            ui.select(label='Department', value=emp.department, 
                                    options=['Engineering', 'Sales', 'HR', 'Finance', 'Operations'])
                            ui.input(label='Position', value=emp.position)
                            ui.input(label='Phone', value=emp.phone)
                            
                            with ui.row().classes('w-full gap-2 justify-end'):
                                ui.button('Cancel').on_click(dialog.close).props('flat')
                                ui.button('Save', icon='save').props('color=blue')
            
            dialog.open()
        
        # Footer
        with ui.card().classes('w-full bg-white shadow-lg'):
            with ui.card_section().classes('p-4 text-center'):
                ui.label('Employee data is securely stored. Last synced with HR system 2 minutes ago.').classes('text-sm text-gray-600')


def create_employee_management_page():
    """Main page function for modern employee management"""
    create_modern_employee_interface()


# Backward compatibility
def create_employee_management():
    """Backward compatibility wrapper"""
    create_modern_employee_interface()


def create_employee_table(manager: EmployeeManager):
    """Backward compatibility wrapper"""
    create_modern_employee_interface()


def calculate_employee_stats(manager: EmployeeManager) -> Dict[str, int]:
    """Calculate employee statistics"""
    employees = manager.get_employees()
    total = len(employees)
    active = sum(1 for e in employees if e.status == EmployeeStatus.ACTIVE)
    on_leave = sum(1 for e in employees if e.status == EmployeeStatus.ON_LEAVE)
    remote = sum(1 for e in employees if e.location == 'Remote')
    
    return {
        "total": total,
        "active": active,
        "on_leave": on_leave,
        "remote": remote
    }
