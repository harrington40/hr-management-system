from nicegui import ui, APIRouter, context, app as ngapp
from components import Login_Page
from helperFuns import readEnv, get_mount_path, build_mount_route
from helperFuns.auth_storage import set_auth_data
from components.attendance import SetHolidays, LeaveRules, AttendanceRules, ShiftTimetable
from components.attendance.staff_schedule import create_modern_staff_schedule_page
from components.attendance.staff_status import create_staff_status_page

from components.reports.dashboard.menu_integration import create_dashboard_landing_page, create_integrated_dashboard_menu
from components.reports.dashboard.main_dashboard import create_main_dashboard
from components.reports.dashboard.dashboard_main import create_comprehensive_dashboard
from components.reports.asset_inventory import create_asset_inventory_page
from components.employees.employee_management import create_employee_management_page
from components.timesheets.timesheet_management import create_modern_timesheet_management_page
from components.administration.departmental_sections import DepartmentalSections
from components.administration.hr_administration import create_hr_administration_page
from components.administration.institution_profile import InstitutionProfile
from components.administration.enroll_staff import EnrollNewStaff
from components.administration.employee_probation import EmployeeProbation
from components.administration.employee_termination import EmployeeTermination
from components.administration.admin_management import create_administration_page
from components.administration.license_pricing import create_license_pricing_page
from components.administration.connectivity import create_connectivity_page
from components.employees.request_leave import RequestLeave
from components.employees.request_transfer import RequestTransfer

from layout.sidebar import Sidebar
from layout.license_guard import require_license

APP_MOUNT_PATH = get_mount_path()

router = APIRouter(prefix=APP_MOUNT_PATH)

# Main dashboard page
@router.page('/')
def show():
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

# Attendance - Set Holidays
@router.page('/attendance/holidays')
def show_holidays():
    """Display holidays management page"""
    Sidebar()
    if require_license('Holiday & Vacation Management'): return
    SetHolidays()

# Attendance - Staff Schedule
@router.page('/attendance/employee/schedule')
def show_staff_schedule():
    """Display staff schedule management page"""
    Sidebar()
    if require_license('Staff Schedule'): return
    create_modern_staff_schedule_page()

# Attendance - Leave Rules
@router.page('/attendance/leave/rules')
def show_leave_rules():
    """Display leave rules management page"""
    Sidebar()
    if require_license('Leave Rules'): return
    LeaveRules()

# Attendance - Shift Timetable
@router.page('/attendance/timetable')
def show_shift_timetable():
    """Display shift timetable management page"""
    Sidebar()
    if require_license('Shift Timetable'): return
    ShiftTimetable()

# Attendance - Attendance Rules
@router.page('/attendance/attendance-rules')
def show_attendance_rules():
    """Display attendance rules management page"""
    Sidebar()
    if require_license('Attendance Rules'): return
    AttendanceRules()

# Attendance - On Duty Status
@router.page('/attendance/staff/on_duty_status')
def show_on_duty_status():
    """Display staff on-duty status management page"""
    Sidebar()
    if require_license('Staff On-Duty Status'): return
    create_staff_status_page()

# Reporting - Dashboard Landing
@router.page('/reporting/dashboard-landing')
def show_dashboard_landing():
    """Display dashboard landing page"""
    Sidebar()
    if require_license('Dashboard'): return
    create_dashboard_landing_page()

# Reporting - Modern Dashboard
@router.page('/reporting/modern-dashboard')
def show_modern_dashboard():
    """Display modern dashboard page"""
    Sidebar()
    if require_license('Modern Dashboard'): return
    create_main_dashboard()

# Reporting - Menu Integration
@router.page('/reporting/menu-integration')
def show_menu_integration():
    """Display integrated dashboard menu page"""
    Sidebar()
    if require_license('Menu Integration'): return
    create_integrated_dashboard_menu()

# Reporting - Comprehensive Dashboard
@router.page('/reporting/dashboard')
def show_dashboard():
    print('[show_dashboard] invoked')
    """Display comprehensive dashboard page.
    Handles ?jwt_token= from magic link redirect via ui.timer (socket context).
    """
    jwt_token = None
    email = ''
    try:
        params = dict(context.client.request.query_params)
        jwt_token = params.get('jwt_token')
        email = params.get('email', '')
    except Exception:
        pass

    if jwt_token:
        from components.authencation.authHelper import decode_jwt_token

        user_data = decode_jwt_token(jwt_token)
        if user_data:
            set_auth_data({
                'token': jwt_token,
                'authenticated': True,
                'username': user_data.get('username', email.split('@')[0]),
                'email': user_data.get('email', email),
            })
            clean_url = build_mount_route('/reporting/dashboard', base=APP_MOUNT_PATH)
            print(f'[show_dashboard] replacing URL with {clean_url}')
            try:
                ui.run_javascript(f"window.history.replaceState(null, '', '{clean_url}');")
            except Exception as exc:
                print(f'[show_dashboard] history replace failed: {exc}')
            Sidebar()
            create_dashboard_landing_page()
            return

    Sidebar()
    if require_license('HR Dashboard'): return
    create_dashboard_landing_page()

# Reporting - Employees
@router.page('/reporting/employees')
def show_employees():
    """Display employees management page"""
    Sidebar()
    if require_license('Employee Management'): return
    create_employee_management_page()

# Reporting - Employees Timesheet
@router.page('/reporting/employees/timesheet')
def show_employees_timesheet():
    """Display employees timesheet management page"""
    Sidebar()
    if require_license('Employee Timesheet'): return
    create_modern_timesheet_management_page()

# Reporting - Departments
@router.page('/reporting/departments')
def show_departments():
    """Display departments management page"""
    Sidebar()
    if require_license('Departments'): return
    DepartmentalSections()

# Reporting - Administration
@router.page('/reporting/administration')
def show_administration():
    """Display HR administration page"""
    Sidebar()
    if require_license('HR Administration'): return
    create_hr_administration_page()

# Reporting - Assets
@router.page('/reporting/assets')
def show_assets():
    """Display asset inventory page"""
    Sidebar()
    if require_license('Asset Inventory'): return
    create_asset_inventory_page()

# Reporting - Leaves
@router.page('/reporting/leaves')
def show_reporting_leaves():
    """Display leave requests / leave management page under reporting"""
    Sidebar()
    if require_license('Leave Reports'): return
    RequestLeave()


# Employees - Request Leave
@router.page('/employees/request-leave')
def show_request_leave():
    """Display request leave management page"""
    Sidebar()
    if require_license('Request Leave'): return
    RequestLeave()

# Employees - Request Transfer
@router.page('/employees/request-transfer')
def show_request_transfer():
    """Display request transfer management page"""
    Sidebar()
    if require_license('Request Transfer'): return
    RequestTransfer()

# Administration - Institution Profile
@router.page('/administration/institution')
def show_institution():
    """Display institution profile management page"""
    Sidebar()
    if require_license('Institution Profile'): return
    InstitutionProfile()

# Administration - Departments
@router.page('/administration/departments')
def show_admin_departments():
    """Display departments management page"""
    Sidebar()
    if require_license('Departments'): return
    DepartmentalSections()

# Administration - Enroll Staff
@router.page('/administration/employee/enroll-staff')
def show_enroll_staff():
    """Display enroll new staff page"""
    Sidebar()
    if require_license('Enroll Staff'): return
    EnrollNewStaff()

# Administration - Probation
@router.page('/administration/probation')
def show_probation():
    """Display employee probation management page"""
    Sidebar()
    if require_license('Employee Probation'): return
    EmployeeProbation()

# Administration - Termination
@router.page('/administration/termination')
def show_termination():
    """Display employee termination management page"""
    Sidebar()
    if require_license('Employee Termination'): return
    EmployeeTermination()

# Administration - Leave Requests
@router.page('/administration/leave/requests')
def show_leave_requests():
    """Display leave requests management page"""
    Sidebar()
    if require_license('Leave Requests'): return
    RequestLeave()

# Administration - Transfer Requests
@router.page('/administration/transfer/requests')
def show_transfer_requests():
    """Display transfer requests management page"""
    Sidebar()
    if require_license('Transfer Requests'): return
    RequestTransfer()


# Billing - License & Pricing
@router.page('/billing/license-pricing')
def show_license_pricing():
    """Display license and pricing management page"""
    Sidebar()
    create_license_pricing_page()


# Administration - Connectivity Hub (Bluetooth + QR Code)
@router.page('/administration/connectivity')
def show_connectivity():
    """Display Bluetooth scanner and QR code generator"""
    Sidebar()
    if require_license('Connectivity Hub'): return
    create_connectivity_page()


# NOTE: Magic link auth is handled by the FastAPI /hrmkit/auth HTTP endpoint in main.py.
# The FastAPI endpoint is registered first and takes priority; this NiceGUI page is
# a fallback that should never be reached in normal operation.
@router.page('/auth')
def show_auth_fallback():
    """Fallback: auth should be handled by the FastAPI /hrmkit/auth endpoint."""
    ui.navigate.to(APP_MOUNT_PATH)


# Generic catch-all route for undefined pages
@router.page('/{path:path}')
def catch_all(path: str):
    """Catch-all route for undefined sub-pages"""
    Sidebar()
    with ui.column():
        ui.label(f"🔄 Page Not Yet Implemented: /{path}").classes('text-xl font-bold text-red-500')
        ui.label("This page route is defined but not yet implemented.").classes('text-gray-500')
        
        # Display the path that was requested
        ui.code(f"Route: {build_mount_route(path, base=APP_MOUNT_PATH)}").classes('bg-gray-100 p-4')
        
        # Back button
        with ui.row():
            ui.button('Back to Dashboard', on_click=lambda: ui.navigate(APP_MOUNT_PATH)).props('flat')
