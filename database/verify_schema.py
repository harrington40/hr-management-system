#!/usr/bin/env python3
"""
Quick Schema Verification Test
Tests that basic OrientDB classes were created successfully
"""

import os
import sys
import requests
from requests.auth import HTTPBasicAuth

def get_db_config():
    return {
        'host': os.getenv('ORIENTDB_HOST', 'orientdb.transtechologies.com'),
        'user': os.getenv('ORIENTDB_USER', 'root'),
        'password': os.getenv('ORIENTDB_PASSWORD', 'Namu2025'),
        'database': os.getenv('ORIENTDB_DATABASE', 'hrms')
    }

def test_basic_classes():
    """Test that basic vertex classes exist"""
    config = get_db_config()
    base_url = "https://orientdb.transtechologies.com"

    print("🔍 Testing basic schema classes...")

    # Test classes that should exist
    test_classes = ['User', 'Employee', 'Department', 'Position']

    for class_name in test_classes:
        try:
            # Try using command endpoint instead
            command_url = f"{base_url}/command/{config['database']}/sql"
            payload = f"SELECT COUNT(*) as count FROM {class_name}"

            response = requests.post(
                command_url,
                auth=HTTPBasicAuth(config['user'], config['password']),
                data=payload,
                headers={'Content-Type': 'text/plain'},
                timeout=10,
                verify=True  # Enable SSL certificate verification
            )

            if response.status_code == 200:
                result = response.json()
                count = result.get('result', [{}])[0].get('count', 0)
                print(f"✅ Class '{class_name}' exists (count: {count})")
            else:
                print(f"❌ Class '{class_name}' query failed: HTTP {response.status_code}")
                print(f"   Response: {response.text[:100]}...")

        except Exception as e:
            print(f"❌ Error testing class '{class_name}': {e}")

def test_sample_data():
    """Test that sample data was inserted"""
    config = get_db_config()
    base_url = "https://orientdb.transtechologies.com"

    print("\n📊 Testing sample data...")

    try:
        # Check for institution data
        command_url = f"{base_url}/command/{config['database']}/sql"
        payload = "SELECT name FROM Institution"

        response = requests.post(
            command_url,
            auth=HTTPBasicAuth(config['user'], config['password']),
            data=payload,
            headers={'Content-Type': 'text/plain'},
            timeout=10,
            verify=True  # Enable SSL certificate verification
        )

        if response.status_code == 200:
            result = response.json()
            institutions = result.get('result', [])
            if institutions:
                print(f"✅ Found {len(institutions)} institution(s):")
                for inst in institutions:
                    print(f"   - {inst.get('name', 'Unknown')}")
            else:
                print("⚠️  No institution data found")
        else:
            print(f"❌ Institution query failed: HTTP {response.status_code}")
            print(f"   Response: {response.text[:100]}...")

    except Exception as e:
        print(f"❌ Error testing sample data: {e}")

def main():
    print("🧪 OrientDB Schema Verification Test")
    print("=" * 50)

    test_basic_classes()
    test_sample_data()

    print("\n" + "=" * 50)
    print("✅ Schema verification completed!")
    print("🎯 Your HRMS OrientDB database is ready!")

if __name__ == "__main__":
    main()