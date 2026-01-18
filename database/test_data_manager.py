#!/usr/bin/env python3
"""
HRMS Test Data Management Script
Creates and manages sample data for testing the HRMS OrientDB database

Usage:
    python3 test_data_manager.py --load      # Load sample data
    python3 test_data_manager.py --clean     # Clean all data
    python3 test_data_manager.py --status    # Show current data status
"""

import os
import sys
import argparse
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, date
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class HRMSTestDataManager:
    """Manages test data for HRMS OrientDB database"""

    def __init__(self):
        self.config = self._get_config()
        self.base_url = f"https://{self.config['host']}"
        self.session = requests.Session()

        # Configure session for security
        self.session.headers.update({'Content-Type': 'text/plain'})

    def _get_config(self):
        """Get database configuration"""
        return {
            'host': os.getenv('ORIENTDB_HOST', 'orientdb.transtechologies.com'),
            'user': os.getenv('ORIENTDB_USER', 'root'),
            'password': os.getenv('ORIENTDB_PASSWORD'),
            'database': os.getenv('ORIENTDB_DATABASE', 'hrms')
        }

    def _execute_query(self, query, description=""):
        """Execute SQL query with error handling"""
        try:
            command_url = f"{self.base_url}/command/{self.config['database']}/sql"
            response = self.session.post(
                command_url,
                auth=HTTPBasicAuth(self.config['user'], self.config['password']),
                data=query,
                timeout=30,
                verify=False  # Disable SSL verification for test environment
            )

            if response.status_code == 200:
                if description:
                    print(f"✅ {description}")
                return response.json()
            else:
                print(f"❌ Query failed: {response.status_code} - {response.text[:100]}")
                return None

        except Exception as e:
            print(f"❌ Error executing query: {e}")
            return None

    def clean_all_data(self):
        """Clean all data from database"""
        print("🧹 Cleaning all data from HRMS database...")

        # Delete all edges first (to avoid constraint violations)
        edge_classes = ['WorksIn', 'ReportsTo', 'AssignedTo', 'Manages']

        for edge_class in edge_classes:
            self._execute_query(f"DELETE FROM {edge_class}", f"Deleted all {edge_class} relationships")

        # Delete all vertices
        vertex_classes = [
            'AuditLog', 'LeaveBalance', 'LeaveRequest', 'AttendanceRecord',
            'Schedule', 'ShiftTemplate', 'Position', 'Department',
            'Employee', 'User', 'Institution', 'SystemSetting'
        ]

        for vertex_class in vertex_classes:
            self._execute_query(f"DELETE FROM {vertex_class}", f"Deleted all {vertex_class} records")

        print("✅ Database cleaned successfully!")

    def load_sample_data(self):
        """Load comprehensive sample data"""
        print("📥 Loading sample data into HRMS database...")

        try:
            # 1. Create Institution
            self._create_institution()

            # 2. Create System Settings
            self._create_system_settings()

            # 3. Create Users and Employees
            self._create_users_and_employees()

            # 4. Create Departments
            self._create_departments()

            # 5. Create Positions
            self._create_positions()

            # 6. Create Shift Templates
            self._create_shift_templates()

            # 7. Create Leave Types
            self._create_leave_types()

            # 8. Create Relationships
            self._create_relationships()

            # 9. Create Sample Schedules and Attendance
            self._create_schedules_and_attendance()

            # 10. Create Leave Requests and Balances
            self._create_leave_data()

            print("✅ Sample data loaded successfully!")

        except Exception as e:
            print(f"❌ Error loading sample data: {e}")
            return False

        return True

    def _create_institution(self):
        """Create institution data (skip if already exists)"""
        # Check if institution already exists
        result = self._execute_query("SELECT COUNT(*) as count FROM Institution")
        if result and 'result' in result and result['result'][0].get('count', 0) > 0:
            self._execute_query("", "Institution already exists, skipping")
            return

        query = """
        INSERT INTO Institution SET
          name = 'TechCorp Solutions',
          description = 'Leading technology solutions provider',
          address = {'street': '123 Innovation Drive', 'city': 'San Francisco', 'state': 'CA', 'zip_code': '94105', 'country': 'USA'},
          phone = '+1-555-0123',
          email = 'admin@techcorp.com',
          website = 'https://techcorp.com',
          tax_id = 'TC123456789',
          founded_date = '2010-01-15'
        """
        self._execute_query(query, "Created institution")

    def _create_system_settings(self):
        """Create system settings (skip if already exist)"""
        # Check if system settings already exist
        result = self._execute_query("SELECT COUNT(*) as count FROM SystemSetting")
        if result and 'result' in result and result['result'][0].get('count', 0) > 0:
            self._execute_query("", "System settings already exist, skipping")
            return

        settings = [
            ("timezone", "America/New_York", "System timezone setting"),
            ("working_days_per_week", "5", "Standard working days"),
            ("default_leave_approval_required", "true", "Leave approval policy"),
            ("company_name", "TechCorp Solutions", "Company display name"),
            ("max_leave_days_per_year", "25", "Maximum annual leave days")
        ]

        for key, value, desc in settings:
            query = f"""
            INSERT INTO SystemSetting SET
              key = '{key}',
              value = '{value}',
              category = 'system',
              description = '{desc}',
              updated_at = sysdate()
            """
            self._execute_query(query, f"Created system setting: {key}")

    def _create_users_and_employees(self):
        """Create users and employees"""
        employees_data = [
            {
                'email': 'john.smith@techcorp.com',
                'password': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6fYzYXkqO',  # 'password123'
                'role': 'admin',
                'employee_id': 'EMP001',
                'first_name': 'John',
                'last_name': 'Smith',
                'date_of_birth': '1985-03-15',
                'gender': 'Male',
                'phone': '+1-555-0101',
                'hire_date': '2015-01-15',
                'salary': 95000.00,
                'position': 'Chief Technology Officer'
            },
            {
                'email': 'sarah.johnson@techcorp.com',
                'password': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6fYzYXkqO',
                'role': 'manager',
                'employee_id': 'EMP002',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'date_of_birth': '1988-07-22',
                'gender': 'Female',
                'phone': '+1-555-0102',
                'hire_date': '2018-03-01',
                'salary': 75000.00,
                'position': 'HR Manager'
            },
            {
                'email': 'mike.davis@techcorp.com',
                'password': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6fYzYXkqO',
                'role': 'manager',
                'employee_id': 'EMP003',
                'first_name': 'Mike',
                'last_name': 'Davis',
                'date_of_birth': '1982-11-08',
                'gender': 'Male',
                'phone': '+1-555-0103',
                'hire_date': '2016-06-15',
                'salary': 80000.00,
                'position': 'Engineering Manager'
            },
            {
                'email': 'emily.brown@techcorp.com',
                'password': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6fYzYXkqO',
                'role': 'employee',
                'employee_id': 'EMP004',
                'first_name': 'Emily',
                'last_name': 'Brown',
                'date_of_birth': '1992-01-30',
                'gender': 'Female',
                'phone': '+1-555-0104',
                'hire_date': '2020-09-01',
                'salary': 65000.00,
                'position': 'Software Developer'
            },
            {
                'email': 'alex.wilson@techcorp.com',
                'password': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6fYzYXkqO',
                'role': 'employee',
                'employee_id': 'EMP005',
                'first_name': 'Alex',
                'last_name': 'Wilson',
                'date_of_birth': '1990-05-12',
                'gender': 'Male',
                'phone': '+1-555-0105',
                'hire_date': '2019-11-15',
                'salary': 70000.00,
                'position': 'DevOps Engineer'
            }
        ]

        for emp_data in employees_data:
            address = {
                'street': f"{emp_data['first_name']}'s Address",
                'city': 'San Francisco',
                'state': 'CA',
                'zip_code': '94105',
                'country': 'USA'
            }

            emergency_contact = {
                'name': f"{emp_data['first_name']}'s Emergency Contact",
                'relationship': 'Spouse',
                'phone': '+1-555-9999',
                'email': f"emergency.{emp_data['first_name'].lower()}@example.com"
            }

            query = f"""
            INSERT INTO Employee SET
              email = '{emp_data['email']}',
              password_hash = '{emp_data['password']}',
              role = '{emp_data['role']}',
              is_active = true,
              created_at = sysdate(),
              updated_at = sysdate(),
              employee_id = '{emp_data['employee_id']}',
              first_name = '{emp_data['first_name']}',
              last_name = '{emp_data['last_name']}',
              date_of_birth = '{emp_data['date_of_birth']}',
              gender = '{emp_data['gender']}',
              phone = '{emp_data['phone']}',
              address = {json.dumps(address)},
              hire_date = '{emp_data['hire_date']}',
              salary = {emp_data['salary']},
              position = '{emp_data['position']}',
              emergency_contact = {json.dumps(emergency_contact)},
              skills = ['Python', 'JavaScript', 'SQL'],
              certifications = [{{
                'name': 'AWS Certified Developer',
                'issuing_authority': 'Amazon Web Services',
                'issue_date': '2023-01-15',
                'expiry_date': '2026-01-15',
                'certification_number': 'AWS-{emp_data['employee_id']}'
              }}]
            """
            self._execute_query(query, f"Created employee: {emp_data['first_name']} {emp_data['last_name']}")

    def _create_departments(self):
        """Create departments"""
        departments = [
            ('Information Technology', 'IT department responsible for technology infrastructure', 500000.00, 'Floor 3'),
            ('Human Resources', 'HR department managing employee relations', 200000.00, 'Floor 2'),
            ('Engineering', 'Software development and engineering', 800000.00, 'Floor 4'),
            ('Finance', 'Financial operations and accounting', 300000.00, 'Floor 5'),
            ('Operations', 'Business operations and support', 250000.00, 'Floor 1')
        ]

        for name, desc, budget, location in departments:
            query = f"""
            INSERT INTO Department SET
              name = '{name}',
              description = '{desc}',
              budget = {budget},
              location = '{location}',
              is_active = true,
              created_at = sysdate()
            """
            self._execute_query(query, f"Created department: {name}")

    def _create_positions(self):
        """Create positions"""
        positions = [
            ('Chief Technology Officer', 'Senior technology leadership role', 'Executive', {'min': 120000, 'max': 180000}),
            ('HR Manager', 'Human resources management', 'Management', {'min': 70000, 'max': 95000}),
            ('Engineering Manager', 'Engineering team leadership', 'Management', {'min': 90000, 'max': 130000}),
            ('Software Developer', 'Application development', 'Technical', {'min': 60000, 'max': 90000}),
            ('DevOps Engineer', 'Infrastructure and deployment', 'Technical', {'min': 75000, 'max': 110000})
        ]

        for title, desc, level, salary_range in positions:
            query = f"""
            INSERT INTO Position SET
              title = '{title}',
              description = '{desc}',
              level = '{level}',
              salary_range = {json.dumps(salary_range)},
              is_active = true
            """
            self._execute_query(query, f"Created position: {title}")

    def _create_shift_templates(self):
        """Create shift templates"""
        shifts = [
            ('Standard Day Shift', 'Regular 9-5 workday', '09:00', '17:00', 8.0, 60),
            ('Morning Shift', 'Early morning shift', '06:00', '14:00', 8.0, 60),
            ('Evening Shift', 'Evening shift', '14:00', '22:00', 8.0, 60),
            ('Night Shift', 'Overnight shift', '22:00', '06:00', 8.0, 60),
            ('Flexible Hours', 'Flexible working hours', '08:00', '16:00', 8.0, 30)
        ]

        for name, desc, start, end, hours, break_min in shifts:
            query = f"""
            INSERT INTO ShiftTemplate SET
              name = '{name}',
              description = '{desc}',
              start_time = '{start}',
              end_time = '{end}',
              duration_hours = {hours},
              break_duration = {break_min},
              is_active = true,
              created_at = sysdate()
            """
            self._execute_query(query, f"Created shift template: {name}")

    def _create_leave_types(self):
        """Create leave types (skip if already exist)"""
        # Check if leave types already exist
        result = self._execute_query("SELECT COUNT(*) as count FROM LeaveType")
        if result and 'result' in result and result['result'][0].get('count', 0) > 0:
            self._execute_query("", "Leave types already exist, skipping")
            return

        leave_types = [
            ('Annual Leave', 'Standard annual vacation leave', 25, True, True),
            ('Sick Leave', 'Medical leave for illness', 10, True, False),
            ('Personal Leave', 'Personal time off', 5, True, True),
            ('Maternity Leave', 'Maternity leave', 90, True, True),
            ('Paternity Leave', 'Paternity leave', 10, True, True)
        ]

        for name, desc, days, paid, approval in leave_types:
            query = f"""
            INSERT INTO LeaveType SET
              name = '{name}',
              description = '{desc}',
              days_per_year = {days},
              is_paid = {str(paid).lower()},
              requires_approval = {str(approval).lower()},
              is_active = true
            """
            self._execute_query(query, f"Created leave type: {name}")

    def _create_relationships(self):
        """Create relationships between entities"""
        # Get RIDs for relationships
        emp_rids = self._get_employee_rids()
        dept_rids = self._get_department_rids()
        pos_rids = self._get_position_rids()

        # Create WorksIn relationships
        relationships = [
            (emp_rids.get('EMP001'), dept_rids.get('Information Technology'), '2020-01-15', None, True),  # CTO in IT
            (emp_rids.get('EMP002'), dept_rids.get('Human Resources'), '2018-03-01', None, True),  # HR Manager in HR
            (emp_rids.get('EMP003'), dept_rids.get('Engineering'), '2016-06-15', None, True),  # Eng Manager in Eng
            (emp_rids.get('EMP004'), dept_rids.get('Engineering'), '2020-09-01', None, True),  # Developer in Eng
            (emp_rids.get('EMP005'), dept_rids.get('Information Technology'), '2019-11-15', None, True),  # DevOps in IT
        ]

        for emp_rid, dept_rid, start_date, end_date, is_primary in relationships:
            if emp_rid and dept_rid:
                query = f"""
                CREATE EDGE WorksIn
                FROM {emp_rid}
                TO {dept_rid}
                SET start_date = '{start_date}',
                    end_date = {f"'{end_date}'" if end_date else 'null'},
                    is_primary = {str(is_primary).lower()}
                """
                self._execute_query(query, "Created WorksIn relationship")

        # Create ReportsTo relationships (reporting hierarchy)
        reports_to = [
            (emp_rids.get('EMP003'), emp_rids.get('EMP001'), 'direct'),  # Eng Manager reports to CTO
            (emp_rids.get('EMP004'), emp_rids.get('EMP003'), 'direct'),  # Developer reports to Eng Manager
            (emp_rids.get('EMP005'), emp_rids.get('EMP001'), 'direct'),  # DevOps reports to CTO
        ]

        for emp_rid, manager_rid, rel_type in reports_to:
            if emp_rid and manager_rid:
                query = f"""
                CREATE EDGE ReportsTo
                FROM {emp_rid}
                TO {manager_rid}
                SET relationship_type = '{rel_type}',
                    start_date = '2020-01-01'
                """
                self._execute_query(query, "Created ReportsTo relationship")

        # Set manager_id references
        manager_updates = [
            ('EMP003', 'EMP001'),  # Eng Manager's manager is CTO
            ('EMP004', 'EMP003'),  # Developer's manager is Eng Manager
            ('EMP005', 'EMP001'),  # DevOps manager is CTO
        ]

        for emp_id, manager_id in manager_updates:
            if emp_rids.get(emp_id) and emp_rids.get(manager_id):
                query = f"""
                UPDATE Employee SET manager_id = {emp_rids[manager_id]}
                WHERE employee_id = '{emp_id}'
                """
                self._execute_query(query, f"Updated manager for {emp_id}")

    def _create_schedules_and_attendance(self):
        """Create sample schedules and attendance records"""
        # Get some employee and shift RIDs
        emp_rids = self._get_employee_rids()
        shift_rids = self._get_shift_template_rids()

        # Create some schedules for next week
        import datetime
        today = datetime.date.today()
        next_week = [today.replace(day=today.day + i) for i in range(7, 14)]

        schedules = []
        for emp_id, emp_rid in list(emp_rids.items())[:3]:  # First 3 employees
            for i, date in enumerate(next_week[:5]):  # Monday to Friday
                shift_rid = list(shift_rids.values())[i % len(shift_rids)]  # Rotate shifts
                schedules.append((emp_rid, shift_rid, date))

        for emp_rid, shift_rid, schedule_date in schedules:
            query = f"""
            INSERT INTO Schedule SET
              employee_id = {emp_rid},
              shift_template_id = {shift_rid},
              date = '{schedule_date}',
              status = 'scheduled',
              notes = 'Regular work schedule'
            """
            self._execute_query(query, f"Created schedule for {schedule_date}")

        # Create some attendance records for past dates
        past_dates = [today.replace(day=today.day - i) for i in range(1, 6)]
        for emp_id, emp_rid in list(emp_rids.items())[:3]:
            for date in past_dates:
                query = f"""
                INSERT INTO AttendanceRecord SET
                  employee_id = {emp_rid},
                  date = '{date}',
                  clock_in_time = '{date} 09:00:00',
                  clock_out_time = '{date} 17:00:00',
                  hours_worked = 8.0,
                  status = 'present',
                  location = 'Office',
                  notes = 'Regular attendance'
                """
                self._execute_query(query, f"Created attendance record for {date}")

    def _create_leave_data(self):
        """Create leave requests and balances"""
        emp_rids = self._get_employee_rids()
        leave_type_rids = self._get_leave_type_rids()

        # Create leave balances for current year
        current_year = datetime.now().year
        for emp_id, emp_rid in emp_rids.items():
            for leave_type_name, leave_rid in leave_type_rids.items():
                # Get leave type details
                leave_info = self._execute_query(f"SELECT days_per_year FROM {leave_rid}")
                if leave_info and 'result' in leave_info:
                    days_per_year = leave_info['result'][0].get('days_per_year', 0)
                else:
                    days_per_year = 0

                query = f"""
                INSERT INTO LeaveBalance SET
                  employee_id = {emp_rid},
                  leave_type_id = {leave_rid},
                  year = {current_year},
                  balance_days = {days_per_year},
                  used_days = 0,
                  carried_forward = 0
                """
                self._execute_query(query, f"Created leave balance for {emp_id} - {leave_type_name}")

        # Create some leave requests
        leave_requests = [
            (emp_rids.get('EMP004'), leave_type_rids.get('Annual Leave'), '2024-12-20', '2024-12-27', 6, 'Holiday vacation'),
            (emp_rids.get('EMP005'), leave_type_rids.get('Sick Leave'), '2024-11-15', '2024-11-15', 1, 'Medical appointment'),
        ]

        for emp_rid, leave_rid, start_date, end_date, days, reason in leave_requests:
            if emp_rid and leave_rid:
                query = f"""
                INSERT INTO LeaveRequest SET
                  employee_id = {emp_rid},
                  leave_type_id = {leave_rid},
                  start_date = '{start_date}',
                  end_date = '{end_date}',
                  days_requested = {days},
                  reason = '{reason}',
                  status = 'approved',
                  approved_by = {emp_rids.get('EMP002')},  # HR Manager
                  approved_at = sysdate(),
                  created_at = sysdate()
                """
                self._execute_query(query, f"Created leave request for {days} days")

    def _get_employee_rids(self):
        """Get employee RIDs by employee_id"""
        result = self._execute_query("SELECT @rid, employee_id FROM Employee")
        if result and 'result' in result:
            return {record['employee_id']: record['@rid'] for record in result['result']}
        return {}

    def _get_department_rids(self):
        """Get department RIDs by name"""
        result = self._execute_query("SELECT @rid, name FROM Department")
        if result and 'result' in result:
            return {record['name']: record['@rid'] for record in result['result']}
        return {}

    def _get_position_rids(self):
        """Get position RIDs by title"""
        result = self._execute_query("SELECT @rid, title FROM Position")
        if result and 'result' in result:
            return {record['title']: record['@rid'] for record in result['result']}
        return {}

    def _get_shift_template_rids(self):
        """Get shift template RIDs by name"""
        result = self._execute_query("SELECT @rid, name FROM ShiftTemplate")
        if result and 'result' in result:
            return {record['name']: record['@rid'] for record in result['result']}
        return {}

    def _get_leave_type_rids(self):
        """Get leave type RIDs by name"""
        result = self._execute_query("SELECT @rid, name FROM LeaveType")
        if result and 'result' in result:
            return {record['name']: record['@rid'] for record in result['result']}
        return {}

    def show_status(self):
        """Show current database status"""
        print("📊 HRMS Database Status")
        print("=" * 50)

        classes_to_check = [
            'Institution', 'User', 'Employee', 'Department', 'Position',
            'ShiftTemplate', 'Schedule', 'AttendanceRecord', 'LeaveType',
            'LeaveRequest', 'LeaveBalance', 'SystemSetting', 'AuditLog'
        ]

        for class_name in classes_to_check:
            result = self._execute_query(f"SELECT COUNT(*) as count FROM {class_name}")
            if result and 'result' in result:
                count = result['result'][0].get('count', 0)
                print(f"📋 {class_name}: {count} records")
            else:
                print(f"📋 {class_name}: Error checking count")

        print("\n" + "=" * 50)


def main():
    parser = argparse.ArgumentParser(description='HRMS Test Data Manager')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--load', action='store_true', help='Load sample data')
    group.add_argument('--clean', action='store_true', help='Clean all data')
    group.add_argument('--status', action='store_true', help='Show database status')

    args = parser.parse_args()

    try:
        manager = HRMSTestDataManager()

        if args.load:
            print("🚀 Starting sample data load...")
            success = manager.load_sample_data()
            if success:
                print("\n" + "=" * 50)
                manager.show_status()
                print("✅ Sample data loaded successfully!")
            else:
                print("❌ Failed to load sample data")
                sys.exit(1)

        elif args.clean:
            print("🧹 Starting database cleanup...")
            manager.clean_all_data()
            print("✅ Database cleaned successfully!")

        elif args.status:
            manager.show_status()

    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()