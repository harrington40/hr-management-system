#!/usr/bin/env python3
"""
HRMS OrientDB Database Initialization Script (REST API Version)
Creates and initializes the OrientDB database for the HRMS application using REST API
"""

import os
import sys
import time
import requests
import json
from requests.auth import HTTPBasicAuth
from pathlib import Path

def get_db_config():
    """Get database configuration from environment variables"""
    return {
        'host': os.getenv('ORIENTDB_HOST', 'orientdb.transtechologies.com'),
        'port': int(os.getenv('ORIENTDB_PORT', 2424)),
        'user': os.getenv('ORIENTDB_USER', 'root'),
        'password': os.getenv('ORIENTDB_PASSWORD', 'Namu2025'),
        'database': os.getenv('ORIENTDB_DATABASE', 'hrms')
    }

def get_base_url():
    """Get the REST API base URL"""
    return "https://orientdb.transtechologies.com"

def test_connection(config):
    """Test OrientDB server connection via REST API"""
    try:
        base_url = get_base_url()
        print("🔌 Testing OrientDB REST API connection...")

        # Test server connection
        server_url = f"{base_url}/server"
        response = requests.get(
            server_url,
            auth=HTTPBasicAuth(config['user'], config['password']),
            timeout=10,
            verify=False  # Disable SSL verification for test environment
        )

        if response.status_code == 200:
            print("✅ Connected to OrientDB Server via REST API")
            return True
        else:
            print(f"❌ Server connection failed: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False

    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def create_database_if_not_exists(config):
    """Create database if it doesn't exist"""
    try:
        base_url = get_base_url()
        print(f"📦 Attempting to create/access database '{config['database']}'...")

        # First, try to create the database directly
        # If it already exists, this might fail, but that's OK
        print(f"📦 Creating database '{config['database']}'...")

        # Try different create database endpoints
        create_endpoints = [
            f"{base_url}/database/{config['database']}/plocal",
            f"{base_url}/database/{config['database']}/memory",
            f"{base_url}/database/{config['database']}"
        ]

        for create_url in create_endpoints:
            try:
                print(f"   Trying endpoint: {create_url}")
                response = requests.post(
                    command_url,
                    auth=HTTPBasicAuth(config['user'], config['password']),
                    data=command,
                    headers={'Content-Type': 'text/plain'},
                    timeout=30,
                    verify=False  # Disable SSL verification for test environment
                )
                if response.status_code in [200, 201, 204]:
                    print(f"✅ Database '{config['database']}' created successfully")
                    return True
                elif response.status_code == 409:  # Conflict - database already exists
                    print(f"✅ Database '{config['database']}' already exists")
                    return True
                else:
                    print(f"   Endpoint failed: HTTP {response.status_code} - {response.text[:100]}...")
                    continue  # Try next endpoint

            except Exception as e:
                print(f"   Endpoint error: {e}")
                continue

        # If all create attempts failed, try to check if database exists
        print(f"📦 Checking if database '{config['database']}' exists...")
        db_url = f"{base_url}/database/{config['database']}"
        response = requests.get(
            db_url,
            auth=HTTPBasicAuth(config['user'], config['password']),
            timeout=10,
            verify=False
        )

        if response.status_code == 200:
            print(f"✅ Database '{config['database']}' exists and is accessible")
            return True
        elif response.status_code == 401:
            print(f"❌ Authentication failed. Please check credentials.")
            print(f"   User: {config['user']}")
            print(f"   Make sure the password is correct and user has database permissions.")
            return False
        elif response.status_code == 404:
            print(f"❌ Database '{config['database']}' does not exist and could not be created")
            print(f"   Please check user permissions or create database manually")
            return False
        else:
            print(f"❌ Unexpected response: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False

    except Exception as e:
        print(f"❌ Database creation/access error: {e}")
        return False

def execute_schema_via_rest(config, schema_file):
    """Execute schema commands via REST API"""
    try:
        base_url = get_base_url()
        print("📋 Executing schema via REST API...")

        if not schema_file.exists():
            print(f"❌ Schema file not found: {schema_file}")
            return False

        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_content = f.read()

        # Split schema into individual commands
        commands = [cmd.strip() for cmd in schema_content.split(';') if cmd.strip() and not cmd.startswith('--')]

        executed_count = 0
        for command in commands:
            if command:
                try:
                    # Execute command via REST API
                    command_url = f"{base_url}/command/{config['database']}/sql"
                    payload = {"command": command}

                    response = requests.post(
                        command_url,
                        auth=HTTPBasicAuth(config['user'], config['password']),
                        json=payload,
                        timeout=30,
                        verify=False
                    )

                    if response.status_code in [200, 201, 204]:
                        executed_count += 1
                        # Show progress for major commands
                        if any(keyword in command.upper() for keyword in ['CREATE CLASS', 'CREATE PROPERTY', 'INSERT INTO']):
                            print(f"   ✓ Executed: {command[:50]}...")
                    else:
                        # Some commands might fail if they already exist
                        if "already exists" not in response.text.lower():
                            print(f"   ⚠️  Warning on command: HTTP {response.status_code}")
                            print(f"      Command: {command[:100]}...")
                            print(f"      Response: {response.text[:200]}...")

                except Exception as e:
                    print(f"   ⚠️  Error executing command: {e}")
                    print(f"      Command: {command[:100]}...")

        print(f"✅ Executed {executed_count} schema commands via REST API")
        return True

    except Exception as e:
        print(f"❌ Failed to execute schema: {e}")
        return False

def verify_schema_via_rest(config):
    """Verify schema creation via REST API"""
    try:
        base_url = get_base_url()
        print("🔍 Verifying schema creation...")

        # Query for existing classes
        query_url = f"{base_url}/query/{config['database']}/sql"
        payload = {"command": "SELECT name FROM (SELECT expand(classes) FROM metadata:schema) WHERE name IN ['User', 'Employee', 'Department', 'Position', 'Schedule', 'AttendanceRecord', 'LeaveType', 'LeaveRequest', 'LeaveBalance', 'Institution', 'SystemSetting', 'AuditLog']"}

        response = requests.post(
            query_url,
            auth=HTTPBasicAuth(config['user'], config['password']),
            json=payload,
            timeout=10,
            verify=False  # Disable SSL verification for test environment
        )

        if response.status_code == 200:
            result = response.json()
            classes_found = [record['name'] for record in result.get('result', [])]
            print(f"✅ Found {len(classes_found)} vertex classes: {', '.join(classes_found)}")
            return True
        else:
            print(f"⚠️  Could not verify schema: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False

    except Exception as e:
        print(f"❌ Schema verification error: {e}")
        return False

def main():
    """Main initialization function"""
    print("🚀 HRMS OrientDB Database Initialization (REST API)")
    print("=" * 60)

    config = get_db_config()
    print(f"Configuration:")
    print(f"  Server: {config['host']}")
    print(f"  REST URL: {get_base_url()}")
    print(f"  Database: {config['database']}")
    print(f"  User: {config['user']}")
    print()

    # Test connection
    if not test_connection(config):
        print("\n❌ Connection test failed. Please check your configuration.")
        return False

    # Create database if needed
    if not create_database_if_not_exists(config):
        print("\n❌ Database creation failed.")
        return False

    # Execute schema
    schema_file = Path(__file__).parent / "hrms_schema.sql"
    if not execute_schema_via_rest(config, schema_file):
        print("\n❌ Schema execution failed.")
        return False

    # Verify schema
    if not verify_schema_via_rest(config):
        print("\n⚠️  Schema verification had issues, but continuing...")

    print("\n" + "=" * 60)
    print("✅ Database initialization completed!")
    print("🎯 Your HRMS database is ready for use.")
    print("\nNext steps:")
    print("  1. Run the test script: python3 test_database.py")
    print("  2. Start your HRMS application")
    print("  3. Access the dashboard at http://localhost:8000")

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)