#!/usr/bin/env python3
"""
Simple test for holidays page rendering
"""

from nicegui import ui, app
import uvicorn

def SimpleHolidays():
    """Very simple holidays page to test rendering"""
    ui.label('🎉 Simple Holiday Test Page').classes('text-2xl font-bold text-center')
    ui.label('This is a test to see if the page renders correctly').classes('text-center mt-4')
    
    with ui.row().classes('w-full justify-center mt-8'):
        ui.button('Test Button', on_click=lambda: ui.notify('Test successful!')).classes('bg-blue-500 text-white px-4 py-2 rounded')

@ui.page('/test-holidays')
def simple_holidays_page():
    SimpleHolidays()

if __name__ in {"__main__", "__mp_main__"}:
    uvicorn.run("test_simple_holidays:app", host="0.0.0.0", port=8081, reload=True)