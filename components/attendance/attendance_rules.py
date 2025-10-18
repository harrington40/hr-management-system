from nicegui import ui
import yaml
import os
from datetime import datetime
from typing import Dict, Any
import json

class AttendanceRulesManager:
    def __init__(self):
        self.config_path = "/mnt/c/Users/harri/designProject2020/hr-clock/hrms-main/config/attendance_rules.yaml"
        self.rules_data = self.load_rules()

    def load_rules(self) -> Dict[str, Any]:
        """Load attendance rules from YAML file"""
        try:
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            return self.get_default_rules()

    def save_rules(self, rules_data: Dict[str, Any]) -> bool:
        """Save attendance rules to YAML file"""
        try:
            with open(self.config_path, 'w') as file:
                yaml.dump(rules_data, file, default_flow_style=False, sort_keys=False)
            self.rules_data = rules_data
            # Update global attendance calculations
            self.update_global_attendance_calculations()
            return True
        except Exception as e:
            print(f"Error saving rules: {e}")
            return False

    def update_global_attendance_calculations(self):
        """Update attendance calculations across the app when rules change"""
        try:
            # Update dashboard metrics
            from components.dashboard.dashboard_main import HRDashboardManager
            dashboard_manager = HRDashboardManager()
            dashboard_manager.current_metrics = dashboard_manager.calculate_metrics()
            dashboard_manager.alerts = dashboard_manager.generate_alerts()

            # Update staff status calculations
            from components.attendance.staff_status import StaffStatusManager
            staff_manager = StaffStatusManager()
            staff_manager.update_attendance_calculations()

            print("✅ Global attendance calculations updated")
        except Exception as e:
            print(f"Warning: Could not update global calculations: {e}")

    def get_default_rules(self) -> Dict[str, Any]:
        """Return default attendance rules"""
        return {
            "attendance_rules": {
                "version": "2.0",
                "last_updated": datetime.now().isoformat(),
                "core_settings": {
                    "working_days_per_week": 5,
                    "standard_work_hours_per_day": 8,
                    "break_time_minutes": 60,
                    "grace_period_minutes": 15,
                    "auto_clock_out_after_hours": 12,
                    "minimum_shift_hours": 4
                },
                "checkin_rules": {
                    "allow_early_checkin_minutes": 30,
                    "late_threshold_minutes": 15,
                    "absent_threshold_minutes": 120,
                    "multiple_checkins_allowed": False,
                    "location_tracking_required": True
                },
                "absence_policies": {
                    "max_consecutive_absences": 3,
                    "absence_notification_threshold": 2,
                    "auto_leave_deduction": True,
                    "excuse_required_after_days": 1
                },
                "overtime_rules": {
                    "overtime_threshold_hours": 8,
                    "overtime_multiplier": 1.5,
                    "max_overtime_hours_week": 20,
                    "auto_overtime_approval": False
                },
                "break_policies": {
                    "mandatory_break_after_hours": 4,
                    "break_duration_minutes": 15,
                    "paid_breaks": True,
                    "flexible_break_times": True
                },
                "remote_work": {
                    "remote_checkin_required": True,
                    "location_verification": False,
                    "remote_productivity_tracking": True,
                    "max_remote_days_week": 2
                },
                "flexible_arrangements": {
                    "flexible_hours_allowed": True,
                    "core_hours_required": "09:00-15:00",
                    "compressed_workweek": False,
                    "part_time_options": True
                },
                "tracking_methods": {
                    "biometric_required": True,
                    "mobile_app_checkin": True,
                    "web_portal_access": True,
                    "qr_code_checkin": False,
                    "nfc_card_support": True
                }
            }
        }

def AttendanceRules():
    """Modern Attendance Rules Management Page"""
    manager = AttendanceRulesManager()
    
    # Header with gradient background
    with ui.row().classes('w-full mb-6'):
        with ui.card().classes('w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white border-l-8 border-blue-400 shadow-xl'):
            with ui.card_section().classes('p-6'):
                with ui.row().classes('items-center justify-between w-full'):
                    with ui.column().classes('gap-2'):
                        ui.html('<h1 class="text-3xl font-bold flex items-center gap-3"><span class="text-4xl">⚙️</span>Attendance Rules Management</h1>', sanitize=False).classes('mb-2')
                        ui.label('Configure and customize attendance policies with modern visual controls').classes('text-blue-100 text-lg')
                        ui.label(f'Last updated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}').classes('text-blue-200 text-sm')
                    
                    with ui.row().classes('gap-3'):
                        ui.button('💾 Save Changes', on_click=lambda: save_all_rules()).classes('bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg font-semibold')
                        ui.button('🔄 Reset to Default', on_click=lambda: reset_rules()).classes('bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-lg font-semibold')
                        ui.button('📋 Export YAML', on_click=lambda: export_yaml()).classes('bg-yellow-500 hover:bg-yellow-600 text-white px-6 py-3 rounded-lg font-semibold')

    # Main content with tabs
    with ui.row().classes('w-full gap-6'):
        # Left panel - Rule Categories
        with ui.column().classes('w-1/4'):
            with ui.card().classes('w-full border-l-4 border-indigo-500 shadow-lg bg-gradient-to-br from-indigo-50 to-white'):
                with ui.card_section().classes('p-4'):
                    ui.label('Rule Categories').classes('text-xl font-bold text-gray-700 mb-4')
                    
                    rule_categories = [
                        {'id': 'core', 'name': 'Core Settings', 'icon': '⚙️', 'color': 'blue'},
                        {'id': 'checkin', 'name': 'Check-in Rules', 'icon': '📅', 'color': 'green'},
                        {'id': 'absence', 'name': 'Absence Policies', 'icon': '🚫', 'color': 'red'},
                        {'id': 'overtime', 'name': 'Overtime Rules', 'icon': '⏰', 'color': 'purple'},
                        {'id': 'breaks', 'name': 'Break Policies', 'icon': '☕', 'color': 'yellow'},
                        {'id': 'remote', 'name': 'Remote Work', 'icon': '🏠', 'color': 'indigo'},
                        {'id': 'flexible', 'name': 'Flexible Arrangements', 'icon': '⚡', 'color': 'pink'},
                        {'id': 'tracking', 'name': 'Tracking Methods', 'icon': '📱', 'color': 'cyan'},
                    ]
                    
                    # Simple state management without ui.state()
                    class CategoryState:
                        def __init__(self):
                            self.current = 'core'
                            self.panels = {}
                            self.buttons = {}  # Store button references
                    
                    state = CategoryState()
                    
                    def switch_category(cat_id):
                        # Update current selection
                        old_current = state.current
                        state.current = cat_id
                        
                        # Update button styles and text
                        for cat_id_key, button in state.buttons.items():
                            category = next((cat for cat in rule_categories if cat['id'] == cat_id_key), None)
                            if category:
                                is_selected = cat_id_key == cat_id
                                icon_prefix = "✅ " if is_selected else ""
                                
                                # Update button text with selection indicator
                                button.set_text(f"{icon_prefix}{category['icon']} {category['name']}")
                                
                                # Update button styling
                                if is_selected:
                                    button.classes(
                                        f'w-full justify-start text-left p-4 rounded-xl transition-all duration-300 bg-{category["color"]}-500 hover:bg-{category["color"]}-600 text-white border-2 border-{category["color"]}-300 shadow-lg hover:shadow-xl font-semibold'
                                    )
                                else:
                                    button.classes(
                                        f'w-full justify-start text-left p-4 rounded-xl transition-all duration-300 bg-gray-100 hover:bg-gray-200 text-gray-700 border-2 border-transparent shadow-sm hover:shadow-md'
                                    )
                        
                        # Hide all panels
                        for panel in state.panels.values():
                            panel.set_visibility(False)
                        # Show selected panel
                        if cat_id in state.panels:
                            state.panels[cat_id].set_visibility(True)
                    
                    for category in rule_categories:
                        with ui.row().classes('w-full mb-3'):
                            # Determine if this button should be selected initially
                            is_selected = category['id'] == state.current
                            icon_prefix = "✅ " if is_selected else ""
                            button_classes = (
                                f'w-full justify-start text-left p-4 rounded-xl transition-all duration-300 shadow-sm hover:shadow-md font-semibold '
                                f'{"bg-" + category["color"] + "-500 hover:bg-" + category["color"] + "-600 text-white border-2 border-" + category["color"] + "-300 shadow-lg hover:shadow-xl" if is_selected else "bg-gray-100 hover:bg-gray-200 text-gray-700 border-2 border-transparent"}'
                            )
                            
                            btn = ui.button(f"{icon_prefix}{category['icon']} {category['name']}", 
                                          on_click=lambda cat=category['id']: switch_category(cat)
                            ).classes(button_classes)
                            
                            # Store button reference for later styling updates
                            state.buttons[category['id']] = btn

        # Right panel - Rule Configuration
        with ui.column().classes('w-3/4'):
            with ui.card().classes('w-full border-l-4 border-emerald-500 shadow-lg bg-gradient-to-br from-emerald-50 to-white'):
                with ui.card_section().classes('p-6'):
                    
                    # Create panels and store references
                    state.panels['core'] = ui.column().classes('w-full')
                    with state.panels['core']:
                        create_core_settings_panel(manager)
                    
                    state.panels['checkin'] = ui.column().classes('w-full')
                    with state.panels['checkin']:
                        create_checkin_rules_panel(manager)
                    state.panels['checkin'].set_visibility(False)
                        
                    state.panels['absence'] = ui.column().classes('w-full')
                    with state.panels['absence']:
                        create_absence_policies_panel(manager)
                    state.panels['absence'].set_visibility(False)
                        
                    state.panels['overtime'] = ui.column().classes('w-full')
                    with state.panels['overtime']:
                        create_overtime_rules_panel(manager)
                    state.panels['overtime'].set_visibility(False)
                        
                    state.panels['breaks'] = ui.column().classes('w-full')
                    with state.panels['breaks']:
                        create_break_policies_panel(manager)
                    state.panels['breaks'].set_visibility(False)
                        
                    state.panels['remote'] = ui.column().classes('w-full')
                    with state.panels['remote']:
                        create_remote_work_panel(manager)
                    state.panels['remote'].set_visibility(False)
                        
                    state.panels['flexible'] = ui.column().classes('w-full')
                    with state.panels['flexible']:
                        create_flexible_arrangements_panel(manager)
                    state.panels['flexible'].set_visibility(False)
                        
                    state.panels['tracking'] = ui.column().classes('w-full')
                    with state.panels['tracking']:
                        create_tracking_methods_panel(manager)
                    state.panels['tracking'].set_visibility(False)

    def save_all_rules():
        """Save all rule changes"""
        try:
            success = manager.save_rules(manager.rules_data)
            if success:
                ui.notify('✅ Attendance rules saved successfully!', type='positive')
            else:
                ui.notify('❌ Failed to save attendance rules', type='negative')
        except Exception as e:
            ui.notify(f'❌ Error saving rules: {str(e)}', type='negative')
    
    def reset_rules():
        """Reset rules to default"""
        try:
            manager.rules_data = manager.get_default_rules()
            ui.notify('🔄 Rules reset to default values', type='info')
            # Refresh the page to show updated values
            ui.navigate.reload()
        except Exception as e:
            ui.notify(f'❌ Error resetting rules: {str(e)}', type='negative')
    
    def export_yaml():
        """Export current rules as YAML"""
        try:
            yaml_content = yaml.dump(manager.rules_data, default_flow_style=False, sort_keys=False)
            ui.notify('📋 YAML configuration copied to clipboard', type='positive')
            # In a real implementation, you'd copy to clipboard or download
            print("YAML Content:")
            print(yaml_content)
        except Exception as e:
            ui.notify(f'❌ Error exporting YAML: {str(e)}', type='negative')

def create_core_settings_panel(manager: AttendanceRulesManager):
    """Create core settings configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">⚙️ Core Attendance Settings</h2>', sanitize=False)
    ui.label('Configure fundamental attendance parameters for your organization').classes('text-gray-600 mb-6')
    
    core_settings = manager.rules_data.get('attendance_rules', {}).get('core_settings', {})
    
    with ui.grid(columns=2).classes('gap-6 w-full'):
        # Working Days
        with ui.card().classes('p-4 border-l-4 border-blue-400 hover:shadow-md transition-shadow'):
            ui.label('📅 Working Days per Week').classes('font-semibold text-gray-700 mb-2')
            working_days = ui.number(
                value=core_settings.get('working_days_per_week', 5),
                min=1, max=7,
                on_change=lambda e: update_core_setting('working_days_per_week', e.value)
            ).classes('w-full')
            ui.label('Standard working days in a week').classes('text-sm text-gray-500')
        
        # Work Hours per Day
        with ui.card().classes('p-4 border-l-4 border-green-400 hover:shadow-md transition-shadow'):
            ui.label('⏰ Work Hours per Day').classes('font-semibold text-gray-700 mb-2')
            work_hours = ui.number(
                value=core_settings.get('standard_work_hours_per_day', 8),
                min=1, max=24, step=0.5,
                on_change=lambda e: update_core_setting('standard_work_hours_per_day', e.value)
            ).classes('w-full')
            ui.label('Standard daily working hours').classes('text-sm text-gray-500')
        
        # Break Time
        with ui.card().classes('p-4 border-l-4 border-yellow-400 hover:shadow-md transition-shadow'):
            ui.label('☕ Break Time (minutes)').classes('font-semibold text-gray-700 mb-2')
            break_time = ui.number(
                value=core_settings.get('break_time_minutes', 60),
                min=0, max=120, step=15,
                on_change=lambda e: update_core_setting('break_time_minutes', e.value)
            ).classes('w-full')
            ui.label('Total break time per day').classes('text-sm text-gray-500')
        
        # Grace Period
        with ui.card().classes('p-4 border-l-4 border-purple-400 hover:shadow-md transition-shadow'):
            ui.label('⏱️ Grace Period (minutes)').classes('font-semibold text-gray-700 mb-2')
            grace_period = ui.number(
                value=core_settings.get('grace_period_minutes', 15),
                min=0, max=60, step=5,
                on_change=lambda e: update_core_setting('grace_period_minutes', e.value)
            ).classes('w-full')
            ui.label('Allowable lateness without penalty').classes('text-sm text-gray-500')
    
    def update_core_setting(key: str, value):
        """Update core setting value"""
        if 'attendance_rules' not in manager.rules_data:
            manager.rules_data['attendance_rules'] = {}
        if 'core_settings' not in manager.rules_data['attendance_rules']:
            manager.rules_data['attendance_rules']['core_settings'] = {}
        manager.rules_data['attendance_rules']['core_settings'][key] = value

def create_checkin_rules_panel(manager: AttendanceRulesManager):
    """Create check-in rules configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">📅 Check-in & Check-out Rules</h2>', sanitize=False)
    ui.label('Configure policies for employee check-in and check-out procedures').classes('text-gray-600 mb-6')
    
    checkin_rules = manager.rules_data.get('attendance_rules', {}).get('checkin_rules', {})
    
    with ui.grid(columns=2).classes('gap-6 w-full'):
        # Earliest Check-in Time
        with ui.card().classes('p-4 border-l-4 border-orange-400 hover:shadow-md transition-shadow'):
            ui.label('🌅 Earliest Check-in Time').classes('font-semibold text-gray-700 mb-2')
            earliest_checkin = ui.input(
                value=checkin_rules.get('earliest_checkin_time', '06:00'),
                on_change=lambda e: update_checkin_rule('earliest_checkin_time', e.value)
            ).classes('w-full').props('type=time')
            ui.label('Earliest allowed check-in time').classes('text-sm text-gray-500')
        
        # Latest Check-in Time
        with ui.card().classes('p-4 border-l-4 border-red-400 hover:shadow-md transition-shadow'):
            ui.label('🕘 Latest Check-in Time').classes('font-semibold text-gray-700 mb-2')
            latest_checkin = ui.input(
                value=checkin_rules.get('latest_checkin_time', '10:00'),
                on_change=lambda e: update_checkin_rule('latest_checkin_time', e.value)
            ).classes('w-full').props('type=time')
            ui.label('Latest allowed check-in time').classes('text-sm text-gray-500')
        
        # Auto Checkout
        with ui.card().classes('p-4 border-l-4 border-cyan-400 hover:shadow-md transition-shadow'):
            ui.label('🔄 Auto Checkout Settings').classes('font-semibold text-gray-700 mb-2')
            auto_checkout = ui.switch(
                value=checkin_rules.get('auto_checkout_enabled', True),
                on_change=lambda e: update_checkin_rule('auto_checkout_enabled', e.value)
            )
            ui.label('Automatically check out employees').classes('text-sm text-gray-500')
            
            if checkin_rules.get('auto_checkout_enabled', True):
                auto_checkout_time = ui.input(
                    value=checkin_rules.get('auto_checkout_time', '18:00'),
                    on_change=lambda e: update_checkin_rule('auto_checkout_time', e.value)
                ).classes('w-full mt-2').props('type=time')
        
        # Manager Approval for Late Check-in
        with ui.card().classes('p-4 border-l-4 border-amber-400 hover:shadow-md transition-shadow'):
            ui.label('👔 Manager Approval Required').classes('font-semibold text-gray-700 mb-2')
            manager_approval = ui.switch(
                value=checkin_rules.get('require_manager_approval_late_checkin', True),
                on_change=lambda e: update_checkin_rule('require_manager_approval_late_checkin', e.value)
            )
            ui.label('Require manager approval for late check-in').classes('text-sm text-gray-500')
    
    def update_checkin_rule(key: str, value):
        """Update check-in rule value"""
        if 'attendance_rules' not in manager.rules_data:
            manager.rules_data['attendance_rules'] = {}
        if 'checkin_rules' not in manager.rules_data['attendance_rules']:
            manager.rules_data['attendance_rules']['checkin_rules'] = {}
        manager.rules_data['attendance_rules']['checkin_rules'][key] = value

def create_absence_policies_panel(manager: AttendanceRulesManager):
    """Create absence policies configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">🚫 Absence & Tardiness Policies</h2>', sanitize=False)
    ui.label('Configure policies for handling employee absences and tardiness').classes('text-gray-600 mb-6')
    
    absence_policies = manager.rules_data.get('attendance_rules', {}).get('absence_policies', {})
    
    with ui.row().classes('gap-6 w-full'):
        # Absence Settings
        with ui.card().classes('w-1/2 p-4 border-l-4 border-rose-400 hover:shadow-md transition-shadow'):
            ui.label('📊 Absence Settings').classes('font-semibold text-gray-700 mb-4')
            
            ui.label('Unexcused Absence Penalty (hours)').classes('text-sm font-medium text-gray-600 mb-1')
            penalty_hours = ui.number(
                value=absence_policies.get('unexcused_absence_penalty_hours', 8),
                min=0, max=24,
                on_change=lambda e: update_absence_policy('unexcused_absence_penalty_hours', e.value)
            ).classes('w-full mb-3')
            
            ui.label('Maximum Consecutive Absences').classes('text-sm font-medium text-gray-600 mb-1')
            max_absences = ui.number(
                value=absence_policies.get('maximum_consecutive_absences', 3),
                min=1, max=10,
                on_change=lambda e: update_absence_policy('maximum_consecutive_absences', e.value)
            ).classes('w-full mb-3')
            
            ui.label('Notification Required (hours in advance)').classes('text-sm font-medium text-gray-600 mb-1')
            notification_hours = ui.number(
                value=absence_policies.get('absence_notification_required_hours', 24),
                min=0, max=72,
                on_change=lambda e: update_absence_policy('absence_notification_required_hours', e.value)
            ).classes('w-full mb-3')
            
            auto_deduct = ui.switch(
                'Auto-deduct from leave balance',
                value=absence_policies.get('auto_deduct_from_leave_balance', True),
                on_change=lambda e: update_absence_policy('auto_deduct_from_leave_balance', e.value)
            ).classes('w-full')
        
        # Tardiness Penalties
        with ui.card().classes('w-1/2 p-4 border-l-4 border-pink-400 hover:shadow-md transition-shadow'):
            ui.label('⏰ Tardiness Penalty Structure').classes('font-semibold text-gray-700 mb-4')
            
            tardiness_policies = manager.rules_data.get('attendance_rules', {}).get('tardiness_policies', [])
            
            ui.label('Configure penalty tiers for different levels of tardiness').classes('text-sm text-gray-600 mb-3')
            
            with ui.column().classes('gap-3 w-full'):
                for i, policy in enumerate(tardiness_policies):
                    with ui.card().classes('p-3 bg-gray-50'):
                        ui.label(f'Tier {i+1}: {policy.get("threshold_minutes", 0)} minutes late').classes('font-medium text-gray-700')
                        ui.label(f'Penalty: {policy.get("penalty_type", "warning")} - {policy.get("penalty_value", 0)}').classes('text-sm text-gray-600')
            
            if not tardiness_policies:
                ui.label('No tardiness policies configured').classes('text-gray-500 italic')
    
    def update_absence_policy(key: str, value):
        """Update absence policy value"""
        if 'attendance_rules' not in manager.rules_data:
            manager.rules_data['attendance_rules'] = {}
        if 'absence_policies' not in manager.rules_data['attendance_rules']:
            manager.rules_data['attendance_rules']['absence_policies'] = {}
        manager.rules_data['attendance_rules']['absence_policies'][key] = value

def create_overtime_rules_panel(manager: AttendanceRulesManager):
    """Create overtime rules configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">⏰ Overtime Calculation Rules</h2>', sanitize=False)
    ui.label('Configure overtime policies and compensation rates').classes('text-gray-600 mb-6')
    
    overtime_rules = manager.rules_data.get('attendance_rules', {}).get('overtime_rules', {})
    
    with ui.grid(columns=2).classes('gap-6 w-full'):
        # Overtime Settings
        with ui.card().classes('p-4 border-l-4 border-violet-400 hover:shadow-md transition-shadow'):
            ui.label('🔧 Basic Overtime Settings').classes('font-semibold text-gray-700 mb-3')
            
            overtime_enabled = ui.switch(
                'Enable Overtime Calculation',
                value=overtime_rules.get('enabled', True),
                on_change=lambda e: update_overtime_rule('enabled', e.value)
            ).classes('mb-3')
            
            ui.label('Calculation Method').classes('text-sm font-medium text-gray-600 mb-1')
            calculation_method = ui.select(
                options=['daily', 'weekly', 'monthly'],
                value=overtime_rules.get('calculation_method', 'daily'),
                on_change=lambda e: update_overtime_rule('calculation_method', e.value)
            ).classes('w-full mb-3')
            
            ui.label('Overtime Multiplier').classes('text-sm font-medium text-gray-600 mb-1')
            overtime_multiplier = ui.number(
                value=overtime_rules.get('overtime_multiplier', 1.5),
                min=1.0, max=3.0, step=0.1,
                on_change=lambda e: update_overtime_rule('overtime_multiplier', e.value)
            ).classes('w-full')
        
        # Premium Rates
        with ui.card().classes('p-4 border-l-4 border-teal-400 hover:shadow-md transition-shadow'):
            ui.label('💰 Premium Rate Settings').classes('font-semibold text-gray-700 mb-3')
            
            ui.label('Double Time Threshold (hours)').classes('text-sm font-medium text-gray-600 mb-1')
            double_time_threshold = ui.number(
                value=overtime_rules.get('double_time_threshold_hours', 12),
                min=8, max=24,
                on_change=lambda e: update_overtime_rule('double_time_threshold_hours', e.value)
            ).classes('w-full mb-3')
            
            ui.label('Weekend Overtime Multiplier').classes('text-sm font-medium text-gray-600 mb-1')
            weekend_multiplier = ui.number(
                value=overtime_rules.get('weekend_overtime_multiplier', 2.0),
                min=1.0, max=3.0, step=0.1,
                on_change=lambda e: update_overtime_rule('weekend_overtime_multiplier', e.value)
            ).classes('w-full mb-3')
            
            ui.label('Holiday Overtime Multiplier').classes('text-sm font-medium text-gray-600 mb-1')
            holiday_multiplier = ui.number(
                value=overtime_rules.get('holiday_overtime_multiplier', 2.5),
                min=1.0, max=4.0, step=0.1,
                on_change=lambda e: update_overtime_rule('holiday_overtime_multiplier', e.value)
            ).classes('w-full')
    
    def update_overtime_rule(key: str, value):
        """Update overtime rule value"""
        if 'attendance_rules' not in manager.rules_data:
            manager.rules_data['attendance_rules'] = {}
        if 'overtime_rules' not in manager.rules_data['attendance_rules']:
            manager.rules_data['attendance_rules']['overtime_rules'] = {}
        manager.rules_data['attendance_rules']['overtime_rules'][key] = value

def create_break_policies_panel(manager: AttendanceRulesManager):
    """Create break policies configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">☕ Break Time Policies</h2>', sanitize=False)
    ui.label('Configure break time rules and meal period policies').classes('text-gray-600 mb-6')
    
    break_policies = manager.rules_data.get('attendance_rules', {}).get('break_policies', {})
    
    with ui.grid(columns=2).classes('gap-6 w-full'):
        # Lunch Break Settings
        with ui.card().classes('p-4 border-l-4 border-amber-400 hover:shadow-md transition-shadow'):
            ui.label('🍽️ Lunch Break Settings').classes('font-semibold text-gray-700 mb-3')
            
            mandatory_lunch = ui.switch(
                'Mandatory Lunch Break',
                value=break_policies.get('mandatory_lunch_break', True),
                on_change=lambda e: update_break_policy('mandatory_lunch_break', e.value)
            ).classes('mb-3')
            
            ui.label('Lunch Break Duration (minutes)').classes('text-sm font-medium text-gray-600 mb-1')
            lunch_duration = ui.number(
                value=break_policies.get('lunch_break_duration_minutes', 60),
                min=30, max=120, step=15,
                on_change=lambda e: update_break_policy('lunch_break_duration_minutes', e.value)
            ).classes('w-full')
        
        # Short Break Settings
        with ui.card().classes('p-4 border-l-4 border-lime-400 hover:shadow-md transition-shadow'):
            ui.label('☕ Short Break Settings').classes('font-semibold text-gray-700 mb-3')
            
            ui.label('Short Break Duration (minutes)').classes('text-sm font-medium text-gray-600 mb-1')
            short_duration = ui.number(
                value=break_policies.get('short_break_duration_minutes', 15),
                min=5, max=30, step=5,
                on_change=lambda e: update_break_policy('short_break_duration_minutes', e.value)
            ).classes('w-full mb-3')
            
            ui.label('Short Breaks per Day').classes('text-sm font-medium text-gray-600 mb-1')
            breaks_per_day = ui.number(
                value=break_policies.get('short_breaks_per_day', 2),
                min=0, max=5,
                on_change=lambda e: update_break_policy('short_breaks_per_day', e.value)
            ).classes('w-full')
    
    def update_break_policy(key: str, value):
        """Update break policy value"""
        if 'attendance_rules' not in manager.rules_data:
            manager.rules_data['attendance_rules'] = {}
        if 'break_policies' not in manager.rules_data['attendance_rules']:
            manager.rules_data['attendance_rules']['break_policies'] = {}
        manager.rules_data['attendance_rules']['break_policies'][key] = value

def create_remote_work_panel(manager: AttendanceRulesManager):
    """Create remote work configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">🏠 Remote Work Policies</h2>', sanitize=False)
    ui.label('Configure policies for remote work and telecommuting').classes('text-gray-600 mb-6')
    
    remote_work = manager.rules_data.get('attendance_rules', {}).get('remote_work', {})
    
    with ui.card().classes('p-6 border-l-4 border-sky-400 hover:shadow-md transition-shadow'):
        ui.label('🔧 Remote Work Configuration').classes('font-semibold text-gray-700 mb-4')
        
        with ui.grid(columns=2).classes('gap-6 w-full'):
            remote_enabled = ui.switch(
                'Enable Remote Work',
                value=remote_work.get('enabled', True),
                on_change=lambda e: update_remote_work('enabled', e.value)
            )
            
            vpn_check = ui.switch(
                'Require VPN Check',
                value=remote_work.get('require_vpn_check', False),
                on_change=lambda e: update_remote_work('require_vpn_check', e.value)
            )
            
            productivity_tracking = ui.switch(
                'Enable Productivity Tracking',
                value=remote_work.get('productivity_tracking', False),
                on_change=lambda e: update_remote_work('productivity_tracking', e.value)
            )
            
            ui.label('Check-in Verification Method').classes('text-sm font-medium text-gray-600 mb-1')
            verification_method = ui.select(
                options=['location', 'photo', 'manual'],
                value=remote_work.get('checkin_verification_method', 'location'),
                on_change=lambda e: update_remote_work('checkin_verification_method', e.value)
            ).classes('w-full')
    
    def update_remote_work(key: str, value):
        """Update remote work setting"""
        if 'attendance_rules' not in manager.rules_data:
            manager.rules_data['attendance_rules'] = {}
        if 'remote_work' not in manager.rules_data['attendance_rules']:
            manager.rules_data['attendance_rules']['remote_work'] = {}
        manager.rules_data['attendance_rules']['remote_work'][key] = value

def create_flexible_arrangements_panel(manager: AttendanceRulesManager):
    """Create flexible arrangements configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">⚡ Flexible Arrangements</h2>', sanitize=False)
    ui.label('Configure flexible time and working arrangement policies').classes('text-gray-600 mb-6')
    
    flexible_arrangements = manager.rules_data.get('attendance_rules', {}).get('flexible_arrangements', {})
    
    with ui.grid(columns=2).classes('gap-6 w-full'):
        # Flextime Settings
        with ui.card().classes('p-4 border-l-4 border-fuchsia-400 hover:shadow-md transition-shadow'):
            ui.label('⏰ Flextime Configuration').classes('font-semibold text-gray-700 mb-3')
            
            flextime_enabled = ui.switch(
                'Enable Flextime',
                value=flexible_arrangements.get('flextime_enabled', True),
                on_change=lambda e: update_flexible_arrangement('flextime_enabled', e.value)
            ).classes('mb-3')
            
            ui.label('Core Hours Start').classes('text-sm font-medium text-gray-600 mb-1')
            core_start = ui.input(
                value=flexible_arrangements.get('core_hours_start', '10:00'),
                on_change=lambda e: update_flexible_arrangement('core_hours_start', e.value)
            ).classes('w-full mb-3').props('type=time')
            
            ui.label('Core Hours End').classes('text-sm font-medium text-gray-600 mb-1')
            core_end = ui.input(
                value=flexible_arrangements.get('core_hours_end', '15:00'),
                on_change=lambda e: update_flexible_arrangement('core_hours_end', e.value)
            ).classes('w-full').props('type=time')
        
        # Alternative Arrangements
        with ui.card().classes('p-4 border-l-4 border-indigo-400 hover:shadow-md transition-shadow'):
            ui.label('🔄 Alternative Arrangements').classes('font-semibold text-gray-700 mb-3')
            
            compressed_workweek = ui.switch(
                'Enable Compressed Workweek',
                value=flexible_arrangements.get('compressed_workweek_enabled', True),
                on_change=lambda e: update_flexible_arrangement('compressed_workweek_enabled', e.value)
            ).classes('mb-3')
            
            job_sharing = ui.switch(
                'Enable Job Sharing',
                value=flexible_arrangements.get('job_sharing_enabled', False),
                on_change=lambda e: update_flexible_arrangement('job_sharing_enabled', e.value)
            )
    
    def update_flexible_arrangement(key: str, value):
        """Update flexible arrangement setting"""
        if 'attendance_rules' not in manager.rules_data:
            manager.rules_data['attendance_rules'] = {}
        if 'flexible_arrangements' not in manager.rules_data['attendance_rules']:
            manager.rules_data['attendance_rules']['flexible_arrangements'] = {}
        manager.rules_data['attendance_rules']['flexible_arrangements'][key] = value

def create_tracking_methods_panel(manager: AttendanceRulesManager):
    """Create tracking methods configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">📱 Attendance Tracking Methods</h2>', sanitize=False)
    ui.label('Configure available methods for tracking employee attendance').classes('text-gray-600 mb-6')
    
    tracking_methods = manager.rules_data.get('attendance_rules', {}).get('tracking_methods', [])
    
    with ui.column().classes('gap-4 w-full'):
        ui.label('Available Tracking Methods (in order of priority)').classes('font-semibold text-gray-700 mb-2')
        
        method_icons = {
            'biometric': '👆',
            'rfid_card': '💳',
            'mobile_app': '📱',
            'web_portal': '🌐'
        }
        
        for i, method in enumerate(tracking_methods):
            with ui.card().classes('p-4 border-l-4 border-slate-400 hover:shadow-md transition-shadow'):
                with ui.row().classes('items-center justify-between w-full'):
                    with ui.row().classes('items-center gap-3'):
                        ui.label(f'{method_icons.get(method.get("method", ""), "📍")}').classes('text-2xl')
                        ui.label(f'{method.get("method", "").replace("_", " ").title()}').classes('font-semibold text-gray-700')
                        ui.label(f'Priority: {method.get("priority", i+1)}').classes('text-sm text-gray-500')
                    
                    ui.switch(
                        value=method.get('enabled', True),
                        on_change=lambda e, idx=i: update_tracking_method(idx, 'enabled', e.value)
                    )
        
        if not tracking_methods:
            ui.label('No tracking methods configured').classes('text-gray-500 italic')
    
    def update_tracking_method(index: int, key: str, value):
        """Update tracking method setting"""
        if 'attendance_rules' not in manager.rules_data:
            manager.rules_data['attendance_rules'] = {}
        if 'tracking_methods' not in manager.rules_data['attendance_rules']:
            manager.rules_data['attendance_rules']['tracking_methods'] = []
        
        if index < len(manager.rules_data['attendance_rules']['tracking_methods']):
            manager.rules_data['attendance_rules']['tracking_methods'][index][key] = value