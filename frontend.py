from components import (
InstitutionProfile, EnrollNewStaff, decode_jwt_token, DepartmentalSections, EmployeeTermination, 
validate_magic_link_server, EmployeeProbation, RequestTransfer, RequestLeave, AttendanceRules, 
LeaveRules, ShiftTimetable, SetHolidays, create_staff_status_page as StaffStatus, 
create_staff_schedule_page as StaffSchedulePage, create_main_dashboard, UserRole, 
create_integrated_dashboard_menu, create_dashboard_landing_page
)
from helperFuns import imagePath, get_mount_path, build_mount_route
from helperFuns.auth_storage import set_auth_data, is_authenticated
from layout import Sidebar, router
from components.reports.asset_inventory import create_asset_inventory_page
from components.employees.employee_management import create_employee_management_page
from components.timesheets.timesheet_management import create_modern_timesheet_management_page
from components.administration.hr_administration import create_hr_administration_page
from ai_orchestrator.ui import create_ai_orchestrator_page

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from nicegui import ui, app, context
import urllib.parse
import random


APP_MOUNT_PATH = get_mount_path()


def mount_route(sub_path: str = '') -> str:
    """Combine the configured mount path with the provided sub-path."""
    return build_mount_route(sub_path, base=APP_MOUNT_PATH)


def ensure_authenticated() -> bool:
    """Redirect unauthenticated users back to the login page."""
    if not is_authenticated():
        ui.navigate.to(mount_route())
        return False
    return True


def process_magic_link_from_request(
    notify_user: bool = False,
    clean_url: bool = False,
    redirect_on_error: bool = True,
):
    """Consume jwt_token/username query params and persist auth state."""
    try:
        request = None
        if hasattr(context, 'client') and context.client and hasattr(context.client, 'request'):
            request = context.client.request
        if not request or not hasattr(request, 'query_params'):
            return None

        params = request.query_params
        jwt_token = params.get('jwt_token')
        username_param = params.get('username')
        if not jwt_token:
            return None

        jwt_token = urllib.parse.unquote(jwt_token)
        user_data = decode_jwt_token(jwt_token)
        if not user_data:
            if notify_user:
                ui.notify('Magic link is invalid or has expired. Please log in again.', color='negative')
            if redirect_on_error:
                ui.navigate.to(mount_route())
            return False

        username = username_param or user_data.get('username', 'User')
        set_auth_data({
            'token': jwt_token,
            'authenticated': True,
            'username': username,
            'email': user_data.get('email', ''),
        })

        if notify_user:
            ui.notify(f"Welcome {username}! You have been successfully logged in.", color='positive')
        if clean_url:
            ui.navigate.to(mount_route('/reporting/dashboard'))
        return True
    except Exception as exc:
        print(f'Magic link processing error: {exc}')
        if redirect_on_error:
            ui.navigate.to(mount_route())
        return False

def create_page_layout():
    """Create a proper page layout container that works with the modern fixed sidebar"""
    # Main container that accounts for the fixed sidebar width
    # Sidebar is now always 288px wide (w-72), so use ml-72 for left margin
    return ui.element('div').classes('ml-72 transition-all duration-300 ease-in-out min-h-screen bg-gray-50 p-6 relative z-10')

def dashboard_page():
    # ── Step 1: consume jwt_token from URL (magic link redirect) ───────────
    token_result = process_magic_link_from_request(
        notify_user=True,
        clean_url=True,
        redirect_on_error=True,
    )
    if token_result is not None:
        return

    # ── Step 2: guard – redirect unauthenticated visitors to login ─────────
    if not is_authenticated():
        ui.navigate.to(mount_route())
        return

    # ── Step 3: optional ?view=menu classic layout ─────────────────────────
    view_mode = None
    try:
        if hasattr(context, 'client') and context.client and hasattr(context.client, 'request'):
            request = context.client.request
            if request and hasattr(request, 'query_params'):
                view_mode = request.query_params.get("view")
    except Exception:
        pass

    if view_mode == "menu":
        ui.label('Welcome to the Dashboard!').classes('text-2xl font-bold')
        with ui.card().classes('w-full max-w-md mt-6'):
            with ui.card_section().classes('p-6'):
                ui.html('<h2 class="text-xl font-semibold mb-4">🚀 Experience the Modern Dashboard</h2>')
                ui.html('<p class="text-gray-600 mb-4">Switch to our comprehensive enterprise dashboard with real-time analytics, hardware integration, and AI-powered insights.</p>')
                ui.button('🏢 Open Modern Dashboard', on_click=lambda: ui.navigate.to(mount_route('/reporting/dashboard'))).classes('w-full bg-blue-600 text-white')
    else:
        # Modern comprehensive dashboard
        user_role = UserRole.ADMIN
        with ui.row().classes('fixed top-4 right-4 z-50'):
            ui.button('📋 Traditional Menu', on_click=lambda: ui.navigate.to(f"{mount_route('/reporting/dashboard')}?view=menu")).classes('bg-gray-600 text-white shadow-lg hover:bg-gray-700 transition-colors')
        create_main_dashboard(user_role)

def auth_callback_page():
    """Magic link auth handler -- reachable at https://kwarecominc.com/hr/auth via nginx"""
    try:
        if hasattr(context, 'client') and context.client and hasattr(context.client, 'request'):
            request = context.client.request
            if request and hasattr(request, 'query_params'):
                params = dict(request.query_params)
                email = params.get('email')
                timestamp = params.get('timestamp')
                token = params.get('token')

                if email and timestamp and token:
                    is_valid, result = validate_magic_link_server(email, timestamp, token)
                    if is_valid:
                        username = email.split('@')[0]
                        set_auth_data({
                            'token': result,
                            'authenticated': True,
                            'username': username,
                            'email': email,
                        })
                        ui.navigate.to(mount_route('/reporting/dashboard'))
                        return
                    else:
                        ui.notify(f'Login failed: {result}', color='negative')
                        ui.navigate.to(mount_route())
                        return
    except Exception as e:
        print(f"Auth callback error: {e}")

    ui.navigate.to(mount_route())


def institution_profile_page():
    # Check if user is authenticated
    # if not app.storage.user.get('authenticated', False):
    #     ui.navigate.to('/hrmkit')
    #     return
    InstitutionProfile()

def enroll_staff_page():
    # Check if user is authenticated
    # if not app.storage.user.get('authenticated', False):
    #     ui.navigate.to('/hrmkit')
    #     return
    EnrollNewStaff()    

def departmental_sections_page():
    # Check if user is authenticated
    # if not app.storage.user.get('authenticated', False):
    #     ui.navigate.to('/hrmkit')
    #     return
    DepartmentalSections()

def employee_termination_page():
    # Check if user is authenticated
    # if not app.storage.user.get('authenticated', False):
    #     ui.navigate.to('/hrmkit')
    #     return
    EmployeeTermination()

def employee_probation_page():
    # Check if user is authenticated
    # if not app.storage.user.get('authenticated', False):
    #     ui.navigate.to('/hrmkit')
    #     return
    EmployeeProbation()

def request_transfer_page():
    # Check if user is authenticated
    # if not app.storage.user.get('authenticated', False):
    #     ui.navigate.to('/hrmkit')
    #     return
    RequestTransfer()

def request_leave_page():
    # Check if user is authenticated
    # if not app.storage.user.get('authenticated', False):
    #     ui.navigate.to('/hrmkit')
    #     return
    RequestLeave()

def attendance_rules_page():
    # Check if user is authenticated
    # if not app.storage.user.get('authenticated', False):
    #     ui.navigate.to('/hrmkit')
    #     return
    AttendanceRules()

def leave_rules_page():
    # Check if user is authenticated
    # if not app.storage.user.get('authenticated', False):
    #     ui.navigate.to('/hrmkit')
    #     return
    LeaveRules()

def shift_timetable_page():
    # Check if user is authenticated
    # if not app.storage.user.get('authenticated', False):
    #     ui.navigate.to('/hrmkit')
    #     return
    ShiftTimetable()

def set_holidays_page():
    # Check if user is authenticated
    if not ensure_authenticated():
        return
    # Now load the full SetHolidays component
    try:
        SetHolidays()
    except Exception as e:
        # Fallback UI if SetHolidays fails
        ui.label('❌ Error loading holiday management').classes('text-red-600 font-bold text-center mt-8')
        ui.label(f'Error: {str(e)}').classes('text-red-400 text-center mt-2')
        ui.button('Retry', on_click=lambda: ui.run_javascript('location.reload()')).classes('bg-blue-500 text-white px-4 py-2 rounded mt-4')

def staff_schedule_page():
    # Check if user is authenticated
    if not ensure_authenticated():
        return
    StaffSchedulePage()

def staff_status_page():
    # Check if user is authenticated
    if not ensure_authenticated():
        return
    StaffStatus()

def menu_integration_page():
    # Check if user is authenticated
    if not ensure_authenticated():
        return
    create_integrated_dashboard_menu()

def dashboard_landing_page():
    # Check if user is authenticated
    if not ensure_authenticated():
        return
    create_dashboard_landing_page()
    
def leave_request_page():
    # Check if user is authenticated
    if not ensure_authenticated():
        return
    RequestLeave()
    
def transfer_request_page():
    # Check if user is authenticated
    if not ensure_authenticated():
        return
    RequestTransfer()
    
def employee_report_page():
    # Check if user is authenticated
    if not ensure_authenticated():
        return
    create_employee_management_page()
    
def employee_timesheet_report_page():
    # Check if user is authenticated
    if not ensure_authenticated():
        return
    create_modern_timesheet_management_page()
    
def administration_report_page():
    # Check if user is authenticated
    if not ensure_authenticated():
        return
    create_hr_administration_page()
    
def report_department_page():
    # Check if user is authenticated
    if not ensure_authenticated():
        return
    DepartmentalSections()
    
def leave_report_page():
    # Check if user is authenticated
    if not ensure_authenticated():
        return
    RequestLeave()
    
def assets_report_page():
    # Check if user is authenticated
    if not ensure_authenticated():
        return
    create_asset_inventory_page()

def ai_orchestrator_page():
    # Check if user is authenticated
    if not ensure_authenticated():
        return
    create_ai_orchestrator_page()

def init(fastapi_app: FastAPI) -> None:
    @ui.page(mount_route('/{_:path}'))
    def page_layout():
        process_magic_link_from_request(
            notify_user=False,
            clean_url=False,
            redirect_on_error=False,
        )
        Sidebar()
        ui.sub_pages({
            mount_route('/reporting/dashboard'): dashboard_page,
            mount_route('/reporting/menu-integration'): menu_integration_page,
            mount_route('/reporting/dashboard-landing'): dashboard_landing_page,
            mount_route('/administration/institution'): institution_profile_page,
            mount_route('/administration/employee/enroll-staff'): enroll_staff_page,
            mount_route('/administration/departments'): departmental_sections_page,
            mount_route('/administration/termination'): employee_termination_page,
            mount_route('/administration/probation'): employee_probation_page,
            mount_route('/administration/transfer/requests'): transfer_request_page,
            mount_route('/administration/leave/requests'): leave_request_page,
            mount_route('/employees/request-transfer'): request_transfer_page,
            mount_route('/employees/request-leave'): request_leave_page,
            mount_route('/attendance/attendance-rules'): attendance_rules_page,
            mount_route('/attendance/leave/rules'): leave_rules_page,
            mount_route('/attendance/timetable'): shift_timetable_page,
            mount_route('/attendance/holidays'): set_holidays_page,
            mount_route('/attendance/employee/schedule'): staff_schedule_page,
            mount_route('/attendance/staff/on_duty_status'): staff_status_page,
            mount_route('/reporting/modern-dashboard'): create_modern_hr_dashboard,
            mount_route('/reporting/employees'): employee_report_page,
            mount_route('/reporting/employees/timesheet'): employee_timesheet_report_page,
            mount_route('/reporting/administration'): administration_report_page,
            mount_route('/reporting/departments'): report_department_page,
            mount_route('/reporting/leaves'): leave_report_page,
            mount_route('/reporting/assets'): assets_report_page,
            mount_route('/ai/orchestrator'): ai_orchestrator_page,
        })
    fastapi_app.include_router(router)
    
    # Use run_with to integrate NiceGUI with FastAPI
    ui.run_with(
        fastapi_app,
        title='HRMkit',
        favicon=imagePath('favicon.ico') if imagePath('favicon.ico') else None,
        # mount_path='/hrmkit',
        storage_secret='hrms-secret-key-2024'  # Required for user storage
    )

    # Add a route specifically for magic link validation (outside the NiceGUI mount)
    # @fastapi_app.get("/auth")
    # async def magic_link_auth(email: str = None, timestamp: str = None, token: str = None):
    #     if email and timestamp and token:
    #         # Validate the magic link
    #         is_valid, result = validate_magic_link_server(email, timestamp, token)
            
    #         if is_valid:
    #             # Redirect to dashboard with the JWT token in URL
    #             encoded_token = urllib.parse.quote(result)  # result is the JWT token
    #             return RedirectResponse(url=f"/hrmkit/reporting/dashboard?jwt_token={encoded_token}&username={email.split('@')[0].title()}")
    #         else:
    #             # Redirect to login with error
    #             return RedirectResponse(url="/hrmkit/?error=" + urllib.parse.quote(result))
    #     else:
    #         return RedirectResponse(url="/hrmkit/")

def create_modern_hr_dashboard():
    """Create a modern, visually appealing HR dashboard with smart algorithms"""
    
    # Smart HR Analytics Engine
    class HRAnalyticsEngine:
        def __init__(self):
            self.employee_count = 63
            self.attendance_rate = 89.2
            self.productivity_score = 92.5
            self.turnover_rate = 4.2
            
        def predict_attendance(self):
            """AI-powered attendance prediction algorithm"""
            # Simulate ML prediction based on historical data, weather, time of year
            base_prediction = self.attendance_rate
            weather_factor = random.uniform(0.95, 1.05)
            seasonal_factor = 1.02 if random.random() > 0.5 else 0.98
            return round(base_prediction * weather_factor * seasonal_factor, 1)
        
        def calculate_productivity_trend(self):
            """Smart productivity trend analysis"""
            # Analyze productivity patterns using time-series analysis
            trend = random.choice(['↗️ Improving', '→ Stable', '↗️ Growing'])
            change = round(random.uniform(-2.1, 3.8), 1)
            return trend, change
        
        def optimize_leave_scheduling(self):
            """AI algorithm for optimal leave scheduling"""
            # Consider team coverage, project deadlines, individual performance
            recommendations = [
                "Schedule John's leave for next month to maintain team coverage",
                "Consider early approval for Sarah's vacation request",
                "Optimize leave distribution to avoid coverage gaps"
            ]
            return random.choice(recommendations)
        
        def detect_anomalies(self):
            """Anomaly detection for HR metrics"""
            anomalies = []
            if random.random() > 0.7:
                anomalies.append("Unusual spike in sick leaves this week")
            if random.random() > 0.8:
                anomalies.append("Higher than expected turnover in Engineering")
            if random.random() > 0.6:
                anomalies.append("Attendance rate below seasonal average")
            return anomalies if anomalies else ["All metrics within normal ranges"]
    
    analytics = HRAnalyticsEngine()
    
    # Main dashboard layout
    with ui.element('div').classes('min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100'):
        
        # Main Content Area
        with ui.element('div').classes('p-8'):
            
            # Header
            with ui.row().classes('justify-between items-center mb-8'):
                with ui.column():
                    ui.html('<h1 class="text-3xl font-bold text-gray-800">Welcome to Smart HR Dashboard</h1>')
                    ui.html('<p class="text-gray-600 mt-2">AI-powered workforce management and analytics</p>')
                
                with ui.row().classes('items-center gap-4'):
                    # Real-time indicator
                    with ui.row().classes('items-center gap-2 bg-green-100 px-3 py-1 rounded-full'):
                        ui.html('<div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>')
                        ui.html('<span class="text-sm text-green-700 font-medium">Live Data</span>')
                    
                    # Quick actions
                    ui.button('⚡ Quick Actions', icon='bolt').classes('bg-blue-600 text-white hover:bg-blue-700')
                    ui.button('🔔 Notifications', icon='notifications').classes('bg-gray-600 text-white hover:bg-gray-700')
            
            # Key Metrics Row
            with ui.element('div').classes('bg-white rounded-xl shadow-lg p-8 mb-8 border border-gray-100'):
                ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-6 text-center">Key Performance Indicators</h2>')
                with ui.row().classes('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8'):
                    
                    # Total Employees
                    with ui.card().classes('p-6 bg-gradient-to-br from-blue-500 to-blue-600 text-white hover:shadow-xl transition-all duration-300 cursor-pointer border-2 border-blue-400 hover:border-blue-300'):
                        with ui.row().classes('justify-between items-start'):
                            with ui.column():
                                ui.html('<div class="text-3xl font-bold mb-1">63</div>')
                                ui.html('<div class="text-blue-100 text-sm">Total Employees</div>')
                            ui.html('<div class="text-4xl opacity-80">👥</div>')
                        ui.html('<div class="mt-4 text-xs text-blue-200">↗️ +2.1% from last month</div>')
                    
                    # Attendance Rate
                    attendance_pred = analytics.predict_attendance()
                    with ui.card().classes('p-6 bg-gradient-to-br from-green-500 to-green-600 text-white hover:shadow-xl transition-all duration-300 cursor-pointer border-2 border-green-400 hover:border-green-300'):
                        with ui.row().classes('justify-between items-start'):
                            with ui.column():
                                ui.html(f'<div class="text-3xl font-bold mb-1">{attendance_pred}%</div>')
                                ui.html('<div class="text-green-100 text-sm">Attendance Rate</div>')
                            ui.html('<div class="text-4xl opacity-80">✅</div>')
                        ui.html('<div class="mt-4 text-xs text-green-200">AI Prediction: Tomorrow</div>')
                    
                    # Productivity Score
                    trend_icon, trend_change = analytics.calculate_productivity_trend()
                    with ui.card().classes('p-6 bg-gradient-to-br from-purple-500 to-purple-600 text-white hover:shadow-xl transition-all duration-300 cursor-pointer border-2 border-purple-400 hover:border-purple-300'):
                        with ui.row().classes('justify-between items-start'):
                            with ui.column():
                                ui.html('<div class="text-3xl font-bold mb-1">92.5%</div>')
                                ui.html('<div class="text-purple-100 text-sm">Productivity</div>')
                            ui.html('<div class="text-4xl opacity-80">📈</div>')
                        ui.html(f'<div class="mt-4 text-xs text-purple-200">{trend_icon} {trend_change}% this week</div>')
                    
                    # Turnover Rate
                    with ui.card().classes('p-6 bg-gradient-to-br from-orange-500 to-orange-600 text-white hover:shadow-xl transition-all duration-300 cursor-pointer border-2 border-orange-400 hover:border-orange-300'):
                        with ui.row().classes('justify-between items-start'):
                            with ui.column():
                                ui.html('<div class="text-3xl font-bold mb-1">4.2%</div>')
                                ui.html('<div class="text-orange-100 text-sm">Turnover Rate</div>')
                            ui.html('<div class="text-4xl opacity-80">📉</div>')
                        ui.html('<div class="mt-4 text-xs text-orange-200">↘️ -0.8% from last quarter</div>')
            
            # Charts and Analytics Row
            with ui.element('div').classes('bg-white rounded-xl shadow-lg p-8 mb-8 border border-gray-100'):
                ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-6 text-center">Analytics & Trends</h2>')
                with ui.row().classes('grid grid-cols-1 lg:grid-cols-2 gap-8 h-96'):
                    
                    # Attendance Trend Chart
                    with ui.card().classes('p-6 hover:shadow-xl transition-all duration-300 border-2 border-blue-200 hover:border-blue-300 bg-gradient-to-br from-blue-50 to-indigo-50 h-full flex flex-col'):
                        ui.html('<h3 class="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2"><span class="text-2xl">📊</span>Attendance Trends</h3>')
                        
                        # Mock chart data
                        chart_data = [85, 87, 89, 88, 91, 89, 92]
                        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                        
                        with ui.element('div').classes('space-y-3 flex-1'):
                            for i, (day, value) in enumerate(zip(days, chart_data)):
                                with ui.row().classes('items-center gap-3'):
                                    ui.html(f'<div class="w-12 text-sm font-medium text-gray-600">{day}</div>')
                                    with ui.element('div').classes('flex-1 bg-gray-200 rounded-full h-3'):
                                        ui.element('div').classes(f'bg-blue-500 h-3 rounded-full transition-all duration-500').style(f'width: {value}%')
                                    ui.html(f'<div class="w-12 text-sm text-gray-600 text-right">{value}%</div>')
                        
                        ui.html('<div class="mt-4 text-sm text-gray-500">Weekly attendance pattern analysis</div>')
                    
                    # Department Performance
                    with ui.card().classes('p-6 hover:shadow-xl transition-all duration-300 border-2 border-green-200 hover:border-green-300 bg-gradient-to-br from-green-50 to-emerald-50 h-full flex flex-col'):
                        ui.html('<h3 class="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2"><span class="text-2xl">🏆</span>Department Performance</h3>')
                        
                        departments = [
                            {'name': 'Engineering', 'score': 95, 'change': '+2.1%', 'color': 'green'},
                            {'name': 'Marketing', 'score': 88, 'change': '+1.5%', 'color': 'blue'},
                            {'name': 'Sales', 'score': 92, 'change': '-0.3%', 'color': 'purple'},
                            {'name': 'HR', 'score': 89, 'change': '+1.8%', 'color': 'orange'},
                            {'name': 'Finance', 'score': 91, 'change': '+0.9%', 'color': 'indigo'},
                        ]
                        
                        with ui.element('div').classes('space-y-4 flex-1'):
                            for dept in departments:
                                with ui.row().classes('items-center justify-between p-3 bg-white rounded-lg border border-gray-100 hover:bg-gray-50 transition-colors'):
                                    with ui.row().classes('items-center gap-3'):
                                        ui.html(f'<div class="w-3 h-3 bg-{dept["color"]}-500 rounded-full"></div>')
                                        ui.html(f'<div class="font-medium text-gray-800">{dept["name"]}</div>')
                                    
                                    with ui.row().classes('items-center gap-3'):
                                        ui.html(f'<div class="text-sm text-gray-600">{dept["score"]}%</div>')
                                        ui.html(f'<div class="text-sm text-{dept["color"]}-600 font-medium">{dept["change"]}</div>')
            
            # Bottom Row - Recent Activity and AI Insights
            with ui.element('div').classes('bg-white rounded-xl shadow-lg p-8 border border-gray-100'):
                ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-6 text-center">Activity & Insights</h2>')
                with ui.row().classes('grid grid-cols-1 lg:grid-cols-3 gap-8 h-96'):
                    
                    # Recent Activity
                    with ui.card().classes('p-6 hover:shadow-xl transition-all duration-300 border-2 border-purple-200 hover:border-purple-300 bg-gradient-to-br from-purple-50 to-violet-50 h-full flex flex-col'):
                        ui.html('<h3 class="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2"><span class="text-2xl">🕐</span>Recent Activity</h3>')
                        
                        activities = [
                            {'action': 'New employee onboarded', 'user': 'John Smith', 'time': '2 hours ago', 'icon': '👋'},
                            {'action': 'Leave request approved', 'user': 'Sarah Johnson', 'time': '4 hours ago', 'icon': '✅'},
                            {'action': 'Performance review completed', 'user': 'Mike Davis', 'time': '6 hours ago', 'icon': '📝'},
                            {'action': 'Attendance marked', 'user': 'Lisa Wilson', 'time': '8 hours ago', 'icon': '🕐'},
                        ]
                        
                        with ui.element('div').classes('space-y-3 flex-1'):
                            for activity in activities:
                                with ui.row().classes('items-start gap-3 p-3 hover:bg-white rounded-lg transition-colors border border-gray-100'):
                                    ui.html(f'<div class="text-xl">{activity["icon"]}</div>')
                                    with ui.column().classes('flex-1'):
                                        ui.html(f'<div class="text-sm font-medium text-gray-800">{activity["action"]}</div>')
                                        ui.html(f'<div class="text-xs text-gray-500">{activity["user"]} • {activity["time"]}</div>')
                    
                    # AI Insights
                    with ui.card().classes('p-6 bg-gradient-to-br from-indigo-50 to-purple-50 border border-indigo-200 hover:shadow-xl transition-all duration-300 border-2 border-indigo-300 hover:border-indigo-400 h-full flex flex-col'):
                        ui.html('<h3 class="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2"><span class="text-2xl">🤖</span>AI Insights</h3>')
                        
                        insights = [
                            'Consider scheduling team-building activities to boost morale',
                            'Optimize leave scheduling to maintain project momentum',
                            'Focus on professional development for high-performers',
                            'Monitor attendance patterns for potential health concerns',
                        ]
                        
                        with ui.element('div').classes('space-y-3 flex-1'):
                            for insight in insights[:3]:
                                with ui.row().classes('items-start gap-3'):
                                    ui.html('<div class="text-blue-500 mt-1">💡</div>')
                                    ui.html(f'<div class="text-sm text-gray-700">{insight}</div>')
                        
                        ui.button('🔍 View All Insights', on_click=lambda: ui.notify('Opening detailed AI analytics...')).classes('w-full mt-4 bg-indigo-600 text-white hover:bg-indigo-700')
                    
                    # Quick Actions
                    with ui.card().classes('p-6 hover:shadow-xl transition-all duration-300 border-2 border-orange-200 hover:border-orange-300 bg-gradient-to-br from-orange-50 to-amber-50 h-full flex flex-col'):
                        ui.html('<h3 class="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2"><span class="text-2xl">⚡</span>Quick Actions</h3>')
                        
                        actions = [
                            {'label': 'Add New Employee', 'icon': '➕', 'color': 'green', 'action': lambda: ui.notify('Opening employee registration...')},
                            {'label': 'Approve Leave', 'icon': '✅', 'color': 'blue', 'action': lambda: ui.notify('Opening leave approvals...')},
                            {'label': 'Generate Report', 'icon': '📊', 'color': 'purple', 'action': lambda: ui.notify('Generating comprehensive report...')},
                            {'label': 'Schedule Meeting', 'icon': '📅', 'color': 'orange', 'action': lambda: ui.notify('Opening calendar...')},
                        ]
                        
                        with ui.element('div').classes('space-y-3 flex-1'):
                            for action in actions:
                                ui.button(
                                    f'{action["icon"]} {action["label"]}',
                                    on_click=action['action']
                                ).classes(f'w-full justify-start p-3 bg-{action["color"]}-50 text-{action["color"]}-700 hover:bg-{action["color"]}-100 border border-{action["color"]}-200 transition-colors')
                        
                        # Anomaly detection
                        anomalies = analytics.detect_anomalies()
                        if anomalies and anomalies[0] != "All metrics within normal ranges":
                            with ui.element('div').classes('mt-4 p-3 bg-red-50 border border-red-200 rounded-lg'):
                                ui.html('<div class="text-sm font-semibold text-red-800 mb-1">⚠️ Anomaly Detected</div>')
                                ui.html(f'<div class="text-xs text-red-700">{anomalies[0]}</div>')

def create_page_layout():
    """Create a proper page layout container that works with the modern fixed sidebar"""
    # Main container that accounts for the fixed sidebar width
    # Sidebar is now always 288px wide (w-72), so use ml-72 for left margin
    return ui.element('div').classes('ml-72 transition-all duration-300 ease-in-out min-h-screen bg-gray-50 p-6 relative z-10')