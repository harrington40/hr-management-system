from datetime import datetime
from nicegui import ui, app, context
from helperFuns import imagePath, Toggle_Boolean, get_mount_path, build_mount_route
from helperFuns.auth_storage import is_authenticated as auth_is_authenticated
from assets import SearchBox

drawerState = Toggle_Boolean()
active_Expansion_label = 'reporting'
active_item = -1
APP_MOUNT_PATH = get_mount_path()


def route(path: str) -> str:
  return build_mount_route(path, base=APP_MOUNT_PATH)

def toggle(drawer: ui.left_drawer):
    if 'mini' in drawer._props:
        drawerState.toggle()
        drawer.props(remove='mini')
    else:    
        drawerState.toggle()
        drawer.props('mini')
# 
images = {
    "administration": 'manage_accounts',
    "employees": 'groups',
    "attendance": 'fingerprint',
    # "document": imagePath('icons/document.png'),
    "reporting": 'addchart',
    "ai": 'psychology',
    "map": 'map',
}
linkData = {
  "administration": [
    {
      "id": 1,
      "label": 'Institution Profile',
      "route": route('/administration/institution')
    },
    {
      "id": 2,
      "label": 'Departmental Sections',
      "route": route('/administration/departments')
    },
    { "id": 3, "label": 'Enroll New Staff', "route": route('/administration/employee/enroll-staff')},
    {
      "id": 4,
      "label": 'Probation',
      "route": route('/administration/probation'),
    },
    {
      "id": 5,
      "label": 'Termination',
      "route": route('/administration/termination')
    },
    {
      "id": 6,
      "label": 'View Leave Requests',
      "route": route('/administration/leave/requests')
    },
    {
      "id": 7,
      "label": 'View Transfer Requests',
      "route": route('/administration/transfer/requests')
    }
  ],
  "employees": [
    {
      "id": 8,
      "label": 'Request Transfer',
      "route": route('/employees/request-transfer')
    },
    {
      "id": 9,
      "label": 'Request Leave',
      "route": route('/employees/request-leave')
    }
  ],
  "attendance": [
    { "id": 10, "label": 'Attendance Rules', "route": route('/attendance/attendance-rules')},
    {
        "id": 11,
      "label": 'Leave Rules',
      "route": route('/attendance/leave/rules')
    },
    { "id": 12, "label": 'Shift Timetable', "route": route('/attendance/timetable')},
    {
      "id": 13,
      "label": 'Set Holidays',
      "route": route('/attendance/holidays')
    },
    {
      "id": 14,
      "label": 'Staff Schedule',
      "route": route('/attendance/employee/schedule')
    },
    {
      "id": 15,
      "label": 'On Duty Status',
      "route": route('/attendance/staff/on_duty_status')
    }
  ],
  "reporting": [
    { "id": 16, "label": 'Dashboard', "route": route('/reporting/dashboard-landing')},
    { "id": 17, "label": 'Analytics', "route": route('/reporting/modern-dashboard')},
    { "id": 18, "label": 'Stats Analysis', "route": route('/reporting/dashboard')},
    { "id": 19, "label": 'Menu View', "route": route('/reporting/menu-integration')},
    { "id": 20, "label": 'Employees', "route": route('/reporting/employees')},
    { "id": 21, "label": 'Timesheet', "route": route('/reporting/employees/timesheet')},
    {
      "id": 22,
      "label": 'Administration',
      "route": route('/reporting/administration'),
      "active": False
    },
    { "id": 23, "label": 'Departments', "route": route('/reporting/departments')},
    { "id": 24, "label": 'Leaves', "route": route('/reporting/leaves')},
    { "id": 25, "label": 'Asset Inventory', "route": route('/reporting/assets')}
  ],
  "ai": [
    { "id": 27, "label": 'AI Orchestrator', "route": route('/ai/orchestrator')},
  ],
  # "map": [{ "id": 26, "label": 'View Interactive Map', "route": '/app/map'}],
}

def set_active_item(item_name):
    """Updates the active item tracker and refreshes the navigation drawer."""
    global active_item
    active_item = item_name
    navigation_menu.refresh()
    
@ui.refreshable
def navigation_menu():
  for navItem, navList in linkData.items():
    with ui.expansion(navItem.capitalize(), group='navitems', icon=images[navItem]).classes('w-full -mt-4 text-gray-200 text-[16px]').props('expand-icon-class="text-gray-200"') as expansion:
      selected_item = next((item for item in linkData[navItem] if item["id"] == active_item), None)
      if selected_item:
        expansion.set_value(True)
      main_page(navList)
  
def main_page(links: list[dict]) -> None:
    @ui.refreshable
    def list_ui():
      with ui.list().props(f'separator').classes('w-full mx-2 border-l-4 border-slate-300 pl-3'):
        for item in links:
          ui.item(item['label'], on_click=lambda i=item: {select_item(i), ui.navigate.to(i['route'])}).classes('hover:font-bold').props(f':active="{item['id'] == active_item}" active-class="text-white font-bold bg-red-400"')
           
    def select_item(selected_item):
      global active_item
      active_item = selected_item['id']
      set_active_item(active_item)
      list_ui.refresh()
    list_ui()

def Sidebar() -> None:
  client = getattr(context, 'client', None)
  storage = getattr(client, 'storage', None) if client else None
  request = getattr(client, 'request', None) if client else None
  current_path = getattr(request, 'url', None)
  if storage is not None and current_path is not None:
    if storage.get('_sidebar_rendered_path') == str(current_path):
      return
    storage['_sidebar_rendered_path'] = str(current_path)
  print('[Sidebar] render invoked')

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
  with ui.left_drawer(top_corner=True, bottom_corner=True, elevated=True).classes('mx-0 bg-gradient-to-b from-[#1c2a48] to-[#31497D] p-0') as drawer:
    # Fixed persistent branding header — no collapse/mini toggle
    with ui.row().classes('items-center gap-3 w-full px-4 py-4 bg-gradient-to-r from-[#465f9c] to-[#7283a7]'):
      ui.label('🚀').classes('text-3xl leading-none')
      with ui.column().classes('gap-0'):
        ui.label('HRMS').classes('text-white font-bold text-xl leading-tight')
        ui.label('Management System').classes('text-gray-300 text-xs leading-tight')
    navigation_menu()
  with ui.footer().style('background-color: #3874c8'):
        label = ui.label()
        ui.timer(1.0, lambda: label.set_text(f'Active Session: {datetime.now():%X}'))

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
       

    