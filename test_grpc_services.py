"""
Test script for HRMS gRPC services
Tests all gRPC endpoints to ensure they work correctly
"""

import logging
import time
from grpc_services.client.hrms_client import HRMSGrpcClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_user_operations(client: HRMSGrpcClient):
    """Test user-related operations"""
    logger.info("Testing user operations...")

    # Test creating a user
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password_hash': 'testpass123',
        'role': 'employee',
        'is_active': True
    }

    created_user = client.create_user(user_data)
    if created_user:
        logger.info(f"✓ Created user: {created_user['username']}")
        user_id = created_user['id']

        # Test getting the user
        retrieved_user = client.get_user(user_id)
        if retrieved_user:
            logger.info(f"✓ Retrieved user: {retrieved_user['username']}")
        else:
            logger.error("✗ Failed to retrieve user")

        # Test authentication
        auth_result = client.authenticate_user('testuser', 'testpass123')
        if auth_result and auth_result['success']:
            logger.info(f"✓ Authentication successful for user: {auth_result['user']['username']}")
        else:
            logger.error("✗ Authentication failed")

    # Test listing users
    users_list = client.list_users()
    if users_list:
        logger.info(f"✓ Listed {users_list['total']} users")
    else:
        logger.error("✗ Failed to list users")


def test_employee_operations(client: HRMSGrpcClient):
    """Test employee-related operations"""
    logger.info("Testing employee operations...")

    # Test creating an employee
    employee_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '+1234567890',
        'hire_date': '2024-01-01',
        'status': 'active',
        'salary': 50000.0
    }

    created_employee = client.create_employee(employee_data)
    if created_employee:
        logger.info(f"✓ Created employee: {created_employee['first_name']} {created_employee['last_name']}")
        employee_id = created_employee['id']

        # Test getting the employee
        retrieved_employee = client.get_employee(employee_id)
        if retrieved_employee:
            logger.info(f"✓ Retrieved employee: {retrieved_employee['first_name']} {retrieved_employee['last_name']}")
        else:
            logger.error("✗ Failed to retrieve employee")

    # Test listing employees
    employees_list = client.list_employees()
    if employees_list:
        logger.info(f"✓ Listed {employees_list['total']} employees")
    else:
        logger.error("✗ Failed to list employees")


def test_dashboard_operations(client: HRMSGrpcClient):
    """Test dashboard operations"""
    logger.info("Testing dashboard operations...")

    # Test getting dashboard stats
    stats = client.get_dashboard_stats()
    if stats:
        logger.info(f"✓ Retrieved dashboard stats: {stats}")
    else:
        logger.error("✗ Failed to get dashboard stats")


def run_all_tests():
    """Run all gRPC service tests"""
    logger.info("Starting HRMS gRPC service tests...")

    client = HRMSGrpcClient()

    if not client.connect():
        logger.error("Failed to connect to gRPC server")
        return False

    try:
        # Wait a moment for server to be ready
        time.sleep(1)

        # Run tests
        test_user_operations(client)
        test_employee_operations(client)
        test_dashboard_operations(client)

        logger.info("All tests completed!")
        return True

    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        return False

    finally:
        client.disconnect()


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)