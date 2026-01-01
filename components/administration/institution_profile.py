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
        """Retrieve current institution data with dynamic statistics"""
        # Get current employee statistics
        try:
            from components.administration.enroll_staff import get_employee_statistics
            current_stats = get_employee_statistics()
            
            # Update the statistics section with current data
            self.institution_data["statistics"].update({
                "total_employees": current_stats["total_employees"],
                "last_updated": datetime.now().isoformat()
            })
        except Exception as e:
            print(f"Warning: Could not get current employee statistics: {e}")
        
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

    # Modern Hero Section with Company Branding
    with ui.element('div').classes('relative overflow-hidden bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-700 rounded-2xl mb-8 shadow-2xl'):
        with ui.element('div').classes('absolute inset-0 bg-black bg-opacity-20'):
            # Background pattern
            ui.html('<div class="absolute inset-0 opacity-10"><svg width="100%" height="100%"><defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M 40 0 L 0 0 0 40" fill="none" stroke="white" stroke-width="1"/></pattern></defs><rect width="100%" height="100%" fill="url(#grid)"/></svg></div>', sanitize=False)

        with ui.element('div').classes('relative z-10 p-8 text-white'):
            with ui.row().classes('justify-between items-start'):
                # Company Info Section
                with ui.column().classes('flex-1'):
                    with ui.row().classes('items-center gap-4 mb-4'):
                        ui.html('<div class="text-6xl">🏢</div>', sanitize=False)
                        with ui.column():
                            ui.html('<h1 class="text-4xl font-bold mb-2">Institution Profile</h1>', sanitize=False)
                            ui.html('<p class="text-blue-100 text-lg">Manage your organization\'s core information and settings</p>', sanitize=False)

                    # Key Metrics Row
                    with ui.row().classes('gap-6 mt-6'):
                        metrics = [
                            {'label': 'Founded', 'value': '2011', 'icon': '🎯'},
                            {'label': 'Employees', 'value': '142', 'icon': '👥'},
                            {'label': 'Departments', 'value': '8', 'icon': '🏗️'},
                            {'label': 'Status', 'value': 'Active', 'icon': '✅'}
                        ]
                        for metric in metrics:
                            with ui.element('div').classes('text-center'):
                                ui.html(f'<div class="text-2xl mb-1">{metric["icon"]}</div>', sanitize=False)
                                ui.html(f'<div class="text-2xl font-bold">{metric["value"]}</div>', sanitize=False)
                                ui.html(f'<div class="text-sm text-blue-100">{metric["label"]}</div>', sanitize=False)

                # Action Buttons
                with ui.column().classes('gap-3'):
                    ui.button('⚡ Quick Actions', icon='bolt').classes('bg-white text-blue-600 hover:bg-blue-50 font-semibold px-6 py-3 rounded-xl shadow-lg transition-all duration-300')
                    ui.button('📊 View Reports', icon='analytics').classes('bg-blue-500 text-white hover:bg-blue-400 font-semibold px-6 py-3 rounded-xl shadow-lg transition-all duration-300').props('outlined')
                    ui.button('🔧 Settings', icon='settings').classes('bg-transparent text-white border-2 border-white hover:bg-white hover:text-blue-600 font-semibold px-6 py-3 rounded-xl transition-all duration-300')

    # Modern Stats Overview Cards
    create_modern_stats_overview()

    # Main Content with Modern Card Layout
    with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-3 gap-8'):

        # Primary Information Card (Spans 2 columns)
        with ui.element('div').classes('lg:col-span-2 space-y-6'):
            create_modern_basic_info_card()
            create_modern_contact_card()

        # Secondary Information Card (Spans 1 column)
        with ui.element('div').classes('space-y-6'):
            create_modern_business_settings_card()
            create_modern_integration_card()

def create_modern_stats_overview():
    """Create modern statistics overview cards with enhanced visual design"""
    data = data_manager.get_institution_data()
    stats = data["statistics"]

    with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8'):

        # Total Employees Card
        with ui.element('div').classes('group relative overflow-hidden bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl p-6 text-white shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:scale-105 cursor-pointer'):
            with ui.element('div').classes('absolute top-0 right-0 w-20 h-20 bg-white bg-opacity-10 rounded-full -mr-10 -mt-10'):
                pass
            with ui.element('div').classes('relative z-10'):
                with ui.row().classes('justify-between items-start mb-4'):
                    ui.html('<div class="text-3xl">👥</div>', sanitize=False)
                    ui.html('<div class="text-blue-200 text-sm font-medium">Employees</div>', sanitize=False)
                ui.html(f'<div class="text-4xl font-bold mb-2">{stats["total_employees"]}</div>', sanitize=False)
                ui.html('<div class="text-blue-100 text-sm">↗️ +12% this quarter</div>', sanitize=False)

        # Departments Card
        with ui.element('div').classes('group relative overflow-hidden bg-gradient-to-br from-emerald-500 to-green-600 rounded-2xl p-6 text-white shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:scale-105 cursor-pointer'):
            with ui.element('div').classes('absolute top-0 right-0 w-20 h-20 bg-white bg-opacity-10 rounded-full -mr-10 -mt-10'):
                pass
            with ui.element('div').classes('relative z-10'):
                with ui.row().classes('justify-between items-start mb-4'):
                    ui.html('<div class="text-3xl">🏗️</div>', sanitize=False)
                    ui.html('<div class="text-emerald-200 text-sm font-medium">Departments</div>', sanitize=False)
                ui.html(f'<div class="text-4xl font-bold mb-2">{stats["departments"]}</div>', sanitize=False)
                ui.html('<div class="text-emerald-100 text-sm">All active</div>', sanitize=False)

        # Locations Card
        with ui.element('div').classes('group relative overflow-hidden bg-gradient-to-br from-purple-500 to-indigo-600 rounded-2xl p-6 text-white shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:scale-105 cursor-pointer'):
            with ui.element('div').classes('absolute top-0 right-0 w-20 h-20 bg-white bg-opacity-10 rounded-full -mr-10 -mt-10'):
                pass
            with ui.element('div').classes('relative z-10'):
                with ui.row().classes('justify-between items-start mb-4'):
                    ui.html('<div class="text-3xl">📍</div>', sanitize=False)
                    ui.html('<div class="text-purple-200 text-sm font-medium">Locations</div>', sanitize=False)
                ui.html(f'<div class="text-4xl font-bold mb-2">{stats["locations"]}</div>', sanitize=False)
                ui.html('<div class="text-purple-100 text-sm">Multi-site</div>', sanitize=False)

        # Active Projects Card
        with ui.element('div').classes('group relative overflow-hidden bg-gradient-to-br from-orange-500 to-red-500 rounded-2xl p-6 text-white shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:scale-105 cursor-pointer'):
            with ui.element('div').classes('absolute top-0 right-0 w-20 h-20 bg-white bg-opacity-10 rounded-full -mr-10 -mt-10'):
                pass
            with ui.element('div').classes('relative z-10'):
                with ui.row().classes('justify-between items-start mb-4'):
                    ui.html('<div class="text-3xl">🚀</div>', sanitize=False)
                    ui.html('<div class="text-orange-200 text-sm font-medium">Projects</div>', sanitize=False)
                ui.html(f'<div class="text-4xl font-bold mb-2">{stats["active_projects"]}</div>', sanitize=False)
                ui.html('<div class="text-orange-100 text-sm">In progress</div>', sanitize=False)

def create_modern_basic_info_card():
    """Create modern basic information card with professional styling"""
    data = data_manager.get_institution_data()["basic_info"]

    with ui.element('div').classes('bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden hover:shadow-2xl transition-all duration-300'):
        # Card Header
        with ui.element('div').classes('bg-gradient-to-r from-blue-600 to-indigo-600 p-6 text-white'):
            with ui.row().classes('items-center gap-4'):
                ui.html('<div class="text-3xl">🏢</div>', sanitize=False)
                with ui.column():
                    ui.html('<h3 class="text-xl font-bold">Basic Information</h3>', sanitize=False)
                    ui.html('<p class="text-blue-100 text-sm">Core company details and registration</p>', sanitize=False)

        # Card Content
        with ui.element('div').classes('p-6'):
            with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 gap-6'):

                # Left Column
                with ui.element('div').classes('space-y-4'):
                    # Institution Name
                    with ui.element('div').classes('group'):
                        ui.html('<label class="block text-sm font-semibold text-gray-700 mb-2">Institution Name</label>', sanitize=False)
                        ui.input(value=data["name"]).classes('w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 hover:border-blue-400').props('outlined dense')

                    # Legal Name
                    with ui.element('div').classes('group'):
                        ui.html('<label class="block text-sm font-semibold text-gray-700 mb-2">Legal Name</label>', sanitize=False)
                        ui.input(value=data["legal_name"]).classes('w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 hover:border-blue-400').props('outlined dense')

                    # Registration Number
                    with ui.element('div').classes('group'):
                        ui.html('<label class="block text-sm font-semibold text-gray-700 mb-2">Registration Number</label>', sanitize=False)
                        ui.input(value=data["registration_number"]).classes('w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 hover:border-blue-400').props('outlined dense')

                # Right Column
                with ui.element('div').classes('space-y-4'):
                    # Founded Date
                    with ui.element('div').classes('group'):
                        ui.html('<label class="block text-sm font-semibold text-gray-700 mb-2">Founded Date</label>', sanitize=False)
                        with ui.input().classes('w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 hover:border-blue-400').props('outlined dense'):
                            ui.date(value=data["founded_date"])

                    # Industry
                    with ui.element('div').classes('group'):
                        ui.html('<label class="block text-sm font-semibold text-gray-700 mb-2">Industry</label>', sanitize=False)
                        ui.select(['Technology Services', 'Healthcare', 'Finance', 'Education', 'Manufacturing', 'Retail', 'Consulting'],
                                 value=data["industry"]).classes('w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 hover:border-blue-400').props('outlined dense')

                    # Company Size & Status Row
                    with ui.element('div').classes('grid grid-cols-2 gap-4'):
                        with ui.element('div').classes('group'):
                            ui.html('<label class="block text-sm font-semibold text-gray-700 mb-2">Company Size</label>', sanitize=False)
                            ui.select(['1-10', '11-50', '51-200', '201-500', '500+'],
                                     value=data["company_size"]).classes('w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 hover:border-blue-400').props('outlined dense')

                        with ui.element('div').classes('group'):
                            ui.html('<label class="block text-sm font-semibold text-gray-700 mb-2">Status</label>', sanitize=False)
                            ui.select(['Active', 'Inactive', 'Suspended'],
                                     value=data["status"]).classes('w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 hover:border-blue-400').props('outlined dense')

            # Action Buttons
            with ui.element('div').classes('flex justify-end gap-3 mt-6 pt-6 border-t border-gray-100'):
                ui.button('Save Changes', icon='save', on_click=save_institution_changes).classes('bg-blue-600 text-white px-6 py-3 rounded-xl hover:bg-blue-700 font-semibold shadow-lg hover:shadow-xl transition-all duration-300')
                ui.button('Reset', icon='refresh').classes('bg-gray-100 text-gray-700 px-6 py-3 rounded-xl hover:bg-gray-200 font-semibold transition-all duration-300')

def create_modern_contact_card():
    """Create modern contact information card with professional styling"""
    data = data_manager.get_institution_data()["contact_info"]

    with ui.element('div').classes('bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden hover:shadow-2xl transition-all duration-300'):
        # Card Header
        with ui.element('div').classes('bg-gradient-to-r from-emerald-600 to-green-600 p-6 text-white'):
            with ui.row().classes('items-center gap-4'):
                ui.html('<div class="text-3xl">📞</div>', sanitize=False)
                with ui.column():
                    ui.html('<h3 class="text-xl font-bold">Contact Information</h3>', sanitize=False)
                    ui.html('<p class="text-emerald-100 text-sm">Communication details and location</p>', sanitize=False)

        # Card Content
        with ui.element('div').classes('p-6 space-y-6'):

            # Headquarters Address
            with ui.element('div').classes('group'):
                ui.html('<label class="block text-sm font-semibold text-gray-700 mb-2">Headquarters Address</label>', sanitize=False)
                ui.textarea(value=data["headquarters"]).classes('w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all duration-200 hover:border-emerald-400 min-h-24').props('outlined dense rows=3')

            # Contact Details Grid
            with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 gap-6'):

                # Phone & Fax
                with ui.element('div').classes('space-y-4'):
                    with ui.element('div').classes('group'):
                        ui.html('<label class="block text-sm font-semibold text-gray-700 mb-2">Phone Number</label>', sanitize=False)
                        ui.input(value=data["phone"]).classes('w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all duration-200 hover:border-emerald-400').props('outlined dense type=tel')

                    with ui.element('div').classes('group'):
                        ui.html('<label class="block text-sm font-semibold text-gray-700 mb-2">Fax Number</label>', sanitize=False)
                        ui.input(value=data["fax"]).classes('w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all duration-200 hover:border-emerald-400').props('outlined dense type=tel')

                # Email & Website
                with ui.element('div').classes('space-y-4'):
                    with ui.element('div').classes('group'):
                        ui.html('<label class="block text-sm font-semibold text-gray-700 mb-2">Email Address</label>', sanitize=False)
                        ui.input(value=data["email"]).classes('w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all duration-200 hover:border-emerald-400').props('outlined dense type=email')

                    with ui.element('div').classes('group'):
                        ui.html('<label class="block text-sm font-semibold text-gray-700 mb-2">Website</label>', sanitize=False)
                        ui.input(value=data["website"]).classes('w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all duration-200 hover:border-emerald-400').props('outlined dense type=url')

            # Quick Contact Actions
            with ui.element('div').classes('flex flex-wrap gap-3 mt-6 pt-6 border-t border-gray-100'):
                ui.button('📧 Send Email', icon='email').classes('bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700 font-medium transition-all duration-300')
                ui.button('📞 Call Now', icon='call').classes('bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 font-medium transition-all duration-300')
                ui.button('🌐 Visit Website', icon='language').classes('bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 font-medium transition-all duration-300')
                ui.button('📍 View Map', icon='map').classes('bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700 font-medium transition-all duration-300')

def create_modern_business_settings_card():
    """Create modern business settings card with professional styling"""
    data = data_manager.get_institution_data()["business_info"]

    with ui.element('div').classes('bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden hover:shadow-2xl transition-all duration-300'):
        # Card Header
        with ui.element('div').classes('bg-gradient-to-r from-purple-600 to-indigo-600 p-6 text-white'):
            with ui.row().classes('items-center gap-4'):
                ui.html('<div class="text-3xl">⚙️</div>', sanitize=False)
                with ui.column():
                    ui.html('<h3 class="text-xl font-bold">Business Settings</h3>', sanitize=False)
                    ui.html('<p class="text-purple-100 text-sm">Operational configuration</p>', sanitize=False)

        # Card Content
        with ui.element('div').classes('p-6 space-y-6'):

            # Business Configuration Grid
            with ui.element('div').classes('grid grid-cols-1 gap-6'):

                # Fiscal Year & Currency
                with ui.element('div').classes('grid grid-cols-2 gap-4'):
                    with ui.element('div').classes('group'):
                        ui.html('<label class="block text-sm font-semibold text-gray-700 mb-2">Fiscal Year Start</label>', sanitize=False)
                        ui.select(['January', 'February', 'March', 'April', 'May', 'June',
                                  'July', 'August', 'September', 'October', 'November', 'December'],
                                 value=data["fiscal_year_start"]).classes('w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 hover:border-purple-400').props('outlined dense')

                    with ui.element('div').classes('group'):
                        ui.html('<label class="block text-sm font-semibold text-gray-700 mb-2">Currency</label>', sanitize=False)
                        ui.select(['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD'],
                                 value=data["currency"]).classes('w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 hover:border-purple-400').props('outlined dense')

                # Timezone & Business Hours
                with ui.element('div').classes('grid grid-cols-2 gap-4'):
                    with ui.element('div').classes('group'):
                        ui.html('<label class="block text-sm font-semibold text-gray-700 mb-2">Timezone</label>', sanitize=False)
                        ui.select(['America/New_York', 'America/Los_Angeles', 'Europe/London', 'Europe/Berlin', 'Asia/Tokyo', 'Asia/Shanghai', 'Australia/Sydney'],
                                 value=data["timezone"]).classes('w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 hover:border-purple-400').props('outlined dense')

                    with ui.element('div').classes('group'):
                        ui.html('<label class="block text-sm font-semibold text-gray-700 mb-2">Business Hours</label>', sanitize=False)
                        ui.input(value=data["business_hours"]).classes('w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 hover:border-purple-400').props('outlined dense')

            # Working Days Section
            with ui.element('div').classes('group'):
                ui.html('<label class="block text-sm font-semibold text-gray-700 mb-4">Working Days</label>', sanitize=False)
                with ui.element('div').classes('grid grid-cols-2 md:grid-cols-4 gap-3'):
                    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    for day in days:
                        is_checked = day in data["working_days"]
                        with ui.element('div').classes(f'flex items-center p-3 rounded-xl border-2 transition-all duration-200 cursor-pointer hover:shadow-md {"border-purple-500 bg-purple-50" if is_checked else "border-gray-200 hover:border-purple-300"}'):
                            ui.checkbox(day, value=is_checked).classes('mr-3')
                            ui.html(f'<span class="text-sm font-medium {"text-purple-700" if is_checked else "text-gray-600"}">{day[:3]}</span>', sanitize=False)

            # Business Rules Section
            with ui.element('div').classes('bg-gray-50 rounded-xl p-4 border border-gray-200'):
                ui.html('<h4 class="text-lg font-semibold text-gray-800 mb-3">Business Rules</h4>', sanitize=False)
                with ui.element('div').classes('space-y-3'):
                    rules = [
                        {'label': 'Overtime Policy', 'value': '1.5x after 40 hours'},
                        {'label': 'Leave Accrual', 'value': '10 days per year'},
                        {'label': 'Remote Work', 'value': 'Hybrid model allowed'}
                    ]
                    for rule in rules:
                        with ui.element('div').classes('flex justify-between items-center py-2 border-b border-gray-100 last:border-b-0'):
                            ui.html(f'<span class="text-sm font-medium text-gray-700">{rule["label"]}</span>', sanitize=False)
                            ui.html(f'<span class="text-sm text-gray-600">{rule["value"]}</span>', sanitize=False)

            # Action Buttons
            with ui.element('div').classes('flex justify-end gap-3 mt-6 pt-6 border-t border-gray-100'):
                ui.button('Update Settings', icon='settings', on_click=save_institution_changes).classes('bg-purple-600 text-white px-6 py-3 rounded-xl hover:bg-purple-700 font-semibold shadow-lg hover:shadow-xl transition-all duration-300')
                ui.button('Reset to Default', icon='refresh').classes('bg-gray-100 text-gray-700 px-6 py-3 rounded-xl hover:bg-gray-200 font-semibold transition-all duration-300')

def create_modern_integration_card():
    """Create modern system integration card with professional styling"""

    with ui.element('div').classes('bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden hover:shadow-2xl transition-all duration-300'):
        # Card Header
        with ui.element('div').classes('bg-gradient-to-r from-orange-600 to-red-600 p-6 text-white'):
            with ui.row().classes('items-center gap-4'):
                ui.html('<div class="text-3xl">🔗</div>', sanitize=False)
                with ui.column():
                    ui.html('<h3 class="text-xl font-bold">System Integration</h3>', sanitize=False)
                    ui.html('<p class="text-orange-100 text-sm">Connected HR modules</p>', sanitize=False)

        # Card Content
        with ui.element('div').classes('p-6'):

            # Connected Modules
            ui.html('<h4 class="text-lg font-semibold text-gray-800 mb-4">HR Module Connections</h4>', sanitize=False)

            modules = [
                {'name': 'Employee Management', 'status': 'Connected', 'icon': '👥', 'color': 'emerald', 'description': 'Staff directory & profiles'},
                {'name': 'Department Management', 'status': 'Connected', 'icon': '🏢', 'color': 'emerald', 'description': 'Organizational structure'},
                {'name': 'Attendance Tracking', 'status': 'Connected', 'icon': '⏰', 'color': 'emerald', 'description': 'Time & attendance'},
                {'name': 'Payroll System', 'status': 'Pending', 'icon': '💰', 'color': 'orange', 'description': 'Salary & compensation'},
                {'name': 'Performance Reviews', 'status': 'Not Connected', 'icon': '⭐', 'color': 'red', 'description': 'Employee evaluations'},
                {'name': 'Recruitment', 'status': 'Not Connected', 'icon': '🎯', 'color': 'red', 'description': 'Hiring & onboarding'}
            ]

            with ui.element('div').classes('space-y-3 mb-6'):
                for module in modules:
                    status_class = f"border-{module['color']}-200 bg-{module['color']}-50" if module["status"] == "Connected" else "border-gray-200"
                    with ui.element('div').classes(f'flex items-center justify-between p-4 rounded-xl border-2 transition-all duration-200 hover:shadow-md {status_class}'):
                        with ui.row().classes('items-center gap-4 flex-1'):
                            ui.html(f'<div class="text-2xl">{module["icon"]}</div>', sanitize=False)
                            with ui.column().classes('flex-1'):
                                ui.html(f'<div class="font-semibold text-gray-800">{module["name"]}</div>', sanitize=False)
                                ui.html(f'<div class="text-sm text-gray-600">{module["description"]}</div>', sanitize=False)

                        with ui.element('div').classes('text-right'):
                            if module["status"] == "Connected":
                                ui.html(f'<div class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-{module["color"]}-100 text-{module["color"]}-800"><div class="w-2 h-2 bg-{module["color"]}-500 rounded-full mr-2"></div>Connected</div>', sanitize=False)
                            elif module["status"] == "Pending":
                                ui.html('<div class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-orange-100 text-orange-800"><div class="w-2 h-2 bg-orange-500 rounded-full mr-2 animate-pulse"></div>Pending</div>', sanitize=False)
                            else:
                                ui.button('Connect', on_click=lambda m=module: connect_module(m)).classes(f'bg-{module["color"]}-600 text-white px-4 py-2 rounded-lg hover:bg-{module["color"]}-700 text-sm font-medium transition-all duration-300')

            # Quick Actions
            ui.html('<h4 class="text-lg font-semibold text-gray-800 mb-4">Quick Actions</h4>', sanitize=False)

            with ui.element('div').classes('grid grid-cols-1 gap-3'):
                actions = [
                    {'name': 'Create Department', 'icon': '🏗️', 'route': '/administration/departments', 'color': 'blue'},
                    {'name': 'Add Employee', 'icon': '👤', 'route': '/administration/enroll-staff', 'color': 'green'},
                    {'name': 'View Reports', 'icon': '📊', 'route': '/reports/dashboard', 'color': 'purple'},
                    {'name': 'System Settings', 'icon': '⚙️', 'route': '/administration/settings', 'color': 'gray'}
                ]

                for action in actions:
                    ui.button(f'{action["icon"]} {action["name"]}',
                             on_click=lambda r=action['route']: navigate_to_module(r)).classes(f'w-full bg-{action["color"]}-600 text-white p-4 rounded-xl hover:bg-{action["color"]}-700 font-semibold shadow-lg hover:shadow-xl transition-all duration-300 text-left').props('no-caps')

            # System Health
            with ui.element('div').classes('mt-6 p-4 bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl border border-green-200'):
                with ui.row().classes('items-center justify-between'):
                    with ui.row().classes('items-center gap-3'):
                        ui.html('<div class="text-2xl">💚</div>', sanitize=False)
                        with ui.column():
                            ui.html('<div class="font-semibold text-green-800">System Health</div>', sanitize=False)
                            ui.html('<div class="text-sm text-green-600">All systems operational</div>', sanitize=False)

                    ui.html('<div class="text-right"><div class="text-2xl font-bold text-green-600">98%</div><div class="text-xs text-green-500">Uptime</div></div>', sanitize=False)

def connect_module(module):
    """Handle module connection logic"""
    ui.notify(f'Connecting to {module["name"]}...', color='info')
    # In a real application, this would initiate the connection process
    print(f"Connecting to module: {module['name']}")

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