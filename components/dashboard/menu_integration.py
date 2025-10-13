"""
HR Dashboard Menu Integration
Links all HR modules with the comprehensive dashboard system
Provides seamless navigation between modern dashboard and traditional menu items
"""

from nicegui import ui
from components.dashboard.main_dashboard import create_main_dashboard, UserRole

def create_integrated_dashboard_menu():
    """Create integrated menu that shows both dashboard and traditional menu options"""
    
    with ui.column().classes('w-full h-full bg-gradient-to-br from-blue-50 to-indigo-50 min-h-screen'):
        # Header
        with ui.row().classes('w-full p-6 bg-gradient-to-r from-blue-600 to-indigo-600 text-white'):
            with ui.row().classes('w-full justify-between items-center'):
                ui.html('<h1 class="text-3xl font-bold flex items-center gap-3"><span class="text-4xl">🏢</span>HR Management System</h1>', sanitize=False)
                
                with ui.row().classes('gap-4'):
                    ui.button('🏠 Modern Dashboard', on_click=lambda: ui.navigate.to('/dashboard')).classes('bg-white text-blue-600 hover:bg-gray-100')
                    ui.button('📋 Traditional Menu', on_click=lambda: ui.navigate.to('/dashboard?view=menu')).classes('bg-white bg-opacity-20 text-white border-white border hover:bg-opacity-30')
        
        # Main menu grid
        with ui.row().classes('w-full p-6 gap-6'):
            
            # Left column - Modern Dashboard Widgets
            with ui.column().classes('w-1/2'):
                with ui.card().classes('w-full'):
                    with ui.card_section().classes('p-6'):
                        ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2"><span class="text-3xl">🚀</span>Modern Dashboard Features</h2>', sanitize=False)
                        
                        dashboard_features = [
                            {
                                'title': 'Real-Time Analytics Dashboard', 
                                'description': 'Live workforce analytics, performance metrics, and AI-powered insights',
                                'icon': '📊', 
                                'route': '/dashboard',
                                'color': 'blue'
                            },
                            {
                                'title': 'Hardware Integration Console', 
                                'description': 'Biometric devices, card readers, face recognition, temperature scanners',
                                'icon': '🔧', 
                                'route': '/dashboard',
                                'color': 'indigo'
                            },
                            {
                                'title': 'Intelligent Attendance Tracking', 
                                'description': 'AI-powered attendance predictions and anomaly detection',
                                'icon': '🤖', 
                                'route': '/dashboard',
                                'color': 'purple'
                            },
                            {
                                'title': 'Comprehensive Staff Management', 
                                'description': 'Enterprise-grade staff directory with performance analytics',
                                'icon': '👥', 
                                'route': '/attendance/staff-status',
                                'color': 'green'
                            },
                            {
                                'title': 'Advanced Holiday & Leave System', 
                                'description': 'Sophisticated vacation accrual algorithms and policy management',
                                'icon': '🏖️', 
                                'route': '/attendance/set-holidays',
                                'color': 'yellow'
                            },
                            {
                                'title': 'Real-Time Alerts & Notifications', 
                                'description': 'Intelligent alert system with priority filtering and automation',
                                'icon': '🔔', 
                                'route': '/dashboard',
                                'color': 'red'
                            }
                        ]
                        
                        for feature in dashboard_features:
                            with ui.card().classes(f'w-full mb-4 border-l-4 border-{feature["color"]}-500 hover:shadow-lg transition-shadow cursor-pointer'):
                                with ui.card_section().classes('p-4'):
                                    with ui.row().classes('w-full items-start gap-4'):
                                        ui.html(f'<span class="text-4xl">{feature["icon"]}</span>', sanitize=False)
                                        with ui.column().classes('flex-1'):
                                            ui.html(f'<h3 class="text-lg font-semibold text-gray-800 mb-2">{feature["title"]}</h3>', sanitize=False)
                                            ui.html(f'<p class="text-sm text-gray-600 mb-3">{feature["description"]}</p>', sanitize=False)
                                            ui.button(f'Open {feature["title"].split()[0]} →', 
                                                     on_click=lambda route=feature["route"]: ui.navigate.to(route)
                                            ).classes(f'bg-{feature["color"]}-500 text-white text-sm')
            
            # Right column - Traditional Menu Items
            with ui.column().classes('w-1/2'):
                with ui.card().classes('w-full'):
                    with ui.card_section().classes('p-6'):
                        ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2"><span class="text-3xl">📋</span>Traditional Menu Access</h2>', sanitize=False)
                        
                        # Administration section
                        with ui.expansion('🏛️ Administration', icon='admin_panel_settings').classes('w-full mb-4'):
                            with ui.column().classes('w-full p-4'):
                                admin_items = [
                                    {'name': 'Institution Profile', 'route': '/administration/institution', 'icon': '🏢'},
                                    {'name': 'Enroll New Staff', 'route': '/administration/enroll-staff', 'icon': '➕'},
                                    {'name': 'Departmental Sections', 'route': '/administration/departments', 'icon': '🏬'},
                                    {'name': 'Employee Termination', 'route': '/administration/termination', 'icon': '❌'},
                                    {'name': 'Employee Probation', 'route': '/administration/probation', 'icon': '⚠️'}
                                ]
                                
                                for item in admin_items:
                                    ui.button(f"{item['icon']} {item['name']}", 
                                             on_click=lambda route=item['route']: ui.navigate.to(route)
                                    ).classes('w-full justify-start mb-2 p-3 bg-blue-50 text-blue-700 hover:bg-blue-100')
                        
                        # Employee Management section  
                        with ui.expansion('👥 Employee Management', icon='people').classes('w-full mb-4'):
                            with ui.column().classes('w-full p-4'):
                                employee_items = [
                                    {'name': 'Request Transfer', 'route': '/employees/request-transfer', 'icon': '🔄'},
                                    {'name': 'Request Leave', 'route': '/employees/request-leave', 'icon': '📝'},
                                    {'name': 'Employee Directory', 'route': '/employees/directory', 'icon': '📞'},
                                    {'name': 'Performance Reviews', 'route': '/employees/performance', 'icon': '⭐'}
                                ]
                                
                                for item in employee_items:
                                    ui.button(f"{item['icon']} {item['name']}", 
                                             on_click=lambda route=item['route']: ui.navigate.to(route)
                                    ).classes('w-full justify-start mb-2 p-3 bg-green-50 text-green-700 hover:bg-green-100')
                        
                        # Attendance & Time Management
                        with ui.expansion('⏰ Attendance & Time', icon='schedule').classes('w-full mb-4'):
                            with ui.column().classes('w-full p-4'):
                                attendance_items = [
                                    {'name': 'Staff Status & On Duty', 'route': '/attendance/staff-status', 'icon': '👤'},
                                    {'name': 'Staff Schedule Management', 'route': '/attendance/staff-schedule', 'icon': '📅'},
                                    {'name': 'Holiday & Vacation Management', 'route': '/attendance/set-holidays', 'icon': '🏖️'},
                                    {'name': 'Attendance Rules', 'route': '/attendance/rules', 'icon': '📏'},
                                    {'name': 'Leave Rules', 'route': '/attendance/leave-rules', 'icon': '📋'},
                                    {'name': 'Shift Timetable', 'route': '/attendance/shift-timetable', 'icon': '🕐'}
                                ]
                                
                                for item in attendance_items:
                                    ui.button(f"{item['icon']} {item['name']}", 
                                             on_click=lambda route=item['route']: ui.navigate.to(route)
                                    ).classes('w-full justify-start mb-2 p-3 bg-purple-50 text-purple-700 hover:bg-purple-100')
                        
                        # Reports & Analytics
                        with ui.expansion('📊 Reports & Analytics', icon='analytics').classes('w-full mb-4'):
                            with ui.column().classes('w-full p-4'):
                                report_items = [
                                    {'name': 'Attendance Reports', 'route': '/reports/attendance', 'icon': '📈'},
                                    {'name': 'Performance Analytics', 'route': '/reports/performance', 'icon': '🎯'},
                                    {'name': 'Payroll Reports', 'route': '/reports/payroll', 'icon': '💰'},
                                    {'name': 'Compliance Reports', 'route': '/reports/compliance', 'icon': '✅'},
                                    {'name': 'Custom Reports', 'route': '/reports/custom', 'icon': '🔧'}
                                ]
                                
                                for item in report_items:
                                    ui.button(f"{item['icon']} {item['name']}", 
                                             on_click=lambda route=item['route']: ui.navigate.to(route)
                                    ).classes('w-full justify-start mb-2 p-3 bg-yellow-50 text-yellow-700 hover:bg-yellow-100')
        
        # Footer with quick stats
        with ui.row().classes('w-full p-6 bg-gray-100 border-t'):
            with ui.row().classes('w-full justify-center gap-8'):
                ui.html('<div class="text-center"><div class="text-2xl font-bold text-blue-600">63</div><div class="text-sm text-gray-600">Total Employees</div></div>', sanitize=False)
                ui.html('<div class="text-center"><div class="text-2xl font-bold text-green-600">49</div><div class="text-sm text-gray-600">Currently Active</div></div>', sanitize=False)
                ui.html('<div class="text-center"><div class="text-2xl font-bold text-yellow-600">7</div><div class="text-sm text-gray-600">On Break</div></div>', sanitize=False)
                ui.html('<div class="text-center"><div class="text-2xl font-bold text-purple-600">6</div><div class="text-sm text-gray-600">Remote Workers</div></div>', sanitize=False)
                ui.html('<div class="text-center"><div class="text-2xl font-bold text-indigo-600">4/4</div><div class="text-sm text-gray-600">Hardware Online</div></div>', sanitize=False)

def create_dashboard_landing_page():
    """Create a landing page that offers both dashboard styles"""
    
    with ui.column().classes('w-full h-full bg-gradient-to-br from-slate-100 via-blue-50 to-indigo-100 min-h-screen'):
        # Hero section
        with ui.row().classes('w-full p-12 text-center'):
            with ui.column().classes('w-full max-w-4xl mx-auto'):
                ui.html('<h1 class="text-5xl font-bold text-gray-800 mb-6">🏢 Enterprise HR Management System</h1>', sanitize=False)
                ui.html('<p class="text-xl text-gray-600 mb-8">Choose your preferred interface for comprehensive workforce management</p>', sanitize=False)
                
                # Interface options
                with ui.row().classes('w-full gap-8 justify-center'):
                    
                    # Modern Dashboard Option
                    with ui.card().classes('w-96 hover:shadow-2xl transition-all duration-300 transform hover:scale-105 cursor-pointer'):
                        with ui.card_section().classes('p-8 text-center'):
                            ui.html('<div class="text-6xl mb-4">🚀</div>', sanitize=False)
                            ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">Modern Dashboard</h2>', sanitize=False)
                            ui.html('<p class="text-gray-600 mb-6">Real-time analytics, AI insights, hardware integration, and comprehensive workforce management</p>', sanitize=False)
                            
                            # Features list
                            features = ['📊 Live Analytics', '🤖 AI-Powered Insights', '🔧 Hardware Integration', '📱 Mobile Responsive']
                            for feature in features:
                                ui.html(f'<div class="text-sm text-blue-600 mb-1">✓ {feature}</div>', sanitize=False)
                            
                            ui.button('🏢 Open Modern Dashboard', 
                                     on_click=lambda: ui.navigate.to('/dashboard')
                            ).classes('w-full mt-6 bg-blue-600 text-white text-lg py-3')
                    
                    # Traditional Menu Option
                    with ui.card().classes('w-96 hover:shadow-2xl transition-all duration-300 transform hover:scale-105 cursor-pointer'):
                        with ui.card_section().classes('p-8 text-center'):
                            ui.html('<div class="text-6xl mb-4">📋</div>', sanitize=False)
                            ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">Traditional Menu</h2>', sanitize=False)
                            ui.html('<p class="text-gray-600 mb-6">Classic navigation interface with organized menu structure and familiar layout</p>', sanitize=False)
                            
                            # Features list
                            features = ['📁 Organized Menus', '🎯 Direct Access', '📋 Structured Layout', '⚡ Quick Navigation']
                            for feature in features:
                                ui.html(f'<div class="text-sm text-green-600 mb-1">✓ {feature}</div>', sanitize=False)
                            
                            ui.button('📋 Open Traditional Menu', 
                                     on_click=lambda: ui.navigate.to('/dashboard?view=menu')
                            ).classes('w-full mt-6 bg-green-600 text-white text-lg py-3')
                
                # Integration option
                with ui.card().classes('w-full max-w-2xl mx-auto mt-8 border-2 border-indigo-200'):
                    with ui.card_section().classes('p-6 text-center'):
                        ui.html('<h3 class="text-xl font-bold text-gray-800 mb-4">🔗 Integrated Menu System</h3>', sanitize=False)
                        ui.html('<p class="text-gray-600 mb-4">Experience both interfaces in one comprehensive menu with seamless navigation between modern and traditional views</p>', sanitize=False)
                        ui.button('🔗 Open Integrated Menu', 
                                 on_click=lambda: ui.navigate.to('/menu-integration')
                        ).classes('bg-indigo-600 text-white px-8 py-3')

        # System features overview
        with ui.row().classes('w-full p-12 bg-white'):
            with ui.column().classes('w-full max-w-6xl mx-auto'):
                ui.html('<h2 class="text-3xl font-bold text-center text-gray-800 mb-12">🎯 Comprehensive HR Solution</h2>', sanitize=False)
                
                with ui.row().classes('w-full gap-8'):
                    system_features = [
                        {
                            'title': 'Staff Management', 
                            'icon': '👥', 
                            'description': 'Complete employee lifecycle management with advanced analytics',
                            'items': ['Employee Directory', 'Performance Tracking', 'Skills Management', 'Career Planning']
                        },
                        {
                            'title': 'Attendance Tracking', 
                            'icon': '⏰', 
                            'description': 'AI-powered attendance with hardware integration',
                            'items': ['Biometric Integration', 'Real-time Monitoring', 'Predictive Analytics', 'Compliance Reports']
                        },
                        {
                            'title': 'Leave Management', 
                            'icon': '🏖️', 
                            'description': 'Sophisticated vacation and leave policy management',
                            'items': ['Accrual Algorithms', 'Policy Automation', 'Approval Workflows', 'Balance Tracking']
                        },
                        {
                            'title': 'Hardware Integration', 
                            'icon': '🔧', 
                            'description': 'Seamless integration with biometric and access control systems',
                            'items': ['Biometric Scanners', 'Card Readers', 'Face Recognition', 'Temperature Monitoring']
                        }
                    ]
                    
                    for feature in system_features:
                        with ui.card().classes('flex-1'):
                            with ui.card_section().classes('p-6'):
                                ui.html(f'<div class="text-4xl text-center mb-4">{feature["icon"]}</div>', sanitize=False)
                                ui.html(f'<h3 class="text-xl font-bold text-gray-800 mb-3 text-center">{feature["title"]}</h3>', sanitize=False)
                                ui.html(f'<p class="text-gray-600 mb-4 text-center">{feature["description"]}</p>', sanitize=False)
                                
                                for item in feature['items']:
                                    ui.html(f'<div class="text-sm text-blue-600 mb-1">✓ {item}</div>', sanitize=False)
        
        # Footer
        with ui.row().classes('w-full p-6 bg-gray-800 text-white'):
            with ui.row().classes('w-full justify-between items-center'):
                ui.html('<div class="text-lg font-semibold">HR-Kit Enterprise v2.1.0</div>', sanitize=False)
                ui.html('<div class="text-sm opacity-75">Modern Workforce Management Solution</div>', sanitize=False)