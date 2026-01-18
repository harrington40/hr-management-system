#!/usr/bin/env python3
"""
Test Jenkins Server Connectivity
This script tests the connection between the HRMS app and Jenkins server
"""

import requests
import sys
from urllib.parse import urljoin

# Jenkins server configuration from JENKINS_README.md
JENKINS_URL = "https://jenkins.transtechologies.com:18084/"

def test_jenkins_connection():
    """Test basic connectivity to Jenkins server"""
    print("=" * 60)
    print("Jenkins Connectivity Test")
    print("=" * 60)
    print(f"\nJenkins URL: {JENKINS_URL}")
    
    try:
        print("\n1. Testing basic connectivity...")
        response = requests.get(JENKINS_URL, timeout=10, verify=False)
        print(f"   ✓ Status Code: {response.status_code}")
        print(f"   ✓ Server is reachable")
        
        # Test API endpoint
        print("\n2. Testing Jenkins API endpoint...")
        api_url = urljoin(JENKINS_URL, "api/json")
        response = requests.get(api_url, timeout=10, verify=False)
        print(f"   ✓ API Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Jenkins Version: {data.get('_class', 'Unknown')}")
        
        return True
        
    except requests.exceptions.SSLError as e:
        print(f"   ✗ SSL Error: {e}")
        print("   Note: SSL verification is disabled, but there may be certificate issues")
        return False
        
    except requests.exceptions.ConnectionError as e:
        print(f"   ✗ Connection Error: {e}")
        print("   The Jenkins server may be down or unreachable")
        return False
        
    except requests.exceptions.Timeout as e:
        print(f"   ✗ Timeout Error: {e}")
        print("   The server took too long to respond")
        return False
        
    except Exception as e:
        print(f"   ✗ Unexpected Error: {e}")
        return False

def test_jenkins_with_auth(username=None, token=None):
    """Test Jenkins connection with authentication"""
    if not username or not token:
        print("\n3. Skipping authenticated test (no credentials provided)")
        return None
    
    print("\n3. Testing with authentication...")
    try:
        response = requests.get(
            JENKINS_URL,
            auth=(username, token),
            timeout=10,
            verify=False
        )
        print(f"   ✓ Authenticated Status Code: {response.status_code}")
        return True
    except Exception as e:
        print(f"   ✗ Authentication Error: {e}")
        return False

def check_local_app():
    """Check if the local HRMS application is running"""
    print("\n4. Checking local HRMS application...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ HRMS App is running")
            print(f"   ✓ Status: {data.get('status')}")
            print(f"   ✓ Service: {data.get('service')}")
            print(f"   ✓ Version: {data.get('version')}")
            return True
        else:
            print(f"   ✗ HRMS App returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ✗ HRMS App is not running on port 8000")
        print("   Tip: Start the app with: python3 main.py or python3 run_dual_services.py")
        return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def main():
    """Main test function"""
    import warnings
    warnings.filterwarnings('ignore', message='Unverified HTTPS request')
    
    results = {
        'jenkins_connection': test_jenkins_connection(),
        'local_app': check_local_app()
    }
    
    # Optional: test with credentials if available
    # Uncomment and add credentials to test authenticated access
    # results['jenkins_auth'] = test_jenkins_with_auth('username', 'api_token')
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test.replace('_', ' ').title()}: {status}")
    
    print("\n")
    
    if not results['local_app']:
        print("📝 Note: The HRMS application must be running for Jenkins")
        print("   to perform CI/CD operations like smoke tests and deployments.")
        print("\n   To start the app, run:")
        print("   python3 run_dual_services.py")
        print("   or")
        print("   python3 main.py")
    
    # Return exit code
    sys.exit(0 if all(v for v in results.values() if v is not None) else 1)

if __name__ == "__main__":
    main()
