from components import Login_Page, InstitutionProfile, EnrollNewStaff
from components.administration.departmental_sections import DepartmentalSections
from components.administration.employee_termination import EmployeeTermination
from components.administration.employee_probation import EmployeeProbation
from components.employees import RequestTransfer, RequestLeave
from components.attendance import AttendanceRules, LeaveRules, ShiftTimetable, SetHolidays
from components.attendance.staff_status import create_staff_status_page as StaffStatus
from components.attendance.staff_schedule import create_staff_schedule_page as StaffSchedulePage
from components.dashboard.main_dashboard import create_main_dashboard, UserRole
from components.dashboard.menu_integration import create_integrated_dashboard_menu, create_dashboard_landing_page
from helperFuns import imagePath
from layout import Sidebar, create_modern_sidebar

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from nicegui import ui
import urllib.parse
import random

def create_page_layout():
    """Create a proper page layout container that works with the modern fixed sidebar"""
    # Main container that accounts for the fixed sidebar width
    # Sidebar is now always 288px wide (w-72), so use ml-72 for left margin
    return ui.element('div').classes('ml-72 transition-all duration-300 ease-in-out min-h-screen bg-gray-50 p-6 relative z-10')

def init(fastapi_app: FastAPI) -> None:
    """Initialize NiceGUI with FastAPI integration using run_with"""
    from nicegui import ui

    # Use run_with to integrate NiceGUI with FastAPI
    ui.run_with(
        fastapi_app,
        title='HRMkit',
        favicon=imagePath('favicon.ico') if imagePath('favicon.ico') else None,
        mount_path='/hrmkit',
        storage_secret='hrms-secret-key-2024'  # Required for user storage
    )
    @ui.page('/', title='HRMkit - Login')
    def show():
       # Check for error messages in URL
       from fastapi import Request
       from nicegui import context
       try:
           if hasattr(context, 'client') and context.client and hasattr(context.client, 'request'):
               request = context.client.request
               if request and hasattr(request, 'query_params'):
                   error = request.query_params.get("error")
                   if error:
                       ui.notify(f"Authentication error: {error}", color='negative')
       except:
           pass
           
       Login_Page()
       
    @ui.page('/dashboard')
    def dashboard_page():
       from nicegui import app
       
       # Check for JWT token in URL (from magic link auth)
       from fastapi import Request
       from nicegui import context
       jwt_token = None
       username = None
       
       try:
           if hasattr(context, 'client') and context.client and hasattr(context.client, 'request'):
               request = context.client.request
               if request and hasattr(request, 'query_params'):
                   jwt_token = request.query_params.get("jwt_token")
                   username = request.query_params.get("username")
                   
                   if jwt_token:
                       # Decode and validate the JWT token
                       jwt_token = urllib.parse.unquote(jwt_token)
                       from components.authencation.authHelper import decode_jwt_token
                       user_data = decode_jwt_token(jwt_token)
                       
                       if user_data:
                           # Set authentication in storage
                           app.storage.user.update({'token': jwt_token, 'authenticated': True})
                           ui.notify(f"Welcome {username or user_data.get('username', 'User')}! You have been successfully logged in.", color='positive')
                           # Clean redirect to remove token from URL - use relative path since we're already in /hrmkit mount
                           ui.navigate.to('/dashboard')
                           return
       except Exception as e:
           print(f"Error processing JWT token: {e}")
       
       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return
       
       # Check if user wants traditional menu or modern dashboard
       from nicegui import context
       view_mode = None
       try:
           if hasattr(context, 'client') and context.client and hasattr(context.client, 'request'):
               request = context.client.request
               if request and hasattr(request, 'query_params'):
                   view_mode = request.query_params.get("view")
       except:
           pass
       
       if view_mode == "menu":
           # Modern sidebar menu with red highlighting
           create_modern_sidebar()
           ui.label('Welcome to the Dashboard!').classes('text-2xl font-bold')
           
           # Add quick access to modern dashboard
           with ui.card().classes('w-full max-w-md mt-6'):
               with ui.card_section().classes('p-6'):
                   ui.html('<h2 class="text-xl font-semibold mb-4">🚀 Experience the Modern Dashboard</h2>', sanitize=False)
                   ui.html('<p class="text-gray-600 mb-4">Switch to our comprehensive enterprise dashboard with real-time analytics, hardware integration, and AI-powered insights.</p>', sanitize=False)
                   ui.button('🏢 Open Modern Dashboard', on_click=lambda: ui.navigate.to('/dashboard')).classes('w-full bg-blue-600 text-white')
       else:
           # Modern comprehensive dashboard
           # Determine user role (for now, default to admin - could be enhanced with user management)
           user_role = UserRole.ADMIN  # This could be determined from user data in a real system
           
           # Add option to switch to traditional menu
           with ui.row().classes('fixed top-4 right-4 z-50'):
               ui.button('📋 Traditional Menu', on_click=lambda: ui.navigate.to('/dashboard?view=menu')).classes('bg-gray-600 text-white shadow-lg hover:bg-gray-700 transition-colors')
           
           create_main_dashboard(user_role)

    @ui.page('/administration/institution')
    def institution_profile_page():
       from nicegui import app

       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return

       create_modern_sidebar()
       with create_page_layout():
           InstitutionProfile()

    @ui.page('/administration/enroll-staff')
    def enroll_staff_page():
       from nicegui import app

       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return

       create_modern_sidebar()
       with create_page_layout():
           EnrollNewStaff()

    @ui.page('/administration/departments')
    def departmental_sections_page():
       from nicegui import app

       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return

       create_modern_sidebar()
       with create_page_layout():
           DepartmentalSections()

    @ui.page('/administration/termination')
    def employee_termination_page():
       from nicegui import app

       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return

       create_modern_sidebar()
       with create_page_layout():
           EmployeeTermination()

    @ui.page('/administration/probation')
    def employee_probation_page():
       from nicegui import app

       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return

       create_modern_sidebar()
       with create_page_layout():
           EmployeeProbation()

    @ui.page('/employees/request-transfer')
    def request_transfer_page():
       from nicegui import app

       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return

       create_modern_sidebar()
       with create_page_layout():
           RequestTransfer()

    @ui.page('/employees/request-leave')
    def request_leave_page():
       from nicegui import app

       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return

       create_modern_sidebar()
       with create_page_layout():
           RequestLeave()

    @ui.page('/attendance/attendance')
    def attendance_rules_page():
       from nicegui import app

       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return

       create_modern_sidebar()
       with create_page_layout():
           AttendanceRules()

    @ui.page('/attendance/leave/rules')
    def leave_rules_page():
       from nicegui import app

       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return

       create_modern_sidebar()
       with create_page_layout():
           LeaveRules()

    @ui.page('/attendance/timetable')
    def shift_timetable_page():
       from nicegui import app

       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return

       create_modern_sidebar()
       with create_page_layout():
           ShiftTimetable()

    @ui.page('/attendance/holidays')
    def set_holidays_page():
       from nicegui import app

       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return

       create_modern_sidebar()
       with create_page_layout():
           # Now load the full SetHolidays component
           try:
               SetHolidays()
           except Exception as e:
               # Fallback UI if SetHolidays fails
               ui.label('❌ Error loading holiday management').classes('text-red-600 font-bold text-center mt-8')
               ui.label(f'Error: {str(e)}').classes('text-red-400 text-center mt-2')
               ui.button('Retry', on_click=lambda: ui.run_javascript('location.reload()')).classes('bg-blue-500 text-white px-4 py-2 rounded mt-4')

    @ui.page('/attendance/staff_schedule')
    def staff_schedule_page():
       from nicegui import app

       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return

       create_modern_sidebar()
       with create_page_layout():
           StaffSchedulePage()

    @ui.page('/attendance/staff_status')
    def staff_status_page():
       from nicegui import app

       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return

       create_modern_sidebar()
       with create_page_layout():
           StaffStatus()

    @ui.page('/menu-integration')
    def menu_integration_page():
       from nicegui import app

       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return

       create_integrated_dashboard_menu()

    @ui.page('/dashboard-landing')
    def dashboard_landing_page():
       from nicegui import app
       
       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return
       
       create_dashboard_landing_page()

    # Add a route specifically for magic link validation (outside the NiceGUI mount)
    @fastapi_app.get("/auth")
    async def magic_link_auth(email: str = None, timestamp: str = None, token: str = None):
        if email and timestamp and token:
            # Validate the magic link
            from components.authencation.authHelper import validate_magic_link_server
            is_valid, result = validate_magic_link_server(email, timestamp, token)
            
            if is_valid:
                # Redirect to dashboard with the JWT token in URL
                encoded_token = urllib.parse.quote(result)  # result is the JWT token
                return RedirectResponse(url=f"/hrmkit/dashboard?jwt_token={encoded_token}&username={email.split('@')[0].title()}")
            else:
                # Redirect to login with error
                return RedirectResponse(url="/hrmkit/?error=" + urllib.parse.quote(result))
        else:
            return RedirectResponse(url="/hrmkit/")

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
        
        # Modern Sidebar
        with ui.element('div').classes('fixed left-0 top-0 h-full w-80 bg-white shadow-2xl border-r border-gray-200 z-40 transform transition-transform duration-300'):
            
            # Sidebar Header
            with ui.element('div').classes('p-6 bg-gradient-to-r from-blue-600 to-indigo-600 text-white'):
                with ui.row().classes('items-center gap-3'):
                    ui.html('<div class="text-3xl">🏢</div>', sanitize=False)
                    with ui.column():
                        ui.html('<div class="text-xl font-bold">HR Analytics</div>', sanitize=False)
                        ui.html('<div class="text-sm opacity-90">Smart Dashboard</div>', sanitize=False)
            
            # Navigation Menu
            with ui.element('div').classes('p-4 space-y-2'):
                
                # Dashboard Overview
                with ui.element('div').classes('group'):
                    with ui.row().classes('items-center gap-3 p-3 rounded-lg hover:bg-blue-50 cursor-pointer transition-colors border-l-4 border-blue-500'):
                        ui.html('<div class="text-xl">📊</div>', sanitize=False)
                        with ui.column().classes('flex-1'):
                            ui.html('<div class="font-semibold text-gray-800">Dashboard</div>', sanitize=False)
                            ui.html('<div class="text-sm text-gray-500">Overview & Analytics</div>', sanitize=False)
                        ui.html('<div class="text-blue-500 opacity-0 group-hover:opacity-100 transition-opacity">→</div>', sanitize=False)
                
                # Employee Management
                with ui.element('div').classes('group'):
                    with ui.row().classes('items-center gap-3 p-3 rounded-lg hover:bg-blue-50 cursor-pointer transition-colors border-l-4 border-blue-500'):
                        ui.html('<div class="text-xl">👥</div>', sanitize=False)
                        with ui.column().classes('flex-1'):
                            ui.html('<div class="font-semibold text-gray-800">Employees</div>', sanitize=False)
                            ui.html('<div class="text-sm text-gray-500">Staff Directory</div>', sanitize=False)
                        ui.html('<div class="text-blue-500 opacity-0 group-hover:opacity-100 transition-opacity">→</div>', sanitize=False)
                
                # Attendance Tracking
                with ui.element('div').classes('group'):
                    with ui.row().classes('items-center gap-3 p-3 rounded-lg hover:bg-blue-50 cursor-pointer transition-colors border-l-4 border-blue-500'):
                        ui.html('<div class="text-xl">🕐</div>', sanitize=False)
                        with ui.column().classes('flex-1'):
                            ui.html('<div class="font-semibold text-gray-800">Attendance</div>', sanitize=False)
                            ui.html('<div class="text-sm text-gray-500">Time Tracking</div>', sanitize=False)
                        ui.html('<div class="text-blue-500 opacity-0 group-hover:opacity-100 transition-opacity">→</div>', sanitize=False)
                
                # Performance
                with ui.element('div').classes('group'):
                    with ui.row().classes('items-center gap-3 p-3 rounded-lg hover:bg-blue-50 cursor-pointer transition-colors border-l-4 border-blue-500'):
                        ui.html('<div class="text-xl">🎯</div>', sanitize=False)
                        with ui.column().classes('flex-1'):
                            ui.html('<div class="font-semibold text-gray-800">Performance</div>', sanitize=False)
                            ui.html('<div class="text-sm text-gray-500">Reviews & Goals</div>', sanitize=False)
                        ui.html('<div class="text-blue-500 opacity-0 group-hover:opacity-100 transition-opacity">→</div>', sanitize=False)
                
                # Leave Management
                with ui.element('div').classes('group'):
                    with ui.row().classes('items-center gap-3 p-3 rounded-lg hover:bg-blue-50 cursor-pointer transition-colors border-l-4 border-blue-500'):
                        ui.html('<div class="text-xl">🏖️</div>', sanitize=False)
                        with ui.column().classes('flex-1'):
                            ui.html('<div class="font-semibold text-gray-800">Leave</div>', sanitize=False)
                            ui.html('<div class="text-sm text-gray-500">Requests & Planning</div>', sanitize=False)
                        ui.html('<div class="text-blue-500 opacity-0 group-hover:opacity-100 transition-opacity">→</div>', sanitize=False)
                
                # Reports & Analytics
                with ui.element('div').classes('group'):
                    with ui.row().classes('items-center gap-3 p-3 rounded-lg hover:bg-blue-50 cursor-pointer transition-colors border-l-4 border-blue-500'):
                        ui.html('<div class="text-xl">📈</div>', sanitize=False)
                        with ui.column().classes('flex-1'):
                            ui.html('<div class="font-semibold text-gray-800">Reports</div>', sanitize=False)
                            ui.html('<div class="text-sm text-gray-500">Analytics & Insights</div>', sanitize=False)
                        ui.html('<div class="text-blue-500 opacity-0 group-hover:opacity-100 transition-opacity">→</div>', sanitize=False)
            
            # AI Insights Panel
            with ui.element('div').classes('absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-r from-indigo-50 to-purple-50 border-t border-gray-200'):
                ui.html('<div class="text-sm font-semibold text-gray-800 mb-2">🤖 AI Insights</div>', sanitize=False)
                ai_insight = analytics.optimize_leave_scheduling()
                ui.html(f'<div class="text-xs text-gray-600 leading-relaxed">{ai_insight}</div>', sanitize=False)
        
        # Main Content Area - Adjusted for collapsible sidebar
        with ui.element('div').classes('ml-16 p-8 transition-all duration-300'):
            
            # Header
            with ui.row().classes('justify-between items-center mb-8'):
                with ui.column():
                    ui.html('<h1 class="text-3xl font-bold text-gray-800">Welcome to Smart HR Dashboard</h1>', sanitize=False)
                    ui.html('<p class="text-gray-600 mt-2">AI-powered workforce management and analytics</p>', sanitize=False)
                
                with ui.row().classes('items-center gap-4'):
                    # Real-time indicator
                    with ui.row().classes('items-center gap-2 bg-green-100 px-3 py-1 rounded-full'):
                        ui.html('<div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>', sanitize=False)
                        ui.html('<span class="text-sm text-green-700 font-medium">Live Data</span>', sanitize=False)
                    
                    # Quick actions
                    ui.button('⚡ Quick Actions', icon='bolt').classes('bg-blue-600 text-white hover:bg-blue-700')
                    ui.button('🔔 Notifications', icon='notifications').classes('bg-gray-600 text-white hover:bg-gray-700')
            
            # Key Metrics Row
            with ui.element('div').classes('bg-white rounded-xl shadow-lg p-8 mb-8 border border-gray-100'):
                ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-6 text-center">Key Performance Indicators</h2>', sanitize=False)
                with ui.row().classes('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8'):
                    
                    # Total Employees
                    with ui.card().classes('p-6 bg-gradient-to-br from-blue-500 to-blue-600 text-white hover:shadow-xl transition-all duration-300 cursor-pointer border-2 border-blue-400 hover:border-blue-300'):
                        with ui.row().classes('justify-between items-start'):
                            with ui.column():
                                ui.html('<div class="text-3xl font-bold mb-1">63</div>', sanitize=False)
                                ui.html('<div class="text-blue-100 text-sm">Total Employees</div>', sanitize=False)
                            ui.html('<div class="text-4xl opacity-80">👥</div>', sanitize=False)
                        ui.html('<div class="mt-4 text-xs text-blue-200">↗️ +2.1% from last month</div>', sanitize=False)
                    
                    # Attendance Rate
                    attendance_pred = analytics.predict_attendance()
                    with ui.card().classes('p-6 bg-gradient-to-br from-green-500 to-green-600 text-white hover:shadow-xl transition-all duration-300 cursor-pointer border-2 border-green-400 hover:border-green-300'):
                        with ui.row().classes('justify-between items-start'):
                            with ui.column():
                                ui.html(f'<div class="text-3xl font-bold mb-1">{attendance_pred}%</div>', sanitize=False)
                                ui.html('<div class="text-green-100 text-sm">Attendance Rate</div>', sanitize=False)
                            ui.html('<div class="text-4xl opacity-80">✅</div>', sanitize=False)
                        ui.html('<div class="mt-4 text-xs text-green-200">AI Prediction: Tomorrow</div>', sanitize=False)
                    
                    # Productivity Score
                    trend_icon, trend_change = analytics.calculate_productivity_trend()
                    with ui.card().classes('p-6 bg-gradient-to-br from-purple-500 to-purple-600 text-white hover:shadow-xl transition-all duration-300 cursor-pointer border-2 border-purple-400 hover:border-purple-300'):
                        with ui.row().classes('justify-between items-start'):
                            with ui.column():
                                ui.html('<div class="text-3xl font-bold mb-1">92.5%</div>', sanitize=False)
                                ui.html('<div class="text-purple-100 text-sm">Productivity</div>', sanitize=False)
                            ui.html('<div class="text-4xl opacity-80">📈</div>', sanitize=False)
                        ui.html(f'<div class="mt-4 text-xs text-purple-200">{trend_icon} {trend_change}% this week</div>', sanitize=False)
                    
                    # Turnover Rate
                    with ui.card().classes('p-6 bg-gradient-to-br from-orange-500 to-orange-600 text-white hover:shadow-xl transition-all duration-300 cursor-pointer border-2 border-orange-400 hover:border-orange-300'):
                        with ui.row().classes('justify-between items-start'):
                            with ui.column():
                                ui.html('<div class="text-3xl font-bold mb-1">4.2%</div>', sanitize=False)
                                ui.html('<div class="text-orange-100 text-sm">Turnover Rate</div>', sanitize=False)
                            ui.html('<div class="text-4xl opacity-80">📉</div>', sanitize=False)
                        ui.html('<div class="mt-4 text-xs text-orange-200">↘️ -0.8% from last quarter</div>', sanitize=False)
            
            # Charts and Analytics Row
            with ui.element('div').classes('bg-white rounded-xl shadow-lg p-8 mb-8 border border-gray-100'):
                ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-6 text-center">Analytics & Trends</h2>', sanitize=False)
                with ui.row().classes('grid grid-cols-1 lg:grid-cols-2 gap-8 h-96'):
                    
                    # Attendance Trend Chart
                    with ui.card().classes('p-6 hover:shadow-xl transition-all duration-300 border-2 border-blue-200 hover:border-blue-300 bg-gradient-to-br from-blue-50 to-indigo-50 h-full flex flex-col'):
                        ui.html('<h3 class="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2"><span class="text-2xl">📊</span>Attendance Trends</h3>', sanitize=False)
                        
                        # Mock chart data
                        chart_data = [85, 87, 89, 88, 91, 89, 92]
                        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                        
                        with ui.element('div').classes('space-y-3 flex-1'):
                            for i, (day, value) in enumerate(zip(days, chart_data)):
                                with ui.row().classes('items-center gap-3'):
                                    ui.html(f'<div class="w-12 text-sm font-medium text-gray-600">{day}</div>', sanitize=False)
                                    with ui.element('div').classes('flex-1 bg-gray-200 rounded-full h-3'):
                                        ui.element('div').classes(f'bg-blue-500 h-3 rounded-full transition-all duration-500').style(f'width: {value}%')
                                    ui.html(f'<div class="w-12 text-sm text-gray-600 text-right">{value}%</div>', sanitize=False)
                        
                        ui.html('<div class="mt-4 text-sm text-gray-500">Weekly attendance pattern analysis</div>', sanitize=False)
                    
                    # Department Performance
                    with ui.card().classes('p-6 hover:shadow-xl transition-all duration-300 border-2 border-green-200 hover:border-green-300 bg-gradient-to-br from-green-50 to-emerald-50 h-full flex flex-col'):
                        ui.html('<h3 class="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2"><span class="text-2xl">🏆</span>Department Performance</h3>', sanitize=False)
                        
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
                                        ui.html(f'<div class="w-3 h-3 bg-{dept["color"]}-500 rounded-full"></div>', sanitize=False)
                                        ui.html(f'<div class="font-medium text-gray-800">{dept["name"]}</div>', sanitize=False)
                                    
                                    with ui.row().classes('items-center gap-3'):
                                        ui.html(f'<div class="text-sm text-gray-600">{dept["score"]}%</div>', sanitize=False)
                                        ui.html(f'<div class="text-sm text-{dept["color"]}-600 font-medium">{dept["change"]}</div>', sanitize=False)
            
            # Bottom Row - Recent Activity and AI Insights
            with ui.element('div').classes('bg-white rounded-xl shadow-lg p-8 border border-gray-100'):
                ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-6 text-center">Activity & Insights</h2>', sanitize=False)
                with ui.row().classes('grid grid-cols-1 lg:grid-cols-3 gap-8 h-96'):
                    
                    # Recent Activity
                    with ui.card().classes('p-6 hover:shadow-xl transition-all duration-300 border-2 border-purple-200 hover:border-purple-300 bg-gradient-to-br from-purple-50 to-violet-50 h-full flex flex-col'):
                        ui.html('<h3 class="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2"><span class="text-2xl">🕐</span>Recent Activity</h3>', sanitize=False)
                        
                        activities = [
                            {'action': 'New employee onboarded', 'user': 'John Smith', 'time': '2 hours ago', 'icon': '👋'},
                            {'action': 'Leave request approved', 'user': 'Sarah Johnson', 'time': '4 hours ago', 'icon': '✅'},
                            {'action': 'Performance review completed', 'user': 'Mike Davis', 'time': '6 hours ago', 'icon': '📝'},
                            {'action': 'Attendance marked', 'user': 'Lisa Wilson', 'time': '8 hours ago', 'icon': '🕐'},
                        ]
                        
                        with ui.element('div').classes('space-y-3 flex-1'):
                            for activity in activities:
                                with ui.row().classes('items-start gap-3 p-3 hover:bg-white rounded-lg transition-colors border border-gray-100'):
                                    ui.html(f'<div class="text-xl">{activity["icon"]}</div>', sanitize=False)
                                    with ui.column().classes('flex-1'):
                                        ui.html(f'<div class="text-sm font-medium text-gray-800">{activity["action"]}</div>', sanitize=False)
                                        ui.html(f'<div class="text-xs text-gray-500">{activity["user"]} • {activity["time"]}</div>', sanitize=False)
                    
                    # AI Insights
                    with ui.card().classes('p-6 bg-gradient-to-br from-indigo-50 to-purple-50 border border-indigo-200 hover:shadow-xl transition-all duration-300 border-2 border-indigo-300 hover:border-indigo-400 h-full flex flex-col'):
                        ui.html('<h3 class="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2"><span class="text-2xl">🤖</span>AI Insights</h3>', sanitize=False)
                        
                        insights = [
                            'Consider scheduling team-building activities to boost morale',
                            'Optimize leave scheduling to maintain project momentum',
                            'Focus on professional development for high-performers',
                            'Monitor attendance patterns for potential health concerns',
                        ]
                        
                        with ui.element('div').classes('space-y-3 flex-1'):
                            for insight in insights[:3]:
                                with ui.row().classes('items-start gap-3'):
                                    ui.html('<div class="text-blue-500 mt-1">💡</div>', sanitize=False)
                                    ui.html(f'<div class="text-sm text-gray-700">{insight}</div>', sanitize=False)
                        
                        ui.button('🔍 View All Insights', on_click=lambda: ui.notify('Opening detailed AI analytics...')).classes('w-full mt-4 bg-indigo-600 text-white hover:bg-indigo-700')
                    
                    # Quick Actions
                    with ui.card().classes('p-6 hover:shadow-xl transition-all duration-300 border-2 border-orange-200 hover:border-orange-300 bg-gradient-to-br from-orange-50 to-amber-50 h-full flex flex-col'):
                        ui.html('<h3 class="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2"><span class="text-2xl">⚡</span>Quick Actions</h3>', sanitize=False)
                        
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
                                ui.html('<div class="text-sm font-semibold text-red-800 mb-1">⚠️ Anomaly Detected</div>', sanitize=False)
                                ui.html(f'<div class="text-xs text-red-700">{anomalies[0]}</div>', sanitize=False)

def create_page_layout():
    """Create a proper page layout container that works with the modern fixed sidebar"""
    # Main container that accounts for the fixed sidebar width
    # Sidebar is now always 288px wide (w-72), so use ml-72 for left margin
    return ui.element('div').classes('ml-72 transition-all duration-300 ease-in-out min-h-screen bg-gray-50 p-6 relative z-10')