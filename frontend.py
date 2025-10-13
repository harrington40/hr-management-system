from components import Login_Page, InstitutionProfile, EnrollNewStaff
from components.administration.departmental_sections import DepartmentalSections
from components.administration.employee_termination import EmployeeTermination
from components.administration.employee_probation import EmployeeProbation
from components.employees import RequestTransfer, RequestLeave
from components.attendance import AttendanceRules, LeaveRules, ShiftTimetable, SetHolidays
from components.attendance.staff_status import create_staff_status_page as StaffStatus
from components.attendance.staff_schedule import create_staff_schedule_page as StaffSchedulePage
from helperFuns import imagePath
from layout import Sidebar

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from nicegui import ui
import urllib.parse

def init(fastapi_app: FastAPI) -> None:
    @ui.page('/')
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
       
       Sidebar()
       ui.label('Welcome to the Dashboard!').classes('text-2xl font-bold')
       # Add more dashboard components here

    @ui.page('/administration/institution')
    def institution_profile_page():
       from nicegui import app
       
       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return
       
       Sidebar()
       InstitutionProfile()

    @ui.page('/administration/enroll-staff')
    def enroll_staff_page():
       from nicegui import app
       
       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return
       
       Sidebar()
       EnrollNewStaff()

    @ui.page('/administration/departments')
    def departmental_sections_page():
       from nicegui import app
       
       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return
       
       Sidebar()
       DepartmentalSections()

    @ui.page('/administration/termination')
    def employee_termination_page():
       from nicegui import app
       
       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return
       
       Sidebar()
       EmployeeTermination()

    @ui.page('/administration/probation')
    def employee_probation_page():
       from nicegui import app
       
       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return
       
       Sidebar()
       EmployeeProbation()

    @ui.page('/employees/request-transfer')
    def request_transfer_page():
       from nicegui import app
       
       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return
       
       Sidebar()
       RequestTransfer()

    @ui.page('/employees/request-leave')
    def request_leave_page():
       from nicegui import app
       
       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return
       
       Sidebar()
       RequestLeave()

    @ui.page('/attendance/attendance')
    def attendance_rules_page():
       from nicegui import app
       
       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return
       
       Sidebar()
       AttendanceRules()

    @ui.page('/attendance/leave/rules')
    def leave_rules_page():
       from nicegui import app
       
       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return
       
       Sidebar()
       LeaveRules()

    @ui.page('/attendance/timetable')
    def shift_timetable_page():
       from nicegui import app
       
       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return
       
       Sidebar()
       ShiftTimetable()

    @ui.page('/attendance/holidays')
    def set_holidays_page():
       from nicegui import app
       
       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return
       
       Sidebar()
       
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
       
       Sidebar()
       StaffSchedulePage()

    @ui.page('/attendance/staff_status')
    def staff_status_page():
       from nicegui import app
       
       # Check if user is authenticated
       if not app.storage.user.get('authenticated', False):
           ui.navigate.to('/')
           return
       
       Sidebar()
       StaffStatus()

    # Add a route specifically for magic link validation (outside the NiceGUI mount)
    @fastapi_app.get("/auth")
    async def magic_link_auth(email: str = None, timestamp: str = None, token: str = None):
        if email and timestamp and token:
            # Validate the magic link
            from components.authencation.authHelper import validate_magic_link_server
            is_valid, result = validate_magic_link_server(email, timestamp, token)
            
            if is_valid:
                # Redirect to dashboard with the JWT token in URL
                import urllib.parse
                encoded_token = urllib.parse.quote(result)  # result is the JWT token
                return RedirectResponse(url=f"/hrmkit/dashboard?jwt_token={encoded_token}&username={email.split('@')[0].title()}")
            else:
                # Redirect to login with error
                return RedirectResponse(url="/hrmkit/?error=" + urllib.parse.quote(result))
        else:
            return RedirectResponse(url="/hrmkit/")

    ui.run_with(
        fastapi_app,
        # port=8000,
        mount_path='/hrmkit',  # NOTE this can be omitted if you want the paths passed to @ui.page to be at the root
        storage_secret='pick your private secret here',  # NOTE setting a secret is optional but allows for persistent storage per user
        title= 'HRMkit',
        favicon= imagePath('favicon.ico'),
        # protocol='https',
        # host='127.0.0.1',
        # prod_js=False
        # dark=True
    )