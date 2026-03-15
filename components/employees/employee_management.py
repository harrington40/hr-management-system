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
from helperFuns.employee_registry import employee_registry

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
    """Manages employee data from the shared registry."""
    
    def __init__(self):
        pass

    def get_employees(self) -> List[Employee]:
        """Load all employees from shared registry, return as Employee dataclass list."""
        result = []
        for rec in employee_registry.get_all():
            # Map status string to enum (tolerate unknown values)
            raw_status = (rec.get('status') or 'active').lower()
            try:
                status = EmployeeStatus(raw_status)
            except ValueError:
                status = EmployeeStatus.ACTIVE

            salary = rec.get('salary')
            sal_str = f"${int(salary):,}" if salary else rec.get('salary_grade', 'N/A')

            result.append(Employee(
                id=rec['employee_id'],
                first_name=rec.get('first_name', ''),
                last_name=rec.get('last_name', ''),
                email=rec.get('email', ''),
                department=rec.get('department', ''),
                position=rec.get('position', ''),
                employment_type=rec.get('employment_type', 'full_time'),
                status=status,
                hire_date=rec.get('hire_date', ''),
                salary_range=sal_str,
                direct_manager=rec.get('manager_id', ''),
                phone=rec.get('phone', ''),
                location=rec.get('location', 'On-site'),
            ))
        # Fall back to sample data only when registry is empty (first-run / no YAML)
        if not result:
            result = self._sample_employees()
        return result

    def _sample_employees(self) -> List[Employee]:
        employees_data = [
            ('Alice Johnson', 'Engineering', 'Senior Developer'),
            ('Bob Smith', 'Sales', 'Sales Manager'),
            ('Carol White', 'Human Resources', 'HR Manager'),
            ('David Brown', 'Finance', 'Accountant'),
            ('Emma Davis', 'Operations', 'Operations Manager'),
        ]
        out = []
        for idx, (name, dept, pos) in enumerate(employees_data):
            first, last = name.split()
            emp_id = f"EMP{1001 + idx:06d}"
            out.append(Employee(
                id=emp_id,
                first_name=first,
                last_name=last,
                email=f"{first.lower()}.{last.lower()}@company.com",
                department=dept,
                position=pos,
                employment_type='Full-time',
                status=EmployeeStatus.ACTIVE,
                hire_date='2022-01-01',
                salary_range='$60K - $90K',
                direct_manager='John Doe' if idx > 0 else 'CEO',
                phone=f'+1-555-{1000+idx}',
                location='On-site',
            ))
        return out


def create_modern_employee_interface():
    """Modern, refactored employee management UI for NiceGUI v2.23"""
    manager = EmployeeManager()
    employees = manager.get_employees()

    # Calculate statistics
    total    = len(employees)
    active   = sum(1 for e in employees if e.status == EmployeeStatus.ACTIVE)
    on_leave = sum(1 for e in employees if e.status == EmployeeStatus.ON_LEAVE)
    remote   = sum(1 for e in employees if e.location == 'Remote')
    pending  = sum(1 for e in employees if e.status == EmployeeStatus.PENDING)

    # State for filtering and search
    selected_employee = {'data': None}

    # ── KPI card helper ───────────────────────────────────────────────────────
    def kpi_card(icon: str, label: str, value: str, gradient: str, sub: str = ''):
        with ui.card().classes(
            f'flex-1 min-w-0 {gradient} text-white rounded-2xl shadow-lg '
            'transition-transform duration-200 hover:-translate-y-1 hover:shadow-2xl'
        ):
            with ui.card_section().classes('p-5 flex flex-col items-center gap-2 text-center'):
                ui.html(f'<div class="text-4xl mb-1">{icon}</div>')
                ui.html(f'<div class="text-3xl font-extrabold tracking-tight">{value}</div>')
                ui.html(f'<div class="text-sm font-semibold uppercase tracking-widest opacity-80">{label}</div>')
                if sub:
                    ui.html(f'<div class="text-xs opacity-60 mt-1">{sub}</div>')

    # ── Main layout ───────────────────────────────────────────────────────────
    with ui.column().classes('w-full bg-gradient-to-br from-slate-100 to-blue-50 min-h-screen p-6 gap-6'):

        # ── Header ────────────────────────────────────────────────────────────
        with ui.card().classes('w-full rounded-2xl shadow-md bg-gradient-to-r from-blue-700 to-indigo-700 text-white'):
            with ui.card_section().classes('px-8 py-6'):
                with ui.row().classes('w-full items-center justify-between'):
                    with ui.column().classes('gap-1'):
                        ui.html('<h1 class="text-3xl font-extrabold tracking-tight flex items-center gap-3">'
                                '👥 Employee Management</h1>')
                        ui.html('<p class="text-blue-100 text-sm">Manage team members, '
                                'track performance &amp; organise company structure</p>')
                    with ui.row().classes('gap-3'):
                        ui.button('Add Employee', icon='person_add').props('color=white text-color=blue-700') \
                            .on_click(lambda: show_add_employee())
                        ui.button('Import', icon='upload').props('outline color=white')
                        ui.button('Export', icon='download').props('outline color=white')

        # ── KPI Cards ─────────────────────────────────────────────────────────
        with ui.row().classes('w-full gap-4 flex-nowrap'):
            kpi_card('👥', 'Total',    str(total),    'bg-gradient-to-br from-blue-500 to-blue-700')
            kpi_card('✅', 'Active',   str(active),   'bg-gradient-to-br from-emerald-500 to-emerald-700')
            kpi_card('🌴', 'On Leave', str(on_leave), 'bg-gradient-to-br from-orange-500 to-orange-700')
            kpi_card('🏠', 'Remote',   str(remote),   'bg-gradient-to-br from-purple-500 to-purple-700')
            kpi_card('⏳', 'Pending',  str(pending),  'bg-gradient-to-br from-amber-500 to-amber-700',
                     'Awaiting onboarding')

        # ── Search & Filter ───────────────────────────────────────────────────
        with ui.card().classes('w-full rounded-2xl shadow-md bg-white'):
            with ui.card_section().classes('px-6 py-4'):
                with ui.row().classes('w-full gap-4 items-end'):
                    search_input = ui.input(placeholder='🔍 Search by name or email…').classes('flex-1')
                    department_select = ui.select(
                        label='Department', value='All',
                        options=['All', 'Engineering', 'Sales', 'HR', 'Finance', 'Operations']
                    ).classes('w-44')
                    status_select = ui.select(
                        label='Status', value='All',
                        options=['All', 'Active', 'On Leave', 'Remote', 'Pending']
                    ).classes('w-40')

        # ── Employee Directory Table ──────────────────────────────────────────
        with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden'):
            with ui.card_section().classes('px-6 pt-6 pb-2'):
                with ui.row().classes('w-full justify-between items-center mb-4'):
                    ui.html('<h2 class="text-xl font-bold text-gray-800 flex items-center gap-2">'
                            '📋 Employee Directory</h2>')
                    ui.html(f'<span class="text-xs text-gray-400 bg-gray-100 px-3 py-1 rounded-full">'
                            f'{total} member{"s" if total != 1 else ""}</span>')

            with ui.element('div').classes('w-full overflow-x-auto px-2 pb-4'):
                with ui.element('table').classes('w-full min-w-full border-collapse'):

                    # ── Table header ──────────────────────────────────────────
                    with ui.element('thead'):
                        with ui.element('tr').classes(
                            'bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-sm'
                        ):
                            th = 'px-4 py-3 text-left font-semibold tracking-wide uppercase whitespace-nowrap'
                            for icon_h, text_h in [
                                ('', ''), ('👤', 'Name'), ('🆔', 'ID'),
                                ('🏢', 'Department'), ('💼', 'Position'),
                                ('🏷', 'Status'), ('📍', 'Location'),
                                ('📅', 'Hire Date'), ('⚙', 'Actions'),
                            ]:
                                with ui.element('th').classes(th):
                                    ui.html(f'{icon_h} {text_h}'.strip())

                    # ── Table body ────────────────────────────────────────────
                    status_colors = {
                        'active':     'bg-emerald-100 text-emerald-800',
                        'on_leave':   'bg-orange-100 text-orange-800',
                        'remote':     'bg-purple-100 text-purple-800',
                        'pending':    'bg-amber-100 text-amber-800',
                        'terminated': 'bg-red-100 text-red-800',
                    }
                    avatar_gradients = [
                        'from-blue-500 to-indigo-600',
                        'from-emerald-500 to-teal-600',
                        'from-purple-500 to-pink-600',
                        'from-orange-500 to-red-500',
                        'from-amber-500 to-yellow-600',
                    ]
                    td = 'px-4 py-3 text-sm text-gray-700 whitespace-nowrap'

                    with ui.element('tbody'):
                        for idx, emp in enumerate(employees):
                            stripe = 'bg-slate-50' if idx % 2 == 0 else 'bg-white'
                            grad   = avatar_gradients[idx % len(avatar_gradients)]
                            initials = f'{emp.first_name[:1]}{emp.last_name[:1]}'.upper()

                            with ui.element('tr').classes(
                                f'{stripe} border-b border-gray-100 '
                                'hover:bg-blue-50 transition-colors duration-150'
                            ):
                                # Avatar
                                with ui.element('td').classes('px-4 py-3'):
                                    ui.html(
                                        f'<div class="w-9 h-9 bg-gradient-to-br {grad} text-white '
                                        f'rounded-full flex items-center justify-center font-bold text-sm '
                                        f'shadow-sm">{initials}</div>'
                                    )

                                # Name
                                with ui.element('td').classes(td):
                                    ui.html(f'<span class="font-semibold text-gray-900">'
                                            f'{emp.first_name} {emp.last_name}</span>')

                                # ID
                                with ui.element('td').classes(td):
                                    ui.html(f'<span class="font-mono text-xs bg-gray-100 text-gray-600 '
                                            f'px-2 py-0.5 rounded">{emp.id}</span>')

                                # Department
                                with ui.element('td').classes(td):
                                    ui.label(emp.department)

                                # Position
                                with ui.element('td').classes(td):
                                    ui.html(f'<span class="text-blue-700 font-medium">{emp.position}</span>')

                                # Status badge
                                with ui.element('td').classes(td):
                                    cls   = status_colors.get(emp.status.value, 'bg-gray-100 text-gray-700')
                                    lbl   = emp.status.value.replace('_', ' ').title()
                                    ui.html(f'<span class="{cls} px-3 py-1 rounded-full text-xs font-bold">{lbl}</span>')

                                # Location
                                with ui.element('td').classes(td):
                                    loc_icon = {'On-site': '🏢', 'Remote': '🏠', 'Hybrid': '🔄'}.get(emp.location, '📍')
                                    ui.html(f'<span>{loc_icon} {emp.location}</span>')

                                # Hire Date
                                with ui.element('td').classes(td):
                                    ui.label(emp.hire_date)

                                # Actions
                                with ui.element('td').classes(td):
                                    with ui.row().classes('gap-1'):
                                        ui.button(icon='visibility').props('flat round dense color=blue size=sm') \
                                            .on_click(lambda e=emp: show_employee_details(e, selected_employee))
                                        ui.button(icon='edit').props('flat round dense color=indigo size=sm') \
                                            .on_click(lambda e=emp: show_edit_employee(e))
                                        ui.button(icon='more_vert').props('flat round dense color=grey size=sm')

        # ── Employee Details Card (shown when selected) ───────────────────────
        details_container = ui.card().classes('w-full rounded-2xl shadow-md bg-white')
        
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
                            fn_in    = ui.input(label='First Name', value=emp.first_name)
                            ln_in    = ui.input(label='Last Name',  value=emp.last_name)
                            email_in = ui.input(label='Email',      value=emp.email)
                            dept_in  = ui.select(
                                label='Department', value=emp.department,
                                options=['Engineering', 'Sales', 'HR', 'Finance', 'Operations', 'IT', 'Marketing']
                            )
                            pos_in   = ui.input(label='Position',   value=emp.position)
                            phone_in = ui.input(label='Phone',      value=emp.phone)

                            def save_edit():
                                updates = {
                                    'first_name': (fn_in.value or '').strip(),
                                    'last_name':  (ln_in.value or '').strip(),
                                    'email':      (email_in.value or '').strip(),
                                    'department': dept_in.value,
                                    'position':   (pos_in.value or '').strip(),
                                    'phone':      (phone_in.value or '').strip(),
                                }
                                employee_registry.update(emp.id, updates)
                                employee_registry.save_yaml()
                                dialog.close()
                                ui.notify(
                                    f"✅ {fn_in.value} {ln_in.value} updated successfully",
                                    type='positive'
                                )
                                ui.navigate.reload()

                            with ui.row().classes('w-full gap-2 justify-end'):
                                ui.button('Cancel').on_click(dialog.close).props('flat')
                                ui.button('Save', icon='save').props('color=blue').on_click(save_edit)

            dialog.open()

        def show_add_employee():
            """Dialog to add a new employee — defined as inner function for NiceGUI context."""
            with ui.dialog() as dialog:
                with ui.card().classes('w-full max-w-2xl'):
                    with ui.card_section().classes('p-6'):
                        ui.label('➕ Add New Employee').classes('text-2xl font-bold text-blue-800 mb-2')
                        preview_id = employee_registry.next_id()
                        ui.label(f'New Employee ID: {preview_id}').classes(
                            'text-sm text-gray-500 font-mono bg-gray-50 px-3 py-1 rounded border mb-3 block'
                        )

                        with ui.column().classes('gap-3 w-full'):
                            with ui.row().classes('w-full gap-3'):
                                f_name  = ui.input(label='First Name *').classes('flex-1')
                                l_name  = ui.input(label='Last Name *').classes('flex-1')

                            email_in  = ui.input(label='Email *', placeholder='user@company.com').classes('w-full')
                            phone_in  = ui.input(label='Phone', placeholder='+1-555-0000').classes('w-full')

                            with ui.row().classes('w-full gap-3'):
                                dept_in = ui.select(
                                    label='Department *', value='Engineering',
                                    options=['Engineering', 'Sales', 'HR', 'Finance', 'Operations', 'IT', 'Marketing']
                                ).classes('flex-1')
                                emp_type = ui.select(
                                    label='Employment Type', value='full_time',
                                    options=[
                                        {'label': 'Full Time',  'value': 'full_time'},
                                        {'label': 'Part Time',  'value': 'part_time'},
                                        {'label': 'Contract',   'value': 'contract'},
                                        {'label': 'Intern',     'value': 'intern'},
                                    ]
                                ).classes('flex-1')

                            position_in = ui.input(label='Position / Job Title *').classes('w-full')

                            with ui.row().classes('w-full gap-3'):
                                hire_date_in = ui.input(
                                    label='Hire Date',
                                    value=datetime.now().strftime('%Y-%m-%d'),
                                    placeholder='YYYY-MM-DD'
                                ).classes('flex-1')
                                status_in = ui.select(
                                    label='Status', value='active',
                                    options=[
                                        {'label': 'Active',  'value': 'active'},
                                        {'label': 'Pending', 'value': 'pending'},
                                    ]
                                ).classes('flex-1')

                            with ui.row().classes('w-full gap-3'):
                                location_in = ui.select(
                                    label='Work Location', value='On-site',
                                    options=['On-site', 'Remote', 'Hybrid']
                                ).classes('flex-1')
                                salary_in = ui.number(label='Salary (optional)', placeholder='e.g. 75000').classes('flex-1')

                            manager_in = ui.input(label='Direct Manager (optional)').classes('w-full')

                        def save_employee():
                            data = {
                                'first_name':      (f_name.value or '').strip(),
                                'last_name':       (l_name.value or '').strip(),
                                'email':           (email_in.value or '').strip(),
                                'phone':           (phone_in.value or '').strip(),
                                'department':      dept_in.value or 'Engineering',
                                'position':        (position_in.value or '').strip(),
                                'employment_type': emp_type.value or 'full_time',
                                'hire_date':       hire_date_in.value or datetime.now().strftime('%Y-%m-%d'),
                                'status':          status_in.value or 'active',
                                'work_location':   location_in.value or 'On-site',
                                'salary':          float(salary_in.value) if salary_in.value else None,
                                'manager_id':      (manager_in.value or '').strip(),
                            }
                            if not data['first_name'] or not data['last_name']:
                                ui.notify('First and last name are required.', type='warning')
                                return
                            if not data['email']:
                                ui.notify('Email is required.', type='warning')
                                return
                            if not data['position']:
                                ui.notify('Position / Job title is required.', type='warning')
                                return

                            new_id = employee_registry.add(data)
                            employee_registry.save_yaml()
                            dialog.close()
                            ui.notify(
                                f"✅ {data['first_name']} {data['last_name']} added (ID: {new_id})",
                                type='positive'
                            )
                            ui.navigate.reload()

                        with ui.row().classes('w-full gap-2 justify-end pt-4'):
                            ui.button('Cancel', icon='close').props('flat').on_click(dialog.close)
                            ui.button('Save Employee', icon='save').props('color=green').on_click(save_employee)

            dialog.open()

        # ── Footer ────────────────────────────────────────────────────────────
        with ui.card().classes('w-full rounded-2xl shadow-sm bg-white'):
            with ui.card_section().classes('px-6 py-4'):
                with ui.row().classes('w-full justify-between items-center'):
                    ui.html('<p class="text-xs text-gray-400">🔒 Employee data is securely stored '
                            '— only authorised HR roles can edit records.</p>')
                    ui.html(f'<p class="text-xs text-gray-400">Last synced: '
                            f'{datetime.now().strftime("%d %b %Y, %H:%M")}</p>')


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
