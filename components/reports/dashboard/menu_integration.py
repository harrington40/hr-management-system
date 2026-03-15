"""
HR Dashboard Menu Integration
Links all HR modules with the comprehensive dashboard system
Provides seamless navigation between modern dashboard and traditional menu items
"""

from nicegui import ui
from helperFuns import build_mount_route
from helperFuns.employee_registry import employee_registry


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
        
        # Footer with quick stats — live from registry
        _f_total  = employee_registry.count()
        _f_active = employee_registry.count('active')
        _f_leave  = employee_registry.count('on_leave')
        _f_remote = sum(1 for e in employee_registry.get_all() if e.get('location', '').lower() == 'remote')
        with ui.row().classes('w-full p-6 bg-gray-100 border-t'):
            with ui.row().classes('w-full justify-center gap-8'):
                ui.html(f'<div class="text-center"><div class="text-2xl font-bold text-blue-600">{_f_total}</div><div class="text-sm text-gray-600">Total Employees</div></div>')
                ui.html(f'<div class="text-center"><div class="text-2xl font-bold text-green-600">{_f_active}</div><div class="text-sm text-gray-600">Currently Active</div></div>')
                ui.html(f'<div class="text-center"><div class="text-2xl font-bold text-yellow-600">{_f_leave}</div><div class="text-sm text-gray-600">On Leave</div></div>')
                ui.html(f'<div class="text-center"><div class="text-2xl font-bold text-purple-600">{_f_remote}</div><div class="text-sm text-gray-600">Remote Workers</div></div>')
                ui.html('<div class="text-center"><div class="text-2xl font-bold text-indigo-600">4/4</div><div class="text-sm text-gray-600">Hardware Online</div></div>')

def create_dashboard_landing_page():
    """HR Dashboard overview – works cleanly with the main dark-blue sidebar navigation."""
    from datetime import datetime
    now = datetime.now()

    # --- Live counts from the shared registry ---
    _total   = employee_registry.count()
    _active  = employee_registry.count('active')
    _leave   = employee_registry.count('on_leave')
    _remote  = sum(1 for e in employee_registry.get_all() if e.get('location', '').lower() == 'remote')
    _present = max(_active, 0)   # active == present for current data model
    _att_pct = f'{round(_present / _total * 100, 1)}% rate' if _total else '0% rate'
    _leave_trend = f'{_leave} on leave'
    _remote_pct  = f'{round(_remote / _total * 100, 1)}% of workforce' if _total else '0% of workforce'

    # KPI cards — gradient defined as inline CSS so Tailwind JIT is not needed
    kpi_cards = [
        {'label': 'Total Employees', 'value': str(_total),   'icon': 'groups',            'gradient': 'linear-gradient(135deg,#3b82f6,#1d4ed8)', 'trend': 'from registry'},
        {'label': 'Present Today',   'value': str(_present), 'icon': 'check_circle',      'gradient': 'linear-gradient(135deg,#10b981,#065f46)', 'trend': _att_pct},
        {'label': 'On Leave',        'value': str(_leave),   'icon': 'beach_access',      'gradient': 'linear-gradient(135deg,#f97316,#c2410c)', 'trend': _leave_trend},
        {'label': 'Remote Workers',  'value': str(_remote),  'icon': 'home_work',         'gradient': 'linear-gradient(135deg,#8b5cf6,#5b21b6)', 'trend': _remote_pct},
        {'label': 'Open Positions',  'value': '4',           'icon': 'work',              'gradient': 'linear-gradient(135deg,#f43f5e,#9f1239)', 'trend': '2 in final round'},
    ]

    # Nav cards — bg/icon colours as hex so they always render
    nav_cards = [
        {'title': 'Analytics',        'desc': 'Trends & KPIs',    'icon': 'analytics',            'route': '/reporting/modern-dashboard',    'bg': '#eef2ff', 'icon_color': '#6366f1'},
        {'title': 'Employee Reports', 'desc': 'Staff & stats',     'icon': 'people',               'route': '/reporting/employees',           'bg': '#eff6ff', 'icon_color': '#3b82f6'},
        {'title': 'Timesheets',       'desc': 'Time logs',         'icon': 'schedule',             'route': '/reporting/employees/timesheet', 'bg': '#f0fdfa', 'icon_color': '#14b8a6'},
        {'title': 'Administration',   'desc': 'HR admin',          'icon': 'admin_panel_settings', 'route': '/reporting/administration',      'bg': '#faf5ff', 'icon_color': '#a855f7'},
        {'title': 'Departments',      'desc': 'Teams overview',    'icon': 'business',             'route': '/reporting/departments',         'bg': '#f0fdf4', 'icon_color': '#22c55e'},
        {'title': 'Leave Reports',    'desc': 'Leave & policy',    'icon': 'event_busy',           'route': '/reporting/leaves',              'bg': '#fff7ed', 'icon_color': '#f97316'},
        {'title': 'Asset Inventory',  'desc': 'Hardware & assets', 'icon': 'inventory',            'route': '/reporting/assets',              'bg': '#f8fafc', 'icon_color': '#64748b'},
        {'title': 'AI Orchestrator',  'desc': 'AI insights',       'icon': 'psychology',           'route': '/ai/orchestrator',               'bg': '#fdf2f8', 'icon_color': '#ec4899'},
    ]

    devices = [
        {'name': 'Biometric – Main Entrance',   'status': 'online'},
        {'name': 'Card Reader – Exec Floor',    'status': 'online'},
        {'name': 'Face Recognition – R&D Lab',  'status': 'maintenance'},
        {'name': 'Temp Scanner – Health Stn',   'status': 'online'},
    ]

    activities = [
        {'text': 'John D. clocked in at 08:02', 'icon': 'login',       'icon_color': '#10b981', 'time': '08:02'},
        {'text': 'Leave request from Sarah M.', 'icon': 'description', 'icon_color': '#3b82f6', 'time': '08:45'},
        {'text': 'New hire enrolled: K. James', 'icon': 'person_add',  'icon_color': '#8b5cf6', 'time': '09:10'},
        {'text': 'Attendance report generated', 'icon': 'bar_chart',   'icon_color': '#14b8a6', 'time': '09:30'},
        {'text': 'Schedule updated – Week 12',  'icon': 'event',       'icon_color': '#6366f1', 'time': '10:00'},
        {'text': 'Transfer request: A. Brown',  'icon': 'swap_horiz',  'icon_color': '#f97316', 'time': '10:22'},
    ]

    # bar chart data — bar colour as hex so it always renders
    bar_data = [
        ('Mon', 88, '#3b82f6'),
        ('Tue', 91, '#6366f1'),
        ('Wed', 87, '#3b82f6'),
        ('Thu', 93, '#6366f1'),
        ('Fri', 85, '#60a5fa'),
    ]

    # ── inject a tiny helper style once ─────────────────────────────────────────
    ui.add_head_html('''
    <style>
      .dash-card-hover:hover { box-shadow: 0 8px 30px rgba(0,0,0,.18) !important; transform: translateY(-2px); }
      .dash-nav-item:hover   { opacity:.85; transform:translateY(-1px); }
      .dash-nav-item         { transition: opacity .15s, transform .15s; }
      .dash-kpi              { transition: box-shadow .2s, transform .2s; }
      .row-sep + .row-sep    { border-top: 1px solid #f1f5f9; }
    </style>
    ''')

    with ui.column().classes('w-full min-h-screen').style('background:#eef2f7'):

        # ── Full-width header ─────────────────────────────────────────────────
        with ui.element('div').classes('w-full').style(
            'background:linear-gradient(100deg,#1c2a48 0%,#2d4a7a 60%,#1e3a5f 100%);'
            'box-shadow:0 4px 24px rgba(0,0,0,.3)'
        ):
            # centred inner container
            with ui.element('div').classes('px-8 py-5').style('max-width:1400px;margin:0 auto'):
                with ui.row().classes('w-full items-center justify-between'):
                    with ui.row().classes('items-center gap-4'):
                        with ui.element('div').classes('flex items-center justify-center flex-shrink-0').style(
                            'width:52px;height:52px;border-radius:14px;'
                            'background:rgba(255,255,255,.13);'
                            'box-shadow:0 2px 8px rgba(0,0,0,.2)'
                        ):
                            ui.icon('dashboard').classes('text-4xl').style('color:#93c5fd')
                        with ui.column().classes('gap-0'):
                            ui.html('<h1 style="font-size:1.4rem;font-weight:800;color:#fff;letter-spacing:-.3px;line-height:1.2">HR Management Dashboard</h1>')
                            ui.html('<p style="color:#93c5fd;font-size:.8rem;margin-top:2px">Real-time workforce analytics &amp; smart reporting</p>')
                            ui.html(
                                f'<p style="color:#6080aa;font-size:.7rem;margin-top:3px">'
                                f'Home › Reporting › Stats Analysis'
                                f'&nbsp;&nbsp;·&nbsp;&nbsp;{now.strftime("%A, %d %b %Y · %H:%M")}'
                                f'</p>'
                            )
                    with ui.element('div').classes('flex items-center gap-2 px-4 py-2').style(
                        'background:rgba(16,185,129,.18);'
                        'border:1px solid rgba(52,211,153,.35);'
                        'border-radius:99px'
                    ):
                        ui.html('<div style="width:8px;height:8px;border-radius:50%;background:#34d399" class="animate-pulse"></div>')
                        ui.html('<span style="font-size:.8rem;font-weight:600;color:#a7f3d0">Live</span>')

        # ── centred content wrapper ───────────────────────────────────────────
        with ui.element('div').classes('px-6 pb-10').style('max-width:1400px;margin:0 auto;width:100%'):

            # ── KPI cards row ─────────────────────────────────────────────────
            with ui.row().classes('w-full pt-6 gap-4').style('flex-wrap:nowrap'):
                for card in kpi_cards:
                    with ui.card().classes('flex-1 overflow-hidden text-white dash-kpi dash-card-hover').style(
                        f'background:{card["gradient"]};border-radius:16px;'
                        'box-shadow:0 4px 16px rgba(0,0,0,.15);cursor:pointer'
                    ):
                        with ui.card_section().classes('p-5'):
                            with ui.row().classes('w-full justify-between items-start mb-3'):
                                with ui.element('div').classes('flex items-center justify-center').style(
                                    'width:44px;height:44px;border-radius:12px;background:rgba(255,255,255,.22)'
                                ):
                                    ui.icon(card['icon']).classes('text-2xl text-white')
                            ui.html(f'<div style="font-size:2rem;font-weight:900;letter-spacing:-.5px">{card["value"]}</div>')
                            ui.html(f'<div style="font-size:.82rem;font-weight:600;opacity:.88;margin-top:2px">{card["label"]}</div>')
                            ui.html(f'<div style="font-size:.7rem;opacity:.65;margin-top:8px">↗&nbsp;{card["trend"]}</div>')

            # ── Main two-column body ──────────────────────────────────────────
            with ui.row().classes('w-full pt-5 gap-5 items-start'):

                # ── LEFT column ───────────────────────────────────────────────
                with ui.column().classes('flex-1 gap-5').style('min-width:0'):

                    # Quick Access card
                    with ui.card().classes('w-full overflow-hidden').style(
                        'border-radius:16px;box-shadow:0 2px 12px rgba(0,0,0,.1)'
                    ):
                        with ui.element('div').classes('px-6 py-4').style(
                            'background:linear-gradient(90deg,#1e293b,#334155)'
                        ):
                            with ui.row().classes('items-center gap-3'):
                                with ui.element('div').classes('flex items-center justify-center').style(
                                    'width:34px;height:34px;border-radius:9px;background:rgba(255,255,255,.1)'
                                ):
                                    ui.icon('grid_view').classes('text-lg').style('color:#94a3b8')
                                ui.html('<span style="color:#fff;font-weight:700;font-size:.9rem;letter-spacing:.3px">Quick Access</span>')
                                ui.html('<span style="color:#475569;font-size:.75rem;margin-left:4px">— jump to any module</span>')

                        with ui.grid(columns=4).classes('gap-3 p-5'):
                            for nav in nav_cards:
                                with ui.element('div').classes('flex flex-col items-center gap-2 p-3 dash-nav-item cursor-pointer').style(
                                    f'background:{nav["bg"]};border-radius:12px'
                                ).on('click', lambda r=nav['route']: _navigate(r)):
                                    with ui.element('div').classes('flex items-center justify-center').style(
                                        f'width:42px;height:42px;border-radius:11px;'
                                        f'background:{nav["icon_color"]};'
                                        f'box-shadow:0 2px 8px rgba(0,0,0,.15)'
                                    ):
                                        ui.icon(nav['icon']).classes('text-xl text-white')
                                    ui.html(f'<div style="font-size:.72rem;font-weight:700;color:#1e293b;text-align:center;line-height:1.3">{nav["title"]}</div>')
                                    ui.html(f'<div style="font-size:.65rem;color:#64748b;text-align:center;line-height:1.3">{nav["desc"]}</div>')

                    # Attendance bar chart card
                    with ui.card().classes('w-full overflow-hidden').style(
                        'border-radius:16px;box-shadow:0 2px 12px rgba(0,0,0,.1)'
                    ):
                        with ui.element('div').classes('px-6 py-4').style(
                            'background:linear-gradient(90deg,#1d4ed8,#4338ca)'
                        ):
                            with ui.row().classes('items-center gap-3'):
                                with ui.element('div').classes('flex items-center justify-center').style(
                                    'width:34px;height:34px;border-radius:9px;background:rgba(255,255,255,.15)'
                                ):
                                    ui.icon('bar_chart').classes('text-lg text-blue-200')
                                ui.html('<span style="color:#fff;font-weight:700;font-size:.9rem;letter-spacing:.3px">This Week\'s Attendance</span>')

                        with ui.column().classes('px-6 py-5 gap-4'):
                            for day, pct, color in bar_data:
                                with ui.row().classes('items-center gap-3'):
                                    ui.html(f'<div style="width:26px;font-size:.73rem;font-weight:700;color:#64748b">{day}</div>')
                                    with ui.element('div').classes('flex-1 overflow-hidden').style(
                                        'background:#dde3ec;border-radius:99px;height:10px'
                                    ):
                                        ui.element('div').style(
                                            f'width:{pct}%;height:100%;border-radius:99px;'
                                            f'background:{color};'
                                            f'box-shadow:0 1px 4px rgba(0,0,0,.15)'
                                        )
                                    ui.html(f'<div style="width:2.4rem;font-size:.73rem;font-weight:700;color:#475569;text-align:right">{pct}%</div>')

                # ── RIGHT column ──────────────────────────────────────────────
                with ui.column().classes('gap-5').style('width:22rem;flex-shrink:0'):

                    # Recent Activity card
                    with ui.card().classes('w-full overflow-hidden').style(
                        'border-radius:16px;box-shadow:0 2px 12px rgba(0,0,0,.1)'
                    ):
                        with ui.element('div').classes('px-6 py-4').style(
                            'background:linear-gradient(90deg,#1c2a48,#31497d)'
                        ):
                            with ui.row().classes('items-center gap-3'):
                                with ui.element('div').classes('flex items-center justify-center').style(
                                    'width:34px;height:34px;border-radius:9px;background:rgba(255,255,255,.1)'
                                ):
                                    ui.icon('bolt').classes('text-lg text-blue-200')
                                ui.html('<span style="color:#fff;font-weight:700;font-size:.9rem;letter-spacing:.3px">Recent Activity</span>')

                        with ui.column().classes('px-4 py-2 gap-0'):
                            for act in activities:
                                with ui.element('div').classes('row-sep').style(
                                    'display:flex;align-items:center;gap:12px;padding:10px 4px'
                                ):
                                    with ui.element('div').classes('flex items-center justify-center flex-shrink-0').style(
                                        'width:32px;height:32px;border-radius:8px;background:#f1f5f9'
                                    ):
                                        ui.icon(act['icon']).classes('text-base').style(f'color:{act["icon_color"]}')
                                    ui.html(
                                        f'<div style="flex:1">'
                                        f'<div style="font-size:.75rem;font-weight:500;color:#1e293b;line-height:1.4">{act["text"]}</div>'
                                        f'<div style="font-size:.7rem;color:#94a3b8;margin-top:1px">{act["time"]} AM</div>'
                                        f'</div>'
                                    )

                    # Hardware Status card
                    with ui.card().classes('w-full overflow-hidden').style(
                        'border-radius:16px;box-shadow:0 2px 12px rgba(0,0,0,.1)'
                    ):
                        with ui.element('div').classes('px-6 py-4').style(
                            'background:linear-gradient(90deg,#065f46,#0f766e)'
                        ):
                            with ui.row().classes('items-center gap-3'):
                                with ui.element('div').classes('flex items-center justify-center').style(
                                    'width:34px;height:34px;border-radius:9px;background:rgba(255,255,255,.12)'
                                ):
                                    ui.icon('developer_board').classes('text-lg').style('color:#6ee7b7')
                                ui.html('<span style="color:#fff;font-weight:700;font-size:.9rem;letter-spacing:.3px">Hardware Status</span>')

                        with ui.column().classes('px-4 py-2 gap-0'):
                            for dev in devices:
                                is_online = dev['status'] == 'online'
                                dot_color  = '#10b981' if is_online else '#f59e0b'
                                badge_bg   = '#d1fae5' if is_online else '#fef3c7'
                                badge_fg   = '#065f46' if is_online else '#92400e'
                                label      = 'Online'  if is_online else 'Maintenance'
                                pulse      = ' class="animate-pulse"' if is_online else ''
                                with ui.element('div').classes('row-sep').style(
                                    'display:flex;align-items:center;gap:10px;padding:10px 4px'
                                ):
                                    ui.html(
                                        f'<div{pulse} style="width:10px;height:10px;border-radius:50%;'
                                        f'background:{dot_color};flex-shrink:0"></div>'
                                    )
                                    ui.html(f'<div style="flex:1;font-size:.75rem;font-weight:500;color:#334155">{dev["name"]}</div>')
                                    ui.html(
                                        f'<span style="font-size:.68rem;font-weight:700;padding:2px 9px;'
                                        f'border-radius:99px;background:{badge_bg};color:{badge_fg}">{label}</span>'
                                    )

            # ── Footer ────────────────────────────────────────────────────────
            with ui.element('div').classes('w-full mt-4 py-3 text-center').style('border-top:1px solid #d1d5db'):
                ui.html(
                    '<span style="font-size:.72rem;color:#94a3b8">'
                    'HRMkit · HR Management Platform · Real-time data</span>'
                )