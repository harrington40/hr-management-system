"""
HRMS gRPC Client
Client for testing and interacting with HRMS gRPC services
"""

import grpc
import logging
from typing import Optional, Dict, Any
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from grpc_services.proto import hrms_pb2, hrms_pb2_grpc

logger = logging.getLogger(__name__)


class HRMSGrpcClient:
    """Client for HRMS gRPC services"""

    def __init__(self, host: str = 'localhost', port: int = 50051):
        self.target = f"{host}:{port}"
        self.channel = None
        self.stub = None

    def connect(self) -> bool:
        """Connect to gRPC server"""
        try:
            self.channel = grpc.insecure_channel(self.target)
            self.stub = hrms_pb2_grpc.HRMSServiceStub(self.channel)
            logger.info(f"Connected to gRPC server at {self.target}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to gRPC server: {e}")
            return False

    def disconnect(self):
        """Disconnect from gRPC server"""
        if self.channel:
            self.channel.close()
            self.channel = None
            self.stub = None
            logger.info("Disconnected from gRPC server")

    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate a user"""
        try:
            request = hrms_pb2.AuthenticateRequest(username=username, password=password)
            response = self.stub.AuthenticateUser(request)

            if response.success:
                return {
                    'success': True,
                    'token': response.token,
                    'user': self._proto_to_dict(response.user) if response.user else None,
                    'message': response.message
                }
            else:
                return {
                    'success': False,
                    'message': response.message
                }
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return None

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            request = hrms_pb2.UserRequest(user_id=user_id)
            response = self.stub.GetUser(request)
            return self._proto_to_dict(response.user) if response.user else None
        except Exception as e:
            logger.error(f"Failed to get user: {e}")
            return None

    def list_users(self, page: int = 1, limit: int = 10, search: str = "") -> Optional[Dict[str, Any]]:
        """List users with pagination"""
        try:
            request = hrms_pb2.ListUsersRequest(page=page, limit=limit, search=search)
            response = self.stub.ListUsers(request)
            return {
                'users': [self._proto_to_dict(user) for user in response.users],
                'total': response.total,
                'page': response.page,
                'limit': response.limit
            }
        except Exception as e:
            logger.error(f"Failed to list users: {e}")
            return None

    def create_user(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new user"""
        try:
            user_proto = self._dict_to_user_proto(user_data)
            request = hrms_pb2.CreateUserRequest(user=user_proto)
            response = self.stub.CreateUser(request)
            return self._proto_to_dict(response.user) if response.user else None
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            return None

    def get_employee(self, employee_id: str) -> Optional[Dict[str, Any]]:
        """Get employee by ID"""
        try:
            request = hrms_pb2.EmployeeRequest(employee_id=employee_id)
            response = self.stub.GetEmployee(request)
            return self._proto_to_dict(response.employee) if response.employee else None
        except Exception as e:
            logger.error(f"Failed to get employee: {e}")
            return None

    def list_employees(self, page: int = 1, limit: int = 10, search: str = "",
                      department_id: str = "", position_id: str = "") -> Optional[Dict[str, Any]]:
        """List employees with filters"""
        try:
            request = hrms_pb2.ListEmployeesRequest(
                page=page, limit=limit, search=search,
                department_id=department_id, position_id=position_id
            )
            response = self.stub.ListEmployees(request)
            return {
                'employees': [self._proto_to_dict(emp) for emp in response.employees],
                'total': response.total,
                'page': response.page,
                'limit': response.limit
            }
        except Exception as e:
            logger.error(f"Failed to list employees: {e}")
            return None

    def create_employee(self, employee_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new employee"""
        try:
            employee_proto = self._dict_to_employee_proto(employee_data)
            request = hrms_pb2.CreateEmployeeRequest(employee=employee_proto)
            response = self.stub.CreateEmployee(request)
            return self._proto_to_dict(response.employee) if response.employee else None
        except Exception as e:
            logger.error(f"Failed to create employee: {e}")
            return None

    def get_dashboard_stats(self, date_from: str = "", date_to: str = "") -> Optional[Dict[str, Any]]:
        """Get dashboard statistics"""
        try:
            request = hrms_pb2.DashboardRequest(date_from=date_from, date_to=date_to)
            response = self.stub.GetDashboardStats(request)
            return self._proto_to_dict(response.stats) if response.stats else None
        except Exception as e:
            logger.error(f"Failed to get dashboard stats: {e}")
            return None

    def _proto_to_dict(self, proto_message) -> Dict[str, Any]:
        """Convert protobuf message to dictionary"""
        result = {}
        for field in proto_message.DESCRIPTOR.fields:
            value = getattr(proto_message, field.name)
            if value:
                result[field.name] = value
        return result

    def _dict_to_user_proto(self, data: Dict[str, Any]) -> hrms_pb2.User:
        """Convert dictionary to User protobuf"""
        user = hrms_pb2.User()
        for key, value in data.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        return user

    def _dict_to_employee_proto(self, data: Dict[str, Any]) -> hrms_pb2.Employee:
        """Convert dictionary to Employee protobuf"""
        employee = hrms_pb2.Employee()
        for key, value in data.items():
            if hasattr(employee, key) and value is not None:
                setattr(employee, key, value)
        return employee


# Global client instance
hrms_client = HRMSGrpcClient()


def get_hrms_client():
    """Get global HRMS gRPC client instance"""
    return hrms_client


if __name__ == '__main__':
    # Example usage
    logging.basicConfig(level=logging.INFO)

    client = HRMSGrpcClient()
    if client.connect():
        # Test authentication
        auth_result = client.authenticate_user('admin', 'password')
        if auth_result and auth_result['success']:
            print(f"Authentication successful: {auth_result['token']}")

            # Test getting users
            users = client.list_users()
            if users:
                print(f"Found {users['total']} users")

        client.disconnect()