from nicegui import ui, app
from helperFuns import imagePath
from assets import FlipCards, SearchBox
import asyncio
from datetime import datetime, timedelta, date
import json
import uuid

# Smart Transfer Request Management System with Advanced HR Algorithms
class TransferRequestManager:
    """
    Intelligent transfer request system with smart algorithms for
    eligibility checking, approval workflows, and impact analysis
    """
    
    def __init__(self):
        # Integration with department and employee systems
        self.departments = [
            {"id": "DEPT-001", "name": "Human Resources", "code": "HR", "capacity": 8, "current_staff": 8},
            {"id": "DEPT-002", "name": "Information Technology", "code": "IT", "capacity": 30, "current_staff": 24},
            {"id": "DEPT-003", "name": "Finance & Accounting", "code": "FIN", "capacity": 15, "current_staff": 12},
            {"id": "DEPT-004", "name": "Marketing & Sales", "code": "MKT", "capacity": 25, "current_staff": 18},
            {"id": "DEPT-005", "name": "Operations", "code": "OPS", "capacity": 20, "current_staff": 16},
            {"id": "DEPT-006", "name": "Customer Service", "code": "CS", "capacity": 12, "current_staff": 10}
        ]
        
        self.transfer_requests = [
            {
                "id": "TR-001",
                "employee_id": "EMP-123",
                "employee_name": "John Smith",
                "current_department": "HR",
                "requested_department": "IT",
                "request_date": "2024-10-01",
                "status": "Pending Review",
                "priority": "Normal",
                "justification": "Seeking career growth in technology sector",
                "estimated_transition_date": "2024-11-01",
                "approval_stage": "Manager Review",
                "smart_score": 78,
                "created_by": "EMP-123"
            },
            {
                "id": "TR-002",
                "employee_id": "EMP-456",
                "employee_name": "Sarah Johnson",
                "current_department": "FIN",
                "requested_department": "MKT",
                "request_date": "2024-09-28",
                "status": "Under Review",
                "priority": "High",
                "justification": "Better alignment with skills and interests",
                "estimated_transition_date": "2024-10-20",
                "approval_stage": "HR Review",
                "smart_score": 85,
                "created_by": "EMP-456"
            }
        ]
        
        # Smart algorithm configurations
        self.eligibility_criteria = {
            "minimum_tenure_months": 6,
            "performance_threshold": 70,
            "pending_requests_limit": 1,
            "cooldown_period_months": 3,
            "critical_position_restriction": True
        }
        
        self.approval_workflow = {
            "stages": [
                {"name": "Manager Review", "auto_approve_score": 90, "timeout_days": 5},
                {"name": "HR Review", "auto_approve_score": 85, "timeout_days": 7},
                {"name": "Receiving Dept Review", "auto_approve_score": 95, "timeout_days": 3},
                {"name": "Final Approval", "auto_approve_score": 100, "timeout_days": 2}
            ]
        }

    def get_employee_eligibility(self, employee_id):
        """Smart algorithm to check employee transfer eligibility"""
        # This would integrate with employee data system
        mock_employee_data = {
            "tenure_months": 12,
            "performance_score": 82,
            "current_position_critical": False,
            "pending_requests": 0,
            "last_transfer_date": "2023-05-01",
            "disciplinary_actions": 0,
            "skill_compatibility": 75
        }
        
        eligibility_score = 0
        issues = []
        
        # Tenure check
        if mock_employee_data["tenure_months"] >= self.eligibility_criteria["minimum_tenure_months"]:
            eligibility_score += 25
        else:
            issues.append(f"Minimum tenure requirement not met (need {self.eligibility_criteria['minimum_tenure_months']} months)")
        
        # Performance check
        if mock_employee_data["performance_score"] >= self.eligibility_criteria["performance_threshold"]:
            eligibility_score += 25
        else:
            issues.append(f"Performance below threshold (need {self.eligibility_criteria['performance_threshold']}%)")
        
        # Pending requests check
        if mock_employee_data["pending_requests"] < self.eligibility_criteria["pending_requests_limit"]:
            eligibility_score += 20
        else:
            issues.append("Maximum pending requests exceeded")
        
        # Critical position check
        if not mock_employee_data["current_position_critical"]:
            eligibility_score += 15
        else:
            issues.append("Currently in critical position")
        
        # Cooldown period check
        last_transfer = datetime.strptime(mock_employee_data["last_transfer_date"], "%Y-%m-%d")
        cooldown_end = last_transfer + timedelta(days=self.eligibility_criteria["cooldown_period_months"] * 30)
        if datetime.now() >= cooldown_end:
            eligibility_score += 15
        else:
            issues.append(f"Cooldown period active until {cooldown_end.strftime('%Y-%m-%d')}")
        
        return {
            "eligible": eligibility_score >= 80,
            "score": eligibility_score,
            "issues": issues,
            "recommendation": self.get_eligibility_recommendation(eligibility_score)
        }

    def get_eligibility_recommendation(self, score):
        """Generate recommendation based on eligibility score"""
        if score >= 90:
            return "Highly recommended for transfer"
        elif score >= 80:
            return "Eligible for transfer with standard process"
        elif score >= 60:
            return "May be eligible with manager approval"
        else:
            return "Not currently eligible for transfer"

    def calculate_smart_score(self, request_data):
        """Advanced algorithm to calculate smart approval score"""
        score = 50  # Base score
        
        # Department capacity analysis
        receiving_dept = next((d for d in self.departments if d["name"] == request_data["requested_department"]), None)
        if receiving_dept:
            capacity_ratio = receiving_dept["current_staff"] / receiving_dept["capacity"]
            if capacity_ratio < 0.8:
                score += 20  # Good capacity
            elif capacity_ratio < 0.9:
                score += 10  # Moderate capacity
            else:
                score -= 10  # Low capacity
        
        # Urgency and business justification
        justification_keywords = ["growth", "skills", "career", "development", "opportunity"]
        justification_lower = request_data["justification"].lower()
        keyword_matches = sum(1 for keyword in justification_keywords if keyword in justification_lower)
        score += keyword_matches * 3
        
        # Priority adjustment
        if request_data["priority"] == "High":
            score += 15
        elif request_data["priority"] == "Low":
            score -= 5
        
        # Transition timeline reasonableness
        request_date = datetime.strptime(request_data["estimated_transition_date"], "%Y-%m-%d")
        days_until_transition = (request_date - datetime.now()).days
        if 14 <= days_until_transition <= 60:
            score += 10  # Reasonable timeline
        elif days_until_transition < 14:
            score -= 15  # Too rushed
        elif days_until_transition > 90:
            score -= 5   # Too distant
        
        return min(max(score, 0), 100)  # Clamp between 0-100

    def create_transfer_request(self, request_data):
        """Create new transfer request with smart validation"""
        # Generate unique ID
        new_id = f"TR-{str(uuid.uuid4())[:6].upper()}"
        
        # Calculate smart score
        smart_score = self.calculate_smart_score(request_data)
        
        new_request = {
            "id": new_id,
            "request_date": datetime.now().strftime("%Y-%m-%d"),
            "status": "Pending Review",
            "approval_stage": "Manager Review",
            "smart_score": smart_score,
            "created_by": request_data.get("employee_id", "CURRENT_USER"),
            **request_data
        }
        
        self.transfer_requests.append(new_request)
        return True, new_id, smart_score

    def get_department_recommendations(self, employee_profile):
        """AI-powered department recommendations"""
        recommendations = []
        
        # Mock employee skills and preferences
        employee_skills = ["communication", "analysis", "technology", "leadership"]
        
        for dept in self.departments:
            compatibility_score = 0
            
            # Capacity check
            capacity_ratio = dept["current_staff"] / dept["capacity"]
            if capacity_ratio < 0.8:
                compatibility_score += 30
            elif capacity_ratio < 0.9:
                compatibility_score += 20
            else:
                compatibility_score += 5
            
            # Skill matching (simplified)
            dept_skill_requirements = {
                "Human Resources": ["communication", "leadership", "empathy"],
                "Information Technology": ["technology", "analysis", "problem-solving"],
                "Finance & Accounting": ["analysis", "attention-to-detail", "mathematics"],
                "Marketing & Sales": ["communication", "creativity", "persuasion"],
                "Operations": ["organization", "efficiency", "leadership"],
                "Customer Service": ["communication", "patience", "problem-solving"]
            }
            
            required_skills = dept_skill_requirements.get(dept["name"], [])
            skill_match = len(set(employee_skills) & set(required_skills)) / len(required_skills) if required_skills else 0
            compatibility_score += skill_match * 40
            
            # Growth opportunity (simplified calculation)
            compatibility_score += 20  # Base growth opportunity
            
            recommendations.append({
                "department": dept["name"],
                "code": dept["code"],
                "compatibility_score": min(compatibility_score, 100),
                "capacity_status": "Available" if capacity_ratio < 0.9 else "Limited",
                "growth_potential": "High" if compatibility_score > 80 else "Medium" if compatibility_score > 60 else "Low"
            })
        
        return sorted(recommendations, key=lambda x: x["compatibility_score"], reverse=True)

    def get_my_requests(self, employee_id):
        """Get transfer requests for current employee"""
        return [req for req in self.transfer_requests if req["created_by"] == employee_id]

    def update_request_status(self, request_id, new_status, approval_stage=None):
        """Update request status with workflow progression"""
        for request in self.transfer_requests:
            if request["id"] == request_id:
                request["status"] = new_status
                if approval_stage:
                    request["approval_stage"] = approval_stage
                request["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                return True
        return False

# Global transfer request manager
transfer_manager = TransferRequestManager()

def RequestTransfer():
    """
    Modern Request Transfer page with smart HR algorithms
    and intelligent recommendation system
    """
    
    # Modern gradient header with career growth focus
    with ui.element('div').classes('w-full bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white p-8 rounded-lg mb-8 shadow-xl'):
        with ui.row().classes('w-full justify-between items-center'):
            with ui.column():
                ui.html('''
                    <div class="flex items-center gap-4">
                        <div class="bg-white bg-opacity-20 p-3 rounded-full">
                            <i class="material-icons text-4xl">transfer_within_a_station</i>
                        </div>
                        <div>
                            <h1 class="text-4xl font-bold mb-2">Smart Career Transitions</h1>
                            <p class="text-indigo-100 text-lg">AI-powered transfer planning and intelligent career pathway optimization</p>
                        </div>
                    </div>
                ''', sanitize=False)
                
                # Breadcrumb navigation
                with ui.row().classes('items-center gap-2 text-sm text-indigo-200 mt-4'):
                    ui.icon('home').classes('text-indigo-300')
                    ui.label('Dashboard')
                    ui.icon('chevron_right').classes('text-xs')
                    ui.label('Employees')
                    ui.icon('chevron_right').classes('text-xs')
                    ui.label('Transfer Management').classes('text-white font-medium')
            
            # Smart action buttons
            with ui.column().classes('gap-3'):
                ui.button('🚀 Career Pathways', on_click=show_career_pathways).props('color=white text-color=indigo-700').classes('font-semibold')
                ui.button('📈 Transfer Analytics', on_click=show_transfer_analytics).props('outlined color=white').classes('font-semibold')

    # Smart transfer dashboard
    create_smart_transfer_dashboard()

    # Main content with tabs
    with ui.tabs().classes('w-full mb-4') as tabs:
        request_tab = ui.tab('New Request', icon='send')
        recommendations_tab = ui.tab('Smart Recommendations', icon='psychology')
        my_requests_tab = ui.tab('My Requests', icon='folder_shared')
        guidelines_tab = ui.tab('Guidelines', icon='info')

    with ui.tab_panels(tabs, value=request_tab).classes('w-full'):
        # New Request Panel
        with ui.tab_panel(request_tab):
            create_new_request_section()
        
        # Smart Recommendations Panel
        with ui.tab_panel(recommendations_tab):
            create_recommendations_section()
        
        # My Requests Panel
        with ui.tab_panel(my_requests_tab):
            create_my_requests_section()
        
        # Guidelines Panel
        with ui.tab_panel(guidelines_tab):
            create_guidelines_section()

def create_eligibility_check_section():
    """Create smart eligibility checking section"""
    with ui.card().classes('w-full p-6 mb-6 bg-gradient-to-r from-blue-50 to-indigo-50'):
        ui.label('🧠 Smart Eligibility Check').classes('text-xl font-semibold mb-4 text-blue-800')
        
        # Mock current employee ID
        current_employee_id = "EMP-123"
        eligibility = transfer_manager.get_employee_eligibility(current_employee_id)
        
        with ui.row().classes('w-full gap-6 items-center'):
            # Eligibility score circle
            with ui.column().classes('items-center'):
                score_color = 'text-green-600' if eligibility['score'] >= 80 else 'text-yellow-600' if eligibility['score'] >= 60 else 'text-red-600'
                with ui.element('div').classes('relative w-24 h-24'):
                    # Background circle
                    ui.element('div').classes('w-24 h-24 rounded-full border-8 border-gray-200')
                    # Progress circle
                    ui.element('div').classes(f'absolute top-0 left-0 w-24 h-24 rounded-full border-8 border-t-blue-500 border-r-blue-500').style(f'transform: rotate({eligibility["score"] * 3.6}deg); transition: transform 1s ease-in-out;')
                    # Score text
                    with ui.element('div').classes('absolute inset-0 flex items-center justify-center'):
                        ui.label(f'{eligibility["score"]}%').classes(f'text-lg font-bold {score_color}')
                
                ui.label('Eligibility Score').classes('text-sm text-gray-600 mt-2')
            
            # Status and recommendation
            with ui.column().classes('flex-1'):
                status_color = 'text-green-600' if eligibility['eligible'] else 'text-red-600'
                status_text = '✅ Eligible for Transfer' if eligibility['eligible'] else '❌ Not Currently Eligible'
                ui.label(status_text).classes(f'text-lg font-semibold {status_color}')
                ui.label(eligibility['recommendation']).classes('text-gray-700 mt-1')
                
                if eligibility['issues']:
                    ui.label('Issues to Address:').classes('text-sm font-medium text-red-600 mt-3')
                    for issue in eligibility['issues']:
                        ui.label(f'• {issue}').classes('text-sm text-red-500 ml-4')

def create_new_request_section():
    """Create new transfer request form"""
    with ui.card().classes('w-full p-6'):
        ui.label('Submit New Transfer Request').classes('text-xl font-semibold mb-4')
        
        with ui.row().classes('w-full gap-6'):
            # Left column - Basic Information
            with ui.column().classes('flex-1'):
                ui.label('Basic Information').classes('font-semibold text-lg text-blue-600 mb-3')
                
                current_dept = ui.input(label='Current Department', value='Human Resources').props('outlined readonly').classes('w-full mb-3')
                
                # Department selection with smart filtering
                departments = [dept["name"] for dept in transfer_manager.departments if dept["name"] != "Human Resources"]
                requested_dept = ui.select(options=departments, label='Requested Department', with_input=True).props('outlined').classes('w-full mb-3')
                
                priority = ui.select(
                    options=['Normal', 'High', 'Low'], 
                    label='Priority Level',
                    value='Normal'
                ).props('outlined').classes('w-full mb-3')
                
                ui.label('Preferred Transition Date').classes('text-sm font-medium text-gray-700 mb-1')
                transition_date = ui.date(value=date.today() + timedelta(days=30)
                ).props('outlined').classes('w-full mb-3')
                
            # Right column - Justification and Details
            with ui.column().classes('flex-1'):
                ui.label('Request Details').classes('font-semibold text-lg text-blue-600 mb-3')
                
                justification = ui.textarea('Justification for Transfer', 
                    placeholder='Please provide detailed reasons for requesting this transfer...'
                ).props('outlined rows=4').classes('w-full mb-3')
                
                skills_input = ui.input('Relevant Skills', 
                    placeholder='List skills relevant to target department'
                ).props('outlined').classes('w-full mb-3')
                
                experience_input = ui.textarea('Relevant Experience', 
                    placeholder='Describe experience relevant to the requested role...'
                ).props('outlined rows=3').classes('w-full mb-3')
        
        # Smart score preview
        with ui.row().classes('w-full p-4 bg-gray-50 rounded-lg mb-4'):
            ui.label('🎯 Smart Score Preview').classes('font-semibold text-gray-700')
            score_preview = ui.label('Score will be calculated automatically').classes('text-blue-600 ml-4')
        
        # Action buttons
        with ui.row().classes('w-full justify-end gap-2 mt-6'):
            ui.button('Save as Draft', on_click=save_as_draft).props('flat color=gray')
            ui.button('Submit Request', on_click=lambda: submit_transfer_request(
                current_dept.value, requested_dept.value, priority.value,
                transition_date.value, justification.value, skills_input.value,
                experience_input.value, score_preview
            )).props('color=primary')

def create_recommendations_section():
    """Create AI-powered department recommendations"""
    with ui.card().classes('w-full p-6'):
        ui.label('🤖 AI-Powered Department Recommendations').classes('text-xl font-semibold mb-4')
        
        # Mock employee profile
        employee_profile = {"skills": ["communication", "analysis"], "interests": ["technology", "leadership"]}
        recommendations = transfer_manager.get_department_recommendations(employee_profile)
        
        ui.label('Based on your skills, performance, and career goals:').classes('text-gray-600 mb-4')
        
        with ui.grid(columns=2).classes('gap-4 w-full'):
            for i, rec in enumerate(recommendations[:6]):  # Show top 6 recommendations
                compatibility_color = 'bg-green-100 border-green-500' if rec['compatibility_score'] >= 80 else 'bg-yellow-100 border-yellow-500' if rec['compatibility_score'] >= 60 else 'bg-red-100 border-red-500'
                
                with ui.card().classes(f'p-4 border-l-4 {compatibility_color}'):
                    with ui.row().classes('items-center justify-between mb-2'):
                        ui.label(rec['department']).classes('font-semibold text-lg')
                        ui.chip(f"{rec['compatibility_score']}%", color='blue').props('dense')
                    
                    with ui.column().classes('gap-2'):
                        with ui.row().classes('justify-between text-sm'):
                            ui.label('Capacity:').classes('text-gray-600')
                            ui.label(rec['capacity_status']).classes('font-medium')
                        
                        with ui.row().classes('justify-between text-sm'):
                            ui.label('Growth Potential:').classes('text-gray-600')
                            ui.label(rec['growth_potential']).classes('font-medium')
                        
                        ui.button(f'Request Transfer to {rec["code"]}', 
                            on_click=lambda dept=rec['department']: quick_request_transfer(dept)
                        ).props('size=sm color=primary').classes('w-full mt-2')

def create_my_requests_section():
    """Create my requests overview"""
    with ui.card().classes('w-full p-6'):
        ui.label('My Transfer Requests').classes('text-xl font-semibold mb-4')
        
        # Mock current employee requests
        my_requests = transfer_manager.get_my_requests("EMP-123")
        
        if not my_requests:
            with ui.column().classes('items-center py-8'):
                ui.icon('folder_open').classes('text-gray-400 text-6xl mb-4')
                ui.label('No transfer requests found').classes('text-gray-500 text-lg')
                ui.label('Submit your first transfer request using the form above').classes('text-gray-400 text-sm')
        else:
            # Requests table
            with ui.row().classes('w-full p-4 bg-gray-50 rounded-t-lg font-semibold'):
                ui.label('Request ID').classes('w-32')
                ui.label('Department').classes('flex-1')
                ui.label('Date').classes('w-32')
                ui.label('Status').classes('w-32')
                ui.label('Smart Score').classes('w-24 text-center')
                ui.label('Actions').classes('w-32 text-center')
            
            for request in my_requests:
                with ui.row().classes('w-full p-4 border-b border-gray-200 hover:bg-gray-50'):
                    ui.label(request['id']).classes('w-32 font-mono text-sm')
                    
                    with ui.column().classes('flex-1'):
                        ui.label(f'{request["current_department"]} → {request["requested_department"]}').classes('font-medium')
                        ui.label(request['justification'][:50] + '...').classes('text-sm text-gray-500')
                    
                    ui.label(request['request_date']).classes('w-32 text-sm')
                    
                    status_color = 'green' if 'Approved' in request['status'] else 'yellow' if 'Pending' in request['status'] else 'red'
                    ui.chip(request['status'], color=status_color).props('dense').classes('w-32')
                    
                    ui.label(f"{request['smart_score']}%").classes('w-24 text-center font-bold')
                    
                    with ui.row().classes('w-32 justify-center gap-1'):
                        ui.button(icon='visibility', on_click=lambda r=request: view_request_details(r)).props('size=sm flat color=blue')
                        if request['status'] == 'Pending Review':
                            ui.button(icon='edit', on_click=lambda r=request: edit_request(r)).props('size=sm flat color=green')

def create_guidelines_section():
    """Create transfer guidelines and policies"""
    with ui.card().classes('w-full p-6'):
        ui.label('📋 Transfer Request Guidelines').classes('text-xl font-semibold mb-4')
        
        guidelines = [
            {
                "title": "Eligibility Requirements",
                "items": [
                    "Minimum 6 months tenure in current position",
                    "Performance rating of 70% or above",
                    "No pending disciplinary actions",
                    "Maximum one pending transfer request"
                ]
            },
            {
                "title": "Process Timeline",
                "items": [
                    "Manager Review: 5 business days",
                    "HR Review: 7 business days", 
                    "Receiving Department Review: 3 business days",
                    "Final Approval: 2 business days"
                ]
            },
            {
                "title": "Smart Score Factors",
                "items": [
                    "Department capacity and fit",
                    "Skills alignment and growth potential",
                    "Business justification strength",
                    "Proposed transition timeline"
                ]
            }
        ]
        
        for guideline in guidelines:
            with ui.expansion(guideline["title"], icon='info').classes('w-full mb-2'):
                with ui.column().classes('p-4'):
                    for item in guideline["items"]:
                        with ui.row().classes('items-center gap-2 mb-2'):
                            ui.icon('check_circle').classes('text-green-500 text-sm')
                            ui.label(item).classes('text-gray-700')

# Action functions
async def submit_transfer_request(current_dept, requested_dept, priority, transition_date, justification, skills, experience, score_preview):
    """Submit transfer request with validation"""
    if not requested_dept or not justification:
        ui.notify('Please fill in all required fields', color='negative')
        return
    
    request_data = {
        "employee_id": "EMP-123",  # Mock current user
        "employee_name": "Current User",
        "current_department": current_dept,
        "requested_department": requested_dept,
        "priority": priority,
        "estimated_transition_date": transition_date.strftime("%Y-%m-%d"),
        "justification": justification,
        "skills": skills,
        "experience": experience
    }
    
    success, request_id, smart_score = transfer_manager.create_transfer_request(request_data)
    
    if success:
        score_preview.text = f'Smart Score: {smart_score}%'
        ui.notify(f'Transfer request submitted successfully! Request ID: {request_id}', color='positive')
        
        # Show success dialog with next steps
        with ui.dialog() as dialog, ui.card().classes('w-96 p-6'):
            ui.label('🎉 Request Submitted Successfully!').classes('text-xl font-semibold mb-4 text-green-600')
            ui.label(f'Request ID: {request_id}').classes('font-mono text-sm mb-2')
            ui.label(f'Smart Score: {smart_score}%').classes('text-blue-600 font-semibold mb-4')
            
            ui.label('Next Steps:').classes('font-semibold mb-2')
            ui.label('1. Your manager will review within 5 business days').classes('text-sm mb-1')
            ui.label('2. HR will conduct secondary review').classes('text-sm mb-1')
            ui.label('3. You will be notified of the decision').classes('text-sm mb-4')
            
            ui.button('OK', on_click=dialog.close).props('color=primary')
        
        dialog.open()
    else:
        ui.notify('Error submitting request. Please try again.', color='negative')

async def save_as_draft():
    """Save request as draft"""
    ui.notify('Request saved as draft', color='info')

async def quick_request_transfer(department):
    """Quick transfer request from recommendations"""
    ui.notify(f'Quick request for {department} - Feature coming soon!', color='info')

async def show_my_requests():
    """Show my requests dialog"""
    ui.notify('Navigating to My Requests tab', color='info')

async def show_transfer_history():
    """Show transfer history"""
    ui.notify('Transfer history - Feature coming soon!', color='info')

async def view_request_details(request):
    """View detailed request information"""
    with ui.dialog() as dialog, ui.card().classes('w-[600px] p-6'):
        ui.label(f'Transfer Request Details - {request["id"]}').classes('text-xl font-semibold mb-4')
        
        with ui.grid(columns=2).classes('gap-4 w-full'):
            # Left column
            with ui.column().classes('gap-3'):
                ui.label('Request Information').classes('font-semibold text-blue-600')
                ui.label(f'Employee: {request["employee_name"]}').classes('text-sm')
                ui.label(f'Current Dept: {request["current_department"]}').classes('text-sm')
                ui.label(f'Requested Dept: {request["requested_department"]}').classes('text-sm')
                ui.label(f'Priority: {request["priority"]}').classes('text-sm')
                ui.label(f'Transition Date: {request["estimated_transition_date"]}').classes('text-sm')
            
            # Right column
            with ui.column().classes('gap-3'):
                ui.label('Status Information').classes('font-semibold text-green-600')
                ui.label(f'Status: {request["status"]}').classes('text-sm')
                ui.label(f'Current Stage: {request["approval_stage"]}').classes('text-sm')
                ui.label(f'Smart Score: {request["smart_score"]}%').classes('text-sm')
                ui.label(f'Request Date: {request["request_date"]}').classes('text-sm')
        
        ui.label('Justification:').classes('font-semibold text-purple-600 mt-4')
        ui.label(request["justification"]).classes('text-sm bg-gray-50 p-3 rounded')
        
        with ui.row().classes('w-full justify-end mt-6'):
            ui.button('Close', on_click=dialog.close).props('flat')
    
    dialog.open()

def create_smart_transfer_dashboard():
    """Create modern transfer dashboard with AI insights"""
    with ui.column().classes('w-full space-y-6'):
        # Quick stats cards
        with ui.row().classes('w-full gap-4 mb-6'):
            with ui.card().classes('p-6 flex-1 bg-gradient-to-br from-indigo-50 to-purple-100'):
                ui.html('''
                    <div class="text-center">
                        <i class="material-icons text-4xl text-indigo-600 mb-2">trending_up</i>
                        <div class="text-2xl font-bold text-indigo-800">89%</div>
                        <div class="text-indigo-700">Success Rate</div>
                    </div>
                ''', sanitize=False)
            
            with ui.card().classes('p-6 flex-1 bg-gradient-to-br from-purple-50 to-pink-100'):
                ui.html('''
                    <div class="text-center">
                        <i class="material-icons text-4xl text-purple-600 mb-2">groups</i>
                        <div class="text-2xl font-bold text-purple-800">12</div>
                        <div class="text-purple-700">Open Positions</div>
                    </div>
                ''', sanitize=False)
            
            with ui.card().classes('p-6 flex-1 bg-gradient-to-br from-pink-50 to-rose-100'):
                ui.html('''
                    <div class="text-center">
                        <i class="material-icons text-4xl text-pink-600 mb-2">psychology</i>
                        <div class="text-2xl font-bold text-pink-800">96%</div>
                        <div class="text-pink-700">Match Accuracy</div>
                    </div>
                ''', sanitize=False)

async def show_career_pathways():
    """Show AI-powered career pathways dialog"""
    with ui.dialog() as dialog, ui.card().classes('w-4xl max-w-4xl p-8'):
        ui.html('''
            <div class="flex items-center gap-3 mb-6">
                <div class="bg-indigo-500 text-white p-3 rounded-full">
                    <i class="material-icons text-2xl">trending_up</i>
                </div>
                <div>
                    <h2 class="text-2xl font-bold text-indigo-800">AI Career Pathways</h2>
                    <p class="text-indigo-600">Intelligent career progression recommendations based on skills and opportunities</p>
                </div>
            </div>
        ''', sanitize=False)
        
        with ui.row().classes('w-full gap-6'):
            # Left column - Career map
            with ui.column().classes('flex-1'):
                ui.label('🚀 Recommended Career Paths').classes('text-xl font-semibold text-gray-800 mb-4')
                with ui.card().classes('p-4'):
                    ui.html('''
                        <div class="space-y-4">
                            <div class="p-4 bg-indigo-50 rounded-lg border-l-4 border-indigo-500">
                                <div class="font-semibold text-indigo-800">Senior Developer (IT)</div>
                                <div class="text-indigo-700">Match: 94% • Timeline: 6 months</div>
                                <div class="text-sm text-indigo-600 mt-1">Skills gap: Advanced Python, Cloud Architecture</div>
                            </div>
                            <div class="p-4 bg-purple-50 rounded-lg border-l-4 border-purple-500">
                                <div class="font-semibold text-purple-800">Product Manager (Marketing)</div>
                                <div class="text-purple-700">Match: 87% • Timeline: 12 months</div>
                                <div class="text-sm text-purple-600 mt-1">Skills gap: Market Analysis, Product Strategy</div>
                            </div>
                            <div class="p-4 bg-pink-50 rounded-lg border-l-4 border-pink-500">
                                <div class="font-semibold text-pink-800">Team Lead (Operations)</div>
                                <div class="text-pink-700">Match: 82% • Timeline: 8 months</div>
                                <div class="text-sm text-pink-600 mt-1">Skills gap: Leadership Training, Process Management</div>
                            </div>
                        </div>
                    ''', sanitize=False)
            
            # Right column - Skills development
            with ui.column().classes('flex-1'):
                ui.label('📚 Skill Development Plan').classes('text-xl font-semibold text-gray-800 mb-4')
                with ui.card().classes('p-4'):
                    ui.html('''
                        <div class="space-y-3">
                            <div class="flex justify-between items-center">
                                <span class="font-medium">Technical Skills</span>
                                <span class="text-indigo-600 font-bold">78%</span>
                            </div>
                            <div class="w-full bg-gray-200 rounded-full h-2">
                                <div class="bg-indigo-500 h-2 rounded-full" style="width: 78%"></div>
                            </div>
                            
                            <div class="flex justify-between items-center">
                                <span class="font-medium">Leadership</span>
                                <span class="text-purple-600 font-bold">65%</span>
                            </div>
                            <div class="w-full bg-gray-200 rounded-full h-2">
                                <div class="bg-purple-500 h-2 rounded-full" style="width: 65%"></div>
                            </div>
                            
                            <div class="flex justify-between items-center">
                                <span class="font-medium">Communication</span>
                                <span class="text-pink-600 font-bold">92%</span>
                            </div>
                            <div class="w-full bg-gray-200 rounded-full h-2">
                                <div class="bg-pink-500 h-2 rounded-full" style="width: 92%"></div>
                            </div>
                        </div>
                    ''', sanitize=False)
        
        ui.button('Close', on_click=dialog.close).props('flat color=indigo').classes('mt-6')
    dialog.open()

async def show_transfer_analytics():
    """Show transfer analytics dashboard"""
    ui.notify('Advanced transfer analytics dashboard - Feature coming soon!', color='info')

async def edit_request(request):
    """Edit existing request"""
    ui.notify(f'Edit request {request["id"]} - Feature coming soon!', color='info')

# Integration APIs
def get_transfer_requests_for_approval(manager_id):
    """API for managers to get requests requiring approval"""
    return [req for req in transfer_manager.transfer_requests if req["approval_stage"] == "Manager Review"]

def approve_transfer_request(request_id, approver_id, comments=""):
    """API for approving transfer requests"""
    return transfer_manager.update_request_status(request_id, "Approved", "HR Review")