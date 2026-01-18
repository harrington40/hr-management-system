#!/usr/bin/env python3
"""
Simple HRMS Test Data Loader
Creates basic test employees for testing purposes
"""

import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SimpleTestDataLoader:
    """Simple test data loader for HRMS"""

    def __init__(self):
        self.config = {
            'host': os.getenv('ORIENTDB_HOST', 'orientdb.transtechologies.com'),
            'user': os.getenv('ORIENTDB_USER', 'root'),
            'password': os.getenv('ORIENTDB_PASSWORD'),
            'database': os.getenv('ORIENTDB_DATABASE', 'hrms')
        }
        self.base_url = f"https://{self.config['host']}"

    def execute_query(self, query, description=""):
        """Execute SQL query"""
        try:
            command_url = f"{self.base_url}/command/{self.config['database']}/sql"
            # Use direct requests.post instead of session
            response = requests.post(
                command_url,
                auth=HTTPBasicAuth(self.config['user'], self.config['password']),
                data=query,
                headers={'Content-Type': 'text/plain'},
                timeout=30,
                verify=False  # Disable SSL verification for test environment
            )

            if response.status_code == 200:
                if description:
                    print(f"✅ {description}")
                return response.json()
            else:
                print(f"❌ Query failed: {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                return None

        except Exception as e:
            print(f"❌ Error: {e}")
            return None

    def create_test_employees(self):
        """Create test employees"""
        print("👥 Creating test employees...")

        employees = [
            {
                'email': 'john.doe@test.com',
                'password': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6fYzYXkqO',
                'role': 'employee',
                'employee_id': 'TEST001',
                'first_name': 'John',
                'last_name': 'Doe',
                'hire_date': '2024-01-15',
                'salary': 50000.00,
                'position': 'Software Developer'
            },
            {
                'email': 'jane.smith@test.com',
                'password': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6fYzYXkqO',
                'role': 'employee',
                'employee_id': 'TEST002',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'hire_date': '2024-02-01',
                'salary': 55000.00,
                'position': 'Project Manager'
            }
        ]

        for emp in employees:
            query = f"""
            INSERT INTO Employee (email, password_hash, role, is_active, created_at, updated_at, employee_id, first_name, last_name, hire_date, salary, position) 
            VALUES ('{emp['email']}', '{emp['password']}', '{emp['role']}', true, sysdate(), sysdate(), '{emp['employee_id']}', '{emp['first_name']}', '{emp['last_name']}', '{emp['hire_date']}', {emp['salary']}, '{emp['position']}')
            """
            self.execute_query(query, f"Created employee: {emp['first_name']} {emp['last_name']}")

    def create_test_departments(self):
        """Create test departments"""
        print("🏢 Creating test departments...")
        print(f"   Connecting to: {self.base_url}/command/{self.config['database']}/sql")

        departments = [
            ('Test Engineering', 'Software development department', 200000.00, 'Floor 3'),
            ('Test Marketing', 'Marketing and sales department', 150000.00, 'Floor 2')
        ]

        for i, (name, desc, budget, location) in enumerate(departments):
            print(f"   Creating department {i+1}: {name}")
            query = f"""
            INSERT INTO Department (name, description, budget, location, is_active, created_at)
            VALUES ('{name}', '{desc}', {budget}, '{location}', true, sysdate())
            """
            print(f"   Query: {query.strip()}")
            result = self.execute_query(query, f"Created department: {name}")
            print(f"   Result: {result is not None}")

    def clean_test_data(self):
        """Clean test data"""
        print("🧹 Cleaning test data...")

        # Delete test employees
        self.execute_query("DELETE FROM Employee WHERE employee_id LIKE 'TEST%'", "Deleted test employees")

        # Delete test departments
        self.execute_query("DELETE FROM Department WHERE name IN ['Test Engineering', 'Test Marketing']", "Deleted test departments")

def main():
    import sys

    if len(sys.argv) != 2 or sys.argv[1] not in ['--load', '--clean']:
        print("Usage: python3 simple_test_loader.py --load | --clean")
        sys.exit(1)

    loader = SimpleTestDataLoader()

    if sys.argv[1] == '--load':
        print("🚀 Loading test data...")
        loader.create_test_departments()
        loader.create_test_employees()
        print("✅ Test data loaded!")
    elif sys.argv[1] == '--clean':
        print("🧹 Cleaning test data...")
        loader.clean_test_data()
        print("✅ Test data cleaned!")

if __name__ == "__main__":
    main()