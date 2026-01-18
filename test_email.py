#!/usr/bin/env python3
"""
Test email configuration for mail.transtechologies.com
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
SMTP_SERVER = 'mail.transtechologies.com'
SMTP_USERNAME = 'dev@transtechologies.com'
SMTP_PASSWORD = 'Cosinesine900**'
TEST_EMAIL = 'dev@transtechologies.com'

def test_smtp_connection():
    """Test SMTP connection with different methods"""
    
    print("="*60)
    print("Testing SMTP Configuration for mail.transtechologies.com")
    print("="*60)
    
    # Test 1: STARTTLS on port 587
    print("\n[Test 1] Trying STARTTLS on port 587...")
    try:
        server = smtplib.SMTP(SMTP_SERVER, 587, timeout=10)
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        print("✅ SUCCESS: STARTTLS on port 587 works!")
        server.quit()
        return True, "STARTTLS-587"
    except Exception as e:
        print(f"❌ FAILED: STARTTLS on port 587 - {e}")
    
    # Test 2: SSL on port 465
    print("\n[Test 2] Trying SSL on port 465...")
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, 465, timeout=10)
        server.set_debuglevel(1)
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        print("✅ SUCCESS: SSL on port 465 works!")
        server.quit()
        return True, "SSL-465"
    except Exception as e:
        print(f"❌ FAILED: SSL on port 465 - {e}")
    
    # Test 3: Plain SMTP on port 25
    print("\n[Test 3] Trying plain SMTP on port 25...")
    try:
        server = smtplib.SMTP(SMTP_SERVER, 25, timeout=10)
        server.set_debuglevel(1)
        server.ehlo()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        print("✅ SUCCESS: Plain SMTP on port 25 works!")
        server.quit()
        return True, "SMTP-25"
    except Exception as e:
        print(f"❌ FAILED: Plain SMTP on port 25 - {e}")
    
    return False, None

def send_test_email(method):
    """Send a test email"""
    print("\n" + "="*60)
    print(f"Sending test email using {method}...")
    print("="*60)
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Test Email from HRMS"
        msg['From'] = SMTP_USERNAME
        msg['To'] = TEST_EMAIL
        
        html_body = """
        <html>
            <body>
                <h2>Test Email</h2>
                <p>This is a test email from your HRMS application.</p>
                <p>If you received this, your email configuration is working correctly!</p>
            </body>
        </html>
        """
        
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        # Send based on method
        if method == "STARTTLS-587":
            server = smtplib.SMTP(SMTP_SERVER, 587, timeout=10)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
        elif method == "SSL-465":
            server = smtplib.SMTP_SSL(SMTP_SERVER, 465, timeout=10)
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
        elif method == "SMTP-25":
            server = smtplib.SMTP(SMTP_SERVER, 25, timeout=10)
            server.ehlo()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
        
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Test email sent successfully to {TEST_EMAIL}")
        return True
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")
        return False

if __name__ == "__main__":
    success, method = test_smtp_connection()
    
    if success:
        print("\n" + "="*60)
        print(f"✅ Email configuration is WORKING with {method}!")
        print("="*60)
        
        send_test = input("\nWould you like to send a test email? (y/n): ")
        if send_test.lower() == 'y':
            send_test_email(method)
    else:
        print("\n" + "="*60)
        print("❌ All SMTP connection attempts FAILED")
        print("Please check:")
        print("1. Server address: mail.transtechologies.com")
        print("2. Username: dev@transtechologies.com")
        print("3. Password is correct")
        print("4. Firewall is not blocking SMTP ports")
        print("="*60)
