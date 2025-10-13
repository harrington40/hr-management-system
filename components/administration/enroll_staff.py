from nicegui import ui, app
from helperFuns import imagePath, emailValidation
from assets import FlipCards, SearchBox
import asyncio
from datetime import datetime, date
import json
import uuid
import re

# Import institution data for integration
from .institution_profile import data_manager as institution_data_manager

# Advanced Employee Data Management System
class EmployeeDataManager:
    """
    Sophisticated employee enrollment system with validation algorithms,
    department integration, and automated employee ID generation
    """
    
    def __init__(self):
        self.employees = {}  # Store employee data
        self.next_employee_id = 1001  # Starting employee ID
        self.departments = [
            "Human Resources", "Information Technology", "Finance", 
            "Marketing", "Operations", "Sales", "Legal", "Administration"
        ]
        self.positions = {
            "Human Resources": ["HR Manager", "HR Specialist", "Recruiter", "Training Coordinator"],
            "Information Technology": ["Software Developer", "System Administrator", "IT Manager", "DevOps Engineer"],
            "Finance": ["Accountant", "Financial Analyst", "Finance Manager", "Payroll Specialist"],
            "Marketing": ["Marketing Manager", "Digital Marketer", "Content Creator", "Brand Manager"],
            "Operations": ["Operations Manager", "Process Analyst", "Quality Assurance", "Operations Coordinator"],
            "Sales": ["Sales Manager", "Sales Representative", "Account Manager", "Business Development"],
            "Legal": ["Legal Counsel", "Compliance Officer", "Legal Assistant", "Contract Manager"],
            "Administration": ["Administrative Assistant", "Office Manager", "Executive Assistant", "Receptionist"]
        }
        self.employment_types = ["Full-time", "Part-time", "Contract", "Temporary", "Intern"]
        self.salary_grades = ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6", "Grade 7", "Grade 8"]
        
        # Validation patterns
        self.validation_patterns = {
            "email": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            "phone": r'^\+?1?\d{9,15}$',
            "ssn": r'^\d{3}-\d{2}-\d{4}$',
            "employee_id": r'^EMP\d{4}$'
        }
    
    def generate_employee_id(self):
        """Generate unique employee ID with algorithm"""
        employee_id = f"EMP{self.next_employee_id}"
        self.next_employee_id += 1
        return employee_id
    
    def validate_employee_data(self, data):
        """Advanced validation algorithm for employee data"""
        errors = []
        
        # Required fields validation
        required_fields = ["first_name", "last_name", "email", "phone", "department", "position", "start_date"]
        for field in required_fields:
            if not data.get(field):
                errors.append(f"{field.replace('_', ' ').title()} is required")
        
        # Email validation
        if data.get("email") and not re.match(self.validation_patterns["email"], data["email"]):
            errors.append("Invalid email format")
        
        # Phone validation
        if data.get("phone") and not re.match(self.validation_patterns["phone"], data["phone"]):
            errors.append("Invalid phone number format")
        
        # SSN validation (if provided)
        if data.get("ssn") and not re.match(self.validation_patterns["ssn"], data["ssn"]):
            errors.append("Invalid SSN format (XXX-XX-XXXX)")
        
        # Date validation
        if data.get("start_date"):
            try:
                start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
                if start_date < date.today():
                    errors.append("Start date cannot be in the past")
            except ValueError:
                errors.append("Invalid start date format")
        
        # Department-Position validation
        if data.get("department") and data.get("position"):
            if data["position"] not in self.positions.get(data["department"], []):
                errors.append("Position is not valid for the selected department")
        
        return errors
    
    def create_employee_profile(self, data):
        """Create comprehensive employee profile with institutional integration"""
        # Validate data first
        validation_errors = self.validate_employee_data(data)
        if validation_errors:
            return False, validation_errors
        
        # Generate employee ID
        employee_id = self.generate_employee_id()
        
        # Get institution data for integration
        institution_data = institution_data_manager.get_institution_data()
        
        # Create comprehensive employee profile
        employee_profile = {
            "employee_id": employee_id,
            "personal_info": {
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "email": data["email"],
                "phone": data["phone"],
                "address": data.get("address", ""),
                "date_of_birth": data.get("date_of_birth", ""),
                "ssn": data.get("ssn", ""),
                "emergency_contact": data.get("emergency_contact", ""),
                "emergency_phone": data.get("emergency_phone", "")
            },
            "employment_info": {
                "department": data["department"],
                "position": data["position"],
                "employment_type": data["employment_type"],
                "start_date": data["start_date"],
                "salary_grade": data.get("salary_grade", ""),
                "reporting_manager": data.get("reporting_manager", ""),
                "work_location": data.get("work_location", institution_data["contact_info"]["headquarters"]),
                "status": "Active"
            },
            "system_info": {
                "created_date": datetime.now().isoformat(),
                "created_by": "HR System",
                "last_updated": datetime.now().isoformat(),
                "institution_id": institution_data["basic_info"]["registration_number"]
            }
        }
        
        # Store employee data
        self.employees[employee_id] = employee_profile
        
        # Update institution statistics
        self.update_institution_statistics()
        
        return True, employee_profile
    
    def update_institution_statistics(self):
        """Update institution employee count automatically"""
        new_count = len(self.employees)
        institution_data_manager.update_section("statistics", {"total_employees": new_count})
    
    def get_department_positions(self, department):
        """Get positions for a specific department"""
        return self.positions.get(department, [])
    
    def search_employees(self, query):
        """Advanced employee search algorithm"""
        results = []
        query_lower = query.lower()
        
        for emp_id, employee in self.employees.items():
            # Search in multiple fields
            searchable_text = f"{employee['personal_info']['first_name']} {employee['personal_info']['last_name']} {employee['personal_info']['email']} {employee['employment_info']['department']} {employee['employment_info']['position']} {emp_id}".lower()
            
            if query_lower in searchable_text:
                results.append(employee)
        
        return results

# Global employee data manager
employee_data_manager = EmployeeDataManager()

def EnrollNewStaff():
    """
    Modern Employee Enrollment page with advanced form handling,
    real-time validation, and institutional integration
    """
    
    # Page header with breadcrumb and actions
    with ui.row().classes('w-full justify-between items-center mb-6'):
        with ui.column():
            ui.label('Enroll New Staff').classes('text-3xl font-bold text-gray-800 dark:text-white')
            with ui.row().classes('items-center gap-2 text-sm text-gray-500'):
                ui.icon('home').classes('text-blue-500')
                ui.label('Dashboard')
                ui.icon('chevron_right').classes('text-xs')
                ui.label('Administration')
                ui.icon('chevron_right').classes('text-xs')
                ui.label('Enroll New Staff').classes('text-blue-600 font-medium')
        
        # Quick actions
        with ui.row().classes('gap-2'):
            ui.button('Import Employees', icon='upload', on_click=import_employees).props('outlined color=blue')
            ui.button('Employee Directory', icon='people', on_click=view_employee_directory).props('outlined color=green')
    
    # Institution integration info
    create_institution_integration_banner()
    
    # Main enrollment form with tabs
    with ui.tabs().classes('w-full mb-4') as tabs:
        personal_tab = ui.tab('Personal Information', icon='person')
        employment_tab = ui.tab('Employment Details', icon='work')
        contact_tab = ui.tab('Contact & Emergency', icon='contact_phone')
        review_tab = ui.tab('Review & Submit', icon='check_circle')
    
    # Form data storage
    form_data = {}
    
    with ui.tab_panels(tabs, value=personal_tab).classes('w-full'):
        # Personal Information Panel
        with ui.tab_panel(personal_tab):
            create_personal_info_section(form_data, tabs, employment_tab)
        
        # Employment Details Panel
        with ui.tab_panel(employment_tab):
            create_employment_details_section(form_data, tabs, contact_tab)
        
        # Contact & Emergency Panel
        with ui.tab_panel(contact_tab):
            create_contact_emergency_section(form_data, tabs, review_tab)
        
        # Review & Submit Panel
        with ui.tab_panel(review_tab):
            create_review_submit_section(form_data, tabs, personal_tab)

def create_institution_integration_banner():
    """Create integration banner showing institution connection"""
    institution_data = institution_data_manager.get_institution_data()
    
    with ui.card().classes('w-full p-4 mb-6 bg-gradient-to-r from-blue-50 to-indigo-50 border-l-4 border-blue-500'):
        with ui.row().classes('items-center justify-between w-full'):
            with ui.row().classes('items-center gap-4'):
                ui.icon('business').classes('text-3xl text-blue-600')
                with ui.column():
                    ui.label(f'Enrolling to: {institution_data["basic_info"]["name"]}').classes('text-lg font-semibold text-gray-800')
                    ui.label(f'Total Employees: {institution_data["statistics"]["total_employees"]} | Departments: {institution_data["statistics"]["departments"]}').classes('text-sm text-gray-600')
            
            with ui.row().classes('gap-2'):
                ui.chip('Active Institution', color='green').props('dense')
                ui.button('View Institution', icon='visibility', on_click=lambda: ui.navigate.to('/administration/institution')).props('flat dense color=blue')

def create_personal_info_section(form_data, tabs, next_tab):
    """Create personal information form section"""
    with ui.card().classes('w-full p-6'):
        ui.label('Personal Information').classes('text-xl font-semibold mb-4 text-gray-800')
        
        with ui.grid(columns=2).classes('gap-6 w-full'):
            # Left column
            with ui.column().classes('gap-4'):
                first_name = ui.input('First Name *', placeholder='Enter first name').classes('w-full').props('outlined dense')
                last_name = ui.input('Last Name *', placeholder='Enter last name').classes('w-full').props('outlined dense')
                
                with ui.input('Date of Birth').classes('w-full').props('outlined dense'):
                    ui.date()
                
                gender = ui.select(['Male', 'Female', 'Other', 'Prefer not to say'], 
                                 label='Gender').classes('w-full').props('outlined dense')
            
            # Right column
            with ui.column().classes('gap-4'):
                email = ui.input('Email Address *', placeholder='john.doe@company.com').classes('w-full').props('outlined dense type=email')
                phone = ui.input('Phone Number *', placeholder='+1 (555) 123-4567').classes('w-full').props('outlined dense')
                ssn = ui.input('SSN', placeholder='XXX-XX-XXXX').classes('w-full').props('outlined dense')
                ui.textarea('Address', placeholder='Street address, City, State, ZIP').classes('w-full').props('outlined dense rows=3')
        
        # Navigation and validation
        with ui.row().classes('justify-end gap-2 mt-6'):
            validate_btn = ui.button('Validate & Continue', icon='arrow_forward', 
                                    on_click=lambda: validate_personal_info(form_data, first_name, last_name, email, phone, ssn, tabs, next_tab)).props('color=primary')

def create_employment_details_section(form_data, tabs, next_tab):
    """Create employment details form section"""
    with ui.card().classes('w-full p-6'):
        ui.label('Employment Details').classes('text-xl font-semibold mb-4 text-gray-800')
        
        with ui.grid(columns=2).classes('gap-6 w-full'):
            # Left column
            with ui.column().classes('gap-4'):
                department = ui.select(employee_data_manager.departments, 
                                     label='Department *').classes('w-full').props('outlined dense')
                position = ui.select([], label='Position *').classes('w-full').props('outlined dense')
                
                # Dynamic position loading based on department
                department.on('update:model-value', lambda e: update_positions(position, e.args))
                
                employment_type = ui.select(employee_data_manager.employment_types, 
                                          label='Employment Type *').classes('w-full').props('outlined dense')
                
                with ui.input('Start Date *').classes('w-full').props('outlined dense'):
                    start_date = ui.date()
            
            # Right column
            with ui.column().classes('gap-4'):
                salary_grade = ui.select(employee_data_manager.salary_grades, 
                                       label='Salary Grade').classes('w-full').props('outlined dense')
                reporting_manager = ui.input('Reporting Manager', placeholder='Manager name').classes('w-full').props('outlined dense')
                work_location = ui.input('Work Location', placeholder='Office location').classes('w-full').props('outlined dense')
                
                # Employee ID preview
                with ui.card().classes('p-3 bg-gray-50'):
                    ui.label('Employee ID (Auto-generated)').classes('text-sm text-gray-600')
                    ui.label(employee_data_manager.generate_employee_id()).classes('text-lg font-mono font-bold text-blue-600')
        
        # Navigation
        with ui.row().classes('justify-between mt-6'):
            ui.button('Previous', icon='arrow_back', 
                     on_click=lambda: tabs.set_value(tabs.tabs[0])).props('outlined')
            ui.button('Continue', icon='arrow_forward', 
                     on_click=lambda: save_employment_details(form_data, department, position, employment_type, start_date, salary_grade, reporting_manager, work_location, tabs, next_tab)).props('color=primary')

def create_contact_emergency_section(form_data, tabs, next_tab):
    """Create contact and emergency information section"""
    with ui.card().classes('w-full p-6'):
        ui.label('Contact & Emergency Information').classes('text-xl font-semibold mb-4 text-gray-800')
        
        with ui.grid(columns=2).classes('gap-6 w-full'):
            # Emergency Contact column
            with ui.column().classes('gap-4'):
                ui.label('Emergency Contact').classes('text-lg font-medium text-gray-700 mb-2')
                emergency_name = ui.input('Emergency Contact Name', placeholder='Full name').classes('w-full').props('outlined dense')
                emergency_relationship = ui.select(['Spouse', 'Parent', 'Sibling', 'Child', 'Friend', 'Other'], 
                                                 label='Relationship').classes('w-full').props('outlined dense')
                emergency_phone = ui.input('Emergency Phone', placeholder='+1 (555) 123-4567').classes('w-full').props('outlined dense')
                emergency_email = ui.input('Emergency Email', placeholder='emergency@email.com').classes('w-full').props('outlined dense type=email')
            
            # Additional Information column
            with ui.column().classes('gap-4'):
                ui.label('Additional Information').classes('text-lg font-medium text-gray-700 mb-2')
                preferred_name = ui.input('Preferred Name', placeholder='Nickname or preferred name').classes('w-full').props('outlined dense')
                
                # Skills and certifications
                ui.textarea('Skills & Certifications', placeholder='List relevant skills and certifications').classes('w-full').props('outlined dense rows=3')
                
                # Special accommodations
                ui.textarea('Special Accommodations', placeholder='Any workplace accommodations needed').classes('w-full').props('outlined dense rows=2')
        
        # Navigation
        with ui.row().classes('justify-between mt-6'):
            ui.button('Previous', icon='arrow_back', 
                     on_click=lambda: tabs.set_value(tabs.tabs[1])).props('outlined')
            ui.button('Continue to Review', icon='arrow_forward', 
                     on_click=lambda: save_contact_info(form_data, emergency_name, emergency_relationship, emergency_phone, emergency_email, preferred_name, tabs, next_tab)).props('color=primary')

def create_review_submit_section(form_data, tabs, first_tab):
    """Create review and submit section"""
    with ui.card().classes('w-full p-6'):
        ui.label('Review Employee Information').classes('text-xl font-semibold mb-4 text-gray-800')
        
        # Review summary will be populated dynamically
        review_container = ui.column().classes('w-full gap-4')
        
        # Action buttons
        with ui.row().classes('justify-between mt-6'):
            with ui.row().classes('gap-2'):
                ui.button('Back to Edit', icon='edit', 
                         on_click=lambda: tabs.set_value(first_tab)).props('outlined')
                ui.button('Save as Draft', icon='save', 
                         on_click=lambda: save_as_draft(form_data)).props('outlined color=orange')
            
            ui.button('Enroll Employee', icon='person_add', 
                     on_click=lambda: submit_enrollment(form_data, review_container)).props('color=success size=lg')

# Helper functions for form handling
def validate_personal_info(form_data, first_name, last_name, email, phone, ssn, tabs, next_tab):
    """Validate personal information and move to next tab"""
    # Store form data
    form_data.update({
        'first_name': first_name.value,
        'last_name': last_name.value,
        'email': email.value,
        'phone': phone.value,
        'ssn': ssn.value
    })
    
    # Basic validation
    errors = []
    if not first_name.value:
        errors.append("First name is required")
    if not last_name.value:
        errors.append("Last name is required")
    if not email.value:
        errors.append("Email is required")
    elif not emailValidation(email.value):
        errors.append("Invalid email format")
    if not phone.value:
        errors.append("Phone number is required")
    
    if errors:
        ui.notify('\n'.join(errors), color='negative')
        return
    
    ui.notify('Personal information validated successfully!', color='positive')
    tabs.set_value(next_tab)

def update_positions(position_select, department_value):
    """Update position options based on selected department"""
    if department_value:
        positions = employee_data_manager.get_department_positions(department_value)
        position_select.set_options(positions)
        position_select.set_value(None)

def save_employment_details(form_data, department, position, employment_type, start_date, salary_grade, reporting_manager, work_location, tabs, next_tab):
    """Save employment details and continue"""
    form_data.update({
        'department': department.value,
        'position': position.value,
        'employment_type': employment_type.value,
        'start_date': start_date.value,
        'salary_grade': salary_grade.value,
        'reporting_manager': reporting_manager.value,
        'work_location': work_location.value
    })
    
    # Validation
    if not all([department.value, position.value, employment_type.value, start_date.value]):
        ui.notify('Please fill in all required employment fields', color='negative')
        return
    
    ui.notify('Employment details saved!', color='positive')
    tabs.set_value(next_tab)

def save_contact_info(form_data, emergency_name, emergency_relationship, emergency_phone, emergency_email, preferred_name, tabs, next_tab):
    """Save contact information and continue"""
    form_data.update({
        'emergency_contact': emergency_name.value,
        'emergency_relationship': emergency_relationship.value,
        'emergency_phone': emergency_phone.value,
        'emergency_email': emergency_email.value,
        'preferred_name': preferred_name.value
    })
    
    ui.notify('Contact information saved!', color='positive')
    tabs.set_value(next_tab)
    
    # Update review section
    update_review_section(form_data)

def update_review_section(form_data):
    """Update the review section with current form data"""
    # This would be called to refresh the review section
    # Implementation would populate the review_container with form data
    pass

async def submit_enrollment(form_data, review_container):
    """Submit the employee enrollment"""
    ui.notify('Processing employee enrollment...', color='info')
    
    # Simulate processing time
    await asyncio.sleep(2)
    
    # Create employee profile
    success, result = employee_data_manager.create_employee_profile(form_data)
    
    if success:
        employee_profile = result
        ui.notify(f'Employee enrolled successfully! ID: {employee_profile["employee_id"]}', color='positive')
        
        # Show success dialog
        with ui.dialog() as dialog, ui.card():
            ui.label('Employee Enrollment Successful!').classes('text-xl font-bold text-green-600')
            ui.separator()
            ui.label(f'Employee ID: {employee_profile["employee_id"]}').classes('text-lg font-mono')
            ui.label(f'Name: {employee_profile["personal_info"]["first_name"]} {employee_profile["personal_info"]["last_name"]}').classes('text-lg')
            ui.label(f'Department: {employee_profile["employment_info"]["department"]}').classes('text-lg')
            ui.label(f'Position: {employee_profile["employment_info"]["position"]}').classes('text-lg')
            
            with ui.row().classes('gap-2 mt-4'):
                ui.button('Print Profile', icon='print').props('color=blue')
                ui.button('Send Welcome Email', icon='email').props('color=green')
                ui.button('Close', on_click=dialog.close).props('color=primary')
        
        dialog.open()
    else:
        errors = result
        ui.notify(f'Enrollment failed: {", ".join(errors)}', color='negative')

async def save_as_draft(form_data):
    """Save employee enrollment as draft"""
    ui.notify('Saving as draft...', color='info')
    await asyncio.sleep(1)
    ui.notify('Draft saved successfully!', color='positive')

async def import_employees():
    """Handle bulk employee import"""
    ui.notify('Import feature coming soon!', color='info')

async def view_employee_directory():
    """Navigate to employee directory"""
    ui.notify('Navigating to employee directory...', color='info')
    # ui.navigate.to('/employees/directory')

# API functions for integration with other modules
def get_employee_data(employee_id):
    """API to get employee data for other modules"""
    return employee_data_manager.employees.get(employee_id)

def get_department_employees(department):
    """API to get all employees in a department"""
    return [emp for emp in employee_data_manager.employees.values() 
            if emp['employment_info']['department'] == department]

def get_employee_statistics():
    """API to get employee statistics for dashboard"""
    total_employees = len(employee_data_manager.employees)
    departments = employee_data_manager.departments
    active_employees = len([emp for emp in employee_data_manager.employees.values() 
                           if emp['employment_info']['status'] == 'Active'])
    
    return {
        'total_employees': total_employees,
        'active_employees': active_employees,
        'departments': len(departments),
        'recent_hires': 0  # Could be calculated based on start dates
    }
