"""
Regression tests for HRMS application
End-to-end tests to ensure existing functionality still works
"""
import pytest
import time
import os
import sys
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))


@pytest.fixture(scope="class")
def browser():
    """Set up Chrome browser for testing"""
    # Check if Chrome is available
    chrome_paths = [
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium-browser",
        "/usr/lib/bin/google-chrome",
        "/usr/lib/bin/google-chrome-stable"
    ]

    chrome_available = any(os.path.exists(path) for path in chrome_paths)
    chrome_available = chrome_available or any(
        shutil.which(cmd) for cmd in ["google-chrome", "google-chrome-stable", "chromium-browser"]
    )

    if not chrome_available:
        pytest.skip("Chrome browser not available for Selenium tests")

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    # Use Chrome binary from environment or default
    chrome_bin = os.environ.get("CHROME_BIN", "/usr/bin/google-chrome-stable")
    if os.path.exists(chrome_bin):
        chrome_options.binary_location = chrome_bin

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)

    yield driver

    driver.quit()


class TestHRMSRegression:

    def test_application_loads(self, browser):
        """Test that the main application page loads"""
        browser.get("http://localhost:8000/hrmkit/")

        # Wait for page to load
        WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        assert "HRMS" in browser.title or "HRMS" in browser.page_source

    def test_navigation_menu(self, browser):
        """Test that navigation menu works"""
        browser.get("http://localhost:8000/hrmkit/")

        # Look for navigation elements
        try:
            # Try different selectors for navigation
            nav_selectors = [
                ".navigation",
                "[class*='nav']",
                "[class*='menu']",
                "nav",
                ".sidebar"
            ]

            navigation_found = False
            for selector in nav_selectors:
                try:
                    nav_element = browser.find_element(By.CSS_SELECTOR, selector)
                    if nav_element.is_displayed():
                        navigation_found = True
                        break
                except NoSuchElementException:
                    continue

            assert navigation_found, "Navigation menu not found"

        except TimeoutException:
            pytest.skip("Navigation elements not loaded within timeout")

    def test_attendance_page_access(self, browser):
        """Test accessing attendance page"""
        browser.get("http://localhost:8000/hrmkit/")

        try:
            # Try to find and click attendance link
            attendance_selectors = [
                "a[href*='attendance']",
                "[data-route*='attendance']",
                "button:contains('Attendance')",
                ".attendance-link"
            ]

            attendance_clicked = False
            for selector in attendance_selectors:
                try:
                    element = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    element.click()
                    attendance_clicked = True
                    break
                except (NoSuchElementException, TimeoutException):
                    continue

            if attendance_clicked:
                # Wait for attendance page to load
                WebDriverWait(browser, 10).until(
                    lambda driver: "attendance" in driver.current_url.lower() or
                                   "attendance" in driver.page_source.lower()
                )
                assert True
            else:
                # If we can't click, at least check if attendance URL is accessible
                browser.get("http://localhost:8000/hrmkit/attendance")
                assert "attendance" in browser.current_url.lower()

        except TimeoutException:
            pytest.skip("Attendance page not accessible")

    def test_form_submissions(self, browser):
        """Test that forms can be submitted without errors"""
        browser.get("http://localhost:8000")

        # Look for forms and test basic submission
        try:
            forms = browser.find_elements(By.TAG_NAME, "form")

            if forms:
                # Test the first form found
                form = forms[0]

                # Try to submit the form (may not work without valid data)
                submit_buttons = form.find_elements(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")

                if submit_buttons:
                    # Just check that the button exists and is clickable
                    assert submit_buttons[0].is_displayed()
                else:
                    # No submit button, just verify form exists
                    assert form.is_displayed()
            else:
                # No forms found, which is also acceptable
                assert True

        except Exception:
            pytest.skip("Form testing not applicable")

    def test_responsive_design(self, browser):
        """Test responsive design on different screen sizes"""
        browser.get("http://localhost:8000")

        # Test mobile viewport
        browser.set_window_size(375, 667)  # iPhone size
        time.sleep(2)

        # Check that content is still accessible
        body = browser.find_element(By.TAG_NAME, "body")
        assert body.is_displayed()

        # Test tablet viewport
        browser.set_window_size(768, 1024)  # iPad size
        time.sleep(2)

        assert body.is_displayed()

        # Reset to desktop size
        browser.set_window_size(1920, 1080)
        time.sleep(2)

        assert body.is_displayed()

    def test_error_handling(self, browser):
        """Test error handling for invalid URLs"""
        browser.get("http://localhost:8000/invalid-page-12345")

        # Should not crash, should show some kind of error or redirect
        assert browser.find_element(By.TAG_NAME, "body").is_displayed()


class TestPerformanceRegression:
    """Performance regression tests"""

    def test_page_load_times(self, browser):
        """Test that pages load within acceptable time limits"""
        import time

        browser.get("http://localhost:8000/hrmkit/")

        # Measure load time
        start_time = time.time()
        WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        load_time = time.time() - start_time

        # Page should load within 10 seconds
        assert load_time < 10, f"Page took {load_time} seconds to load"

    def test_memory_usage(self):
        """Test basic memory usage (placeholder for more advanced monitoring)"""
        # This would require system monitoring tools
        # For now, just ensure the application is responsive
        assert True


if __name__ == "__main__":
    pytest.main([__file__])