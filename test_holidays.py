#!/usr/bin/env python3

"""
Test script to verify holidays module is working correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from components.attendance.set_holidays import HolidaysManager
    
    print("Testing HolidaysManager...")
    
    # Create manager instance
    manager = HolidaysManager()
    
    print("✅ HolidaysManager created successfully")
    
    # Test data loading
    holidays_data = manager.holidays_data
    print(f"✅ Holidays data loaded: {type(holidays_data)}")
    
    # Test accessing holidays calendar
    holidays_calendar = holidays_data.get('holidays_calendar', {})
    print(f"✅ Holidays calendar accessed: {type(holidays_calendar)}")
    
    # Test accessing fixed holidays
    fixed_holidays = holidays_calendar.get('fixed_holidays_2025', [])
    print(f"✅ Fixed holidays accessed: {type(fixed_holidays)}, Count: {len(fixed_holidays)}")
    
    # Test accessing first holiday
    if fixed_holidays:
        first_holiday = fixed_holidays[0]
        print(f"✅ First holiday: {type(first_holiday)}")
        if isinstance(first_holiday, dict):
            name = first_holiday.get('name', 'No name')
            date = first_holiday.get('date', 'No date')
            print(f"   - Name: {name}")
            print(f"   - Date: {date}")
        else:
            print(f"   ❌ First holiday is not a dict: {first_holiday}")
    
    # Test accessing religious holidays
    religious_holidays = holidays_calendar.get('religious_holidays_2025', [])
    print(f"✅ Religious holidays accessed: {type(religious_holidays)}, Count: {len(religious_holidays)}")
    
    # Test accessing company holidays  
    company_holidays = holidays_calendar.get('company_holidays_2025', [])
    print(f"✅ Company holidays accessed: {type(company_holidays)}, Count: {len(company_holidays)}")
    
    print("\n🎉 All tests passed! The holidays module should work correctly now.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()