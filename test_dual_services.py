#!/usr/bin/env python3
"""
Test script to verify both FastAPI and gRPC services are running
"""

import requests
import grpc
import time
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from grpc_services.client.hrms_client import HRMSGrpcClient

def test_fastapi_service():
    """Test FastAPI service on port 8000"""
    print("🔍 Testing FastAPI service (port 8000)...")

    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ FastAPI health check passed")
            print(f"   Status: {data.get('status', 'unknown')}")
            print(f"   Services: {list(data.get('services', {}).keys())}")
            return True
        else:
            print(f"❌ FastAPI health check failed: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ FastAPI connection failed: {e}")
        return False

def test_grpc_service():
    """Test gRPC service on port 50051"""
    print("🔍 Testing gRPC service (port 50051)...")

    client = HRMSGrpcClient('localhost', 50051)

    try:
        if client.connect():
            print("✅ gRPC connection established")

            # Try to authenticate (this might fail without proper setup, but connection should work)
            auth_result = client.authenticate_user('test', 'test')
            if auth_result:
                print("✅ gRPC authentication test completed")
            else:
                print("⚠️  gRPC authentication test returned None (expected if no users)")

            client.disconnect()
            return True
        else:
            print("❌ gRPC connection failed")
            return False
    except Exception as e:
        print(f"❌ gRPC test error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing HRMS Dual Services")
    print("=" * 50)

    # Wait a moment for services to start
    print("⏳ Waiting 3 seconds for services to initialize...")
    time.sleep(3)

    fastapi_ok = test_fastapi_service()
    print()
    grpc_ok = test_grpc_service()

    print()
    print("=" * 50)
    print("📊 Test Results:")

    if fastapi_ok and grpc_ok:
        print("🎉 SUCCESS: Both services are running correctly!")
        print("   📱 FastAPI Web UI: http://localhost:8000/hrmkit/")
        print("   🔧 gRPC API: localhost:50051")
        return 0
    elif fastapi_ok:
        print("⚠️  PARTIAL: FastAPI is running, but gRPC failed")
        return 1
    elif grpc_ok:
        print("⚠️  PARTIAL: gRPC is running, but FastAPI failed")
        return 1
    else:
        print("❌ FAILURE: Both services failed to start")
        return 1

if __name__ == "__main__":
    sys.exit(main())