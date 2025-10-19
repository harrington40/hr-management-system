from nicegui import ui, app
from helperFuns import imagePath
from assets import FlipCards, SearchBox
import asyncio
from datetime import datetime, timedelta, date
import json
import uuid
import hashlib

# Secure Employee Termination Management System with Advanced HR Algorithms
class TerminationManager:
    """
    Secure termination management system with smart algorithms for
    termination processing, compliance checking, and audit trail management
    """
    
    def __init__(self):
        # Termination types and their security levels
        self.termination_types = {
            "Voluntary Resignation": {
                "code": "VR",
                "notice_period_days": 30,
                "requires_approval": False,
                "security_level": "Low",
                "documentation_required": ["Resignation Letter", "Handover Document"],
                "exit_interview_required": True,
                "clearance_checklist": ["IT Equipment", "Access Cards", "Office Keys"]
            },
            "End of Contract": {
                "code": "EOC",
                "notice_period_days": 14,
                "requires_approval": False,
                "security_level": "Medium",
                "documentation_required": ["Contract Completion Form", "Performance Review"],
                "exit_interview_required": False,
                "clearance_checklist": ["IT Equipment", "Access Cards", "Project Handover"]
            },
            "Dismissal for Cause": {
                "code": "DFC",
                "notice_period_days": 0,
                "requires_approval": True,
                "security_level": "High",
                "documentation_required": ["Disciplinary Record", "Investigation Report", "Legal Review"],
                "exit_interview_required": False,
                "clearance_checklist": ["Immediate Access Revocation", "Security Escort", "Asset Recovery"]
            },
            "Redundancy": {
                "code": "RED",
                "notice_period_days": 60,
                "requires_approval": True,
                "security_level": "Medium",
                "documentation_required": ["Redundancy Notice", "Consultation Record", "Support Package"],
                "exit_interview_required": True,
                "clearance_checklist": ["IT Equipment", "Access Cards", "Final Pay Calculation"]
            },
            "Retirement": {
                "code": "RET",
                "notice_period_days": 90,
                "requires_approval": False,
                "security_level": "Low",
                "documentation_required": ["Retirement Notice", "Pension Documentation", "Benefits Transfer"],
                "exit_interview_required": True,
                "clearance_checklist": ["Knowledge Transfer", "IT Equipment", "Access Cards"]
            },
            "Mutual Agreement": {
                "code": "MA",
                "notice_period_days": 21,
                "requires_approval": True,
                "security_level": "Medium",
                "documentation_required": ["Settlement Agreement", "Legal Confirmation", "Mutual Release"],
                "exit_interview_required": False,
                "clearance_checklist": ["IT Equipment", "Confidentiality Agreement", "Final Settlement"]
            }
        }
        
        # Mock employee data with security classifications
        self.employees = [
            {
                "id": "EMP-001",
                "name": "John Smith",
                "department": "Information Technology",
                "position": "Senior Developer",
                "security_clearance": "High",
                "start_date": "2020-03-15",
                "direct_reports": 2,
                "access_level": "Administrative",
                "critical_projects": ["Banking System", "Security Framework"]
            },
            {
                "id": "EMP-002",
                "name": "Sarah Johnson",
                "department": "Human Resources",
                "position": "HR Manager",
                "security_clearance": "High",
                "start_date": "2019-01-10",
                "direct_reports": 5,
                "access_level": "Administrative",
                "critical_projects": ["Employee Management System"]
            },
            {
                "id": "EMP-003",
                "name": "Mike Davis",
                "department": "Finance",
                "position": "Accountant",
                "security_clearance": "Medium",
                "start_date": "2021-06-20",
                "direct_reports": 0,
                "access_level": "Standard",
                "critical_projects": []
            }
        ]
        
        # Existing termination records
        self.termination_records = [
            {
                "id": "TERM-001",
                "employee_id": "EMP-456",
                "employee_name": "Alice Brown",
                "termination_type": "Voluntary Resignation",
                "initiation_date": "2024-09-15",
                "effective_date": "2024-10-15",
                "reason": "Career advancement opportunity",
                "status": "In Progress",
                "initiated_by": "Employee",
                "security_score": 95,
                "approval_stage": "Manager Review",
                "documentation_complete": 80,
                "clearance_progress": 60,
                "created_by": "EMP-456",
                "created_date": "2024-09-15"
            },
            {
                "id": "TERM-002",
                "employee_id": "EMP-789",
                "employee_name": "Robert Wilson",
                "termination_type": "End of Contract",
                "initiation_date": "2024-09-20",
                "effective_date": "2024-10-05",
                "reason": "Contract completion",
                "status": "Completed",
                "initiated_by": "HR",
                "security_score": 98,
                "approval_stage": "Completed",
                "documentation_complete": 100,
                "clearance_progress": 100,
                "created_by": "HR-001",
                "created_date": "2024-09-20"
            }
        ]
        
        # Security audit configuration
        self.security_settings = {
            "require_dual_authorization": True,
            "audit_trail_retention_days": 2555,  # 7 years
            "immediate_access_revocation_types": ["Dismissal for Cause"],
            "sensitive_data_handling": True,
            "mandatory_security_review": ["High", "Administrative"],
            "encryption_required": True
        }
        
        # Approval workflow based on security level
        self.approval_workflows = {
            "Low": [
                {"stage": "Manager Approval", "timeout_days": 3},
                {"stage": "HR Review", "timeout_days": 2}
            ],
            "Medium": [
                {"stage": "Manager Approval", "timeout_days": 2},
                {"stage": "HR Review", "timeout_days": 2},
                {"stage": "Department Head Approval", "timeout_days": 1}
            ],
            "High": [
                {"stage": "Manager Approval", "timeout_days": 1},
                {"stage": "HR Review", "timeout_days": 1},
                {"stage": "Department Head Approval", "timeout_days": 1},
                {"stage": "Security Review", "timeout_days": 1},
                {"stage": "Executive Approval", "timeout_days": 1}
            ]
        }

    def calculate_security_score(self, termination_data):
        """Advanced security scoring algorithm"""
        score = 70  # Base score
        
        termination_type = termination_data.get("termination_type")
        employee_id = termination_data.get("employee_id")
        
        # Get employee security profile
        employee = next((emp for emp in self.employees if emp["id"] == employee_id), None)
        if not employee:
            return 50  # Low score for unknown employee
        
        termination_config = self.termination_types.get(termination_type, {})
        
        # Security clearance factor
        clearance_scores = {"Low": 0, "Medium": -5, "High": -15}
        score += clearance_scores.get(employee.get("security_clearance", "Low"), 0)
        
        # Access level factor
        access_scores = {"Standard": 0, "Administrative": -10, "Executive": -20}
        score += access_scores.get(employee.get("access_level", "Standard"), 0)
        
        # Critical projects factor
        if employee.get("critical_projects"):
            score -= len(employee["critical_projects"]) * 5
        
        # Direct reports factor (management responsibility)
        if employee.get("direct_reports", 0) > 0:
            score -= employee["direct_reports"] * 2
        
        # Termination type factor
        type_scores = {
            "Voluntary Resignation": 20,
            "End of Contract": 15,
            "Retirement": 25,
            "Mutual Agreement": 10,
            "Redundancy": 5,
            "Dismissal for Cause": -20
        }
        score += type_scores.get(termination_type, 0)
        
        # Notice period compliance
        required_notice = termination_config.get("notice_period_days", 0)
        provided_notice = self.calculate_notice_period(termination_data)
        if provided_notice >= required_notice:
            score += 10
        else:
            score -= 15
        
        # Documentation completeness
        required_docs = len(termination_config.get("documentation_required", []))
        provided_docs = len(termination_data.get("documentation_provided", []))
        if provided_docs >= required_docs:
            score += 15
        else:
            score -= (required_docs - provided_docs) * 5
        
        return min(max(score, 0), 100)  # Clamp between 0-100

    def calculate_notice_period(self, termination_data):
        """Calculate notice period provided"""
        initiation_date = datetime.strptime(termination_data.get("initiation_date", ""), "%Y-%m-%d").date()
        effective_date = datetime.strptime(termination_data.get("effective_date", ""), "%Y-%m-%d").date()
        return (effective_date - initiation_date).days

    def validate_termination_request(self, termination_data):
        """Comprehensive security validation"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "security_alerts": []
        }
        
        employee_id = termination_data.get("employee_id")
        termination_type = termination_data.get("termination_type")
        
        # Employee existence check
        employee = next((emp for emp in self.employees if emp["id"] == employee_id), None)
        if not employee:
            validation_result["valid"] = False
            validation_result["errors"].append("Employee not found in system")
            return validation_result
        
        # Security clearance validation
        if employee.get("security_clearance") == "High":
            validation_result["security_alerts"].append("High security clearance employee - Enhanced security protocols required")
        
        # Critical project validation
        if employee.get("critical_projects"):
            validation_result["warnings"].append(f"Employee involved in {len(employee['critical_projects'])} critical projects - Handover required")
        
        # Management responsibility validation
        if employee.get("direct_reports", 0) > 0:
            validation_result["warnings"].append(f"Employee manages {employee['direct_reports']} direct reports - Succession planning required")
        
        # Termination type validation
        termination_config = self.termination_types.get(termination_type)
        if not termination_config:
            validation_result["valid"] = False
            validation_result["errors"].append("Invalid termination type")
            return validation_result
        
        # Notice period validation
        notice_provided = self.calculate_notice_period(termination_data)
        notice_required = termination_config.get("notice_period_days", 0)
        
        if notice_provided < notice_required:
            if termination_type == "Dismissal for Cause":
                validation_result["security_alerts"].append("Immediate termination - Security protocols activated")
            else:
                validation_result["errors"].append(f"Insufficient notice period: {notice_provided} days provided, {notice_required} days required")
        
        # Dual authorization check for high-risk terminations
        if (termination_config.get("security_level") == "High" and 
            self.security_settings["require_dual_authorization"]):
            validation_result["security_alerts"].append("Dual authorization required for high-security termination")
        
        return validation_result

    def create_termination_record(self, termination_data):
        """Create termination record with security audit trail"""
        # Generate secure ID
        new_id = f"TERM-{str(uuid.uuid4())[:6].upper()}"
        
        # Calculate security score
        security_score = self.calculate_security_score(termination_data)
        
        # Determine approval workflow
        employee = next((emp for emp in self.employees if emp["id"] == termination_data.get("employee_id")), None)
        termination_config = self.termination_types.get(termination_data.get("termination_type"), {})
        
        security_level = termination_config.get("security_level", "Low")
        if employee and employee.get("security_clearance") == "High":
            security_level = "High"
        
        workflow = self.approval_workflows.get(security_level, self.approval_workflows["Low"])
        first_stage = workflow[0]["stage"] if workflow else "HR Review"
        
        # Create audit trail hash
        audit_data = f"{new_id}{termination_data.get('employee_id')}{datetime.now().isoformat()}"
        audit_hash = hashlib.sha256(audit_data.encode()).hexdigest()
        
        new_record = {
            "id": new_id,
            "status": "Pending Approval",
            "security_score": security_score,
            "approval_stage": first_stage,
            "security_level": security_level,
            "documentation_complete": 0,
            "clearance_progress": 0,
            "audit_hash": audit_hash,
            "created_by": "CURRENT_USER",  # Would be actual user ID
            "created_date": datetime.now().strftime("%Y-%m-%d"),
            "last_updated": datetime.now().isoformat(),
            **termination_data
        }
        
        self.termination_records.append(new_record)
        
        # Log security event
        self.log_security_event("TERMINATION_INITIATED", new_id, termination_data.get("employee_id"))
        
        return True, new_id, security_score

    def log_security_event(self, event_type, record_id, employee_id):
        """Log security events for audit trail"""
        # In a real system, this would write to a secure audit log
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "record_id": record_id,
            "employee_id": employee_id,
            "user_id": "CURRENT_USER",
            "ip_address": "127.0.0.1",  # Would be actual IP
            "session_id": "SESSION_123"  # Would be actual session
        }
        print(f"SECURITY AUDIT LOG: {event}")

    def get_termination_records(self, security_filter=None):
        """Get termination records with security filtering"""
        records = self.termination_records.copy()
        
        # Apply security filtering based on user permissions
        if security_filter:
            records = [r for r in records if r.get("security_level") in security_filter]
        
        return records

    def update_termination_status(self, record_id, new_status, user_id):
        """Update termination status with audit trail"""
        for record in self.termination_records:
            if record["id"] == record_id:
                old_status = record["status"]
                record["status"] = new_status
                record["last_updated"] = datetime.now().isoformat()

                # If termination is completed, update employee status and statistics
                if new_status == "Completed" and old_status != "Completed":
                    self._complete_employee_termination(record)

                # Log status change
                self.log_security_event("STATUS_CHANGED", record_id, record.get("employee_id"))

                return True
        return False

    def _complete_employee_termination(self, termination_record):
        """Complete employee termination by updating status and statistics"""
        try:
            employee_id = termination_record.get("employee_id")

            # Import here to avoid circular imports
            from components.administration.enroll_staff import employee_data_manager, update_global_statistics_sync

            # Update employee status to Terminated if they exist in the system
            if employee_id in employee_data_manager.employees:
                employee_data_manager.employees[employee_id]['employment_info']['status'] = 'Terminated'
                employee_data_manager.employees[employee_id]['employment_info']['termination_date'] = termination_record.get("effective_date")
                employee_data_manager.employees[employee_id]['employment_info']['termination_reason'] = termination_record.get("reason")

                # Update global statistics after termination
                update_global_statistics_sync()

                print(f"Employee {employee_id} termination completed. Statistics updated.")

        except Exception as e:
            print(f"Error completing employee termination: {e}")

# Global termination manager instance
termination_manager = TerminationManager()

def EmployeeTermination():
    """
    Modern Secure Employee Termination Management page
    """
    
    # Modern security header with gradient
    with ui.element('div').classes('w-full bg-gradient-to-r from-red-600 via-red-700 to-red-900 text-white p-8 rounded-xl shadow-2xl mb-8'):
        with ui.row().classes('w-full justify-between items-center'):
            with ui.column():
                ui.html('''
                    <div class="flex items-center gap-4">
                        <div class="bg-white bg-opacity-20 p-3 rounded-full">
                            <i class="material-icons text-4xl">security</i>
                        </div>
                        <div>
                            <h1 class="text-4xl font-bold mb-2">Employee Termination Management</h1>
                            <p class="text-red-100 text-lg">Secure termination processing with dual authorization and audit trails</p>
                        </div>
                    </div>
                ''', sanitize=False)
                
                # Security breadcrumb
                with ui.row().classes('items-center gap-2 text-sm text-red-200 mt-4'):
                    ui.icon('home').classes('text-red-300')
                    ui.label('Dashboard')
                    ui.icon('chevron_right').classes('text-xs')
                    ui.label('Administration')
                    ui.icon('chevron_right').classes('text-xs')
                    ui.label('Termination').classes('text-white font-medium')
                
                # Security indicator
                with ui.row().classes('items-center gap-2 mt-3 p-3 bg-red-800 bg-opacity-50 rounded-lg'):
                    ui.icon('shield').classes('text-yellow-300')
                    ui.label('HIGH SECURITY AREA - All actions are monitored and audited').classes('text-red-100 text-sm font-medium')
            
            # Secure action buttons
            with ui.column().classes('gap-3'):
                ui.button('🛡️ Security Audit', on_click=show_security_audit).props('color=white text-color=red-700').classes('font-semibold')
                ui.button('⚠️ New Termination', on_click=show_new_termination_dialog).props('outlined color=white').classes('font-semibold')

    # Security dashboard
    create_security_dashboard()

    # Main content with secure tabs
    with ui.element('div').classes('w-full'):
        with ui.tabs().classes('w-full mb-6 bg-white rounded-lg shadow-lg') as tabs:
            tabs.props('indicator-color=red-600 active-color=red-600')
            overview_tab = ui.tab('🔍 Security Overview', icon='dashboard')
            active_tab = ui.tab('⏳ Active Terminations', icon='pending_actions')
            new_tab = ui.tab('🚨 Initiate Termination', icon='person_remove')
            completed_tab = ui.tab('✅ Completed', icon='done_all')
            analytics_tab = ui.tab('📊 Security Analytics', icon='analytics')
            policies_tab = ui.tab('📋 Policies', icon='policy')

        with ui.tab_panels(tabs, value=overview_tab).classes('w-full'):
            # Security Overview Panel - New
            with ui.tab_panel(overview_tab):
                create_termination_overview_section()
            
            # Active Terminations Panel
            with ui.tab_panel(active_tab):
                create_active_terminations_section()
            
            # New Termination Panel
            with ui.tab_panel(new_tab):
                create_new_termination_section()
            
            # Completed Terminations Panel
            with ui.tab_panel(completed_tab):
                create_completed_terminations_section()
            
            # Security Analytics Panel
            with ui.tab_panel(analytics_tab):
                create_security_analytics_section()
            
            # Policies Panel
            with ui.tab_panel(policies_tab):
                create_termination_policies_section()

def create_termination_overview_section():
    """Create modern termination overview dashboard"""
    with ui.row().classes('w-full gap-6'):
        # Left column - Security metrics
        with ui.column().classes('flex-1'):
            ui.label('🔐 Security Overview').classes('text-2xl font-bold text-gray-800 mb-4')
            
            # Security metrics grid
            with ui.grid(columns=2).classes('w-full gap-4 mb-6'):
                # Active terminations card
                with ui.card().classes('p-6 bg-gradient-to-br from-red-500 to-red-600 text-white'):
                    ui.html('''
                        <div class="flex items-center justify-between">
                            <div>
                                <div class="text-3xl font-bold">4</div>
                                <div class="text-red-100">Active Cases</div>
                            </div>
                            <i class="material-icons text-4xl opacity-75">warning</i>
                        </div>
                    ''', sanitize=False)
                
                # High risk cases
                with ui.card().classes('p-6 bg-gradient-to-br from-orange-500 to-orange-600 text-white'):
                    ui.html('''
                        <div class="flex items-center justify-between">
                            <div>
                                <div class="text-3xl font-bold">2</div>
                                <div class="text-orange-100">High Risk</div>
                            </div>
                            <i class="material-icons text-4xl opacity-75">error</i>
                        </div>
                    ''', sanitize=False)
                
                # Security score
                with ui.card().classes('p-6 bg-gradient-to-br from-green-500 to-green-600 text-white'):
                    ui.html('''
                        <div class="flex items-center justify-between">
                            <div>
                                <div class="text-3xl font-bold">98%</div>
                                <div class="text-green-100">Security Score</div>
                            </div>
                            <i class="material-icons text-4xl opacity-75">shield</i>
                        </div>
                    ''', sanitize=False)
                
                # Compliance rate
                with ui.card().classes('p-6 bg-gradient-to-br from-blue-500 to-blue-600 text-white'):
                    ui.html('''
                        <div class="flex items-center justify-between">
                            <div>
                                <div class="text-3xl font-bold">100%</div>
                                <div class="text-blue-100">Compliance</div>
                            </div>
                            <i class="material-icons text-4xl opacity-75">verified</i>
                        </div>
                    ''', sanitize=False)
            
            # Recent security events
            with ui.card().classes('p-6'):
                ui.label('🔒 Recent Security Events').classes('text-xl font-semibold text-gray-800 mb-4')
                security_events = [
                    {"event": "Dual Authorization Required", "employee": "Michael Brown", "time": "1 hour ago", "severity": "high"},
                    {"event": "Access Revoked", "employee": "Jennifer Davis", "time": "3 hours ago", "severity": "medium"},
                    {"event": "Document Secured", "employee": "Robert Wilson", "time": "6 hours ago", "severity": "low"},
                    {"event": "Background Check Completed", "employee": "Lisa Thompson", "time": "1 day ago", "severity": "info"}
                ]
                
                for event in security_events:
                    with ui.row().classes('w-full items-center justify-between p-3 hover:bg-gray-50 rounded-lg'):
                        with ui.row().classes('items-center gap-3'):
                            severity_colors = {
                                'high': 'text-red-500',
                                'medium': 'text-orange-500',
                                'low': 'text-yellow-500',
                                'info': 'text-blue-500'
                            }
                            ui.icon('circle').classes(f'{severity_colors[event["severity"]]} text-xs')
                            with ui.column().classes('gap-1'):
                                ui.label(event['event']).classes('font-medium text-gray-800')
                                ui.label(event['employee']).classes('text-sm text-gray-600')
                        ui.label(event['time']).classes('text-xs text-gray-500')
        
        # Right column - Risk assessment and alerts
        with ui.column().classes('flex-1'):
            ui.label('⚠️ Risk Assessment').classes('text-2xl font-bold text-gray-800 mb-4')
            
            # Critical alert card
            with ui.card().classes('p-6 bg-gradient-to-br from-red-50 to-orange-50 border-l-4 border-red-500 mb-6'):
                ui.html('''
                    <div class="flex items-start gap-4">
                        <div class="bg-red-500 text-white p-2 rounded-full">
                            <i class="material-icons">warning</i>
                        </div>
                        <div>
                            <h3 class="text-lg font-semibold text-red-800 mb-2">Critical Security Alert</h3>
                            <p class="text-red-700 mb-3">Employee Michael Brown requires immediate dual authorization for termination due to administrative access level.</p>
                            <button class="bg-red-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-red-600">
                                Review Case
                            </button>
                        </div>
                    </div>
                ''', sanitize=False)
            
            # Risk factors analysis
            with ui.card().classes('p-6'):
                ui.label('📊 Risk Factor Analysis').classes('text-xl font-semibold text-gray-800 mb-4')
                ui.html('''
                    <div class="space-y-4">
                        <div class="flex justify-between items-center">
                            <span class="text-sm font-medium text-gray-600">Administrative Access</span>
                            <span class="text-sm text-red-600 font-semibold">HIGH RISK</span>
                        </div>
                        <div class="w-full bg-gray-200 rounded-full h-2">
                            <div class="bg-red-500 h-2 rounded-full" style="width: 90%"></div>
                        </div>
                        
                        <div class="flex justify-between items-center">
                            <span class="text-sm font-medium text-gray-600">Critical Projects</span>
                            <span class="text-sm text-orange-600 font-semibold">MEDIUM</span>
                        </div>
                        <div class="w-full bg-gray-200 rounded-full h-2">
                            <div class="bg-orange-500 h-2 rounded-full" style="width: 60%"></div>
                        </div>
                        
                        <div class="flex justify-between items-center">
                            <span class="text-sm font-medium text-gray-600">Security Clearance</span>
                            <span class="text-sm text-red-600 font-semibold">HIGH RISK</span>
                        </div>
                        <div class="w-full bg-gray-200 rounded-full h-2">
                            <div class="bg-red-500 h-2 rounded-full" style="width: 85%"></div>
                        </div>
                        
                        <div class="flex justify-between items-center">
                            <span class="text-sm font-medium text-gray-600">Data Access Level</span>
                            <span class="text-sm text-yellow-600 font-semibold">MEDIUM</span>
                        </div>
                        <div class="w-full bg-gray-200 rounded-full h-2">
                            <div class="bg-yellow-500 h-2 rounded-full" style="width: 70%"></div>
                        </div>
                    </div>
                ''', sanitize=False)

def create_security_dashboard():
    """Create security monitoring dashboard"""
    with ui.row().classes('w-full gap-4 mb-6'):
        # Active Terminations Card
        with ui.card().classes('p-4 bg-gradient-to-r from-red-500 to-red-600 text-white min-w-48'):
            with ui.row().classes('items-center justify-between'):
                with ui.column():
                    ui.label('Active Terminations').classes('text-red-100 text-sm')
                    active_count = len([r for r in termination_manager.get_termination_records() if r["status"] in ["Pending Approval", "In Progress"]])
                    ui.label(f'{active_count}').classes('text-2xl font-bold')
                ui.icon('pending_actions').classes('text-3xl text-red-200')
        
        # High Security Alerts Card
        with ui.card().classes('p-4 bg-gradient-to-r from-orange-500 to-orange-600 text-white min-w-48'):
            with ui.row().classes('items-center justify-between'):
                with ui.column():
                    ui.label('Security Alerts').classes('text-orange-100 text-sm')
                    high_security_count = len([r for r in termination_manager.get_termination_records() if r.get("security_level") == "High"])
                    ui.label(f'{high_security_count}').classes('text-2xl font-bold')
                ui.icon('warning').classes('text-3xl text-orange-200')
        
        # Compliance Score Card
        with ui.card().classes('p-4 bg-gradient-to-r from-green-500 to-green-600 text-white min-w-48'):
            with ui.row().classes('items-center justify-between'):
                with ui.column():
                    ui.label('Compliance Score').classes('text-green-100 text-sm')
                    ui.label('98%').classes('text-2xl font-bold')
                ui.icon('verified').classes('text-3xl text-green-200')
        
        # Audit Trail Card
        with ui.card().classes('p-4 bg-gradient-to-r from-blue-500 to-blue-600 text-white min-w-48'):
            with ui.row().classes('items-center justify-between'):
                with ui.column():
                    ui.label('Audit Events Today').classes('text-blue-100 text-sm')
                    ui.label('12').classes('text-2xl font-bold')
                ui.icon('history').classes('text-3xl text-blue-200')

def create_active_terminations_section():
    """Create active terminations management section"""
    with ui.card().classes('w-full p-6'):
        ui.label('Active Termination Cases').classes('text-xl font-semibold mb-4')
        
        active_records = [r for r in termination_manager.get_termination_records() if r["status"] in ["Pending Approval", "In Progress"]]
        
        if not active_records:
            with ui.column().classes('items-center py-8'):
                ui.icon('check_circle').classes('text-green-400 text-6xl mb-4')
                ui.label('No active termination cases').classes('text-gray-500 text-lg')
                ui.label('All termination processes are completed').classes('text-gray-400 text-sm')
        else:
            # Table header
            with ui.row().classes('w-full p-4 bg-gray-50 rounded-t-lg font-semibold'):
                ui.label('Case ID').classes('w-28')
                ui.label('Employee').classes('flex-1')
                ui.label('Type').classes('w-32')
                ui.label('Security Level').classes('w-28')
                ui.label('Status').classes('w-32')
                ui.label('Progress').classes('w-24 text-center')
                ui.label('Actions').classes('w-32 text-center')
            
            for record in active_records:
                security_color = 'text-red-600' if record.get("security_level") == "High" else 'text-yellow-600' if record.get("security_level") == "Medium" else 'text-green-600'
                
                with ui.row().classes('w-full p-4 border-b border-gray-200 hover:bg-gray-50'):
                    ui.label(record['id']).classes('w-28 font-mono text-sm')
                    
                    with ui.column().classes('flex-1'):
                        ui.label(record["employee_name"]).classes('font-medium')
                        ui.label(f'Effective: {record["effective_date"]}').classes('text-sm text-gray-500')
                    
                    ui.chip(record['termination_type'], color='gray').props('dense').classes('w-32')
                    
                    ui.label(record.get('security_level', 'Low')).classes(f'w-28 font-bold {security_color}')
                    
                    status_color = 'yellow' if 'Pending' in record['status'] else 'blue'
                    ui.chip(record['status'], color=status_color).props('dense').classes('w-32')
                    
                    # Progress indicator
                    progress = (record.get('documentation_complete', 0) + record.get('clearance_progress', 0)) // 2
                    progress_color = 'text-green-600' if progress >= 80 else 'text-yellow-600' if progress >= 50 else 'text-red-600'
                    ui.label(f'{progress}%').classes(f'w-24 text-center font-bold {progress_color}')
                    
                    with ui.row().classes('w-32 justify-center gap-1'):
                        ui.button(icon='visibility', on_click=lambda r=record: view_termination_details(r)).props('size=sm flat color=blue')
                        ui.button(icon='edit', on_click=lambda r=record: edit_termination_record(r)).props('size=sm flat color=orange')

def create_new_termination_section():
    """Create new termination initiation form with security validation"""
    with ui.card().classes('w-full p-6'):
        ui.label('Initiate Employee Termination').classes('text-xl font-semibold mb-4')
        
        # Security warning
        with ui.card().classes('p-4 border-l-4 border-red-500 bg-red-50 mb-6'):
            with ui.row().classes('items-center gap-2'):
                ui.icon('warning').classes('text-red-500 text-xl')
                ui.label('SECURITY NOTICE: All termination activities are logged and audited. Ensure compliance with company policies and legal requirements.').classes('text-red-700 font-medium')
        
        with ui.row().classes('w-full gap-6'):
            # Left column - Employee Selection
            with ui.column().classes('flex-1'):
                ui.label('Employee Information').classes('font-semibold text-lg text-red-600 mb-3')
                
                # Employee selection with security info
                employee_options = [f"{emp['id']} - {emp['name']} ({emp['department']})" for emp in termination_manager.employees]
                employee_select = ui.select(options=employee_options, label='Select Employee').props('outlined').classes('w-full mb-3')
                
                # Security information display
                security_info_display = ui.element('div').classes('p-3 border rounded-lg mb-3 bg-gray-50')
                
                # Termination type selection
                termination_types = list(termination_manager.termination_types.keys())
                termination_type_select = ui.select(options=termination_types, label='Termination Type').props('outlined').classes('w-full mb-3')
                
                ui.label('Initiation Date').classes('text-sm font-medium text-gray-700 mb-1')
                initiation_date_input = ui.date(value=date.today()).props('outlined').classes('w-full mb-3')
                
                ui.label('Effective Date').classes('text-sm font-medium text-gray-700 mb-1')
                effective_date_input = ui.date(value=date.today() + timedelta(days=30)).props('outlined').classes('w-full mb-3')
                
            # Right column - Details and Security
            with ui.column().classes('flex-1'):
                ui.label('Termination Details').classes('font-semibold text-lg text-red-600 mb-3')
                
                reason_input = ui.textarea('Reason for Termination', 
                    placeholder='Provide detailed reason for termination...'
                ).props('outlined rows=4').classes('w-full mb-3')
                
                # Security clearance requirements
                ui.label('Security Considerations').classes('font-semibold text-orange-600 mb-2')
                
                immediate_access_checkbox = ui.checkbox('Immediate access revocation required').classes('mb-2')
                security_escort_checkbox = ui.checkbox('Security escort required').classes('mb-2')
                confidential_data_checkbox = ui.checkbox('Employee has access to confidential data').classes('mb-3')
                
                # Documentation upload placeholder
                ui.label('Required Documentation').classes('font-semibold text-blue-600 mb-2')
                documentation_list = ui.element('div').classes('p-3 border rounded-lg mb-3')
        
        # Real-time security assessment
        with ui.row().classes('w-full p-4 bg-gray-50 rounded-lg mb-4'):
            ui.label('🛡️ Security Risk Assessment').classes('font-semibold text-gray-700')
            security_score_display = ui.label('Select employee and termination type for assessment').classes('text-blue-600 ml-4 font-bold')
        
        # Update security info when selections change
        def update_security_assessment():
            if employee_select.value and termination_type_select.value:
                # Extract employee ID from selection
                employee_id = employee_select.value.split(' - ')[0]
                employee = next((emp for emp in termination_manager.employees if emp["id"] == employee_id), None)
                
                if employee:
                    # Update security info display
                    security_info_display.clear()
                    with security_info_display:
                        ui.label('Employee Security Profile').classes('font-semibold text-blue-600 mb-2')
                        ui.label(f'Security Clearance: {employee.get("security_clearance", "Unknown")}').classes('text-sm')
                        ui.label(f'Access Level: {employee.get("access_level", "Unknown")}').classes('text-sm')
                        ui.label(f'Direct Reports: {employee.get("direct_reports", 0)}').classes('text-sm')
                        if employee.get("critical_projects"):
                            ui.label(f'Critical Projects: {", ".join(employee["critical_projects"])}').classes('text-sm text-red-600')
                    
                    # Update documentation requirements
                    termination_config = termination_manager.termination_types.get(termination_type_select.value, {})
                    documentation_list.clear()
                    with documentation_list:
                        ui.label('Required Documents:').classes('font-semibold mb-2')
                        for doc in termination_config.get('documentation_required', []):
                            ui.label(f'• {doc}').classes('text-sm text-gray-700')
                    
                    # Calculate security score
                    mock_termination_data = {
                        "employee_id": employee_id,
                        "termination_type": termination_type_select.value,
                        "initiation_date": initiation_date_input.value.strftime("%Y-%m-%d") if initiation_date_input.value else "",
                        "effective_date": effective_date_input.value.strftime("%Y-%m-%d") if effective_date_input.value else "",
                        "documentation_provided": []
                    }
                    
                    security_score = termination_manager.calculate_security_score(mock_termination_data)
                    score_color = 'text-green-600' if security_score >= 80 else 'text-yellow-600' if security_score >= 60 else 'text-red-600'
                    security_score_display.text = f'Security Score: {security_score}%'
                    security_score_display.classes(f'{score_color} ml-4 font-bold')
        
        # Bind security assessment updates
        employee_select.on('update:model-value', lambda: update_security_assessment())
        termination_type_select.on('update:model-value', lambda: update_security_assessment())
        initiation_date_input.on('update:model-value', lambda: update_security_assessment())
        effective_date_input.on('update:model-value', lambda: update_security_assessment())
        
        # Action buttons
        with ui.row().classes('w-full justify-end gap-2 mt-6'):
            ui.button('Security Validation', on_click=lambda: validate_termination_request(
                employee_select.value, termination_type_select.value, initiation_date_input.value,
                effective_date_input.value, reason_input.value
            )).props('flat color=orange')
            ui.button('Initiate Termination', on_click=lambda: submit_termination_request(
                employee_select.value, termination_type_select.value, initiation_date_input.value,
                effective_date_input.value, reason_input.value, immediate_access_checkbox.value,
                security_escort_checkbox.value, confidential_data_checkbox.value
            )).props('color=red')

def create_completed_terminations_section():
    """Create completed terminations archive"""
    with ui.card().classes('w-full p-6'):
        ui.label('Completed Terminations Archive').classes('text-xl font-semibold mb-4')
        
        completed_records = [r for r in termination_manager.get_termination_records() if r["status"] == "Completed"]
        
        if completed_records:
            # Archive table with security indicators
            with ui.row().classes('w-full p-4 bg-gray-50 rounded-t-lg font-semibold'):
                ui.label('Case ID').classes('w-28')
                ui.label('Employee').classes('flex-1')
                ui.label('Type').classes('w-32')
                ui.label('Completion Date').classes('w-32')
                ui.label('Security Score').classes('w-28 text-center')
                ui.label('Actions').classes('w-24 text-center')
            
            for record in completed_records:
                with ui.row().classes('w-full p-4 border-b border-gray-200 hover:bg-gray-50'):
                    ui.label(record['id']).classes('w-28 font-mono text-sm')
                    ui.label(record["employee_name"]).classes('flex-1 font-medium')
                    ui.chip(record['termination_type'], color='gray').props('dense').classes('w-32')
                    ui.label(record["effective_date"]).classes('w-32 text-sm')
                    
                    score_color = 'text-green-600' if record['security_score'] >= 80 else 'text-yellow-600' if record['security_score'] >= 60 else 'text-red-600'
                    ui.label(f"{record['security_score']}%").classes(f'w-28 text-center font-bold {score_color}')
                    
                    ui.button(icon='visibility', on_click=lambda r=record: view_termination_details(r)).props('size=sm flat color=blue').classes('w-24')
        else:
            ui.label('No completed terminations found').classes('text-gray-500 text-center py-8')

def create_security_analytics_section():
    """Create security analytics and monitoring"""
    with ui.card().classes('w-full p-6'):
        ui.label('🛡️ Security Analytics Dashboard').classes('text-xl font-semibold mb-4')
        
        with ui.row().classes('w-full gap-6'):
            # Security metrics
            with ui.card().classes('flex-1 p-4'):
                ui.label('Security Metrics').classes('font-semibold text-red-600 mb-3')
                
                metrics = [
                    {"label": "High Security Cases", "value": "3", "trend": "↑"},
                    {"label": "Average Security Score", "value": "87%", "trend": "→"},
                    {"label": "Compliance Rate", "value": "98%", "trend": "↑"},
                    {"label": "Audit Findings", "value": "0", "trend": "↓"}
                ]
                
                for metric in metrics:
                    with ui.row().classes('justify-between items-center mb-2'):
                        ui.label(metric["label"]).classes('text-sm')
                        with ui.row().classes('items-center gap-2'):
                            ui.label(metric["value"]).classes('font-bold')
                            ui.label(metric["trend"]).classes('text-blue-600 font-bold')
            
            # Risk assessment
            with ui.card().classes('flex-1 p-4'):
                ui.label('Risk Assessment').classes('font-semibold text-orange-600 mb-3')
                
                risk_factors = [
                    {"factor": "Privileged Access Users", "level": "Medium", "count": 2},
                    {"factor": "Critical Project Members", "level": "High", "count": 1},
                    {"factor": "Immediate Terminations", "level": "Low", "count": 0},
                    {"factor": "Documentation Gaps", "level": "Low", "count": 1}
                ]
                
                for risk in risk_factors:
                    color = 'text-red-600' if risk["level"] == "High" else 'text-yellow-600' if risk["level"] == "Medium" else 'text-green-600'
                    with ui.row().classes('justify-between items-center mb-2'):
                        ui.label(risk["factor"]).classes('text-sm')
                        with ui.row().classes('items-center gap-2'):
                            ui.label(str(risk["count"])).classes('font-bold')
                            ui.chip(risk["level"], color='gray' if risk["level"] == "Low" else 'yellow' if risk["level"] == "Medium" else 'red').props('dense size=sm')

def create_termination_policies_section():
    """Create termination policies and procedures"""
    with ui.card().classes('w-full p-6'):
        ui.label('📋 Termination Policies & Procedures').classes('text-xl font-semibold mb-4')
        
        for termination_type, config in termination_manager.termination_types.items():
            with ui.expansion(termination_type, icon='policy').classes('w-full mb-2'):
                with ui.column().classes('p-4'):
                    with ui.grid(columns=2).classes('gap-4'):
                        # Left column
                        with ui.column():
                            ui.label('Policy Details').classes('font-semibold text-blue-600 mb-2')
                            ui.label(f'Code: {config["code"]}').classes('text-sm mb-1')
                            ui.label(f'Notice Period: {config["notice_period_days"]} days').classes('text-sm mb-1')
                            ui.label(f'Security Level: {config["security_level"]}').classes('text-sm mb-1')
                            ui.label(f'Approval Required: {"Yes" if config["requires_approval"] else "No"}').classes('text-sm mb-1')
                            ui.label(f'Exit Interview: {"Required" if config["exit_interview_required"] else "Optional"}').classes('text-sm mb-1')
                        
                        # Right column
                        with ui.column():
                            ui.label('Requirements').classes('font-semibold text-green-600 mb-2')
                            
                            ui.label('Documentation Required:').classes('text-sm font-medium mb-1')
                            for doc in config["documentation_required"]:
                                ui.label(f'• {doc}').classes('text-sm text-gray-700')
                            
                            ui.label('Clearance Checklist:').classes('text-sm font-medium mt-2 mb-1')
                            for item in config["clearance_checklist"]:
                                ui.label(f'• {item}').classes('text-sm text-gray-700')

# Action functions with security logging
async def submit_termination_request(employee_selection, termination_type, initiation_date, effective_date, reason, immediate_access, security_escort, confidential_data):
    """Submit termination request with comprehensive security validation"""
    if not all([employee_selection, termination_type, initiation_date, effective_date, reason]):
        ui.notify('Please fill in all required fields', color='negative')
        return
    
    # Extract employee ID
    employee_id = employee_selection.split(' - ')[0]
    employee_name = employee_selection.split(' - ')[1].split(' (')[0]
    
    # Validate dates
    if effective_date <= initiation_date:
        ui.notify('Effective date must be after initiation date', color='negative')
        return
    
    # Final security validation
    termination_data = {
        "employee_id": employee_id,
        "employee_name": employee_name,
        "termination_type": termination_type,
        "initiation_date": initiation_date.strftime("%Y-%m-%d"),
        "effective_date": effective_date.strftime("%Y-%m-%d"),
        "reason": reason,
        "immediate_access_revocation": immediate_access,
        "security_escort_required": security_escort,
        "confidential_data_access": confidential_data,
        "initiated_by": "HR"
    }
    
    validation = termination_manager.validate_termination_request(termination_data)
    
    if not validation["valid"]:
        error_messages = '\n'.join(validation["errors"])
        ui.notify(f'Security Validation Failed:\n{error_messages}', color='negative')
        return
    
    success, record_id, security_score = termination_manager.create_termination_record(termination_data)
    
    if success:
        ui.notify(f'Termination case initiated successfully! Case ID: {record_id}', color='positive')
        
        # Show security confirmation dialog
        with ui.dialog() as dialog, ui.card().classes('w-96 p-6'):
            ui.label('🛡️ Termination Case Initiated').classes('text-xl font-semibold mb-4 text-red-600')
            ui.label(f'Case ID: {record_id}').classes('font-mono text-sm mb-2')
            ui.label(f'Security Score: {security_score}%').classes('text-blue-600 font-semibold mb-4')
            
            if validation["security_alerts"]:
                ui.label('Security Alerts:').classes('font-semibold text-red-600 mb-2')
                for alert in validation["security_alerts"]:
                    ui.label(f'⚠️ {alert}').classes('text-sm text-red-500 mb-1')
            
            if validation["warnings"]:
                ui.label('Warnings:').classes('font-semibold text-yellow-600 mb-2')
                for warning in validation["warnings"]:
                    ui.label(f'⚠️ {warning}').classes('text-sm text-yellow-500 mb-1')
            
            ui.label('Next Steps:').classes('font-semibold mb-2')
            ui.label('• Security clearance process initiated').classes('text-sm mb-1')
            ui.label('• Approval workflow activated').classes('text-sm mb-1')
            ui.label('• Audit trail created').classes('text-sm mb-4')
            
            ui.button('Acknowledge', on_click=dialog.close).props('color=red')
        
        dialog.open()
    else:
        ui.notify('Error creating termination case. Please try again.', color='negative')

async def validate_termination_request(employee_selection, termination_type, initiation_date, effective_date, reason):
    """Validate termination request and show security assessment"""
    if not all([employee_selection, termination_type]):
        ui.notify('Please select employee and termination type', color='warning')
        return
    
    employee_id = employee_selection.split(' - ')[0]
    
    termination_data = {
        "employee_id": employee_id,
        "termination_type": termination_type,
        "initiation_date": initiation_date.strftime("%Y-%m-%d") if initiation_date else "",
        "effective_date": effective_date.strftime("%Y-%m-%d") if effective_date else "",
        "reason": reason
    }
    
    validation = termination_manager.validate_termination_request(termination_data)
    
    # Show validation results
    with ui.dialog() as dialog, ui.card().classes('w-[500px] p-6'):
        ui.label('🔍 Security Validation Results').classes('text-xl font-semibold mb-4')
        
        if validation["valid"]:
            ui.label('✅ Validation Passed').classes('text-green-600 font-semibold mb-4')
        else:
            ui.label('❌ Validation Failed').classes('text-red-600 font-semibold mb-4')
            ui.label('Errors:').classes('font-semibold text-red-600 mb-2')
            for error in validation["errors"]:
                ui.label(f'• {error}').classes('text-sm text-red-500 mb-1')
        
        if validation["warnings"]:
            ui.label('Warnings:').classes('font-semibold text-yellow-600 mb-2 mt-4')
            for warning in validation["warnings"]:
                ui.label(f'• {warning}').classes('text-sm text-yellow-500 mb-1')
        
        if validation["security_alerts"]:
            ui.label('Security Alerts:').classes('font-semibold text-red-600 mb-2 mt-4')
            for alert in validation["security_alerts"]:
                ui.label(f'🚨 {alert}').classes('text-sm text-red-500 mb-1')
        
        ui.button('Close', on_click=dialog.close).props('color=primary').classes('w-full mt-4')
    
    dialog.open()

async def view_termination_details(record):
    """View detailed termination record with security information"""
    with ui.dialog() as dialog, ui.card().classes('w-[700px] p-6'):
        ui.label(f'Termination Case Details - {record["id"]}').classes('text-xl font-semibold mb-4')
        
        with ui.grid(columns=2).classes('gap-4 w-full'):
            # Left column
            with ui.column().classes('gap-3'):
                ui.label('Case Information').classes('font-semibold text-blue-600')
                ui.label(f'Employee: {record["employee_name"]}').classes('text-sm')
                ui.label(f'Type: {record["termination_type"]}').classes('text-sm')
                ui.label(f'Initiation Date: {record["initiation_date"]}').classes('text-sm')
                ui.label(f'Effective Date: {record["effective_date"]}').classes('text-sm')
                ui.label(f'Status: {record["status"]}').classes('text-sm')
            
            # Right column
            with ui.column().classes('gap-3'):
                ui.label('Security Information').classes('font-semibold text-red-600')
                ui.label(f'Security Level: {record.get("security_level", "Unknown")}').classes('text-sm')
                ui.label(f'Security Score: {record["security_score"]}%').classes('text-sm')
                ui.label(f'Approval Stage: {record["approval_stage"]}').classes('text-sm')
                ui.label(f'Documentation: {record.get("documentation_complete", 0)}%').classes('text-sm')
                ui.label(f'Clearance Progress: {record.get("clearance_progress", 0)}%').classes('text-sm')
        
        ui.label('Reason:').classes('font-semibold text-purple-600 mt-4')
        ui.label(record["reason"]).classes('text-sm bg-gray-50 p-3 rounded')
        
        if record.get("audit_hash"):
            ui.label('Audit Information:').classes('font-semibold text-gray-600 mt-4')
            ui.label(f'Audit Hash: {record["audit_hash"][:16]}...').classes('text-xs font-mono bg-gray-100 p-2 rounded')
        
        with ui.row().classes('w-full justify-end mt-6'):
            ui.button('Close', on_click=dialog.close).props('flat')
    
    dialog.open()

async def edit_termination_record(record):
    """Edit termination record with security controls"""
    ui.notify(f'Edit case {record["id"]} - Enhanced security controls required', color='info')



# Integration APIs with security controls
def get_termination_records_for_approval(approver_id, security_clearance):
    """API for managers to get termination records requiring approval"""
    # Security filtering based on clearance level
    allowed_levels = {
        "High": ["Low", "Medium", "High"],
        "Medium": ["Low", "Medium"],
        "Low": ["Low"]
    }
    
    filter_levels = allowed_levels.get(security_clearance, ["Low"])
    return termination_manager.get_termination_records(filter_levels)

def approve_termination_record(record_id, approver_id, security_clearance):
    """API for approving termination records with security validation"""
    # Additional security validation would be implemented here
    return termination_manager.update_termination_status(record_id, "Approved", approver_id)

# Modern dialog functions for termination page
async def show_security_audit():
    """Show security audit dialog"""
    with ui.dialog() as dialog, ui.card().classes('w-4xl max-w-4xl p-8'):
        ui.html('''
            <div class="flex items-center gap-3 mb-6">
                <div class="bg-red-500 text-white p-3 rounded-full">
                    <i class="material-icons text-2xl">shield</i>
                </div>
                <div>
                    <h2 class="text-2xl font-bold text-red-800">Security Audit Trail</h2>
                    <p class="text-red-600">Complete audit history and security monitoring</p>
                </div>
            </div>
        ''', sanitize=False)
        
        with ui.row().classes('w-full gap-6'):
            # Left column - Recent audits
            with ui.column().classes('flex-1'):
                ui.label('🔒 Recent Security Events').classes('text-xl font-semibold text-gray-800 mb-4')
                with ui.card().classes('p-4 max-h-80 overflow-y-auto'):
                    audit_events = [
                        {"timestamp": "2025-10-12 14:30", "event": "Dual Authorization Required", "user": "admin@company.com", "level": "HIGH"},
                        {"timestamp": "2025-10-12 12:15", "event": "Access Revoked", "user": "hr@company.com", "level": "MEDIUM"},
                        {"timestamp": "2025-10-12 10:45", "event": "Document Accessed", "user": "manager@company.com", "level": "LOW"},
                        {"timestamp": "2025-10-12 09:20", "event": "Security Check Passed", "user": "security@company.com", "level": "INFO"}
                    ]
                    
                    for event in audit_events:
                        with ui.row().classes('w-full items-center justify-between p-2 hover:bg-gray-50 rounded'):
                            with ui.column().classes('gap-1'):
                                ui.label(event['event']).classes('font-medium text-sm')
                                ui.label(f"{event['timestamp']} - {event['user']}").classes('text-xs text-gray-500')
                            level_colors = {"HIGH": "text-red-600", "MEDIUM": "text-orange-600", "LOW": "text-yellow-600", "INFO": "text-blue-600"}
                            ui.label(event['level']).classes(f'text-xs font-bold {level_colors[event["level"]]}')
            
            # Right column - Security stats
            with ui.column().classes('flex-1'):
                ui.label('📊 Security Statistics').classes('text-xl font-semibold text-gray-800 mb-4')
                with ui.card().classes('p-4'):
                    ui.html('''
                        <div class="space-y-4">
                            <div class="flex justify-between items-center">
                                <span class="font-medium">Total Audit Events</span>
                                <span class="text-blue-600 font-bold">1,247</span>
                            </div>
                            <div class="flex justify-between items-center">
                                <span class="font-medium">High Security Events</span>
                                <span class="text-red-600 font-bold">15</span>
                            </div>
                            <div class="flex justify-between items-center">
                                <span class="font-medium">Compliance Score</span>
                                <span class="text-green-600 font-bold">98.7%</span>
                            </div>
                            <div class="flex justify-between items-center">
                                <span class="font-medium">Failed Authorizations</span>
                                <span class="text-orange-600 font-bold">3</span>
                            </div>
                        </div>
                    ''', sanitize=False)
        
        ui.button('Close', on_click=dialog.close).props('flat color=red').classes('mt-6')
    dialog.open()

async def show_new_termination_dialog():
    """Show new termination creation dialog"""
    with ui.dialog() as dialog, ui.card().classes('w-3xl max-w-3xl p-8'):
        ui.html('''
            <div class="flex items-center gap-3 mb-6">
                <div class="bg-red-500 text-white p-3 rounded-full">
                    <i class="material-icons text-2xl">person_remove</i>
                </div>
                <div>
                    <h2 class="text-2xl font-bold text-red-800">Initiate Employee Termination</h2>
                    <p class="text-red-600">⚠️ High security process - requires dual authorization</p>
                </div>
            </div>
        ''', sanitize=False)
        
        # Security warning
        with ui.card().classes('p-4 bg-red-50 border-l-4 border-red-500 mb-6'):
            ui.html('''
                <div class="flex items-center gap-2">
                    <i class="material-icons text-red-500">warning</i>
                    <div>
                        <div class="font-semibold text-red-800">Security Notice</div>
                        <div class="text-sm text-red-700">This action requires additional authorization for high-risk employees</div>
                    </div>
                </div>
            ''', sanitize=False)
        
        # Quick termination form
        with ui.row().classes('w-full gap-4 mb-4'):
            employee_select = ui.select(['EMP-001 - John Smith (High Risk)', 'EMP-002 - Sarah Johnson'], 
                label='Select Employee').classes('flex-1')
            termination_type = ui.select(['Voluntary Resignation', 'End of Contract', 'Dismissal for Cause', 'Redundancy'], 
                label='Termination Type').classes('flex-1')
        
        effective_date = ui.date('Effective Date').classes('w-full mb-4')
        reason_input = ui.textarea('Reason', placeholder='Provide detailed reason for termination...').props('rows=3').classes('w-full mb-4')
        
        # Security options
        with ui.row().classes('w-full gap-4 mb-4'):
            ui.checkbox('Immediate access revocation required').classes('text-red-600')
            ui.checkbox('Security escort required').classes('text-orange-600')
        
        with ui.row().classes('gap-2 justify-end'):
            ui.button('Cancel', on_click=dialog.close).props('flat')
            ui.button('Initiate Termination', on_click=lambda: [ui.notify('Termination process initiated - pending authorization', color='warning'), dialog.close()]).props('color=red')
    
    dialog.open()