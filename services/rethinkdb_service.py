"""
RethinkDB Service for HR Management System
Provides database operations for the HRMS application
"""

from rethinkdb import RethinkDB
from rethinkdb.errors import ReqlDriverError, ReqlRuntimeError
import logging
import os
from typing import Optional, Dict, List, Any
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class RethinkDBService:
    """RethinkDB database service"""
    
    def __init__(self):
        self.r = RethinkDB()
        self.conn = None
        self.config = {
            'host': os.getenv('RETHINKDB_HOST', 'localhost'),
            'port': int(os.getenv('RETHINKDB_PORT', 28015)),
            'db': os.getenv('RETHINKDB_DATABASE', 'hrms'),
            'user': os.getenv('RETHINKDB_USER', 'admin'),
            'password': os.getenv('RETHINKDB_PASSWORD', '')
        }
        self.is_connected = False
    
    def connect(self) -> bool:
        """Connect to RethinkDB"""
        try:
            logger.info(f"Connecting to RethinkDB at {self.config['host']}:{self.config['port']}")
            
            self.conn = self.r.connect(
                host=self.config['host'],
                port=self.config['port'],
                db=self.config['db'],
                user=self.config.get('user'),
                password=self.config.get('password')
            )
            
            self.is_connected = True
            logger.info("RethinkDB connection established successfully")
            return True
            
        except (ReqlDriverError, ReqlRuntimeError) as e:
            logger.error(f"RethinkDB connection failed: {e}")
            self.is_connected = False
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.is_connected = False
            logger.info("RethinkDB connection closed")
    
    def get_connection(self):
        """Get the current connection"""
        if not self.is_connected or not self.conn:
            self.connect()
        return self.conn
    
    # Employee operations
    def get_employee(self, employee_id: str) -> Optional[Dict]:
        """Get employee by ID"""
        try:
            result = self.r.table('employees').get(employee_id).run(self.get_connection())
            return result
        except Exception as e:
            logger.error(f"Error getting employee {employee_id}: {e}")
            return None
    
    def get_employee_by_email(self, email: str) -> Optional[Dict]:
        """Get employee by email"""
        try:
            result = list(self.r.table('employees').filter({'email': email}).run(self.get_connection()))
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Error getting employee by email {email}: {e}")
            return None
    
    def get_all_employees(self, status: Optional[str] = None) -> List[Dict]:
        """Get all employees, optionally filtered by status"""
        try:
            query = self.r.table('employees')
            if status:
                query = query.filter({'status': status})
            return list(query.run(self.get_connection()))
        except Exception as e:
            logger.error(f"Error getting employees: {e}")
            return []
    
    def create_employee(self, employee_data: Dict) -> bool:
        """Create a new employee"""
        try:
            result = self.r.table('employees').insert(employee_data).run(self.get_connection())
            return result.get('inserted', 0) > 0
        except Exception as e:
            logger.error(f"Error creating employee: {e}")
            return False
    
    def update_employee(self, employee_id: str, updates: Dict) -> bool:
        """Update employee data"""
        try:
            result = self.r.table('employees').get(employee_id).update(updates).run(self.get_connection())
            return result.get('replaced', 0) > 0 or result.get('unchanged', 0) > 0
        except Exception as e:
            logger.error(f"Error updating employee {employee_id}: {e}")
            return False
    
    # User operations
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        try:
            result = list(self.r.table('users').filter({'username': username}).run(self.get_connection()))
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Error getting user {username}: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        try:
            result = list(self.r.table('users').filter({'email': email}).run(self.get_connection()))
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {e}")
            return None
    
    def create_user(self, user_data: Dict) -> bool:
        """Create a new user"""
        try:
            result = self.r.table('users').insert(user_data).run(self.get_connection())
            return result.get('inserted', 0) > 0
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return False
    
    # Attendance operations
    def create_attendance(self, attendance_data: Dict) -> bool:
        """Create attendance record"""
        try:
            result = self.r.table('attendance_records').insert(attendance_data).run(self.get_connection())
            return result.get('inserted', 0) > 0
        except Exception as e:
            logger.error(f"Error creating attendance: {e}")
            return False
    
    def get_attendance_by_date(self, date: str) -> List[Dict]:
        """Get all attendance records for a date"""
        try:
            return list(self.r.table('attendance_records').filter({'attendanceDate': date}).run(self.get_connection()))
        except Exception as e:
            logger.error(f"Error getting attendance for {date}: {e}")
            return []
    
    # Department operations
    def get_all_departments(self) -> List[Dict]:
        """Get all departments"""
        try:
            return list(self.r.table('departments').run(self.get_connection()))
        except Exception as e:
            logger.error(f"Error getting departments: {e}")
            return []
    
    def get_department(self, department_id: str) -> Optional[Dict]:
        """Get department by ID"""
        try:
            result = self.r.table('departments').get(department_id).run(self.get_connection())
            return result
        except Exception as e:
            logger.error(f"Error getting department {department_id}: {e}")
            return None
    
    # Leave request operations
    def create_leave_request(self, leave_data: Dict) -> bool:
        """Create leave request"""
        try:
            result = self.r.table('leave_requests').insert(leave_data).run(self.get_connection())
            return result.get('inserted', 0) > 0
        except Exception as e:
            logger.error(f"Error creating leave request: {e}")
            return False
    
    def get_leave_requests(self, employee_id: Optional[str] = None, status: Optional[str] = None) -> List[Dict]:
        """Get leave requests, optionally filtered"""
        try:
            query = self.r.table('leave_requests')
            if employee_id:
                query = query.filter({'employeeId': employee_id})
            if status:
                query = query.filter({'status': status})
            return list(query.run(self.get_connection()))
        except Exception as e:
            logger.error(f"Error getting leave requests: {e}")
            return []
    
    # System settings
    def get_system_settings(self) -> Optional[Dict]:
        """Get system settings"""
        try:
            result = self.r.table('system_settings').get('settings').run(self.get_connection())
            return result
        except Exception as e:
            logger.error(f"Error getting system settings: {e}")
            return None
    
    def update_system_settings(self, settings: Dict) -> bool:
        """Update system settings"""
        try:
            result = self.r.table('system_settings').get('settings').update(settings).run(self.get_connection())
            return result.get('replaced', 0) > 0 or result.get('unchanged', 0) > 0
        except Exception as e:
            logger.error(f"Error updating system settings: {e}")
            return False
    
    # User authentication methods
    def get_user_by_username_or_email(self, username_or_email: str) -> Optional[Dict[str, Any]]:
        """Get user by username or email"""
        try:
            # First try to find by username
            result = list(self.r.table('users').filter(
                lambda user: user['username'].eq(username_or_email)
            ).run(self.get_connection()))
            
            if not result:
                # Try to find by email
                result = list(self.r.table('users').filter(
                    lambda user: user['email'].eq(username_or_email)
                ).run(self.get_connection()))
            
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Error getting user by username/email {username_or_email}: {e}")
            return None
    
    def update_user_last_login(self, user_id: str) -> bool:
        """Update user's last login timestamp"""
        try:
            from datetime import datetime
            result = self.r.table('users').get(user_id).update({
                'last_login': datetime.now().isoformat()
            }).run(self.get_connection())
            return result.get('replaced', 0) > 0
        except Exception as e:
            logger.error(f"Error updating last login for user {user_id}: {e}")
            return False

# Global instance
rethinkdb_service = RethinkDBService()
