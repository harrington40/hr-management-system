"""
Comprehensive HRMS gRPC Service Implementation
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import json

import grpc
from concurrent import futures
from google.protobuf import json_format

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from grpc_services.proto import hrms_pb2, hrms_pb2_grpc
from services.database_service import DatabaseService
from services.auth_service import AuthService
from helperFuns.helperFuns import HelperFunctions

logger = logging.getLogger(__name__)


class HRMSService(hrms_pb2_grpc.HRMSServiceServicer):
    """Comprehensive HRMS gRPC service implementation"""

    def __init__(self, db_service: DatabaseService, auth_service: AuthService):
        self.db_service = db_service
        self.auth_service = auth_service
        self.helper = HelperFunctions()

    # User operations
    def GetUser(self, request, context):
        """Get a user by ID"""
        try:
            user_id = request.user_id
            query = f"SELECT FROM User WHERE id = '{user_id}'"
            result = self.db_service.execute_query(query)

            if not result:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return hrms_pb2.UserResponse()

            user_data = result[0]
            user_proto = self._user_data_to_proto(user_data)

            return hrms_pb2.UserResponse(user=user_proto, message="User retrieved successfully")
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return hrms_pb2.UserResponse()

    def ListUsers(self, request, context):
        """List users with pagination and search"""
        try:
            page = request.page or 1
            limit = request.limit or 10
            search = request.search or ""

            skip = (page - 1) * limit

            query = "SELECT FROM User"
            conditions = []

            if search:
                conditions.append(f"(username.toLowerCase() CONTAINS '{search.lower()}' OR email.toLowerCase() CONTAINS '{search.lower()}')")

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += f" SKIP {skip} LIMIT {limit}"

            result = self.db_service.execute_query(query)
            total_query = f"SELECT COUNT(*) FROM User" + (" WHERE " + " AND ".join(conditions) if conditions else "")
            total_result = self.db_service.execute_query(total_query)
            total = total_result[0]['COUNT'] if total_result else 0

            users = [self._user_data_to_proto(user_data) for user_data in result]

            return hrms_pb2.ListUsersResponse(
                users=users,
                total=total,
                page=page,
                limit=limit
            )
        except Exception as e:
            logger.error(f"Error listing users: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return hrms_pb2.ListUsersResponse()

    def CreateUser(self, request, context):
        """Create a new user"""
        try:
            user_data = self._proto_to_user_data(request.user)

            # Hash password
            user_data['password_hash'] = self.auth_service.hash_password(user_data['password_hash'])

            # Generate ID if not provided
            if not user_data.get('id'):
                user_data['id'] = self.helper.generate_id()

            user_data['created_at'] = datetime.now().isoformat()
            user_data['updated_at'] = datetime.now().isoformat()

            query = f"INSERT INTO User CONTENT {json.dumps(user_data)}"
            result = self.db_service.execute_query(query)

            if result:
                user_proto = self._user_data_to_proto(result[0])
                return hrms_pb2.UserResponse(user=user_proto, message="User created successfully")
            else:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to create user")
                return hrms_pb2.UserResponse()

        except Exception as e:
            logger.error(f"Error creating user: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return hrms_pb2.UserResponse()

    def UpdateUser(self, request, context):
        """Update an existing user"""
        try:
            user_id = request.user_id
            user_data = self._proto_to_user_data(request.user)

            # Don't update password hash unless explicitly provided
            if 'password_hash' in user_data and user_data['password_hash']:
                user_data['password_hash'] = self.auth_service.hash_password(user_data['password_hash'])
            else:
                del user_data['password_hash']

            user_data['updated_at'] = datetime.now().isoformat()

            # Remove None values
            user_data = {k: v for k, v in user_data.items() if v is not None}

            query = f"UPDATE User SET {', '.join([f'{k} = {json.dumps(v)}' for k, v in user_data.items()])} WHERE id = '{user_id}'"
            result = self.db_service.execute_query(query)

            if result:
                user_proto = self._user_data_to_proto(result[0])
                return hrms_pb2.UserResponse(user=user_proto, message="User updated successfully")
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return hrms_pb2.UserResponse()

        except Exception as e:
            logger.error(f"Error updating user: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return hrms_pb2.UserResponse()

    def DeleteUser(self, request, context):
        """Delete a user"""
        try:
            user_id = request.user_id

            query = f"DELETE FROM User WHERE id = '{user_id}'"
            result = self.db_service.execute_query(query)

            if result:
                return hrms_pb2.DeleteResponse(success=True, message="User deleted successfully")
            else:
                return hrms_pb2.DeleteResponse(success=False, message="User not found")

        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            return hrms_pb2.DeleteResponse(success=False, message=str(e))

    def AuthenticateUser(self, request, context):
        """Authenticate a user"""
        try:
            username = request.username
            password = request.password

            success, token, user_data = self.auth_service.authenticate_user(username, password)

            if success:
                user_proto = self._user_data_to_proto(user_data) if user_data else None
                return hrms_pb2.AuthenticateResponse(
                    success=True,
                    token=token,
                    user=user_proto,
                    message="Authentication successful"
                )
            else:
                return hrms_pb2.AuthenticateResponse(
                    success=False,
                    message="Invalid credentials"
                )

        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            return hrms_pb2.AuthenticateResponse(
                success=False,
                message=str(e)
            )

    # Employee operations
    def GetEmployee(self, request, context):
        """Get an employee by ID"""
        try:
            employee_id = request.employee_id
            query = f"SELECT FROM Employee WHERE id = '{employee_id}'"
            result = self.db_service.execute_query(query)

            if not result:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Employee not found")
                return hrms_pb2.EmployeeResponse()

            employee_data = result[0]
            employee_proto = self._employee_data_to_proto(employee_data)

            return hrms_pb2.EmployeeResponse(employee=employee_proto, message="Employee retrieved successfully")
        except Exception as e:
            logger.error(f"Error getting employee: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return hrms_pb2.EmployeeResponse()

    def ListEmployees(self, request, context):
        """List employees with filters"""
        try:
            page = request.page or 1
            limit = request.limit or 10
            search = request.search or ""
            department_id = request.department_id or ""
            position_id = request.position_id or ""

            skip = (page - 1) * limit

            query = "SELECT FROM Employee"
            conditions = []

            if search:
                conditions.append(f"(first_name.toLowerCase() CONTAINS '{search.lower()}' OR last_name.toLowerCase() CONTAINS '{search.lower()}' OR email.toLowerCase() CONTAINS '{search.lower()}')")

            if department_id:
                conditions.append(f"department_id = '{department_id}'")

            if position_id:
                conditions.append(f"position_id = '{position_id}'")

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += f" SKIP {skip} LIMIT {limit}"

            result = self.db_service.execute_query(query)
            total_query = f"SELECT COUNT(*) FROM Employee" + (" WHERE " + " AND ".join(conditions) if conditions else "")
            total_result = self.db_service.execute_query(total_query)
            total = total_result[0]['COUNT'] if total_result else 0

            employees = [self._employee_data_to_proto(emp_data) for emp_data in result]

            return hrms_pb2.ListEmployeesResponse(
                employees=employees,
                total=total,
                page=page,
                limit=limit
            )
        except Exception as e:
            logger.error(f"Error listing employees: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return hrms_pb2.ListEmployeesResponse()

    def CreateEmployee(self, request, context):
        """Create a new employee"""
        try:
            employee_data = self._proto_to_employee_data(request.employee)

            # Generate ID and employee number if not provided
            if not employee_data.get('id'):
                employee_data['id'] = self.helper.generate_id()

            if not employee_data.get('employee_number'):
                employee_data['employee_number'] = self.helper.generate_employee_number()

            employee_data['created_at'] = datetime.now().isoformat()
            employee_data['updated_at'] = datetime.now().isoformat()

            query = f"INSERT INTO Employee CONTENT {json.dumps(employee_data)}"
            result = self.db_service.execute_query(query)

            if result:
                employee_proto = self._employee_data_to_proto(result[0])
                return hrms_pb2.EmployeeResponse(employee=employee_proto, message="Employee created successfully")
            else:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to create employee")
                return hrms_pb2.EmployeeResponse()

        except Exception as e:
            logger.error(f"Error creating employee: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return hrms_pb2.EmployeeResponse()

    def UpdateEmployee(self, request, context):
        """Update an existing employee"""
        try:
            employee_id = request.employee_id
            employee_data = self._proto_to_employee_data(request.employee)

            employee_data['updated_at'] = datetime.now().isoformat()

            # Remove None values
            employee_data = {k: v for k, v in employee_data.items() if v is not None}

            query = f"UPDATE Employee SET {', '.join([f'{k} = {json.dumps(v)}' for k, v in employee_data.items()])} WHERE id = '{employee_id}'"
            result = self.db_service.execute_query(query)

            if result:
                employee_proto = self._employee_data_to_proto(result[0])
                return hrms_pb2.EmployeeResponse(employee=employee_proto, message="Employee updated successfully")
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Employee not found")
                return hrms_pb2.EmployeeResponse()

        except Exception as e:
            logger.error(f"Error updating employee: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return hrms_pb2.EmployeeResponse()

    def DeleteEmployee(self, request, context):
        """Delete an employee"""
        try:
            employee_id = request.employee_id

            query = f"DELETE FROM Employee WHERE id = '{employee_id}'"
            result = self.db_service.execute_query(query)

            if result:
                return hrms_pb2.DeleteResponse(success=True, message="Employee deleted successfully")
            else:
                return hrms_pb2.DeleteResponse(success=False, message="Employee not found")

        except Exception as e:
            logger.error(f"Error deleting employee: {e}")
            return hrms_pb2.DeleteResponse(success=False, message=str(e))

    # Helper methods for data conversion
    def _user_data_to_proto(self, data: Dict[str, Any]) -> hrms_pb2.User:
        """Convert user data from database to protobuf"""
        user = hrms_pb2.User()
        for key, value in data.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, str(value) if not isinstance(value, (str, int, float, bool)) else value)
        return user

    def _proto_to_user_data(self, proto) -> Dict[str, Any]:
        """Convert user protobuf to database data"""
        data = {}
        for field in proto.DESCRIPTOR.fields:
            value = getattr(proto, field.name)
            if value:
                data[field.name] = value
        return data

    def _employee_data_to_proto(self, data: Dict[str, Any]) -> hrms_pb2.Employee:
        """Convert employee data from database to protobuf"""
        employee = hrms_pb2.Employee()
        for key, value in data.items():
            if hasattr(employee, key) and value is not None:
                setattr(employee, key, str(value) if not isinstance(value, (str, int, float, bool)) else value)
        return employee

    def _proto_to_employee_data(self, proto) -> Dict[str, Any]:
        """Convert employee protobuf to database data"""
        data = {}
        for field in proto.DESCRIPTOR.fields:
            value = getattr(proto, field.name)
            if value:
                data[field.name] = value
        return data


def serve():
    """Start the gRPC server"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Initialize services
    db_service = DatabaseService()
    auth_service = AuthService(db_service)

    # Add service to server
    hrms_pb2_grpc.add_HRMSServiceServicer_to_server(
        HRMSService(db_service, auth_service), server
    )

    server.add_insecure_port('[::]:50051')
    server.start()
    logger.info("gRPC server started on port 50051")

    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()