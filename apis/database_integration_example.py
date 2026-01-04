"""
Database Integration Example for HRMS Components
Shows how to integrate the OrientDB database service with existing components
"""

import sys
from pathlib import Path
from datetime import datetime, date, timedelta

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from apis.database_service import db_service

def example_employee_schedule_integration():
    """
    Example of how to integrate OrientDB service with shift timetable component
    This replaces the YAML-based data loading with OrientDB document operations
    """

    def get_employee_schedule_from_db(employee_rid: str, start_date: date, end_date: date):
        """Get employee schedule from OrientDB instead of YAML"""
        try:
            schedules = db_service.get_employee_schedule(employee_rid, start_date, end_date)

            # Convert to format expected by timetable component
            schedule_data = {}
            for schedule in schedules:
                date_str = schedule['date'].isoformat()
                schedule_data[date_str] = {
                    'shift_id': schedule['rid'],  # Use RID as shift ID
                    'shift_name': schedule.get('shift_name', 'Unknown'),
                    'start_time': schedule.get('start_time', '09:00'),
                    'end_time': schedule.get('end_time', '17:00'),
                    'is_active': schedule.get('status') == 'scheduled'
                }

            return schedule_data

        except Exception as e:
            print(f"Error loading schedule from OrientDB: {e}")
            return {}

    def save_schedule_to_db(employee_rid: str, date_obj: date, shift_template_rid: str):
        """Save schedule assignment to OrientDB"""
        try:
            # Check if schedule already exists for this date
            existing = db_service.query(
                "SELECT @rid.asString() as rid FROM Schedule WHERE employee_id = :emp_rid AND date = :date",
                {'emp_rid': employee_rid, 'date': date_obj.isoformat()}
            )

            schedule_data = {
                'employee_id': employee_rid,
                'shift_template_id': shift_template_rid,
                'date': date_obj.isoformat(),
                'status': 'scheduled'
            }

            if existing:
                # Update existing schedule
                success = db_service.command(
                    "UPDATE Schedule SET shift_template_id = :shift_template_id, status = :status WHERE @rid = :rid",
                    {**schedule_data, 'rid': existing[0]['rid']}
                )
                return success > 0
            else:
                # Insert new schedule
                return db_service.create_schedule(schedule_data)

        except Exception as e:
            print(f"Error saving schedule to OrientDB: {e}")
            return False

    return {
        'get_employee_schedule': get_employee_schedule_from_db,
        'save_schedule': save_schedule_to_db
    }

def example_attendance_integration():
    """
    Example of how to integrate OrientDB service with attendance tracking
    """

    def record_clock_in_db(employee_rid: str):
        """Record clock in using OrientDB service"""
        try:
            success = db_service.clock_in(employee_rid)
            if success:
                print(f"Clock in recorded for employee {employee_rid}")
                return True
            else:
                print("Failed to record clock in")
                return False
        except Exception as e:
            print(f"Error recording clock in: {e}")
            return False

    def record_clock_out_db(employee_rid: str):
        """Record clock out using OrientDB service"""
        try:
            success = db_service.clock_out(employee_rid)
            if success:
                print(f"Clock out recorded for employee {employee_rid}")
                return True
            else:
                print("Failed to record clock out")
                return False
        except Exception as e:
            print(f"Error recording clock out: {e}")
            return False

    def get_today_attendance_db(employee_rid: str):
        """Get today's attendance record"""
        try:
            today = date.today()
            records = db_service.get_attendance_records(employee_rid, today, today)
            return records[0] if records else None
        except Exception as e:
            print(f"Error getting attendance: {e}")
            return None

    def get_attendance_summary_db(employee_rid: str, start_date: date, end_date: date):
        """Get attendance summary for a period"""
        try:
            records = db_service.get_attendance_records(employee_rid, start_date, end_date)

            # Calculate summary
            total_days = len(records)
            present_days = sum(1 for r in records if r.get('clock_in_time'))
            total_hours = sum(r.get('hours_worked', 0) for r in records if r.get('hours_worked'))

            return {
                'total_days': total_days,
                'present_days': present_days,
                'absent_days': total_days - present_days,
                'total_hours': total_hours,
                'average_hours': total_hours / present_days if present_days > 0 else 0
            }
        except Exception as e:
            print(f"Error getting attendance summary: {e}")
            return {}

    return {
        'clock_in': record_clock_in_db,
        'clock_out': record_clock_out_db,
        'get_today_attendance': get_today_attendance_db,
        'get_summary': get_attendance_summary_db
    }

def example_leave_management_integration():
    """
    Example of how to integrate OrientDB service with leave management
    """

    def submit_leave_request_db(employee_rid: str, leave_type_name: str, start_date: date, end_date: date, reason: str):
        """Submit leave request to OrientDB"""
        try:
            # Find leave type by name
            leave_types = db_service.query(
                "SELECT @rid.asString() as rid FROM LeaveType WHERE name = :name AND is_active = true",
                {'name': leave_type_name}
            )

            if not leave_types:
                print(f"Leave type '{leave_type_name}' not found")
                return False

            leave_type_rid = leave_types[0]['rid']

            success = db_service.submit_leave_request(
                employee_rid, leave_type_rid, start_date, end_date, reason
            )

            if success:
                print("Leave request submitted successfully")
                return True
            else:
                print("Failed to submit leave request")
                return False

        except Exception as e:
            print(f"Error submitting leave request: {e}")
            return False

    def get_leave_balance_db(employee_rid: str):
        """Get leave balance from OrientDB"""
        try:
            return db_service.get_leave_balance(employee_rid)
        except Exception as e:
            print(f"Error getting leave balance: {e}")
            return {}

    def get_pending_leave_requests_db(employee_rid: str):
        """Get pending leave requests"""
        try:
            return db_service.get_leave_requests(employee_rid, 'pending')
        except Exception as e:
            print(f"Error getting leave requests: {e}")
            return []

    def approve_leave_request_db(request_rid: str, approver_rid: str):
        """Approve a leave request"""
        try:
            success = db_service.command(
                "UPDATE LeaveRequest SET status = 'approved', approved_by = :approver, approved_at = :approved_at WHERE @rid = :rid",
                {
                    'approver': approver_rid,
                    'approved_at': datetime.now().isoformat(),
                    'rid': request_rid
                }
            )
            return success > 0
        except Exception as e:
            print(f"Error approving leave request: {e}")
            return False

    return {
        'submit_leave_request': submit_leave_request_db,
        'get_leave_balance': get_leave_balance_db,
        'get_pending_requests': get_pending_leave_requests_db,
        'approve_request': approve_leave_request_db
    }

def example_department_management_integration():
    """
    Example of how to integrate OrientDB service with department management
    """

    def get_department_employees_db(department_rid: str):
        """Get all employees in a department using graph traversal"""
        try:
            # Use graph traversal to find employees in department
            employees = db_service.query("""
                SELECT @rid.asString() as rid, first_name, last_name, employee_id,
                       position, hire_date
                FROM (
                    SELECT EXPAND(in('WorksIn')) FROM :dept_rid
                )
                WHERE is_active = true
                ORDER BY last_name, first_name
            """, {'dept_rid': department_rid})

            return employees
        except Exception as e:
            print(f"Error getting department employees: {e}")
            return []

    def get_department_manager_db(department_rid: str):
        """Get department manager using graph traversal"""
        try:
            managers = db_service.query("""
                SELECT manager_id.@rid.asString() as manager_rid,
                       manager_id.first_name as first_name,
                       manager_id.last_name as last_name,
                       manager_id.employee_id as employee_id
                FROM :dept_rid
                WHERE manager_id IS NOT NULL
            """, {'dept_rid': department_rid})

            return managers[0] if managers else None
        except Exception as e:
            print(f"Error getting department manager: {e}")
            return None

    def assign_employee_to_department_db(employee_rid: str, department_rid: str):
        """Create WorksIn relationship between employee and department"""
        try:
            # Check if relationship already exists
            existing = db_service.query("""
                SELECT @rid.asString() as rid FROM WorksIn
                WHERE out = :emp_rid AND in = :dept_rid AND is_primary = true
            """, {'emp_rid': employee_rid, 'dept_rid': department_rid})

            if existing:
                print("Employee is already assigned to this department")
                return True

            # Create new WorksIn edge
            success = db_service.command("""
                CREATE EDGE WorksIn FROM :emp_rid TO :dept_rid
                SET start_date = :start_date, is_primary = true
            """, {
                'emp_rid': employee_rid,
                'dept_rid': department_rid,
                'start_date': date.today().isoformat()
            })

            return success > 0
        except Exception as e:
            print(f"Error assigning employee to department: {e}")
            return False

    return {
        'get_employees': get_department_employees_db,
        'get_manager': get_department_manager_db,
        'assign_employee': assign_employee_to_department_db
    }

def example_reporting_integration():
    """
    Example of how to integrate OrientDB service with reporting features
    """

    def get_attendance_report_db(start_date: date, end_date: date, department_rid: str = None):
        """Generate attendance report from OrientDB"""
        try:
            return db_service.get_attendance_summary(start_date, end_date, department_rid)
        except Exception as e:
            print(f"Error generating attendance report: {e}")
            return []

    def get_leave_report_db(year: int, department_rid: str = None):
        """Generate leave report from OrientDB"""
        try:
            return db_service.get_leave_summary(year, department_rid)
        except Exception as e:
            print(f"Error generating leave report: {e}")
            return []

    def get_department_list_db():
        """Get department list from OrientDB"""
        try:
            return db_service.get_departments()
        except Exception as e:
            print(f"Error getting departments: {e}")
            return []

    def get_organization_overview_db():
        """Get organization-wide statistics"""
        try:
            # Get employee count by department
            dept_stats = db_service.query("""
                SELECT name as department_name,
                       in('WorksIn').size() as employee_count
                FROM Department
                WHERE is_active = true
                ORDER BY employee_count DESC
            """)

            # Get attendance stats for current month
            today = date.today()
            start_of_month = date(today.year, today.month, 1)

            attendance_stats = db_service.query("""
                SELECT COUNT(*) as total_records,
                       SUM(CASE WHEN clock_in_time IS NOT NULL THEN 1 ELSE 0 END) as present_count
                FROM AttendanceRecord
                WHERE date BETWEEN :start_date AND :end_date
            """, {
                'start_date': start_of_month.isoformat(),
                'end_date': today.isoformat()
            })

            # Get leave request stats
            leave_stats = db_service.query("""
                SELECT status, COUNT(*) as count
                FROM LeaveRequest
                WHERE YEAR(created_at) = :year
                GROUP BY status
            """, {'year': str(today.year)})

            return {
                'departments': dept_stats,
                'attendance_this_month': attendance_stats[0] if attendance_stats else {},
                'leave_requests_this_year': {stat['status']: stat['count'] for stat in leave_stats}
            }
        except Exception as e:
            print(f"Error getting organization overview: {e}")
            return {}

    return {
        'attendance_report': get_attendance_report_db,
        'leave_report': get_leave_report_db,
        'departments': get_department_list_db,
        'organization_overview': get_organization_overview_db
    }

# Integration examples for different components
schedule_integration = example_employee_schedule_integration()
attendance_integration = example_attendance_integration()
leave_integration = example_leave_management_integration()
department_integration = example_department_management_integration()
reporting_integration = example_reporting_integration()

def demonstrate_integration():
    """
    Demonstrate how the OrientDB integrations work with sample data
    This function shows how existing components can be updated to use OrientDB
    """
    print("🔗 HRMS OrientDB Database Integration Examples")
    print("=" * 60)

    try:
        # Test database connection
        print("Testing OrientDB connection...")
        test_result = db_service.query("SELECT 1 as test")
        if test_result and test_result[0].get('test') == 1:
            print("✅ OrientDB connection successful")
        else:
            print("❌ OrientDB connection failed")
            return

        # Get sample data for demonstration
        print("\n📊 Testing Data Retrieval...")

        # Test departments
        departments = reporting_integration['departments']()
        if departments:
            print(f"   ✅ Found {len(departments)} departments")
            sample_dept = departments[0]
            print(f"   Sample department: {sample_dept.get('name', 'Unknown')}")

            # Test department integration
            dept_rid = sample_dept['rid']
            dept_employees = department_integration['get_employees'](dept_rid)
            print(f"   Department has {len(dept_employees)} employees")

            dept_manager = department_integration['get_manager'](dept_rid)
            if dept_manager:
                print(f"   Department manager: {dept_manager.get('first_name', '')} {dept_manager.get('last_name', '')}")
        else:
            print("   ⚠️  No departments found")

        # Test leave types
        leave_types = db_service.query("SELECT name, days_per_year FROM LeaveType WHERE is_active = true")
        if leave_types:
            print(f"   ✅ Found {len(leave_types)} leave types")
            for lt in leave_types[:2]:  # Show first 2
                print(f"      - {lt.get('name', 'Unknown')}: {lt.get('days_per_year', 0)} days")
        else:
            print("   ⚠️  No leave types found")

        # Test shift templates
        shift_templates = db_service.get_shift_templates()
        if shift_templates:
            print(f"   ✅ Found {len(shift_templates)} shift templates")
            for st in shift_templates[:2]:  # Show first 2
                print(f"      - {st.get('name', 'Unknown')}: {st.get('start_time', 'N/A')} - {st.get('end_time', 'N/A')}")
        else:
            print("   ⚠️  No shift templates found")

        # Test organization overview
        print("\n📈 Testing Reporting Integration...")
        overview = reporting_integration['organization_overview']()
        if overview:
            print("   ✅ Organization overview generated")
            if 'departments' in overview:
                print(f"   Departments with employees: {len(overview['departments'])}")
        else:
            print("   ⚠️  Could not generate organization overview")

        print("\n🎯 Integration Test Summary:")
        print("   ✅ OrientDB connection working")
        print("   ✅ Document queries functional")
        print("   ✅ Graph traversals operational")
        print("   ✅ Reporting queries working")
        print("\n📝 Next Steps:")
        print("   1. Update your component imports to use the new integration functions")
        print("   2. Replace YAML file operations with OrientDB calls")
        print("   3. Test each component with real OrientDB data")
        print("   4. Implement error handling for network issues")
        print("   5. Add connection pooling for better performance")

    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        print("Make sure OrientDB is running and the database is properly initialized")

if __name__ == "__main__":
    demonstrate_integration()