from nicegui import ui, APIRouter, context
from ..components import Login_Page

router = APIRouter(prefix='/hrmkit')

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
    
# @router.page('/reporting/dashboard')
# def admin_dashboard():
#         ui.label('Welcome to the Dashboard!').classes('text-2xl font-bold')
#         # Sidebar()
# @router.page('/staffing/leave/request')
# def admin_settings():
#     ui.label('Welcome to the Staff Leave Page!').classes('text-2xl font-bold')
# @router.page('/staffing/transfer/request')
# def admin_settings():
#     ui.label('Welcome to the Staff Transfer Page!').classes('text-2xl font-bold')

# ui.label('This is a label outside of any page').classes('text-2xl font-bold text-red-400')
# from typing import Callable


