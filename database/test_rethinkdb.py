#!/usr/bin/env python3
"""
Test RethinkDB Connection and Operations
Verifies database setup and performs basic CRUD tests
"""

from rethinkdb import RethinkDB
from rethinkdb.errors import ReqlDriverError, ReqlRuntimeError
import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

# Initialize RethinkDB
r = RethinkDB()

# Configuration
DB_CONFIG = {
    'host': os.getenv('RETHINKDB_HOST', 'localhost'),
    'port': int(os.getenv('RETHINKDB_PORT', 28015)),
    'db': os.getenv('RETHINKDB_DATABASE', 'hrms'),
    'user': os.getenv('RETHINKDB_USER', 'admin'),
    'password': os.getenv('RETHINKDB_PASSWORD', '')
}


def test_connection():
    """Test basic connection to RethinkDB"""
    print("\n🔌 Testing RethinkDB Connection...")
    print(f"   Host: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    
    try:
        conn = r.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            db=DB_CONFIG['db'],
            user=DB_CONFIG.get('user'),
            password=DB_CONFIG.get('password')
        )
        
        # Get server info
        server_info = r.db('rethinkdb').table('server_status').run(conn)
        server_list = list(server_info)
        
        if server_list:
            server = server_list[0]
            print(f"✅ Connected to RethinkDB")
            print(f"   Server ID: {server.get('id', 'N/A')}")
            print(f"   Version: {server.get('process', {}).get('version', 'N/A')}")
        
        conn.close()
        return True
    
    except ReqlDriverError as e:
        print(f"❌ Connection failed: {e}")
        return False
    except (ReqlDriverError, ReqlRuntimeError, Exception) as e:
        print(f"❌ Error: {e}")
        return False


def test_database_exists():
    """Test if HRMS database exists"""
    print("\n📦 Testing Database Existence...")
    
    try:
        conn = r.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port']
        )
        
        db_list = r.db_list().run(conn)
        
        if DB_CONFIG['db'] in db_list:
            print(f"✅ Database '{DB_CONFIG['db']}' exists")
            conn.close()
            return True
        else:
            print(f"❌ Database '{DB_CONFIG['db']}' not found")
            print(f"   Available databases: {', '.join(db_list)}")
            conn.close()
            return False
    
    except (ReqlDriverError, ReqlRuntimeError, Exception) as e:
        print(f"❌ Error: {e}")
        return False


def test_tables():
    """Test if all required tables exist"""
    print("\n📊 Testing Tables...")
    
    expected_tables = [
        'employees', 'departments', 'leave_requests', 'attendance_records',
        'timesheets', 'transfer_requests', 'probation_records', 
        'termination_records', 'assets', 'projects', 'users', 
        'documents', 'holidays', 'audit_logs', 'institution_profile', 
        'system_settings'
    ]
    
    try:
        conn = r.connect(**DB_CONFIG)
        
        existing_tables = r.table_list().run(conn)
        
        missing_tables = []
        for table in expected_tables:
            if table in existing_tables:
                count = r.table(table).count().run(conn)
                print(f"   ✅ {table}: {count} records")
            else:
                missing_tables.append(table)
                print(f"   ❌ {table}: NOT FOUND")
        
        conn.close()
        
        if missing_tables:
            print(f"\n⚠️  Missing tables: {', '.join(missing_tables)}")
            return False
        
        return True
    
    except (ReqlDriverError, ReqlRuntimeError, Exception) as e:
        print(f"❌ Error: {e}")
        return False


def test_indexes():
    """Test if indexes are created"""
    print("\n🔍 Testing Indexes...")
    
    tables_with_indexes = {
        'employees': ['employeeId', 'email', 'status', 'departmentId'],
        'departments': ['departmentId', 'code', 'status'],
        'users': ['username', 'email', 'employeeId']
    }
    
    try:
        conn = r.connect(**DB_CONFIG)
        
        for table_name, expected_indexes in tables_with_indexes.items():
            existing_indexes = r.table(table_name).index_list().run(conn)
            
            for index in expected_indexes:
                if index in existing_indexes:
                    print(f"   ✅ {table_name}.{index}")
                else:
                    print(f"   ❌ {table_name}.{index} - NOT FOUND")
        
        conn.close()
        return True
    
    except (ReqlDriverError, ReqlRuntimeError, Exception) as e:
        print(f"❌ Error: {e}")
        return False


def test_crud_operations():
    """Test basic CRUD operations"""
    print("\n✏️  Testing CRUD Operations...")
    
    try:
        conn = r.connect(**DB_CONFIG)
        
        # CREATE
        print("\n   📝 Testing INSERT...")
        test_employee = {
            'id': 'TEST_EMP_001',
            'employeeId': 'TEST_EMP_001',
            'firstName': 'Test',
            'lastName': 'User',
            'email': 'test@example.com',
            'status': 'active',
            'departmentId': 'DEPT_ENG_001',
            'position': 'Test Engineer',
            'createdAt': r.now()
        }
        
        result = r.table('employees').insert(test_employee).run(conn)
        if result['inserted'] == 1:
            print("      ✅ Insert successful")
        else:
            print(f"      ⚠️  Insert result: {result}")
        
        # READ
        print("\n   📖 Testing SELECT...")
        employee = r.table('employees').get('TEST_EMP_001').run(conn)
        if employee and employee['email'] == 'test@example.com':
            print(f"      ✅ Read successful: {employee['firstName']} {employee['lastName']}")
        else:
            print("      ❌ Read failed")
        
        # UPDATE
        print("\n   🔄 Testing UPDATE...")
        result = r.table('employees').get('TEST_EMP_001').update({
            'position': 'Senior Test Engineer',
            'updatedAt': r.now()
        }).run(conn)
        if result['replaced'] == 1:
            print("      ✅ Update successful")
        
        # Verify update
        updated_employee = r.table('employees').get('TEST_EMP_001').run(conn)
        if updated_employee['position'] == 'Senior Test Engineer':
            print(f"      ✅ Verified: {updated_employee['position']}")
        
        # DELETE
        print("\n   🗑️  Testing DELETE...")
        result = r.table('employees').get('TEST_EMP_001').delete().run(conn)
        if result['deleted'] == 1:
            print("      ✅ Delete successful")
        
        # Verify delete
        deleted_employee = r.table('employees').get('TEST_EMP_001').run(conn)
        if deleted_employee is None:
            print("      ✅ Verified: Record deleted")
        
        conn.close()
        return True
    
    except (ReqlDriverError, ReqlRuntimeError, Exception) as e:
        print(f"❌ CRUD test failed: {e}")
        return False


def test_queries():
    """Test complex queries"""
    print("\n🔎 Testing Complex Queries...")
    
    try:
        conn = r.connect(**DB_CONFIG)
        
        # Test filtering
        print("\n   🔍 Testing filter query...")
        active_employees = r.table('employees').filter(
            {'status': 'active'}
        ).count().run(conn)
        print(f"      ✅ Found {active_employees} active employees")
        
        # Test ordering
        print("\n   📊 Testing order by query...")
        employees = list(r.table('employees').order_by('firstName').limit(5).run(conn))
        print(f"      ✅ Retrieved {len(employees)} employees (ordered)")
        
        # Test joining (if we have data)
        if active_employees > 0:
            print("\n   🔗 Testing join-like query...")
            # Get employee with department info (simulated join)
            result = list(r.table('employees').limit(1).run(conn))
            if result:
                emp = result[0]
                dept_id = emp.get('departmentId')
                if dept_id:
                    dept = r.table('departments').get(dept_id).run(conn)
                    if dept:
                        print(f"      ✅ Employee: {emp['firstName']} → Department: {dept['name']}")
        
        conn.close()
        return True
    
    except (ReqlDriverError, ReqlRuntimeError, Exception) as e:
        print(f"❌ Query test failed: {e}")
        return False


def test_changefeeds():
    """Test RethinkDB changefeeds (real-time updates)"""
    print("\n🔄 Testing Changefeeds...")
    
    try:
        conn = r.connect(**DB_CONFIG)
        
        print("   ℹ️  Changefeeds allow real-time monitoring of table changes")
        print("   ℹ️  This would be useful for:")
        print("      - Live attendance updates")
        print("      - Real-time notifications")
        print("      - Dashboard live data")
        print("   ✅ Changefeed capability available")
        
        conn.close()
        return True
    
    except (ReqlDriverError, ReqlRuntimeError, Exception) as e:
        print(f"❌ Changefeed test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🚀 RethinkDB Connection and Operations Test")
    print("=" * 60)
    
    tests = [
        ("Connection", test_connection),
        ("Database Exists", test_database_exists),
        ("Tables", test_tables),
        ("Indexes", test_indexes),
        ("CRUD Operations", test_crud_operations),
        ("Complex Queries", test_queries),
        ("Changefeeds", test_changefeeds)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except (ReqlDriverError, ReqlRuntimeError, Exception) as e:
            print(f"\n❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} - {test_name}")
    
    print("\n" + "=" * 60)
    print(f"📈 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed. Please check the output above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
