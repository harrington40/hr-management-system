#!/usr/bin/env python3
"""
HRMS OrientDB Database Connection Test
Tests database connectivity and basic operations
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    import orientdb
    from orientdb.client import OrientDB
except ImportError:
    print("❌ Error: orientdb-python not installed")
    print("Install with: pip install orientdb-python")
    sys.exit(1)

import os
import time
from datetime import datetime, date

def get_db_config():
    """Get database configuration"""
    return {
        'host': os.getenv('ORIENTDB_HOST', 'localhost'),
        'port': int(os.getenv('ORIENTDB_PORT', 2424)),
        'user': os.getenv('ORIENTDB_USER', 'root'),
        'password': os.getenv('ORIENTDB_PASSWORD', 'root'),
        'database': os.getenv('ORIENTDB_DATABASE', 'hrms_db')
    }

def test_connection(config):
    """Test basic OrientDB connection"""
    try:
        print("🔌 Testing OrientDB connection...")
        client = OrientDB(host=config['host'], port=config['port'])
        client.connect(user=config['user'], password=config['password'])

        # Get server info
        info = client.get_server_info()
        version = info.get('version', 'unknown')
        print(f"✅ Connected to OrientDB Server version {version}")

        # Test database connection
        db = client.open_database(
            name=config['database'],
            user=config['user'],
            password=config['password']
        )

        # Simple test query
        result = db.query("SELECT 1 as test")
        if result and result[0].get('test') == 1:
            print("✅ Database query test passed")
        else:
            print("⚠️  Database query test failed")

        db.close()
        client.close()
        return True

    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_basic_queries(config):
    """Test basic database queries"""
    client = None
    db = None
    try:
        print("\n📊 Testing basic queries...")
        client = OrientDB(host=config['host'], port=config['port'])
        client.connect(user=config['user'], password=config['password'])
        db = client.open_database(
            name=config['database'],
            user=config['user'],
            password=config['password']
        )

        # Test user count
        result = db.query("SELECT COUNT(*) as user_count FROM User")
        user_count = result[0].get('user_count', 0) if result else 0
        print(f"   👥 Total users: {user_count}")

        # Test department count
        result = db.query("SELECT COUNT(*) as dept_count FROM Department")
        dept_count = result[0].get('dept_count', 0) if result else 0
        print(f"   🏢 Total departments: {dept_count}")

        # Test leave types
        result = db.query("SELECT name, days_per_year FROM LeaveType WHERE is_active = true")
        leave_types = result if result else []
        print(f"   📅 Leave types: {len(leave_types)}")
        for leave in leave_types[:3]:  # Show first 3
            print(f"      - {leave.get('name', 'Unknown')}: {leave.get('days_per_year', 0)} days")

        # Test shift templates
        result = db.query("SELECT name, start_time, end_time FROM ShiftTemplate WHERE is_active = true LIMIT 3")
        shifts = result if result else []
        print(f"   ⏰ Active shifts: {len(shifts)}")
        for shift in shifts:
            print(f"      - {shift.get('name', 'Unknown')}: {shift.get('start_time', 'N/A')} - {shift.get('end_time', 'N/A')}")

        db.close()
        client.close()
        return True

    except Exception as e:
        print(f"❌ Query error: {e}")
        if db:
            try:
                db.close()
            except:
                pass
        if client:
            try:
                client.close()
            except:
                pass
        return False

def test_data_integrity(config):
    """Test referential integrity and data consistency"""
    client = None
    db = None
    try:
        print("\n🔗 Testing data integrity...")
        client = OrientDB(host=config['host'], port=config['port'])
        client.connect(user=config['user'], password=config['password'])
        db = client.open_database(
            name=config['database'],
            user=config['user'],
            password=config['password']
        )

        all_passed = True

        # Test for users with invalid roles
        result = db.query("SELECT COUNT(*) as count FROM User WHERE role NOT IN ['admin', 'manager', 'employee']")
        invalid_roles = result[0].get('count', 0) if result else 0
        if invalid_roles > 0:
            print(f"   ❌ Users with invalid roles: {invalid_roles}")
            all_passed = False
        else:
            print("   ✅ User roles: OK")

        # Test for employees without departments (should be allowed in graph model)
        result = db.query("SELECT COUNT(*) as count FROM Employee WHERE department_id IS NULL")
        no_dept = result[0].get('count', 0) if result else 0
        print(f"   ℹ️  Employees without department: {no_dept} (OK in graph model)")

        # Test for leave requests with invalid status
        result = db.query("SELECT COUNT(*) as count FROM LeaveRequest WHERE status NOT IN ['pending', 'approved', 'rejected', 'cancelled']")
        invalid_status = result[0].get('count', 0) if result else 0
        if invalid_status > 0:
            print(f"   ❌ Leave requests with invalid status: {invalid_status}")
            all_passed = False
        else:
            print("   ✅ Leave request status: OK")

        # Test for orphaned attendance records
        result = db.query("""
            SELECT COUNT(*) as count FROM AttendanceRecord
            WHERE employee_id NOT IN (SELECT @rid FROM Employee)
        """)
        orphaned = result[0].get('count', 0) if result else 0
        if orphaned > 0:
            print(f"   ❌ Orphaned attendance records: {orphaned}")
            all_passed = False
        else:
            print("   ✅ Attendance record relationships: OK")

        db.close()
        client.close()
        return all_passed

    except Exception as e:
        print(f"❌ Integrity test error: {e}")
        if db:
            try:
                db.close()
            except:
                pass
        if client:
            try:
                client.close()
            except:
                pass
        return False

def test_performance(config):
    """Test basic performance metrics"""
    client = None
    db = None
    try:
        print("\n⚡ Testing performance...")
        client = OrientDB(host=config['host'], port=config['port'])
        client.connect(user=config['user'], password=config['password'])
        db = client.open_database(
            name=config['database'],
            user=config['user'],
            password=config['password']
        )

        # Test query execution time
        start_time = time.time()
        result = db.query("SELECT COUNT(*) FROM AttendanceRecord")
        count = result[0].get('COUNT', 0) if result else 0
        end_time = time.time()
        query_time = end_time - start_time
        print(".4f"
        # Test graph traversal performance
        start_time = time.time()
        result = db.query("""
            SELECT FROM (
                SELECT EXPAND(out('WorksIn')) FROM Department
            )
        """)
        traversal_time = time.time() - start_time
        print(".4f"
        # Test index usage (check if indexes exist)
        indexes = db.query("SELECT name, type FROM (SELECT EXPAND(indexes) FROM metadata:indexmanager)")
        index_count = len(indexes) if indexes else 0
        print(f"   📊 Total indexes: {index_count}")

        db.close()
        client.close()
        return True

    except Exception as e:
        print(f"❌ Performance test error: {e}")
        if db:
            try:
                db.close()
            except:
                pass
        if client:
            try:
                client.close()
            except:
                pass
        return False

def test_graph_operations(config):
    """Test graph-specific operations"""
    client = None
    db = None
    try:
        print("\n🌐 Testing graph operations...")
        client = OrientDB(host=config['host'], port=config['port'])
        client.connect(user=config['user'], password=config['password'])
        db = client.open_database(
            name=config['database'],
            user=config['user'],
            password=config['password']
        )

        # Test edge traversal
        result = db.query("""
            SELECT name, out('Manages').size() as manages_count
            FROM Department
        """)
        dept_managers = result if result else []
        print(f"   👔 Department managers: {len(dept_managers)} relationships")

        # Test employee reporting structure
        result = db.query("""
            SELECT first_name, last_name, out('ReportsTo').size() as reports_count
            FROM Employee
            LIMIT 5
        """)
        reporting = result if result else []
        print(f"   👥 Employee reporting relationships: {len(reporting)} checked")

        # Test department membership
        result = db.query("""
            SELECT name, in('WorksIn').size() as employee_count
            FROM Department
        """)
        memberships = result if result else []
        total_employees = sum(m.get('employee_count', 0) for m in memberships)
        print(f"   🏢 Department memberships: {total_employees} employee assignments")

        db.close()
        client.close()
        return True

    except Exception as e:
        print(f"❌ Graph operations test error: {e}")
        if db:
            try:
                db.close()
            except:
                pass
        if client:
            try:
                client.close()
            except:
                pass
        return False

def main():
    """Main test function"""
    print("🧪 HRMS OrientDB Database Test Suite")
    print("=" * 40)

    config = get_db_config()
    print(f"📍 Testing Database: {config['host']}:{config['port']}/{config['database']}")

    tests = [
        ("Connection Test", test_connection),
        ("Basic Queries Test", test_basic_queries),
        ("Data Integrity Test", test_data_integrity),
        ("Performance Test", test_performance),
        ("Graph Operations Test", test_graph_operations)
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n🔬 Running {test_name}...")
        result = test_func(config)
        results.append((test_name, result))
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {status}")

    # Summary
    print("\n" + "=" * 40)
    print("📋 TEST SUMMARY")
    print("=" * 40)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")

    print(f"\n🎯 Overall: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! OrientDB database is ready for production.")
        print("\n📋 Next steps:")
        print("   1. Configure your application to use OrientDB")
        print("   2. Set up automated backups")
        print("   3. Configure monitoring and alerting")
        print("   4. Test your application with real data")
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
        print("   Check your OrientDB setup and try again.")
        print("\n🔧 Troubleshooting:")
        print("   - Ensure OrientDB server is running")
        print("   - Verify database credentials")
        print("   - Check if database was properly initialized")
        print("   - Run: python3 init_database.py")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

def get_db_config():
    """Get database configuration"""
    return {
        'host': os.getenv('MYSQL_HOST', 'localhost'),
        'port': int(os.getenv('MYSQL_PORT', 3306)),
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', ''),
        'database': os.getenv('MYSQL_DATABASE', 'hrms_db')
    }

def test_connection(config):
    """Test basic database connection"""
    try:
        print("🔌 Testing database connection...")
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"✅ Connected to MySQL Server version {db_info}")
            connection.close()
            return True
        else:
            print("❌ Connection failed")
            return False
    except Error as e:
        print(f"❌ Connection error: {e}")
        return False

def test_basic_queries(config):
    """Test basic database queries"""
    try:
        print("\n📊 Testing basic queries...")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)

        # Test user count
        cursor.execute("SELECT COUNT(*) as user_count FROM users")
        result = cursor.fetchone()
        print(f"   👥 Total users: {result['user_count']}")

        # Test department count
        cursor.execute("SELECT COUNT(*) as dept_count FROM departments")
        result = cursor.fetchone()
        print(f"   🏢 Total departments: {result['dept_count']}")

        # Test leave types
        cursor.execute("SELECT name, days_per_year FROM leave_types WHERE is_active = TRUE")
        leave_types = cursor.fetchall()
        print(f"   📅 Leave types: {len(leave_types)}")
        for leave in leave_types[:3]:  # Show first 3
            print(f"      - {leave['name']}: {leave['days_per_year']} days")

        # Test shift templates
        cursor.execute("SELECT name, start_time, end_time FROM shift_templates WHERE is_active = TRUE LIMIT 3")
        shifts = cursor.fetchall()
        print(f"   ⏰ Active shifts: {len(shifts)}")
        for shift in shifts:
            print(f"      - {shift['name']}: {shift['start_time']} - {shift['end_time']}")

        cursor.close()
        connection.close()
        return True

    except Error as e:
        print(f"❌ Query error: {e}")
        return False

def test_data_integrity(config):
    """Test referential integrity"""
    try:
        print("\n🔗 Testing data integrity...")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Test foreign key constraints
        tests = [
            ("Users with invalid roles", "SELECT COUNT(*) FROM users WHERE role NOT IN ('admin', 'manager', 'employee')"),
            ("Employees without departments", "SELECT COUNT(*) FROM employees WHERE department_id IS NULL"),
            ("Leave requests with invalid status", "SELECT COUNT(*) FROM leave_requests WHERE status NOT IN ('pending', 'approved', 'rejected', 'cancelled')"),
            ("Attendance records without employees", "SELECT COUNT(*) FROM attendance_records ar LEFT JOIN employees e ON ar.employee_id = e.id WHERE e.id IS NULL")
        ]

        all_passed = True
        for test_name, query in tests:
            cursor.execute(query)
            count = cursor.fetchone()[0]
            if count > 0:
                print(f"   ❌ {test_name}: {count} issues found")
                all_passed = False
            else:
                print(f"   ✅ {test_name}: OK")

        cursor.close()
        connection.close()
        return all_passed

    except Error as e:
        print(f"❌ Integrity test error: {e}")
        return False

def test_performance(config):
    """Test basic performance metrics"""
    try:
        print("\n⚡ Testing performance...")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Test query execution time
        import time

        # Simple count query
        start_time = time.time()
        cursor.execute("SELECT COUNT(*) FROM attendance_records")
        cursor.fetchone()
        end_time = time.time()
        query_time = end_time - start_time
        print(f"   Query time: {query_time:.4f} seconds")
        # Test index usage (explain plan)
        cursor.execute("EXPLAIN SELECT * FROM employees WHERE department_id = 1")
        explain_result = cursor.fetchall()
        has_index = any('department_id' in str(row) for row in explain_result)
        if has_index:
            print("   ✅ Department index: Available")
        else:
            print("   ⚠️  Department index: Not used")

        cursor.close()
        connection.close()
        return True

    except Error as e:
        print(f"❌ Performance test error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 HRMS Database Test Suite")
    print("=" * 40)

    config = get_db_config()
    print(f"📍 Testing Database: {config['host']}:{config['port']}/{config['database']}")

    tests = [
        ("Connection Test", test_connection),
        ("Basic Queries Test", test_basic_queries),
        ("Data Integrity Test", test_data_integrity),
        ("Performance Test", test_performance)
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n🔬 Running {test_name}...")
        result = test_func(config)
        results.append((test_name, result))
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {status}")

    # Summary
    print("\n" + "=" * 40)
    print("📋 TEST SUMMARY")
    print("=" * 40)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")

    print(f"\n🎯 Overall: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! Database is ready for production.")
        print("\n📋 Next steps:")
        print("   1. Configure your application to use this database")
        print("   2. Set up automated backups")
        print("   3. Configure monitoring and alerting")
        print("   4. Test your application with real data")
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
        print("   Check your database setup and try again.")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)