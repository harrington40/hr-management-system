"""
HRMS gRPC Service Implementation
Provides gRPC endpoints for HRMS operations
"""

import logging
import grpc
from concurrent import futures
from typing import List, Dict, Any
from services.database_service import database_service
from config.services import config

logger = logging.getLogger(__name__)

# Simple message classes (since we don't have proto generated code)
class EmployeeMessage:
    def __init__(self, employee_id="", first_name="", last_name="", email="", department="", position="", hire_date="", status=""):
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.department = department
        self.position = position
        self.hire_date = hire_date
        self.status = status

class DepartmentMessage:
    def __init__(self, id="", name="", description="", budget=0.0, location="", is_active=True):
        self.id = id
        self.name = name
        self.description = description
        self.budget = budget
        self.location = location
        self.is_active = is_active

class AttendanceMessage:
    def __init__(self, id="", employee_id="", check_in="", check_out="", date="", status="", notes=""):
        self.id = id
        self.employee_id = employee_id
        self.check_in = check_in
        self.check_out = check_out
        self.date = date
        self.status = status
        self.notes = notes

class HRMSServiceServicer:
    """gRPC service implementation for HRMS"""

    def GetEmployee(self, request, context):
        """Get employee by ID"""
        try:
            query = f"SELECT * FROM Employee WHERE employee_id = '{request.employee_id}'"
            result = database_service.execute_query(query)

            if result and len(result) > 0:
                emp_data = result[0]
                employee = EmployeeMessage(
                    employee_id=emp_data.get('employee_id', ''),
                    first_name=emp_data.get('first_name', ''),
                    last_name=emp_data.get('last_name', ''),
                    email=emp_data.get('email', ''),
                    department=emp_data.get('department', ''),
                    position=emp_data.get('position', ''),
                    hire_date=str(emp_data.get('hire_date', '')),
                    status=emp_data.get('status', 'active')
                )
                return type('EmployeeResponse', (), {'employee': employee, 'error': ''})()
            else:
                return type('EmployeeResponse', (), {'employee': None, 'error': 'Employee not found'})()

        except Exception as e:
            logger.error(f"Error getting employee: {e}")
            return type('EmployeeResponse', (), {'employee': None, 'error': str(e)})()

    def ListEmployees(self, request, context):
        """List employees with pagination"""
        try:
            limit = min(request.limit or 50, 100)  # Max 100 records
            offset = (request.page or 0) * limit

            query = f"SELECT * FROM Employee LIMIT {limit} OFFSET {offset}"
            result = database_service.execute_query(query)

            employees = []
            if result:
                for emp_data in result:
                    employee = EmployeeMessage(
                        employee_id=emp_data.get('employee_id', ''),
                        first_name=emp_data.get('first_name', ''),
                        last_name=emp_data.get('last_name', ''),
                        email=emp_data.get('email', ''),
                        department=emp_data.get('department', ''),
                        position=emp_data.get('position', ''),
                        hire_date=str(emp_data.get('hire_date', '')),
                        status=emp_data.get('status', 'active')
                    )
                    employees.append(employee)

            return type('ListEmployeesResponse', (), {'employees': employees, 'total': len(employees), 'error': ''})()

        except Exception as e:
            logger.error(f"Error listing employees: {e}")
            return type('ListEmployeesResponse', (), {'employees': [], 'total': 0, 'error': str(e)})()

    def GetDepartment(self, request, context):
        """Get department by ID"""
        try:
            query = f"SELECT * FROM Department WHERE @rid = '{request.department_id}'"
            result = database_service.execute_query(query)

            if result and len(result) > 0:
                dept_data = result[0]
                department = DepartmentMessage(
                    id=str(dept_data.get('@rid', '')),
                    name=dept_data.get('name', ''),
                    description=dept_data.get('description', ''),
                    budget=float(dept_data.get('budget', 0.0)),
                    location=dept_data.get('location', ''),
                    is_active=dept_data.get('is_active', True)
                )
                return type('DepartmentResponse', (), {'department': department, 'error': ''})()
            else:
                return type('DepartmentResponse', (), {'department': None, 'error': 'Department not found'})()

        except Exception as e:
            logger.error(f"Error getting department: {e}")
            return type('DepartmentResponse', (), {'department': None, 'error': str(e)})()

    def ListDepartments(self, request, context):
        """List departments with pagination"""
        try:
            limit = min(request.limit or 50, 100)
            offset = (request.page or 0) * limit

            query = f"SELECT * FROM Department LIMIT {limit} OFFSET {offset}"
            result = database_service.execute_query(query)

            departments = []
            if result:
                for dept_data in result:
                    department = DepartmentMessage(
                        id=str(dept_data.get('@rid', '')),
                        name=dept_data.get('name', ''),
                        description=dept_data.get('description', ''),
                        budget=float(dept_data.get('budget', 0.0)),
                        location=dept_data.get('location', ''),
                        is_active=dept_data.get('is_active', True)
                    )
                    departments.append(department)

            return type('ListDepartmentsResponse', (), {'departments': departments, 'total': len(departments), 'error': ''})()

        except Exception as e:
            logger.error(f"Error listing departments: {e}")
            return type('ListDepartmentsResponse', (), {'departments': [], 'total': 0, 'error': str(e)})()

def add_HRMSServiceServicer_to_server(servicer, server):
    """Add HRMS service to gRPC server"""
    # This would normally be generated by protoc
    # For now, we'll manually register the service
    pass

# Create servicer instance
hrms_servicer = HRMSServiceServicer()