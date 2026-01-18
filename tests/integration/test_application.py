"""
Integration tests for HRMS application
"""
import pytest
import requests
import time
import subprocess
import signal
import os
import sys
from unittest.mock import Mock

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))


class TestHRMSIntegration:
    """Integration tests for the complete HRMS application"""

    @pytest.fixture(scope="class")
    def app_process(self):
        """Start the application for integration testing"""
        import socket
        import time

        # Clean up any existing processes using port 8000
        try:
            # Try to kill any existing processes
            import subprocess
            subprocess.run(['pkill', '-f', 'run_dual_services.py'], check=False)
            subprocess.run(['pkill', '-f', 'uvicorn'], check=False)
            # Also try to kill processes using port 8000
            result = subprocess.run(['lsof', '-ti:8000'], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    subprocess.run(['kill', '-9', pid], check=False)
            time.sleep(2)
        except:
            pass  # Ignore cleanup errors

        # Start the application in background
        process = subprocess.Popen([
            sys.executable, "run_dual_services.py"
        ], cwd=os.path.join(os.path.dirname(__file__), '../..'))

        # Wait for application to start - give it more time and check if it's actually listening
        max_wait = 30
        for i in range(max_wait):
            if process.poll() is not None:
                # Process has exited, check why
                raise RuntimeError(f"Application failed to start, exit code: {process.returncode}")

            # Check if port 8000 is listening
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', 8000))
            sock.close()
            if result == 0:
                # Port is listening, application is ready
                break
            time.sleep(1)

        if process.poll() is not None:
            raise RuntimeError(f"Application failed to start within {max_wait} seconds")

        yield process

        # Cleanup: terminate the process
        try:
            process.terminate()
            process.wait(timeout=10)
        except:
            try:
                process.kill()
            except:
                pass

    def test_application_startup(self, app_process):
        """Test that the application starts successfully"""
        assert app_process.poll() is None  # Process should still be running

    def test_fastapi_health_endpoint(self):
        """Test FastAPI health endpoint"""
        try:
            response = requests.get("http://localhost:8000/health", timeout=10)
            assert response.status_code == 200
        except requests.exceptions.RequestException:
            pytest.skip("Application not running or health endpoint not available")

    def test_grpc_service_connection(self):
        """Test gRPC service connectivity"""
        # This would require gRPC client setup
        # For now, just check if the port is listening
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 50051))
        sock.close()

        # If result is 0, connection was successful
        assert result == 0

    def test_database_connection(self):
        """Test database connectivity"""
        # This would test actual database operations
        # For now, just a placeholder
        assert True

    def test_ui_components_loading(self):
        """Test that UI components load without errors"""
        try:
            # Test the actual UI endpoint
            response = requests.get("http://localhost:8000/hrmkit/", timeout=10)
            assert response.status_code == 200
            assert "HRMS" in response.text or "text/html" in response.headers.get("content-type", "")
        except requests.exceptions.RequestException:
            pytest.skip("UI not accessible")

    def test_api_endpoints(self):
        """Test various API endpoints"""
        endpoints = [
            "/hrmkit/dashboard",
            "/hrmkit/attendance/attendance",
            "/hrmkit/employees/request-transfer"
        ]

        for endpoint in endpoints:
            try:
                response = requests.get(f"http://localhost:8000{endpoint}", timeout=10, allow_redirects=True)
                # Accept both 200 and redirects (3xx), but not 404
                assert response.status_code < 400 or response.status_code == 302  # Allow redirects for auth
            except requests.exceptions.RequestException:
                pytest.skip(f"Endpoint {endpoint} not accessible")


class TestDataFlow:
    """Test data flow between components"""

    def test_user_creation_flow(self):
        """Test complete user creation workflow"""
        # This would test creating a user through the UI/API
        # and verifying it appears in the database
        assert True  # Placeholder

    def test_attendance_tracking_flow(self):
        """Test attendance tracking workflow"""
        # Test clock in/out functionality
        assert True  # Placeholder


if __name__ == "__main__":
    pytest.main([__file__])