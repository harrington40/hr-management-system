#!/usr/bin/env python3
"""
Test RethinkDB Service Integration
Verifies the RethinkDB service can connect and perform operations
"""

import sys
from services.rethinkdb_service import rethinkdb_service

def test_connection():
    """Test basic connection"""
    print("\n🔌 Testing RethinkDB Connection...")
    if rethinkdb_service.connect():
        print("✅ Connection successful")
        return True
    else:
        print("❌ Connection failed")
        return False

def test_user_operations():
    """Test user operations"""
    print("\n👤 Testing User Operations...")
    
    # Get admin user by email
    user = rethinkdb_service.get_user_by_email("admin@hrmkit.com")
    if user:
        print(f"✅ Found admin user:")
        print(f"   Username: {user.get('username')}")
        print(f"   Email: {user.get('email')}")
        print(f"   Employee ID: {user.get('employeeId')}")
        print(f"   Role: {user.get('role')}")
        print(f"   Active: {user.get('isActive')}")
        return True
    else:
        print("❌ Admin user not found")
        return False

def test_employee_operations():
    """Test employee operations"""
    print("\n👥 Testing Employee Operations...")
    
    # Get all employees
    employees = rethinkdb_service.get_all_employees()
    print(f"✅ Found {len(employees)} employee(s)")
    
    if employees:
        emp = employees[0]
        print(f"   Sample: {emp.get('firstName')} {emp.get('lastName')} ({emp.get('id')})")
        
        # Get specific employee
        employee = rethinkdb_service.get_employee(emp.get('id'))
        if employee:
            print(f"✅ Retrieved employee by ID: {employee.get('id')}")
        return True
    return True

def test_department_operations():
    """Test department operations"""
    print("\n🏢 Testing Department Operations...")
    
    departments = rethinkdb_service.get_all_departments()
    print(f"✅ Found {len(departments)} department(s)")
    
    if departments:
        dept = departments[0]
        print(f"   Sample: {dept.get('departmentName')} ({dept.get('id')})")
    return True

def test_system_settings():
    """Test system settings"""
    print("\n⚙️  Testing System Settings...")
    
    settings = rethinkdb_service.get_system_settings()
    if settings:
        print(f"✅ Retrieved system settings")
        print(f"   Institution: {settings.get('institutionName', 'N/A')}")
        return True
    else:
        print("⚠️  No system settings found")
        return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("RethinkDB Service Integration Test")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Connection", test_connection()))
    
    if results[0][1]:  # If connection succeeded
        results.append(("User Operations", test_user_operations()))
        results.append(("Employee Operations", test_employee_operations()))
        results.append(("Department Operations", test_department_operations()))
        results.append(("System Settings", test_system_settings()))
    
    # Close connection
    rethinkdb_service.disconnect()
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    print("=" * 60)
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
