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

    with ui.column().classes('w-full bg-gradient-to-br from-slate-100 to-red-50 min-h-screen p-6 gap-6'):

        # ── Gradient Header ─────────────────────────────────────────────────
        with ui.card().classes('w-full rounded-2xl shadow-md text-white overflow-hidden') \
                .style('background: linear-gradient(135deg, #dc2626, #e11d48, #f59e0b);'):
            with ui.card_section().classes('px-8 py-6'):
                ui.html('<p style="font-size:.75rem;opacity:.75;letter-spacing:.08em;'
                        'text-transform:uppercase;margin-bottom:.5rem;">Attendance &#8250; Holiday &amp; Vacation</p>')
                with ui.row().classes('items-center gap-5 w-full justify-between'):
                    with ui.row().classes('items-center gap-5'):
                        ui.html('<div style="width:52px;height:52px;border-radius:.75rem;'
                                'background:rgba(255,255,255,.18);display:flex;align-items:center;'
                                'justify-content:center;font-size:1.6rem;flex-shrink:0;">&#128197;</div>')
                        with ui.column().classes('gap-1'):
                            ui.html('<h1 style="font-size:1.6rem;font-weight:900;margin:0;'
                                    'letter-spacing:-.02em;">HR Holiday &amp; Vacation Management</h1>')
                            ui.html('<p style="font-size:.9rem;opacity:.82;margin:0;">'
                                    'Comprehensive employee vacation tracking, holiday calendar &amp; HR policy management</p>')
                    with ui.row().classes('gap-3'):
                        ui.button('\U0001f4be Save All', on_click=lambda: save_all_hr_data(manager)) \
                            .style('background:rgba(255,255,255,.18);color:#fff;'
                                   'border:1px solid rgba(255,255,255,.35);border-radius:.75rem;'
                                   'padding:.45rem 1.1rem;font-size:.85rem;font-weight:600;')
                        ui.button('\U0001f4ca Report', on_click=lambda: generate_hr_report(manager)) \
                            .style('background:rgba(255,255,255,.18);color:#fff;'
                                   'border:1px solid rgba(255,255,255,.35);border-radius:.75rem;'
                                   'padding:.45rem 1.1rem;font-size:.85rem;font-weight:600;')
                        ui.button('\u2699\ufe0f Policy Builder', on_click=lambda: show_policy_builder(manager)) \
                            .style('background:rgba(255,255,255,.18);color:#fff;'
                                   'border:1px solid rgba(255,255,255,.35);border-radius:.75rem;'
                                   'padding:.45rem 1.1rem;font-size:.85rem;font-weight:600;')

        # ── Module Tabs ─────────────────────────────────────────────────────
        with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden'):
            tabs = ui.tabs().classes('w-full border-b border-slate-200')
            with tabs:
                t_dash       = ui.tab('Dashboard',         icon='dashboard')
                t_vacation   = ui.tab('Vacation Tracking', icon='beach_access')
                t_calendar   = ui.tab('Holiday Calendar',  icon='event')
                t_policies   = ui.tab('Policies',          icon='policy')
                t_balances   = ui.tab('Balances',          icon='balance')
                t_blackout   = ui.tab('Blackout Periods',  icon='block')
                t_payroll    = ui.tab('Payroll',           icon='payments')
                t_compliance = ui.tab('Compliance',        icon='verified')
                t_settings   = ui.tab('Settings',          icon='settings')

            with ui.tab_panels(tabs, value=t_dash).classes('w-full'):
                with ui.tab_panel(t_dash).classes('p-6'):
                    create_hr_dashboard(manager)
                with ui.tab_panel(t_vacation).classes('p-6'):
                    create_vacation_tracking(manager)
                with ui.tab_panel(t_calendar).classes('p-6'):
                    create_holiday_calendar(manager)
                with ui.tab_panel(t_policies).classes('p-6'):
                    create_vacation_policies(manager)
                with ui.tab_panel(t_balances).classes('p-6'):
                    create_employee_balances(manager)
                with ui.tab_panel(t_blackout).classes('p-6'):
                    create_blackout_periods(manager)
                with ui.tab_panel(t_payroll).classes('p-6'):
                    create_payroll_integration(manager)
                with ui.tab_panel(t_compliance).classes('p-6'):
                    create_compliance_reports(manager)
                with ui.tab_panel(t_settings).classes('p-6'):
                    create_hr_settings(manager)

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
            else:
                ui.notify('Failed to save holiday', type='negative')
                
        except ValueError:
            ui.notify('Invalid date format. Please use YYYY-MM-DD', type='negative')


def create_hr_dashboard(manager):
    """Create comprehensive HR dashboard with key metrics"""
    holidays_data      = manager.holidays_data.get('holidays_calendar', {})
    fixed_holidays     = holidays_data.get('fixed_holidays_2025', [])
    company_holidays   = holidays_data.get('company_holidays', [])
    religious_holidays = holidays_data.get('religious_holidays', [])
    vacation_policies  = manager.vacation_policies.get('vacation_policies', {}).get('policies', {})
    total_holidays     = len(fixed_holidays) + len(company_holidays) + len(religious_holidays)

    # ── KPI flex cards ──────────────────────────────────────────────────────
    _kpis = [
        {'icon': '\U0001f5d3', 'value': str(total_holidays), 'label': 'TOTAL HOLIDAYS',
         'sub': 'Across all categories', 'f': '#dc2626', 't': '#ef4444'},
        {'icon': '\U0001f4cb', 'value': str(len(vacation_policies)), 'label': 'VACATION POLICIES',
         'sub': 'Active policies', 'f': '#e11d48', 't': '#f43f5e'},
        {'icon': '\u23f3', 'value': '12', 'label': 'PENDING REQUESTS',
         'sub': 'Awaiting approval', 'f': '#f59e0b', 't': '#f97316'},
        {'icon': '\u2696\ufe0f', 'value': '14.2', 'label': 'AVG BALANCE (DAYS)',
         'sub': 'Per employee', 'f': '#0891b2', 't': '#0d9488'},
        {'icon': '\u2705', 'value': '98%', 'label': 'COMPLIANCE SCORE',
         'sub': 'Policy adherence', 'f': '#059669', 't': '#10b981'},
    ]
    with ui.element('div').style('display:flex;flex-wrap:nowrap;gap:1rem;width:100%;margin-bottom:1.5rem;'):
        for c in _kpis:
            ui.html(f'<div style="flex:1 1 0%;background:linear-gradient(135deg,{c["f"]},{c["t"]});'
                    'border-radius:1.25rem;padding:1.4rem 1.5rem;color:#fff;position:relative;overflow:hidden;'
                    'box-shadow:0 8px 24px -6px rgba(0,0,0,0.28);transition:transform .2s,box-shadow .2s;"'
                    ' onmouseover="this.style.transform=\'translateY(-5px)\';this.style.boxShadow=\'0 14px 32px -6px rgba(0,0,0,0.35)\'"'
                    ' onmouseout="this.style.transform=\'\';this.style.boxShadow=\'0 8px 24px -6px rgba(0,0,0,0.28)\'">'
                    '<div style="position:absolute;top:-18px;right:-18px;width:90px;height:90px;border-radius:50%;background:rgba(255,255,255,.12);"></div>'
                    '<div style="position:absolute;bottom:-12px;left:-12px;width:64px;height:64px;border-radius:50%;background:rgba(255,255,255,.08);"></div>'
                    f'<div style="width:48px;height:48px;border-radius:.75rem;background:rgba(255,255,255,.18);'
                    f'display:flex;align-items:center;justify-content:center;font-size:1.4rem;margin-bottom:.75rem;">{c["icon"]}</div>'
                    f'<div style="font-size:2rem;font-weight:900;letter-spacing:-.03em;line-height:1;">{c["value"]}</div>'
                    f'<div style="font-size:.72rem;text-transform:uppercase;letter-spacing:.1em;opacity:.8;margin-top:.3rem;">{c["label"]}</div>'
                    f'<div style="font-size:.68rem;opacity:.6;margin-top:.15rem;">{c["sub"]}</div></div>')

    # ── Two-column: Upcoming Dates | Quick Actions ───────────────────────────
    with ui.element('div').style('display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin-bottom:1.5rem;'):
        # Upcoming Important Dates
        with ui.card().classes('rounded-2xl shadow-md bg-white overflow-hidden'):
            with ui.element('div').style('background:linear-gradient(90deg,#dc2626,#e11d48);padding:1rem 1.5rem;'):
                ui.html('<h2 style="font-size:1rem;font-weight:700;color:#fff;margin:0;">\U0001f4c5 Upcoming Important Dates</h2>')
            with ui.element('div').classes('p-4'):
                all_holidays = []
                for cat in ['fixed_holidays_2025', 'company_holidays']:
                    all_holidays.extend(holidays_data.get(cat, []))
                today = date.today()
                upcoming = []
                for h in all_holidays:
                    try:
                        hd = datetime.strptime(h['date'], '%Y-%m-%d').date()
                        if hd >= today:
                            upcoming.append((h, hd))
                    except Exception:
                        pass
                upcoming.sort(key=lambda x: x[1])
                if upcoming:
                    for h, hd in upcoming[:5]:
                        days_until = (hd - today).days
                        badge_bg  = '#fef3c7' if h.get('type') == 'company' else '#fee2e2'
                        badge_col = '#92400e' if h.get('type') == 'company' else '#991b1b'
                        ui.html(f'<div style="display:flex;align-items:center;justify-content:space-between;'
                                f'padding:.55rem .75rem;border-radius:.75rem;margin-bottom:.45rem;'
                                f'background:#fafafa;border-left:3px solid #dc2626;">'
                                f'<div><div style="font-weight:600;font-size:.85rem;color:#1e293b;">{h["name"]}</div>'
                                f'<div style="font-size:.72rem;color:#64748b;">{hd.strftime("%b %d, %Y")} &bull; {days_until} days</div></div>'
                                f'<span style="font-size:.7rem;font-weight:700;padding:.2rem .55rem;border-radius:9999px;'
                                f'background:{badge_bg};color:{badge_col};">{h.get("type","company").title()}</span></div>')
                else:
                    ui.html('<p style="color:#94a3b8;font-style:italic;text-align:center;padding:1.5rem;">No upcoming holidays configured</p>')

        # Quick Actions
        with ui.card().classes('rounded-2xl shadow-md bg-white overflow-hidden'):
            with ui.element('div').style('background:linear-gradient(90deg,#e11d48,#f59e0b);padding:1rem 1.5rem;'):
                ui.html('<h2 style="font-size:1rem;font-weight:700;color:#fff;margin:0;">\U0001f680 Quick Actions</h2>')
            with ui.element('div').classes('p-4 flex flex-col gap-3'):
                ui.button('\u2795 Add New Holiday',
                         on_click=lambda: ui.notify('Use the Holiday Calendar tab to add holidays', type='info')
                         ).classes('w-full justify-start text-blue-700 bg-blue-50 hover:bg-blue-100 rounded-xl border border-blue-200 font-semibold')
                ui.button('\U0001f4cb Create Vacation Policy',
                         on_click=lambda: ui.notify('Use the Policies tab to manage vacation policies', type='info')
                         ).classes('w-full justify-start text-emerald-700 bg-emerald-50 hover:bg-emerald-100 rounded-xl border border-emerald-200 font-semibold')
                ui.button('\U0001f4ca Generate Reports',
                         on_click=lambda: ui.notify('Generating HR compliance report...', type='info')
                         ).classes('w-full justify-start text-purple-700 bg-purple-50 hover:bg-purple-100 rounded-xl border border-purple-200 font-semibold')
                ui.button('\U0001f4be Export Calendar',
                         on_click=lambda: ui.notify('Exporting holiday calendar...', type='info')
                         ).classes('w-full justify-start text-slate-700 bg-slate-50 hover:bg-slate-100 rounded-xl border border-slate-200 font-semibold')

    # ── Recent HR Activity ───────────────────────────────────────────────────
    with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden'):
        with ui.element('div').style('background:linear-gradient(90deg,#dc2626,#f59e0b);padding:1rem 1.5rem;'):
            ui.html('<h2 style="font-size:1rem;font-weight:700;color:#fff;margin:0;">\U0001f4cb Recent HR Activity</h2>')
        with ui.element('div').classes('p-4'):
            activities = [
                {'action': 'Holiday Added', 'details': 'Martin Luther King Jr. Day added to public holidays',
                 'time': '2h ago', 'icon': '\U0001f389', 'bg': '#fee2e2'},
                {'action': 'Policy Updated', 'details': 'Senior employee vacation policy \u2014 increased carryover days',
                 'time': '1d ago', 'icon': '\U0001f4cb', 'bg': '#dbeafe'},
                {'action': 'Report Generated', 'details': 'Q4 vacation utilization report generated',
                 'time': '2d ago', 'icon': '\U0001f4ca', 'bg': '#d1fae5'},
                {'action': 'Blackout Period Set', 'details': 'Year-end processing blackout period configured',
                 'time': '3d ago', 'icon': '\U0001f6ab', 'bg': '#fef3c7'},
            ]
            for a in activities:
                ui.html(f'<div style="display:flex;align-items:center;gap:1rem;padding:.65rem .9rem;'
                        f'border-radius:.75rem;margin-bottom:.45rem;background:{a["bg"]}55;">'
                        f'<div style="width:36px;height:36px;border-radius:.5rem;background:{a["bg"]};'
                        f'display:flex;align-items:center;justify-content:center;font-size:1.1rem;flex-shrink:0;">{a["icon"]}</div>'
                        f'<div style="flex:1;"><div style="font-weight:600;font-size:.85rem;color:#1e293b;">{a["action"]}</div>'
                        f'<div style="font-size:.75rem;color:#64748b;">{a["details"]}</div></div>'
                        f'<div style="font-size:.72rem;color:#94a3b8;white-space:nowrap;">{a["time"]}</div></div>')
def create_vacation_tracking(manager):
    """Create vacation tracking interface"""
    # ── Search bar ──────────────────────────────────────────────────────────
    with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden mb-4'):
        with ui.element('div').style('background:linear-gradient(90deg,#dc2626,#e11d48);padding:1rem 1.5rem;'):
            ui.html('<h2 style="font-size:1rem;font-weight:700;color:#fff;margin:0;">🏖️ Employee Vacation Tracking</h2>')
        with ui.element('div').classes('p-4'):
            with ui.row().classes('gap-3 items-center'):
                ui.input('Search employees...', placeholder='Name or ID').classes('flex-1')
                ui.select(['All Departments', 'Engineering', 'HR', 'Sales', 'Marketing'],
                          value='All Departments').classes('w-48')
                ui.button('🔍 Search',
                         on_click=lambda: ui.notify('Searching employees...', type='info')
                         ).classes('bg-red-600 text-white px-4 py-2 rounded-lg font-semibold')
                ui.button('📥 Import',
                         on_click=lambda: ui.notify('Import dialog would open here', type='info')
                         ).classes('bg-emerald-600 text-white px-4 py-2 rounded-lg font-semibold')

    # ── KPI summary strip ────────────────────────────────────────────────────
    _vcards = [
        {'label': 'Available Days',    'value': '1,247', 'sub': 'Total across all employees', 'f': '#059669', 't': '#10b981', 'icon': '📅'},
        {'label': 'Used This Year',    'value': '832',   'sub': 'Days taken so far',           'f': '#0891b2', 't': '#0284c7', 'icon': '✅'},
        {'label': 'Pending Requests',  'value': '47',    'sub': 'Awaiting approval',           'f': '#f59e0b', 't': '#f97316', 'icon': '⏳'},
        {'label': 'At-Risk Employees', 'value': '8',     'sub': 'May lose vacation days',      'f': '#dc2626', 't': '#e11d48', 'icon': '⚠️'},
    ]
    with ui.element('div').style('display:flex;flex-wrap:nowrap;gap:1rem;width:100%;margin-bottom:1.5rem;'):
        for c in _vcards:
            ui.html(
                f'<div style="flex:1 1 0%;background:linear-gradient(135deg,{c["f"]},{c["t"]});'
                'border-radius:1.25rem;padding:1.3rem 1.4rem;color:#fff;position:relative;overflow:hidden;'
                'box-shadow:0 6px 20px -5px rgba(0,0,0,0.25);">'
                '<div style="position:absolute;top:-14px;right:-14px;width:70px;height:70px;'
                'border-radius:50%;background:rgba(255,255,255,.12);"></div>'
                f'<div style="font-size:1.5rem;margin-bottom:.4rem;">{c["icon"]}</div>'
                f'<div style="font-size:1.9rem;font-weight:900;line-height:1;">{c["value"]}</div>'
                f'<div style="font-size:.8rem;font-weight:600;opacity:.9;margin-top:.25rem;">{c["label"]}</div>'
                f'<div style="font-size:.68rem;opacity:.65;margin-top:.1rem;">{c["sub"]}</div></div>'
            )

    # ── Employee balance table ───────────────────────────────────────────────
    with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden'):
        with ui.element('div').style('background:linear-gradient(90deg,#dc2626,#e11d48);padding:1rem 1.5rem;'):
            ui.html('<h2 style="font-size:1rem;font-weight:700;color:#fff;margin:0;">📊 Employee Vacation Balances</h2>')
        with ui.element('div').classes('p-4'):
            sample_employees = [
                {'id': 'EMP001', 'name': 'John Smith',    'dept': 'Engineering', 'policy': 'Senior',
                 'available': 18.5, 'used': 6.5,  'pending': 3.0, 'accrued': 20.0},
                {'id': 'EMP002', 'name': 'Sarah Johnson', 'dept': 'HR',          'policy': 'Standard',
                 'available': 12.0, 'used': 8.0,  'pending': 0.0, 'accrued': 15.0},
                {'id': 'EMP003', 'name': 'Mike Davis',    'dept': 'Sales',       'policy': 'Executive',
                 'available': 22.0, 'used': 3.0,  'pending': 5.0, 'accrued': 25.0},
                {'id': 'EMP004', 'name': 'Lisa Chen',     'dept': 'Marketing',   'policy': 'New Hire',
                 'available':  5.5, 'used': 2.5,  'pending': 0.0, 'accrued':  8.0},
                {'id': 'EMP005', 'name': 'Robert Wilson', 'dept': 'Engineering', 'policy': 'Senior',
                 'available':  0.5, 'used': 19.5, 'pending': 0.0, 'accrued': 20.0},
            ]
            thead = (
                '<thead><tr style="background:linear-gradient(90deg,#dc2626,#e11d48);color:#fff;">'
                '<th style="padding:.75rem 1rem;text-align:left;">Employee</th>'
                '<th style="padding:.75rem 1rem;text-align:left;">Department</th>'
                '<th style="padding:.75rem 1rem;text-align:left;">Policy</th>'
                '<th style="padding:.75rem 1rem;text-align:center;">Available</th>'
                '<th style="padding:.75rem 1rem;text-align:center;">Used</th>'
                '<th style="padding:.75rem 1rem;text-align:center;">Pending</th>'
                '<th style="padding:.75rem 1rem;text-align:center;">Total Accrued</th>'
                '<th style="padding:.75rem 1rem;text-align:center;">Actions</th>'
                '</tr></thead>'
            )
            tbody = '<tbody>'
            for i, emp in enumerate(sample_employees):
                row_bg = '#f8fafc' if i % 2 == 0 else '#ffffff'
                if emp['available'] > 10:
                    avail_style = 'background:#d1fae5;color:#065f46'
                elif emp['available'] < 5:
                    avail_style = 'background:#fee2e2;color:#991b1b'
                else:
                    avail_style = 'background:#fef3c7;color:#92400e'
                tbody += (
                    f'<tr style="background:{row_bg};">'
                    f'<td style="padding:.65rem 1rem;font-weight:600;color:#1e293b;">{emp["name"]}'
                    f'<br><span style="font-size:.72rem;color:#94a3b8;font-weight:400;">{emp["id"]}</span></td>'
                    f'<td style="padding:.65rem 1rem;color:#475569;">{emp["dept"]}</td>'
                    f'<td style="padding:.65rem 1rem;">'
                    f'<span style="padding:.2rem .6rem;border-radius:9999px;background:#dbeafe;color:#1d4ed8;font-size:.75rem;font-weight:700;">{emp["policy"]}</span></td>'
                    f'<td style="padding:.65rem 1rem;text-align:center;">'
                    f'<span style="padding:.2rem .55rem;border-radius:9999px;font-size:.8rem;font-weight:700;{avail_style};">{emp["available"]:.1f}</span></td>'
                    f'<td style="padding:.65rem 1rem;text-align:center;color:#475569;font-weight:600;">{emp["used"]:.1f}</td>'
                    f'<td style="padding:.65rem 1rem;text-align:center;">'
                    f'<span style="color:#f97316;font-weight:700;">{emp["pending"]:.1f}</span></td>'
                    f'<td style="padding:.65rem 1rem;text-align:center;color:#475569;">{emp["accrued"]:.1f}</td>'
                    f'<td style="padding:.65rem 1rem;text-align:center;">'
                    f'<span style="display:inline-flex;gap:.3rem;">'
                    f'<span style="padding:.25rem .5rem;border-radius:.35rem;background:#3b82f6;color:#fff;font-size:.75rem;cursor:pointer;">📝</span>'
                    f'<span style="padding:.25rem .5rem;border-radius:.35rem;background:#10b981;color:#fff;font-size:.75rem;cursor:pointer;">📊</span>'
                    f'</span></td></tr>'
                )
            tbody += '</tbody>'
            ui.html(
                '<table style="width:100%;border-collapse:collapse;font-size:.85rem;">'
                + thead + tbody + '</table>'
            )

def create_holiday_calendar(manager):
    """Create comprehensive holiday calendar interface"""
    holidays_data = manager.holidays_data.get('holidays_calendar', {})
    public_holidays = holidays_data.get('fixed_holidays_2025', [])
    company_holidays = holidays_data.get('company_holidays', [])
    religious_holidays = holidays_data.get('religious_holidays', [])
    floating_holidays = holidays_data.get('floating_holidays', [])
    public_count = len([h for h in public_holidays if h.get('type') == 'public'])

    # ── Section Header ────────────────────────────────────────────────────
    with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden mb-4'):
        with ui.element('div').style(
            'background:linear-gradient(90deg,#dc2626,#b91c1c);padding:1rem 1.5rem;'
        ):
            with ui.row().classes('items-center justify-between w-full'):
                ui.html('<h2 style="font-size:1.05rem;font-weight:700;color:#fff;margin:0;">'
                        '&#128197; Holiday Calendar Management</h2>')
                with ui.row().classes('gap-2'):
                    ui.button('+ Add Holiday',
                              on_click=lambda: show_add_holiday_dialog(manager)) \
                        .style('background:rgba(255,255,255,.18);color:#fff;'
                               'border:1px solid rgba(255,255,255,.35);border-radius:.75rem;'
                               'padding:.4rem 1rem;font-size:.82rem;font-weight:600;')
                    ui.button('\U0001f4e5 Import',
                              on_click=lambda: show_import_holidays_dialog()) \
                        .style('background:rgba(255,255,255,.18);color:#fff;'
                               'border:1px solid rgba(255,255,255,.35);border-radius:.75rem;'
                               'padding:.4rem 1rem;font-size:.82rem;font-weight:600;')
                    ui.button('\U0001f4e4 Export',
                              on_click=lambda: export_holiday_calendar()) \
                        .style('background:rgba(255,255,255,.18);color:#fff;'
                               'border:1px solid rgba(255,255,255,.35);border-radius:.75rem;'
                               'padding:.4rem 1rem;font-size:.82rem;font-weight:600;')
                    ui.button('\U0001f504 Sync',
                              on_click=lambda: sync_national_holidays()) \
                        .style('background:rgba(255,255,255,.18);color:#fff;'
                               'border:1px solid rgba(255,255,255,.35);border-radius:.75rem;'
                               'padding:.4rem 1rem;font-size:.82rem;font-weight:600;')

    # ── KPI cards ─────────────────────────────────────────────────────────
    _kpis = [
        {'icon': '\U0001f3db\ufe0f', 'value': str(public_count), 'label': 'Public Holidays',
         'sub': 'Federal mandated', 'f': '#dc2626', 't': '#b91c1c'},
        {'icon': '\U0001f3e2', 'value': str(len(company_holidays)), 'label': 'Company Holidays',
         'sub': 'Company specific', 'f': '#2563eb', 't': '#1d4ed8'},
        {'icon': '\U0001f54a\ufe0f', 'value': str(len(religious_holidays)), 'label': 'Religious',
         'sub': 'Optional observances', 'f': '#7c3aed', 't': '#6d28d9'},
        {'icon': '\U0001f388', 'value': str(len(floating_holidays)), 'label': 'Floating',
         'sub': 'Employee choice', 'f': '#059669', 't': '#047857'},
    ]
    with ui.element('div').style(
        'display:flex;flex-wrap:nowrap;gap:1rem;width:100%;margin-bottom:1.5rem;'
    ):
        for c in _kpis:
            ui.html(
                f'<div style="flex:1 1 0%;background:linear-gradient(135deg,{c["f"]},{c["t"]});'
                'border-radius:1.25rem;padding:1.3rem 1.4rem;color:#fff;position:relative;'
                'overflow:hidden;box-shadow:0 6px 20px -5px rgba(0,0,0,0.25);">'
                '<div style="position:absolute;top:-18px;right:-18px;width:80px;height:80px;'
                'border-radius:50%;background:rgba(255,255,255,.1);"></div>'
                f'<div style="font-size:1.6rem;margin-bottom:.35rem;">{c["icon"]}</div>'
                f'<div style="font-size:2rem;font-weight:900;line-height:1;">{c["value"]}</div>'
                f'<div style="font-size:.82rem;font-weight:700;opacity:.95;margin-top:.2rem;">{c["label"]}</div>'
                f'<div style="font-size:.75rem;opacity:.75;margin-top:.1rem;">{c["sub"]}</div>'
                '</div>'
            )

    # ── Category tabs ─────────────────────────────────────────────────────
    with ui.card().classes('w-full rounded-2xl shadow-sm bg-white overflow-hidden'):
        with ui.element('div').style('border-bottom:2px solid #f1f5f9;padding:.75rem 1.25rem .0rem;'):
            tabs = ui.tabs().classes('w-full')
            with tabs:
                public_tab   = ui.tab('Public Holidays')
                company_tab  = ui.tab('Company Holidays')
                religious_tab= ui.tab('Religious Holidays')
                floating_tab = ui.tab('Floating Holidays')

        with ui.tab_panels(tabs, value=public_tab).classes('w-full p-4'):
            with ui.tab_panel(public_tab):
                create_holiday_category_panel(manager, 'fixed_holidays_2025', 'public', 'Public')
            with ui.tab_panel(company_tab):
                create_holiday_category_panel(manager, 'company_holidays', 'company', 'Company')
            with ui.tab_panel(religious_tab):
                create_holiday_category_panel(manager, 'religious_holidays', 'religious', 'Religious')
            with ui.tab_panel(floating_tab):
                create_floating_holidays_panel(manager)

def create_holiday_category_panel(manager, category_key, holiday_type, category_name):
    """Create a panel for a specific holiday category"""
    holidays_data = manager.holidays_data.get('holidays_calendar', {})
    holidays = holidays_data.get(category_key, [])

    if holiday_type != 'all':
        holidays = [h for h in holidays if h.get('type') == holiday_type]

    with ui.row().classes('w-full gap-3 mb-4 items-center justify-between'):
        with ui.row().classes('gap-2'):
            ui.button(f'+ Add {category_name} Holiday',
                      on_click=lambda: show_add_specific_holiday_dialog(manager, holiday_type)) \
                .classes('bg-red-600 text-white px-4 py-2 rounded-xl font-semibold text-sm')
            if holidays:
                ui.button(f'\U0001f4ca Analyze Impact',
                          on_click=lambda: analyze_holiday_impact(holidays)) \
                    .classes('bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 '
                             'rounded-xl font-semibold text-sm px-4 py-2')

    if holidays:
        try:
            holidays.sort(key=lambda x: x.get('date', '2025-01-01'))
        except Exception:
            pass

        # Color scheme per type
        _pal = {
            'public':   {'from': '#dc2626', 'to': '#ef4444', 'badge_bg': '#fee2e2', 'badge_fg': '#991b1b'},
            'company':  {'from': '#2563eb', 'to': '#3b82f6', 'badge_bg': '#dbeafe', 'badge_fg': '#1e40af'},
            'religious':{'from': '#7c3aed', 'to': '#8b5cf6', 'badge_bg': '#ede9fe', 'badge_fg': '#5b21b6'},
        }
        pal = _pal.get(holiday_type, _pal['company'])

        thead = (
            '<thead><tr style="background:linear-gradient(90deg,#dc2626,#b91c1c);color:#fff;">'
            '<th style="padding:.75rem 1rem;text-align:left;font-size:.82rem;">Holiday</th>'
            '<th style="padding:.75rem 1rem;text-align:left;font-size:.82rem;">Date</th>'
            '<th style="padding:.75rem 1rem;text-align:center;font-size:.82rem;">Type</th>'
            '<th style="padding:.75rem 1rem;text-align:center;font-size:.82rem;">Paid</th>'
            '<th style="padding:.75rem 1rem;text-align:center;font-size:.82rem;">Mandatory</th>'
            '<th style="padding:.75rem 1rem;text-align:center;font-size:.82rem;">Pay Rate</th>'
            '</tr></thead>'
        )
        tbody = '<tbody>'
        for i, h in enumerate(holidays):
            bg = '#f8fafc' if i % 2 == 0 else '#ffffff'
            type_label = h.get('type', holiday_type).title()
            paid_html   = ('<span style="padding:.2rem .65rem;border-radius:9999px;background:#dcfce7;color:#166534;font-size:.75rem;font-weight:700;">Paid</span>'
                          if h.get('affects_payroll', True) else
                          '<span style="padding:.2rem .65rem;border-radius:9999px;background:#f1f5f9;color:#64748b;font-size:.75rem;font-weight:700;">Unpaid</span>')
            mand_html   = ('<span style="padding:.2rem .65rem;border-radius:9999px;background:#ffedd5;color:#9a3412;font-size:.75rem;font-weight:700;">Required</span>'
                          if h.get('is_mandatory', True) else
                          '<span style="padding:.2rem .65rem;border-radius:9999px;background:#f8fafc;color:#64748b;font-size:.75rem;font-weight:700;">Optional</span>')
            mult = h.get('compensation_multiplier', 1.5)
            tbody += (
                f'<tr style="background:{bg};border-bottom:1px solid #e2e8f0;">'
                f'<td style="padding:.7rem 1rem;font-weight:600;color:#1e293b;font-size:.88rem;">{h.get("name","—")}</td>'
                f'<td style="padding:.7rem 1rem;color:#475569;font-size:.85rem;">{h.get("date","—")}</td>'
                f'<td style="padding:.7rem 1rem;text-align:center;">'
                f'<span style="padding:.2rem .65rem;border-radius:9999px;background:{pal["badge_bg"]};color:{pal["badge_fg"]};font-size:.75rem;font-weight:700;">{type_label}</span>'
                f'</td>'
                f'<td style="padding:.7rem 1rem;text-align:center;">{paid_html}</td>'
                f'<td style="padding:.7rem 1rem;text-align:center;">{mand_html}</td>'
                f'<td style="padding:.7rem 1rem;text-align:center;color:#475569;font-size:.85rem;">{mult}x</td>'
                '</tr>'
            )
        tbody += '</tbody>'
        ui.html(
            '<div style="overflow-x:auto;border-radius:1rem;box-shadow:0 2px 12px -3px rgba(0,0,0,.1);">'
            f'<table style="width:100%;border-collapse:collapse;">{thead}{tbody}</table></div>'
        )

        # Action buttons row
        with ui.row().classes('gap-2 mt-3 justify-end'):
            ui.button('\u270f\ufe0f Edit Selected',
                      on_click=lambda: ui.notify('Select a holiday to edit', type='info')) \
                .classes('bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 px-4 py-2 rounded-xl text-sm font-semibold')
            ui.button('\U0001f5d1\ufe0f Remove Selected',
                      on_click=lambda: ui.notify('Select a holiday to remove', type='warning')) \
                .classes('bg-red-50 hover:bg-red-100 text-red-700 border border-red-200 px-4 py-2 rounded-xl text-sm font-semibold')
    else:
        ui.html(
            '<div style="padding:3rem 2rem;text-align:center;color:#94a3b8;">'
            f'<div style="font-size:2.5rem;margin-bottom:.75rem;">\U0001f4c5</div>'
            f'<div style="font-size:1rem;font-weight:600;">No {category_name.lower()} holidays configured yet.</div>'
            '<div style="font-size:.875rem;margin-top:.4rem;">Use the button above to add holidays.</div>'
            '</div>'
        )
        
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

    ui.html(
        '<p style="color:#64748b;font-size:.9rem;margin-bottom:1rem;">'
        'Floating holidays allow employees to choose when to take specific days off.</p>'
    )

    with ui.row().classes('w-full gap-2 mb-4'):
        ui.button('+ Add Floating Holiday',
                  on_click=lambda: show_add_floating_holiday_dialog(manager)) \
            .classes('bg-red-600 text-white px-4 py-2 rounded-xl font-semibold text-sm')

    if floating_holidays:
        with ui.element('div').style('display:flex;flex-wrap:wrap;gap:1rem;width:100%;'):
            for fh in floating_holidays:
                ui.html(
                    '<div style="flex:1 1 220px;border-radius:1rem;overflow:hidden;'
                    'box-shadow:0 4px 18px -4px rgba(0,0,0,0.12);background:#fff;"'
                    ' onmouseover="this.style.transform=\'translateY(-3px)\'"'
                    ' onmouseout="this.style.transform=\'\'">'
                    '<div style="height:5px;background:linear-gradient(90deg,#059669,#047857);"></div>'
                    '<div style="padding:1.1rem 1.2rem;">'
                    f'<div style="font-size:1.6rem;margin-bottom:.5rem;">\U0001f388</div>'
                    f'<div style="font-weight:700;font-size:.95rem;color:#1e293b;margin-bottom:.4rem;">{fh.get("name","—")}</div>'
                    f'<div style="font-size:.82rem;color:#64748b;">\U0001f4c5 {fh.get("days_available",1)} day(s) available</div>'
                    f'<div style="font-size:.82rem;color:#64748b;margin-top:.2rem;">\u23f0 Expires: {fh.get("expiry_date","No expiry")}</div>'
                    '</div></div>'
                )
    else:
        ui.html(
            '<div style="padding:3rem 2rem;text-align:center;color:#94a3b8;">'
            '<div style="font-size:2.5rem;margin-bottom:.75rem;">\U0001f388</div>'
            '<div style="font-size:1rem;font-weight:600;">No floating holiday policies configured yet.</div>'
            '</div>'
        )
    
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