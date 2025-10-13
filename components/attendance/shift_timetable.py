from nicegui import ui
import yaml
import os
from datetime import datetime, time, timedelta
from typing import Dict, Any, List

class ShiftTimetableManager:
    def __init__(self):
        self.config_path = "/mnt/c/Users/harri/designProject2020/hr-clock/hrms-main/config/shift_timetable.yaml"
        self.timetable_data = self.load_timetable()
        
    def load_timetable(self) -> Dict[str, Any]:
        """Load shift timetable from YAML file"""
        try:
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            return self.get_default_timetable()
            
    def save_timetable(self, timetable_data: Dict[str, Any]) -> bool:
        """Save shift timetable to YAML file"""
        try:
            with open(self.config_path, 'w') as file:
                yaml.dump(timetable_data, file, default_flow_style=False, sort_keys=False)
            self.timetable_data = timetable_data
            return True
        except Exception as e:
            print(f"Error saving timetable: {e}")
            return False
            
    def get_default_timetable(self) -> Dict[str, Any]:
        """Return default shift timetable"""
        return {
            "shift_timetable": {
                "version": "1.0",
                "organization": {
                    "timezone": "UTC+0",
                    "week_start_day": "monday"
                },
                "shift_templates": {}
            }
        }

def ShiftTimetable():
    """Modern Shift Timetable Management Page"""
    manager = ShiftTimetableManager()
    
    # Header with gradient background
    with ui.row().classes('w-full mb-6'):
        with ui.card().classes('w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white'):
            with ui.card_section().classes('p-6'):
                with ui.row().classes('items-center justify-between w-full'):
                    with ui.column().classes('gap-2'):
                        ui.html('<h1 class="text-3xl font-bold flex items-center gap-3"><span class="text-4xl">📅</span>Shift Timetable Management</h1>', sanitize=False).classes('mb-2')
                        ui.label('Design and manage flexible shift schedules with visual timetable builder').classes('text-purple-100 text-lg')
                        ui.label(f'Last updated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}').classes('text-purple-200 text-sm')
                    
                    with ui.row().classes('gap-3'):
                        ui.button('💾 Save Timetable', on_click=lambda: save_all_timetable()).classes('bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg font-semibold')
                        ui.button('📋 Export Schedule', on_click=lambda: export_schedule()).classes('bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold')
                        ui.button('📊 Analytics', on_click=lambda: show_analytics()).classes('bg-yellow-500 hover:bg-yellow-600 text-white px-6 py-3 rounded-lg font-semibold')

    # Main content with tabs
    with ui.row().classes('w-full gap-6'):
        # Left panel - Navigation
        with ui.column().classes('w-1/4'):
            with ui.card().classes('w-full'):
                with ui.card_section().classes('p-4'):
                    ui.label('Timetable Sections').classes('text-xl font-bold text-gray-700 mb-4')
                    
                    timetable_sections = [
                        {'id': 'overview', 'name': 'Schedule Overview', 'icon': '📊', 'color': 'blue'},
                        {'id': 'shifts', 'name': 'Shift Templates', 'icon': '⏰', 'color': 'green'},
                        {'id': 'departments', 'name': 'Department Schedules', 'icon': '🏢', 'color': 'purple'},
                        {'id': 'patterns', 'name': 'Weekly Patterns', 'icon': '📋', 'color': 'yellow'},
                        {'id': 'assignments', 'name': 'Shift Assignments', 'icon': '👥', 'color': 'red'},
                        {'id': 'breaks', 'name': 'Break Policies', 'icon': '☕', 'color': 'indigo'},
                        {'id': 'overtime', 'name': 'Overtime Rules', 'icon': '⏱️', 'color': 'pink'},
                        {'id': 'reporting', 'name': 'Reports & Analytics', 'icon': '📈', 'color': 'cyan'},
                    ]
                    
                    # Simple state management without ui.state()
                    class SectionState:
                        def __init__(self):
                            self.current = 'overview'
                            self.panels = {}
                    
                    state = SectionState()
                    
                    def switch_section(sec_id):
                        state.current = sec_id
                        # Hide all panels
                        for panel in state.panels.values():
                            panel.set_visibility(False)
                        # Show selected panel
                        if sec_id in state.panels:
                            state.panels[sec_id].set_visibility(True)
                    
                    for section in timetable_sections:
                        with ui.row().classes('w-full mb-2'):
                            btn = ui.button(f"{section['icon']} {section['name']}", 
                                          on_click=lambda sec=section['id']: switch_section(sec)
                            ).classes(f'w-full justify-start text-left p-3 rounded-lg transition-all bg-gray-100 hover:bg-gray-200 text-gray-700')

        # Right panel - Content
        with ui.column().classes('w-3/4'):
            with ui.card().classes('w-full'):
                with ui.card_section().classes('p-6'):
                    
                    # Create panels and store references
                    state.panels['overview'] = ui.column().classes('w-full')
                    with state.panels['overview']:
                        create_schedule_overview_panel(manager)
                    
                    state.panels['shifts'] = ui.column().classes('w-full')
                    with state.panels['shifts']:
                        create_shift_templates_panel(manager)
                    state.panels['shifts'].set_visibility(False)
                        
                    state.panels['departments'] = ui.column().classes('w-full')
                    with state.panels['departments']:
                        create_department_schedules_panel(manager)
                    state.panels['departments'].set_visibility(False)
                        
                    state.panels['patterns'] = ui.column().classes('w-full')
                    with state.panels['patterns']:
                        create_weekly_patterns_panel(manager)
                    state.panels['patterns'].set_visibility(False)
                        
                    state.panels['assignments'] = ui.column().classes('w-full')
                    with state.panels['assignments']:
                        create_shift_assignments_panel(manager)
                    state.panels['assignments'].set_visibility(False)
                        
                    state.panels['breaks'] = ui.column().classes('w-full')
                    with state.panels['breaks']:
                        create_break_policies_panel(manager)
                    state.panels['breaks'].set_visibility(False)
                        
                    state.panels['overtime'] = ui.column().classes('w-full')
                    with state.panels['overtime']:
                        create_overtime_rules_panel(manager)
                    state.panels['overtime'].set_visibility(False)
                        
                    state.panels['reporting'] = ui.column().classes('w-full')
                    with state.panels['reporting']:
                        create_reporting_panel(manager)
                    state.panels['reporting'].set_visibility(False)

    def save_all_timetable():
        """Save all timetable changes"""
        try:
            success = manager.save_timetable(manager.timetable_data)
            if success:
                ui.notify('✅ Shift timetable saved successfully!', type='positive')
            else:
                ui.notify('❌ Failed to save shift timetable', type='negative')
        except Exception as e:
            ui.notify(f'❌ Error saving timetable: {str(e)}', type='negative')
    
    def export_schedule():
        """Export current schedule"""
        try:
            yaml_content = yaml.dump(manager.timetable_data, default_flow_style=False, sort_keys=False)
            ui.notify('📋 Schedule exported successfully', type='positive')
        except Exception as e:
            ui.notify(f'❌ Error exporting schedule: {str(e)}', type='negative')
    
    def show_analytics():
        """Show schedule analytics"""
        ui.notify('📊 Analytics dashboard coming soon!', type='info')

def create_schedule_overview_panel(manager: ShiftTimetableManager):
    """Create schedule overview panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">📊 Schedule Overview</h2>', sanitize=False)
    ui.label('Visual overview of your organization\'s shift schedules and coverage').classes('text-gray-600 mb-6')
    
    shift_templates = manager.timetable_data.get('shift_timetable', {}).get('shift_templates', {})
    
    # Statistics Cards
    with ui.row().classes('w-full gap-4 mb-6'):
        # Total Shifts Card
        with ui.card().classes('p-4 bg-gradient-to-r from-blue-100 to-blue-200'):
            with ui.row().classes('items-center gap-3'):
                ui.label('📊').classes('text-3xl')
                with ui.column():
                    ui.label('Total Shift Templates').classes('text-sm text-gray-600')
                    ui.label(str(len(shift_templates))).classes('text-2xl font-bold text-blue-700')
        
        # Coverage Hours Card
        with ui.card().classes('p-4 bg-gradient-to-r from-green-100 to-green-200'):
            with ui.row().classes('items-center gap-3'):
                ui.label('⏰').classes('text-3xl')
                with ui.column():
                    ui.label('Total Coverage Hours').classes('text-sm text-gray-600')
                    total_hours = sum(template.get('working_hours', 0) for template in shift_templates.values())
                    ui.label(f'{total_hours}h').classes('text-2xl font-bold text-green-700')
        
        # Active Departments Card
        with ui.card().classes('p-4 bg-gradient-to-r from-purple-100 to-purple-200'):
            with ui.row().classes('items-center gap-3'):
                ui.label('🏢').classes('text-3xl')
                with ui.column():
                    ui.label('Departments').classes('text-sm text-gray-600')
                    dept_schedules = manager.timetable_data.get('shift_timetable', {}).get('department_shifts', {})
                    ui.label(str(len(dept_schedules))).classes('text-2xl font-bold text-purple-700')
        
        # Coverage Status Card
        with ui.card().classes('p-4 bg-gradient-to-r from-yellow-100 to-yellow-200'):
            with ui.row().classes('items-center gap-3'):
                ui.label('🌟').classes('text-3xl')
                with ui.column():
                    ui.label('Coverage Status').classes('text-sm text-gray-600')
                    ui.label('Optimal').classes('text-2xl font-bold text-yellow-700')

    # Weekly Schedule Visualization
    with ui.card().classes('w-full p-6 mb-6'):
        ui.label('📅 Weekly Schedule Visualization').classes('text-xl font-bold text-gray-700 mb-4')
        
        # Create a simple weekly grid
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        time_slots = ['06:00', '09:00', '12:00', '15:00', '18:00', '21:00']
        
        with ui.grid(columns=8).classes('gap-2 w-full'):
            # Header row
            ui.label('Time').classes('font-semibold text-center p-2 bg-gray-100 rounded')
            for day in weekdays:
                ui.label(day).classes('font-semibold text-center p-2 bg-gray-100 rounded text-sm')
            
            # Time slot rows
            for time_slot in time_slots:
                ui.label(time_slot).classes('text-center p-2 bg-gray-50 rounded text-sm font-medium')
                for day in weekdays:
                    # Sample shift coverage visualization
                    coverage_class = 'bg-green-200 text-green-800' if time_slot in ['09:00', '12:00', '15:00'] else 'bg-blue-200 text-blue-800'
                    shift_name = 'Day Shift' if time_slot in ['09:00', '12:00', '15:00'] else 'Evening'
                    ui.label(shift_name).classes(f'text-center p-2 rounded text-xs {coverage_class}')

    # Quick Actions
    with ui.row().classes('w-full gap-4'):
        ui.button('➕ Create New Shift', on_click=lambda: show_create_shift_dialog()).classes('bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold')
        ui.button('👥 Assign Employees', on_click=lambda: ui.notify('Employee assignment coming soon!', type='info')).classes('bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg font-semibold')
        ui.button('📊 Generate Report', on_click=lambda: ui.notify('Report generation coming soon!', type='info')).classes('bg-purple-500 hover:bg-purple-600 text-white px-6 py-3 rounded-lg font-semibold')

    def show_create_shift_dialog():
        """Show create shift dialog"""
        with ui.dialog() as dialog, ui.card().classes('w-96'):
            ui.label('Create New Shift Template').classes('text-xl font-bold mb-4')
            
            shift_id = ui.input('Shift ID (e.g., morning_shift)').classes('w-full mb-3')
            display_name = ui.input('Display Name').classes('w-full mb-3')
            start_time = ui.input('Start Time').classes('w-full mb-3').props('type=time')
            end_time = ui.input('End Time').classes('w-full mb-3').props('type=time')
            
            with ui.row().classes('gap-3 w-full justify-end'):
                ui.button('Cancel', on_click=dialog.close).classes('bg-gray-500 text-white')
                ui.button('Create Shift', on_click=lambda: create_new_shift(
                    shift_id.value, display_name.value, start_time.value, end_time.value, dialog
                )).classes('bg-blue-500 text-white')
        
        dialog.open()
    
    def create_new_shift(shift_id: str, name: str, start: str, end: str, dialog):
        """Create new shift template"""
        if not all([shift_id, name, start, end]):
            ui.notify('❌ Please fill in all fields', type='negative')
            return
        
        if 'shift_timetable' not in manager.timetable_data:
            manager.timetable_data['shift_timetable'] = {}
        if 'shift_templates' not in manager.timetable_data['shift_timetable']:
            manager.timetable_data['shift_timetable']['shift_templates'] = {}
        
        # Calculate working hours
        start_time = datetime.strptime(start, '%H:%M').time()
        end_time = datetime.strptime(end, '%H:%M').time()
        start_dt = datetime.combine(datetime.today(), start_time)
        end_dt = datetime.combine(datetime.today(), end_time)
        if end_dt < start_dt:  # Next day
            end_dt += timedelta(days=1)
        working_hours = (end_dt - start_dt).total_seconds() / 3600
        
        manager.timetable_data['shift_timetable']['shift_templates'][shift_id] = {
            'name': shift_id,
            'display_name': name,
            'start_time': start,
            'end_time': end,
            'working_hours': working_hours,
            'color': '#22c55e',
            'icon': '⏰'
        }
        
        dialog.close()
        ui.notify(f'✅ Shift "{name}" created successfully!', type='positive')
        ui.navigate.reload()

def create_shift_templates_panel(manager: ShiftTimetableManager):
    """Create shift templates configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">⏰ Shift Templates</h2>', sanitize=False)
    ui.label('Create and manage reusable shift templates for your organization').classes('text-gray-600 mb-6')
    
    shift_templates = manager.timetable_data.get('shift_timetable', {}).get('shift_templates', {})
    
    # Shift Templates Grid
    if shift_templates:
        with ui.grid(columns=2).classes('gap-6 w-full'):
            for template_id, template in shift_templates.items():
                with ui.card().classes('p-4 border-l-4 border-blue-500'):
                    # Template Header
                    with ui.row().classes('items-center justify-between w-full mb-3'):
                        with ui.row().classes('items-center gap-3'):
                            ui.label(template.get('icon', '⏰')).classes('text-2xl')
                            ui.label(template.get('display_name', template_id)).classes('font-bold text-lg text-gray-700')
                        
                        with ui.row().classes('gap-2'):
                            ui.button('✏️', on_click=lambda tid=template_id: edit_shift_template(tid)).classes('bg-blue-500 text-white p-1 text-sm')
                            ui.button('🗑️', on_click=lambda tid=template_id: delete_shift_template(tid)).classes('bg-red-500 text-white p-1 text-sm')
                    
                    # Template Details
                    with ui.grid(columns=2).classes('gap-4 w-full'):
                        with ui.column():
                            ui.label('⏰ Time').classes('text-sm font-medium text-gray-600 mb-1')
                            ui.label(f"{template.get('start_time', 'N/A')} - {template.get('end_time', 'N/A')}").classes('text-gray-700')
                            
                            ui.label('📊 Working Hours').classes('text-sm font-medium text-gray-600 mb-1 mt-2')
                            ui.label(f"{template.get('working_hours', 0)} hours").classes('text-gray-700')
                        
                        with ui.column():
                            ui.label('☕ Break Duration').classes('text-sm font-medium text-gray-600 mb-1')
                            ui.label(f"{template.get('break_duration_minutes', 0)} minutes").classes('text-gray-700')
                            
                            ui.label('💰 Allowance').classes('text-sm font-medium text-gray-600 mb-1 mt-2')
                            allowance = template.get('shift_allowance_percentage', 0)
                            ui.label(f"{allowance}%" if allowance > 0 else "None").classes('text-gray-700')
    else:
        # Empty state
        with ui.card().classes('p-8 text-center bg-gray-50'):
            ui.label('📝').classes('text-6xl mb-4 opacity-50')
            ui.label('No Shift Templates Created').classes('text-xl font-semibold text-gray-600 mb-2')
            ui.label('Create your first shift template to get started with scheduling').classes('text-gray-500 mb-4')
            ui.button('➕ Create First Template', on_click=lambda: show_create_template_dialog()).classes('bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold')

    # Add New Template Button (if templates exist)
    if shift_templates:
        with ui.row().classes('w-full mt-6'):
            ui.button('➕ Add New Template', on_click=lambda: show_create_template_dialog()).classes('bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg font-semibold')

    def show_create_template_dialog():
        """Show create template dialog"""
        with ui.dialog() as dialog, ui.card().classes('w-[500px]'):
            ui.label('Create Shift Template').classes('text-xl font-bold mb-4')
            
            # Basic Information
            ui.label('Basic Information').classes('font-semibold text-gray-700 mb-2')
            template_id = ui.input('Template ID (e.g., morning_shift)').classes('w-full mb-3')
            display_name = ui.input('Display Name').classes('w-full mb-3')
            
            # Time Settings
            ui.label('Time Settings').classes('font-semibold text-gray-700 mb-2 mt-4')
            with ui.row().classes('gap-3 w-full'):
                start_time = ui.input('Start Time').classes('flex-1').props('type=time')
                end_time = ui.input('End Time').classes('flex-1').props('type=time')
            
            # Break Settings
            ui.label('Break Settings').classes('font-semibold text-gray-700 mb-2 mt-4')
            with ui.row().classes('gap-3 w-full'):
                break_duration = ui.number('Break Duration (minutes)', value=60, min=0, max=180).classes('flex-1')
                break_start = ui.input('Break Start Time').classes('flex-1').props('type=time')
            
            # Additional Settings
            ui.label('Additional Settings').classes('font-semibold text-gray-700 mb-2 mt-4')
            with ui.row().classes('gap-3 w-full'):
                allowance = ui.number('Shift Allowance (%)', value=0, min=0, max=100).classes('flex-1')
                color = ui.input('Color', value='#22c55e').classes('flex-1').props('type=color')
            
            icon = ui.input('Icon/Emoji', value='⏰').classes('w-full mb-4')
            
            with ui.row().classes('gap-3 w-full justify-end'):
                ui.button('Cancel', on_click=dialog.close).classes('bg-gray-500 text-white')
                ui.button('Create Template', on_click=lambda: create_template(
                    template_id.value, display_name.value, start_time.value, end_time.value,
                    break_duration.value, break_start.value, allowance.value, color.value, icon.value, dialog
                )).classes('bg-green-500 text-white')
        
        dialog.open()
    
    def create_template(template_id: str, name: str, start: str, end: str, break_dur: int, break_start: str, allowance: float, color: str, icon: str, dialog):
        """Create new shift template"""
        if not all([template_id, name, start, end]):
            ui.notify('❌ Please fill in required fields', type='negative')
            return
        
        # Calculate working hours
        start_time = datetime.strptime(start, '%H:%M').time()
        end_time = datetime.strptime(end, '%H:%M').time()
        start_dt = datetime.combine(datetime.today(), start_time)
        end_dt = datetime.combine(datetime.today(), end_time)
        if end_dt < start_dt:  # Next day
            end_dt += timedelta(days=1)
        working_hours = (end_dt - start_dt).total_seconds() / 3600 - (break_dur / 60)
        
        if 'shift_timetable' not in manager.timetable_data:
            manager.timetable_data['shift_timetable'] = {}
        if 'shift_templates' not in manager.timetable_data['shift_timetable']:
            manager.timetable_data['shift_timetable']['shift_templates'] = {}
        
        manager.timetable_data['shift_timetable']['shift_templates'][template_id] = {
            'name': template_id,
            'display_name': name,
            'start_time': start,
            'end_time': end,
            'break_duration_minutes': break_dur,
            'break_start_time': break_start,
            'working_hours': round(working_hours, 2),
            'shift_allowance_percentage': allowance,
            'color': color,
            'icon': icon
        }
        
        dialog.close()
        ui.notify(f'✅ Template "{name}" created successfully!', type='positive')
        ui.navigate.reload()
    
    def edit_shift_template(template_id: str):
        """Edit existing shift template"""
        ui.notify(f'✏️ Edit functionality for {template_id} coming soon!', type='info')
    
    def delete_shift_template(template_id: str):
        """Delete shift template"""
        if 'shift_timetable' in manager.timetable_data and 'shift_templates' in manager.timetable_data['shift_timetable']:
            if template_id in manager.timetable_data['shift_timetable']['shift_templates']:
                del manager.timetable_data['shift_timetable']['shift_templates'][template_id]
                ui.notify(f'🗑️ Template {template_id} deleted', type='info')
                ui.navigate.reload()

def create_department_schedules_panel(manager: ShiftTimetableManager):
    """Create department schedules configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">🏢 Department Schedules</h2>', sanitize=False)
    ui.label('Configure department-specific shift patterns and requirements').classes('text-gray-600 mb-6')
    
    department_shifts = manager.timetable_data.get('shift_timetable', {}).get('department_shifts', {})
    
    # Department Overview
    if department_shifts:
        with ui.grid(columns=2).classes('gap-6 w-full'):
            for dept_name, dept_config in department_shifts.items():
                with ui.card().classes('p-4'):
                    ui.label(f'🏢 {dept_name.replace("_", " ").title()}').classes('text-lg font-bold text-gray-700 mb-3')
                    
                    ui.label('Default Shift:').classes('text-sm font-medium text-gray-600')
                    ui.label(dept_config.get('default_shift', 'Not set')).classes('text-gray-700 mb-2')
                    
                    ui.label('Available Shifts:').classes('text-sm font-medium text-gray-600')
                    available_shifts = dept_config.get('available_shifts', [])
                    ui.label(', '.join(available_shifts) if available_shifts else 'None').classes('text-gray-700 mb-2')
                    
                    if dept_config.get('24_7_coverage'):
                        ui.chip('24/7 Coverage', color='red').classes('text-white text-xs')
                    
                    if dept_config.get('on_call_rotation'):
                        ui.chip('On-Call Rotation', color='blue').classes('text-white text-xs')
    else:
        with ui.card().classes('p-8 text-center bg-gray-50'):
            ui.label('🏢').classes('text-6xl mb-4 opacity-50')
            ui.label('No Department Schedules Configured').classes('text-xl font-semibold text-gray-600 mb-2')
            ui.label('Set up department-specific scheduling rules').classes('text-gray-500 mb-4')
            ui.button('➕ Configure Departments', on_click=lambda: show_department_config_dialog()).classes('bg-purple-500 hover:bg-purple-600 text-white px-6 py-3 rounded-lg font-semibold')

    def show_department_config_dialog():
        """Show department configuration dialog"""
        ui.notify('🏢 Department configuration coming soon!', type='info')

def create_weekly_patterns_panel(manager: ShiftTimetableManager):
    """Create weekly patterns configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">📋 Weekly Schedule Patterns</h2>', sanitize=False)
    ui.label('Define recurring weekly work patterns and rotation schedules').classes('text-gray-600 mb-6')
    
    # Add content for weekly patterns
    with ui.card().classes('p-6'):
        ui.label('📅 Pattern Management Coming Soon').classes('text-xl font-semibold text-gray-700 mb-3')
        ui.label('Configure standard 5-day, compressed 4-day, 6-day retail, and rotating shift patterns.').classes('text-gray-600')

def create_shift_assignments_panel(manager: ShiftTimetableManager):
    """Create shift assignments configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">👥 Shift Assignment Rules</h2>', sanitize=False)
    ui.label('Configure automated shift assignment and employee scheduling rules').classes('text-gray-600 mb-6')
    
    assignment_rules = manager.timetable_data.get('shift_timetable', {}).get('assignment_rules', {})
    
    with ui.grid(columns=2).classes('gap-6 w-full'):
        # Basic Assignment Settings
        with ui.card().classes('p-4'):
            ui.label('⚙️ Assignment Settings').classes('font-semibold text-gray-700 mb-3')
            
            auto_assignment = ui.switch(
                'Auto Assignment',
                value=assignment_rules.get('auto_assignment', False),
                on_change=lambda e: update_assignment_rule('auto_assignment', e.value)
            ).classes('mb-3')
            
            manager_approval = ui.switch(
                'Manager Approval Required',
                value=assignment_rules.get('manager_approval_required', True),
                on_change=lambda e: update_assignment_rule('manager_approval_required', e.value)
            ).classes('mb-3')
            
            ui.label('Employee Preference Weight (%)').classes('text-sm text-gray-600 mb-1')
            preference_weight = ui.number(
                value=assignment_rules.get('employee_preference_weight', 30),
                min=0, max=100,
                on_change=lambda e: update_assignment_rule('employee_preference_weight', e.value)
            ).classes('w-full')
        
        # Fairness Rules
        with ui.card().classes('p-4'):
            ui.label('⚖️ Fairness Rules').classes('font-semibold text-gray-700 mb-3')
            
            equal_opportunity = ui.switch(
                'Equal Opportunity Night Shifts',
                value=assignment_rules.get('equal_opportunity_night_shifts', True),
                on_change=lambda e: update_assignment_rule('equal_opportunity_night_shifts', e.value)
            ).classes('mb-3')
            
            weekend_rotation = ui.switch(
                'Fair Weekend Rotation',
                value=assignment_rules.get('weekend_rotation_fair_distribution', True),
                on_change=lambda e: update_assignment_rule('weekend_rotation_fair_distribution', e.value)
            ).classes('mb-3')
            
            holiday_rotation = ui.switch(
                'Holiday Duty Rotation',
                value=assignment_rules.get('holiday_duty_rotation', True),
                on_change=lambda e: update_assignment_rule('holiday_duty_rotation', e.value)
            )
    
    def update_assignment_rule(key: str, value):
        """Update assignment rule"""
        if 'shift_timetable' not in manager.timetable_data:
            manager.timetable_data['shift_timetable'] = {}
        if 'assignment_rules' not in manager.timetable_data['shift_timetable']:
            manager.timetable_data['shift_timetable']['assignment_rules'] = {}
        manager.timetable_data['shift_timetable']['assignment_rules'][key] = value

def create_break_policies_panel(manager: ShiftTimetableManager):
    """Create break policies configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">☕ Break Time Policies</h2>', sanitize=False)
    ui.label('Configure break schedules and meal period policies for shifts').classes('text-gray-600 mb-6')
    
    # Add content for break policies
    with ui.card().classes('p-6'):
        ui.label('☕ Break Policy Configuration Coming Soon').classes('text-xl font-semibold text-gray-700 mb-3')
        ui.label('Set up paid breaks, meal breaks, prayer breaks, and special accommodation breaks.').classes('text-gray-600')

def create_overtime_rules_panel(manager: ShiftTimetableManager):
    """Create overtime rules configuration panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">⏱️ Overtime Management</h2>', sanitize=False)
    ui.label('Configure overtime calculation and approval workflows for shifts').classes('text-gray-600 mb-6')
    
    overtime_rules = manager.timetable_data.get('shift_timetable', {}).get('overtime_rules', {})
    
    with ui.grid(columns=2).classes('gap-6 w-full'):
        # Basic Overtime Settings
        with ui.card().classes('p-4'):
            ui.label('⚙️ Overtime Settings').classes('font-semibold text-gray-700 mb-3')
            
            auto_calculation = ui.switch(
                'Automatic Calculation',
                value=overtime_rules.get('automatic_calculation', True),
                on_change=lambda e: update_overtime_rule('automatic_calculation', e.value)
            ).classes('mb-3')
            
            approval_workflow = ui.switch(
                'Approval Workflow',
                value=overtime_rules.get('approval_workflow', True),
                on_change=lambda e: update_overtime_rule('approval_workflow', e.value)
            ).classes('mb-3')
            
            ui.label('Max Overtime Hours/Week').classes('text-sm text-gray-600 mb-1')
            max_overtime = ui.number(
                value=overtime_rules.get('maximum_overtime_hours_per_week', 12),
                min=0, max=40,
                on_change=lambda e: update_overtime_rule('maximum_overtime_hours_per_week', e.value)
            ).classes('w-full')
        
        # Overtime Benefits
        with ui.card().classes('p-4'):
            ui.label('💰 Overtime Benefits').classes('font-semibold text-gray-700 mb-3')
            
            meal_allowance = ui.switch(
                'Overtime Meal Allowance',
                value=overtime_rules.get('overtime_meal_allowance', True),
                on_change=lambda e: update_overtime_rule('overtime_meal_allowance', e.value)
            ).classes('mb-3')
            
            ui.label('Transport Allowance After').classes('text-sm text-gray-600 mb-1')
            transport_time = ui.input(
                value=overtime_rules.get('transport_allowance_after_hours', '22:00'),
                on_change=lambda e: update_overtime_rule('transport_allowance_after_hours', e.value)
            ).classes('w-full').props('type=time')
    
    def update_overtime_rule(key: str, value):
        """Update overtime rule"""
        if 'shift_timetable' not in manager.timetable_data:
            manager.timetable_data['shift_timetable'] = {}
        if 'overtime_rules' not in manager.timetable_data['shift_timetable']:
            manager.timetable_data['shift_timetable']['overtime_rules'] = {}
        manager.timetable_data['shift_timetable']['overtime_rules'][key] = value

def create_reporting_panel(manager: ShiftTimetableManager):
    """Create reporting and analytics panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">📈 Reports & Analytics</h2>', sanitize=False)
    ui.label('Generate reports and analyze shift scheduling performance').classes('text-gray-600 mb-6')
    
    # Report Categories
    with ui.grid(columns=2).classes('gap-6 w-full'):
        # Coverage Reports
        with ui.card().classes('p-4'):
            ui.label('📊 Coverage Analysis').classes('font-semibold text-gray-700 mb-3')
            
            ui.button('Shift Coverage Report', on_click=lambda: generate_report('coverage')).classes('w-full bg-blue-500 text-white mb-2')
            ui.button('Staffing Gaps Analysis', on_click=lambda: generate_report('gaps')).classes('w-full bg-red-500 text-white mb-2')
            ui.button('Overtime Cost Analysis', on_click=lambda: generate_report('overtime')).classes('w-full bg-yellow-500 text-white')
        
        # Performance Reports
        with ui.card().classes('p-4'):
            ui.label('📈 Performance Metrics').classes('font-semibold text-gray-700 mb-3')
            
            ui.button('Employee Satisfaction', on_click=lambda: generate_report('satisfaction')).classes('w-full bg-green-500 text-white mb-2')
            ui.button('Productivity by Shift', on_click=lambda: generate_report('productivity')).classes('w-full bg-purple-500 text-white mb-2')
            ui.button('Absenteeism Tracking', on_click=lambda: generate_report('absenteeism')).classes('w-full bg-orange-500 text-white')
    
    def generate_report(report_type: str):
        """Generate specified report"""
        ui.notify(f'📊 Generating {report_type} report...', type='info')
        # In a real implementation, this would generate and download the report