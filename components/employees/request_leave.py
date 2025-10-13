from nicegui import ui, app
from helperFuns import imagePath
from assets import FlipCards, SearchBox
import asyncio
from datetime import datetime, timedelta, date
import json
import uuid
import calendar

# Smart Leave Request Management System with Advanced HR Algorithms
class LeaveRequestManager:
    """
    Intelligent leave management system with smart algorithms for
    leave allocation, conflict detection, and approval workflows
    """
    
    def __init__(self):
        # Leave types configuration
        self.leave_types = {
            "Annual Leave": {
                "code": "AL",
                "allocation_per_year": 25,
                "max_consecutive_days": 20,
                "advance_notice_days": 14,
                "can_carry_forward": True,
                "max_carry_forward": 5,
                "color": "blue"
            },
            "Sick Leave": {
                "code": "SL", 
                "allocation_per_year": 12,
                "max_consecutive_days": 10,
                "advance_notice_days": 0,
                "can_carry_forward": False,
                "max_carry_forward": 0,
                "color": "red"
            },
            "Personal Leave": {
                "code": "PL",
                "allocation_per_year": 5,
                "max_consecutive_days": 3,
                "advance_notice_days": 7,
                "can_carry_forward": False,
                "max_carry_forward": 0,
                "color": "green"
            },
            "Maternity Leave": {
                "code": "ML",
                "allocation_per_year": 90,
                "max_consecutive_days": 90,
                "advance_notice_days": 30,
                "can_carry_forward": False,
                "max_carry_forward": 0,
                "color": "purple"
            },
            "Paternity Leave": {
                "code": "PTL",
                "allocation_per_year": 14,
                "max_consecutive_days": 14,
                "advance_notice_days": 30,
                "can_carry_forward": False,
                "max_carry_forward": 0,
                "color": "orange"
            },
            "Study Leave": {
                "code": "STL",
                "allocation_per_year": 10,
                "max_consecutive_days": 5,
                "advance_notice_days": 21,
                "can_carry_forward": True,
                "max_carry_forward": 3,
                "color": "indigo"
            }
        }
        
        # Employee leave balances (mock data)
        self.employee_balances = {
            "EMP-123": {
                "Annual Leave": {"used": 8, "remaining": 17, "pending": 3},
                "Sick Leave": {"used": 2, "remaining": 10, "pending": 0},
                "Personal Leave": {"used": 1, "remaining": 4, "pending": 0},
                "Maternity Leave": {"used": 0, "remaining": 90, "pending": 0},
                "Paternity Leave": {"used": 0, "remaining": 14, "pending": 0},
                "Study Leave": {"used": 3, "remaining": 7, "pending": 0}
            }
        }
        
        # Existing leave requests
        self.leave_requests = [
            {
                "id": "LR-001",
                "employee_id": "EMP-123",
                "employee_name": "John Smith",
                "leave_type": "Annual Leave",
                "start_date": "2024-11-15",
                "end_date": "2024-11-19",
                "days_requested": 5,
                "status": "Approved",
                "request_date": "2024-10-01",
                "reason": "Family vacation",
                "approval_stage": "Completed",
                "smart_score": 92,
                "work_coverage": "Team members informed",
                "created_by": "EMP-123"
            },
            {
                "id": "LR-002", 
                "employee_id": "EMP-123",
                "employee_name": "John Smith",
                "leave_type": "Sick Leave",
                "start_date": "2024-10-20",
                "end_date": "2024-10-21",
                "days_requested": 2,
                "status": "Pending Approval",
                "request_date": "2024-10-12",
                "reason": "Medical appointment",
                "approval_stage": "Manager Review",
                "smart_score": 88,
                "work_coverage": "Emergency only",
                "created_by": "EMP-123"
            }
        ]
        
        # Company holidays and blackout dates
        self.company_holidays = [
            {"date": "2024-12-25", "name": "Christmas Day"},
            {"date": "2024-12-26", "name": "Boxing Day"},
            {"date": "2025-01-01", "name": "New Year's Day"},
            {"date": "2025-04-18", "name": "Good Friday"},
            {"date": "2025-04-21", "name": "Easter Monday"}
        ]
        
        self.blackout_periods = [
            {"start": "2024-12-20", "end": "2025-01-05", "reason": "Year-end closure"},
            {"start": "2024-06-01", "end": "2024-06-15", "reason": "Quarter-end busy period"}
        ]
        
        # Smart algorithm configurations
        self.approval_workflow = {
            "stages": [
                {"name": "Manager Review", "timeout_days": 3, "auto_approve_threshold": 90},
                {"name": "HR Review", "timeout_days": 2, "auto_approve_threshold": 95},
                {"name": "Final Approval", "timeout_days": 1, "auto_approve_threshold": 98}
            ]
        }

    def get_employee_leave_balance(self, employee_id):
        """Get current leave balances for employee"""
        return self.employee_balances.get(employee_id, {})

    def calculate_business_days(self, start_date, end_date):
        """Calculate business days excluding weekends and holidays"""
        current = start_date
        business_days = 0
        holiday_dates = [datetime.strptime(h["date"], "%Y-%m-%d").date() for h in self.company_holidays]
        
        while current <= end_date:
            # Skip weekends (Saturday=5, Sunday=6)
            if current.weekday() < 5 and current not in holiday_dates:
                business_days += 1
            current += timedelta(days=1)
        
        return business_days

    def check_leave_conflicts(self, employee_id, start_date, end_date, exclude_request_id=None):
        """Smart algorithm to detect leave conflicts and overlaps"""
        conflicts = []
        
        # Check against existing approved/pending leaves
        for request in self.leave_requests:
            if (request["employee_id"] == employee_id and 
                request["status"] in ["Approved", "Pending Approval"] and
                request["id"] != exclude_request_id):
                
                existing_start = datetime.strptime(request["start_date"], "%Y-%m-%d").date()
                existing_end = datetime.strptime(request["end_date"], "%Y-%m-%d").date()
                
                # Check for overlap
                if not (end_date < existing_start or start_date > existing_end):
                    conflicts.append({
                        "type": "Leave Conflict",
                        "message": f"Overlaps with existing {request['leave_type']} request ({request['start_date']} to {request['end_date']})",
                        "severity": "High",
                        "request_id": request["id"]
                    })
        
        # Check against blackout periods
        for blackout in self.blackout_periods:
            blackout_start = datetime.strptime(blackout["start"], "%Y-%m-%d").date()
            blackout_end = datetime.strptime(blackout["end"], "%Y-%m-%d").date()
            
            if not (end_date < blackout_start or start_date > blackout_end):
                conflicts.append({
                    "type": "Blackout Period",
                    "message": f"Overlaps with blackout period: {blackout['reason']} ({blackout['start']} to {blackout['end']})",
                    "severity": "High",
                    "reason": blackout["reason"]
                })
        
        # Check team capacity (simplified - would integrate with team management)
        team_leave_count = len([r for r in self.leave_requests 
                               if r["status"] == "Approved" and
                               datetime.strptime(r["start_date"], "%Y-%m-%d").date() <= end_date and
                               datetime.strptime(r["end_date"], "%Y-%m-%d").date() >= start_date])
        
        if team_leave_count >= 3:  # Max 3 team members on leave simultaneously
            conflicts.append({
                "type": "Team Capacity",
                "message": f"High team absence during requested period ({team_leave_count} others on leave)",
                "severity": "Medium"
            })
        
        return conflicts

    def validate_leave_request(self, employee_id, leave_type, start_date, end_date, reason=""):
        """Comprehensive leave request validation algorithm"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "recommendations": []
        }
        
        leave_config = self.leave_types.get(leave_type)
        if not leave_config:
            validation_result["valid"] = False
            validation_result["errors"].append("Invalid leave type selected")
            return validation_result
        
        # Calculate requested days
        business_days = self.calculate_business_days(start_date, end_date)
        
        # Check leave balance
        employee_balance = self.get_employee_leave_balance(employee_id)
        leave_balance = employee_balance.get(leave_type, {"remaining": 0})
        
        if business_days > leave_balance["remaining"]:
            validation_result["valid"] = False
            validation_result["errors"].append(f"Insufficient {leave_type} balance. Requested: {business_days} days, Available: {leave_balance['remaining']} days")
        
        # Check maximum consecutive days
        if business_days > leave_config["max_consecutive_days"]:
            validation_result["valid"] = False
            validation_result["errors"].append(f"Exceeds maximum consecutive days for {leave_type} ({leave_config['max_consecutive_days']} days)")
        
        # Check advance notice requirement
        days_notice = (start_date - date.today()).days
        if days_notice < leave_config["advance_notice_days"]:
            if leave_type == "Sick Leave":
                validation_result["warnings"].append(f"Sick leave can be taken with short notice")
            else:
                validation_result["errors"].append(f"Requires {leave_config['advance_notice_days']} days advance notice")
        
        # Check conflicts
        conflicts = self.check_leave_conflicts(employee_id, start_date, end_date)
        for conflict in conflicts:
            if conflict["severity"] == "High":
                validation_result["errors"].append(conflict["message"])
            else:
                validation_result["warnings"].append(conflict["message"])
        
        # Generate recommendations
        if business_days > 5:
            validation_result["recommendations"].append("Consider splitting long leave periods for better work coverage")
        
        if start_date.weekday() == 0:  # Monday
            validation_result["recommendations"].append("Starting leave on Monday provides a longer continuous break")
        
        if end_date.weekday() == 4:  # Friday
            validation_result["recommendations"].append("Ending leave on Friday provides a longer continuous break")
        
        return validation_result

    def calculate_smart_score(self, request_data):
        """Advanced algorithm to calculate leave approval score"""
        score = 60  # Base score
        
        leave_type = request_data["leave_type"]
        start_date = datetime.strptime(request_data["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(request_data["end_date"], "%Y-%m-%d").date()
        days_requested = self.calculate_business_days(start_date, end_date)
        
        # Leave balance factor
        employee_balance = self.get_employee_leave_balance(request_data["employee_id"])
        leave_balance = employee_balance.get(leave_type, {"remaining": 0})
        balance_ratio = leave_balance["remaining"] / self.leave_types[leave_type]["allocation_per_year"]
        
        if balance_ratio > 0.5:
            score += 20  # Good balance
        elif balance_ratio > 0.3:
            score += 10  # Moderate balance
        else:
            score -= 10  # Low balance
        
        # Advance notice factor
        days_notice = (start_date - date.today()).days
        required_notice = self.leave_types[leave_type]["advance_notice_days"]
        
        if days_notice >= required_notice * 2:
            score += 15  # Excellent advance notice
        elif days_notice >= required_notice:
            score += 10  # Good advance notice
        elif days_notice >= required_notice * 0.5:
            score += 5   # Moderate notice
        else:
            score -= 15  # Short notice
        
        # Duration reasonableness
        max_consecutive = self.leave_types[leave_type]["max_consecutive_days"]
        duration_ratio = days_requested / max_consecutive
        
        if duration_ratio <= 0.5:
            score += 10  # Reasonable duration
        elif duration_ratio <= 0.8:
            score += 5   # Moderate duration
        else:
            score -= 5   # Long duration
        
        # Team impact (simplified)
        conflicts = self.check_leave_conflicts(request_data["employee_id"], start_date, end_date)
        high_severity_conflicts = [c for c in conflicts if c.get("severity") == "High"]
        medium_severity_conflicts = [c for c in conflicts if c.get("severity") == "Medium"]
        
        score -= len(high_severity_conflicts) * 15
        score -= len(medium_severity_conflicts) * 5
        
        # Reason quality (basic sentiment analysis)
        reason = request_data.get("reason", "").lower()
        positive_keywords = ["medical", "family", "emergency", "planned", "vacation", "rest"]
        reason_score = sum(2 for keyword in positive_keywords if keyword in reason)
        score += min(reason_score, 10)
        
        # Work coverage plan
        if request_data.get("work_coverage"):
            score += 10
        
        return min(max(score, 0), 100)  # Clamp between 0-100

    def get_leave_recommendations(self, employee_id):
        """AI-powered leave recommendations"""
        recommendations = []
        employee_balance = self.get_employee_leave_balance(employee_id)
        
        # Analyze usage patterns
        for leave_type, balance in employee_balance.items():
            leave_config = self.leave_types[leave_type]
            utilization_rate = balance["used"] / leave_config["allocation_per_year"]
            
            if utilization_rate < 0.3 and leave_type == "Annual Leave":
                recommendations.append({
                    "type": "Use Annual Leave",
                    "message": f"You have {balance['remaining']} unused annual leave days. Consider taking time off for rest and recreation.",
                    "priority": "Medium",
                    "action": "Plan upcoming vacation"
                })
            
            if balance["remaining"] < 3 and leave_type == "Sick Leave":
                recommendations.append({
                    "type": "Low Sick Leave",
                    "message": f"Low sick leave balance ({balance['remaining']} days). Plan medical appointments carefully.",
                    "priority": "Low",
                    "action": "Monitor health closely"
                })
        
        # Seasonal recommendations
        current_month = datetime.now().month
        if current_month in [11, 12]:  # November, December
            recommendations.append({
                "type": "Year-end Planning",
                "message": "Year-end approaching. Use remaining annual leave before expiry.",
                "priority": "High",
                "action": "Plan year-end vacation"
            })
        
        return recommendations

    def create_leave_request(self, request_data):
        """Create new leave request with smart validation"""
        # Generate unique ID
        new_id = f"LR-{str(uuid.uuid4())[:6].upper()}"
        
        # Calculate smart score
        smart_score = self.calculate_smart_score(request_data)
        
        # Calculate business days
        start_date = datetime.strptime(request_data["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(request_data["end_date"], "%Y-%m-%d").date()
        business_days = self.calculate_business_days(start_date, end_date)
        
        new_request = {
            "id": new_id,
            "request_date": datetime.now().strftime("%Y-%m-%d"),
            "status": "Pending Approval",
            "approval_stage": "Manager Review",
            "smart_score": smart_score,
            "days_requested": business_days,
            "created_by": request_data.get("employee_id", "CURRENT_USER"),
            **request_data
        }
        
        self.leave_requests.append(new_request)
        
        # Update pending balance
        employee_id = request_data["employee_id"]
        leave_type = request_data["leave_type"]
        if employee_id in self.employee_balances and leave_type in self.employee_balances[employee_id]:
            self.employee_balances[employee_id][leave_type]["pending"] += business_days
        
        return True, new_id, smart_score

    def get_my_leave_requests(self, employee_id):
        """Get leave requests for current employee"""
        return [req for req in self.leave_requests if req["created_by"] == employee_id]

    def get_leave_calendar_data(self, employee_id, year=None):
        """Get calendar data for leave visualization"""
        if year is None:
            year = datetime.now().year
        
        calendar_data = {}
        employee_requests = self.get_my_leave_requests(employee_id)
        
        for request in employee_requests:
            if request["status"] in ["Approved", "Pending Approval"]:
                start_date = datetime.strptime(request["start_date"], "%Y-%m-%d").date()
                end_date = datetime.strptime(request["end_date"], "%Y-%m-%d").date()
                
                if start_date.year == year or end_date.year == year:
                    current = start_date
                    while current <= end_date:
                        if current.year == year:
                            calendar_data[current.strftime("%Y-%m-%d")] = {
                                "leave_type": request["leave_type"],
                                "status": request["status"],
                                "request_id": request["id"]
                            }
                        current += timedelta(days=1)
        
        return calendar_data

# Global leave request manager
leave_manager = LeaveRequestManager()

def RequestLeave():
    """
    Modern Request Leave page with smart HR algorithms
    and intelligent leave management system
    """
    
    # Modern gradient header with AI-powered analytics
    with ui.element('div').classes('w-full bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600 text-white p-8 rounded-lg mb-8 shadow-xl'):
        with ui.row().classes('w-full justify-between items-center'):
            with ui.column():
                ui.html('''
                    <div class="flex items-center gap-4">
                        <div class="bg-white bg-opacity-20 p-3 rounded-full">
                            <i class="material-icons text-4xl">event_available</i>
                        </div>
                        <div>
                            <h1 class="text-4xl font-bold mb-2">Smart Leave Management</h1>
                            <p class="text-emerald-100 text-lg">AI-powered leave planning and intelligent work-life balance optimization</p>
                        </div>
                    </div>
                ''', sanitize=False)
                
                # Breadcrumb navigation
                with ui.row().classes('items-center gap-2 text-sm text-emerald-200 mt-4'):
                    ui.icon('home').classes('text-emerald-300')
                    ui.label('Dashboard')
                    ui.icon('chevron_right').classes('text-xs')
                    ui.label('Employees')
                    ui.icon('chevron_right').classes('text-xs')
                    ui.label('Leave Management').classes('text-white font-medium')
            
            # Smart action buttons
            with ui.column().classes('gap-3'):
                ui.button('🤖 AI Leave Planner', on_click=show_ai_leave_planner).props('color=white text-color=emerald-700').classes('font-semibold')
                ui.button('📊 Leave Analytics', on_click=show_leave_analytics).props('outlined color=white').classes('font-semibold')

    # Smart leave dashboard
    create_smart_leave_dashboard()

    # Main content with tabs
    with ui.tabs().classes('w-full mb-4') as tabs:
        request_tab = ui.tab('New Request', icon='send')
        recommendations_tab = ui.tab('Smart Recommendations', icon='psychology')
        my_requests_tab = ui.tab('My Requests', icon='folder_shared')
        calendar_tab = ui.tab('Leave Calendar', icon='calendar_month')
        policies_tab = ui.tab('Leave Policies', icon='policy')

    with ui.tab_panels(tabs, value=request_tab).classes('w-full'):
        # New Request Panel
        with ui.tab_panel(request_tab):
            create_new_leave_request_section()
        
        # Smart Recommendations Panel
        with ui.tab_panel(recommendations_tab):
            create_leave_recommendations_section()
        
        # My Requests Panel
        with ui.tab_panel(my_requests_tab):
            create_my_leave_requests_section()
        
        # Calendar Panel
        with ui.tab_panel(calendar_tab):
            create_leave_calendar_section()
        
        # Policies Panel
        with ui.tab_panel(policies_tab):
            create_leave_policies_section()

def create_leave_balance_overview():
    """Create leave balance overview cards"""
    employee_id = "EMP-123"  # Mock current user
    employee_balance = leave_manager.get_employee_leave_balance(employee_id)
    
    with ui.row().classes('w-full gap-4 mb-6'):
        for leave_type, balance in employee_balance.items():
            leave_config = leave_manager.leave_types[leave_type]
            color = leave_config["color"]
            
            with ui.card().classes(f'p-4 bg-gradient-to-r from-{color}-500 to-{color}-600 text-white min-w-48'):
                with ui.row().classes('items-center justify-between'):
                    with ui.column():
                        ui.label(leave_type).classes(f'text-{color}-100 text-sm')
                        ui.label(f'{balance["remaining"]} days').classes('text-2xl font-bold')
                        if balance["pending"] > 0:
                            ui.label(f'{balance["pending"]} pending').classes(f'text-{color}-200 text-xs')
                    ui.icon('event_available').classes(f'text-3xl text-{color}-200')

def create_new_leave_request_section():
    """Create new leave request form with smart validation"""
    with ui.card().classes('w-full p-6'):
        ui.label('Submit New Leave Request').classes('text-xl font-semibold mb-4')
        
        with ui.row().classes('w-full gap-6'):
            # Left column - Leave Details
            with ui.column().classes('flex-1'):
                ui.label('Leave Details').classes('font-semibold text-lg text-blue-600 mb-3')
                
                leave_types = list(leave_manager.leave_types.keys())
                leave_type_select = ui.select(options=leave_types, label='Leave Type').props('outlined').classes('w-full mb-3')
                
                ui.label('Start Date').classes('text-sm font-medium text-gray-700 mb-1')
                start_date_input = ui.date(value=date.today() + timedelta(days=7)).props('outlined').classes('w-full mb-3')
                
                ui.label('End Date').classes('text-sm font-medium text-gray-700 mb-1')
                end_date_input = ui.date(value=date.today() + timedelta(days=7)).props('outlined').classes('w-full mb-3')
                
                # Dynamic days calculation
                days_calculated = ui.label('Days: 1 business day').classes('text-blue-600 font-medium mb-3')
                
                reason_input = ui.textarea('Reason for Leave', 
                    placeholder='Please provide detailed reason for this leave request...'
                ).props('outlined rows=3').classes('w-full mb-3')
                
            # Right column - Work Coverage & Validation
            with ui.column().classes('flex-1'):
                ui.label('Work Coverage & Validation').classes('font-semibold text-lg text-blue-600 mb-3')
                
                coverage_input = ui.textarea('Work Coverage Plan', 
                    placeholder='Describe how your work will be covered during absence...'
                ).props('outlined rows=3').classes('w-full mb-3')
                
                emergency_contact = ui.input('Emergency Contact', 
                    placeholder='Contact person during leave'
                ).props('outlined').classes('w-full mb-3')
                
                # Real-time validation display
                validation_display = ui.element('div').classes('p-3 border rounded-lg mb-3')
                with validation_display:
                    ui.label('🔍 Real-time Validation').classes('font-semibold text-gray-700 mb-2')
                    validation_content = ui.column()
        
        # Smart score preview
        with ui.row().classes('w-full p-4 bg-gray-50 rounded-lg mb-4'):
            ui.label('🎯 Smart Approval Score').classes('font-semibold text-gray-700')
            score_preview = ui.label('Score will be calculated automatically').classes('text-blue-600 ml-4 font-bold')
        
        # Update validation and score when dates change
        def update_validation():
            if start_date_input.value and end_date_input.value and leave_type_select.value:
                # Calculate business days
                business_days = leave_manager.calculate_business_days(start_date_input.value, end_date_input.value)
                days_calculated.text = f'Days: {business_days} business day{"s" if business_days != 1 else ""}'
                
                # Validate request
                validation = leave_manager.validate_leave_request(
                    "EMP-123", leave_type_select.value, start_date_input.value, end_date_input.value, reason_input.value
                )
                
                # Update validation display
                validation_content.clear()
                
                if validation["valid"]:
                    with validation_content:
                        ui.icon('check_circle').classes('text-green-500 mr-2')
                        ui.label('Request appears valid').classes('text-green-600 font-medium')
                else:
                    with validation_content:
                        ui.icon('error').classes('text-red-500 mr-2')
                        ui.label('Issues found:').classes('text-red-600 font-medium')
                        for error in validation["errors"]:
                            ui.label(f'• {error}').classes('text-red-500 text-sm ml-6')
                
                if validation["warnings"]:
                    with validation_content:
                        ui.icon('warning').classes('text-yellow-500 mr-2')
                        ui.label('Warnings:').classes('text-yellow-600 font-medium')
                        for warning in validation["warnings"]:
                            ui.label(f'• {warning}').classes('text-yellow-500 text-sm ml-6')
                
                # Calculate and show smart score
                if validation["valid"]:
                    request_data = {
                        "employee_id": "EMP-123",
                        "leave_type": leave_type_select.value,
                        "start_date": start_date_input.value.strftime("%Y-%m-%d"),
                        "end_date": end_date_input.value.strftime("%Y-%m-%d"),
                        "reason": reason_input.value,
                        "work_coverage": coverage_input.value
                    }
                    smart_score = leave_manager.calculate_smart_score(request_data)
                    score_color = 'text-green-600' if smart_score >= 80 else 'text-yellow-600' if smart_score >= 60 else 'text-red-600'
                    score_preview.text = f'Smart Score: {smart_score}%'
                    score_preview.classes(f'{score_color} ml-4 font-bold')
        
        # Bind validation updates
        start_date_input.on('update:model-value', lambda: update_validation())
        end_date_input.on('update:model-value', lambda: update_validation())
        leave_type_select.on('update:model-value', lambda: update_validation())
        reason_input.on('update:model-value', lambda: update_validation())
        coverage_input.on('update:model-value', lambda: update_validation())
        
        # Action buttons
        with ui.row().classes('w-full justify-end gap-2 mt-6'):
            ui.button('Save as Draft', on_click=save_leave_as_draft).props('flat color=gray')
            ui.button('Submit Request', on_click=lambda: submit_leave_request(
                leave_type_select.value, start_date_input.value, end_date_input.value,
                reason_input.value, coverage_input.value, emergency_contact.value
            )).props('color=primary')

def create_leave_recommendations_section():
    """Create AI-powered leave recommendations"""
    with ui.card().classes('w-full p-6'):
        ui.label('🤖 AI-Powered Leave Recommendations').classes('text-xl font-semibold mb-4')
        
        employee_id = "EMP-123"
        recommendations = leave_manager.get_leave_recommendations(employee_id)
        
        if recommendations:
            for rec in recommendations:
                priority_color = 'border-red-500 bg-red-50' if rec['priority'] == 'High' else 'border-yellow-500 bg-yellow-50' if rec['priority'] == 'Medium' else 'border-blue-500 bg-blue-50'
                
                with ui.card().classes(f'p-4 border-l-4 {priority_color} mb-3'):
                    with ui.row().classes('items-center justify-between'):
                        with ui.column().classes('flex-1'):
                            ui.label(rec['type']).classes('font-semibold text-lg')
                            ui.label(rec['message']).classes('text-gray-700 text-sm')
                        
                        with ui.column().classes('items-end'):
                            ui.chip(rec['priority'], color='gray').props('dense')
                            ui.button(rec['action'], on_click=lambda a=rec['action']: handle_recommendation_action(a)).props('size=sm color=primary')
        else:
            with ui.column().classes('items-center py-8'):
                ui.icon('recommend').classes('text-gray-400 text-6xl mb-4')
                ui.label('No recommendations at this time').classes('text-gray-500 text-lg')
                ui.label('All your leave balances are in good standing').classes('text-gray-400 text-sm')

def create_my_leave_requests_section():
    """Create my leave requests overview"""
    with ui.card().classes('w-full p-6'):
        ui.label('My Leave Requests').classes('text-xl font-semibold mb-4')
        
        employee_id = "EMP-123"
        my_requests = leave_manager.get_my_leave_requests(employee_id)
        
        if not my_requests:
            with ui.column().classes('items-center py-8'):
                ui.icon('event_busy').classes('text-gray-400 text-6xl mb-4')
                ui.label('No leave requests found').classes('text-gray-500 text-lg')
                ui.label('Submit your first leave request using the form above').classes('text-gray-400 text-sm')
        else:
            # Requests table
            with ui.row().classes('w-full p-4 bg-gray-50 rounded-t-lg font-semibold'):
                ui.label('Request ID').classes('w-28')
                ui.label('Leave Type').classes('w-32')
                ui.label('Dates').classes('flex-1')
                ui.label('Days').classes('w-20 text-center')
                ui.label('Status').classes('w-32')
                ui.label('Score').classes('w-20 text-center')
                ui.label('Actions').classes('w-32 text-center')
            
            for request in sorted(my_requests, key=lambda x: x['request_date'], reverse=True):
                with ui.row().classes('w-full p-4 border-b border-gray-200 hover:bg-gray-50'):
                    ui.label(request['id']).classes('w-28 font-mono text-sm')
                    
                    leave_config = leave_manager.leave_types[request['leave_type']]
                    ui.chip(request['leave_type'], color=leave_config['color']).props('dense').classes('w-32')
                    
                    with ui.column().classes('flex-1'):
                        ui.label(f"{request['start_date']} to {request['end_date']}").classes('font-medium')
                        ui.label(request['reason'][:50] + '...' if len(request['reason']) > 50 else request['reason']).classes('text-sm text-gray-500')
                    
                    ui.label(f"{request['days_requested']}").classes('w-20 text-center font-bold')
                    
                    status_color = 'green' if 'Approved' in request['status'] else 'yellow' if 'Pending' in request['status'] else 'red'
                    ui.chip(request['status'], color=status_color).props('dense').classes('w-32')
                    
                    score_color = 'text-green-600' if request['smart_score'] >= 80 else 'text-yellow-600' if request['smart_score'] >= 60 else 'text-red-600'
                    ui.label(f"{request['smart_score']}%").classes(f'w-20 text-center font-bold {score_color}')
                    
                    with ui.row().classes('w-32 justify-center gap-1'):
                        ui.button(icon='visibility', on_click=lambda r=request: view_leave_request_details(r)).props('size=sm flat color=blue')
                        if request['status'] == 'Pending Approval':
                            ui.button(icon='edit', on_click=lambda r=request: edit_leave_request(r)).props('size=sm flat color=green')

def create_leave_calendar_section():
    """Create leave calendar visualization"""
    with ui.card().classes('w-full p-6'):
        ui.label('📅 Leave Calendar').classes('text-xl font-semibold mb-4')
        
        # Year selector
        current_year = datetime.now().year
        with ui.row().classes('mb-4'):
            year_select = ui.select(options=[current_year-1, current_year, current_year+1], label='Year', value=current_year).props('outlined')
        
        # Calendar grid (simplified monthly view)
        employee_id = "EMP-123"
        calendar_data = leave_manager.get_leave_calendar_data(employee_id, current_year)
        
        with ui.grid(columns=4).classes('gap-4 w-full'):
            for month in range(1, 13):
                month_name = calendar.month_name[month]
                with ui.card().classes('p-3'):
                    ui.label(f'{month_name} {current_year}').classes('font-semibold text-center mb-2')
                    
                    # Show days with leave
                    month_leaves = [(date_str, data) for date_str, data in calendar_data.items() 
                                   if datetime.strptime(date_str, "%Y-%m-%d").month == month]
                    
                    if month_leaves:
                        for date_str, leave_data in month_leaves:
                            day = datetime.strptime(date_str, "%Y-%m-%d").day
                            leave_config = leave_manager.leave_types[leave_data['leave_type']]
                            ui.chip(f'{day} - {leave_data["leave_type"][:2]}', color=leave_config['color']).props('dense').classes('mb-1')
                    else:
                        ui.label('No leave scheduled').classes('text-gray-400 text-sm text-center')

def create_leave_policies_section():
    """Create leave policies and guidelines"""
    with ui.card().classes('w-full p-6'):
        ui.label('📋 Leave Policies & Guidelines').classes('text-xl font-semibold mb-4')
        
        for leave_type, config in leave_manager.leave_types.items():
            with ui.expansion(leave_type, icon='info').classes('w-full mb-2'):
                with ui.column().classes('p-4'):
                    with ui.grid(columns=2).classes('gap-4'):
                        # Left column
                        with ui.column():
                            ui.label('Allocation & Limits').classes('font-semibold text-blue-600 mb-2')
                            ui.label(f'Annual Allocation: {config["allocation_per_year"]} days').classes('text-sm mb-1')
                            ui.label(f'Max Consecutive: {config["max_consecutive_days"]} days').classes('text-sm mb-1')
                            ui.label(f'Advance Notice: {config["advance_notice_days"]} days').classes('text-sm mb-1')
                        
                        # Right column
                        with ui.column():
                            ui.label('Rules & Conditions').classes('font-semibold text-green-600 mb-2')
                            carry_forward = 'Yes' if config["can_carry_forward"] else 'No'
                            ui.label(f'Carry Forward: {carry_forward}').classes('text-sm mb-1')
                            if config["can_carry_forward"]:
                                ui.label(f'Max Carry Forward: {config["max_carry_forward"]} days').classes('text-sm mb-1')
                            ui.label(f'Code: {config["code"]}').classes('text-sm mb-1')

# Action functions
async def submit_leave_request(leave_type, start_date, end_date, reason, coverage, emergency_contact):
    """Submit leave request with comprehensive validation"""
    if not all([leave_type, start_date, end_date, reason]):
        ui.notify('Please fill in all required fields', color='negative')
        return
    
    # Validate dates
    if start_date > end_date:
        ui.notify('End date must be after start date', color='negative')
        return
    
    # Final validation
    validation = leave_manager.validate_leave_request("EMP-123", leave_type, start_date, end_date, reason)
    
    if not validation["valid"]:
        error_messages = '\n'.join(validation["errors"])
        ui.notify(f'Validation failed:\n{error_messages}', color='negative')
        return
    
    request_data = {
        "employee_id": "EMP-123",
        "employee_name": "Current User",
        "leave_type": leave_type,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "reason": reason,
        "work_coverage": coverage,
        "emergency_contact": emergency_contact
    }
    
    success, request_id, smart_score = leave_manager.create_leave_request(request_data)
    
    if success:
        ui.notify(f'Leave request submitted successfully! Request ID: {request_id}', color='positive')
        
        # Show success dialog
        with ui.dialog() as dialog, ui.card().classes('w-96 p-6'):
            ui.label('🎉 Leave Request Submitted!').classes('text-xl font-semibold mb-4 text-green-600')
            ui.label(f'Request ID: {request_id}').classes('font-mono text-sm mb-2')
            ui.label(f'Smart Score: {smart_score}%').classes('text-blue-600 font-semibold mb-4')
            
            score_interpretation = "Excellent chance of approval" if smart_score >= 80 else "Good chance of approval" if smart_score >= 60 else "May require additional review"
            ui.label(f'Approval Likelihood: {score_interpretation}').classes('text-gray-700 mb-4')
            
            ui.label('Next Steps:').classes('font-semibold mb-2')
            ui.label('• Manager review within 3 business days').classes('text-sm mb-1')
            ui.label('• HR review if required').classes('text-sm mb-1')
            ui.label('• You will be notified of the decision').classes('text-sm mb-4')
            
            ui.button('OK', on_click=dialog.close).props('color=primary')
        
        dialog.open()
    else:
        ui.notify('Error submitting request. Please try again.', color='negative')

async def save_leave_as_draft():
    """Save leave request as draft"""
    ui.notify('Leave request saved as draft', color='info')

async def handle_recommendation_action(action):
    """Handle recommendation action"""
    ui.notify(f'Action: {action} - Feature coming soon!', color='info')

async def show_leave_calendar():
    """Show leave calendar in dialog"""
    ui.notify('Opening leave calendar view', color='info')

async def show_leave_balance():
    """Show detailed leave balance"""
    employee_id = "EMP-123"
    employee_balance = leave_manager.get_employee_leave_balance(employee_id)
    
    with ui.dialog() as dialog, ui.card().classes('w-[500px] p-6'):
        ui.label('📊 Detailed Leave Balance').classes('text-xl font-semibold mb-4')
        
        for leave_type, balance in employee_balance.items():
            leave_config = leave_manager.leave_types[leave_type]
            with ui.card().classes('p-3 mb-3 border-l-4 border-blue-500'):
                ui.label(leave_type).classes('font-semibold mb-2')
                
                with ui.grid(columns=3).classes('gap-2 text-sm'):
                    ui.label(f'Allocated: {leave_config["allocation_per_year"]}').classes('text-center')
                    ui.label(f'Used: {balance["used"]}').classes('text-center text-red-600')
                    ui.label(f'Remaining: {balance["remaining"]}').classes('text-center text-green-600')
                
                if balance["pending"] > 0:
                    ui.label(f'Pending: {balance["pending"]} days').classes('text-yellow-600 text-sm')
        
        ui.button('Close', on_click=dialog.close).props('color=primary').classes('w-full mt-4')
    
    dialog.open()

async def view_leave_request_details(request):
    """View detailed leave request information"""
    with ui.dialog() as dialog, ui.card().classes('w-[600px] p-6'):
        ui.label(f'Leave Request Details - {request["id"]}').classes('text-xl font-semibold mb-4')
        
        with ui.grid(columns=2).classes('gap-4 w-full'):
            # Left column
            with ui.column().classes('gap-3'):
                ui.label('Request Information').classes('font-semibold text-blue-600')
                ui.label(f'Employee: {request["employee_name"]}').classes('text-sm')
                ui.label(f'Leave Type: {request["leave_type"]}').classes('text-sm')
                ui.label(f'Duration: {request["start_date"]} to {request["end_date"]}').classes('text-sm')
                ui.label(f'Days Requested: {request["days_requested"]}').classes('text-sm')
                ui.label(f'Request Date: {request["request_date"]}').classes('text-sm')
            
            # Right column
            with ui.column().classes('gap-3'):
                ui.label('Status & Approval').classes('font-semibold text-green-600')
                ui.label(f'Status: {request["status"]}').classes('text-sm')
                ui.label(f'Current Stage: {request["approval_stage"]}').classes('text-sm')
                ui.label(f'Smart Score: {request["smart_score"]}%').classes('text-sm')
                
                if request.get("work_coverage"):
                    ui.label('Work Coverage Planned: Yes').classes('text-sm text-green-600')
                else:
                    ui.label('Work Coverage Planned: No').classes('text-sm text-red-600')
        
        ui.label('Reason:').classes('font-semibold text-purple-600 mt-4')
        ui.label(request["reason"]).classes('text-sm bg-gray-50 p-3 rounded')
        
        if request.get("work_coverage"):
            ui.label('Work Coverage Plan:').classes('font-semibold text-orange-600 mt-4')
            ui.label(request["work_coverage"]).classes('text-sm bg-gray-50 p-3 rounded')
        
        with ui.row().classes('w-full justify-end mt-6'):
            ui.button('Close', on_click=dialog.close).props('flat')
    
    dialog.open()

async def edit_leave_request(request):
    """Edit existing leave request"""
    ui.notify(f'Edit request {request["id"]} - Feature coming soon!', color='info')

# Integration APIs
def get_leave_requests_for_approval(manager_id):
    """API for managers to get leave requests requiring approval"""
    return [req for req in leave_manager.leave_requests if req["approval_stage"] == "Manager Review"]

def create_smart_leave_dashboard():
    """Create modern leave dashboard with AI insights"""
    with ui.column().classes('w-full space-y-6'):
        # Quick stats cards
        with ui.row().classes('w-full gap-4 mb-6'):
            with ui.card().classes('p-6 flex-1 bg-gradient-to-br from-emerald-50 to-green-100'):
                ui.html('''
                    <div class="text-center">
                        <i class="material-icons text-4xl text-emerald-600 mb-2">event_available</i>
                        <div class="text-2xl font-bold text-emerald-800">18</div>
                        <div class="text-emerald-700">Available Days</div>
                    </div>
                ''', sanitize=False)
            
            with ui.card().classes('p-6 flex-1 bg-gradient-to-br from-blue-50 to-blue-100'):
                ui.html('''
                    <div class="text-center">
                        <i class="material-icons text-4xl text-blue-600 mb-2">pending_actions</i>
                        <div class="text-2xl font-bold text-blue-800">3</div>
                        <div class="text-blue-700">Pending Requests</div>
                    </div>
                ''', sanitize=False)
            
            with ui.card().classes('p-6 flex-1 bg-gradient-to-br from-purple-50 to-purple-100'):
                ui.html('''
                    <div class="text-center">
                        <i class="material-icons text-4xl text-purple-600 mb-2">psychology</i>
                        <div class="text-2xl font-bold text-purple-800">94%</div>
                        <div class="text-purple-700">AI Accuracy</div>
                    </div>
                ''', sanitize=False)

async def show_ai_leave_planner():
    """Show AI-powered leave planner dialog"""
    with ui.dialog() as dialog, ui.card().classes('w-4xl max-w-4xl p-8'):
        ui.html('''
            <div class="flex items-center gap-3 mb-6">
                <div class="bg-emerald-500 text-white p-3 rounded-full">
                    <i class="material-icons text-2xl">psychology</i>
                </div>
                <div>
                    <h2 class="text-2xl font-bold text-emerald-800">AI Leave Planner</h2>
                    <p class="text-emerald-600">Intelligent leave optimization based on work patterns and team requirements</p>
                </div>
            </div>
        ''', sanitize=False)
        
        with ui.row().classes('w-full gap-6'):
            # Left column - AI recommendations
            with ui.column().classes('flex-1'):
                ui.label('🤖 AI Recommendations').classes('text-xl font-semibold text-gray-800 mb-4')
                with ui.card().classes('p-4'):
                    ui.html('''
                        <div class="space-y-3">
                            <div class="p-3 bg-emerald-50 rounded-lg border-l-4 border-emerald-500">
                                <div class="font-semibold text-emerald-800">Optimal Leave Period</div>
                                <div class="text-emerald-700">November 15-22, 2025 (Confidence: 94%)</div>
                            </div>
                            <div class="p-3 bg-blue-50 rounded-lg border-l-4 border-blue-500">
                                <div class="font-semibold text-blue-800">Team Impact</div>
                                <div class="text-blue-700">Low impact - 2 other team members available</div>
                            </div>
                            <div class="p-3 bg-purple-50 rounded-lg border-l-4 border-purple-500">
                                <div class="font-semibold text-purple-800">Weather Prediction</div>
                                <div class="text-purple-700">Perfect weather for vacation activities</div>
                            </div>
                        </div>
                    ''', sanitize=False)
            
            # Right column - Smart calendar
            with ui.column().classes('flex-1'):
                ui.label('📅 Smart Calendar View').classes('text-xl font-semibold text-gray-800 mb-4')
                with ui.card().classes('p-4'):
                    ui.label('Interactive calendar with AI-powered suggestions coming soon...').classes('text-gray-600')
        
        ui.button('Close', on_click=dialog.close).props('flat color=emerald').classes('mt-6')
    dialog.open()

async def show_leave_analytics():
    """Show leave analytics dashboard"""
    ui.notify('Advanced leave analytics dashboard - Feature coming soon!', color='info')

def approve_leave_request(request_id, approver_id, comments=""):
    """API for approving leave requests"""
    for request in leave_manager.leave_requests:
        if request["id"] == request_id:
            request["status"] = "Approved"
            request["approval_stage"] = "Completed"
            return True
    return False

def get_team_leave_calendar(team_id, start_date, end_date):
    """API for team leave calendar integration"""
    # This would integrate with team management system
    return leave_manager.get_leave_calendar_data("EMP-123")  # Mock for now