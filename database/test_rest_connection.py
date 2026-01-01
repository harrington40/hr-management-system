#!/usr/bin/env python3
"""
Simple OrientDB Connection Test using REST API
Tests connectivity to OrientDB server using HTTP REST API
"""

import os
import sys
import requests
from requests.auth import HTTPBasicAuth

def get_db_config():
    """Get database configuration from environment variables"""
    return {
        'host': os.getenv('ORIENTDB_HOST', 'orientdb.transtechologies.com'),
        'port': int(os.getenv('ORIENTDB_PORT', 2424)),
        'user': os.getenv('ORIENTDB_USER', 'root'),
        'password': os.getenv('ORIENTDB_PASSWORD', 'Namu2025'),
        'database': os.getenv('ORIENTDB_DATABASE', 'hrms')
    }

def test_rest_api_connection(config):
    """Test OrientDB connection using REST API"""
    try:
        # Use the HTTPS endpoint that the user mentioned
        base_url = "https://orientdb.transtechologies.com"

        print("🔌 Testing OrientDB REST API connection...")
        print(f"   URL: {base_url}")
        print(f"   Database: {config['database']}")
        print(f"   User: {config['user']}")

        # Test server info endpoint
        server_url = f"{base_url}/server"
        print(f"   Testing server endpoint: {server_url}")

        response = requests.get(
            server_url,
            auth=HTTPBasicAuth(config['user'], config['password']),
            timeout=10,
            verify=False  # Since it's HTTPS, but we might need to handle certificates
        )

        if response.status_code == 200:
            server_info = response.json()
            print("✅ Connected to OrientDB Server via REST API")
            print(f"   Server Version: {server_info.get('version', 'unknown')}")
            return True, response
        else:
            print(f"❌ REST API connection failed: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False, response

    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return False, None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False, None

def test_database_access(config):
    """Test database access via REST API"""
    try:
        base_url = "https://orientdb.transtechologies.com"

        print(f"📦 Testing database '{config['database']}' access...")

        # Test database exists
        db_url = f"{base_url}/database/{config['database']}"
        print(f"   Testing database endpoint: {db_url}")

        response = requests.get(
            db_url,
            auth=HTTPBasicAuth(config['user'], config['password']),
            timeout=10,
            verify=False
        )

        if response.status_code == 200:
            print(f"✅ Database '{config['database']}' is accessible")
            return True
        elif response.status_code == 404:
            print(f"⚠️  Database '{config['database']}' does not exist")
            print("   You may need to create it first")
            return False
        else:
            print(f"❌ Database access failed: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False

    except Exception as e:
        print(f"❌ Database access error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 OrientDB REST API Connection Test")
    print("=" * 50)

    config = get_db_config()
    print(f"Configuration:")
    print(f"  Host: {config['host']}")
    print(f"  Port: {config['port']}")
    print(f"  Database: {config['database']}")
    print(f"  User: {config['user']}")
    print()

    # Test REST API connection
    success, response = test_rest_api_connection(config)
    if not success:
        print("\n❌ REST API connection test failed")
        return False

    # Test database access
    db_success = test_database_access(config)

    print("\n" + "=" * 50)
    if success:
        print("✅ OrientDB REST API connection successful!")
        if db_success:
            print("✅ Database access successful!")
        else:
            print("⚠️  Server connection OK, but database access needs attention")
    else:
        print("❌ OrientDB connection failed")

    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)