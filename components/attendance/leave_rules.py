from nicegui import ui
import yaml
import os
from datetime import datetime
from typing import Dict, Any, List

class LeaveRulesManager:
    def __init__(self):
        self.config_path = "/mnt/c/Users/harri/designProject2020/hr-clock/hrms-main/config/leave_rules.yaml"
        self.rules_data = self.load_rules()
        
    def load_rules(self) -> Dict[str, Any]:
        """Load leave rules from YAML file"""
        try:
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            return self.get_default_rules()
            
    def save_rules(self, rules_data: Dict[str, Any]) -> bool:
        """Save leave rules to YAML file"""
        try:
            with open(self.config_path, 'w') as file:
                yaml.dump(rules_data, file, default_flow_style=False, sort_keys=False)
            self.rules_data = rules_data
            return True
        except Exception as e:
            print(f"Error saving rules: {e}")
            return False
            
    def get_default_rules(self) -> Dict[str, Any]:
        """Return default leave rules"""
        return {
            "leave_rules": {
                "version": "1.0",
                "general_settings": {
                    "leave_year_start_month": 1,
                    "maximum_carry_forward_days": 5,
                    "advance_leave_booking_days": 30
                },
                "leave_types": {}
            }
        }

def LeaveRules():
    """Modern Leave Rules Management Page"""
    manager = LeaveRulesManager()
    
    # Header with gradient background
    with ui.row().classes('w-full mb-6'):
        with ui.card().classes('w-full bg-gradient-to-r from-green-600 to-blue-600 text-white'):
            with ui.card_section().classes('p-6'):
                with ui.row().classes('items-center justify-between w-full'):
                    with ui.column().classes('gap-2'):
                        ui.html('<h1 class="text-3xl font-bold flex items-center gap-3"><span class="text-4xl">🏖️</span>Leave Rules Management</h1>', sanitize=False).classes('mb-2')
                        ui.label('Design and customize comprehensive leave policies with visual policy builder').classes('text-green-100 text-lg')
                        ui.label(f'Last updated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}').classes('text-green-200 text-sm')
                    
                    with ui.row().classes('gap-3'):
                        ui.button('💾 Save Configuration', on_click=lambda: save_all_rules()).classes('bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg font-semibold')
                        ui.button('📋 Export YAML', on_click=lambda: export_yaml()).classes('bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold')
                        ui.button('🔄 Import Template', on_click=lambda: import_template()).classes('bg-purple-500 hover:bg-purple-600 text-white px-6 py-3 rounded-lg font-semibold')

    # Main content with tabs
    with ui.row().classes('w-full gap-6'):
        # Left panel - Navigation
        with ui.column().classes('w-1/4'):
            with ui.card().classes('w-full'):
                with ui.card_section().classes('p-4'):
                    ui.label('Policy Categories').classes('text-xl font-bold text-gray-700 mb-4')
                    
                    policy_categories = [
                        {'id': 'general', 'name': 'General Settings', 'icon': '⚙️', 'color': 'blue'},
                        {'id': 'leave_types', 'name': 'Leave Types', 'icon': '📝', 'color': 'green'},
                        {'id': 'approval', 'name': 'Approval Workflow', 'icon': '✅', 'color': 'purple'},
                        {'id': 'calculation', 'name': 'Calculations', 'icon': '🧮', 'color': 'yellow'},
                        {'id': 'blackout', 'name': 'Blackout Periods', 'icon': '🚫', 'color': 'red'},
                        {'id': 'integration', 'name': 'Integrations', 'icon': '🔗', 'color': 'indigo'},
                        {'id': 'custom', 'name': 'Custom Rules', 'icon': '🎯', 'color': 'pink'},
                    ]
                    
                    # Simple state management without ui.state()
                    class CategoryState:
                        def __init__(self):
                            self.current = 'general'
                            self.panels = {}
                    
                    state = CategoryState()
                    
                    def switch_category(cat_id):
                        state.current = cat_id
                        # Hide all panels
                        for panel in state.panels.values():
                            panel.set_visibility(False)
                        # Show selected panel
                        if cat_id in state.panels:
                            state.panels[cat_id].set_visibility(True)
                    
                    for category in policy_categories:
                        with ui.row().classes('w-full mb-2'):
                            btn = ui.button(f"{category['icon']} {category['name']}", 
                                          on_click=lambda cat=category['id']: switch_category(cat)
                            ).classes(f'w-full justify-start text-left p-3 rounded-lg transition-all bg-gray-100 hover:bg-gray-200 text-gray-700')

        # Right panel - Configuration
        with ui.column().classes('w-3/4'):
            with ui.card().classes('w-full'):
                with ui.card_section().classes('p-6'):
                    
                    # Create panels and store references
                    state.panels['general'] = ui.column().classes('w-full')
                    with state.panels['general']:
                        create_general_settings_panel(manager)
                    
                    state.panels['leave_types'] = ui.column().classes('w-full')
                    with state.panels['leave_types']:
                        create_leave_types_panel(manager)
                    state.panels['leave_types'].set_visibility(False)
                        
                    state.panels['approval'] = ui.column().classes('w-full')
                    with state.panels['approval']:
                        create_approval_workflow_panel(manager)
                    state.panels['approval'].set_visibility(False)
                        
                    state.panels['calculation'] = ui.column().classes('w-full')
                    with state.panels['calculation']:
                        create_calculation_rules_panel(manager)
                    state.panels['calculation'].set_visibility(False)
                        
                    state.panels['blackout'] = ui.column().classes('w-full')
                    with state.panels['blackout']:
                        create_blackout_periods_panel(manager)
                    state.panels['blackout'].set_visibility(False)
                        
                    state.panels['integration'] = ui.column().classes('w-full')
                    with state.panels['integration']:
                        create_integration_panel(manager)
                    state.panels['integration'].set_visibility(False)
                        
                    state.panels['custom'] = ui.column().classes('w-full')
                    with state.panels['custom']:
                        create_custom_rules_panel(manager)
                    state.panels['custom'].set_visibility(False)

    def save_all_rules():
        """Save all rule changes"""
        try:
            success = manager.save_rules(manager.rules_data)
            if success:
                ui.notify('✅ Leave rules saved successfully!', type='positive')
            else:
                ui.notify('❌ Failed to save leave rules', type='negative')
        except Exception as e:
            ui.notify(f'❌ Error saving rules: {str(e)}', type='negative')
    
    def export_yaml():
        """Export current rules as YAML"""
        try:
            yaml_content = yaml.dump(manager.rules_data, default_flow_style=False, sort_keys=False)
            ui.notify('📋 YAML configuration exported successfully', type='positive')
            print("YAML Content:")
            print(yaml_content)
        except Exception as e:
            ui.notify(f'❌ Error exporting YAML: {str(e)}', type='negative')
    
    def import_template():
        """Import a leave policy template"""
        ui.notify('📥 Template import feature coming soon!', type='info')

def create_general_settings_panel(manager: LeaveRulesManager):
    """Create general settings configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">⚙️ General Leave Settings</h2>', sanitize=False)
    ui.label('Configure fundamental leave management parameters').classes('text-gray-600 mb-6')
    
    general_settings = manager.rules_data.get('leave_rules', {}).get('general_settings', {})
    
    with ui.grid(columns=2).classes('gap-6 w-full'):
        # Leave Year Settings
        with ui.card().classes('p-4'):
            ui.label('📅 Leave Year Configuration').classes('font-semibold text-gray-700 mb-3')
            
            ui.label('Leave Year Start Month').classes('text-sm font-medium text-gray-600 mb-1')
            start_month = ui.select(
                options={1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                        7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'},
                value=general_settings.get('leave_year_start_month', 1),
                on_change=lambda e: update_general_setting('leave_year_start_month', e.value)
            ).classes('w-full mb-3')
            
            ui.label('Leave Year Start Day').classes('text-sm font-medium text-gray-600 mb-1')
            start_day = ui.number(
                value=general_settings.get('leave_year_start_day', 1),
                min=1, max=31,
                on_change=lambda e: update_general_setting('leave_year_start_day', e.value)
            ).classes('w-full')
        
        # Carry Forward Settings
        with ui.card().classes('p-4'):
            ui.label('🔄 Carry Forward Policy').classes('font-semibold text-gray-700 mb-3')
            
            ui.label('Maximum Carry Forward Days').classes('text-sm font-medium text-gray-600 mb-1')
            carry_forward = ui.number(
                value=general_settings.get('maximum_carry_forward_days', 5),
                min=0, max=30,
                on_change=lambda e: update_general_setting('maximum_carry_forward_days', e.value)
            ).classes('w-full mb-3')
            
            ui.label('Advance Booking Limit (days)').classes('text-sm font-medium text-gray-600 mb-1')
            advance_booking = ui.number(
                value=general_settings.get('advance_leave_booking_days', 30),
                min=1, max=365,
                on_change=lambda e: update_general_setting('advance_leave_booking_days', e.value)
            ).classes('w-full mb-3')
            
            ui.label('Minimum Notice Period (days)').classes('text-sm font-medium text-gray-600 mb-1')
            notice_period = ui.number(
                value=general_settings.get('minimum_notice_period_days', 7),
                min=0, max=30,
                on_change=lambda e: update_general_setting('minimum_notice_period_days', e.value)
            ).classes('w-full')
        
        # Balance Management
        with ui.card().classes('p-4'):
            ui.label('💰 Balance Management').classes('font-semibold text-gray-700 mb-3')
            
            allow_negative = ui.switch(
                'Allow Negative Balance',
                value=general_settings.get('allow_negative_balance', False),
                on_change=lambda e: update_general_setting('allow_negative_balance', e.value)
            ).classes('mb-3')
            
            if general_settings.get('allow_negative_balance', False):
                ui.label('Maximum Negative Days').classes('text-sm font-medium text-gray-600 mb-1')
                max_negative = ui.number(
                    value=general_settings.get('maximum_negative_days', -5),
                    min=-30, max=0,
                    on_change=lambda e: update_general_setting('maximum_negative_days', e.value)
                ).classes('w-full')
        
        # Quick Settings
        with ui.card().classes('p-4 bg-blue-50'):
            ui.label('⚡ Quick Configuration Templates').classes('font-semibold text-gray-700 mb-3')
            
            with ui.column().classes('gap-2 w-full'):
                ui.button('🏢 Corporate Standard', on_click=lambda: apply_template('corporate')).classes('w-full bg-blue-500 text-white')
                ui.button('🏭 Manufacturing', on_click=lambda: apply_template('manufacturing')).classes('w-full bg-green-500 text-white')
                ui.button('🏥 Healthcare', on_click=lambda: apply_template('healthcare')).classes('w-full bg-red-500 text-white')
                ui.button('🎓 Education', on_click=lambda: apply_template('education')).classes('w-full bg-purple-500 text-white')
    
    def update_general_setting(key: str, value):
        """Update general setting value"""
        if 'leave_rules' not in manager.rules_data:
            manager.rules_data['leave_rules'] = {}
        if 'general_settings' not in manager.rules_data['leave_rules']:
            manager.rules_data['leave_rules']['general_settings'] = {}
        manager.rules_data['leave_rules']['general_settings'][key] = value
    
    def apply_template(template_type: str):
        """Apply a predefined template"""
        templates = {
            'corporate': {
                'leave_year_start_month': 1,
                'maximum_carry_forward_days': 5,
                'advance_leave_booking_days': 60,
                'minimum_notice_period_days': 7,
                'allow_negative_balance': False
            },
            'manufacturing': {
                'leave_year_start_month': 4,  # Fiscal year
                'maximum_carry_forward_days': 10,
                'advance_leave_booking_days': 30,
                'minimum_notice_period_days': 14,
                'allow_negative_balance': True,
                'maximum_negative_days': -3
            },
            'healthcare': {
                'leave_year_start_month': 1,
                'maximum_carry_forward_days': 0,  # Use it or lose it
                'advance_leave_booking_days': 90,
                'minimum_notice_period_days': 21,
                'allow_negative_balance': False
            },
            'education': {
                'leave_year_start_month': 9,  # Academic year
                'maximum_carry_forward_days': 15,
                'advance_leave_booking_days': 180,
                'minimum_notice_period_days': 30,
                'allow_negative_balance': True,
                'maximum_negative_days': -5
            }
        }
        
        if template_type in templates:
            for key, value in templates[template_type].items():
                update_general_setting(key, value)
            ui.notify(f'✅ {template_type.title()} template applied!', type='positive')
            ui.navigate.reload()

def create_leave_types_panel(manager: LeaveRulesManager):
    """Create leave types configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">📝 Leave Types & Allocations</h2>', sanitize=False)
    ui.label('Configure different types of leave and their allocation rules').classes('text-gray-600 mb-6')
    
    leave_types = manager.rules_data.get('leave_rules', {}).get('leave_types', {})
    
    # Leave Types Overview
    with ui.row().classes('w-full mb-6'):
        with ui.card().classes('w-full p-4 bg-gradient-to-r from-green-100 to-blue-100'):
            ui.label('📊 Leave Types Overview').classes('font-semibold text-gray-700 mb-3')
            
            if leave_types:
                with ui.grid(columns=4).classes('gap-4 w-full'):
                    for leave_type, config in leave_types.items():
                        with ui.card().classes('p-3 text-center'):
                            ui.label(config.get('icon', '📋')).classes('text-2xl mb-1')
                            ui.label(config.get('display_name', leave_type)).classes('font-semibold text-gray-700 text-sm')
                            ui.label(f"{config.get('allocation_rules', {}).get('base_allocation_days', 0)} days").classes('text-gray-600 text-xs')
            else:
                ui.label('No leave types configured yet').classes('text-gray-500 italic')

    # Leave Type Configuration
    with ui.column().classes('w-full gap-6'):
        for leave_type, config in leave_types.items():
            with ui.card().classes('w-full'):
                with ui.card_section().classes('p-4'):
                    # Leave Type Header
                    with ui.row().classes('items-center justify-between w-full mb-4'):
                        with ui.row().classes('items-center gap-3'):
                            ui.label(config.get('icon', '📋')).classes('text-2xl')
                            ui.label(config.get('display_name', leave_type)).classes('text-xl font-bold text-gray-700')
                            ui.chip(leave_type, color=config.get('color', '#64748b')).classes('text-white')
                        
                        with ui.row().classes('gap-2'):
                            ui.switch(
                                'Enabled',
                                value=config.get('enabled', True),
                                on_change=lambda e, lt=leave_type: update_leave_type_setting(lt, 'enabled', e.value)
                            )
                            ui.button('🗑️', on_click=lambda lt=leave_type: delete_leave_type(lt)).classes('bg-red-500 text-white p-1')
                    
                    # Configuration Grid
                    with ui.grid(columns=3).classes('gap-6 w-full'):
                        # Basic Settings
                        with ui.column().classes('gap-3'):
                            ui.label('Basic Configuration').classes('font-semibold text-gray-700 mb-2')
                            
                            ui.label('Display Name').classes('text-sm text-gray-600')
                            ui.input(
                                value=config.get('display_name', ''),
                                on_change=lambda e, lt=leave_type: update_leave_type_setting(lt, 'display_name', e.value)
                            ).classes('w-full')
                            
                            ui.label('Color').classes('text-sm text-gray-600')
                            ui.input(
                                value=config.get('color', '#64748b'),
                                on_change=lambda e, lt=leave_type: update_leave_type_setting(lt, 'color', e.value)
                            ).classes('w-full').props('type=color')
                            
                            ui.label('Icon/Emoji').classes('text-sm text-gray-600')
                            ui.input(
                                value=config.get('icon', '📋'),
                                on_change=lambda e, lt=leave_type: update_leave_type_setting(lt, 'icon', e.value)
                            ).classes('w-full')
                        
                        # Allocation Rules
                        with ui.column().classes('gap-3'):
                            ui.label('Allocation Rules').classes('font-semibold text-gray-700 mb-2')
                            
                            allocation_rules = config.get('allocation_rules', {})
                            
                            ui.label('Base Allocation (days)').classes('text-sm text-gray-600')
                            ui.number(
                                value=allocation_rules.get('base_allocation_days', 0),
                                min=0, max=365,
                                on_change=lambda e, lt=leave_type: update_allocation_rule(lt, 'base_allocation_days', e.value)
                            ).classes('w-full')
                            
                            ui.label('Probation Allocation (days)').classes('text-sm text-gray-600')
                            ui.number(
                                value=allocation_rules.get('probation_allocation_days', 0),
                                min=0, max=365,
                                on_change=lambda e, lt=leave_type: update_allocation_rule(lt, 'probation_allocation_days', e.value)
                            ).classes('w-full')
                            
                            ui.label('Accrual Method').classes('text-sm text-gray-600')
                            ui.select(
                                options=['monthly', 'quarterly', 'annual', 'daily'],
                                value=config.get('accrual_method', 'monthly'),
                                on_change=lambda e, lt=leave_type: update_leave_type_setting(lt, 'accrual_method', e.value)
                            ).classes('w-full')
                        
                        # Advanced Settings
                        with ui.column().classes('gap-3'):
                            ui.label('Advanced Settings').classes('font-semibold text-gray-700 mb-2')
                            
                            ui.switch(
                                'Carry Forward Allowed',
                                value=config.get('carry_forward_allowed', True),
                                on_change=lambda e, lt=leave_type: update_leave_type_setting(lt, 'carry_forward_allowed', e.value)
                            )
                            
                            ui.switch(
                                'Encashment Allowed',
                                value=config.get('encashment_allowed', False),
                                on_change=lambda e, lt=leave_type: update_leave_type_setting(lt, 'encashment_allowed', e.value)
                            )
                            
                            ui.switch(
                                'Documentation Required',
                                value=config.get('requires_documentation', False),
                                on_change=lambda e, lt=leave_type: update_leave_type_setting(lt, 'requires_documentation', e.value)
                            )
                            
                            if config.get('carries_forward_allowed', True):
                                ui.label('Max Carry Forward').classes('text-sm text-gray-600')
                                ui.number(
                                    value=config.get('maximum_carry_forward', 5),
                                    min=0, max=30,
                                    on_change=lambda e, lt=leave_type: update_leave_type_setting(lt, 'maximum_carry_forward', e.value)
                                ).classes('w-full')

    # Add New Leave Type Button
    with ui.row().classes('w-full mt-6'):
        ui.button('➕ Add New Leave Type', on_click=lambda: show_add_leave_type_dialog()).classes('bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg font-semibold')

    def update_leave_type_setting(leave_type: str, key: str, value):
        """Update leave type setting"""
        if 'leave_rules' not in manager.rules_data:
            manager.rules_data['leave_rules'] = {}
        if 'leave_types' not in manager.rules_data['leave_rules']:
            manager.rules_data['leave_rules']['leave_types'] = {}
        if leave_type not in manager.rules_data['leave_rules']['leave_types']:
            manager.rules_data['leave_rules']['leave_types'][leave_type] = {}
        
        manager.rules_data['leave_rules']['leave_types'][leave_type][key] = value
    
    def update_allocation_rule(leave_type: str, key: str, value):
        """Update allocation rule"""
        if 'leave_rules' not in manager.rules_data:
            manager.rules_data['leave_rules'] = {}
        if 'leave_types' not in manager.rules_data['leave_rules']:
            manager.rules_data['leave_rules']['leave_types'] = {}
        if leave_type not in manager.rules_data['leave_rules']['leave_types']:
            manager.rules_data['leave_rules']['leave_types'][leave_type] = {}
        if 'allocation_rules' not in manager.rules_data['leave_rules']['leave_types'][leave_type]:
            manager.rules_data['leave_rules']['leave_types'][leave_type]['allocation_rules'] = {}
        
        manager.rules_data['leave_rules']['leave_types'][leave_type]['allocation_rules'][key] = value
    
    def delete_leave_type(leave_type: str):
        """Delete a leave type"""
        if 'leave_rules' in manager.rules_data and 'leave_types' in manager.rules_data['leave_rules']:
            if leave_type in manager.rules_data['leave_rules']['leave_types']:
                del manager.rules_data['leave_rules']['leave_types'][leave_type]
                ui.notify(f'🗑️ {leave_type} leave type deleted', type='info')
                ui.navigate.reload()
    
    def show_add_leave_type_dialog():
        """Show dialog to add new leave type"""
        with ui.dialog() as dialog, ui.card().classes('w-96'):
            ui.label('Add New Leave Type').classes('text-xl font-bold mb-4')
            
            leave_type_id = ui.input('Leave Type ID (e.g., sick_leave)').classes('w-full mb-3')
            display_name = ui.input('Display Name').classes('w-full mb-3')
            icon = ui.input('Icon/Emoji', value='📋').classes('w-full mb-3')
            color = ui.input('Color', value='#64748b').classes('w-full mb-3').props('type=color')
            base_days = ui.number('Base Allocation (days)', value=0, min=0, max=365).classes('w-full mb-4')
            
            with ui.row().classes('gap-3 w-full justify-end'):
                ui.button('Cancel', on_click=dialog.close).classes('bg-gray-500 text-white')
                ui.button('Add Leave Type', on_click=lambda: add_new_leave_type(
                    leave_type_id.value, display_name.value, icon.value, color.value, base_days.value, dialog
                )).classes('bg-green-500 text-white')
        
        dialog.open()
    
    def add_new_leave_type(type_id: str, name: str, icon: str, color: str, days: int, dialog):
        """Add new leave type"""
        if not type_id or not name:
            ui.notify('❌ Please fill in all required fields', type='negative')
            return
        
        if 'leave_rules' not in manager.rules_data:
            manager.rules_data['leave_rules'] = {}
        if 'leave_types' not in manager.rules_data['leave_rules']:
            manager.rules_data['leave_rules']['leave_types'] = {}
        
        manager.rules_data['leave_rules']['leave_types'][type_id] = {
            'display_name': name,
            'icon': icon,
            'color': color,
            'enabled': True,
            'allocation_rules': {
                'base_allocation_days': days
            },
            'accrual_method': 'monthly',
            'carry_forward_allowed': True,
            'encashment_allowed': False
        }
        
        dialog.close()
        ui.notify(f'✅ {name} leave type added successfully!', type='positive')
        ui.navigate.reload()

def create_approval_workflow_panel(manager: LeaveRulesManager):
    """Create approval workflow configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">✅ Approval Workflow Configuration</h2>', sanitize=False)
    ui.label('Design multi-level approval workflows for leave requests').classes('text-gray-600 mb-6')
    
    # Add simplified approval workflow content
    with ui.card().classes('p-6'):
        ui.label('🔄 Workflow Configuration Coming Soon').classes('text-xl font-semibold text-gray-700 mb-3')
        ui.label('Advanced approval workflow configuration with multi-level approvers, escalation rules, and automated notifications will be available in the next update.').classes('text-gray-600')

def create_calculation_rules_panel(manager: LeaveRulesManager):
    """Create calculation rules configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">🧮 Leave Calculation Rules</h2>', sanitize=False)
    ui.label('Configure how leave balances and accruals are calculated').classes('text-gray-600 mb-6')
    
    calculation_rules = manager.rules_data.get('leave_rules', {}).get('calculation_rules', {})
    
    with ui.grid(columns=2).classes('gap-6 w-full'):
        # Basic Calculation Settings
        with ui.card().classes('p-4'):
            ui.label('⚙️ Basic Calculation Settings').classes('font-semibold text-gray-700 mb-3')
            
            pro_rata = ui.switch(
                'Pro-rata Calculation',
                value=calculation_rules.get('pro_rata_calculation', True),
                on_change=lambda e: update_calculation_rule('pro_rata_calculation', e.value)
            ).classes('mb-3')
            
            weekend_inclusion = ui.switch(
                'Include Weekends',
                value=calculation_rules.get('weekend_inclusion', False),
                on_change=lambda e: update_calculation_rule('weekend_inclusion', e.value)
            ).classes('mb-3')
            
            holiday_inclusion = ui.switch(
                'Include Public Holidays',
                value=calculation_rules.get('public_holiday_inclusion', False),
                on_change=lambda e: update_calculation_rule('public_holiday_inclusion', e.value)
            )
        
        # Minimum Leave Periods
        with ui.card().classes('p-4'):
            ui.label('📏 Minimum Leave Periods').classes('font-semibold text-gray-700 mb-3')
            
            ui.label('Half Day Minimum').classes('text-sm text-gray-600 mb-1')
            half_day = ui.number(
                value=calculation_rules.get('half_day_minimum', 0.5),
                min=0.1, max=1.0, step=0.1,
                on_change=lambda e: update_calculation_rule('half_day_minimum', e.value)
            ).classes('w-full mb-3')
            
            ui.label('Quarter Day Minimum').classes('text-sm text-gray-600 mb-1')
            quarter_day = ui.number(
                value=calculation_rules.get('quarter_day_minimum', 0.25),
                min=0.1, max=0.5, step=0.05,
                on_change=lambda e: update_calculation_rule('quarter_day_minimum', e.value)
            ).classes('w-full')
    
    def update_calculation_rule(key: str, value):
        """Update calculation rule"""
        if 'leave_rules' not in manager.rules_data:
            manager.rules_data['leave_rules'] = {}
        if 'calculation_rules' not in manager.rules_data['leave_rules']:
            manager.rules_data['leave_rules']['calculation_rules'] = {}
        manager.rules_data['leave_rules']['calculation_rules'][key] = value

def create_blackout_periods_panel(manager: LeaveRulesManager):
    """Create blackout periods configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">🚫 Blackout Periods</h2>', sanitize=False)
    ui.label('Configure periods when certain types of leave are restricted').classes('text-gray-600 mb-6')
    
    # Add simplified blackout periods content
    with ui.card().classes('p-6'):
        ui.label('📅 Blackout Period Management Coming Soon').classes('text-xl font-semibold text-gray-700 mb-3')
        ui.label('Configure restricted periods, department-specific blackouts, and emergency override rules.').classes('text-gray-600')

def create_integration_panel(manager: LeaveRulesManager):
    """Create integration configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">🔗 System Integrations</h2>', sanitize=False)
    ui.label('Configure integrations with other HR and business systems').classes('text-gray-600 mb-6')
    
    integrations = manager.rules_data.get('leave_rules', {}).get('integrations', {})
    
    with ui.grid(columns=2).classes('gap-6 w-full'):
        # Core Integrations
        with ui.card().classes('p-4'):
            ui.label('🔧 Core System Integrations').classes('font-semibold text-gray-700 mb-3')
            
            calendar_sync = ui.switch(
                'Calendar Sync',
                value=integrations.get('calendar_sync', True),
                on_change=lambda e: update_integration('calendar_sync', e.value)
            ).classes('mb-3')
            
            payroll_integration = ui.switch(
                'Payroll Integration',
                value=integrations.get('payroll_integration', True),
                on_change=lambda e: update_integration('payroll_integration', e.value)
            ).classes('mb-3')
            
            email_notifications = ui.switch(
                'Email Notifications',
                value=integrations.get('email_notifications', True),
                on_change=lambda e: update_integration('email_notifications', e.value)
            )
        
        # Mobile and Self-Service
        with ui.card().classes('p-4'):
            ui.label('📱 Mobile & Self-Service').classes('font-semibold text-gray-700 mb-3')
            
            mobile_app = ui.switch(
                'Mobile App Sync',
                value=integrations.get('mobile_app_sync', True),
                on_change=lambda e: update_integration('mobile_app_sync', e.value)
            ).classes('mb-3')
            
            project_management = ui.switch(
                'Project Management Sync',
                value=integrations.get('project_management_sync', False),
                on_change=lambda e: update_integration('project_management_sync', e.value)
            )
    
    def update_integration(key: str, value):
        """Update integration setting"""
        if 'leave_rules' not in manager.rules_data:
            manager.rules_data['leave_rules'] = {}
        if 'integrations' not in manager.rules_data['leave_rules']:
            manager.rules_data['leave_rules']['integrations'] = {}
        manager.rules_data['leave_rules']['integrations'][key] = value

def create_custom_rules_panel(manager: LeaveRulesManager):
    """Create custom rules configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">🎯 Custom Business Rules</h2>', sanitize=False)
    ui.label('Create custom rules and conditions for specific business requirements').classes('text-gray-600 mb-6')
    
    custom_rules = manager.rules_data.get('leave_rules', {}).get('custom_business_rules', [])
    
    # Display existing custom rules
    if custom_rules:
        with ui.column().classes('gap-4 w-full mb-6'):
            for i, rule in enumerate(custom_rules):
                with ui.card().classes('p-4'):
                    with ui.row().classes('items-center justify-between w-full'):
                        with ui.column().classes('flex-1'):
                            ui.label(rule.get('name', f'Rule {i+1}')).classes('font-semibold text-gray-700')
                            ui.label(f"Condition: {rule.get('condition', 'N/A')}").classes('text-sm text-gray-600')
                            ui.label(f"Action: {rule.get('action', 'N/A')}").classes('text-sm text-gray-600')
                        
                        with ui.row().classes('gap-2'):
                            ui.switch(
                                value=rule.get('enabled', True),
                                on_change=lambda e, idx=i: toggle_custom_rule(idx, e.value)
                            )
                            ui.button('🗑️', on_click=lambda idx=i: delete_custom_rule(idx)).classes('bg-red-500 text-white p-1')
    else:
        ui.label('No custom rules configured').classes('text-gray-500 italic')
    
    # Add new custom rule button
    ui.button('➕ Add Custom Rule', on_click=lambda: show_add_custom_rule_dialog()).classes('bg-purple-500 hover:bg-purple-600 text-white px-6 py-3 rounded-lg font-semibold')
    
    def toggle_custom_rule(index: int, enabled: bool):
        """Toggle custom rule enabled state"""
        if (index < len(manager.rules_data.get('leave_rules', {}).get('custom_business_rules', []))):
            manager.rules_data['leave_rules']['custom_business_rules'][index]['enabled'] = enabled
    
    def delete_custom_rule(index: int):
        """Delete custom rule"""
        if 'leave_rules' in manager.rules_data and 'custom_business_rules' in manager.rules_data['leave_rules']:
            if index < len(manager.rules_data['leave_rules']['custom_business_rules']):
                del manager.rules_data['leave_rules']['custom_business_rules'][index]
                ui.notify('🗑️ Custom rule deleted', type='info')
                ui.navigate.reload()
    
    def show_add_custom_rule_dialog():
        """Show dialog to add custom rule"""
        with ui.dialog() as dialog, ui.card().classes('w-96'):
            ui.label('Add Custom Business Rule').classes('text-xl font-bold mb-4')
            
            rule_name = ui.input('Rule Name').classes('w-full mb-3')
            condition = ui.input('Condition (e.g., department == "Sales")').classes('w-full mb-3')
            action = ui.input('Action (e.g., require_manager_approval)').classes('w-full mb-4')
            
            with ui.row().classes('gap-3 w-full justify-end'):
                ui.button('Cancel', on_click=dialog.close).classes('bg-gray-500 text-white')
                ui.button('Add Rule', on_click=lambda: add_custom_rule(
                    rule_name.value, condition.value, action.value, dialog
                )).classes('bg-purple-500 text-white')
        
        dialog.open()
    
    def add_custom_rule(name: str, condition: str, action: str, dialog):
        """Add new custom rule"""
        if not name or not condition or not action:
            ui.notify('❌ Please fill in all fields', type='negative')
            return
        
        if 'leave_rules' not in manager.rules_data:
            manager.rules_data['leave_rules'] = {}
        if 'custom_business_rules' not in manager.rules_data['leave_rules']:
            manager.rules_data['leave_rules']['custom_business_rules'] = []
        
        new_rule = {
            'name': name,
            'condition': condition,
            'action': action,
            'enabled': True
        }
        
        manager.rules_data['leave_rules']['custom_business_rules'].append(new_rule)
        
        dialog.close()
        ui.notify(f'✅ Custom rule "{name}" added successfully!', type='positive')
        ui.navigate.reload()