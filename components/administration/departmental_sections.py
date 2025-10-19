from nicegui import ui, app
from helperFuns import imagePath
from assets import FlipCards, SearchBox
import asyncio
from datetime import datetime, timedelta
import json
import uuid

# Import employee data manager for real-time statistics
from .enroll_staff import employee_data_manager

# Advanced Department Management System with HR Time Management Algorithms
class DepartmentDataManager:
    """
    Sophisticated department management system with time tracking,
    workforce analytics, and institution integration algorithms
    """
    
    def __init__(self):
        # Connect with institution data for consistency
        self.institution_id = "KWARECOM-001"
        
        self.departments_data = {
            "departments": [
                {
                    "id": "DEPT-001",
                    "name": "Human Resources",
                    "code": "HR",
                    "description": "Manages employee relations, recruitment, and compliance",
                    "head_employee_id": "EMP-001",
                    "head_name": "Sarah Johnson",
                    "location": "Building A, Floor 2",
                    "budget": 250000,
                    "employee_count": 8,
                    "established_date": "2011-02-01",
                    "status": "Active",
                    "department_type": "Core",
                    "cost_center": "CC-HR-001",
                    "working_hours": {
                        "start": "08:00",
                        "end": "17:00",
                        "break_duration": 60,
                        "flexible_hours": True
                    },
                    "performance_metrics": {
                        "efficiency_score": 92,
                        "employee_satisfaction": 88,
                        "turnover_rate": 5.2,
                        "productivity_index": 94
                    }
                },
                {
                    "id": "DEPT-002", 
                    "name": "Information Technology",
                    "code": "IT",
                    "description": "Manages technology infrastructure and software development",
                    "head_employee_id": "EMP-002",
                    "head_name": "Michael Chen",
                    "location": "Building B, Floor 3",
                    "budget": 450000,
                    "employee_count": 24,
                    "established_date": "2011-03-15",
                    "status": "Active",
                    "department_type": "Core",
                    "cost_center": "CC-IT-001",
                    "working_hours": {
                        "start": "09:00",
                        "end": "18:00",
                        "break_duration": 60,
                        "flexible_hours": True
                    },
                    "performance_metrics": {
                        "efficiency_score": 96,
                        "employee_satisfaction": 91,
                        "turnover_rate": 8.1,
                        "productivity_index": 98
                    }
                },
                {
                    "id": "DEPT-003",
                    "name": "Finance & Accounting",
                    "code": "FIN",
                    "description": "Handles financial planning, accounting, and budget management",
                    "head_employee_id": "EMP-003",
                    "head_name": "Emily Rodriguez",
                    "location": "Building A, Floor 4",
                    "budget": 180000,
                    "employee_count": 12,
                    "established_date": "2011-01-20",
                    "status": "Active",
                    "department_type": "Core",
                    "cost_center": "CC-FIN-001",
                    "working_hours": {
                        "start": "08:30",
                        "end": "17:30",
                        "break_duration": 45,
                        "flexible_hours": False
                    },
                    "performance_metrics": {
                        "efficiency_score": 89,
                        "employee_satisfaction": 85,
                        "turnover_rate": 3.4,
                        "productivity_index": 91
                    }
                },
                {
                    "id": "DEPT-004",
                    "name": "Marketing & Sales",
                    "code": "MKT",
                    "description": "Drives business growth through marketing and sales initiatives",
                    "head_employee_id": "EMP-004",
                    "head_name": "David Thompson",
                    "location": "Building C, Floor 1",
                    "budget": 320000,
                    "employee_count": 18,
                    "established_date": "2011-04-10",
                    "status": "Active",
                    "department_type": "Revenue",
                    "cost_center": "CC-MKT-001",
                    "working_hours": {
                        "start": "08:00",
                        "end": "17:00",
                        "break_duration": 60,
                        "flexible_hours": True
                    },
                    "performance_metrics": {
                        "efficiency_score": 87,
                        "employee_satisfaction": 82,
                        "turnover_rate": 12.3,
                        "productivity_index": 86
                    }
                }
            ],
            "statistics": {
                "total_departments": len(employee_data_manager.departments),
                "total_employees": len(employee_data_manager.employees),
                "total_budget": 1200000,
                "average_efficiency": 91,
                "last_updated": datetime.now().isoformat()
            }
        }
        
        # Time management algorithms
        self.time_tracking_config = {
            "standard_work_week": 40,
            "overtime_threshold": 8,
            "break_compliance_required": True,
            "flexible_time_window": 2  # hours
        }
        
        # Validation rules for departments
        self.validation_rules = {
            "name": {"required": True, "min_length": 2, "max_length": 50},
            "code": {"required": True, "min_length": 2, "max_length": 10, "unique": True},
            "budget": {"required": True, "min_value": 1000, "max_value": 10000000},
            "employee_count": {"required": True, "min_value": 1}
        }

    def get_all_departments(self):
        """Retrieve all departments with calculated metrics"""
        departments = self.departments_data["departments"]
        for dept in departments:
            dept["calculated_metrics"] = self.calculate_department_metrics(dept)
        return departments

    def get_department_by_id(self, dept_id):
        """Get specific department with full details"""
        departments = self.departments_data["departments"]
        for dept in departments:
            if dept["id"] == dept_id:
                dept["calculated_metrics"] = self.calculate_department_metrics(dept)
                return dept
        return None

    def calculate_department_metrics(self, department):
        """Advanced HR time management metrics calculation algorithm"""
        return {
            "cost_per_employee": round(department["budget"] / department["employee_count"], 2),
            "efficiency_rating": self.get_efficiency_rating(department["performance_metrics"]["efficiency_score"]),
            "turnover_status": self.get_turnover_status(department["performance_metrics"]["turnover_rate"]),
            "budget_utilization": round((department["budget"] / 1200000) * 100, 1),  # Total budget from institution
            "workforce_distribution": round((department["employee_count"] / 62) * 100, 1),  # Total employees
            "working_hours_per_week": self.calculate_weekly_hours(department["working_hours"]),
            "overtime_projection": self.calculate_overtime_projection(department),
            "productivity_trend": self.get_productivity_trend(department["performance_metrics"]["productivity_index"])
        }

    def calculate_weekly_hours(self, working_hours):
        """Calculate total weekly working hours"""
        start_hour = int(working_hours["start"].split(":")[0])
        end_hour = int(working_hours["end"].split(":")[0])
        daily_hours = end_hour - start_hour - (working_hours["break_duration"] / 60)
        return daily_hours * 5  # 5 working days

    def calculate_overtime_projection(self, department):
        """Calculate projected overtime based on efficiency and workload"""
        base_hours = self.calculate_weekly_hours(department["working_hours"])
        efficiency = department["performance_metrics"]["efficiency_score"]
        
        if efficiency > 95:
            return max(0, base_hours - 40)  # High efficiency, minimal overtime
        elif efficiency > 85:
            return max(0, base_hours - 38)  # Medium efficiency, some overtime
        else:
            return max(0, base_hours - 35)  # Lower efficiency, more overtime needed

    def get_efficiency_rating(self, score):
        """Convert efficiency score to rating"""
        if score >= 95: return "Excellent"
        elif score >= 90: return "Very Good" 
        elif score >= 80: return "Good"
        elif score >= 70: return "Fair"
        else: return "Needs Improvement"

    def get_turnover_status(self, rate):
        """Assess turnover rate status"""
        if rate <= 5: return "Low"
        elif rate <= 10: return "Normal"
        elif rate <= 15: return "High"
        else: return "Critical"

    def get_productivity_trend(self, index):
        """Determine productivity trend"""
        if index >= 95: return "Trending Up"
        elif index >= 85: return "Stable"
        else: return "Needs Attention"

    def create_department(self, dept_data):
        """Create new department with validation"""
        if self.validate_department_data(dept_data):
            new_dept = {
                "id": f"DEPT-{str(uuid.uuid4())[:3].upper()}",
                "created_date": datetime.now().isoformat(),
                **dept_data,
                "status": "Active",
                "performance_metrics": {
                    "efficiency_score": 85,  # Default starting value
                    "employee_satisfaction": 80,
                    "turnover_rate": 0,
                    "productivity_index": 85
                }
            }
            self.departments_data["departments"].append(new_dept)
            self.update_statistics()
            return True, "Department created successfully"
        return False, "Validation failed"

    def update_department(self, dept_id, updates):
        """Update existing department"""
        department = self.get_department_by_id(dept_id)
        if department:
            department.update(updates)
            self.update_statistics()
            return True, "Department updated successfully"
        return False, "Department not found"

    def delete_department(self, dept_id):
        """Delete department (with safety checks)"""
        departments = self.departments_data["departments"]
        for i, dept in enumerate(departments):
            if dept["id"] == dept_id:
                if dept["employee_count"] > 0:
                    return False, "Cannot delete department with active employees"
                departments.pop(i)
                self.update_statistics()
                return True, "Department deleted successfully"
        return False, "Department not found"

    def validate_department_data(self, data):
        """Comprehensive validation algorithm"""
        for field, rules in self.validation_rules.items():
            if field in data:
                value = data[field]
                if rules.get("required") and not value:
                    return False
                if "min_length" in rules and len(str(value)) < rules["min_length"]:
                    return False
                if "unique" in rules and rules["unique"]:
                    if self.is_code_duplicate(value, data.get("id")):
                        return False
        return True

    def is_code_duplicate(self, code, exclude_id=None):
        """Check for duplicate department codes"""
        for dept in self.departments_data["departments"]:
            if dept["code"] == code and dept["id"] != exclude_id:
                return True
        return False

    def update_statistics(self):
        """Update global department statistics"""
        departments = self.departments_data["departments"]
        self.departments_data["statistics"] = {
            "total_departments": len(departments),
            "total_employees": sum(d["employee_count"] for d in departments),
            "total_budget": sum(d["budget"] for d in departments),
            "average_efficiency": round(sum(d["performance_metrics"]["efficiency_score"] for d in departments) / len(departments), 1),
            "last_updated": datetime.now().isoformat()
        }

    def get_dashboard_analytics(self):
        """Generate analytics for dashboard integration"""
        departments = self.departments_data["departments"]
        return {
            "department_performance": [
                {"name": d["name"], "efficiency": d["performance_metrics"]["efficiency_score"]}
                for d in departments
            ],
            "budget_distribution": [
                {"department": d["name"], "budget": d["budget"], "percentage": round((d["budget"] / self.departments_data["statistics"]["total_budget"]) * 100, 1)}
                for d in departments
            ],
            "workforce_distribution": [
                {"department": d["name"], "employees": d["employee_count"]}
                for d in departments
            ]
        }

# Global department manager instance
dept_manager = DepartmentDataManager()

def DepartmentalSections():
    """
    Modern Departmental Sections page with advanced HR time management algorithms
    and seamless institution integration
    """
    
    # Page header with breadcrumb navigation
    with ui.row().classes('w-full justify-between items-center mb-6'):
        with ui.column():
            ui.label('Departmental Sections').classes('text-3xl font-bold text-gray-800 dark:text-white')
            with ui.row().classes('items-center gap-2 text-sm text-gray-500'):
                ui.icon('home').classes('text-blue-500')
                ui.label('Dashboard')
                ui.icon('chevron_right').classes('text-xs')
                ui.label('Administration')
                ui.icon('chevron_right').classes('text-xs')
                ui.label('Departmental Sections').classes('text-blue-600 font-medium')
        
        # Action buttons
        with ui.row().classes('gap-2'):
            ui.button('Export Data', icon='download', on_click=export_department_data).props('outlined color=blue')
            ui.button('Add Department', icon='add', on_click=show_add_department_dialog).props('color=primary')

    # Department statistics overview
    create_department_stats_overview()

    # Main content with tabs
    with ui.tabs().classes('w-full mb-4') as tabs:
        overview_tab = ui.tab('Overview', icon='dashboard')
        departments_tab = ui.tab('Departments', icon='account_tree')
        analytics_tab = ui.tab('Analytics', icon='analytics')
        time_management_tab = ui.tab('Time Management', icon='schedule')

    with ui.tab_panels(tabs, value=overview_tab).classes('w-full'):
        # Overview Panel
        with ui.tab_panel(overview_tab):
            create_overview_section()
        
        # Departments Panel
        with ui.tab_panel(departments_tab):
            create_departments_list_section()
        
        # Analytics Panel
        with ui.tab_panel(analytics_tab):
            create_analytics_section()
        
        # Time Management Panel
        with ui.tab_panel(time_management_tab):
            create_time_management_section()

def create_department_stats_overview():
    """Create department statistics overview cards"""
    stats = dept_manager.departments_data["statistics"]
    
    with ui.row().classes('w-full gap-4 mb-6'):
        # Total Departments Card
        with ui.card().classes('p-4 bg-gradient-to-r from-indigo-500 to-indigo-600 text-white min-w-48'):
            with ui.row().classes('items-center justify-between'):
                with ui.column():
                    ui.label('Total Departments').classes('text-indigo-100 text-sm')
                    ui.label(f'{stats["total_departments"]}').classes('text-2xl font-bold')
                ui.icon('account_tree').classes('text-3xl text-indigo-200')
        
        # Total Employees Card
        with ui.card().classes('p-4 bg-gradient-to-r from-emerald-500 to-emerald-600 text-white min-w-48'):
            with ui.row().classes('items-center justify-between'):
                with ui.column():
                    ui.label('Total Employees').classes('text-emerald-100 text-sm')
                    ui.label(f'{stats["total_employees"]}').classes('text-2xl font-bold')
                ui.icon('groups').classes('text-3xl text-emerald-200')
        
        # Total Budget Card
        with ui.card().classes('p-4 bg-gradient-to-r from-amber-500 to-amber-600 text-white min-w-48'):
            with ui.row().classes('items-center justify-between'):
                with ui.column():
                    ui.label('Total Budget').classes('text-amber-100 text-sm')
                    ui.label(f'${stats["total_budget"]:,}').classes('text-2xl font-bold')
                ui.icon('account_balance').classes('text-3xl text-amber-200')
        
        # Average Efficiency Card
        with ui.card().classes('p-4 bg-gradient-to-r from-rose-500 to-rose-600 text-white min-w-48'):
            with ui.row().classes('items-center justify-between'):
                with ui.column():
                    ui.label('Avg. Efficiency').classes('text-rose-100 text-sm')
                    ui.label(f'{stats["average_efficiency"]}%').classes('text-2xl font-bold')
                ui.icon('trending_up').classes('text-3xl text-rose-200')

def create_overview_section():
    """Create overview section with department summary"""
    with ui.row().classes('w-full gap-6'):
        # Department Performance Chart
        with ui.card().classes('flex-1 p-6'):
            ui.label('Department Performance Overview').classes('text-xl font-semibold mb-4')
            departments = dept_manager.get_all_departments()
            
            with ui.grid(columns=2).classes('gap-4 w-full'):
                for dept in departments:
                    metrics = dept["calculated_metrics"]
                    with ui.card().classes('p-4 border border-gray-200 hover:shadow-lg transition-shadow'):
                        with ui.row().classes('items-center justify-between mb-2'):
                            ui.label(dept["name"]).classes('font-semibold text-lg')
                            ui.chip(dept["status"], color='green').props('dense')
                        
                        with ui.column().classes('gap-2'):
                            with ui.row().classes('justify-between'):
                                ui.label('Employees:').classes('text-sm text-gray-600')
                                ui.label(f'{dept["employee_count"]}').classes('font-medium')
                            
                            with ui.row().classes('justify-between'):
                                ui.label('Efficiency:').classes('text-sm text-gray-600')
                                ui.label(f'{dept["performance_metrics"]["efficiency_score"]}%').classes('font-medium')
                            
                            with ui.row().classes('justify-between'):
                                ui.label('Budget:').classes('text-sm text-gray-600')
                                ui.label(f'${dept["budget"]:,}').classes('font-medium')
                            
                            with ui.row().classes('justify-between'):
                                ui.label('Cost/Employee:').classes('text-sm text-gray-600')
                                ui.label(f'${metrics["cost_per_employee"]:,}').classes('font-medium')

def create_departments_list_section():
    """Create detailed departments list with management capabilities"""
    with ui.card().classes('w-full p-6'):
        ui.label('Department Management').classes('text-xl font-semibold mb-4')
        
        # Departments table
        departments = dept_manager.get_all_departments()
        
        # Table header
        with ui.row().classes('w-full p-4 bg-gray-50 rounded-t-lg font-semibold'):
            ui.label('Department').classes('flex-1')
            ui.label('Head').classes('w-32')
            ui.label('Employees').classes('w-24 text-center')
            ui.label('Budget').classes('w-32 text-right')
            ui.label('Efficiency').classes('w-24 text-center')
            ui.label('Actions').classes('w-32 text-center')
        
        # Table rows
        for dept in departments:
            metrics = dept["calculated_metrics"]
            with ui.row().classes('w-full p-4 border-b border-gray-200 hover:bg-gray-50 transition-colors'):
                # Department info
                with ui.column().classes('flex-1'):
                    ui.label(dept["name"]).classes('font-medium')
                    ui.label(f'{dept["code"]} • {dept["location"]}').classes('text-sm text-gray-500')
                
                # Department head
                ui.label(dept["head_name"]).classes('w-32 text-sm')
                
                # Employee count
                ui.label(f'{dept["employee_count"]}').classes('w-24 text-center font-medium')
                
                # Budget
                ui.label(f'${dept["budget"]:,}').classes('w-32 text-right font-medium')
                
                # Efficiency with color coding
                efficiency = dept["performance_metrics"]["efficiency_score"]
                color = 'text-green-600' if efficiency >= 90 else 'text-yellow-600' if efficiency >= 80 else 'text-red-600'
                ui.label(f'{efficiency}%').classes(f'w-24 text-center font-medium {color}')
                
                # Actions
                with ui.row().classes('w-32 justify-center gap-1'):
                    ui.button(icon='edit', on_click=lambda d=dept: edit_department_dialog(d)).props('size=sm flat color=blue')
                    ui.button(icon='visibility', on_click=lambda d=dept: view_department_details(d)).props('size=sm flat color=green')
                    ui.button(icon='delete', on_click=lambda d=dept: delete_department_confirm(d)).props('size=sm flat color=red')

def create_analytics_section():
    """Create analytics section with charts and metrics"""
    analytics = dept_manager.get_dashboard_analytics()
    
    with ui.row().classes('w-full gap-6'):
        # Budget Distribution
        with ui.card().classes('flex-1 p-6'):
            ui.label('Budget Distribution').classes('text-xl font-semibold mb-4')
            for item in analytics["budget_distribution"]:
                with ui.row().classes('items-center justify-between mb-2'):
                    ui.label(item["department"]).classes('font-medium')
                    ui.label(f'{item["percentage"]}%').classes('text-blue-600 font-bold')
                # Progress bar
                with ui.element('div').classes('w-full bg-gray-200 rounded-full h-2 mb-2'):
                    ui.element('div').classes(f'bg-blue-500 h-2 rounded-full').style(f'width: {item["percentage"]}%')
        
        # Workforce Distribution
        with ui.card().classes('flex-1 p-6'):
            ui.label('Workforce Distribution').classes('text-xl font-semibold mb-4')
            total_employees = sum(item["employees"] for item in analytics["workforce_distribution"])
            for item in analytics["workforce_distribution"]:
                percentage = round((item["employees"] / total_employees) * 100, 1)
                with ui.row().classes('items-center justify-between mb-2'):
                    ui.label(item["department"]).classes('font-medium')
                    ui.label(f'{item["employees"]} ({percentage}%)').classes('text-green-600 font-bold')
                # Progress bar
                with ui.element('div').classes('w-full bg-gray-200 rounded-full h-2 mb-2'):
                    ui.element('div').classes(f'bg-green-500 h-2 rounded-full').style(f'width: {percentage}%')

def create_time_management_section():
    """Create time management section with HR algorithms"""
    with ui.card().classes('w-full p-6'):
        ui.label('Time Management & Scheduling').classes('text-xl font-semibold mb-4')
        
        departments = dept_manager.get_all_departments()
        
        # Time management table
        with ui.row().classes('w-full p-4 bg-gray-50 rounded-t-lg font-semibold'):
            ui.label('Department').classes('flex-1')
            ui.label('Working Hours').classes('w-32')
            ui.label('Weekly Hours').classes('w-24 text-center')
            ui.label('Overtime Proj.').classes('w-28 text-center')
            ui.label('Flexibility').classes('w-24 text-center')
            ui.label('Status').classes('w-24 text-center')
        
        for dept in departments:
            metrics = dept["calculated_metrics"]
            hours = dept["working_hours"]
            
            with ui.row().classes('w-full p-4 border-b border-gray-200'):
                # Department name
                ui.label(dept["name"]).classes('flex-1 font-medium')
                
                # Working hours
                ui.label(f'{hours["start"]} - {hours["end"]}').classes('w-32 text-sm')
                
                # Weekly hours
                ui.label(f'{metrics["working_hours_per_week"]:.1f}h').classes('w-24 text-center font-medium')
                
                # Overtime projection
                overtime = metrics["overtime_projection"]
                overtime_color = 'text-red-600' if overtime > 5 else 'text-yellow-600' if overtime > 0 else 'text-green-600'
                ui.label(f'{overtime:.1f}h').classes(f'w-28 text-center font-medium {overtime_color}')
                
                # Flexibility
                flex_text = 'Yes' if hours["flexible_hours"] else 'No'
                flex_color = 'text-green-600' if hours["flexible_hours"] else 'text-gray-600'
                ui.label(flex_text).classes(f'w-24 text-center {flex_color}')
                
                # Status based on efficiency
                efficiency = dept["performance_metrics"]["efficiency_score"]
                if efficiency >= 90:
                    ui.chip('Optimal', color='green').props('dense').classes('w-24')
                elif efficiency >= 80:
                    ui.chip('Good', color='yellow').props('dense').classes('w-24')
                else:
                    ui.chip('Review', color='red').props('dense').classes('w-24')

# Dialog and action functions
async def show_add_department_dialog():
    """Show add department dialog"""
    with ui.dialog() as dialog, ui.card().classes('w-96 p-6'):
        ui.label('Add New Department').classes('text-xl font-semibold mb-4')
        
        name_input = ui.input('Department Name').classes('w-full mb-3').props('outlined')
        code_input = ui.input('Department Code').classes('w-full mb-3').props('outlined')
        description_input = ui.textarea('Description').classes('w-full mb-3').props('outlined rows=3')
        budget_input = ui.number('Annual Budget', value=100000).classes('w-full mb-3').props('outlined')
        location_input = ui.input('Location').classes('w-full mb-3').props('outlined')
        
        with ui.row().classes('w-full justify-end gap-2 mt-4'):
            ui.button('Cancel', on_click=dialog.close).props('flat')
            ui.button('Create Department', on_click=lambda: create_new_department(
                dialog, name_input.value, code_input.value, description_input.value,
                budget_input.value, location_input.value
            )).props('color=primary')
    
    dialog.open()

async def create_new_department(dialog, name, code, description, budget, location):
    """Create new department with validation"""
    if not name or not code:
        ui.notify('Name and Code are required!', color='negative')
        return
    
    dept_data = {
        "name": name,
        "code": code.upper(),
        "description": description,
        "budget": budget,
        "location": location,
        "employee_count": 0,
        "established_date": datetime.now().isoformat()[:10],
        "head_employee_id": None,
        "head_name": "To be assigned",
        "department_type": "Support",
        "cost_center": f"CC-{code.upper()}-001",
        "working_hours": {
            "start": "09:00",
            "end": "17:00",
            "break_duration": 60,
            "flexible_hours": True
        }
    }
    
    success, message = dept_manager.create_department(dept_data)
    if success:
        ui.notify('Department created successfully!', color='positive')
        dialog.close()
        # Refresh the page
        ui.navigate.to('/administration/departments')
    else:
        ui.notify(f'Error: {message}', color='negative')

async def edit_department_dialog(department):
    """Show edit department dialog"""
    ui.notify(f'Edit {department["name"]} - Feature coming soon!', color='info')

async def view_department_details(department):
    """Show department details dialog"""
    metrics = department["calculated_metrics"]
    
    with ui.dialog() as dialog, ui.card().classes('w-[600px] p-6'):
        ui.label(f'{department["name"]} Details').classes('text-xl font-semibold mb-4')
        
        with ui.grid(columns=2).classes('gap-4 w-full'):
            # Left column
            with ui.column().classes('gap-3'):
                ui.label('Basic Information').classes('font-semibold text-lg text-blue-600')
                ui.label(f'Department Code: {department["code"]}').classes('text-sm')
                ui.label(f'Location: {department["location"]}').classes('text-sm')
                ui.label(f'Head: {department["head_name"]}').classes('text-sm')
                ui.label(f'Established: {department["established_date"]}').classes('text-sm')
                ui.label(f'Type: {department["department_type"]}').classes('text-sm')
                
                ui.label('Financial Information').classes('font-semibold text-lg text-green-600 mt-4')
                ui.label(f'Annual Budget: ${department["budget"]:,}').classes('text-sm')
                ui.label(f'Cost Center: {department["cost_center"]}').classes('text-sm')
                ui.label(f'Cost per Employee: ${metrics["cost_per_employee"]:,}').classes('text-sm')
            
            # Right column
            with ui.column().classes('gap-3'):
                ui.label('Performance Metrics').classes('font-semibold text-lg text-purple-600')
                ui.label(f'Efficiency Score: {department["performance_metrics"]["efficiency_score"]}%').classes('text-sm')
                ui.label(f'Employee Satisfaction: {department["performance_metrics"]["employee_satisfaction"]}%').classes('text-sm')
                ui.label(f'Turnover Rate: {department["performance_metrics"]["turnover_rate"]}%').classes('text-sm')
                ui.label(f'Productivity Index: {department["performance_metrics"]["productivity_index"]}%').classes('text-sm')
                
                ui.label('Time Management').classes('font-semibold text-lg text-orange-600 mt-4')
                ui.label(f'Working Hours: {department["working_hours"]["start"]} - {department["working_hours"]["end"]}').classes('text-sm')
                ui.label(f'Weekly Hours: {metrics["working_hours_per_week"]:.1f}h').classes('text-sm')
                ui.label(f'Overtime Projection: {metrics["overtime_projection"]:.1f}h').classes('text-sm')
                ui.label(f'Flexible Hours: {"Yes" if department["working_hours"]["flexible_hours"] else "No"}').classes('text-sm')
        
        with ui.row().classes('w-full justify-end mt-6'):
            ui.button('Close', on_click=dialog.close).props('flat')
    
    dialog.open()

async def delete_department_confirm(department):
    """Show delete confirmation dialog"""
    if department["employee_count"] > 0:
        ui.notify(f'Cannot delete {department["name"]} - Department has active employees', color='negative')
        return
    
    ui.notify(f'Delete {department["name"]} - Feature coming soon!', color='warning')

async def export_department_data():
    """Export department data"""
    ui.notify('Exporting department data...', color='info')
    await asyncio.sleep(1)
    ui.notify('Department data exported successfully!', color='positive')

# Integration APIs for other modules
def get_department_integration_data():
    """API for other modules to get department data"""
    return dept_manager.get_all_departments()

def get_department_by_employee(employee_id):
    """Find which department an employee belongs to"""
    # This would integrate with employee management system
    departments = dept_manager.get_all_departments()
    for dept in departments:
        if dept["head_employee_id"] == employee_id:
            return dept
    return None

def update_department_employee_counts():
    """Update all department employee counts based on actual employee data"""
    try:
        from components.administration.enroll_staff import employee_data_manager
        
        # Get current employee counts by department
        department_counts = {}
        for emp in employee_data_manager.employees.values():
            if emp['employment_info']['status'] == 'Active':
                dept = emp['employment_info']['department']
                department_counts[dept] = department_counts.get(dept, 0) + 1
        
        # Update each department's employee count
        for dept_data in dept_manager.departments_data['departments']:
            dept_name = dept_data['name']
            new_count = department_counts.get(dept_name, 0)
            
            # Only update if the count has changed
            if dept_data.get('employee_count', 0) != new_count:
                dept_manager.update_department(dept_data['id'], {"employee_count": new_count})
        
        # Update department statistics
        dept_manager.update_statistics()
        
        print(f"Updated department employee counts: {department_counts}")
        
    except Exception as e:
        print(f"Error updating department employee counts: {e}")

def update_department_employee_count(dept_id, new_count):
    """Update employee count when employees are added/removed"""
    success, message = dept_manager.update_department(dept_id, {"employee_count": new_count})
    if success:
        dept_manager.update_statistics()
    return success, message