from nicegui import ui, context, app
from helperFuns import imagePath, Toggle_Boolean
from assets import SearchBox

# Global state management for menu items
class MenuState:
    def __init__(self):
        self.active_item_id = None
        self.menu_items = {}  # Store references to menu items
        
    def set_active(self, item_id):
        """Set the active menu item and update all menu items"""
        # Store the active item in persistent storage
        try:
            app.storage.user['active_menu_item'] = item_id
        except:
            pass
            
        # Reset all items to inactive (remove red background)
        for menu_id, item_ref in self.menu_items.items():
            if item_ref:
                try:
                    # Remove active state classes
                    item_ref.classes(remove='bg-red-500 text-white font-bold border-l-4 border-red-200')
                    item_ref.classes(remove='bg-red-400')
                    # Reset to default colors
                    item_ref.classes(add='text-gray-200')
                except Exception as e:
                    print(f"Error resetting menu item {menu_id}: {e}")
                
        # Set the clicked item as active (add red background)
        self.active_item_id = item_id
        if item_id in self.menu_items and self.menu_items[item_id]:
            try:
                # Remove default colors first
                self.menu_items[item_id].classes(remove='text-gray-200')
                # Add active state classes
                self.menu_items[item_id].classes(add='bg-red-500 text-white font-bold border-l-4 border-red-200')
                print(f"Set menu item {item_id} as active")
            except Exception as e:
                print(f"Error setting active menu item {item_id}: {e}")
            
    def register_item(self, item_id, item_ref):
        """Register a menu item with the state manager"""
        self.menu_items[item_id] = item_ref
        print(f"Registered menu item {item_id}: {item_ref}")
        
        # Check if this item should be active based on stored state
        try:
            stored_active_item = app.storage.user.get('active_menu_item')
            if stored_active_item == item_id:
                # This item should be active, apply styling
                item_ref.classes(remove='text-gray-200')
                item_ref.classes(add='bg-red-500 text-white font-bold border-l-4 border-red-200')
                self.active_item_id = item_id
                print(f"Restored active state for menu item {item_id}")
        except Exception as e:
            print(f"Error checking stored active state: {e}")
        
    def is_active(self, item_id):
        """Check if an item is currently active"""
        return self.active_item_id == item_id
        
    def get_stored_active_item(self):
        """Get the active item from storage"""
        try:
            return app.storage.user.get('active_menu_item')
        except:
            return None

# Create global menu state instance
menu_state = MenuState()

# validate_magic_link()
drawerState = Toggle_Boolean()
def toggle(drawer: ui.left_drawer):
    if 'mini' in drawer._props:
        drawerState.toggle()
        drawer.props(remove='mini')
    else:    
        drawerState.toggle()
        drawer.props('mini')
images = {
    "administration": 'manage_accounts',
    "employees": 'groups',
    "attendance": 'fingerprint',
    # "business": 'price_change',
    # "document": imagePath('icons/document.png'),
    # "request": imagePath('icons/request.png'),
    # "assets": imagePath('icons/assets.png'),
    "reporting": 'addchart',
    # "lookup": imagePath('icons/lookup.png'),
    "map": 'map',
    # "guide": imagePath('icons/guide.png')
}
linkData = {
  "administration": [
    {
      "id": 1,
      "label": 'Institution Profile',
      "route": '/hrmkit/administration/institution'
    },
    {
      "id": 2,
      "label": 'Departmental Sections',
      "route": '/hrmkit/administration/departments'
    },
    { "id": 3, "label": 'Enroll New Staff', "route": '/hrmkit/administration/enroll-staff' },
    {
      "id": 4,
      "label": 'Probation',
      "route": '/hrmkit/administration/probation'
    },
    {
      "id": 5,
      "label": 'Termination',
      "route": '/hrmkit/administration/termination'
    },
    {
      "id": 6,
      "label": 'View Leave Requests',
      "route": '/hrmkit/employees/request-leave'
    },
    {
      "id": 7,
      "label": 'View Transfer Requests',
      "route": '/hrmkit/employees/request-transfer'
    }
  ],
  "employees": [
    {
      "id": 8,
      "label": 'Request Transfer',
      "route": '/hrmkit/employees/request-transfer'
    },
    {
      "id": 9,
      "label": 'Request Leave',
      "route": '/hrmkit/employees/request-leave'
    }
  ],
  "attendance": [
    { "id": 10, "label": 'Attendance Rules', "route": '/hrmkit/attendance/attendance' },
    {
        "id": 11,
      "label": 'Leave Rules',
      "route": '/hrmkit/attendance/leave/rules'
    },
    { "id": 12, "label": 'Shift Timetable', "route": '/hrmkit/attendance/timetable' },
    {
        "id": 13,
      "label": 'Set Holidays',
      "route": '/hrmkit/attendance/holidays'
    },
    {
        "id": 14,
      "label": 'Staff Schedule',
      "route": '/hrmkit/attendance/staff_schedule'
    },
    {
        "id": 15,
      "label": 'Staff & On Duty Status',
      "route": '/hrmkit/attendance/staff_status'
    }
  ],
#   "business": [
#     { "label": 'Cash Receipt', "route": '/ktimas/business/cash' },
#     { "label": 'Bank Deposit', "route": '/ktimas/business/deposit' },
#     { "label": 'Manage Payroll', "route": '/ktimas/business/payroll' },
#     { "label": 'Process Salary', "route": '/ktimas/business/salary' },
#     { "label": 'Pay Adjustment & Overtime', "route": '/ktimas/business/salary' },
#     { "label": 'Other Payments', "route": '/ktimas/business/salary' },
#     { "label": 'Manage Expenses', "route": '/ktimas/business/expense' },
#     {
#       "label": 'Purchase Request',
#       "route": '/ktimas/business/request'
#     }
#   ],
#   "document": [
#     { "label": 'Institutional Policy', "route": '/ktimas/document/policy' },
#     { "label": 'Tax Form', "route": '/ktimas/document/tax' },
#     { "label": 'Social Security Form', "route": '/ktimas/document/social' },
#     {
#       "label": 'Benefit Application Form',
#       "route": '/ktimas/document/benefit'
#     },
#     { "label": 'Training Resources', "route": '/ktimas/document/training' },
#     { "label": 'Create Report', "route": '/ktimas/document/report' }
#   ],
#   "request": [
#     { "label": 'Leave Request', "route": '/ktimas/request/leave' },
#     { "label": 'Time-off Request', "route": '/ktimas/request/timeoff' },
#     { "label": 'Transfer Request', "route": '/ktimas/request/transfer' },
#     { "label": 'Resignation', "route": '/ktimas/request/resignation' }
#   ],
#   "assets": [
#     { "label": 'New Asset', "route": '/ktimas/assets/new' },
#     { "label": 'Assign Assets', "route": '/ktimas/assets/assign' },
#     { "label": 'Track Repairs', "route": '/ktimas/assets/repair' },
#     { "label": 'Retrieve Assets', "route": '/ktimas/assets/retrieve' },
#     { "label": 'Dispose Assets', "route": '/ktimas/assets/dispose' },
#     { "label": 'Inventories', "route": '/ktimas/assets/inventory' }
#   ],
  "reporting": [
    { "id": 16, "label": 'Dashboard', "route": '/ktimas/reporting/dashboard' },
    { "id": 17, "label": 'Employees', "route": '/ktimas/reporting/employees' },
    { "id": 18, "label": 'Timesheet', "route": '/ktimas/reporting/timesheet' },
    {
        "id": 19,
      "label": 'Administration',
      "route": '/ktimas/reporting/administration'
    },
    {
        "id": 20,
      "label": 'Bank Balances',
      "route": '/ktimas/reporting/bank'
    },
    { "id": 21, "label": 'Expenditure', "route": '/ktimas/reporting/expenditure' },
    { "id": 22, "label": 'Departments', "route": '/ktimas/reporting/departments' },
    { "id": 23, "label": 'Leaves', "route": '/ktimas/reporting/leaves' },
    { "id": 24, "label": 'Asset Inventory', "route": '/ktimas/reporting/asset' }
  ],
#   "lookup": [
#     { "label": 'Add Bank', "route": '/ktimas/lookup/bank_names/1' },
#     { "label": 'Add Department', "route": '/ktimas/lookup/department/2' },
#     { "label": 'Add Asset', "route": '/ktimas/lookup/assets/7' },
#     { "label": 'Add Building', "route": '/ktimas/lookup/building/8' },
#     { "label": 'Room Number', "route": '/ktimas/lookup/room_number/6' },
#     { "label": 'Leave Type', "route": '/ktimas/lookup/leave_type/3' },
#     { "label": 'Position', "route": '/ktimas/lookup/position/4' },
#     { "label": 'Salary Grade', "route": '/ktimas/lookup/salary' }
#   ],
  "map": [{ "id": 25, "label": 'View Interactive Map', "route": '/ktimas/map' }],
#   "guide": [
#     { "label": 'User Guide', "route": '/ktimas/guide/map' },
#     { "label": 'Employee Handbook', "route": '/ktimas/guide/handbook' }
#   ]
}

def Sidebar():
    # Detect current page to set active menu item
    try:
        from nicegui import context
        current_path = getattr(context.client, 'page_route', '') if hasattr(context, 'client') and context.client else ''
        print(f"Current page route: {current_path}")
        
        # Map current path to menu item ID
        path_to_menu_id = {
            '/hrmkit/administration/departments': 2,
            '/hrmkit/administration/enroll-staff': 3,
            '/hrmkit/administration/probation': 4,
            '/hrmkit/administration/termination': 5,
            '/hrmkit/employees/request-leave': 9,  # For both admin view and employee request
            '/hrmkit/employees/request-transfer': 8,  # For both admin view and employee request
            '/hrmkit/attendance/attendance': 10,
            '/hrmkit/attendance/leave/rules': 11,
            '/hrmkit/attendance/timetable': 12,
            '/hrmkit/attendance/holidays': 13,
            '/hrmkit/attendance/staff_schedule': 14,
            '/hrmkit/attendance/staff_status': 15,
        }
        
        # Set the menu item as active based on current page
        for path, menu_id in path_to_menu_id.items():
            if path in current_path:
                try:
                    app.storage.user['active_menu_item'] = menu_id
                    print(f"Set active menu item {menu_id} for path {current_path}")
                except:
                    pass
                break
    except Exception as e:
        print(f"Error detecting current page: {e}")
    
    with ui.header(elevated=True).classes('bg-gradient-to-r from-[#7283a7] to-[#2e3951] py-2'):
        SearchBox()
        with ui.row().classes('justify-between items-center w-full'):
             with ui.element('div').classes('searchWrapper') as div:
                 with ui.element('div').classes('inputHolder'):
                     ui.element('input').classes('searchInput searchPlaceholder').props('placeholder="Search employees here..." type="text"')
                     with ui.element('button').classes('searchIcon').on('click', lambda: handleOpenSearch(div, btn)) as btn:
                        ui.element('span')
                 ui.element('button').classes('close').on('click', lambda: handleCloseSearch(div, btn))
             mobileToggleBtn = ui.button(icon='menu_open', on_click=lambda: handleDrawerToggle(drawer, mobileToggleBtn)).props('flat color=white size="26px" padding="none" dense round unelevated').classes('sm:hidden')
             with ui.row().classes('flex justify-end'):
                with ui.avatar(color='white', size='xl') as avatar:
                    ui.image(f'{imagePath('blank-silhouette.jpg')}')
                    with ui.menu().props('transition-show="scale" transition-hide="scale" dense :offset="[0, 9]" bordered separator') as menu:
                        avatar.on ('mouseenter', lambda : menu.open ())
                        menu.on ('mouseleave', lambda : menu.close ())
                        with ui.list().props('bordered separator'):
                            with ui.item(on_click=lambda: { ui.notify('You clicked manage account'), menu.close()}).classes('hover:font-bold transition delay-150 duration-200 ease-in-out hover:translate-1 hover:scale-105'):
                                with ui.item_section().props('side'):
                                    ui.icon('manage_accounts').classes('text-blue-600 text-2xl')
                                with ui.item_section():
                                    ui.item_label('Account Profile')
                            with ui.item(on_click=lambda: {ui.notify('You clicked change password'), menu.close()}).classes('hover:font-bold transition delay-150 duration-200 ease-in-out hover:translate-1 hover:scale-105'):
                                with ui.item_section().props('side'):
                                    ui.icon('key').classes('text-green-600 text-2xl')
                                with ui.item_section():
                                    ui.item_label('Change Password')
                            with ui.item(on_click=lambda: {ui.notify('You clicked log out'), menu.close()}).classes('hover:font-bold transition delay-150 duration-200 ease-in-out hover:translate-1 hover:scale-105'):
                                with ui.item_section().props('side'):
                                    ui.icon('logout').classes('text-red-600 text-2xl')
                                with ui.item_section():
                                    ui.item_label('Log Out')
                with ui.column().classes('items-start pr-5'):
                    ui.label('Yarkpawolo Kulobo').classes('text-white font-bold text-lg -mb-5')
                    ui.label('KWARECOM Developer').classes('text-stone-200 text-sm')
    with ui.left_drawer(top_corner=True, bottom_corner=True, elevated=True, ).classes('mx-0 bg-gradient-to-b from-[#1c2a48] to-[#31497D] p-0') as drawer:
        with ui.row().classes('flex justify-between items-center bg-gradient-to-r from-[#465f9c] to-[#7283a7] w-full px-[0.35rem] py-[0.40rem]').bind_visibility_from(drawerState, 'visible'):
            with ui.avatar(color='white', size='xl'):
                ui.image(f'{imagePath('logo.png')}')
            ui.button(on_click=lambda: toggle(drawer)).props('icon=menu flat color=white size="xl" padding="xs" dense round unelevated')
        with ui.column().classes('flex justify-between items-center bg-gradient-to-r from-[#465f9c] to-[#7283a7] w-full p-[0.35rem]').bind_visibility_from(drawerState, 'is_visible'):
            ui.button(on_click=lambda: toggle(drawer)).props('icon=clear flat color=white size="xl" padding="none" dense round unelevated')
        
        # with ui.column().classes('px-2'):
        for navItem, navList in linkData.items():
            with ui.expansion(navItem.capitalize(), group='navitems', icon=images[navItem], on_value_change=lambda: expansion_state(expan)).classes('w-full -mt-4 text-gray-200 text-[16px]').props('expand-icon-class="text-gray-200"') as expan:
                with ui.list().props(f'separator :tabindex={navItem}').classes('w-full mx-2 border-l-4 border-slate-300 pl-3'):
                    for nav in navList:
                        # Create a closure to capture the current nav item
                        def create_menu_item(nav_item):
                            item_id = nav_item['id']
                            item_label = nav_item['label']
                            item_route = nav_item['route']
                            
                            # Create the menu item with proper click handler and initial styling
                            list_item = ui.item(
                                item_label, 
                                on_click=lambda nav=nav_item: handle_menu_click(nav['id'], nav['label'], nav['route'])
                            ).classes('hover:font-bold transition-all duration-300 ease-in-out cursor-pointer rounded-md mx-1 px-2 py-1 text-gray-200 hover:bg-gray-700')
                            
                            # Register the item with the state manager
                            menu_state.register_item(item_id, list_item)
                            print(f"Created menu item: {item_id} - {item_label}")
                            return list_item
                            
                        # Create the menu item
                        create_menu_item(nav)
        # with ui.expansion('Test 1', caption='Handle administrative tasks', icon='work', on_value_change=lambda: expansion_state(exp)).classes('w-full') as exp:
        #     with ui.list().props('dense separator').classes('w-full mx-2 border-l-4 border-slate-300 -mt-4 pl-3'):
        #         Profile = ui.item('Institution Profile', on_click=lambda: {ui.notify('You clicked Institution Profile'), listItem_state(Profile)}).classes('hover:font-bold').props(f':tabindex="{105}" :active="{print('isActive') if isActive == 105 else print(isActive)}" active-class="text-white font-bold bg-red-400"').bind_visibility_from(drawerState, 'isActive')
        #         Sections = ui.item('Departmental Sections', on_click=lambda: {ui.notify('You clicked Departmental Sections'), listItem_state(Sections)}).classes('hover:font-bold').props(f':tabindex="{107}" :active="{True if isActive == 107 else print(isActive)}" active-class="text-white font-bold bg-red-400"')
        #         Staff = ui.item('Enroll New Staff', on_click=lambda: ui.notify('You clicked Enroll New Staff')).classes('hover:font-bold')
        #         Probation = ui.item('Probation', on_click=lambda: ui.notify('You clicked Probation')).classes('hover:font-bold')
        #         Termination = ui.item('Termination', on_click=lambda: ui.notify('You clicked Termination')).classes('hover:font-bold')
        #         Leave = ui.item('View Leave Requests', on_click=lambda: ui.notify('You clicked View Leave Requests')).classes('hover:font-bold')
        #         Transfer = ui.item('View Transfer Requests', on_click=lambda: ui.notify('You clicked View Transfer Requests')).classes('hover:font-bold')
        # with ui.expansion('Employees 2', caption='Handle administrative tasks', on_value_change=lambda: print(ex)).classes('w-full') as ex:
        #      with ui.list().props('dense separator').classes('w-full mx-2 border-l-4 border-slate-300 -mt-4 pl-3'):
        #         Probation1 = ui.item('Probation', on_click=lambda: ui.notify('You clicked Probation')).classes('hover:font-bold')
        #         Termination1 = ui.item('Termination', on_click=lambda: ui.notify('You clicked Termination')).classes('hover:font-bold')
        #         Leave1 = ui.item('View Leave Requests', on_click=lambda: ui.notify('You clicked View Leave Requests')).classes('hover:font-bold')
    with ui.footer().style('background-color: #3874c8'):
        ui.label('HRMkit - HR Management System').classes('text-white text-sm')
    
def handle_menu_click(item_id, item_label, item_route):
    """Handle menu item click - update state and navigate"""
    print(f'Menu clicked: ID={item_id}, Label={item_label}, Route={item_route}')
    
    # Update the active state BEFORE navigation
    menu_state.set_active(item_id)
    
    # Show notification
    ui.notify(f'You clicked {item_label}', color='positive')
    
    # Navigate to route with proper routing logic
    try:
        if item_route == '/hrmkit/administration/institution':
            ui.navigate.to('/administration/institution')
        elif item_route == '/hrmkit/administration/departments':
            ui.navigate.to('/administration/departments')
        elif item_route == '/hrmkit/administration/enroll-staff':
            ui.navigate.to('/administration/enroll-staff')
        elif item_route == '/hrmkit/administration/probation':
            ui.navigate.to('/administration/probation')
        elif item_route == '/hrmkit/administration/termination':
            ui.navigate.to('/administration/termination')
        elif item_route == '/hrmkit/employees/request-transfer':
            ui.navigate.to('/employees/request-transfer')
        elif item_route == '/hrmkit/employees/request-leave':
            ui.navigate.to('/employees/request-leave')
        elif item_route == '/hrmkit/attendance/attendance':
            ui.navigate.to('/attendance/attendance')
        elif item_route == '/hrmkit/attendance/leave/rules':
            ui.navigate.to('/attendance/leave/rules')
        elif item_route == '/hrmkit/attendance/timetable':
            ui.navigate.to('/attendance/timetable')
        elif item_route == '/hrmkit/attendance/holidays':
            ui.navigate.to('/attendance/holidays')
        elif item_route == '/hrmkit/attendance/staff_schedule':
            ui.navigate.to('/attendance/staff_schedule')
        elif item_route == '/hrmkit/attendance/staff_status':
            ui.navigate.to('/attendance/staff_status')
        elif 'reporting' in item_route:
            ui.navigate.to('/dashboard')  # For now, redirect reporting to dashboard
        else:
            ui.notify(f'Page under development: {item_label}', color='info')
            return  # Don't navigate if page doesn't exist
    except Exception as e:
        print(f"Navigation error: {e}")
        ui.notify(f'Navigation error: {e}', color='negative')
        return
    
    print(f'Successfully navigated to: {item_route}')
    print(f'Active menu items: {list(menu_state.menu_items.keys())}')
    print(f'Current active item: {menu_state.active_item_id}')

def toggle(drawer: ui.left_drawer):
    if 'mini' in drawer._props:
        drawerState.toggle()
        drawer.props(remove='mini')
    else:    
        drawerState.toggle()
        drawer.props('mini')

def handleDrawerToggle(drawer: ui.left_drawer, btn: ui.button):
    drawer.toggle()
    if not drawerState.isChecked:
        btn.classes(remove='rotate-0')
        btn.classes(add='rotate-180')
        drawerState.isChecked = True
    else:
        btn.classes(remove='rotate-180')
        btn.classes(add='rotate-0')
        drawerState.isChecked = False

def handleCloseSearch(div: ui.element, btn: ui.element):
    div.classes(remove='active')
    btn.classes(remove='activeIcon')

def handleOpenSearch(div: ui.element, btn: ui.element):
    div.classes(add='active')
    btn.classes(add='activeIcon')
       
def expansion_state(val: ui.expansion):
    print(f'Expansion state changed: {val.text}')