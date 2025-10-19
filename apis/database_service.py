"""
HRMS OrientDB Database Service
Provides a clean interface for database operations using OrientDB's multi-model capabilities
"""

import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, date, time
from contextlib import contextmanager

try:
    import pyorient
except ImportError:
    print("❌ Error: pyorient not installed")
    print("Install with: pip install pyorient")
    raise

class OrientDBService:
    """Database service for HRMS operations using OrientDB"""

    def __init__(self):
        self.client = None
        self.db = None
        self.logger = logging.getLogger(__name__)
        self._connect()

    def _connect(self):
        """Establish connection to OrientDB"""
        try:
            config = {
                'host': os.getenv('ORIENTDB_HOST', 'localhost'),
                'port': int(os.getenv('ORIENTDB_PORT', 2424)),
                'user': os.getenv('ORIENTDB_USER', 'root'),
                'password': os.getenv('ORIENTDB_PASSWORD', 'root'),
                'database': os.getenv('ORIENTDB_DATABASE', 'hrms_db')
            }

            self.client = pyorient.OrientDB(host=config['host'], port=config['port'])
            self.client.connect(user=config['user'], password=config['password'])

            if not self.client.db_exists(config['database']):
                self.client.db_create(
                    config['database'],
                    pyorient.DB_TYPE_GRAPH,
                    pyorient.STORAGE_TYPE_MEMORY
                )

            self.db = self.client.db_open(
                config['database'],
                config['user'],
                config['password']
            )

            self.logger.info("OrientDB connection established successfully")

        except Exception as e:
            self.logger.error(f"Failed to connect to OrientDB: {e}")
            raise

    def close(self):
        """Close database connections"""
        try:
            if self.db:
                self.db.close()
            if self.client:
                self.client.close()
        except Exception as e:
            self.logger.error(f"Error closing connections: {e}")

    def query(self, sql: str, params: Dict = None) -> List[Dict]:
        """Execute a SELECT query and return results"""
        try:
            if params:
                # OrientDB parameter binding
                result = self.db.query(sql, params)
            else:
                result = self.db.query(sql)

            # Convert OrientDB results to dict format
            return [dict(record) for record in result] if result else []

        except Exception as e:
            self.logger.error(f"Query error: {e}")
            return []

    def command(self, sql: str, params: Dict = None) -> int:
        """Execute an INSERT, UPDATE, or DELETE command and return affected count"""
        try:
            if params:
                result = self.db.command(sql, params)
            else:
                result = self.db.command(sql)

            # Return affected count if available
            return getattr(result, 'count', 1) if result else 0

        except Exception as e:
            self.logger.error(f"Command error: {e}")
            return 0

    # User Management Methods
    def authenticate_user(self, email: str, password_hash: str) -> Optional[Dict]:
        """Authenticate a user"""
        sql = """
            SELECT @rid.asString() as rid, email, role, is_active, created_at,
                   first_name, last_name, employee_id
            FROM User
            WHERE email = :email AND password_hash = :password_hash AND is_active = true
        """
        result = self.query(sql, {'email': email, 'password_hash': password_hash})
        return result[0] if result else None

    def get_user_by_id(self, user_rid: str) -> Optional[Dict]:
        """Get user details by RID"""
        sql = """
            SELECT @rid.asString() as rid, email, role, is_active, created_at,
                   first_name, last_name, employee_id
            FROM :rid
        """
        result = self.query(sql, {'rid': user_rid})
        return result[0] if result else None

    def create_user(self, user_data: Dict) -> Optional[str]:
        """Create a new user and return RID"""
        sql = """
            INSERT INTO User SET
            email = :email,
            password_hash = :password_hash,
            role = :role,
            is_active = :is_active,
            created_at = :created_at,
            updated_at = :updated_at
        """
        try:
            result = self.command(sql, user_data)
            if result > 0:
                # Get the created record
                created = self.query("SELECT @rid.asString() as rid FROM User WHERE email = :email", {'email': user_data['email']})
                return created[0]['rid'] if created else None
        except Exception as e:
            self.logger.error(f"Error creating user: {e}")
        return None

    # Employee Management Methods
    def get_employees(self, department_rid: str = None, active_only: bool = True) -> List[Dict]:
        """Get employees, optionally filtered by department"""
        conditions = []
        params = {}

        if department_rid:
            conditions.append("department_id = :dept_rid")
            params['dept_rid'] = department_rid

        if active_only:
            conditions.append("is_active = true")

        where_clause = " AND ".join(conditions) if conditions else "true"

        sql = f"""
            SELECT @rid.asString() as rid, first_name, last_name, employee_id,
                   email, role, department_id.asString() as department_rid
            FROM Employee
            WHERE {where_clause}
            ORDER BY last_name, first_name
        """

        return self.query(sql, params)

    def get_employee_details(self, employee_rid: str) -> Optional[Dict]:
        """Get detailed employee information"""
        sql = """
            SELECT @rid.asString() as rid, first_name, last_name, employee_id,
                   date_of_birth, gender, phone, address, hire_date, salary,
                   position, emergency_contact, skills, certifications,
                   email, role, is_active
            FROM :rid
        """
        result = self.query(sql, {'rid': employee_rid})
        return result[0] if result else None

    def create_employee(self, employee_data: Dict) -> Optional[str]:
        """Create a new employee"""
        sql = """
            INSERT INTO Employee SET
            employee_id = :employee_id,
            first_name = :first_name,
            last_name = :last_name,
            date_of_birth = :date_of_birth,
            gender = :gender,
            phone = :phone,
            address = :address,
            hire_date = :hire_date,
            salary = :salary,
            position = :position,
            emergency_contact = :emergency_contact,
            skills = :skills,
            certifications = :certifications,
            email = :email,
            password_hash = :password_hash,
            role = :role,
            is_active = :is_active,
            created_at = :created_at,
            updated_at = :updated_at
        """
        try:
            result = self.command(sql, employee_data)
            if result > 0:
                created = self.query("SELECT @rid.asString() as rid FROM Employee WHERE employee_id = :emp_id",
                                   {'emp_id': employee_data['employee_id']})
                return created[0]['rid'] if created else None
        except Exception as e:
            self.logger.error(f"Error creating employee: {e}")
        return None

    # Department Management Methods
    def get_departments(self) -> List[Dict]:
        """Get all active departments"""
        sql = """
            SELECT @rid.asString() as rid, name, description, budget, location,
                   manager_id.asString() as manager_rid
            FROM Department
            WHERE is_active = true
            ORDER BY name
        """
        return self.query(sql)

    def create_department(self, dept_data: Dict) -> Optional[str]:
        """Create a new department"""
        sql = """
            INSERT INTO Department SET
            name = :name,
            description = :description,
            budget = :budget,
            location = :location,
            is_active = :is_active,
            created_at = :created_at
        """
        try:
            result = self.command(sql, dept_data)
            if result > 0:
                created = self.query("SELECT @rid.asString() as rid FROM Department WHERE name = :name",
                                   {'name': dept_data['name']})
                return created[0]['rid'] if created else None
        except Exception as e:
            self.logger.error(f"Error creating department: {e}")
        return None

    # Schedule Management Methods
    def get_employee_schedule(self, employee_rid: str, start_date: date, end_date: date) -> List[Dict]:
        """Get employee schedule for a date range"""
        sql = """
            SELECT @rid.asString() as rid, date, status, notes,
                   shift_template_id.name as shift_name,
                   shift_template_id.start_time as start_time,
                   shift_template_id.end_time as end_time
            FROM Schedule
            WHERE employee_id = :emp_rid
            AND date BETWEEN :start_date AND :end_date
            ORDER BY date
        """
        return self.query(sql, {
            'emp_rid': employee_rid,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        })

    def create_schedule(self, schedule_data: Dict) -> bool:
        """Create a new schedule entry"""
        sql = """
            INSERT INTO Schedule SET
            employee_id = :employee_id,
            shift_template_id = :shift_template_id,
            date = :date,
            status = :status,
            notes = :notes
        """
        try:
            result = self.command(sql, schedule_data)
            return result > 0
        except Exception as e:
            self.logger.error(f"Error creating schedule: {e}")
            return False

    # Attendance Management Methods
    def clock_in(self, employee_rid: str, timestamp: datetime = None) -> bool:
        """Record clock in"""
        if timestamp is None:
            timestamp = datetime.now()

        attendance_data = {
            'employee_id': employee_rid,
            'date': timestamp.date().isoformat(),
            'clock_in_time': timestamp.isoformat(),
            'status': 'present'
        }

        sql = """
            INSERT INTO AttendanceRecord SET
            employee_id = :employee_id,
            date = :date,
            clock_in_time = :clock_in_time,
            status = :status
        """
        try:
            result = self.command(sql, attendance_data)
            return result > 0
        except Exception as e:
            self.logger.error(f"Clock in failed: {e}")
            return False

    def clock_out(self, employee_rid: str, timestamp: datetime = None) -> bool:
        """Record clock out"""
        if timestamp is None:
            timestamp = datetime.now()

        # Find today's attendance record and update it
        sql = """
            UPDATE AttendanceRecord SET
            clock_out_time = :clock_out_time,
            hours_worked = TIMESTAMPDIFF(HOUR, clock_in_time, :clock_out_time)
            WHERE employee_id = :employee_id
            AND date = :date
            AND clock_out_time IS NULL
        """
        try:
            result = self.command(sql, {
                'employee_id': employee_rid,
                'date': timestamp.date().isoformat(),
                'clock_out_time': timestamp.isoformat()
            })
            return result > 0
        except Exception as e:
            self.logger.error(f"Clock out failed: {e}")
            return False

    def get_attendance_records(self, employee_rid: str, start_date: date, end_date: date) -> List[Dict]:
        """Get attendance records for an employee in a date range"""
        sql = """
            SELECT @rid.asString() as rid, date, clock_in_time, clock_out_time,
                   hours_worked, status, location, notes
            FROM AttendanceRecord
            WHERE employee_id = :emp_rid
            AND date BETWEEN :start_date AND :end_date
            ORDER BY date DESC
        """
        return self.query(sql, {
            'emp_rid': employee_rid,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        })

    # Leave Management Methods
    def get_leave_balance(self, employee_rid: str) -> Dict[str, float]:
        """Get leave balance for an employee"""
        sql = """
            SELECT leave_type_id.name as leave_type,
                   leave_type_id.days_per_year as days_per_year,
                   COALESCE(SUM(days_requested), 0) as used_days
            FROM LeaveRequest
            WHERE employee_id = :emp_rid
            AND status = 'approved'
            GROUP BY leave_type_id
        """
        balances = self.query(sql, {'emp_rid': employee_rid})

        # Calculate remaining days for each leave type
        result = {}
        for balance in balances:
            leave_type = balance.get('leave_type', 'Unknown')
            total_days = balance.get('days_per_year', 0)
            used_days = balance.get('used_days', 0)
            result[leave_type] = total_days - used_days

        return result

    def submit_leave_request(self, employee_rid: str, leave_type_rid: str,
                           start_date: date, end_date: date, reason: str) -> bool:
        """Submit a leave request"""
        from dateutil import rrule
        import math

        # Calculate business days
        business_days = 0
        for dt in rrule.rrule(rrule.DAILY, dtstart=start_date, until=end_date):
            if dt.weekday() < 5:  # Monday to Friday
                business_days += 1

        request_data = {
            'employee_id': employee_rid,
            'leave_type_id': leave_type_rid,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'days_requested': business_days,
            'reason': reason,
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }

        sql = """
            INSERT INTO LeaveRequest SET
            employee_id = :employee_id,
            leave_type_id = :leave_type_id,
            start_date = :start_date,
            end_date = :end_date,
            days_requested = :days_requested,
            reason = :reason,
            status = :status,
            created_at = :created_at
        """
        try:
            result = self.command(sql, request_data)
            return result > 0
        except Exception as e:
            self.logger.error(f"Leave request submission failed: {e}")
            return False

    def get_leave_requests(self, employee_rid: str = None, status: str = None) -> List[Dict]:
        """Get leave requests, optionally filtered"""
        conditions = []
        params = {}

        if employee_rid:
            conditions.append("employee_id = :emp_rid")
            params['emp_rid'] = employee_rid

        if status:
            conditions.append("status = :status")
            params['status'] = status

        where_clause = " AND ".join(conditions) if conditions else "true"

        sql = f"""
            SELECT @rid.asString() as rid, start_date, end_date, days_requested,
                   reason, status, created_at,
                   leave_type_id.name as leave_type_name,
                   employee_id.first_name as emp_first_name,
                   employee_id.last_name as emp_last_name
            FROM LeaveRequest
            WHERE {where_clause}
            ORDER BY created_at DESC
        """

        return self.query(sql, params)

    # Shift Template Methods
    def get_shift_templates(self) -> List[Dict]:
        """Get all active shift templates"""
        sql = """
            SELECT @rid.asString() as rid, name, description, start_time, end_time,
                   duration_hours, break_duration, is_active
            FROM ShiftTemplate
            WHERE is_active = true
            ORDER BY name
        """
        return self.query(sql)

    # Reporting Methods
    def get_attendance_summary(self, start_date: date, end_date: date,
                             department_rid: str = None) -> List[Dict]:
        """Get attendance summary for reporting"""
        conditions = []
        params = {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        }

        if department_rid:
            conditions.append("department_id = :dept_rid")
            params['dept_rid'] = department_rid

        where_clause = " AND ".join(conditions) if conditions else "true"

        sql = f"""
            SELECT employee_id.@rid.asString() as employee_rid,
                   employee_id.first_name as first_name,
                   employee_id.last_name as last_name,
                   employee_id.employee_id as employee_id,
                   department_id.name as department_name,
                   COUNT(*) as total_days,
                   SUM(CASE WHEN clock_in_time IS NOT NULL THEN 1 ELSE 0 END) as present_days,
                   SUM(hours_worked) as total_hours
            FROM AttendanceRecord
            WHERE date BETWEEN :start_date AND :end_date
            AND employee_id.is_active = true
            AND ({where_clause})
            GROUP BY employee_id, department_id
            ORDER BY department_name, last_name, first_name
        """

        return self.query(sql, params)

    def get_leave_summary(self, year: int, department_rid: str = None) -> List[Dict]:
        """Get leave summary for the year"""
        conditions = []
        params = {'year': str(year)}

        if department_rid:
            conditions.append("employee_id.department_id = :dept_rid")
            params['dept_rid'] = department_rid

        where_clause = " AND ".join(conditions) if conditions else "true"

        sql = f"""
            SELECT employee_id.@rid.asString() as employee_rid,
                   employee_id.first_name as first_name,
                   employee_id.last_name as last_name,
                   employee_id.employee_id as employee_id,
                   employee_id.department_id.name as department_name,
                   SUM(CASE WHEN status = 'approved' THEN days_requested ELSE 0 END) as approved_days,
                   SUM(CASE WHEN status = 'pending' THEN days_requested ELSE 0 END) as pending_days
            FROM LeaveRequest
            WHERE YEAR(start_date) = :year
            AND employee_id.is_active = true
            AND ({where_clause})
            GROUP BY employee_id
            ORDER BY department_name, last_name, first_name
        """

        return self.query(sql, params)

# Global database service instance
db_service = OrientDBService()