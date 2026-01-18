#!/usr/bin/env python3

"""
Test script to check if we can reproduce the AttributeError
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from nicegui import ui
from components.attendance.set_holidays import HolidaysManager, SetHolidays

@ui.page('/test_holidays')
def test_holidays_page():
    try:
        ui.label('Testing Holidays Page...')
        
        # Test HolidaysManager creation
        manager = HolidaysManager()
        ui.label(f'✅ HolidaysManager created - loaded {len(manager.holidays_data.get("holidays_calendar", {}).get("fixed_holidays_2025", []))} fixed holidays')
        
        # Try to create the holidays page
        ui.label('Creating SetHolidays component...')
        SetHolidays()
        ui.label('✅ SetHolidays component created successfully')
        
    except Exception as e:
        ui.label(f'❌ Error: {str(e)}').classes('text-red-500')
        import traceback
        ui.html(f'<pre>{traceback.format_exc()}</pre>').classes('text-red-500 bg-red-50 p-4')

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(port=8081)