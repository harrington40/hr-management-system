from __future__ import annotations
from nicegui import ui
from typing import Dict, Any, List, Optional
import yaml
from datetime import datetime, date, timedelta
from dataclasses import dataclass
from enum import Enum
import calendar
import os


class HolidayType(Enum):
    PUBLIC = "public"
    COMPANY = "company"
    RELIGIOUS = "religious"
    FLOATING = "floating"
    EMERGENCY = "emergency"
    REGIONAL = "regional"


class VacationAccrualMethod(Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUALLY = "annually"
    PRORATED = "prorated"


@dataclass
class Holiday:
    name: str
    date: str
    holiday_type: HolidayType
    is_mandatory: bool = True
    affects_payroll: bool = True
    regional_code: Optional[str] = None
    description: Optional[str] = None
    compensation_multiplier: float = 1.5  # Overtime rate for working on holiday


@dataclass
class VacationPolicy:
    name: str
    accrual_method: VacationAccrualMethod
    days_per_year: float
    max_carryover: int
    probation_period_days: int
    min_service_months: int = 0
    accrual_cap: Optional[int] = None
    blackout_periods: List[tuple] = None  # (start_date, end_date) tuples


@dataclass
class EmployeeVacationBalance:
    employee_id: str
    available_days: float
    accrued_this_year: float
    used_this_year: float
    carried_over: float
    pending_requests: float
    last_updated: datetime


class HolidaysManager:
    """Comprehensive HR Holiday and Vacation Management System"""

    def __init__(self) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        self.config_path = os.path.join(project_root, 'config', 'holidays.yaml')
        self.vacation_policies_path = os.path.join(project_root, 'config', 'vacation_policies.yaml')
        self.holidays_data = self.load_holidays()
        self.vacation_policies = self.load_vacation_policies()

    def load_holidays(self) -> Dict[str, Any]:
        """Load holidays from YAML file"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            if not os.path.exists(self.config_path):
                return self.get_default_holidays()
            
            with open(self.config_path, 'r') as file:
                data = yaml.safe_load(file) or {}
                if not isinstance(data, dict):
                    return self.get_default_holidays()
                return data
        except Exception:
            return self.get_default_holidays()

    def load_vacation_policies(self) -> Dict[str, Any]:
        """Load vacation policies from YAML file"""
        try:
            os.makedirs(os.path.dirname(self.vacation_policies_path), exist_ok=True)
            if not os.path.exists(self.vacation_policies_path):
                return self.get_default_vacation_policies()
            
            with open(self.vacation_policies_path, 'r') as file:
                data = yaml.safe_load(file) or {}
                if not isinstance(data, dict):
                    return self.get_default_vacation_policies()
                return data
        except Exception:
            return self.get_default_vacation_policies()

    def save_holidays(self, holidays_data: Dict[str, Any]) -> bool:
        """Save holidays to YAML file"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as file:
                yaml.dump(holidays_data, file, default_flow_style=False, sort_keys=False)
            self.holidays_data = holidays_data
            return True
        except Exception as e:
            print(f"Error saving holidays: {e}")
            return False

    def save_vacation_policies(self, policies_data: Dict[str, Any]) -> bool:
        """Save vacation policies to YAML file"""
        try:
            os.makedirs(os.path.dirname(self.vacation_policies_path), exist_ok=True)
            with open(self.vacation_policies_path, 'w') as file:
                yaml.dump(policies_data, file, default_flow_style=False, sort_keys=False)
            self.vacation_policies = policies_data
            return True
        except Exception as e:
            print(f"Error saving vacation policies: {e}")
            return False

    def calculate_vacation_accrual(self, employee_start_date: date, policy: VacationPolicy, 
                                 current_date: date = None) -> float:
        """Calculate vacation days accrued for an employee based on policy"""
        if current_date is None:
            current_date = date.today()
        
        # Check if employee has completed probation period
        days_employed = (current_date - employee_start_date).days
        if days_employed < policy.probation_period_days:
            return 0.0
        
        # Calculate service months
        service_months = max(0, (current_date.year - employee_start_date.year) * 12 + 
                           current_date.month - employee_start_date.month)
        
        if service_months < policy.min_service_months:
            return 0.0
        
        if policy.accrual_method == VacationAccrualMethod.ANNUALLY:
            years_of_service = service_months / 12.0
            return min(years_of_service * policy.days_per_year, policy.accrual_cap or float('inf'))
        
        elif policy.accrual_method == VacationAccrualMethod.MONTHLY:
            monthly_accrual = policy.days_per_year / 12.0
            return min(service_months * monthly_accrual, policy.accrual_cap or float('inf'))
        
        elif policy.accrual_method == VacationAccrualMethod.QUARTERLY:
            quarters = service_months // 3
            quarterly_accrual = policy.days_per_year / 4.0
            return min(quarters * quarterly_accrual, policy.accrual_cap or float('inf'))
        
        elif policy.accrual_method == VacationAccrualMethod.PRORATED:
            days_this_year = (current_date - max(employee_start_date, 
                                               date(current_date.year, 1, 1))).days
            return min((days_this_year / 365.0) * policy.days_per_year, 
                      policy.accrual_cap or float('inf'))
        
        return 0.0

    def check_blackout_period(self, requested_dates: List[date], policy: VacationPolicy) -> bool:
        """Check if requested vacation dates conflict with blackout periods"""
        if not policy.blackout_periods:
            return False
        
        for start_date, end_date in policy.blackout_periods:
            blackout_start = datetime.strptime(start_date, '%Y-%m-%d').date()
            blackout_end = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            for req_date in requested_dates:
                if blackout_start <= req_date <= blackout_end:
                    return True
        return False

    def calculate_holiday_pay(self, base_salary: float, holiday: Holiday, hours_worked: float = 0) -> float:
        """Calculate holiday pay including overtime compensation"""
        if not holiday.affects_payroll:
            return base_salary
        
        if hours_worked > 0:
            # Employee worked on holiday - pay regular + overtime
            overtime_pay = (base_salary / 8) * hours_worked * holiday.compensation_multiplier
            return base_salary + overtime_pay
        else:
            # Employee didn't work - just regular holiday pay
            return base_salary if holiday.is_mandatory else 0.0

    def get_holidays_in_date_range(self, start_date: date, end_date: date) -> List[Holiday]:
        """Get all holidays within a specified date range"""
        holidays = []
        for category in ['fixed_holidays_2025', 'company_holidays', 'religious_holidays']:
            if category in self.holidays_data.get('holidays_calendar', {}):
                for holiday_data in self.holidays_data['holidays_calendar'][category]:
                    holiday_date = datetime.strptime(holiday_data['date'], '%Y-%m-%d').date()
                    if start_date <= holiday_date <= end_date:
                        holidays.append(Holiday(
                            name=holiday_data['name'],
                            date=holiday_data['date'],
                            holiday_type=HolidayType(holiday_data.get('type', 'company')),
                            is_mandatory=holiday_data.get('is_mandatory', True),
                            affects_payroll=holiday_data.get('affects_payroll', True),
                            description=holiday_data.get('description', '')
                        ))
        return sorted(holidays, key=lambda x: x.date)

    def get_default_holidays(self) -> Dict[str, Any]:
        """Return comprehensive default holidays configuration for HR system"""
        return {
            "holidays_calendar": {
                "version": "2.0",
                "general_settings": {
                    "default_country": "United States",
                    "timezone": "UTC+0",
                    "fiscal_year_start": "01-01",
                    "weekend_days": ["Saturday", "Sunday"],
                    "holiday_pay_multiplier": 1.5
                },
                "fixed_holidays_2025": [
                    {"name": "New Year's Day", "date": "2025-01-01", "type": "public", "is_mandatory": True, "affects_payroll": True, "compensation_multiplier": 1.5},
                    {"name": "Martin Luther King Jr. Day", "date": "2025-01-20", "type": "public", "is_mandatory": True, "affects_payroll": True},
                    {"name": "Presidents' Day", "date": "2025-02-17", "type": "public", "is_mandatory": True, "affects_payroll": True},
                    {"name": "Memorial Day", "date": "2025-05-26", "type": "public", "is_mandatory": True, "affects_payroll": True},
                    {"name": "Independence Day", "date": "2025-07-04", "type": "public", "is_mandatory": True, "affects_payroll": True, "compensation_multiplier": 2.0},
                    {"name": "Labor Day", "date": "2025-09-01", "type": "public", "is_mandatory": True, "affects_payroll": True},
                    {"name": "Columbus Day", "date": "2025-10-13", "type": "public", "is_mandatory": False, "affects_payroll": False},
                    {"name": "Veterans Day", "date": "2025-11-11", "type": "public", "is_mandatory": True, "affects_payroll": True},
                    {"name": "Thanksgiving Day", "date": "2025-11-27", "type": "public", "is_mandatory": True, "affects_payroll": True},
                    {"name": "Christmas Day", "date": "2025-12-25", "type": "public", "is_mandatory": True, "affects_payroll": True, "compensation_multiplier": 2.0}
                ],
                "company_holidays": [
                    {"name": "Company Foundation Day", "date": "2025-03-15", "type": "company", "is_mandatory": True, "affects_payroll": True},
                    {"name": "Summer Shutdown Start", "date": "2025-07-01", "type": "company", "is_mandatory": True, "affects_payroll": True},
                    {"name": "Summer Shutdown End", "date": "2025-07-05", "type": "company", "is_mandatory": True, "affects_payroll": True},
                    {"name": "Year-end Closure Start", "date": "2025-12-24", "type": "company", "is_mandatory": True, "affects_payroll": True},
                    {"name": "Year-end Closure End", "date": "2025-12-31", "type": "company", "is_mandatory": True, "affects_payroll": True}
                ],
                "religious_holidays": [
                    {"name": "Good Friday", "date": "2025-04-18", "type": "religious", "is_mandatory": False, "affects_payroll": False},
                    {"name": "Easter Sunday", "date": "2025-04-20", "type": "religious", "is_mandatory": False, "affects_payroll": False},
                    {"name": "Yom Kippur", "date": "2025-10-04", "type": "religious", "is_mandatory": False, "affects_payroll": False},
                    {"name": "Diwali", "date": "2025-11-01", "type": "religious", "is_mandatory": False, "affects_payroll": False}
                ],
                "floating_holidays": [
                    {"name": "Personal Choice Day 1", "type": "floating", "days_available": 1, "expiry_date": "2025-12-31"},
                    {"name": "Personal Choice Day 2", "type": "floating", "days_available": 1, "expiry_date": "2025-12-31"},
                    {"name": "Cultural Celebration Day", "type": "floating", "days_available": 1, "expiry_date": "2025-12-31"}
                ],
                "blackout_periods": [
                    {"name": "Year-end Processing", "start_date": "2025-12-15", "end_date": "2025-12-31", "reason": "Critical business operations"},
                    {"name": "Q1 Close", "start_date": "2025-03-25", "end_date": "2025-04-05", "reason": "Financial reporting"}
                ]
            }
        }

    def get_default_vacation_policies(self) -> Dict[str, Any]:
        """Return default vacation policies for different employee categories"""
        return {
            "vacation_policies": {
                "version": "1.0",
                "policies": {
                    "new_hire": {
                        "name": "New Employee Policy",
                        "accrual_method": "monthly",
                        "days_per_year": 10,
                        "max_carryover": 5,
                        "probation_period_days": 90,
                        "min_service_months": 3,
                        "accrual_cap": 15,
                        "eligible_employee_types": ["full-time", "part-time"]
                    },
                    "standard": {
                        "name": "Standard Employee Policy",
                        "accrual_method": "monthly",
                        "days_per_year": 15,
                        "max_carryover": 10,
                        "probation_period_days": 0,
                        "min_service_months": 12,
                        "accrual_cap": 25,
                        "eligible_employee_types": ["full-time"]
                    },
                    "senior": {
                        "name": "Senior Employee Policy (3+ years)",
                        "accrual_method": "monthly",
                        "days_per_year": 20,
                        "max_carryover": 15,
                        "probation_period_days": 0,
                        "min_service_months": 36,
                        "accrual_cap": 35,
                        "eligible_employee_types": ["full-time"]
                    },
                    "executive": {
                        "name": "Executive Policy (5+ years)",
                        "accrual_method": "annually",
                        "days_per_year": 25,
                        "max_carryover": 20,
                        "probation_period_days": 0,
                        "min_service_months": 60,
                        "accrual_cap": 40,
                        "eligible_employee_types": ["full-time", "executive"]
                    }
                },
                "general_rules": {
                    "min_vacation_request_days": 1,
                    "max_consecutive_days": 15,
                    "advance_notice_required_days": 14,
                    "approval_required_threshold": 5,
                    "use_or_lose_policy": True,
                    "payout_on_termination": True
                }
            }
        }


def SetHolidays() -> None:
    """Enterprise HR Holiday and Vacation Management System"""
    manager = HolidaysManager()

    # Header with gradient background
    with ui.row().classes('w-full mb-6'):
        with ui.card().classes('w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white'):
            with ui.card_section().classes('p-6'):
                with ui.row().classes('items-center justify-between w-full'):
                    with ui.column().classes('gap-2'):
                        ui.html('<h1 class="text-3xl font-bold flex items-center gap-3"><span class="text-4xl">�</span>HR Holiday & Vacation Management</h1>', sanitize=False).classes('mb-2')
                        ui.label('Comprehensive employee vacation tracking, holiday calendar, and HR policy management').classes('text-indigo-100 text-lg')
                        ui.label(f'System Status: Active • Last Sync: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}').classes('text-indigo-200 text-sm')
                    
                    with ui.row().classes('gap-3'):
                        ui.button('💾 Save All Changes', 
                                 on_click=lambda: save_all_hr_data(manager)
                        ).classes('bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg font-semibold')
                        ui.button('� Generate Report', 
                                 on_click=lambda: generate_hr_report(manager)
                        ).classes('bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold')
                        ui.button('⚙️ Policy Builder', 
                                 on_click=lambda: show_policy_builder(manager)
                        ).classes('bg-purple-500 hover:bg-purple-600 text-white px-6 py-3 rounded-lg font-semibold')

    # Main content area with HR modules
    with ui.row().classes('w-full gap-6'):
        # Left panel - HR Navigation
        with ui.column().classes('w-1/4'):
            with ui.card().classes('w-full'):
                with ui.card_section().classes('p-4'):
                    ui.label('HR Management Modules').classes('text-xl font-bold text-gray-700 mb-4')
                    
                    # Current active view state
                    current_view = ui.state({'view': 'dashboard'})
                    
                    # HR Navigation categories
                    hr_modules = [
                        {'id': 'dashboard', 'name': 'HR Dashboard', 'icon': '📊', 'color': 'blue'},
                        {'id': 'vacation_tracking', 'name': 'Vacation Tracking', 'icon': '🏖️', 'color': 'green'},
                        {'id': 'holiday_calendar', 'name': 'Holiday Calendar', 'icon': '📅', 'color': 'red'},
                        {'id': 'vacation_policies', 'name': 'Vacation Policies', 'icon': '📋', 'color': 'purple'},
                        {'id': 'employee_balances', 'name': 'Employee Balances', 'icon': '⚖️', 'color': 'orange'},
                        {'id': 'blackout_periods', 'name': 'Blackout Periods', 'icon': '🚫', 'color': 'gray'},
                        {'id': 'payroll_integration', 'name': 'Payroll Integration', 'icon': '💰', 'color': 'yellow'},
                        {'id': 'compliance', 'name': 'Compliance Reports', 'icon': '📑', 'color': 'indigo'},
                        {'id': 'settings', 'name': 'System Settings', 'icon': '⚙️', 'color': 'gray'},
                    ]
                    
                    for module in hr_modules:
                        ui.button(
                            f"{module['icon']} {module['name']}",
                            on_click=lambda mod=module['id']: switch_view(mod)
                        ).classes(f'w-full justify-start text-left p-3 rounded-lg mb-2 bg-{module["color"]}-50 hover:bg-{module["color"]}-100 text-gray-700 border-l-4 border-{module["color"]}-400')

        # Right panel - HR Content Area
        with ui.column().classes('w-3/4'):
            with ui.card().classes('w-full'):
                with ui.card_section().classes('p-6'):
                    @ui.refreshable
                    def content_area():
                        if current_view['view'] == 'dashboard':
                            create_hr_dashboard(manager)
                        elif current_view['view'] == 'vacation_tracking':
                            create_vacation_tracking(manager)
                        elif current_view['view'] == 'holiday_calendar':
                            create_holiday_calendar(manager)
                        elif current_view['view'] == 'vacation_policies':
                            create_vacation_policies(manager)
                        elif current_view['view'] == 'employee_balances':
                            create_employee_balances(manager)
                        elif current_view['view'] == 'blackout_periods':
                            create_blackout_periods(manager)
                        elif current_view['view'] == 'payroll_integration':
                            create_payroll_integration(manager)
                        elif current_view['view'] == 'compliance':
                            create_compliance_reports(manager)
                        elif current_view['view'] == 'settings':
                            create_hr_settings(manager)
                    
                    content_area()

    def switch_view(view_id):
        """Switch between different HR module views"""
        current_view['view'] = view_id
        content_area.refresh()

    def save_all_hr_data(manager):
        """Save all HR data including holidays and vacation policies"""
        try:
            holidays_saved = manager.save_holidays(manager.holidays_data)
            policies_saved = manager.save_vacation_policies(manager.vacation_policies)
            
            if holidays_saved and policies_saved:
                ui.notify('✅ All HR data saved successfully!', type='positive')
            else:
                ui.notify('❌ Failed to save some HR data', type='negative')
        except Exception as e:
            ui.notify(f'❌ Error saving HR data: {str(e)}', type='negative')

    def generate_hr_report(manager):
        """Generate comprehensive HR report"""
        ui.notify('📊 Generating HR compliance report...', type='info')
        # This would typically generate PDF/Excel reports
        
    def show_policy_builder(manager):
        """Show vacation policy builder dialog"""
        with ui.dialog() as dialog, ui.card().classes('w-[800px]'):
            ui.label('Vacation Policy Builder').classes('text-2xl font-bold mb-4')
            ui.label('Create custom vacation policies for different employee categories').classes('text-gray-600 mb-6')
            
            with ui.row().classes('w-full gap-4'):
                with ui.column().classes('flex-1'):
                    policy_name = ui.input('Policy Name', placeholder='e.g., Senior Developer Policy').classes('w-full mb-3')
                    accrual_method = ui.select(
                        ['monthly', 'quarterly', 'annually', 'prorated'], 
                        label='Accrual Method', 
                        value='monthly'
                    ).classes('w-full mb-3')
                    days_per_year = ui.number('Vacation Days Per Year', value=15, min=0, max=50).classes('w-full mb-3')
                
                with ui.column().classes('flex-1'):
                    max_carryover = ui.number('Max Carryover Days', value=5, min=0, max=20).classes('w-full mb-3')
                    probation_days = ui.number('Probation Period (Days)', value=90, min=0, max=365).classes('w-full mb-3')
                    min_service_months = ui.number('Min Service Months', value=0, min=0, max=60).classes('w-full mb-3')
            
            with ui.row().classes('gap-3 w-full justify-end mt-6'):
                ui.button('Cancel', on_click=dialog.close).classes('bg-gray-500 text-white px-4 py-2 rounded')
                ui.button('Create Policy', on_click=lambda: create_vacation_policy(
                    manager, policy_name.value, accrual_method.value, days_per_year.value,
                    max_carryover.value, probation_days.value, min_service_months.value, dialog
                )).classes('bg-blue-500 text-white px-4 py-2 rounded')
        
        dialog.open()

    def create_vacation_policy(manager, name, method, days_year, carryover, probation, service_months, dialog):
        """Create a new vacation policy"""
        if not name:
            ui.notify('Please enter a policy name', type='negative')
            return
        
        try:
            new_policy = {
                'name': name,
                'accrual_method': method,
                'days_per_year': days_year,
                'max_carryover': carryover,
                'probation_period_days': probation,
                'min_service_months': service_months,
                'created_date': datetime.now().isoformat(),
                'status': 'active'
            }
            
            # Add to vacation policies
            if 'vacation_policies' not in manager.vacation_policies:
                manager.vacation_policies['vacation_policies'] = {'policies': {}}
            
            policy_id = name.lower().replace(' ', '_')
            manager.vacation_policies['vacation_policies']['policies'][policy_id] = new_policy
            
            if manager.save_vacation_policies(manager.vacation_policies):
                ui.notify(f'✅ Vacation policy "{name}" created successfully!', type='positive')
                dialog.close()
                content_area.refresh()
            else:
                ui.notify('❌ Failed to save vacation policy', type='negative')
                
        except Exception as e:
            ui.notify(f'❌ Error creating policy: {str(e)}', type='negative')

    def show_add_holiday_dialog(manager):
        """Show dialog to add new holiday"""
        with ui.dialog() as dialog, ui.card().classes('w-96'):
            ui.label('Add New Holiday').classes('text-xl font-bold mb-4')
            
            holiday_name = ui.input('Holiday Name', placeholder='e.g., New Year\'s Day').classes('w-full mb-3')
            holiday_date = ui.input('Date', placeholder='YYYY-MM-DD').classes('w-full mb-3')
            holiday_type = ui.select(
                ['public', 'company', 'religious'], 
                label='Holiday Type', 
                value='public'
            ).classes('w-full mb-3')
            holiday_description = ui.textarea('Description (Optional)', 
                                            placeholder='Brief description').classes('w-full mb-4')
            
            with ui.row().classes('gap-3 w-full justify-end'):
                ui.button('Cancel', on_click=dialog.close).classes('bg-gray-500 text-white')
                ui.button('Add Holiday', on_click=lambda: add_holiday(
                    manager, holiday_name.value, holiday_date.value, 
                    holiday_type.value, holiday_description.value, dialog
                )).classes('bg-blue-500 text-white')
        
        dialog.open()

    def add_holiday(manager, name, date_str, holiday_type, description, dialog):
        """Add a new holiday"""
        if not name or not date_str:
            ui.notify('Please fill in holiday name and date', type='negative')
            return
        
        try:
            # Validate date format
            datetime.strptime(date_str, '%Y-%m-%d')
            
            new_holiday = {
                'name': name,
                'date': date_str,
                'type': holiday_type,
                'description': description or ''
            }
            
            # Ensure holidays_calendar exists
            if 'holidays_calendar' not in manager.holidays_data:
                manager.holidays_data['holidays_calendar'] = manager.get_default_holidays()['holidays_calendar']
            
            # Add to appropriate list
            if holiday_type == 'public':
                if 'fixed_holidays_2025' not in manager.holidays_data['holidays_calendar']:
                    manager.holidays_data['holidays_calendar']['fixed_holidays_2025'] = []
                manager.holidays_data['holidays_calendar']['fixed_holidays_2025'].append(new_holiday)
            elif holiday_type == 'company':
                if 'company_holidays' not in manager.holidays_data['holidays_calendar']:
                    manager.holidays_data['holidays_calendar']['company_holidays'] = []
                manager.holidays_data['holidays_calendar']['company_holidays'].append(new_holiday)
            
            if manager.save_holidays(manager.holidays_data):
                ui.notify(f'Holiday "{name}" added successfully!', type='positive')
                dialog.close()
                content_area.refresh()
            else:
                ui.notify('Failed to save holiday', type='negative')
                
        except ValueError:
            ui.notify('Invalid date format. Please use YYYY-MM-DD', type='negative')


def create_hr_dashboard(manager):
    """Create comprehensive HR dashboard with key metrics"""
    ui.label('� HR Dashboard Overview').classes('text-3xl font-bold mb-6')
    
    # Key HR Metrics Row
    with ui.row().classes('w-full gap-4 mb-8'):
        # Holiday Statistics
        holidays_data = manager.holidays_data.get('holidays_calendar', {})
        fixed_holidays = holidays_data.get('fixed_holidays_2025', [])
        company_holidays = holidays_data.get('company_holidays', [])
        religious_holidays = holidays_data.get('religious_holidays', [])
        
        with ui.card().classes('flex-1 bg-gradient-to-br from-blue-50 to-blue-100'):
            with ui.card_section().classes('text-center p-6'):
                total_holidays = len(fixed_holidays) + len(company_holidays) + len(religious_holidays)
                ui.label(str(total_holidays)).classes('text-4xl font-bold text-blue-600 mb-2')
                ui.label('Total Holidays').classes('text-gray-700 font-semibold')
                ui.label('Across all categories').classes('text-gray-500 text-sm')
        
        # Vacation Policies Count
        vacation_policies = manager.vacation_policies.get('vacation_policies', {}).get('policies', {})
        with ui.card().classes('flex-1 bg-gradient-to-br from-green-50 to-green-100'):
            with ui.card_section().classes('text-center p-6'):
                ui.label(str(len(vacation_policies))).classes('text-4xl font-bold text-green-600 mb-2')
                ui.label('Vacation Policies').classes('text-gray-700 font-semibold')
                ui.label('Active policies').classes('text-gray-500 text-sm')
        
        # Pending Requests (Simulated)
        with ui.card().classes('flex-1 bg-gradient-to-br from-orange-50 to-orange-100'):
            with ui.card_section().classes('text-center p-6'):
                ui.label('12').classes('text-4xl font-bold text-orange-600 mb-2')
                ui.label('Pending Requests').classes('text-gray-700 font-semibold')
                ui.label('Awaiting approval').classes('text-gray-500 text-sm')
        
        # Compliance Score (Simulated)
        with ui.card().classes('flex-1 bg-gradient-to-br from-purple-50 to-purple-100'):
            with ui.card_section().classes('text-center p-6'):
                ui.label('98%').classes('text-4xl font-bold text-purple-600 mb-2')
                ui.label('Compliance Score').classes('text-gray-700 font-semibold')
                ui.label('Policy adherence').classes('text-gray-500 text-sm')

    # Quick Actions Section
    with ui.row().classes('w-full gap-6 mb-8'):
        with ui.column().classes('w-1/2'):
            ui.label('🚀 Quick Actions').classes('text-xl font-bold text-gray-700 mb-4')
            with ui.column().classes('gap-3'):
                ui.button('➕ Add New Holiday', 
                         on_click=lambda: show_add_holiday_dialog(manager)
                ).classes('w-full bg-blue-500 text-white p-3 rounded-lg hover:bg-blue-600')
                ui.button('📋 Create Vacation Policy', 
                         on_click=lambda: show_policy_builder(manager)
                ).classes('w-full bg-green-500 text-white p-3 rounded-lg hover:bg-green-600')
                ui.button('📊 Generate Reports', 
                         on_click=lambda: generate_hr_report(manager)
                ).classes('w-full bg-purple-500 text-white p-3 rounded-lg hover:bg-purple-600')
        
        with ui.column().classes('w-1/2'):
            ui.label('📅 Upcoming Important Dates').classes('text-xl font-bold text-gray-700 mb-4')
            
            # Get next 5 holidays
            all_holidays = []
            for category in ['fixed_holidays_2025', 'company_holidays']:
                if category in holidays_data:
                    all_holidays.extend(holidays_data[category])
            
            # Sort by date and get upcoming ones
            today = date.today()
            upcoming_holidays = []
            for holiday in all_holidays:
                try:
                    holiday_date = datetime.strptime(holiday['date'], '%Y-%m-%d').date()
                    if holiday_date >= today:
                        upcoming_holidays.append((holiday, holiday_date))
                except:
                    continue
            
            upcoming_holidays.sort(key=lambda x: x[1])
            
            if upcoming_holidays:
                for holiday, holiday_date in upcoming_holidays[:5]:
                    days_until = (holiday_date - today).days
                    with ui.row().classes('w-full p-3 bg-gray-50 rounded-lg mb-2 border-l-4 border-indigo-400'):
                        with ui.column().classes('flex-1'):
                            ui.label(holiday['name']).classes('font-semibold')
                            ui.label(f"{holiday_date.strftime('%B %d, %Y')} ({days_until} days)").classes('text-gray-600 text-sm')
                        ui.badge(holiday.get('type', 'company').title()).classes('bg-indigo-100 text-indigo-800')
            else:
                ui.label('No upcoming holidays configured').classes('text-gray-500 italic')

    # Recent Activity Timeline (Simulated)
    ui.label('📋 Recent HR Activity').classes('text-xl font-bold text-gray-700 mb-4')
    with ui.card().classes('w-full'):
        with ui.card_section().classes('p-4'):
            activities = [
                {'action': 'Holiday Added', 'details': 'Martin Luther King Jr. Day added to public holidays', 'time': '2 hours ago', 'type': 'holiday'},
                {'action': 'Policy Updated', 'details': 'Senior employee vacation policy modified - increased carryover days', 'time': '1 day ago', 'type': 'policy'},
                {'action': 'Report Generated', 'details': 'Q4 vacation utilization report generated', 'time': '2 days ago', 'type': 'report'},
                {'action': 'Blackout Period Set', 'details': 'Year-end processing blackout period configured', 'time': '3 days ago', 'type': 'blackout'},
            ]
            
            for activity in activities:
                icon_map = {
                    'holiday': '🎉',
                    'policy': '📋',
                    'report': '📊',
                    'blackout': '🚫'
                }
                
                with ui.row().classes('w-full p-3 border-b border-gray-200 last:border-b-0'):
                    ui.label(icon_map.get(activity['type'], '📝')).classes('text-2xl mr-3')
                    with ui.column().classes('flex-1'):
                        ui.label(activity['action']).classes('font-semibold text-gray-800')
                        ui.label(activity['details']).classes('text-gray-600 text-sm')
                    ui.label(activity['time']).classes('text-gray-500 text-sm')


def create_vacation_tracking(manager):
    """Create vacation tracking interface"""
    ui.label('�️ Employee Vacation Tracking').classes('text-3xl font-bold mb-6')
    
    # Search and filter bar
    with ui.row().classes('w-full gap-4 mb-6'):
        search_input = ui.input('Search employees...', placeholder='Enter employee name or ID').classes('flex-1')
        department_filter = ui.select(['All Departments', 'Engineering', 'HR', 'Sales', 'Marketing'], 
                                    value='All Departments').classes('w-48')
        ui.button('🔍 Search', on_click=lambda: search_employees()).classes('bg-blue-500 text-white px-4 py-2 rounded')
        ui.button('📥 Import Data', on_click=lambda: show_import_dialog()).classes('bg-green-500 text-white px-4 py-2 rounded')

    # Vacation Balance Summary Cards
    with ui.row().classes('w-full gap-4 mb-8'):
        with ui.card().classes('flex-1 bg-gradient-to-r from-green-400 to-green-600 text-white'):
            with ui.card_section().classes('p-6'):
                ui.label('Available Days').classes('text-lg font-semibold mb-2')
                ui.label('1,247').classes('text-3xl font-bold')
                ui.label('Total across all employees').classes('text-green-100 text-sm')
        
        with ui.card().classes('flex-1 bg-gradient-to-r from-blue-400 to-blue-600 text-white'):
            with ui.card_section().classes('p-6'):
                ui.label('Used This Year').classes('text-lg font-semibold mb-2')
                ui.label('832').classes('text-3xl font-bold')
                ui.label('Days taken so far').classes('text-blue-100 text-sm')
        
        with ui.card().classes('flex-1 bg-gradient-to-r from-yellow-400 to-yellow-600 text-white'):
            with ui.card_section().classes('p-6'):
                ui.label('Pending Requests').classes('text-lg font-semibold mb-2')
                ui.label('47').classes('text-3xl font-bold')
                ui.label('Awaiting approval').classes('text-yellow-100 text-sm')
        
        with ui.card().classes('flex-1 bg-gradient-to-r from-red-400 to-red-600 text-white'):
            with ui.card_section().classes('p-6'):
                ui.label('At-Risk Employees').classes('text-lg font-semibold mb-2')
                ui.label('8').classes('text-3xl font-bold')
                ui.label('May lose vacation days').classes('text-red-100 text-sm')

    # Employee Vacation Table
    ui.label('Employee Vacation Balances').classes('text-xl font-bold mb-4')
    
    # Sample employee data (in a real system, this would come from database)
    sample_employees = [
        {'id': 'EMP001', 'name': 'John Smith', 'department': 'Engineering', 'policy': 'Senior', 
         'available': 18.5, 'used': 6.5, 'pending': 3.0, 'accrued': 20.0, 'start_date': '2020-03-15'},
        {'id': 'EMP002', 'name': 'Sarah Johnson', 'department': 'HR', 'policy': 'Standard', 
         'available': 12.0, 'used': 8.0, 'pending': 0.0, 'accrued': 15.0, 'start_date': '2022-01-10'},
        {'id': 'EMP003', 'name': 'Mike Davis', 'department': 'Sales', 'policy': 'Executive', 
         'available': 22.0, 'used': 3.0, 'pending': 5.0, 'accrued': 25.0, 'start_date': '2018-06-01'},
        {'id': 'EMP004', 'name': 'Lisa Chen', 'department': 'Marketing', 'policy': 'New Hire', 
         'available': 5.5, 'used': 2.5, 'pending': 0.0, 'accrued': 8.0, 'start_date': '2024-09-01'},
        {'id': 'EMP005', 'name': 'Robert Wilson', 'department': 'Engineering', 'policy': 'Senior', 
         'available': 0.5, 'used': 19.5, 'pending': 0.0, 'accrued': 20.0, 'start_date': '2019-11-20'},
    ]
    
    with ui.card().classes('w-full'):
        with ui.card_section().classes('p-0'):
            # Table header
            with ui.row().classes('w-full bg-gray-50 p-4 font-bold text-gray-700'):
                ui.label('Employee').classes('w-48')
                ui.label('Department').classes('w-32')
                ui.label('Policy').classes('w-32')
                ui.label('Available').classes('w-24 text-center')
                ui.label('Used').classes('w-24 text-center')
                ui.label('Pending').classes('w-24 text-center')
                ui.label('Total Accrued').classes('w-32 text-center')
                ui.label('Actions').classes('w-32 text-center')
            
            # Table rows
            for emp in sample_employees:
                with ui.row().classes('w-full p-4 border-b border-gray-200 hover:bg-gray-50'):
                    # Employee info
                    with ui.column().classes('w-48'):
                        ui.label(emp['name']).classes('font-semibold')
                        ui.label(emp['id']).classes('text-gray-600 text-sm')
                    
                    ui.label(emp['department']).classes('w-32')
                    ui.badge(emp['policy']).classes('w-32 bg-blue-100 text-blue-800')
                    
                    # Vacation numbers with color coding
                    available_color = 'text-green-600' if emp['available'] > 10 else 'text-red-600' if emp['available'] < 5 else 'text-yellow-600'
                    ui.label(f"{emp['available']:.1f}").classes(f'w-24 text-center font-bold {available_color}')
                    ui.label(f"{emp['used']:.1f}").classes('w-24 text-center')
                    ui.label(f"{emp['pending']:.1f}").classes('w-24 text-center text-orange-600')
                    ui.label(f"{emp['accrued']:.1f}").classes('w-32 text-center')
                    
                    # Action buttons
                    with ui.row().classes('w-32 gap-1'):
                        ui.button('📝', on_click=lambda e=emp: show_employee_details(e)).classes('bg-blue-500 text-white px-2 py-1 rounded text-xs')
                        ui.button('📊', on_click=lambda e=emp: show_vacation_history(e)).classes('bg-green-500 text-white px-2 py-1 rounded text-xs')

    def search_employees():
        ui.notify('🔍 Searching employees...', type='info')
        
    def show_import_dialog():
        with ui.dialog() as dialog, ui.card().classes('w-96'):
            ui.label('Import Employee Data').classes('text-xl font-bold mb-4')
            ui.label('Upload CSV file with employee vacation data').classes('text-gray-600 mb-4')
            
            ui.upload(on_upload=lambda e: handle_file_upload(e, dialog)).classes('w-full mb-4')
            
            with ui.row().classes('gap-3 w-full justify-end'):
                ui.button('Cancel', on_click=dialog.close).classes('bg-gray-500 text-white')
                ui.button('Import', on_click=lambda: process_import(dialog)).classes('bg-blue-500 text-white')
        
        dialog.open()
    
    def handle_file_upload(event, dialog):
        ui.notify(f'File uploaded: {event.name}', type='positive')
    
    def process_import(dialog):
        ui.notify('📥 Processing import...', type='info')
        dialog.close()
    
    def show_employee_details(employee):
        ui.notify(f'📝 Viewing details for {employee["name"]}', type='info')
    
    def show_vacation_history(employee):
        ui.notify(f'📊 Loading vacation history for {employee["name"]}', type='info')


def create_holiday_calendar(manager):
    """Create comprehensive holiday calendar interface"""
    ui.label('📅 Holiday Calendar Management').classes('text-3xl font-bold mb-6')
    
    # Calendar control toolbar
    with ui.row().classes('w-full gap-4 mb-6'):
        ui.button('➕ Add Holiday', on_click=lambda: show_add_holiday_dialog(manager)).classes('bg-blue-500 text-white px-4 py-2 rounded')
        ui.button('📥 Import Holidays', on_click=lambda: show_import_holidays_dialog()).classes('bg-green-500 text-white px-4 py-2 rounded')
        ui.button('📤 Export Calendar', on_click=lambda: export_holiday_calendar()).classes('bg-purple-500 text-white px-4 py-2 rounded')
        ui.button('🔄 Sync with National Calendar', on_click=lambda: sync_national_holidays()).classes('bg-orange-500 text-white px-4 py-2 rounded')
    
    # Holiday categories with counts
    holidays_data = manager.holidays_data.get('holidays_calendar', {})
    
    with ui.row().classes('w-full gap-4 mb-8'):
        # Public Holidays
        public_holidays = holidays_data.get('fixed_holidays_2025', [])
        public_count = len([h for h in public_holidays if h.get('type') == 'public'])
        with ui.card().classes('flex-1 bg-red-50 border-l-4 border-red-400'):
            with ui.card_section().classes('p-4'):
                with ui.row().classes('items-center'):
                    ui.label('�️').classes('text-3xl mr-3')
                    with ui.column():
                        ui.label(f'{public_count} Public Holidays').classes('font-bold text-red-700')
                        ui.label('Government mandated').classes('text-red-600 text-sm')

        # Company Holidays
        company_holidays = holidays_data.get('company_holidays', [])
        with ui.card().classes('flex-1 bg-blue-50 border-l-4 border-blue-400'):
            with ui.card_section().classes('p-4'):
                with ui.row().classes('items-center'):
                    ui.label('🏢').classes('text-3xl mr-3')
                    with ui.column():
                        ui.label(f'{len(company_holidays)} Company Holidays').classes('font-bold text-blue-700')
                        ui.label('Company specific').classes('text-blue-600 text-sm')

        # Religious Holidays
        religious_holidays = holidays_data.get('religious_holidays', [])
        with ui.card().classes('flex-1 bg-purple-50 border-l-4 border-purple-400'):
            with ui.card_section().classes('p-4'):
                with ui.row().classes('items-center'):
                    ui.label('🕊️').classes('text-3xl mr-3')
                    with ui.column():
                        ui.label(f'{len(religious_holidays)} Religious Holidays').classes('font-bold text-purple-700')
                        ui.label('Optional observances').classes('text-purple-600 text-sm')

        # Floating Holidays
        floating_holidays = holidays_data.get('floating_holidays', [])
        with ui.card().classes('flex-1 bg-green-50 border-l-4 border-green-400'):
            with ui.card_section().classes('p-4'):
                with ui.row().classes('items-center'):
                    ui.label('🎈').classes('text-3xl mr-3')
                    with ui.column():
                        ui.label(f'{len(floating_holidays)} Floating Holidays').classes('font-bold text-green-700')
                        ui.label('Employee choice').classes('text-green-600 text-sm')

    # Holiday list by category with enhanced details
    ui.label('Holiday Details by Category').classes('text-xl font-bold mb-4')
    
    # Tabbed interface for different holiday categories
    with ui.tabs().classes('w-full') as tabs:
        public_tab = ui.tab('Public Holidays')
        company_tab = ui.tab('Company Holidays') 
        religious_tab = ui.tab('Religious Holidays')
        floating_tab = ui.tab('Floating Holidays')

    with ui.tab_panels(tabs, value=public_tab).classes('w-full'):
        # Public Holidays Panel
        with ui.tab_panel(public_tab):
            create_holiday_category_panel(manager, 'fixed_holidays_2025', 'public', 'Public')
        
        # Company Holidays Panel  
        with ui.tab_panel(company_tab):
            create_holiday_category_panel(manager, 'company_holidays', 'company', 'Company')
            
        # Religious Holidays Panel
        with ui.tab_panel(religious_tab):
            create_holiday_category_panel(manager, 'religious_holidays', 'religious', 'Religious')
            
        # Floating Holidays Panel
        with ui.tab_panel(floating_tab):
            create_floating_holidays_panel(manager)

    def show_import_holidays_dialog():
        with ui.dialog() as dialog, ui.card().classes('w-[600px]'):
            ui.label('Import Holiday Calendar').classes('text-xl font-bold mb-4')
            ui.label('Import holidays from various sources').classes('text-gray-600 mb-4')
            
            with ui.column().classes('w-full gap-4'):
                ui.select(['US Federal Holidays', 'UK Bank Holidays', 'Canadian Holidays', 'Custom CSV'], 
                         label='Holiday Source').classes('w-full')
                ui.number('Year', value=2025, min=2024, max=2030).classes('w-full')
                ui.upload(on_upload=lambda e: ui.notify(f'File uploaded: {e.name}')).classes('w-full')
                
            with ui.row().classes('gap-3 w-full justify-end mt-4'):
                ui.button('Cancel', on_click=dialog.close).classes('bg-gray-500 text-white')
                ui.button('Import', on_click=lambda: [ui.notify('📥 Importing holidays...'), dialog.close()]).classes('bg-blue-500 text-white')
        
        dialog.open()
    
    def export_holiday_calendar():
        ui.notify('📤 Exporting holiday calendar to CSV...', type='info')
        
    def sync_national_holidays():
        ui.notify('🔄 Syncing with national holiday database...', type='info')

def create_holiday_category_panel(manager, category_key, holiday_type, category_name):
    """Create a panel for a specific holiday category"""
    holidays_data = manager.holidays_data.get('holidays_calendar', {})
    holidays = holidays_data.get(category_key, [])
    
    if holiday_type != 'all':
        holidays = [h for h in holidays if h.get('type') == holiday_type]
    
    with ui.row().classes('w-full gap-4 mb-4'):
        ui.button(f'➕ Add {category_name} Holiday', 
                 on_click=lambda: show_add_specific_holiday_dialog(manager, holiday_type)
        ).classes('bg-blue-500 text-white px-4 py-2 rounded')
        
        if holidays:
            ui.button(f'📊 Analyze {category_name} Impact', 
                     on_click=lambda: analyze_holiday_impact(holidays)
            ).classes('bg-green-500 text-white px-4 py-2 rounded')
    
    if holidays:
        # Sort holidays by date
        try:
            holidays.sort(key=lambda x: datetime.strptime(x.get('date', '2025-01-01'), '%Y-%m-%d'))
        except:
            pass
            
        for holiday in holidays:
            with ui.card().classes('w-full mb-3 hover:shadow-lg transition-shadow'):
                with ui.card_section().classes('p-4'):
                    with ui.row().classes('items-center justify-between'):
                        with ui.column().classes('flex-1'):
                            with ui.row().classes('items-center gap-3 mb-2'):
                                # Holiday type badge
                                type_colors = {
                                    'public': 'bg-red-100 text-red-800',
                                    'company': 'bg-blue-100 text-blue-800', 
                                    'religious': 'bg-purple-100 text-purple-800'
                                }
                                ui.badge(holiday.get('type', 'company').title()).classes(type_colors.get(holiday.get('type'), 'bg-gray-100 text-gray-800'))
                                
                                # Mandatory indicator
                                if holiday.get('is_mandatory', True):
                                    ui.badge('Mandatory').classes('bg-orange-100 text-orange-800')
                                else:
                                    ui.badge('Optional').classes('bg-gray-100 text-gray-600')
                                
                                # Payroll impact
                                if holiday.get('affects_payroll', True):
                                    ui.badge('Paid').classes('bg-green-100 text-green-800')
                            
                            ui.label(holiday.get('name', 'Unnamed Holiday')).classes('text-lg font-semibold text-gray-800')
                            
                            with ui.row().classes('items-center gap-4 text-sm text-gray-600'):
                                ui.label(f"📅 {holiday.get('date', 'No date')}")
                                if holiday.get('compensation_multiplier'):
                                    ui.label(f"💰 {holiday.get('compensation_multiplier')}x pay rate")
                                if holiday.get('description'):
                                    ui.label(f"ℹ️ {holiday.get('description')}")
                        
                        with ui.column().classes('gap-2'):
                            ui.button('✏️ Edit', 
                                     on_click=lambda h=holiday: edit_holiday(manager, h)
                            ).classes('bg-blue-500 text-white px-3 py-1 rounded text-sm')
                            ui.button('🗑️ Remove', 
                                     on_click=lambda h=holiday: remove_holiday(manager, h, category_key)
                            ).classes('bg-red-500 text-white px-3 py-1 rounded text-sm')
    else:
        ui.label(f'No {category_name.lower()} holidays configured yet.').classes('text-gray-500 italic text-center p-8')

def create_floating_holidays_panel(manager):
    """Create panel for floating holidays management"""
    holidays_data = manager.holidays_data.get('holidays_calendar', {})
    floating_holidays = holidays_data.get('floating_holidays', [])
    
    ui.label('Floating holidays allow employees to choose when to take specific days off.').classes('text-gray-600 mb-4')
    
    with ui.row().classes('w-full gap-4 mb-4'):
        ui.button('➕ Add Floating Holiday Policy', 
                 on_click=lambda: show_add_floating_holiday_dialog(manager)
        ).classes('bg-blue-500 text-white px-4 py-2 rounded')
    
    if floating_holidays:
        for floating in floating_holidays:
            with ui.card().classes('w-full mb-3'):
                with ui.card_section().classes('p-4'):
                    with ui.row().classes('items-center justify-between'):
                        with ui.column().classes('flex-1'):
                            ui.label(floating.get('name', 'Unnamed Floating Holiday')).classes('text-lg font-semibold')
                            with ui.row().classes('gap-4 text-sm text-gray-600'):
                                ui.label(f"📅 {floating.get('days_available', 1)} day(s) available")
                                ui.label(f"⏰ Expires: {floating.get('expiry_date', 'No expiry')}")
                        
                        ui.button('🗑️ Remove', 
                                 on_click=lambda f=floating: remove_floating_holiday(manager, f)
                        ).classes('bg-red-500 text-white px-3 py-1 rounded text-sm')
    else:
        ui.label('No floating holiday policies configured yet.').classes('text-gray-500 italic text-center p-8')

def show_add_specific_holiday_dialog(manager, holiday_type):
    """Show dialog to add holiday of specific type"""
    with ui.dialog() as dialog, ui.card().classes('w-[600px]'):
        ui.label(f'Add {holiday_type.title()} Holiday').classes('text-xl font-bold mb-4')
        
        with ui.column().classes('w-full gap-4'):
            holiday_name = ui.input('Holiday Name', placeholder=f'e.g., Independence Day').classes('w-full')
            holiday_date = ui.input('Date (YYYY-MM-DD)', placeholder='2025-07-04').classes('w-full')
            
            is_mandatory = ui.checkbox('Mandatory Holiday', value=True).classes('w-full')
            affects_payroll = ui.checkbox('Affects Payroll', value=True).classes('w-full')
            
            compensation_multiplier = ui.number('Overtime Pay Multiplier', value=1.5, min=1.0, max=3.0, step=0.1).classes('w-full')
            description = ui.textarea('Description (Optional)', placeholder='Additional details about this holiday').classes('w-full')
        
        with ui.row().classes('gap-3 w-full justify-end mt-4'):
            ui.button('Cancel', on_click=dialog.close).classes('bg-gray-500 text-white')
            ui.button('Add Holiday', on_click=lambda: add_typed_holiday(
                manager, holiday_name.value, holiday_date.value, holiday_type,
                is_mandatory.value, affects_payroll.value, compensation_multiplier.value, 
                description.value, dialog
            )).classes('bg-blue-500 text-white')
    
    dialog.open()

def analyze_holiday_impact(holidays):
    """Analyze the business impact of holidays"""
    ui.notify(f'📊 Analyzing impact of {len(holidays)} holidays on business operations...', type='info')

def edit_holiday(manager, holiday):
    """Edit existing holiday"""
    ui.notify(f'✏️ Editing holiday: {holiday.get("name")}', type='info')

def remove_floating_holiday(manager, floating_holiday):
    """Remove floating holiday policy"""
    ui.notify(f'🗑️ Removing floating holiday policy: {floating_holiday.get("name")}', type='info')

def add_typed_holiday(manager, name, date_str, holiday_type, mandatory, payroll, multiplier, description, dialog):
    """Add holiday with specific type and properties"""
    if not name or not date_str:
        ui.notify('Please fill in required fields', type='negative')
        return
    
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        
        new_holiday = {
            'name': name,
            'date': date_str,
            'type': holiday_type,
            'is_mandatory': mandatory,
            'affects_payroll': payroll,
            'compensation_multiplier': multiplier,
            'description': description
        }
        
        # Determine which category to add to
        category_map = {
            'public': 'fixed_holidays_2025',
            'company': 'company_holidays',
            'religious': 'religious_holidays'
        }
        
        category = category_map.get(holiday_type, 'company_holidays')
        
        if 'holidays_calendar' not in manager.holidays_data:
            manager.holidays_data['holidays_calendar'] = {}
        
        if category not in manager.holidays_data['holidays_calendar']:
            manager.holidays_data['holidays_calendar'][category] = []
        
        manager.holidays_data['holidays_calendar'][category].append(new_holiday)
        
        if manager.save_holidays(manager.holidays_data):
            ui.notify(f'✅ {holiday_type.title()} holiday "{name}" added successfully!', type='positive')
            dialog.close()
            # Refresh content would go here
        else:
            ui.notify('❌ Failed to save holiday', type='negative')
            
    except ValueError:
        ui.notify('❌ Invalid date format. Please use YYYY-MM-DD', type='negative')

def show_add_floating_holiday_dialog(manager):
    """Show dialog to add floating holiday policy"""
    with ui.dialog() as dialog, ui.card().classes('w-96'):
        ui.label('Add Floating Holiday Policy').classes('text-xl font-bold mb-4')
        
        policy_name = ui.input('Policy Name', placeholder='e.g., Personal Choice Day').classes('w-full mb-3')
        days_available = ui.number('Days Available', value=1, min=1, max=5).classes('w-full mb-3')
        expiry_date = ui.input('Expiry Date (YYYY-MM-DD)', value='2025-12-31').classes('w-full mb-3')
        
        with ui.row().classes('gap-3 w-full justify-end'):
            ui.button('Cancel', on_click=dialog.close).classes('bg-gray-500 text-white')
            ui.button('Add Policy', on_click=lambda: add_floating_holiday_policy(
                manager, policy_name.value, days_available.value, expiry_date.value, dialog
            )).classes('bg-blue-500 text-white')
    
    dialog.open()

def add_floating_holiday_policy(manager, name, days, expiry, dialog):
    """Add floating holiday policy"""
    if not name:
        ui.notify('Please enter a policy name', type='negative')
        return
    
    new_policy = {
        'name': name,
        'type': 'floating',
        'days_available': days,
        'expiry_date': expiry
    }
    
    if 'holidays_calendar' not in manager.holidays_data:
        manager.holidays_data['holidays_calendar'] = {}
    
    if 'floating_holidays' not in manager.holidays_data['holidays_calendar']:
        manager.holidays_data['holidays_calendar']['floating_holidays'] = []
    
    manager.holidays_data['holidays_calendar']['floating_holidays'].append(new_policy)
    
    if manager.save_holidays(manager.holidays_data):
        ui.notify(f'✅ Floating holiday policy "{name}" added successfully!', type='positive')
        dialog.close()
    else:
        ui.notify('❌ Failed to save policy', type='negative')


def create_settings_content(manager):
    """Create settings content"""
    ui.label('⚙️ Holiday Settings').classes('text-2xl font-bold mb-4')
    ui.label('Configure holiday calendar settings').classes('text-gray-600 mb-4')
    
    # General settings
    with ui.card().classes('w-full mb-4'):
        with ui.card_section().classes('p-4'):
            ui.label('General Settings').classes('text-lg font-semibold mb-3')
            
            general_settings = manager.holidays_data.get('holidays_calendar', {}).get('general_settings', {})
            
            with ui.row().classes('items-center gap-4 mb-3'):
                ui.label('Default Country:').classes('w-32')
                country_input = ui.input(value=general_settings.get('default_country', 'United States')).classes('flex-1')
            
            with ui.row().classes('items-center gap-4 mb-3'):
                ui.label('Timezone:').classes('w-32')
                timezone_input = ui.input(value=general_settings.get('timezone', 'UTC+0')).classes('flex-1')
    
    with ui.row().classes('gap-4'):
        ui.button('Save Settings', 
                 on_click=lambda: save_settings(manager, country_input.value, timezone_input.value)
        ).classes('bg-blue-500 text-white px-4 py-2 rounded')
        ui.button('Reset to Default', 
                 on_click=lambda: reset_settings(manager)
        ).classes('bg-gray-500 text-white px-4 py-2 rounded')


def show_add_public_holiday_dialog(manager):
    """Show add public holiday dialog"""
    with ui.dialog() as dialog, ui.card().classes('w-96'):
        ui.label('Add Public Holiday').classes('text-xl font-bold mb-4')
        
        holiday_name = ui.input('Holiday Name').classes('w-full mb-3')
        holiday_date = ui.input('Date').classes('w-full mb-3')
        description = ui.textarea('Description').classes('w-full mb-4')
        
        with ui.row().classes('gap-3 w-full justify-end'):
            ui.button('Cancel', on_click=dialog.close).classes('bg-gray-500 text-white')
            ui.button('Add Holiday', on_click=lambda: add_specific_holiday(
                manager, holiday_name.value, holiday_date.value, 'public', description.value, dialog
            )).classes('bg-blue-500 text-white')
    
    dialog.open()


def show_add_company_holiday_dialog(manager):
    """Show add company holiday dialog"""
    with ui.dialog() as dialog, ui.card().classes('w-96'):
        ui.label('Add Company Holiday').classes('text-xl font-bold mb-4')
        
        holiday_name = ui.input('Holiday Name').classes('w-full mb-3')
        holiday_date = ui.input('Date').classes('w-full mb-3')
        description = ui.textarea('Description').classes('w-full mb-4')
        
        with ui.row().classes('gap-3 w-full justify-end'):
            ui.button('Cancel', on_click=dialog.close).classes('bg-gray-500 text-white')
            ui.button('Add Holiday', on_click=lambda: add_specific_holiday(
                manager, holiday_name.value, holiday_date.value, 'company', description.value, dialog
            )).classes('bg-green-500 text-white')
    
    dialog.open()


def add_specific_holiday(manager, name, date_str, holiday_type, description, dialog):
    """Add a specific type of holiday"""
    if not name or not date_str:
        ui.notify('Please fill in required fields', type='negative')
        return
    
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        
        new_holiday = {
            'name': name,
            'date': date_str,
            'type': holiday_type,
            'description': description
        }
        
        if 'holidays_calendar' not in manager.holidays_data:
            manager.holidays_data['holidays_calendar'] = {}
        
        if holiday_type == 'public':
            if 'fixed_holidays_2025' not in manager.holidays_data['holidays_calendar']:
                manager.holidays_data['holidays_calendar']['fixed_holidays_2025'] = []
            manager.holidays_data['holidays_calendar']['fixed_holidays_2025'].append(new_holiday)
        elif holiday_type == 'company':
            if 'company_holidays' not in manager.holidays_data['holidays_calendar']:
                manager.holidays_data['holidays_calendar']['company_holidays'] = []
            manager.holidays_data['holidays_calendar']['company_holidays'].append(new_holiday)
        
        if manager.save_holidays(manager.holidays_data):
            ui.notify(f'{holiday_type.title()} holiday "{name}" added successfully!', type='positive')
            dialog.close()
            SetHolidays.content_area.refresh() if hasattr(SetHolidays, 'content_area') else None
        else:
            ui.notify('Failed to save holiday', type='negative')
            
    except ValueError:
        ui.notify('Invalid date format. Please use YYYY-MM-DD', type='negative')


def remove_holiday(manager, holiday, category):
    """Remove a holiday from the specified category"""
    try:
        if category in manager.holidays_data.get('holidays_calendar', {}):
            holidays_list = manager.holidays_data['holidays_calendar'][category]
            if holiday in holidays_list:
                holidays_list.remove(holiday)
                if manager.save_holidays(manager.holidays_data):
                    ui.notify(f'Removed holiday: {holiday.get("name", "Unknown")}', type='positive')
                    SetHolidays.content_area.refresh() if hasattr(SetHolidays, 'content_area') else None
                else:
                    ui.notify('Error removing holiday', type='negative')
    except Exception as e:
        ui.notify(f'Error removing holiday: {str(e)}', type='negative')


def save_settings(manager, country, timezone):
    """Save general settings"""
    if 'holidays_calendar' not in manager.holidays_data:
        manager.holidays_data['holidays_calendar'] = {}
    if 'general_settings' not in manager.holidays_data['holidays_calendar']:
        manager.holidays_data['holidays_calendar']['general_settings'] = {}
    
    manager.holidays_data['holidays_calendar']['general_settings']['default_country'] = country
    manager.holidays_data['holidays_calendar']['general_settings']['timezone'] = timezone
    
    if manager.save_holidays(manager.holidays_data):
        ui.notify('Settings saved successfully!', type='positive')
    else:
        ui.notify('Error saving settings', type='negative')


def create_vacation_policies(manager):
    """Create vacation policies management interface"""
    ui.label('📋 Vacation Policy Management').classes('text-3xl font-bold mb-6')
    
    with ui.row().classes('w-full gap-4 mb-6'):
        ui.button('➕ Create New Policy', on_click=lambda: show_policy_builder(manager)).classes('bg-blue-500 text-white px-4 py-2 rounded')
        ui.button('📊 Policy Analytics', on_click=lambda: show_policy_analytics()).classes('bg-green-500 text-white px-4 py-2 rounded')
        ui.button('📋 Policy Templates', on_click=lambda: show_policy_templates()).classes('bg-purple-500 text-white px-4 py-2 rounded')
    
    # Policy overview cards
    policies_data = manager.vacation_policies.get('vacation_policies', {}).get('policies', {})
    
    ui.label('Current Vacation Policies').classes('text-xl font-bold mb-4')
    
    if policies_data:
        for policy_id, policy in policies_data.items():
            with ui.card().classes('w-full mb-4 border-l-4 border-blue-400'):
                with ui.card_section().classes('p-6'):
                    with ui.row().classes('items-start justify-between'):
                        with ui.column().classes('flex-1'):
                            ui.label(policy.get('name', 'Unnamed Policy')).classes('text-xl font-bold text-gray-800 mb-2')
                            
                            with ui.row().classes('gap-8 mb-4'):
                                with ui.column():
                                    ui.label('📅 Accrual Details').classes('font-semibold text-gray-700 mb-2')
                                    ui.label(f"Method: {policy.get('accrual_method', 'monthly').title()}").classes('text-gray-600')
                                    ui.label(f"Days/Year: {policy.get('days_per_year', 0)}").classes('text-gray-600')
                                    ui.label(f"Accrual Cap: {policy.get('accrual_cap', 'Unlimited')}").classes('text-gray-600')
                                
                                with ui.column():
                                    ui.label('⏰ Service Requirements').classes('font-semibold text-gray-700 mb-2')
                                    ui.label(f"Probation: {policy.get('probation_period_days', 0)} days").classes('text-gray-600')
                                    ui.label(f"Min Service: {policy.get('min_service_months', 0)} months").classes('text-gray-600')
                                    ui.label(f"Max Carryover: {policy.get('max_carryover', 0)} days").classes('text-gray-600')
                                
                                with ui.column():
                                    ui.label('👥 Eligibility').classes('font-semibold text-gray-700 mb-2')
                                    eligible_types = policy.get('eligible_employee_types', [])
                                    if eligible_types:
                                        for emp_type in eligible_types:
                                            ui.badge(emp_type.title()).classes('bg-blue-100 text-blue-800 mb-1')
                                    else:
                                        ui.label('All employees').classes('text-gray-600')
                        
                        with ui.column().classes('gap-2'):
                            ui.button('✏️ Edit Policy', on_click=lambda p=policy: edit_policy(p)).classes('bg-blue-500 text-white px-3 py-1 rounded')
                            ui.button('📋 Duplicate', on_click=lambda p=policy: duplicate_policy(p)).classes('bg-green-500 text-white px-3 py-1 rounded') 
                            ui.button('🗑️ Delete', on_click=lambda p=policy: delete_policy(policy_id)).classes('bg-red-500 text-white px-3 py-1 rounded')
    else:
        ui.label('No vacation policies configured yet. Create your first policy to get started.').classes('text-gray-500 italic text-center p-8')
    
    def show_policy_analytics():
        ui.notify('📊 Loading policy utilization analytics...', type='info')
    
    def show_policy_templates():
        ui.notify('📋 Opening policy template library...', type='info')
    
    def edit_policy(policy):
        ui.notify(f'✏️ Editing policy: {policy.get("name")}', type='info')
    
    def duplicate_policy(policy):
        ui.notify(f'📋 Duplicating policy: {policy.get("name")}', type='info')
    
    def delete_policy(policy_id):
        ui.notify(f'🗑️ Deleting policy: {policy_id}', type='info')


def create_employee_balances(manager):
    """Create employee vacation balances interface"""
    ui.label('⚖️ Employee Vacation Balances').classes('text-3xl font-bold mb-6')
    
    # Balance calculation tools
    with ui.row().classes('w-full gap-4 mb-6'):
        ui.button('🔄 Recalculate All Balances', on_click=lambda: recalculate_all_balances()).classes('bg-blue-500 text-white px-4 py-2 rounded')
        ui.button('📊 Balance Report', on_click=lambda: generate_balance_report()).classes('bg-green-500 text-white px-4 py-2 rounded')
        ui.button('⚠️ Find At-Risk Employees', on_click=lambda: find_at_risk_employees()).classes('bg-orange-500 text-white px-4 py-2 rounded')
        ui.button('💰 Calculate Payouts', on_click=lambda: calculate_termination_payouts()).classes('bg-purple-500 text-white px-4 py-2 rounded')
    
    # Balance calculation demo
    ui.label('Vacation Balance Calculator').classes('text-xl font-bold mb-4')
    
    with ui.card().classes('w-full mb-6'):
        with ui.card_section().classes('p-6'):
            ui.label('Calculate vacation balance for an employee').classes('text-gray-600 mb-4')
            
            with ui.row().classes('w-full gap-4 mb-4'):
                employee_start_date = ui.input('Start Date (YYYY-MM-DD)', value='2022-01-15').classes('flex-1')
                policy_select = ui.select(['new_hire', 'standard', 'senior', 'executive'], 
                                        label='Vacation Policy', value='standard').classes('flex-1')
                calculation_date = ui.input('Calculation Date (YYYY-MM-DD)', 
                                          value=date.today().strftime('%Y-%m-%d')).classes('flex-1')
            
            with ui.row().classes('gap-4'):
                ui.button('Calculate Balance', on_click=lambda: calculate_demo_balance(
                    manager, employee_start_date.value, policy_select.value, calculation_date.value
                )).classes('bg-blue-500 text-white px-4 py-2 rounded')
                
                # Results area
                result_area = ui.column().classes('flex-1 ml-4')
    
    def calculate_demo_balance(manager, start_date_str, policy_id, calc_date_str):
        """Calculate and display vacation balance for demo"""
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            calc_date = datetime.strptime(calc_date_str, '%Y-%m-%d').date()
            
            # Get policy
            policies = manager.vacation_policies.get('vacation_policies', {}).get('policies', {})
            if policy_id not in policies:
                ui.notify('Policy not found', type='negative')
                return
            
            policy_data = policies[policy_id]
            policy = VacationPolicy(
                name=policy_data['name'],
                accrual_method=VacationAccrualMethod(policy_data['accrual_method']),
                days_per_year=policy_data['days_per_year'],
                max_carryover=policy_data['max_carryover'],
                probation_period_days=policy_data['probation_period_days'],
                min_service_months=policy_data['min_service_months'],
                accrual_cap=policy_data.get('accrual_cap')
            )
            
            # Calculate balance
            accrued_days = manager.calculate_vacation_accrual(start_date, policy, calc_date)
            
            result_area.clear()
            with result_area:
                ui.label('Calculation Results').classes('font-bold text-green-700 mb-2')
                ui.label(f'Total Accrued: {accrued_days:.2f} days').classes('text-gray-700')
                ui.label(f'Service Period: {(calc_date - start_date).days} days').classes('text-gray-700')
                ui.label(f'Policy: {policy.name}').classes('text-gray-700')
                
        except Exception as e:
            ui.notify(f'Calculation error: {str(e)}', type='negative')
    
    def recalculate_all_balances():
        ui.notify('🔄 Recalculating vacation balances for all employees...', type='info')
    
    def generate_balance_report():
        ui.notify('📊 Generating comprehensive balance report...', type='info')
    
    def find_at_risk_employees():
        ui.notify('⚠️ Identifying employees at risk of losing vacation days...', type='info')
    
    def calculate_termination_payouts():
        ui.notify('💰 Calculating vacation payouts for terminated employees...', type='info')


def create_blackout_periods(manager):
    """Create blackout periods management interface"""
    ui.label('🚫 Blackout Period Management').classes('text-3xl font-bold mb-6')
    
    ui.label('Blackout periods are times when vacation requests are restricted due to business needs.').classes('text-gray-600 mb-6')
    
    with ui.row().classes('w-full gap-4 mb-6'):
        ui.button('➕ Add Blackout Period', on_click=lambda: show_add_blackout_dialog()).classes('bg-red-500 text-white px-4 py-2 rounded')
        ui.button('📅 Import from Calendar', on_click=lambda: import_blackout_calendar()).classes('bg-blue-500 text-white px-4 py-2 rounded')
        ui.button('📊 Impact Analysis', on_click=lambda: analyze_blackout_impact()).classes('bg-green-500 text-white px-4 py-2 rounded')
    
    # Display existing blackout periods
    holidays_data = manager.holidays_data.get('holidays_calendar', {})
    blackout_periods = holidays_data.get('blackout_periods', [])
    
    if blackout_periods:
        ui.label('Active Blackout Periods').classes('text-xl font-bold mb-4')
        
        for period in blackout_periods:
            with ui.card().classes('w-full mb-3 border-l-4 border-red-400'):
                with ui.card_section().classes('p-4'):
                    with ui.row().classes('items-center justify-between'):
                        with ui.column().classes('flex-1'):
                            ui.label(period.get('name', 'Unnamed Blackout Period')).classes('text-lg font-semibold text-gray-800')
                            ui.label(f"📅 {period.get('start_date')} to {period.get('end_date')}").classes('text-gray-600')
                            ui.label(f"ℹ️ {period.get('reason', 'No reason specified')}").classes('text-gray-600 text-sm')
                        
                        with ui.row().classes('gap-2'):
                            ui.button('✏️ Edit', on_click=lambda p=period: edit_blackout_period(p)).classes('bg-blue-500 text-white px-3 py-1 rounded text-sm')
                            ui.button('🗑️ Remove', on_click=lambda p=period: remove_blackout_period(p)).classes('bg-red-500 text-white px-3 py-1 rounded text-sm')
    else:
        ui.label('No blackout periods configured.').classes('text-gray-500 italic text-center p-8')
    
    def show_add_blackout_dialog():
        with ui.dialog() as dialog, ui.card().classes('w-96'):
            ui.label('Add Blackout Period').classes('text-xl font-bold mb-4')
            
            period_name = ui.input('Period Name', placeholder='e.g., Year-end Processing').classes('w-full mb-3')
            start_date = ui.input('Start Date (YYYY-MM-DD)').classes('w-full mb-3') 
            end_date = ui.input('End Date (YYYY-MM-DD)').classes('w-full mb-3')
            reason = ui.textarea('Reason', placeholder='Why is vacation restricted during this time?').classes('w-full mb-4')
            
            with ui.row().classes('gap-3 w-full justify-end'):
                ui.button('Cancel', on_click=dialog.close).classes('bg-gray-500 text-white')
                ui.button('Add Blackout Period', on_click=lambda: add_blackout_period(
                    period_name.value, start_date.value, end_date.value, reason.value, dialog
                )).classes('bg-red-500 text-white')
        
        dialog.open()
    
    def add_blackout_period(name, start, end, reason, dialog):
        if not all([name, start, end]):
            ui.notify('Please fill in all required fields', type='negative')
            return
        
        new_period = {
            'name': name,
            'start_date': start,
            'end_date': end,
            'reason': reason
        }
        
        if 'holidays_calendar' not in manager.holidays_data:
            manager.holidays_data['holidays_calendar'] = {}
        
        if 'blackout_periods' not in manager.holidays_data['holidays_calendar']:
            manager.holidays_data['holidays_calendar']['blackout_periods'] = []
        
        manager.holidays_data['holidays_calendar']['blackout_periods'].append(new_period)
        
        if manager.save_holidays(manager.holidays_data):
            ui.notify(f'✅ Blackout period "{name}" added successfully!', type='positive')
            dialog.close()
        else:
            ui.notify('❌ Failed to save blackout period', type='negative')
    
    def import_blackout_calendar():
        ui.notify('📅 Importing blackout periods from external calendar...', type='info')
    
    def analyze_blackout_impact():
        ui.notify('📊 Analyzing impact of blackout periods on vacation requests...', type='info')
    
    def edit_blackout_period(period):
        ui.notify(f'✏️ Editing blackout period: {period.get("name")}', type='info')
    
    def remove_blackout_period(period):
        ui.notify(f'🗑️ Removing blackout period: {period.get("name")}', type='info')


def create_payroll_integration(manager):
    """Create payroll integration interface"""
    ui.label('💰 Payroll Integration').classes('text-3xl font-bold mb-6')
    
    ui.label('Integrate vacation and holiday data with payroll systems for accurate compensation calculations.').classes('text-gray-600 mb-6')
    
    # Integration status cards
    with ui.row().classes('w-full gap-4 mb-8'):
        with ui.card().classes('flex-1 bg-green-50 border-l-4 border-green-400'):
            with ui.card_section().classes('p-6 text-center'):
                ui.label('✅ Connected').classes('text-2xl font-bold text-green-600 mb-2')
                ui.label('Payroll System').classes('text-gray-700 font-semibold')
                ui.label('Last sync: 2 hours ago').classes('text-green-600 text-sm')
        
        with ui.card().classes('flex-1 bg-blue-50 border-l-4 border-blue-400'):
            with ui.card_section().classes('p-6 text-center'):
                ui.label('847').classes('text-2xl font-bold text-blue-600 mb-2')
                ui.label('Records Synced').classes('text-gray-700 font-semibold')
                ui.label('This month').classes('text-blue-600 text-sm')
        
        with ui.card().classes('flex-1 bg-yellow-50 border-l-4 border-yellow-400'):
            with ui.card_section().classes('p-6 text-center'):
                ui.label('3').classes('text-2xl font-bold text-yellow-600 mb-2')
                ui.label('Pending Reviews').classes('text-gray-700 font-semibold')
                ui.label('Require attention').classes('text-yellow-600 text-sm')
    
    # Payroll actions
    with ui.row().classes('w-full gap-4 mb-6'):
        ui.button('🔄 Sync Now', on_click=lambda: sync_payroll_data()).classes('bg-blue-500 text-white px-4 py-2 rounded')
        ui.button('📊 Payroll Report', on_click=lambda: generate_payroll_report()).classes('bg-green-500 text-white px-4 py-2 rounded')
        ui.button('💰 Calculate Holiday Pay', on_click=lambda: calculate_holiday_pay_bulk()).classes('bg-purple-500 text-white px-4 py-2 rounded')
        ui.button('⚙️ Integration Settings', on_click=lambda: show_payroll_settings()).classes('bg-gray-500 text-white px-4 py-2 rounded')
    
    # Holiday pay calculation demo
    ui.label('Holiday Pay Calculator').classes('text-xl font-bold mb-4')
    
    with ui.card().classes('w-full'):
        with ui.card_section().classes('p-6'):
            ui.label('Calculate holiday pay for employees who worked on holidays').classes('text-gray-600 mb-4')
            
            with ui.row().classes('w-full gap-4 mb-4'):
                base_salary = ui.number('Base Daily Salary ($)', value=200.0, min=0).classes('flex-1')
                hours_worked = ui.number('Hours Worked on Holiday', value=8.0, min=0, max=24).classes('flex-1')
                holiday_multiplier = ui.number('Holiday Pay Multiplier', value=1.5, min=1.0, max=3.0, step=0.1).classes('flex-1')
            
            with ui.row().classes('gap-4 items-center'):
                ui.button('Calculate Pay', on_click=lambda: calculate_demo_holiday_pay(
                    base_salary.value, hours_worked.value, holiday_multiplier.value
                )).classes('bg-blue-500 text-white px-4 py-2 rounded')
                
                pay_result = ui.label('').classes('text-lg font-semibold text-green-600')
    
    def calculate_demo_holiday_pay(base, hours, multiplier):
        """Calculate holiday pay demonstration"""
        if hours > 0:
            regular_pay = base
            overtime_pay = (base / 8) * hours * multiplier
            total_pay = regular_pay + overtime_pay
            pay_result.text = f'Total Pay: ${total_pay:.2f} (Regular: ${regular_pay:.2f} + Holiday OT: ${overtime_pay:.2f})'
        else:
            pay_result.text = f'Holiday Pay: ${base:.2f}'
    
    def sync_payroll_data():
        ui.notify('🔄 Synchronizing vacation and holiday data with payroll system...', type='info')
    
    def generate_payroll_report():
        ui.notify('📊 Generating payroll integration report...', type='info')
    
    def calculate_holiday_pay_bulk():
        ui.notify('💰 Calculating holiday pay for all employees...', type='info')
    
    def show_payroll_settings():
        ui.notify('⚙️ Opening payroll integration settings...', type='info')


def create_compliance_reports(manager):
    """Create compliance reporting interface"""
    ui.label('📑 Compliance & Reporting').classes('text-3xl font-bold mb-6')
    
    ui.label('Generate comprehensive reports for legal compliance, audits, and management review.').classes('text-gray-600 mb-6')
    
    # Compliance status overview
    with ui.row().classes('w-full gap-4 mb-8'):
        with ui.card().classes('flex-1 bg-green-50 border-l-4 border-green-400'):
            with ui.card_section().classes('p-6'):
                ui.label('✅ Labor Law Compliance').classes('text-lg font-bold text-green-700 mb-2')
                ui.label('98% Compliant').classes('text-2xl font-bold text-green-600')
                ui.label('2 minor issues to address').classes('text-green-600 text-sm')
        
        with ui.card().classes('flex-1 bg-blue-50 border-l-4 border-blue-400'):
            with ui.card_section().classes('p-6'):
                ui.label('📊 Audit Readiness').classes('text-lg font-bold text-blue-700 mb-2')
                ui.label('Ready').classes('text-2xl font-bold text-blue-600')
                ui.label('All documentation current').classes('text-blue-600 text-sm')
        
        with ui.card().classes('flex-1 bg-yellow-50 border-l-4 border-yellow-400'):
            with ui.card_section().classes('p-6'):
                ui.label('📋 Policy Updates').classes('text-lg font-bold text-yellow-700 mb-2')
                ui.label('3 Pending').classes('text-2xl font-bold text-yellow-600')
                ui.label('Review required').classes('text-yellow-600 text-sm')
    
    # Report generation tools
    ui.label('Available Reports').classes('text-xl font-bold mb-4')
    
    reports = [
        {'name': 'Vacation Utilization Report', 'desc': 'Employee vacation usage patterns and trends', 'icon': '📈'},
        {'name': 'Holiday Compliance Report', 'desc': 'Adherence to holiday policies and regulations', 'icon': '📅'},
        {'name': 'Payroll Audit Trail', 'desc': 'Vacation and holiday pay calculations for audit', 'icon': '💰'},
        {'name': 'Employee Balance Summary', 'desc': 'Current vacation balances across all employees', 'icon': '⚖️'},
        {'name': 'Policy Effectiveness Report', 'desc': 'Analysis of vacation policy performance', 'icon': '📊'},
        {'name': 'Compliance Checklist', 'desc': 'Legal and regulatory compliance status', 'icon': '✅'},
    ]
    
    with ui.row().classes('w-full gap-4 flex-wrap'):
        for report in reports:
            with ui.card().classes('w-80 hover:shadow-lg transition-shadow cursor-pointer'):
                with ui.card_section().classes('p-4'):
                    with ui.row().classes('items-center mb-3'):
                        ui.label(report['icon']).classes('text-3xl mr-3')
                        ui.label(report['name']).classes('text-lg font-semibold text-gray-800')
                    
                    ui.label(report['desc']).classes('text-gray-600 text-sm mb-4')
                    
                    with ui.row().classes('gap-2 w-full'):
                        ui.button('📄 Generate', on_click=lambda r=report: generate_report(r)).classes('bg-blue-500 text-white px-3 py-1 rounded text-sm flex-1')
                        ui.button('📅 Schedule', on_click=lambda r=report: schedule_report(r)).classes('bg-green-500 text-white px-3 py-1 rounded text-sm flex-1')
    
    def generate_report(report):
        ui.notify(f'📄 Generating {report["name"]}...', type='info')
    
    def schedule_report(report):
        ui.notify(f'📅 Scheduling {report["name"]}...', type='info')


def create_hr_settings(manager):
    """Create HR system settings interface"""
    ui.label('⚙️ HR System Settings').classes('text-3xl font-bold mb-6')
    
    # General settings section
    with ui.card().classes('w-full mb-6'):
        with ui.card_section().classes('p-6'):
            ui.label('🏢 Company Information').classes('text-xl font-bold text-gray-700 mb-4')
            
            general_settings = manager.holidays_data.get('holidays_calendar', {}).get('general_settings', {})
            
            with ui.row().classes('w-full gap-4 mb-4'):
                company_name = ui.input('Company Name', value='ACME Corporation').classes('flex-1')
                country = ui.input('Default Country', value=general_settings.get('default_country', 'United States')).classes('flex-1')
                timezone = ui.input('Timezone', value=general_settings.get('timezone', 'UTC+0')).classes('flex-1')
            
            with ui.row().classes('w-full gap-4 mb-4'):
                fiscal_year_start = ui.input('Fiscal Year Start (MM-DD)', 
                                           value=general_settings.get('fiscal_year_start', '01-01')).classes('flex-1')
                weekend_days = ui.input('Weekend Days', 
                                      value=', '.join(general_settings.get('weekend_days', ['Saturday', 'Sunday']))).classes('flex-1')
                holiday_pay_multiplier = ui.number('Default Holiday Pay Multiplier', 
                                                 value=general_settings.get('holiday_pay_multiplier', 1.5), 
                                                 min=1.0, max=3.0, step=0.1).classes('flex-1')
    
    # Vacation policy settings
    with ui.card().classes('w-full mb-6'):
        with ui.card_section().classes('p-6'):
            ui.label('🏖️ Vacation Policy Settings').classes('text-xl font-bold text-gray-700 mb-4')
            
            general_rules = manager.vacation_policies.get('vacation_policies', {}).get('general_rules', {})
            
            with ui.row().classes('w-full gap-4 mb-4'):
                min_request_days = ui.number('Min Vacation Request (Days)', 
                                           value=general_rules.get('min_vacation_request_days', 1),
                                           min=0.5, max=5, step=0.5).classes('flex-1')
                max_consecutive = ui.number('Max Consecutive Days', 
                                          value=general_rules.get('max_consecutive_days', 15),
                                          min=1, max=30).classes('flex-1')
                advance_notice = ui.number('Required Advance Notice (Days)', 
                                         value=general_rules.get('advance_notice_required_days', 14),
                                         min=1, max=60).classes('flex-1')
            
            with ui.row().classes('w-full gap-4 mb-4'):
                approval_threshold = ui.number('Approval Required Threshold (Days)', 
                                             value=general_rules.get('approval_required_threshold', 5),
                                             min=1, max=10).classes('flex-1')
                
                use_or_lose = ui.checkbox('Use-or-Lose Policy', 
                                        value=general_rules.get('use_or_lose_policy', True)).classes('flex-1')
                
                payout_on_termination = ui.checkbox('Payout on Termination', 
                                                  value=general_rules.get('payout_on_termination', True)).classes('flex-1')
    
    # System settings
    with ui.card().classes('w-full mb-6'):
        with ui.card_section().classes('p-6'):
            ui.label('🔧 System Configuration').classes('text-xl font-bold text-gray-700 mb-4')
            
            with ui.row().classes('w-full gap-4 mb-4'):
                auto_backup = ui.checkbox('Enable Automatic Backups', value=True).classes('flex-1')
                email_notifications = ui.checkbox('Email Notifications', value=True).classes('flex-1')
                audit_logging = ui.checkbox('Audit Logging', value=True).classes('flex-1')
            
            with ui.row().classes('w-full gap-4 mb-4'):
                backup_frequency = ui.select(['Daily', 'Weekly', 'Monthly'], value='Daily').classes('flex-1')
                notification_email = ui.input('Notification Email', value='hr@company.com').classes('flex-1')
                log_retention = ui.number('Log Retention (Days)', value=365, min=30, max=2555).classes('flex-1')
    
    # Save settings
    with ui.row().classes('gap-4 mt-6'):
        ui.button('💾 Save All Settings', on_click=lambda: save_hr_settings(
            manager, company_name.value, country.value, timezone.value,
            fiscal_year_start.value, weekend_days.value, holiday_pay_multiplier.value,
            min_request_days.value, max_consecutive.value, advance_notice.value,
            approval_threshold.value, use_or_lose.value, payout_on_termination.value
        )).classes('bg-blue-500 text-white px-6 py-3 rounded-lg font-semibold')
        
        ui.button('🔄 Reset to Defaults', on_click=lambda: reset_hr_settings(manager)).classes('bg-gray-500 text-white px-6 py-3 rounded-lg')
        ui.button('📤 Export Configuration', on_click=lambda: export_hr_config()).classes('bg-green-500 text-white px-6 py-3 rounded-lg')
        ui.button('📥 Import Configuration', on_click=lambda: import_hr_config()).classes('bg-purple-500 text-white px-6 py-3 rounded-lg')

def save_hr_settings(manager, company, country, timezone, fiscal_start, weekends, pay_multiplier,
                     min_req, max_consec, advance_notice, approval_threshold, use_lose, payout_term):
    """Save all HR settings"""
    try:
        # Update general settings
        if 'holidays_calendar' not in manager.holidays_data:
            manager.holidays_data['holidays_calendar'] = {}
        
        manager.holidays_data['holidays_calendar']['general_settings'] = {
            'company_name': company,
            'default_country': country,
            'timezone': timezone,
            'fiscal_year_start': fiscal_start,
            'weekend_days': [day.strip() for day in weekends.split(',')],
            'holiday_pay_multiplier': pay_multiplier
        }
        
        # Update vacation policy general rules
        if 'vacation_policies' not in manager.vacation_policies:
            manager.vacation_policies['vacation_policies'] = {}
        
        manager.vacation_policies['vacation_policies']['general_rules'] = {
            'min_vacation_request_days': min_req,
            'max_consecutive_days': max_consec,
            'advance_notice_required_days': advance_notice,
            'approval_required_threshold': approval_threshold,
            'use_or_lose_policy': use_lose,
            'payout_on_termination': payout_term
        }
        
        # Save both configurations
        holidays_saved = manager.save_holidays(manager.holidays_data)
        policies_saved = manager.save_vacation_policies(manager.vacation_policies)
        
        if holidays_saved and policies_saved:
            ui.notify('✅ All HR settings saved successfully!', type='positive')
        else:
            ui.notify('❌ Failed to save some settings', type='negative')
            
    except Exception as e:
        ui.notify(f'❌ Error saving settings: {str(e)}', type='negative')

def reset_hr_settings(manager):
    """Reset all HR settings to defaults"""
    manager.holidays_data = manager.get_default_holidays()
    manager.vacation_policies = manager.get_default_vacation_policies()
    
    holidays_saved = manager.save_holidays(manager.holidays_data)
    policies_saved = manager.save_vacation_policies(manager.vacation_policies)
    
    if holidays_saved and policies_saved:
        ui.notify('🔄 All settings reset to defaults!', type='positive')
        # Refresh the UI would go here in a real implementation
    else:
        ui.notify('❌ Error resetting settings', type='negative')

def export_hr_config():
    """Export HR configuration"""
    ui.notify('📤 Exporting HR configuration to file...', type='info')

def import_hr_config():
    """Import HR configuration"""
    ui.notify('📥 Importing HR configuration from file...', type='info')


# Additional helper functions for the HR system
def show_add_holiday_dialog(manager, refresh_callback=None):
    """Show dialog to add a new holiday"""
    with ui.dialog() as dialog, ui.card().classes('w-96'):
        ui.label('Add New Holiday').classes('text-xl font-bold mb-4')
        
        holiday_name = ui.input('Holiday Name', placeholder='e.g., Independence Day').classes('w-full mb-3')
        holiday_date = ui.input('Date (YYYY-MM-DD)', placeholder='e.g., 2024-07-04').classes('w-full mb-3')
        holiday_type = ui.select(['public', 'company', 'religious', 'floating'], 
                                label='Holiday Type', value='public').classes('w-full mb-3')
        is_paid = ui.checkbox('Paid Holiday', value=True).classes('mb-3')
        description = ui.textarea('Description (Optional)', placeholder='Additional details about this holiday').classes('w-full mb-4')
        
        with ui.row().classes('gap-3 w-full justify-end'):
            ui.button('Cancel', on_click=dialog.close).classes('bg-gray-500 text-white')
            ui.button('Add Holiday', on_click=lambda: add_new_holiday(
                manager, holiday_name.value, holiday_date.value, holiday_type.value, 
                is_paid.value, description.value, dialog, refresh_callback
            )).classes('bg-blue-500 text-white')
    
    dialog.open()

def add_new_holiday(manager, name, date_str, holiday_type, is_paid, description, dialog, refresh_callback):
    """Add a new holiday to the system"""
    if not name or not date_str:
        ui.notify('Please provide holiday name and date', type='negative')
        return
    
    try:
        # Validate date format
        datetime.strptime(date_str, '%Y-%m-%d')
        
        new_holiday = {
            'name': name,
            'date': date_str,
            'type': holiday_type,
            'is_paid': is_paid,
            'description': description,
            'created_date': datetime.now().strftime('%Y-%m-%d')
        }
        
        # Add to appropriate category
        if 'holidays_calendar' not in manager.holidays_data:
            manager.holidays_data['holidays_calendar'] = {}
        
        category_key = f'{holiday_type}_holidays'
        if category_key not in manager.holidays_data['holidays_calendar']:
            manager.holidays_data['holidays_calendar'][category_key] = []
        
        manager.holidays_data['holidays_calendar'][category_key].append(new_holiday)
        
        if manager.save_holidays(manager.holidays_data):
            ui.notify(f'✅ Holiday "{name}" added successfully!', type='positive')
            dialog.close()
            if refresh_callback:
                refresh_callback()
        else:
            ui.notify('❌ Failed to save holiday', type='negative')
            
    except ValueError:
        ui.notify('Invalid date format. Please use YYYY-MM-DD', type='negative')
    except Exception as e:
        ui.notify(f'Error adding holiday: {str(e)}', type='negative')

def remove_holiday(manager, holiday, category, refresh_callback=None):
    """Remove a holiday from the system"""
    try:
        holidays_list = manager.holidays_data.get('holidays_calendar', {}).get(category, [])
        
        # Find and remove the holiday
        for i, h in enumerate(holidays_list):
            if h.get('name') == holiday.get('name') and h.get('date') == holiday.get('date'):
                holidays_list.pop(i)
                break
        
        if manager.save_holidays(manager.holidays_data):
            ui.notify(f'🗑️ Holiday "{holiday.get("name")}" removed successfully!', type='positive')
            if refresh_callback:
                refresh_callback()
        else:
            ui.notify('❌ Failed to remove holiday', type='negative')
            
    except Exception as e:
        ui.notify(f'Error removing holiday: {str(e)}', type='negative')

def show_policy_builder(manager):
    """Show comprehensive policy builder dialog"""
    with ui.dialog() as dialog, ui.card().classes('w-[600px] max-h-[80vh] overflow-y-auto'):
        ui.label('🏗️ Vacation Policy Builder').classes('text-2xl font-bold mb-4')
        
        # Basic policy information
        ui.label('📝 Basic Information').classes('text-lg font-semibold mb-3')
        policy_name = ui.input('Policy Name', placeholder='e.g., Standard Employee Policy').classes('w-full mb-3')
        policy_desc = ui.textarea('Description', placeholder='Describe this vacation policy...').classes('w-full mb-4')
        
        # Accrual settings
        ui.label('📈 Accrual Settings').classes('text-lg font-semibold mb-3')
        
        with ui.row().classes('w-full gap-4 mb-3'):
            accrual_method = ui.select(['monthly', 'quarterly', 'annually', 'prorated'], 
                                     label='Accrual Method', value='monthly').classes('flex-1')
            days_per_year = ui.number('Days Per Year', value=20, min=0, max=50).classes('flex-1')
            accrual_cap = ui.number('Accrual Cap (Days)', value=30, min=0).classes('flex-1')
        
        # Service requirements
        ui.label('⏰ Service Requirements').classes('text-lg font-semibold mb-3 mt-4')
        
        with ui.row().classes('w-full gap-4 mb-3'):
            probation_days = ui.number('Probation Period (Days)', value=90, min=0, max=365).classes('flex-1')
            min_service_months = ui.number('Min Service (Months)', value=3, min=0, max=24).classes('flex-1')
            max_carryover = ui.number('Max Carryover (Days)', value=5, min=0, max=20).classes('flex-1')
        
        # Eligibility
        ui.label('👥 Employee Eligibility').classes('text-lg font-semibold mb-3 mt-4')
        
        eligible_types = ui.select(['full_time', 'part_time', 'contract', 'temporary', 'intern'], 
                                  multiple=True, value=['full_time'],
                                  label='Eligible Employee Types').classes('w-full mb-4')
        
        # Advanced settings
        with ui.expansion('🔧 Advanced Settings', icon='settings').classes('w-full mb-4'):
            with ui.column().classes('gap-3 p-3'):
                use_anniversary = ui.checkbox('Use Anniversary Date for Accrual Reset', value=False)
                allow_negative = ui.checkbox('Allow Negative Balances', value=False) 
                auto_payout = ui.checkbox('Auto Payout on Termination', value=True)
                
                with ui.row().classes('gap-4 w-full'):
                    max_request_days = ui.number('Max Single Request (Days)', value=10, min=1).classes('flex-1')
                    blackout_override = ui.checkbox('Allow Blackout Period Override', value=False).classes('flex-1')
        
        # Save/Cancel buttons
        with ui.row().classes('gap-4 w-full justify-end mt-6'):
            ui.button('Cancel', on_click=dialog.close).classes('bg-gray-500 text-white px-4 py-2')
            ui.button('💾 Create Policy', on_click=lambda: create_vacation_policy(
                manager, policy_name.value, policy_desc.value, accrual_method.value,
                days_per_year.value, accrual_cap.value, probation_days.value,
                min_service_months.value, max_carryover.value, eligible_types.value, dialog
            )).classes('bg-blue-500 text-white px-4 py-2')
    
    dialog.open()

def create_vacation_policy(manager, name, description, accrual_method, days_per_year,
                          accrual_cap, probation_days, min_service_months, max_carryover, 
                          eligible_types, dialog):
    """Create a new vacation policy"""
    if not name:
        ui.notify('Please provide a policy name', type='negative')
        return
    
    try:
        # Generate unique policy ID
        policy_id = name.lower().replace(' ', '_').replace('-', '_')
        
        new_policy = {
            'name': name,
            'description': description,
            'accrual_method': accrual_method,
            'days_per_year': days_per_year,
            'accrual_cap': accrual_cap,
            'probation_period_days': probation_days,
            'min_service_months': min_service_months,
            'max_carryover': max_carryover,
            'eligible_employee_types': eligible_types,
            'created_date': datetime.now().strftime('%Y-%m-%d'),
            'active': True
        }
        
        # Ensure vacation policies structure exists
        if 'vacation_policies' not in manager.vacation_policies:
            manager.vacation_policies['vacation_policies'] = {}
        if 'policies' not in manager.vacation_policies['vacation_policies']:
            manager.vacation_policies['vacation_policies']['policies'] = {}
        
        # Add the new policy
        manager.vacation_policies['vacation_policies']['policies'][policy_id] = new_policy
        
        if manager.save_vacation_policies(manager.vacation_policies):
            ui.notify(f'✅ Vacation policy "{name}" created successfully!', type='positive')
            dialog.close()
        else:
            ui.notify('❌ Failed to save vacation policy', type='negative')
            
    except Exception as e:
        ui.notify(f'Error creating policy: {str(e)}', type='negative')


def reset_settings(manager):
    """Reset settings to default"""
    manager.holidays_data = manager.get_default_holidays()
    if manager.save_holidays(manager.holidays_data):
        ui.notify('Settings reset to default!', type='positive')
    else:
        ui.notify('Error resetting settings', type='negative')


class SetHolidays:
    """Main HR Holiday & Vacation Management System"""
    
    def __init__(self):
        """Initialize and display the HR system"""
        self.manager = HolidaysManager()
        self.current_tab = "dashboard"
        self.content_container = None
        self.show()
    
    @ui.refreshable
    def show_content(self):
        """Show content based on selected tab"""
        if self.current_tab == "dashboard":
            create_hr_dashboard(self.manager)
        elif self.current_tab == "vacation_tracking":
            create_vacation_tracking(self.manager)
        elif self.current_tab == "holiday_calendar":
            create_holiday_calendar(self.manager)
        elif self.current_tab == "vacation_policies":
            create_vacation_policies(self.manager)
        elif self.current_tab == "employee_balances":
            create_employee_balances(self.manager)
        elif self.current_tab == "blackout_periods":
            create_blackout_periods(self.manager)
        elif self.current_tab == "payroll_integration":
            create_payroll_integration(self.manager)
        elif self.current_tab == "compliance_reports":
            create_compliance_reports(self.manager)
        elif self.current_tab == "hr_settings":
            create_hr_settings(self.manager)
        else:
            create_hr_dashboard(self.manager)
    
    def switch_tab(self, tab_id):
        """Switch to a different tab"""
        self.current_tab = tab_id
        self.show_content.refresh()
    
    def show(self):
        """Main function to display the HR Holiday Management system"""
        
        with ui.column().classes('w-full min-h-screen bg-gray-50'):
            # Header section
            self.create_header()
            
            # Navigation tabs
            self.create_navigation_tabs()
            
            # Main content area that refreshes based on selected tab
            with ui.column().classes('flex-1 p-6'):
                self.show_content()
    
    def create_header(self):
        """Create the header section"""
        with ui.card().classes('w-full mb-6 bg-gradient-to-r from-blue-600 to-purple-600 text-white'):
            with ui.card_section().classes('p-8'):
                with ui.row().classes('items-center justify-between'):
                    with ui.column():
                        ui.label('🏢 HR Holiday & Vacation Management').classes('text-4xl font-bold mb-2')
                        ui.label('Comprehensive employee vacation tracking, holiday calendar, and HR policy management').classes('text-blue-100 text-lg')
                        
                        # Status indicators
                        with ui.row().classes('items-center gap-6 mt-4'):
                            ui.label('System Status: ').classes('text-blue-100')
                            ui.badge('Active', color='green').classes('px-3 py-1')
                            ui.label('•').classes('text-blue-100 mx-2')
                            ui.label('Last Sync: ').classes('text-blue-100')
                            ui.label(f'{datetime.now().strftime("%B %d, %Y at %I:%M %p")}').classes('text-white font-semibold')
                    
                    # Quick stats
                    with ui.column().classes('text-right'):
                        ui.label('HR Management Modules').classes('text-lg font-semibold mb-3')
                        with ui.row().classes('gap-4'):
                            self.create_stat_badge('📊', '9', 'Active Modules')
                            self.create_stat_badge('👥', '247', 'Employees')
                            self.create_stat_badge('📅', '12', 'Holidays')
    
    def create_stat_badge(self, icon, value, label):
        """Create a stat badge"""
        with ui.card().classes('bg-white/20 backdrop-blur-sm border-0'):
            with ui.card_section().classes('p-4 text-center'):
                ui.label(icon).classes('text-2xl mb-2')
                ui.label(value).classes('text-2xl font-bold')
                ui.label(label).classes('text-sm text-blue-100')
    
    def create_navigation_tabs(self):
        """Create navigation tabs"""
        tabs = [
            {"id": "dashboard", "name": "📊 Dashboard", "desc": "Overview & Analytics"},
            {"id": "vacation_tracking", "name": "🏖️ Vacation Tracking", "desc": "Employee Time Off"},
            {"id": "holiday_calendar", "name": "📅 Holiday Calendar", "desc": "Company Holidays"},
            {"id": "vacation_policies", "name": "📋 Vacation Policies", "desc": "Policy Management"},
            {"id": "employee_balances", "name": "⚖️ Employee Balances", "desc": "Balance Tracking"},
            {"id": "blackout_periods", "name": "🚫 Blackout Periods", "desc": "Restricted Dates"},
            {"id": "payroll_integration", "name": "💰 Payroll Integration", "desc": "Pay Calculations"},
            {"id": "compliance_reports", "name": "📑 Compliance Reports", "desc": "Regulatory Reports"},
            {"id": "hr_settings", "name": "⚙️ HR Settings", "desc": "System Configuration"}
        ]
        
        with ui.card().classes('w-full mb-6'):
            with ui.card_section().classes('p-0'):
                with ui.row().classes('w-full bg-gray-100 overflow-x-auto'):
                    for tab in tabs:
                        self.create_tab_button(tab)
    
    def create_tab_button(self, tab):
        """Create individual tab button"""
        is_active = self.current_tab == tab["id"]
        
        button_classes = (
            'flex-1 min-w-48 p-4 cursor-pointer border-b-4 transition-all duration-200 '
            f'{"bg-white border-blue-500 text-blue-600" if is_active else "hover:bg-gray-50 border-transparent text-gray-600 hover:text-blue-600"}'
        )
        
        with ui.element('div').classes(button_classes).on('click', lambda t=tab["id"]: self.switch_tab(t)):
            with ui.column().classes('items-center text-center'):
                ui.label(tab["name"]).classes(f'text-sm font-semibold {"text-blue-600" if is_active else ""}')
                ui.label(tab["desc"]).classes(f'text-xs mt-1 {"text-blue-500" if is_active else "text-gray-500"}')