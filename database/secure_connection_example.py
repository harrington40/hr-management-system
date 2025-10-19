#!/usr/bin/env python3
"""
Secure Database Connection Example for HRMS
Demonstrates proper SSL/TLS configuration for OrientDB connections
"""

import os
import requests
import ssl
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class SecureOrientDBClient:
    """Secure OrientDB REST API client with proper SSL/TLS configuration"""

    def __init__(self, host, port, user, password, database):
        self.base_url = f"https://{host}"
        self.user = user
        self.password = password
        self.database = database

        # Create a session with secure SSL configuration
        self.session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=1
        )

        # Create HTTP adapter with SSL verification enabled
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)

        # Set default headers
        self.session.headers.update({
            'Content-Type': 'text/plain',
            'User-Agent': 'HRMS-Secure-Client/1.0'
        })

    def execute_query(self, query, timeout=30):
        """Execute SQL query with secure connection"""
        command_url = f"{self.base_url}/command/{self.database}/sql"

        try:
            response = self.session.post(
                command_url,
                auth=HTTPBasicAuth(self.user, self.password),
                data=query,
                timeout=timeout,
                verify=True  # Always verify SSL certificates
            )

            response.raise_for_status()  # Raise exception for bad status codes
            return response.json()

        except requests.exceptions.SSLError as e:
            print(f"❌ SSL Certificate Error: {e}")
            print("💡 Ensure your system's CA certificates are up to date")
            raise
        except requests.exceptions.ConnectionError as e:
            print(f"❌ Connection Error: {e}")
            raise
        except requests.exceptions.Timeout as e:
            print(f"❌ Timeout Error: {e}")
            raise
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP Error: {e}")
            raise

def get_secure_config():
    """Get database configuration with security validation"""
    config = {
        'host': os.getenv('ORIENTDB_HOST', 'orientdb.transtechologies.com'),
        'port': int(os.getenv('ORIENTDB_PORT', 2424)),
        'user': os.getenv('ORIENTDB_USER'),
        'password': os.getenv('ORIENTDB_PASSWORD'),
        'database': os.getenv('ORIENTDB_DATABASE', 'hrms')
    }

    # Validate required configuration
    required_fields = ['user', 'password']
    missing = [field for field in required_fields if not config.get(field)]

    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    return config

def main():
    """Example usage of secure database client"""
    print("🔒 Secure OrientDB Connection Example")
    print("=" * 50)

    try:
        # Get secure configuration
        config = get_secure_config()

        # Create secure client
        client = SecureOrientDBClient(**config)

        # Test connection with a simple query
        print("🔍 Testing secure connection...")
        result = client.execute_query("SELECT COUNT(*) as user_count FROM User")

        user_count = result.get('result', [{}])[0].get('user_count', 0)
        print(f"✅ Secure connection successful! Found {user_count} users.")

        # Test a simple data operation
        print("📝 Testing secure data retrieval...")
        result = client.execute_query("SELECT name FROM Institution LIMIT 1")

        institutions = result.get('result', [])
        if institutions:
            print(f"✅ Secure data retrieval successful! Found institution: {institutions[0].get('name')}")
        else:
            print("⚠️  No institution data found, but connection is secure")

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    print("\n🔐 Security Features Implemented:")
    print("   ✅ SSL/TLS certificate verification enabled")
    print("   ✅ HTTP Basic Authentication over HTTPS")
    print("   ✅ Request retry strategy for resilience")
    print("   ✅ Timeout protection against hanging connections")
    print("   ✅ Proper error handling and logging")
    print("   ✅ Environment variable validation")

    return 0

if __name__ == "__main__":
    exit(main())