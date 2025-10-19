"""
OrientDB Database Service for Data Persistence

Handles database connections, queries, and operations using OrientDB REST API
"""

import logging
import requests
from typing import List, Dict, Any, Optional
from config.services import config
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)


class DatabaseService:
    """OrientDB Database service for data persistence"""

    def __init__(self):
        self.base_url = f"https://{config.ORIENTDB_HOST}"
        self.database = config.ORIENTDB_DATABASE
        self.auth = HTTPBasicAuth(config.ORIENTDB_USER, config.ORIENTDB_PASSWORD)
        self.is_connected = False
        # Don't create session during init to avoid FastAPI conflicts
        self.session = None
        # Set a reasonable timeout to prevent hanging
        self.timeout = 10

    def connect(self) -> bool:
        """Test database connectivity"""
        try:
            # Create session when connecting
            self.session = requests.Session()
            self.session.auth = self.auth
            
            url = f"{self.base_url}/database/{self.database}"
            response = self.session.get(url, timeout=self.timeout)

            if response.status_code == 200:
                self.is_connected = True
                logger.info("OrientDB connection established successfully")
                return True
            else:
                logger.error(f"Database connection failed with status: {response.status_code}")
                self.is_connected = False
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Database connection failed: {e}")
            self.is_connected = False
            return False

    def disconnect(self):
        """Close database connection"""
        self.is_connected = False
        self.session.close()
        logger.info("Database connection closed")

    def execute_query(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Execute SELECT query and return results"""
        if not self.is_connected:
            logger.warning("Database not connected, attempting to connect...")
            if not self.connect():
                return []

        try:
            url = f"{self.base_url}/query/{self.database}/sql/{query}"
            response = self.session.get(url, timeout=self.timeout)

            if response.status_code == 200:
                data = response.json()
                return data.get('result', [])
            else:
                logger.error(f"Query failed with status {response.status_code}: {response.text}")
                return []

        except requests.exceptions.RequestException as e:
            logger.error(f"Query execution failed: {e}")
            return []

    def execute_command(self, command: str, params: Dict[str, Any] = None) -> bool:
        """Execute INSERT, UPDATE, DELETE commands"""
        if not self.is_connected:
            logger.warning("Database not connected, attempting to connect...")
            if not self.connect():
                return False

        try:
            url = f"{self.base_url}/command/{self.database}/sql/{command}"
            response = self.session.post(url, timeout=self.timeout)

            if response.status_code in [200, 201]:
                logger.info("Command executed successfully")
                return True
            else:
                logger.error(f"Command failed with status {response.status_code}: {response.text}")
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Command execution failed: {e}")
            return False

    def get_employee_by_id(self, employee_id: str) -> Optional[Dict[str, Any]]:
        """Get employee by employee_id"""
        query = f"SELECT FROM Employee WHERE employee_id = '{employee_id}'"
        results = self.execute_query(query)
        return results[0] if results else None

    def get_employee_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get employee by email"""
        query = f"SELECT FROM Employee WHERE email = '{email}'"
        results = self.execute_query(query)
        return results[0] if results else None

    def get_all_employees(self) -> List[Dict[str, Any]]:
        """Get all employees"""
        query = "SELECT FROM Employee"
        return self.execute_query(query)

    def get_departments(self) -> List[Dict[str, Any]]:
        """Get all departments"""
        query = "SELECT FROM Department"
        return self.execute_query(query)

    def get_attendance_records(self, employee_id: str = None, date: str = None) -> List[Dict[str, Any]]:
        """Get attendance records with optional filters"""
        conditions = []
        if employee_id:
            conditions.append(f"employee_id = '{employee_id}'")
        if date:
            conditions.append(f"date = '{date}'")

        where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
        query = f"SELECT FROM AttendanceRecord{where_clause}"
        return self.execute_query(query)

    def create_employee(self, employee_data: Dict[str, Any]) -> bool:
        """Create a new employee record"""
        # Build INSERT command
        fields = ", ".join(employee_data.keys())
        values = ", ".join([f"'{v}'" if isinstance(v, str) else str(v) for v in employee_data.values()])
        command = f"INSERT INTO Employee ({fields}) VALUES ({values})"
        return self.execute_command(command)

    def update_employee(self, employee_id: str, update_data: Dict[str, Any]) -> bool:
        """Update employee record"""
        set_clause = ", ".join([f"{k} = '{v}'" if isinstance(v, str) else f"{k} = {v}"
                               for k, v in update_data.items()])
        command = f"UPDATE Employee SET {set_clause} WHERE employee_id = '{employee_id}'"
        return self.execute_command(command)

    def create_attendance_record(self, attendance_data: Dict[str, Any]) -> bool:
        """Create attendance record"""
        fields = ", ".join(attendance_data.keys())
        values = ", ".join([f"'{v}'" if isinstance(v, str) else str(v) for v in attendance_data.values()])
        command = f"INSERT INTO AttendanceRecord ({fields}) VALUES ({values})"
        return self.execute_command(command)

    def get_leave_requests(self, employee_id: str = None, status: str = None) -> List[Dict[str, Any]]:
        """Get leave requests with optional filters"""
        conditions = []
        if employee_id:
            conditions.append(f"employee_id = '{employee_id}'")
        if status:
            conditions.append(f"status = '{status}'")

        where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
        query = f"SELECT FROM LeaveRequest{where_clause}"
        return self.execute_query(query)

    def create_leave_request(self, leave_data: Dict[str, Any]) -> bool:
        """Create leave request"""
        fields = ", ".join(leave_data.keys())
        values = ", ".join([f"'{v}'" if isinstance(v, str) else str(v) for v in leave_data.values()])
        command = f"INSERT INTO LeaveRequest ({fields}) VALUES ({values})"
        return self.execute_command(command)

    def get_system_settings(self) -> Dict[str, Any]:
        """Get all system settings"""
        query = "SELECT FROM SystemSetting"
        results = self.execute_query(query)
        return {setting['key']: setting['value'] for setting in results}

    def update_system_setting(self, key: str, value: str) -> bool:
        """Update or create system setting"""
        # First check if setting exists
        query = f"SELECT FROM SystemSetting WHERE key = '{key}'"
        results = self.execute_query(query)

        if results:
            # Update existing
            command = f"UPDATE SystemSetting SET value = '{value}' WHERE key = '{key}'"
        else:
            # Create new
            command = f"INSERT INTO SystemSetting (key, value) VALUES ('{key}', '{value}')"

        return self.execute_command(command)


# Global database service instance
database_service = DatabaseService()

def get_database_service():
    """Get global database service instance"""
    return database_service
