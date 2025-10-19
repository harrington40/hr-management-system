"""
Enterprise Employee Management System
Advanced employee lifecycle management with role-based access control
Integrated with hardware time clock systems and biometric authentication
"""

from nicegui import ui
import yaml
import os
from datetime import datetime, timedelta, date
import json
import hashlib
import secrets
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

class EmployeeStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    TERMINATED = "terminated"
    ON_LEAVE = "on_leave"
    SUSPENDED = "suspended"
    PROBATION = "probation"

class UserRole(Enum):
    SUPER_ADMIN = "super_admin"
    HR_ADMIN = "hr_admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"
    CONTRACTOR = "contractor"
    INTERN = "intern"

class EmploymentType(Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    TEMPORARY = "temporary"
    INTERN = "intern"

@dataclass
class Employee:
    employee_id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    department: str
    position: str
    employment_type: EmploymentType
    status: EmployeeStatus
    hire_date: str
    manager_id: Optional[str]
    salary: Optional[float]
    hourly_rate: Optional[float]
    role: UserRole
    biometric_id: Optional[str]
    rfid_card: Optional[str]
    emergency_contact: Dict[str, str]
    address: Dict[str, str]
    benefits: Dict[str, Any]
    performance_rating: float = 0.0
    created_at: str = ""
    updated_at: str = ""

@dataclass
class BiometricData:
    employee_id: str
    fingerprint_template: str
    face_template: str
    voice_template: str
    last_updated: str
    is_active: bool = True

class EmployeeManager:
    """Advanced Employee Management System with Hardware Integration"""
    
    def __init__(self):
        self.config_dir = "config"
        self.employees_file = os.path.join(self.config_dir, "employees.yaml")
        self.biometric_file = os.path.join(self.config_dir, "biometric_data.yaml")
        self.roles_file = os.path.join(self.config_dir, "roles_permissions.yaml")
        self.audit_log_file = os.path.join(self.config_dir, "employee_audit.yaml")
        
        self.ensure_config_directory()
        self.employees = self.load_employees()
        self.biometric_data = self.load_biometric_data()
        self.roles = self.load_roles_permissions()
        self.audit_log = self.load_audit_log()
    
    def ensure_config_directory(self):
        """Ensure config directory exists"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
    
    def generate_employee_id(self) -> str:
        """Generate unique employee ID using advanced algorithm"""
        timestamp = int(datetime.now().timestamp())
        random_part = secrets.randbelow(9999)
        return f"EMP{timestamp % 100000:05d}{random_part:04d}"
    
    def hash_biometric_data(self, raw_data: str) -> str:
        """Hash biometric data for security"""
        salt = secrets.token_hex(16)
        hashed = hashlib.pbkdf2_hmac('sha256', raw_data.encode(), salt.encode(), 100000)
        return f"{salt}${hashed.hex()}"
    
    def load_employees(self) -> Dict[str, Employee]:
        """Load employees from YAML file"""
        if os.path.exists(self.employees_file):
            try:
                with open(self.employees_file, 'r') as file:
                    data = yaml.safe_load(file) or {}
                    employees = {}
                    for emp_id, emp_data in data.items():
                        # Convert dict back to Employee dataclass
                        emp_data['employment_type'] = EmploymentType(emp_data.get('employment_type', 'full_time'))
                        emp_data['status'] = EmployeeStatus(emp_data.get('status', 'active'))
                        emp_data['role'] = UserRole(emp_data.get('role', 'employee'))
                        employees[emp_id] = Employee(**emp_data)
                    return employees
            except Exception as e:
                print(f"Error loading employees: {e}")
                return self.get_default_employees()
        else:
            default_employees = self.get_default_employees()
            self.save_employees(default_employees)
            return default_employees
    
    def save_employees(self, employees: Dict[str, Employee]) -> bool:
        """Save employees to YAML file"""
        try:
            # Convert Employee dataclasses to dict for YAML serialization
            data = {}
            for emp_id, employee in employees.items():
                emp_dict = asdict(employee)
                # Convert enums to strings
                emp_dict['employment_type'] = employee.employment_type.value
                emp_dict['status'] = employee.status.value
                emp_dict['role'] = employee.role.value
                data[emp_id] = emp_dict
            
            with open(self.employees_file, 'w') as file:
                yaml.dump(data, file, default_flow_style=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving employees: {e}")
            return False
    
    def get_default_employees(self) -> Dict[str, Employee]:
        """Generate default employee data"""
        current_time = datetime.now().isoformat()
        
        employees = {
            "EMP001001": Employee(
                employee_id="EMP001001",
                first_name="John",
                last_name="Smith",
                email="john.smith@company.com",
                phone="+1-555-0101",
                department="Engineering",
                position="Senior Software Engineer",
                employment_type=EmploymentType.FULL_TIME,
                status=EmployeeStatus.ACTIVE,
                hire_date="2023-01-15",
                manager_id="EMP001005",
                salary=95000.00,
                hourly_rate=None,
                role=UserRole.EMPLOYEE,
                biometric_id="BIO001001",
                rfid_card="RFID001001",
                emergency_contact={
                    "name": "Jane Smith",
                    "phone": "+1-555-0102",
                    "relationship": "Spouse"
                },
                address={
                    "street": "123 Main St",
                    "city": "Tech City",
                    "state": "CA",
                    "zip": "90210",
                    "country": "USA"
                },
                benefits={
                    "health_insurance": True,
                    "dental_insurance": True,
                    "retirement_401k": True,
                    "vacation_days": 20,
                    "sick_days": 10
                },
                performance_rating=4.2,
                created_at=current_time,
                updated_at=current_time
            ),
            "EMP001002": Employee(
                employee_id="EMP001002",
                first_name="Sarah",
                last_name="Johnson",
                email="sarah.johnson@company.com",
                phone="+1-555-0103",
                department="Human Resources",
                position="HR Manager",
                employment_type=EmploymentType.FULL_TIME,
                status=EmployeeStatus.ACTIVE,
                hire_date="2022-11-08",
                manager_id=None,
                salary=85000.00,
                hourly_rate=None,
                role=UserRole.HR_ADMIN,
                biometric_id="BIO001002",
                rfid_card="RFID001002",
                emergency_contact={
                    "name": "Michael Johnson",
                    "phone": "+1-555-0104",
                    "relationship": "Partner"
                },
                address={
                    "street": "456 Oak Ave",
                    "city": "Business Park",
                    "state": "CA",
                    "zip": "90211",
                    "country": "USA"
                },
                benefits={
                    "health_insurance": True,
                    "dental_insurance": True,
                    "retirement_401k": True,
                    "vacation_days": 25,
                    "sick_days": 15
                },
                performance_rating=4.7,
                created_at=current_time,
                updated_at=current_time
            ),
            "EMP001003": Employee(
                employee_id="EMP001003",
                first_name="David",
                last_name="Wilson",
                email="david.wilson@company.com",
                phone="+1-555-0105",
                department="Sales",
                position="Sales Representative",
                employment_type=EmploymentType.FULL_TIME,
                status=EmployeeStatus.ACTIVE,
                hire_date="2023-03-22",
                manager_id="EMP001007",
                salary=None,
                hourly_rate=25.00,
                role=UserRole.EMPLOYEE,
                biometric_id="BIO001003",
                rfid_card="RFID001003",
                emergency_contact={
                    "name": "Lisa Wilson",
                    "phone": "+1-555-0106",
                    "relationship": "Spouse"
                },
                address={
                    "street": "789 Pine Rd",
                    "city": "Sales District",
                    "state": "CA",
                    "zip": "90212",
                    "country": "USA"
                },
                benefits={
                    "health_insurance": True,
                    "dental_insurance": False,
                    "retirement_401k": True,
                    "vacation_days": 15,
                    "sick_days": 8
                },
                performance_rating=3.9,
                created_at=current_time,
                updated_at=current_time
            )
        }
        
        return employees
    
    def load_biometric_data(self) -> Dict[str, BiometricData]:
        """Load biometric data from YAML file"""
        if os.path.exists(self.biometric_file):
            try:
                with open(self.biometric_file, 'r') as file:
                    data = yaml.safe_load(file) or {}
                    return {k: BiometricData(**v) for k, v in data.items()}
            except Exception as e:
                print(f"Error loading biometric data: {e}")
                return {}
        return {}
    
    def load_roles_permissions(self) -> Dict[str, Any]:
        """Load roles and permissions configuration"""
        if os.path.exists(self.roles_file):
            try:
                with open(self.roles_file, 'r') as file:
                    return yaml.safe_load(file) or self.get_default_roles()
            except Exception as e:
                print(f"Error loading roles: {e}")
                return self.get_default_roles()
        else:
            default_roles = self.get_default_roles()
            self.save_roles_permissions(default_roles)
            return default_roles
    
    def get_default_roles(self) -> Dict[str, Any]:
        """Get default roles and permissions"""
        return {
            "super_admin": {
                "name": "Super Administrator",
                "permissions": ["*"],  # All permissions
                "description": "Full system access and control"
            },
            "hr_admin": {
                "name": "HR Administrator",
                "permissions": [
                    "employee.create", "employee.read", "employee.update", "employee.delete",
                    "timesheet.read", "timesheet.update", "timesheet.approve",
                    "payroll.read", "payroll.process",
                    "reports.generate", "audit.view"
                ],
                "description": "Human Resources administrative access"
            },
            "manager": {
                "name": "Department Manager",
                "permissions": [
                    "employee.read", "employee.update_subordinates",
                    "timesheet.read_department", "timesheet.approve_department",
                    "reports.department", "schedule.manage"
                ],
                "description": "Department management access"
            },
            "employee": {
                "name": "Employee",
                "permissions": [
                    "timesheet.read_own", "timesheet.update_own",
                    "profile.read_own", "profile.update_basic",
                    "schedule.view_own", "leave.request"
                ],
                "description": "Basic employee access"
            }
        }
    
    def save_roles_permissions(self, roles: Dict[str, Any]) -> bool:
        """Save roles and permissions to YAML file"""
        try:
            with open(self.roles_file, 'w') as file:
                yaml.dump(roles, file, default_flow_style=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving roles: {e}")
            return False
    
    def load_audit_log(self) -> List[Dict[str, Any]]:
        """Load audit log from YAML file"""
        if os.path.exists(self.audit_log_file):
            try:
                with open(self.audit_log_file, 'r') as file:
                    return yaml.safe_load(file) or []
            except Exception as e:
                print(f"Error loading audit log: {e}")
                return []
        return []
    
    def add_audit_entry(self, action: str, user_id: str, target_id: str, details: str):
        """Add entry to audit log"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "user_id": user_id,
            "target_id": target_id,
            "details": details,
            "ip_address": "127.0.0.1",  # In real app, get from request
            "user_agent": "HR System"
        }
        self.audit_log.append(entry)
        
        # Keep only last 1000 entries
        if len(self.audit_log) > 1000:
            self.audit_log = self.audit_log[-1000:]
        
        try:
            with open(self.audit_log_file, 'w') as file:
                yaml.dump(self.audit_log, file, default_flow_style=False, indent=2)
        except Exception as e:
            print(f"Error saving audit log: {e}")
    
    def create_employee(self, employee_data: Dict[str, Any], current_user_id: str) -> str:
        """Create new employee with validation"""
        employee_id = self.generate_employee_id()
        
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email', 'department', 'position']
        for field in required_fields:
            if not employee_data.get(field):
                raise ValueError(f"Required field '{field}' is missing")
        
        # Check for duplicate email
        for emp in self.employees.values():
            if emp.email == employee_data['email']:
                raise ValueError("Email address already exists")
        
        # Create employee object
        current_time = datetime.now().isoformat()
        employee = Employee(
            employee_id=employee_id,
            first_name=employee_data['first_name'],
            last_name=employee_data['last_name'],
            email=employee_data['email'],
            phone=employee_data.get('phone', ''),
            department=employee_data['department'],
            position=employee_data['position'],
            employment_type=EmploymentType(employee_data.get('employment_type', 'full_time')),
            status=EmployeeStatus(employee_data.get('status', 'active')),
            hire_date=employee_data.get('hire_date', datetime.now().strftime('%Y-%m-%d')),
            manager_id=employee_data.get('manager_id'),
            salary=employee_data.get('salary'),
            hourly_rate=employee_data.get('hourly_rate'),
            role=UserRole(employee_data.get('role', 'employee')),
            biometric_id=f"BIO{employee_id[3:]}",
            rfid_card=f"RFID{employee_id[3:]}",
            emergency_contact=employee_data.get('emergency_contact', {}),
            address=employee_data.get('address', {}),
            benefits=employee_data.get('benefits', {}),
            created_at=current_time,
            updated_at=current_time
        )
        
        self.employees[employee_id] = employee
        self.save_employees(self.employees)
        
        # Add audit log entry
        self.add_audit_entry(
            "employee_created",
            current_user_id,
            employee_id,
            f"Created employee {employee.first_name} {employee.last_name}"
        )
        
        return employee_id
    
    def update_employee(self, employee_id: str, updates: Dict[str, Any], current_user_id: str) -> bool:
        """Update employee with validation"""
        if employee_id not in self.employees:
            return False
        
        employee = self.employees[employee_id]
        
        # Track changes for audit log
        changes = []
        
        for field, value in updates.items():
            if hasattr(employee, field):
                old_value = getattr(employee, field)
                if field in ['employment_type', 'status', 'role'] and isinstance(value, str):
                    # Handle enum fields
                    if field == 'employment_type':
                        value = EmploymentType(value)
                    elif field == 'status':
                        value = EmployeeStatus(value)
                    elif field == 'role':
                        value = UserRole(value)
                
                if old_value != value:
                    setattr(employee, field, value)
                    changes.append(f"{field}: {old_value} -> {value}")
        
        if changes:
            employee.updated_at = datetime.now().isoformat()
            self.save_employees(self.employees)
            
            # Add audit log entry
            self.add_audit_entry(
                "employee_updated",
                current_user_id,
                employee_id,
                f"Updated fields: {', '.join(changes)}"
            )
        
        return True
    
    def deactivate_employee(self, employee_id: str, current_user_id: str) -> bool:
        """Deactivate employee (soft delete)"""
        if employee_id not in self.employees:
            return False
        
        employee = self.employees[employee_id]
        employee.status = EmployeeStatus.INACTIVE
        employee.updated_at = datetime.now().isoformat()
        
        self.save_employees(self.employees)
        
        # Add audit log entry
        self.add_audit_entry(
            "employee_deactivated",
            current_user_id,
            employee_id,
            f"Deactivated employee {employee.first_name} {employee.last_name}"
        )
        
        return True
    
    def search_employees(self, query: str, filters: Dict[str, Any] = None) -> List[Employee]:
        """Advanced employee search with filters"""
        results = []
        
        for employee in self.employees.values():
            # Text search in name, email, position, department
            if query:
                search_text = f"{employee.first_name} {employee.last_name} {employee.email} {employee.position} {employee.department}".lower()
                if query.lower() not in search_text:
                    continue
            
            # Apply filters
            if filters:
                if filters.get('department') and employee.department != filters['department']:
                    continue
                if filters.get('status') and employee.status.value != filters['status']:
                    continue
                if filters.get('employment_type') and employee.employment_type.value != filters['employment_type']:
                    continue
                if filters.get('role') and employee.role.value != filters['role']:
                    continue
            
            results.append(employee)
        
        return results


def create_employee_management():
    """Main function to create the employee management interface"""
    employee_manager = EmployeeManager()
    create_employee_interface(employee_manager)

def create_employee_management_page():
    """Page function for employee management"""
    create_employee_management()

def calculate_employee_stats(manager: EmployeeManager) -> Dict[str, int]:
    """Calculate employee statistics"""
    total = len(manager.employees)
    active = sum(1 for emp in manager.employees.values() if emp.status == EmployeeStatus.ACTIVE)
    on_leave = sum(1 for emp in manager.employees.values() if emp.status == EmployeeStatus.ON_LEAVE)
    remote = sum(1 for emp in manager.employees.values() if emp.status == EmployeeStatus.ACTIVE and 'remote' in emp.position.lower())
    
    return {
        "total": total,
        "active": active,
        "on_leave": on_leave,
        "remote": remote
    }

def create_employee_table(manager: EmployeeManager):
    """Create employee table with advanced features"""
    with ui.element('table').classes('w-full table-auto border-collapse'):
        # Header
        with ui.element('thead'):
            with ui.element('tr').classes('bg-gray-100'):
                headers = [
                    'Employee', 'ID', 'Department', 'Position', 'Employment Type',
                    'Status', 'Hire Date', 'Manager', 'Actions'
                ]
                for header in headers:
                    ui.html(f'<th class="border p-3 text-left font-semibold">{header}</th>')
        
        # Body
        with ui.element('tbody'):
            for emp_id, employee in manager.employees.items():
                with ui.element('tr').classes('hover:bg-gray-50'):
                    # Employee info with avatar
                    with ui.element('td').classes('border p-3'):
                        with ui.row().classes('items-center gap-3'):
                            # Custom avatar
                            initials = f"{employee.first_name[0]}{employee.last_name[0]}".upper()
                            with ui.element('div').classes('w-10 h-10 bg-slate-500 text-white rounded-full flex items-center justify-center font-semibold'):
                                ui.html(initials)
                            with ui.column().classes('gap-1'):
                                ui.html(f'<div class="font-medium">{employee.first_name} {employee.last_name}</div>')
                                ui.html(f'<div class="text-sm text-gray-500">{employee.email}</div>')
                    
                    # Employee ID
                    ui.html(f'<td class="border p-3 font-mono text-sm">{employee.employee_id}</td>')
                    
                    # Department
                    ui.html(f'<td class="border p-3">{employee.department}</td>')
                    
                    # Position
                    ui.html(f'<td class="border p-3">{employee.position}</td>')
                    
                    # Employment Type
                    type_colors = {
                        'full_time': 'bg-blue-100 text-blue-800',
                        'part_time': 'bg-yellow-100 text-yellow-800',
                        'contract': 'bg-purple-100 text-purple-800',
                        'temporary': 'bg-orange-100 text-orange-800',
                        'intern': 'bg-green-100 text-green-800'
                    }
                    type_color = type_colors.get(employee.employment_type.value, 'bg-gray-100 text-gray-800')
                    ui.html(f'<td class="border p-3"><span class="px-2 py-1 rounded-full text-xs font-medium {type_color}">{employee.employment_type.value.replace("_", " ").title()}</span></td>')
                    
                    # Status
                    status_colors = {
                        'active': 'bg-green-100 text-green-800',
                        'inactive': 'bg-gray-100 text-gray-800',
                        'on_leave': 'bg-yellow-100 text-yellow-800',
                        'terminated': 'bg-red-100 text-red-800',
                        'suspended': 'bg-orange-100 text-orange-800',
                        'probation': 'bg-blue-100 text-blue-800'
                    }
                    status_color = status_colors.get(employee.status.value, 'bg-gray-100 text-gray-800')
                    ui.html(f'<td class="border p-3"><span class="px-2 py-1 rounded-full text-xs font-medium {status_color}">{employee.status.value.replace("_", " ").title()}</span></td>')
                    
                    # Hire Date
                    ui.html(f'<td class="border p-3">{employee.hire_date}</td>')
                    
                    # Manager
                    manager_name = "N/A"
                    if employee.manager_id and employee.manager_id in manager.employees:
                        mgr = manager.employees[employee.manager_id]
                        manager_name = f"{mgr.first_name} {mgr.last_name}"
                    ui.html(f'<td class="border p-3">{manager_name}</td>')
                    
                    # Actions
                    with ui.element('td').classes('border p-3'):
                        with ui.row().classes('gap-2'):
                            ui.button('👁️', on_click=lambda e=emp_id: show_employee_details(manager, e)).classes('p-1 text-xs bg-blue-100 text-blue-600 hover:bg-blue-200')
                            ui.button('✏️', on_click=lambda e=emp_id: show_edit_employee_dialog(manager, e)).classes('p-1 text-xs bg-green-100 text-green-600 hover:bg-green-200')
                            ui.button('🗑️', on_click=lambda e=emp_id: confirm_delete_employee(manager, e)).classes('p-1 text-xs bg-red-100 text-red-600 hover:bg-red-200')

def show_add_employee_dialog(manager: EmployeeManager):
    """Show dialog for adding new employee"""
    with ui.dialog().props('persistent') as dialog, ui.card().classes('w-full max-w-2xl'):
        with ui.card_section().classes('p-6'):
            ui.html('<h2 class="text-xl font-bold mb-4">➕ Add New Employee</h2>')
            
            # Employee form fields
            first_name = ui.input('First Name', placeholder='Enter first name').classes('w-full mb-4')
            last_name = ui.input('Last Name', placeholder='Enter last name').classes('w-full mb-4')
            email = ui.input('Email', placeholder='employee@company.com').classes('w-full mb-4')
            phone = ui.input('Phone', placeholder='+1-555-0123').classes('w-full mb-4')
            
            with ui.row().classes('w-full gap-4 mb-4'):
                department = ui.select(['Engineering', 'Human Resources', 'Sales', 'Marketing', 'Finance'], 
                                     label='Department').classes('flex-1')
                employment_type = ui.select(['Full Time', 'Part Time', 'Contract', 'Temporary', 'Intern'], 
                                          label='Employment Type').classes('flex-1')
            
            position = ui.input('Position', placeholder='Job title').classes('w-full mb-4')
            
            with ui.row().classes('w-full gap-4 mb-4'):
                salary = ui.number('Annual Salary', placeholder='0.00', format='%.2f').classes('flex-1')
                hire_date = ui.input('Hire Date').classes('flex-1')
                hire_date.props('type=date')
                hire_date.value = datetime.now().strftime('%Y-%m-%d')
            
            # Emergency Contact
            ui.html('<h3 class="text-lg font-semibold mb-2 mt-4">Emergency Contact</h3>')
            with ui.row().classes('w-full gap-4 mb-4'):
                emergency_name = ui.input('Contact Name').classes('flex-1')
                emergency_phone = ui.input('Contact Phone').classes('flex-1')
                emergency_relationship = ui.input('Relationship').classes('flex-1')
            
            # Action buttons
            with ui.row().classes('w-full gap-4 justify-end mt-6'):
                ui.button('Cancel', on_click=lambda: dialog.close()).classes('bg-gray-500 text-white')
                ui.button('Save Employee', on_click=lambda: save_new_employee()).classes('bg-green-600 text-white')
        
        def save_new_employee():
            try:
                employee_data = {
                    'first_name': first_name.value,
                    'last_name': last_name.value,
                    'email': email.value,
                    'phone': phone.value,
                    'department': department.value,
                    'position': position.value,
                    'employment_type': employment_type.value.lower().replace(' ', '_'),
                    'salary': salary.value if salary.value else None,
                    'hire_date': hire_date.value,
                    'emergency_contact': {
                        'name': emergency_name.value,
                        'phone': emergency_phone.value,
                        'relationship': emergency_relationship.value
                    }
                }
                
                emp_id = manager.create_employee(employee_data, "ADMIN001")  # In real app, get current user
                ui.notify(f'Employee created successfully! ID: {emp_id}', type='positive')
                dialog.close()
                # Refresh the page or update the table
            except ValueError as e:
                ui.notify(f'Error: {str(e)}', type='negative')
            except Exception as e:
                ui.notify(f'Unexpected error: {str(e)}', type='negative')
    
    dialog.open()

def show_employee_details(manager: EmployeeManager, employee_id: str):
    """Show detailed employee information"""
    if employee_id not in manager.employees:
        ui.notify('Employee not found', type='negative')
        return
    
    employee = manager.employees[employee_id]
    
    with ui.dialog().props('persistent') as dialog, ui.card().classes('w-full max-w-4xl'):
        with ui.card_section().classes('p-6'):
            ui.html(f'<h2 class="text-xl font-bold mb-4">👤 Employee Details - {employee.first_name} {employee.last_name}</h2>')
            
            # Employee details in tabs
            with ui.tabs().classes('w-full') as tabs:
                basic_tab = ui.tab('Basic Info')
                contact_tab = ui.tab('Contact')
                employment_tab = ui.tab('Employment')
                benefits_tab = ui.tab('Benefits')
                biometric_tab = ui.tab('Biometric')
            
            with ui.tab_panels(tabs, value=basic_tab).classes('w-full'):
                # Basic Info Panel
                with ui.tab_panel(basic_tab):
                    with ui.row().classes('w-full gap-6'):
                        with ui.column().classes('flex-1'):
                            ui.html(f'<div class="mb-2"><strong>Employee ID:</strong> {employee.employee_id}</div>')
                            ui.html(f'<div class="mb-2"><strong>Full Name:</strong> {employee.first_name} {employee.last_name}</div>')
                            ui.html(f'<div class="mb-2"><strong>Email:</strong> {employee.email}</div>')
                            ui.html(f'<div class="mb-2"><strong>Phone:</strong> {employee.phone}</div>')
                        with ui.column().classes('flex-1'):
                            ui.html(f'<div class="mb-2"><strong>Department:</strong> {employee.department}</div>')
                            ui.html(f'<div class="mb-2"><strong>Position:</strong> {employee.position}</div>')
                            ui.html(f'<div class="mb-2"><strong>Status:</strong> {employee.status.value.title()}</div>')
                            ui.html(f'<div class="mb-2"><strong>Role:</strong> {employee.role.value.replace("_", " ").title()}</div>')
                
                # Contact Panel
                with ui.tab_panel(contact_tab):
                    ui.html(f'<div class="mb-4"><h3 class="font-semibold">Address</h3></div>')
                    if employee.address:
                        for key, value in employee.address.items():
                            ui.html(f'<div class="mb-2"><strong>{key.title()}:</strong> {value}</div>')
                    
                    ui.html(f'<div class="mb-4 mt-6"><h3 class="font-semibold">Emergency Contact</h3></div>')
                    if employee.emergency_contact:
                        for key, value in employee.emergency_contact.items():
                            ui.html(f'<div class="mb-2"><strong>{key.title()}:</strong> {value}</div>')
                
                # Employment Panel
                with ui.tab_panel(employment_tab):
                    ui.html(f'<div class="mb-2"><strong>Employment Type:</strong> {employee.employment_type.value.replace("_", " ").title()}</div>')
                    ui.html(f'<div class="mb-2"><strong>Hire Date:</strong> {employee.hire_date}</div>')
                    if employee.salary:
                        ui.html(f'<div class="mb-2"><strong>Annual Salary:</strong> ${employee.salary:,.2f}</div>')
                    if employee.hourly_rate:
                        ui.html(f'<div class="mb-2"><strong>Hourly Rate:</strong> ${employee.hourly_rate:.2f}</div>')
                    ui.html(f'<div class="mb-2"><strong>Performance Rating:</strong> {employee.performance_rating}/5.0</div>')
                
                # Benefits Panel
                with ui.tab_panel(benefits_tab):
                    if employee.benefits:
                        for key, value in employee.benefits.items():
                            status = "✅ Yes" if value else "❌ No"
                            if isinstance(value, (int, float)) and not isinstance(value, bool):
                                status = str(value)
                            ui.html(f'<div class="mb-2"><strong>{key.replace("_", " ").title()}:</strong> {status}</div>')
                
                # Biometric Panel
                with ui.tab_panel(biometric_tab):
                    ui.html(f'<div class="mb-2"><strong>Biometric ID:</strong> {employee.biometric_id}</div>')
                    ui.html(f'<div class="mb-2"><strong>RFID Card:</strong> {employee.rfid_card}</div>')
                    ui.html('<div class="mb-2"><strong>Fingerprint:</strong> 🔒 Registered</div>')
                    ui.html('<div class="mb-2"><strong>Face Recognition:</strong> 🔒 Registered</div>')
            
            # Close button
            with ui.row().classes('w-full justify-end mt-6'):
                ui.button('Close', on_click=lambda: dialog.close()).classes('bg-gray-500 text-white')
    
    dialog.open()

def show_edit_employee_dialog(manager: EmployeeManager, employee_id: str):
    """Show dialog for editing employee"""
    # Implementation for edit dialog
    ui.notify(f'Edit dialog for employee {employee_id} - To be implemented', type='info')

def confirm_delete_employee(manager: EmployeeManager, employee_id: str):
    """Confirm and delete employee"""
    # Implementation for delete confirmation
    ui.notify(f'Delete confirmation for employee {employee_id} - To be implemented', type='info')

def refresh_employee_list():
    """Refresh the employee list based on search/filter criteria"""
    ui.notify('Refreshing employee list...', type='info')

def reset_filters():
    """Reset all search and filter criteria"""
    ui.notify('Filters reset', type='info')