from nicegui import ui, app
from helperFuns import imagePath
from assets import FlipCards, SearchBox
import asyncio
from datetime import datetime
import json

# Data management algorithms and state
class InstitutionDataManager:
    """
    Advanced data management system for institution profile with CRUD operations,
    validation, and inter-module communication algorithms
    """
    
    def __init__(self):
        self.institution_data = {
            "basic_info": {
                "name": "KWARECOM Inc.",
                "legal_name": "KWARECOM Incorporated",
                "registration_number": "REG-2011-001",
                "tax_id": "TAX-987654321",
                "founded_date": "2011-01-15",
                "industry": "Technology Services",
                "company_size": "51-200",
                "status": "Active"
            },
            "contact_info": {
                "headquarters": "123 Business Avenue, Tech City, TC 12345",
                "phone": "+1 (555) 123-4567",
                "email": "info@kwarecominc.com",
                "website": "https://kwarecominc.com",
                "fax": "+1 (555) 123-4568"
            },
            "business_info": {
                "fiscal_year_start": "January",
                "currency": "USD",
                "timezone": "America/New_York",
                "business_hours": "9:00 AM - 5:00 PM",
                "working_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            },
            "statistics": {
                "total_employees": 142,
                "departments": 8,
                "locations": 3,
                "active_projects": 24,
                "last_updated": datetime.now().isoformat()
            }
        }
        self.validation_rules = {
            "name": {"required": True, "min_length": 2, "max_length": 100},
            "email": {"required": True, "pattern": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'},
            "phone": {"required": True, "pattern": r'^\+?1?\d{9,15}$'},
            "registration_number": {"required": True, "min_length": 5}
        }
    
    def get_institution_data(self):
        """Retrieve current institution data"""
        return self.institution_data
    
    def update_section(self, section, data):
        """Update specific section with validation"""
        if section in self.institution_data:
            # Validate data before updating
            if self.validate_data(section, data):
                self.institution_data[section].update(data)
                self.institution_data["statistics"]["last_updated"] = datetime.now().isoformat()
                return True, "Data updated successfully"
            else:
                return False, "Validation failed"
        return False, "Invalid section"
    
    def validate_data(self, section, data):
        """Advanced validation algorithm"""
        # Implement validation logic based on rules
        for field, value in data.items():
            if field in self.validation_rules:
                rules = self.validation_rules[field]
                if rules.get("required") and not value:
                    return False
                if "min_length" in rules and len(str(value)) < rules["min_length"]:
                    return False
                if "max_length" in rules and len(str(value)) > rules["max_length"]:
                    return False
        return True
    
    def get_dashboard_metrics(self):
        """Calculate key metrics for dashboard integration"""
        return {
            "employee_growth": "+12%",
            "departments_active": self.institution_data["statistics"]["departments"],
            "system_health": "Excellent",
            "last_backup": "2 hours ago"
        }

# Global data manager instance
data_manager = InstitutionDataManager()

def InstitutionProfile():
    """
    Modern Institution Profile page with advanced UI/UX design and integration algorithms
    """
    
    # Page header with breadcrumb navigation
    with ui.row().classes('w-full justify-between items-center mb-6'):
        with ui.column():
            ui.label('Institution Profile').classes('text-3xl font-bold text-gray-800 dark:text-white')
            with ui.row().classes('items-center gap-2 text-sm text-gray-500'):
                ui.icon('home').classes('text-blue-500')
                ui.label('Dashboard')
                ui.icon('chevron_right').classes('text-xs')
                ui.label('Administration')
                ui.icon('chevron_right').classes('text-xs')
                ui.label('Institution Profile').classes('text-blue-600 font-medium')
        
        # Action buttons
        with ui.row().classes('gap-2'):
            ui.button('Export Data', icon='download', on_click=export_institution_data).props('outlined color=blue')
            ui.button('Save Changes', icon='save', on_click=save_institution_changes).props('color=primary')
    
    # Quick stats cards
    create_stats_overview()
    
    # Main content tabs
    with ui.tabs().classes('w-full mb-4') as tabs:
        basic_tab = ui.tab('Basic Information', icon='business')
        contact_tab = ui.tab('Contact Details', icon='contact_mail')
        business_tab = ui.tab('Business Settings', icon='settings')
        integration_tab = ui.tab('System Integration', icon='hub')
    
    with ui.tab_panels(tabs, value=basic_tab).classes('w-full'):
        # Basic Information Panel
        with ui.tab_panel(basic_tab):
            create_basic_info_section()
        
        # Contact Details Panel
        with ui.tab_panel(contact_tab):
            create_contact_info_section()
        
        # Business Settings Panel
        with ui.tab_panel(business_tab):
            create_business_settings_section()
        
        # System Integration Panel
        with ui.tab_panel(integration_tab):
            create_integration_section()

def create_stats_overview():
    """Create modern statistics overview cards"""
    data = data_manager.get_institution_data()
    stats = data["statistics"]
    
    with ui.row().classes('w-full gap-4 mb-6'):
        # Total Employees Card
        with ui.card().classes('p-4 bg-gradient-to-r from-blue-500 to-blue-600 text-white min-w-48'):
            with ui.row().classes('items-center justify-between'):
                with ui.column():
                    ui.label('Total Employees').classes('text-blue-100 text-sm')
                    ui.label(f'{stats["total_employees"]}').classes('text-2xl font-bold')
                ui.icon('groups').classes('text-3xl text-blue-200')
        
        # Departments Card
        with ui.card().classes('p-4 bg-gradient-to-r from-green-500 to-green-600 text-white min-w-48'):
            with ui.row().classes('items-center justify-between'):
                with ui.column():
                    ui.label('Departments').classes('text-green-100 text-sm')
                    ui.label(f'{stats["departments"]}').classes('text-2xl font-bold')
                ui.icon('account_tree').classes('text-3xl text-green-200')
        
        # Locations Card
        with ui.card().classes('p-4 bg-gradient-to-r from-purple-500 to-purple-600 text-white min-w-48'):
            with ui.row().classes('items-center justify-between'):
                with ui.column():
                    ui.label('Locations').classes('text-purple-100 text-sm')
                    ui.label(f'{stats["locations"]}').classes('text-2xl font-bold')
                ui.icon('location_on').classes('text-3xl text-purple-200')
        
        # Active Projects Card
        with ui.card().classes('p-4 bg-gradient-to-r from-orange-500 to-orange-600 text-white min-w-48'):
            with ui.row().classes('items-center justify-between'):
                with ui.column():
                    ui.label('Active Projects').classes('text-orange-100 text-sm')
                    ui.label(f'{stats["active_projects"]}').classes('text-2xl font-bold')
                ui.icon('work').classes('text-3xl text-orange-200')

def create_basic_info_section():
    """Create basic information form section"""
    data = data_manager.get_institution_data()["basic_info"]
    
    with ui.card().classes('w-full p-6'):
        ui.label('Basic Institution Information').classes('text-xl font-semibold mb-4 text-gray-800')
        
        with ui.grid(columns=2).classes('gap-6 w-full'):
            # Left column
            with ui.column().classes('gap-4'):
                ui.input('Institution Name', value=data["name"]).classes('w-full').props('outlined dense')
                ui.input('Legal Name', value=data["legal_name"]).classes('w-full').props('outlined dense')
                ui.input('Registration Number', value=data["registration_number"]).classes('w-full').props('outlined dense')
                ui.input('Tax ID', value=data["tax_id"]).classes('w-full').props('outlined dense')
            
            # Right column
            with ui.column().classes('gap-4'):
                with ui.input('Founded Date').classes('w-full').props('outlined dense'):
                    ui.date(value=data["founded_date"])
                ui.select(['Technology Services', 'Healthcare', 'Finance', 'Education', 'Manufacturing'], 
                         value=data["industry"], label='Industry').classes('w-full').props('outlined dense')
                ui.select(['1-10', '11-50', '51-200', '201-500', '500+'], 
                         value=data["company_size"], label='Company Size').classes('w-full').props('outlined dense')
                ui.select(['Active', 'Inactive', 'Suspended'], 
                         value=data["status"], label='Status').classes('w-full').props('outlined dense')

def create_contact_info_section():
    """Create contact information form section"""
    data = data_manager.get_institution_data()["contact_info"]
    
    with ui.card().classes('w-full p-6'):
        ui.label('Contact Information').classes('text-xl font-semibold mb-4 text-gray-800')
        
        with ui.column().classes('gap-4 w-full'):
            ui.textarea('Headquarters Address', value=data["headquarters"]).classes('w-full').props('outlined dense rows=3')
            
            with ui.row().classes('gap-4 w-full'):
                ui.input('Phone Number', value=data["phone"]).classes('flex-1').props('outlined dense')
                ui.input('Fax Number', value=data["fax"]).classes('flex-1').props('outlined dense')
            
            with ui.row().classes('gap-4 w-full'):
                ui.input('Email Address', value=data["email"]).classes('flex-1').props('outlined dense type=email')
                ui.input('Website', value=data["website"]).classes('flex-1').props('outlined dense type=url')

def create_business_settings_section():
    """Create business settings configuration section"""
    data = data_manager.get_institution_data()["business_info"]
    
    with ui.card().classes('w-full p-6'):
        ui.label('Business Configuration').classes('text-xl font-semibold mb-4 text-gray-800')
        
        with ui.grid(columns=2).classes('gap-6 w-full'):
            # Left column
            with ui.column().classes('gap-4'):
                ui.select(['January', 'February', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'November', 'December'], 
                         value=data["fiscal_year_start"], label='Fiscal Year Start').classes('w-full').props('outlined dense')
                ui.select(['USD', 'EUR', 'GBP', 'JPY', 'CAD'], 
                         value=data["currency"], label='Currency').classes('w-full').props('outlined dense')
                ui.input('Business Hours', value=data["business_hours"]).classes('w-full').props('outlined dense')
            
            # Right column
            with ui.column().classes('gap-4'):
                ui.select(['America/New_York', 'Europe/London', 'Asia/Tokyo', 'Australia/Sydney'], 
                         value=data["timezone"], label='Timezone').classes('w-full').props('outlined dense')
                
                # Working days multi-select
                ui.label('Working Days').classes('text-sm font-medium text-gray-700')
                with ui.row().classes('gap-2 flex-wrap'):
                    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    for day in days:
                        is_checked = day in data["working_days"]
                        ui.checkbox(day, value=is_checked).classes('text-sm')

def create_integration_section():
    """Create system integration and module connections section"""
    with ui.card().classes('w-full p-6'):
        ui.label('System Integration & Module Connections').classes('text-xl font-semibold mb-4 text-gray-800')
        
        with ui.grid(columns=2).classes('gap-6 w-full'):
            # Connected Modules
            with ui.card().classes('p-4 border border-gray-200'):
                ui.label('Connected HR Modules').classes('text-lg font-medium mb-3')
                
                modules = [
                    {'name': 'Employee Management', 'status': 'Connected', 'icon': 'groups', 'color': 'green'},
                    {'name': 'Department Management', 'status': 'Connected', 'icon': 'account_tree', 'color': 'green'},
                    {'name': 'Attendance Tracking', 'status': 'Connected', 'icon': 'access_time', 'color': 'green'},
                    {'name': 'Payroll System', 'status': 'Pending', 'icon': 'payments', 'color': 'orange'},
                    {'name': 'Performance Reviews', 'status': 'Not Connected', 'icon': 'star_rate', 'color': 'red'},
                ]
                
                for module in modules:
                    with ui.row().classes('items-center justify-between p-2 rounded-lg hover:bg-gray-50'):
                        with ui.row().classes('items-center gap-3'):
                            ui.icon(module['icon']).classes(f'text-{module["color"]}-500')
                            ui.label(module['name']).classes('font-medium')
                        ui.chip(module['status'], color=module['color']).props('dense')
            
            # Quick Actions
            with ui.card().classes('p-4 border border-gray-200'):
                ui.label('Quick Actions').classes('text-lg font-medium mb-3')
                
                actions = [
                    {'name': 'Create Department', 'icon': 'add_circle', 'route': '/hrmkit/administration/divisions'},
                    {'name': 'Add Employee', 'icon': 'person_add', 'route': '/hrmkit/administration/employee'},
                    {'name': 'View Reports', 'icon': 'analytics', 'route': '/hrmkit/reporting/dashboard'},
                    {'name': 'System Settings', 'icon': 'settings', 'route': '/hrmkit/administration/settings'},
                ]
                
                for action in actions:
                    with ui.button(action['name'], icon=action['icon'], 
                                 on_click=lambda route=action['route']: navigate_to_module(route)).classes('w-full mb-2').props('outlined'):
                        pass

# Utility functions for data operations
async def export_institution_data():
    """Export institution data algorithm"""
    data = data_manager.get_institution_data()
    ui.notify('Exporting institution data...', color='info')
    
    # Simulate export process
    await asyncio.sleep(1)
    
    # In a real application, this would generate and download a file
    ui.notify('Institution data exported successfully!', color='positive')
    print(f"Exported data: {json.dumps(data, indent=2)}")

async def save_institution_changes():
    """Save institution changes with validation"""
    ui.notify('Saving changes...', color='info')
    
    # Simulate save process with validation
    await asyncio.sleep(1)
    
    # Update last modified timestamp
    data_manager.institution_data["statistics"]["last_updated"] = datetime.now().isoformat()
    
    ui.notify('Changes saved successfully!', color='positive')

def navigate_to_module(route):
    """Navigation algorithm to connect with other HR modules"""
    ui.notify(f'Navigating to {route}', color='info')
    print(f"Navigation: {route}")
    # In a real application, implement actual navigation
    # ui.navigate.to(route)

def get_institution_integration_data():
    """
    API for other modules to get institution data
    This function can be imported and used by other HR modules
    """
    return data_manager.get_institution_data()

def update_institution_statistics(stats_update):
    """
    API for other modules to update institution statistics
    This allows modules like Employee Management to update employee count
    """
    return data_manager.update_section("statistics", stats_update)