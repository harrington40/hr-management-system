#!/usr/bin/env python3
"""
Simple authentication test
"""

from nicegui import ui, app
from components.attendance.set_holidays import SetHolidays

@ui.page('/test-auth')  
def test_auth_page():
    # Bypass authentication for testing
    app.storage.user['authenticated'] = True
    ui.label('Authentication bypassed for testing').classes('text-green-600 font-bold')
    ui.label('Attempting to load SetHolidays component...').classes('mt-4')
    
    try:
        SetHolidays()
        ui.label('✅ SetHolidays loaded successfully!').classes('text-green-600 font-bold mt-4')
    except Exception as e:
        ui.label(f'❌ Error loading SetHolidays: {str(e)}').classes('text-red-600 font-bold mt-4')

if __name__ == "__main__":
    ui.run(host="0.0.0.0", port=8082)