"""
HR Dashboard Menu Integration
Links all HR modules with the comprehensive dashboard system
Provides seamless navigation between modern dashboard and traditional menu items
"""

from nicegui import ui
from helperFuns import build_mount_route


def _navigate(route: str) -> None:
    """Navigate to a mount-aware route"""
    ui.navigate.to(build_mount_route(route))

def create_integrated_dashboard_menu():
    """Create integrated menu that shows both dashboard and traditional menu options"""
    
    with ui.column().classes('w-full h-full bg-gradient-to-br from-blue-50 to-indigo-50 min-h-screen'):
        # Header
        with ui.row().classes('w-full p-6 bg-gradient-to-r from-blue-600 to-indigo-600 text-white'):
            with ui.row().classes('w-full justify-between items-center'):
                ui.html('<h1 class="text-3xl font-bold flex items-center gap-3"><span class="text-4xl">🏢</span>HR Management System</h1>')
                
                with ui.row().classes('gap-4'):
                    ui.button('🏠 Modern Dashboard', on_click=lambda: _navigate('/reporting/modern-dashboard')).classes('bg-white text-blue-600 hover:bg-gray-100')
                    ui.button('📋 Traditional Menu', on_click=lambda: _navigate('/reporting/menu-integration')).classes('bg-white bg-opacity-20 text-white border-white border hover:bg-opacity-30')
        
        # Main menu grid
        with ui.row().classes('w-full p-6 gap-6'):
            
            # Left column - Modern Dashboard Widgets
            with ui.column().classes('w-1/2'):
                with ui.card().classes('w-full'):
                    with ui.card_section().classes('p-6'):
                        ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2"><span class="text-3xl">🚀</span>Modern Dashboard Features</h2>')
                        
                        dashboard_features = [
                            {
                                'title': 'Real-Time Analytics Dashboard', 
                                'description': 'Live workforce analytics, performance metrics, and AI-powered insights',
                                'icon': '📊', 
                                'route': '/reporting/modern-dashboard',
                                'color': 'blue'
                            },
                            {
                                'title': 'Hardware Integration Console', 
                                'description': 'Biometric devices, card readers, face recognition, temperature scanners',
                                'icon': '🔧', 
                                'route': '/reporting/modern-dashboard',
                                'color': 'indigo'
                            },
                            {
                                'title': 'Intelligent Attendance Tracking', 
                                'description': 'AI-powered attendance predictions and anomaly detection',
                                'icon': '🤖', 
                                'route': '/reporting/modern-dashboard',
                                'color': 'purple'
                            },
                            {
                                'title': 'Comprehensive Staff Management', 
                                'description': 'Enterprise-grade staff directory with performance analytics',
                                'icon': '👥', 
                                'route': '/attendance/staff/on_duty_status',
                                'color': 'green'
                            },
                            {
                                'title': 'Advanced Holiday & Leave System', 
                                'description': 'Sophisticated vacation accrual algorithms and policy management',
                                'icon': '🏖️', 
                                'route': '/attendance/holidays',
                                'color': 'yellow'
                            },
                            {
                                'title': 'Real-Time Alerts & Notifications', 
                                'description': 'Intelligent alert system with priority filtering and automation',
                                'icon': '🔔', 
                                'route': '/reporting/modern-dashboard',
                                'color': 'red'
                            }
                        ]
                        
                        for feature in dashboard_features:
                            with ui.card().classes(f'w-full mb-4 border-l-4 border-{feature["color"]}-500 hover:shadow-lg transition-shadow cursor-pointer'):
                                with ui.card_section().classes('p-4'):
                                    with ui.row().classes('w-full items-start gap-4'):
                                        ui.html(f'<span class="text-4xl">{feature["icon"]}</span>')
                                        with ui.column().classes('flex-1'):
                                            ui.html(f'<h3 class="text-lg font-semibold text-gray-800 mb-2">{feature["title"]}</h3>')
                                            ui.html(f'<p class="text-sm text-gray-600 mb-3">{feature["description"]}</p>')
                                            ui.button(f'Open {feature["title"].split()[0]} →', 
                                                     on_click=lambda route=feature["route"]: _navigate(route)
                                            ).classes(f'bg-{feature["color"]}-500 text-white text-sm')
            
            # Right column - Traditional Menu Items
            with ui.column().classes('w-1/2'):
                with ui.card().classes('w-full'):
                    with ui.card_section().classes('p-6'):
                        ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2"><span class="text-3xl">📋</span>Traditional Menu Access</h2>')
                        
                        # Administration section
                        with ui.expansion('🏛️ Administration', icon='admin_panel_settings').classes('w-full mb-4'):
                            with ui.column().classes('w-full p-4'):
                                admin_items = [
                                    {'name': 'Institution Profile', 'route': '/administration/institution', 'icon': '🏢'},
                                    {'name': 'Enroll New Staff', 'route': '/administration/employee/enroll-staff', 'icon': '➕'},
                                    {'name': 'Departmental Sections', 'route': '/administration/departments', 'icon': '🏬'},
                                    {'name': 'Employee Termination', 'route': '/administration/termination', 'icon': '❌'},
                                    {'name': 'Employee Probation', 'route': '/administration/probation', 'icon': '⚠️'}
                                ]
                                
                                for item in admin_items:
                                    ui.button(f"{item['icon']} {item['name']}", 
                                             on_click=lambda route=item['route']: _navigate(route)
                                    ).classes('w-full justify-start mb-2 p-3 bg-blue-50 text-blue-700 hover:bg-blue-100')
                        
                        # Employee Management section  
                        with ui.expansion('👥 Employee Management', icon='people').classes('w-full mb-4'):
                            with ui.column().classes('w-full p-4'):
                                employee_items = [
                                    {'name': 'Request Transfer', 'route': '/employees/request-transfer', 'icon': '🔄'},
                                    {'name': 'Request Leave', 'route': '/employees/request-leave', 'icon': '📝'},
                                    {'name': 'Employee Directory', 'route': '/reporting/employees', 'icon': '📞'},
                                    {'name': 'Performance Reviews', 'route': '/reporting/employees', 'icon': '⭐'}
                                ]
                                
                                for item in employee_items:
                                    ui.button(f"{item['icon']} {item['name']}", 
                                             on_click=lambda route=item['route']: _navigate(route)
                                    ).classes('w-full justify-start mb-2 p-3 bg-green-50 text-green-700 hover:bg-green-100')
                        
                        # Attendance & Time Management
                        with ui.expansion('⏰ Attendance & Time', icon='schedule').classes('w-full mb-4'):
                            with ui.column().classes('w-full p-4'):
                                attendance_items = [
                                    {'name': 'Staff Status & On Duty', 'route': '/attendance/staff/on_duty_status', 'icon': '👤'},
                                    {'name': 'Staff Schedule Management', 'route': '/attendance/employee/schedule', 'icon': '📅'},
                                    {'name': 'Holiday & Vacation Management', 'route': '/attendance/holidays', 'icon': '🏖️'},
                                    {'name': 'Attendance Rules', 'route': '/attendance/attendance-rules', 'icon': '📏'},
                                    {'name': 'Leave Rules', 'route': '/attendance/leave/rules', 'icon': '📋'},
                                    {'name': 'Shift Timetable', 'route': '/attendance/timetable', 'icon': '🕐'}
                                ]
                                
                                for item in attendance_items:
                                    ui.button(f"{item['icon']} {item['name']}", 
                                             on_click=lambda route=item['route']: _navigate(route)
                                    ).classes('w-full justify-start mb-2 p-3 bg-purple-50 text-purple-700 hover:bg-purple-100')
                        
                        # Reports & Analytics
                        with ui.expansion('📊 Reports & Analytics', icon='analytics').classes('w-full mb-4'):
                            with ui.column().classes('w-full p-4'):
                                report_items = [
                                    {'name': 'Attendance Reports', 'route': '/reporting/dashboard', 'icon': '📈'},
                                    {'name': 'Performance Analytics', 'route': '/reporting/modern-dashboard', 'icon': '🎯'},
                                    {'name': 'Payroll Reports', 'route': '/reporting/administration', 'icon': '💰'},
                                    {'name': 'Compliance Reports', 'route': '/reporting/administration', 'icon': '✅'},
                                    {'name': 'Custom Reports', 'route': '/reporting/menu-integration', 'icon': '🔧'}
                                ]
                                
                                for item in report_items:
                                    ui.button(f"{item['icon']} {item['name']}", 
                                             on_click=lambda route=item['route']: _navigate(route)
                                    ).classes('w-full justify-start mb-2 p-3 bg-yellow-50 text-yellow-700 hover:bg-yellow-100')
        
        # Footer with quick stats
        with ui.row().classes('w-full p-6 bg-gray-100 border-t'):
            with ui.row().classes('w-full justify-center gap-8'):
                ui.html('<div class="text-center"><div class="text-2xl font-bold text-blue-600">63</div><div class="text-sm text-gray-600">Total Employees</div></div>')
                ui.html('<div class="text-center"><div class="text-2xl font-bold text-green-600">49</div><div class="text-sm text-gray-600">Currently Active</div></div>')
                ui.html('<div class="text-center"><div class="text-2xl font-bold text-yellow-600">7</div><div class="text-sm text-gray-600">On Break</div></div>')
                ui.html('<div class="text-center"><div class="text-2xl font-bold text-purple-600">6</div><div class="text-sm text-gray-600">Remote Workers</div></div>')
                ui.html('<div class="text-center"><div class="text-2xl font-bold text-indigo-600">4/4</div><div class="text-sm text-gray-600">Hardware Online</div></div>')

def create_dashboard_landing_page():
    """HR Dashboard overview – works cleanly with the main dark-blue sidebar navigation."""
    from datetime import datetime
    now = datetime.now()

    kpi_cards = [
        {'label': 'Total Employees', 'value': '63',  'icon': 'groups',            'bg': 'bg-blue-600',   'trend': '+2 this month'},
        {'label': 'Present Today',   'value': '49',  'icon': 'check_circle',      'bg': 'bg-green-600',  'trend': '77.8% rate'},
        {'label': 'On Leave',        'value': '7',   'icon': 'beach_access',      'bg': 'bg-orange-500', 'trend': '3 pending approval'},
        {'label': 'Remote Workers',  'value': '6',   'icon': 'home_work',         'bg': 'bg-purple-600', 'trend': '9.5% of workforce'},
        {'label': 'Open Positions',  'value': '4',   'icon': 'work',              'bg': 'bg-red-600',    'trend': '2 in final round'},
    ]

    devices = [
        {'name': 'Biometric – Main Entrance',   'status': 'online'},
        {'name': 'Card Reader – Exec Floor',    'status': 'online'},
        {'name': 'Face Recognition – R&D Lab',  'status': 'maintenance'},
        {'name': 'Temp Scanner – Health Stn',   'status': 'online'},
    ]

    activities = [
        {'text': 'John D. clocked in at 08:02',     'icon': '✅', 'time': '08:02'},
        {'text': 'Leave request from Sarah M.',      'icon': '📝', 'time': '08:45'},
        {'text': 'New hire enrolled: K. James',      'icon': '👤', 'time': '09:10'},
        {'text': 'Attendance report generated',      'icon': '📊', 'time': '09:30'},
        {'text': 'Schedule updated – Week 12',       'icon': '📅', 'time': '10:00'},
        {'text': 'Transfer request: A. Brown',       'icon': '🔄', 'time': '10:22'},
    ]

    with ui.column().classes('w-full min-h-screen bg-gray-50'):

        # ── Page header (same colour palette as the app sidebar) ──────────────
        with ui.element('div').classes(
            'w-full bg-gradient-to-r from-[#1c2a48] to-[#31497D] px-8 py-6 text-white'
        ):
            with ui.row().classes('w-full items-center justify-between'):
                with ui.row().classes('items-center gap-4'):
                    ui.icon('dashboard').classes('text-5xl text-blue-200')
                    with ui.column():
                        ui.html('<h1 class="text-3xl font-bold leading-tight">HR Management Dashboard</h1>')
                        ui.html('<p class="text-blue-200 text-sm mt-1">Real-time workforce analytics and overview</p>')
                        ui.html(
                            f'<p class="text-blue-300 text-xs mt-1">'
                            f'🏠 Home &rsaquo; Reporting &rsaquo; Dashboard'
                            f'&nbsp;·&nbsp; {now.strftime("%A, %B %d %Y  %H:%M")}'
                            f'</p>'
                        )
                with ui.row().classes(
                    'items-center gap-2 bg-green-500 bg-opacity-30 px-3 py-1 rounded-full'
                ):
                    ui.html('<div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>')
                    ui.html('<span class="text-sm text-green-100 font-medium">Live Data</span>')

        # ── KPI stat cards ─────────────────────────────────────────────────────
        with ui.row().classes('w-full px-6 pt-6 gap-4'):
            for card in kpi_cards:
                with ui.card().classes(
                    f'flex-1 {card["bg"]} text-white hover:shadow-xl transition-shadow cursor-pointer'
                ):
                    with ui.card_section().classes('p-4'):
                        with ui.row().classes('items-start justify-between'):
                            with ui.column():
                                ui.html(f'<div class="text-3xl font-bold">{card["value"]}</div>')
                                ui.html(f'<div class="text-sm opacity-90 mt-1">{card["label"]}</div>')
                            ui.icon(card['icon']).classes('text-4xl opacity-70')
                        ui.html(f'<div class="text-xs mt-3 opacity-75">↗ {card["trend"]}</div>')

        # ── Main body ──────────────────────────────────────────────────────────
        with ui.row().classes('w-full px-6 py-6 gap-6 items-start'):

            # Left – module quick-access + attendance bars
            with ui.column().classes('flex-1 gap-4'):
                ui.html('<h2 class="text-base font-bold text-gray-700">Quick Access</h2>')
                with ui.row().classes('w-full gap-4 flex-wrap'):
                    nav_cards = [
                        {'title': 'Analytics',        'desc': 'Performance & trends',    'icon': 'analytics',           'route': '/reporting/modern-dashboard',    'border': 'border-indigo-500'},
                        {'title': 'Employee Reports', 'desc': 'Staff directory & stats', 'icon': 'people',              'route': '/reporting/employees',           'border': 'border-blue-500'},
                        {'title': 'Timesheets',       'desc': 'Time & attendance logs',  'icon': 'schedule',            'route': '/reporting/employees/timesheet', 'border': 'border-teal-500'},
                        {'title': 'Administration',   'desc': 'HR admin reports',        'icon': 'admin_panel_settings','route': '/reporting/administration',      'border': 'border-purple-500'},
                        {'title': 'Departments',      'desc': 'Department overview',     'icon': 'business',            'route': '/reporting/departments',         'border': 'border-green-500'},
                        {'title': 'Leave Reports',    'desc': 'Leave tracking & policy', 'icon': 'event_busy',          'route': '/reporting/leaves',              'border': 'border-orange-500'},
                        {'title': 'Asset Inventory',  'desc': 'Hardware & assets',       'icon': 'inventory',           'route': '/reporting/assets',              'border': 'border-gray-500'},
                        {'title': 'AI Orchestrator',  'desc': 'AI-powered insights',     'icon': 'psychology',          'route': '/ai/orchestrator',               'border': 'border-pink-500'},
                    ]
                    for nav in nav_cards:
                        with ui.card().classes(
                            f'w-44 hover:shadow-lg transition-all cursor-pointer border-l-4 {nav["border"]}'
                        ).on('click', lambda r=nav['route']: _navigate(r)):
                            with ui.card_section().classes('p-3'):
                                with ui.row().classes('items-center gap-2 mb-1'):
                                    ui.icon(nav['icon']).classes('text-gray-600 text-xl')
                                    ui.html(f'<div class="font-semibold text-gray-800 text-sm">{nav["title"]}</div>')
                                ui.html(f'<div class="text-xs text-gray-500">{nav["desc"]}</div>')

                # Attendance bar chart
                with ui.card().classes('w-full mt-2'):
                    with ui.card_section().classes('p-4'):
                        ui.html('<h3 class="font-bold text-gray-700 mb-3">📊 This Week\'s Attendance</h3>')
                        for day, pct in [('Mon', 88), ('Tue', 91), ('Wed', 87), ('Thu', 93), ('Fri', 85)]:
                            with ui.row().classes('items-center gap-3 mb-2'):
                                ui.html(f'<div class="w-10 text-xs font-medium text-gray-600">{day}</div>')
                                with ui.element('div').classes('flex-1 bg-gray-200 rounded-full h-3'):
                                    ui.element('div').classes(
                                        'bg-blue-500 h-3 rounded-full'
                                    ).style(f'width:{pct}%')
                                ui.html(f'<div class="w-10 text-xs text-gray-500 text-right">{pct}%</div>')

            # Right – activity feed + hardware status
            with ui.column().classes('w-72 gap-4'):

                with ui.card().classes('w-full'):
                    with ui.card_section().classes(
                        'p-3 bg-gradient-to-r from-[#1c2a48] to-[#31497D] text-white rounded-t'
                    ):
                        ui.html('<h3 class="font-bold">⚡ Recent Activity</h3>')
                    with ui.card_section().classes('p-3'):
                        for act in activities:
                            with ui.row().classes('items-center gap-3 py-2 border-b border-gray-100 last:border-0'):
                                ui.html(f'<span class="text-base">{act["icon"]}</span>')
                                with ui.column().classes('flex-1'):
                                    ui.html(f'<div class="text-xs text-gray-800">{act["text"]}</div>')
                                    ui.html(f'<div class="text-xs text-gray-400">{act["time"]} AM</div>')

                with ui.card().classes('w-full'):
                    with ui.card_section().classes(
                        'p-3 bg-gradient-to-r from-green-700 to-green-600 text-white rounded-t'
                    ):
                        ui.html('<h3 class="font-bold">🔧 Hardware Status</h3>')
                    with ui.card_section().classes('p-3'):
                        for dev in devices:
                            icon = '🟢' if dev['status'] == 'online' else '🟡'
                            with ui.row().classes('items-center gap-2 py-1'):
                                ui.html(f'<span>{icon}</span>')
                                ui.html(f'<div class="text-xs text-gray-700">{dev["name"]}</div>')
                ui.html('<div class="text-sm opacity-75">Modern Workforce Management Solution</div>')