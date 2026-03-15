from nicegui import ui, app
from helperFuns import imagePath
from helperFuns.employee_registry import employee_registry
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
        
        # Employee leave balances — keyed by canonical ID, pre-seeded from registry
        # New employees start with full allocations; requests reduce them at runtime.
        self.employee_balances = self._build_balances()
        self._init_runtime_data()

    def _build_balances(self):
        """Build default leave balances for every employee in the registry."""
        balances = {}
        for emp in employee_registry.get_all():
            eid = emp['employee_id']
            balances[eid] = {
                lt: {
                    'used': 0,
                    'remaining': cfg['allocation_per_year'],
                    'pending': 0,
                }
                for lt, cfg in self.leave_types.items()
            }
        # Keep any legacy hard-coded entries for backward compat
        if not balances:
            balances['EMP000123'] = {
                lt: {'used': 0, 'remaining': cfg['allocation_per_year'], 'pending': 0}
                for lt, cfg in self.leave_types.items()
            }
        return balances

    def _init_runtime_data(self):
        """Initialise runtime leave requests and config — called from __init__."""
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
    with ui.column().classes('w-full bg-gradient-to-br from-slate-100 to-emerald-50 min-h-screen p-6 gap-6'):

        # ── Header card ──────────────────────────────────────────────────────
        with ui.card().classes(
            'w-full rounded-2xl shadow-md text-white overflow-hidden'
        ).style('background: linear-gradient(135deg, #059669, #0d9488, #0891b2);'):
            with ui.card_section().classes('px-8 py-6'):
                with ui.row().classes('w-full justify-between items-center'):
                    with ui.column().classes('gap-2'):
                        with ui.row().classes('items-center gap-2 text-emerald-200 text-sm mb-1'):
                            ui.html('<span>🏠 Dashboard</span>')
                            ui.html('<span class="opacity-50">/</span>')
                            ui.html('<span>Employees</span>')
                            ui.html('<span class="opacity-50">/</span>')
                            ui.html('<span class="text-white font-medium">Leave Management</span>')
                        with ui.row().classes('items-center gap-4'):
                            ui.html(
                                '<div style="background:rgba(255,255,255,0.18);border-radius:0.875rem;'
                                'width:52px;height:52px;display:flex;align-items:center;'
                                'justify-content:center;font-size:1.75rem;">🌿</div>'
                            )
                            with ui.column().classes('gap-0.5'):
                                ui.html('<h1 class="text-3xl font-extrabold tracking-tight">Smart Leave Management</h1>')
                                ui.html('<p class="text-emerald-100 text-sm">AI-powered leave planning and intelligent work-life balance optimization</p>')
                    with ui.row().classes('gap-3'):
                        ui.button('🤖 AI Leave Planner', on_click=show_ai_leave_planner).props('outline color=white')
                        ui.button('📊 Leave Analytics',  on_click=show_leave_analytics).props('outline color=white')

        # ── KPI dashboard ─────────────────────────────────────────────────────
        create_smart_leave_dashboard()

        # ── Leave balance cards ────────────────────────────────────────────────
        create_leave_balance_overview()

        # ── Tabs ──────────────────────────────────────────────────────────────
        with ui.tabs().classes('w-full') as tabs:
            request_tab         = ui.tab('New Request',           icon='send')
            recommendations_tab = ui.tab('Smart Recommendations', icon='psychology')
            my_requests_tab     = ui.tab('My Requests',           icon='folder_shared')
            calendar_tab        = ui.tab('Leave Calendar',        icon='calendar_month')
            policies_tab        = ui.tab('Leave Policies',        icon='policy')

        with ui.tab_panels(tabs, value=request_tab).classes('w-full'):
            with ui.tab_panel(request_tab):
                create_new_leave_request_section()
            with ui.tab_panel(recommendations_tab):
                create_leave_recommendations_section()
            with ui.tab_panel(my_requests_tab):
                create_my_leave_requests_section()
            with ui.tab_panel(calendar_tab):
                create_leave_calendar_section()
            with ui.tab_panel(policies_tab):
                create_leave_policies_section()

def create_leave_balance_overview():
    """Leave balance cards — evenly distributed, vivid gradient design."""
    employee_id = "EMP-123"
    employee_balance = leave_manager.get_employee_leave_balance(employee_id)

    _gradients = [
        ("#059669", "#065f46"),  # emerald
        ("#dc2626", "#9f1239"),  # rose/red
        ("#10b981", "#047857"),  # green
        ("#7c3aed", "#4c1d95"),  # violet
        ("#f59e0b", "#b45309"),  # amber
        ("#0891b2", "#0e7490"),  # cyan
    ]

    with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden'):
        with ui.element('div').style(
            'background: linear-gradient(90deg, #059669, #0d9488);'
            'padding: .8rem 1.5rem;'
        ):
            ui.html('<h2 class="text-base font-bold text-white">📊 Leave Balances at a Glance</h2>')

        with ui.card_section().classes('p-4'):
            with ui.element('div').style('display:flex; flex-wrap:wrap; gap:.85rem; width:100%;'):
                for i, (leave_type, balance) in enumerate(employee_balance.items()):
                    g_from, g_to     = _gradients[i % len(_gradients)]
                    alloc            = leave_manager.leave_types[leave_type]['allocation_per_year']
                    pct              = int(balance['remaining'] / alloc * 100) if alloc else 0
                    code             = leave_manager.leave_types[leave_type]['code']

                    ui.html(f"""
<div style="
    flex: 1 1 130px; min-width: 130px;
    border-radius:.875rem; overflow:hidden;
    box-shadow: 0 4px 14px -4px rgba(0,0,0,0.14);
    background: #fff;
    transition: transform .18s ease, box-shadow .18s ease;
    cursor: default;
" onmouseover="this.style.transform='translateY(-4px)';this.style.boxShadow='0 12px 24px -6px rgba(0,0,0,0.18)'"
   onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 4px 14px -4px rgba(0,0,0,0.14)'">

  <div style="height:5px;background:linear-gradient(90deg,{g_from},{g_to});"></div>

  <div style="padding:.75rem .9rem .85rem;">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.5rem;">
      <span style="font-size:.68rem;font-weight:700;color:#64748b;
                   text-transform:uppercase;letter-spacing:.08em;">{code}</span>
      <span style="font-size:.68rem;font-weight:700;padding:.1rem .4rem;border-radius:9999px;
                   background:linear-gradient(90deg,{g_from},{g_to});color:#fff;">
        {balance['remaining']}d
      </span>
    </div>

    <div style="font-size:.72rem;font-weight:600;color:#1e293b;margin-bottom:.5rem;line-height:1.3;">
      {leave_type}
    </div>

    <div style="width:100%;height:5px;background:#e2e8f0;border-radius:9999px;overflow:hidden;margin-bottom:.4rem;">
      <div style="height:5px;background:linear-gradient(90deg,{g_from},{g_to});
                  border-radius:9999px;width:{pct}%;"></div>
    </div>

    <div style="display:flex;justify-content:space-between;font-size:.65rem;color:#94a3b8;">
      <span>{balance['used']} used</span>
      <span>{alloc} total</span>
    </div>
    {'<div style="font-size:.62rem;color:#d97706;font-weight:600;margin-top:.25rem;">' + str(balance["pending"]) + ' pending</div>' if balance.get('pending') else ''}
  </div>
</div>
""")

def create_new_leave_request_section():
    """Create new leave request form with smart validation — styled fields and modern date picker."""
    with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden'):
        with ui.element('div').style(
            'background: linear-gradient(90deg, #059669, #0d9488);'
            'padding: 1rem 1.5rem;'
        ):
            ui.html('<h2 class="text-lg font-bold text-white">📝 Submit New Leave Request</h2>')

        with ui.card_section().classes('p-6'):
            with ui.row().classes('w-full gap-6'):

                # ── Left — Leave Details ─────────────────────────────────────────────
                with ui.card().classes('flex-1 rounded-xl border border-emerald-100 bg-emerald-50/40'):
                    with ui.card_section().classes('p-5'):
                        ui.html(
                            '<div class="flex items-center gap-2 mb-4">'
                            '<span style="background:linear-gradient(135deg,#059669,#0d9488);'
                            'color:#fff;padding:.25rem .65rem;border-radius:.5rem;'
                            'font-size:.75rem;font-weight:700;">STEP 1</span>'
                            '<span class="font-semibold text-emerald-800">Leave Details</span></div>'
                        )

                        leave_types        = list(leave_manager.leave_types.keys())
                        leave_type_select  = ui.select(
                            options=leave_types, label='Leave Type ✦'
                        ).props('outlined bg-color=white').classes('w-full')

                        ui.html('<div class="text-xs font-semibold text-gray-500 uppercase '
                                'tracking-wider mt-3 mb-1">📅 Start Date</div>')
                        start_date_input = ui.date(
                            value=date.today() + timedelta(days=7)
                        ).classes('w-full').props('minimal today-btn color=teal')

                        ui.html('<div class="text-xs font-semibold text-gray-500 uppercase '
                                'tracking-wider mt-3 mb-1">📅 End Date</div>')
                        end_date_input = ui.date(
                            value=date.today() + timedelta(days=7)
                        ).classes('w-full').props('minimal today-btn color=teal')

                        days_calculated = ui.html(
                            '<div style="margin-top:.6rem;padding:.4rem .75rem;'
                            'background:linear-gradient(90deg,#ecfdf5,#f0fdfa);'
                            'border-radius:.5rem;border-left:3px solid #059669;'
                            'font-size:.8rem;font-weight:600;color:#065f46;">'
                            '🗓 1 business day</div>'
                        )

                        reason_input = ui.textarea(
                            'Reason for Leave ✦',
                            placeholder='Please provide detailed reason for this leave request...'
                        ).props('outlined rows=3 bg-color=white').classes('w-full')

                # ── Right — Work Coverage & Validation ──────────────────────
                with ui.card().classes('flex-1 rounded-xl border border-teal-100 bg-teal-50/40'):
                    with ui.card_section().classes('p-5'):
                        ui.html(
                            '<div class="flex items-center gap-2 mb-4">'
                            '<span style="background:linear-gradient(135deg,#0d9488,#0891b2);'
                            'color:#fff;padding:.25rem .65rem;border-radius:.5rem;'
                            'font-size:.75rem;font-weight:700;">STEP 2</span>'
                            '<span class="font-semibold text-teal-800">Coverage &amp; Validation</span></div>'
                        )

                        coverage_input = ui.textarea(
                            'Work Coverage Plan',
                            placeholder='Describe how your work will be covered during absence...'
                        ).props('outlined rows=3 bg-color=white').classes('w-full')

                        emergency_contact = ui.input(
                            'Emergency Contact',
                            placeholder='Contact person during leave'
                        ).props('outlined bg-color=white').classes('w-full')

                        # Real-time validation display
                        with ui.element('div').style(
                            'margin-top:.75rem;padding:.75rem;'
                            'background:#f8fafc;border-radius:.625rem;'
                            'border:1px solid #e2e8f0;'
                        ):
                            ui.html('<div class="text-xs font-bold text-gray-500 uppercase '
                                    'tracking-wider mb-2">🔍 Real-time Validation</div>')
                            validation_content = ui.column()

            # ── Smart score preview ───────────────────────────────────────────
            with ui.element('div').style(
                'margin-top:1.25rem;padding:1rem 1.25rem;'
                'background:linear-gradient(90deg,#ecfdf5,#f0fdfa);'
                'border-radius:.875rem;border-left:4px solid #059669;'
                'display:flex;justify-content:space-between;align-items:center;'
            ):
                ui.html('<span class="font-semibold text-emerald-800">🎯 Smart Approval Score</span>')
                score_preview = ui.label('Score will be calculated automatically')
                score_preview.style('color:#0d9488;font-weight:600;font-size:.9rem;')

            def update_validation():
                if start_date_input.value and end_date_input.value and leave_type_select.value:
                    business_days = leave_manager.calculate_business_days(
                        start_date_input.value, end_date_input.value
                    )
                    days_calculated.content = (
                        f'<div style="margin-top:.6rem;padding:.4rem .75rem;'
                        f'background:linear-gradient(90deg,#ecfdf5,#f0fdfa);'
                        f'border-radius:.5rem;border-left:3px solid #059669;'
                        f'font-size:.8rem;font-weight:600;color:#065f46;">'
                        f'🗓 {business_days} business day{"s" if business_days != 1 else ""}</div>'
                    )
                    validation = leave_manager.validate_leave_request(
                        "EMP-123", leave_type_select.value,
                        start_date_input.value, end_date_input.value, reason_input.value
                    )
                    validation_content.clear()
                    if validation["valid"]:
                        with validation_content:
                            ui.html('<span style="color:#059669;font-size:.8rem;font-weight:600;">✅ Request appears valid</span>')
                    else:
                        with validation_content:
                            ui.html('<span style="color:#dc2626;font-size:.8rem;font-weight:600;">❌ Issues found:</span>')
                            for error in validation["errors"]:
                                ui.html(f'<div style="font-size:.75rem;color:#ef4444;margin-left:.75rem;">• {error}</div>')
                    if validation["warnings"]:
                        with validation_content:
                            ui.html('<span style="color:#d97706;font-size:.8rem;font-weight:600;">⚠️ Warnings:</span>')
                            for w in validation["warnings"]:
                                ui.html(f'<div style="font-size:.75rem;color:#f59e0b;margin-left:.75rem;">• {w}</div>')
                    if validation["valid"]:
                        request_data = {
                            "employee_id": "EMP-123",
                            "leave_type": leave_type_select.value,
                            "start_date": start_date_input.value.strftime("%Y-%m-%d"),
                            "end_date":   end_date_input.value.strftime("%Y-%m-%d"),
                            "reason":     reason_input.value,
                            "work_coverage": coverage_input.value,
                        }
                        smart_score  = leave_manager.calculate_smart_score(request_data)
                        sc_color     = ('#059669' if smart_score >= 80
                                        else '#d97706' if smart_score >= 60
                                        else '#dc2626')
                        score_preview.text = f'Smart Score: {smart_score}%'
                        score_preview.style(f'color:{sc_color};font-weight:700;font-size:.9rem;')

            start_date_input.on('update:model-value', lambda: update_validation())
            end_date_input.on('update:model-value',   lambda: update_validation())
            leave_type_select.on('update:model-value', lambda: update_validation())
            reason_input.on('update:model-value',     lambda: update_validation())
            coverage_input.on('update:model-value',   lambda: update_validation())

            # ── Actions ───────────────────────────────────────────────────────
            with ui.row().classes('w-full justify-end gap-3 mt-4'):
                ui.button('Save as Draft', on_click=save_leave_as_draft).props('flat color=teal')
                ui.button('🚀 Submit Request', on_click=lambda: submit_leave_request(
                    leave_type_select.value, start_date_input.value, end_date_input.value,
                    reason_input.value, coverage_input.value, emergency_contact.value
                )).props('color=positive').style(
                    'background:linear-gradient(90deg,#059669,#0d9488);'
                    'color:#fff;border-radius:.75rem;font-weight:700;padding:.5rem 1.5rem;'
                )

def create_leave_recommendations_section():
    """Create AI-powered leave recommendations — styled modern cards."""
    employee_id = "EMP-123"
    recommendations = leave_manager.get_leave_recommendations(employee_id)

    _priority_map = {
        'High':   ("#dc2626", "#9f1239",  "#fee2e2", "#7f1d1d"),
        'Medium': ("#d97706", "#b45309",  "#fef3c7", "#78350f"),
        'Low':    ("#0891b2", "#0e7490",  "#e0f2fe", "#0c4a6e"),
    }

    with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden'):
        with ui.element('div').style(
            'background: linear-gradient(90deg, #059669, #0d9488);'
            'padding: 1rem 1.5rem;'
        ):
            ui.html('<h2 class="text-lg font-bold text-white">🤖 AI-Powered Leave Recommendations</h2>')

        with ui.card_section().classes('p-6'):
            if not recommendations:
                with ui.column().classes('items-center py-8 gap-3'):
                    ui.html('<div style="font-size:3rem;">🌟</div>')
                    ui.html('<p class="text-gray-500 font-medium">No recommendations at this time</p>')
                    ui.html('<p class="text-gray-400 text-sm">All your leave balances are in good standing</p>')
            else:
                with ui.element('div').style('display:flex; flex-wrap:wrap; gap:1rem; width:100%;'):
                    for rec in recommendations:
                        g_from, g_to, bg, txt = _priority_map.get(
                            rec['priority'], ("#64748b", "#475569", "#f1f5f9", "#1e293b")
                        )
                        ui.html(f"""
<div style="
    flex: 1 1 240px; min-width: 240px;
    border-radius: 1rem; overflow: hidden;
    box-shadow: 0 4px 18px -4px rgba(0,0,0,0.12);
    background: #fff;
    transition: transform .18s ease, box-shadow .18s ease;
" onmouseover="this.style.transform='translateY(-4px)';this.style.boxShadow='0 12px 24px -6px rgba(0,0,0,0.16)'"
   onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 4px 18px -4px rgba(0,0,0,0.12)'">

  <div style="height:5px;background:linear-gradient(90deg,{g_from},{g_to});"></div>

  <div style="padding:.9rem 1rem 1rem;">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.5rem;">
      <span style="font-weight:700;font-size:.85rem;color:#1e293b;">{rec['type']}</span>
      <span style="padding:.15rem .55rem;border-radius:9999px;font-size:.65rem;font-weight:700;
                   background:{bg};color:{txt};">{rec['priority']}</span>
    </div>
    <p style="font-size:.75rem;color:#64748b;line-height:1.5;margin-bottom:.7rem;">{rec['message']}</p>
    <button style="
        width:100%;padding:.4rem;
        background:linear-gradient(90deg,{g_from},{g_to});
        color:#fff;font-size:.72rem;font-weight:700;
        border:none;border-radius:.5rem;cursor:pointer;
        transition:opacity .15s;
    " onmouseover="this.style.opacity='.8'" onmouseout="this.style.opacity='1'">
      {rec['action']}
    </button>
  </div>
</div>
""")

def create_my_leave_requests_section():
    """My leave requests — styled gradient-header table with status pills and score colouring."""
    employee_id = "EMP-123"
    my_requests  = leave_manager.get_my_leave_requests(employee_id)

    with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden'):
        with ui.element('div').style(
            'background: linear-gradient(90deg, #059669, #0d9488);'
            'padding: 1rem 1.5rem; display:flex; justify-content:space-between; align-items:center;'
        ):
            ui.html('<h2 class="text-lg font-bold text-white">📂 My Leave Requests</h2>')
            ui.html(f'<span style="background:rgba(255,255,255,0.2);color:#fff;padding:.2rem .75rem;'
                    f'border-radius:9999px;font-size:.72rem;font-weight:700;">{len(my_requests)} records</span>')

        if not my_requests:
            with ui.card_section().classes('py-12'):
                with ui.column().classes('items-center gap-3'):
                    ui.html('<div style="font-size:3rem;">📅</div>')
                    ui.html('<p class="text-gray-500 font-medium">No leave requests found</p>')
                    ui.html('<p class="text-gray-400 text-sm">Submit your first leave request using the New Request tab</p>')
        else:
            with ui.element('div').classes('w-full overflow-x-auto'):
                with ui.element('table').classes('w-full min-w-full border-collapse'):
                    with ui.element('thead'):
                        with ui.element('tr').classes(
                            'bg-gradient-to-r from-emerald-600 to-teal-600 text-white text-sm'
                        ):
                            th = 'px-4 py-3 text-left font-semibold tracking-wide uppercase whitespace-nowrap'
                            for h in ['🆔 ID', '🌿 Leave Type', '📅 Dates', '🗓 Days',
                                      '🔵 Status', '🎯 Score', '⚙ Actions']:
                                with ui.element('th').classes(th):
                                    ui.html(h)

                    with ui.element('tbody'):
                        td = 'px-4 py-3 text-sm text-gray-700 whitespace-nowrap'
                        sorted_requests = sorted(my_requests, key=lambda x: x['request_date'], reverse=True)
                        for idx, req in enumerate(sorted_requests):
                            stripe    = 'bg-slate-50' if idx % 2 == 0 else 'bg-white'
                            score     = req['smart_score']
                            sc_cls    = ('text-emerald-600 font-bold' if score >= 80
                                         else 'text-amber-600 font-bold' if score >= 60
                                         else 'text-rose-600 font-bold')

                            if 'Approved' in req['status']:
                                pill = 'bg-emerald-100 text-emerald-800'
                            elif 'Pending' in req['status']:
                                pill = 'bg-amber-100 text-amber-800'
                            else:
                                pill = 'bg-rose-100 text-rose-800'

                            leave_cfg   = leave_manager.leave_types.get(req['leave_type'], {})
                            _lt_colours = {
                                'Annual Leave': ('#4f46e5', '#3730a3'),
                                'Sick Leave':   ('#dc2626', '#9f1239'),
                                'Personal Leave': ('#10b981', '#065f46'),
                                'Maternity Leave': ('#7c3aed', '#4c1d95'),
                                'Paternity Leave': ('#f59e0b', '#b45309'),
                                'Study Leave':  ('#0891b2', '#0e7490'),
                            }
                            lc_f, lc_t  = _lt_colours.get(req['leave_type'], ('#64748b', '#475569'))

                            with ui.element('tr').classes(
                                f'{stripe} border-b border-gray-100 '
                                'hover:bg-emerald-50 transition-colors duration-150'
                            ):
                                with ui.element('td').classes(td):
                                    ui.html(f'<span class="font-mono text-xs font-semibold text-emerald-700">{req["id"]}</span>')
                                with ui.element('td').classes(td):
                                    ui.html(
                                        f'<span style="padding:.15rem .55rem;border-radius:9999px;'
                                        f'font-size:.7rem;font-weight:700;'
                                        f'background:linear-gradient(90deg,{lc_f},{lc_t});color:#fff;">'
                                        f'{req["leave_type"]}</span>'
                                    )
                                with ui.element('td').classes(td):
                                    ui.html(
                                        f'<div class="font-semibold text-gray-900">'
                                        f'{req["start_date"]} → {req["end_date"]}</div>'
                                        f'<div class="text-xs text-gray-400">'
                                        f'{req["reason"][:46]}…</div>'
                                    )
                                with ui.element('td').classes(td):
                                    ui.html(f'<span class="font-bold text-gray-900">{req["days_requested"]}d</span>')
                                with ui.element('td').classes(td):
                                    ui.html(f'<span class="px-2 py-0.5 rounded-full text-xs font-bold {pill}">{req["status"]}</span>')
                                with ui.element('td').classes(td):
                                    ui.html(f'<span class="{sc_cls}">{score}%</span>')
                                with ui.element('td').classes(td):
                                    with ui.row().classes('gap-1'):
                                        ui.button(icon='visibility').props('flat round dense color=teal size=sm') \
                                            .on_click(lambda r=req: view_leave_request_details(r))
                                        if req['status'] == 'Pending Approval':
                                            ui.button(icon='edit').props('flat round dense color=green size=sm') \
                                                .on_click(lambda r=req: edit_leave_request(r))

def create_leave_calendar_section():
    """Leave calendar — modern monthly grid with gradient top bars."""
    current_year = datetime.now().year
    employee_id  = "EMP-123"
    calendar_data = leave_manager.get_leave_calendar_data(employee_id, current_year)

    _lt_colours = {
        'Annual Leave':   ('#4f46e5', '#3730a3'),
        'Sick Leave':     ('#dc2626', '#9f1239'),
        'Personal Leave': ('#10b981', '#065f46'),
        'Maternity Leave':('#7c3aed', '#4c1d95'),
        'Paternity Leave':('#f59e0b', '#b45309'),
        'Study Leave':    ('#0891b2', '#0e7490'),
    }
    _month_grads = [
        ('#059669','#0d9488'), ('#3b82f6','#6366f1'), ('#f59e0b','#ef4444'),
        ('#10b981','#0891b2'), ('#a855f7','#ec4899'), ('#0284c7','#0891b2'),
        ('#84cc16','#10b981'), ('#f97316','#ef4444'), ('#8b5cf6','#a855f7'),
        ('#0d9488','#059669'), ('#e11d48','#f97316'), ('#0ea5e9','#6366f1'),
    ]

    with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden'):
        with ui.element('div').style(
            'background: linear-gradient(90deg, #059669, #0d9488);'
            'padding: 1rem 1.5rem; display:flex; justify-content:space-between; align-items:center;'
        ):
            ui.html('<h2 class="text-lg font-bold text-white">📅 Leave Calendar</h2>')
            with ui.row().classes('items-center gap-2'):
                ui.select(
                    options=[current_year - 1, current_year, current_year + 1],
                    value=current_year, label='Year'
                ).props('outlined dense bg-color=white').classes('w-24')

        with ui.card_section().classes('p-6'):
            with ui.element('div').style(
                'display:grid;grid-template-columns:repeat(4,1fr);gap:1.25rem;width:100%;'
            ):
                for month in range(1, 13):
                    month_nm     = calendar.month_name[month]
                    g_from, g_to = _month_grads[month - 1]

                    month_leaves = [
                        (ds, d) for ds, d in calendar_data.items()
                        if datetime.strptime(ds, "%Y-%m-%d").month == month
                    ]

                    with ui.element('div').style(
                        'border-radius:1rem;overflow:hidden;'
                        'box-shadow:0 4px 16px -4px rgba(0,0,0,0.13);background:#fff;'
                        'transition:transform .18s ease,box-shadow .18s ease;'
                    ).on('mouseover', None).on('mouseout', None):
                        # Tall gradient top bar
                        with ui.element('div').style(
                            f'height:6px;background:linear-gradient(90deg,{g_from},{g_to});'
                        ):
                            pass
                        with ui.element('div').style('padding:1rem 1.1rem 1rem;min-height:90px;'):
                            # Month name with gradient text
                            ui.html(
                                f'<div style="font-weight:800;font-size:.85rem;'
                                f'background:linear-gradient(90deg,{g_from},{g_to});'
                                f'-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
                                f'margin-bottom:.6rem;letter-spacing:.01em;">{month_nm} {current_year}</div>'
                            )
                            if month_leaves:
                                for ds, leave_data in month_leaves:
                                    day  = datetime.strptime(ds, "%Y-%m-%d").day
                                    lc_f, lc_t = _lt_colours.get(
                                        leave_data['leave_type'], ('#64748b', '#475569')
                                    )
                                    ui.html(
                                        f'<div style="display:inline-flex;align-items:center;'
                                        f'gap:.25rem;margin:.15rem .1rem;'
                                        f'padding:.2rem .55rem;border-radius:9999px;'
                                        f'background:linear-gradient(90deg,{lc_f},{lc_t});'
                                        f'color:#fff;font-size:.68rem;font-weight:700;'
                                        f'box-shadow:0 2px 6px -2px rgba(0,0,0,0.2);">'  
                                        f'<span style="opacity:.85;">{day}</span>'
                                        f'<span>{leave_data["leave_type"][:3]}</span>'
                                        f'</div>'
                                    )
                            else:
                                ui.html(
                                    '<div style="color:#cbd5e1;font-size:.72rem;'
                                    'padding:.3rem 0;font-style:italic;">No leave planned</div>'
                                )

def create_leave_policies_section():
    """Leave policies — styled outer card with expansion items."""
    _type_pal = {
        'Annual Leave':   ('#059669','#065f46'),
        'Sick Leave':     ('#dc2626','#9f1239'),
        'Personal Leave': ('#10b981','#047857'),
        'Maternity Leave':('#7c3aed','#4c1d95'),
        'Paternity Leave':('#f59e0b','#b45309'),
        'Study Leave':    ('#0891b2','#0e7490'),
    }

    with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden'):
        with ui.element('div').style(
            'background: linear-gradient(90deg, #059669, #0d9488);'
            'padding: 1rem 1.5rem;'
        ):
            ui.html('<h2 class="text-lg font-bold text-white">📋 Leave Policies &amp; Guidelines</h2>')

        with ui.card_section().classes('p-6'):
            with ui.element('div').style('display:flex;flex-wrap:wrap;gap:1rem;width:100%;'):
                for leave_type, config in leave_manager.leave_types.items():
                    g_from, g_to = _type_pal.get(leave_type, ('#059669','#0d9488'))
                    carry        = 'Yes' if config['can_carry_forward'] else 'No'
                    cf_max       = f'  ·  Max carry: {config["max_carry_forward"]}d' if config['can_carry_forward'] else ''

                    ui.html(f"""
<div style="
  flex: 1 1 280px; min-width: 260px;
  border-radius: 1rem; overflow: hidden;
  box-shadow: 0 4px 16px -4px rgba(0,0,0,0.12);
  background: #fff;
  transition: transform .18s ease, box-shadow .18s ease;
" onmouseover="this.style.transform='translateY(-4px)';this.style.boxShadow='0 12px 24px -6px rgba(0,0,0,0.17)'"
   onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 4px 16px -4px rgba(0,0,0,0.12)'">

  <!-- Gradient top bar -->
  <div style="height:5px;background:linear-gradient(90deg,{g_from},{g_to});"></div>

  <!-- Header row -->
  <div style="display:flex;align-items:center;gap:.65rem;
              padding:.75rem 1rem .6rem;
              border-bottom:1px solid #f1f5f9;">
    <div style="background:linear-gradient(135deg,{g_from},{g_to});
                width:36px;height:36px;border-radius:.6rem;flex-shrink:0;
                display:flex;align-items:center;justify-content:center;
                font-size:1rem;color:#fff;font-weight:800;">
      {config['code'][0]}
    </div>
    <div>
      <div style="font-weight:800;font-size:.82rem;color:#1e293b;">{leave_type}</div>
      <div style="font-size:.66rem;color:#94a3b8;">Code: {config['code']}</div>
    </div>
    <div style="margin-left:auto;background:linear-gradient(90deg,{g_from},{g_to});
                color:#fff;font-size:.7rem;font-weight:700;
                padding:.2rem .6rem;border-radius:9999px;white-space:nowrap;">
      {config['allocation_per_year']}d / yr
    </div>
  </div>

  <!-- Stats row -->
  <div style="display:flex;justify-content:space-between;
              padding:.6rem 1rem .75rem;gap:.5rem;">
    <div style="text-align:center;flex:1;">
      <div style="font-size:.95rem;font-weight:800;color:#1e293b;">{config['max_consecutive_days']}</div>
      <div style="font-size:.62rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.06em;margin-top:.1rem;">Max consec.</div>
    </div>
    <div style="width:1px;background:#f1f5f9;"></div>
    <div style="text-align:center;flex:1;">
      <div style="font-size:.95rem;font-weight:800;color:#1e293b;">{config['advance_notice_days']}</div>
      <div style="font-size:.62rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.06em;margin-top:.1rem;">Notice days</div>
    </div>
    <div style="width:1px;background:#f1f5f9;"></div>
    <div style="text-align:center;flex:1;">
      <div style="font-size:.95rem;font-weight:800;
                  color:{'#059669' if config['can_carry_forward'] else '#dc2626'}">{carry}</div>
      <div style="font-size:.62rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.06em;margin-top:.1rem;">Carry fwd</div>
    </div>
    {'<div style="width:1px;background:#f1f5f9;"></div><div style="text-align:center;flex:1;"><div style="font-size:.95rem;font-weight:800;color:#1e293b;">' + str(config["max_carry_forward"]) + '</div><div style="font-size:.62rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.06em;margin-top:.1rem;">Max carry</div></div>' if config['can_carry_forward'] else ''}
  </div>
</div>
""")

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
    """KPI dashboard — 5 evenly distributed vivid gradient cards."""
    _kpis = [
        {'icon':'🌿', 'value':'18',  'label':'AVAILABLE DAYS',     'sub':'annual leave pool',
         'from_':'#059669','to_':'#065f46'},
        {'icon':'⏳',   'value':'3',   'label':'PENDING REQUESTS',   'sub':'awaiting manager',
         'from_':'#d97706','to_':'#b45309'},
        {'icon':'✅',   'value':'86%', 'label':'APPROVAL RATE',       'sub':'last 12 months',
         'from_':'#0891b2','to_':'#0e7490'},
        {'icon':'🤖',  'value':'94%', 'label':'AI ACCURACY',         'sub':'smart score model',
         'from_':'#7c3aed','to_':'#4c1d95'},
        {'icon':'🏖',  'value':'12',  'label':'DAYS TAKEN THIS YEAR', 'sub':'vs 18 planned',
         'from_':'#0d9488','to_':'#0f766e'},
    ]
    with ui.element('div').style('display:flex; flex-wrap:nowrap; gap:1rem; width:100%;'):
        for c in _kpis:
            ui.html(f"""
<div style="
  flex: 1 1 0%;
  background: linear-gradient(135deg, {c['from_']}, {c['to_']});
  border-radius: 1.25rem;
  padding: 1.4rem 1.5rem;
  color: #fff;
  position: relative;
  overflow: hidden;
  box-shadow: 0 8px 24px -6px rgba(0,0,0,0.28);
  transition: transform .2s ease, box-shadow .2s ease;
  cursor: default;
"
onmouseover="this.style.transform='translateY(-5px)';this.style.boxShadow='0 16px 32px -8px rgba(0,0,0,0.35)'"
onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 8px 24px -6px rgba(0,0,0,0.28)'">
  <div style="position:absolute;top:-18px;right:-18px;width:90px;height:90px;
              background:rgba(255,255,255,0.12);border-radius:50%;"></div>
  <div style="position:absolute;bottom:-16px;left:-12px;width:64px;height:64px;
              background:rgba(255,255,255,0.08);border-radius:50%;"></div>
  <div style="position:relative;z-index:1;">
    <div style="background:rgba(255,255,255,0.18);border-radius:.75rem;
                width:48px;height:48px;display:flex;align-items:center;
                justify-content:center;font-size:1.35rem;margin-bottom:.75rem;">
      {c['icon']}
    </div>
    <div style="font-size:2rem;font-weight:900;letter-spacing:-.02em;">{c['value']}</div>
    <div style="font-size:.72rem;font-weight:700;text-transform:uppercase;
                letter-spacing:.1em;opacity:.85;margin-top:.25rem;">{c['label']}</div>
    <div style="font-size:.68rem;opacity:.6;margin-top:.15rem;">{c['sub']}</div>
  </div>
</div>
""")

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
        ''')
        
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
                    ''')
            
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