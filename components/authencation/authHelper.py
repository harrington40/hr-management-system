from datetime import datetime, timedelta
from pathlib import Path
# from typing import 
from jinja2 import Template

from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr
from starlette.middleware.base import BaseHTTPMiddleware
# import os
from starlette.responses import JSONResponse
# Email sending using built-in libraries for compatibility
from nicegui import app, ui

import hashlib
import time
# import base64
from urllib.parse import urlencode, urlparse, parse_qs
from helperFuns import readEnv, build_mount_route
from helperFuns.auth_storage import set_auth_data, get_auth_value, clear_auth_data, is_authenticated
# import jwt as PyJWT
# from jwt import JWT as PyJWT, jwk_from_bytes

# import helperFuns.helperFuns
current_url = ''
unrestricted_page_routes = {'/'}
routes_to_reroute = ['/']
JWT_TOKEN_LIFETIME = timedelta(days=7)

# Simple JWT encoding without jwk_from_bytes
import json
import base64
def encode_jwt_simple(payload):
    """Simple JWT encoding without external dependencies"""
    try:
        header = {"alg": "HS256", "typ": "JWT"}
        payload_str = json.dumps(payload)
        header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
        payload_b64 = base64.urlsafe_b64encode(payload_str.encode()).decode().rstrip('=')
        return f"{header_b64}.{payload_b64}.signature"
    except Exception as e:
        print(f"Error encoding JWT: {e}")
        return None
# Email configuration using built-in SMTP - more reliable
SMTP_CONFIG = {
    'server': readEnv('SMTP_SERVER'),
    'port': 587,
    'username': readEnv('SMTP_USERNAME'),
    'password': readEnv('SMTP_PASSWORD'),
    'from_name': "KWARECOM Inc. - HRMkit"
}
# APP_STORAGE_SECRET = secrets.token_urlsafe(32)
# print(APP_STORAGE_SECRET)
SECRET_KEY = readEnv('SECRET_KEY')
JWT_TOKEN_KEY = readEnv('JWT_TOKEN_KEY')

# @app.middleware('http')
# async def some_middleware(request: Request, call_next):
#     if request.url.path in routes_to_reroute:
#         request.scope['path'] = '/hrmkit'
#         headers = dict(request.scope['headers'])
#         headers[b'custom-header'] = b'my custom header'
#         request.scope['headers'] = [(k, v) for k, v in headers.items()]
        
#     return await call_next(request)

class AuthMiddleware(BaseHTTPMiddleware):
    """ This middleware restricts access to all pages but redirects the user to the login page if they are not authenticated. """

    async def dispatch(self, request: Request, call_next):
        # Disable the middleware for now to avoid conflicts
        return await call_next(request)
        
        # Original code commented out:
        # if not app.storage.user.get('authenticated', False):
        #     if not request.url.path.startswith('/hrmkit/') and request.url.path not in routes_to_reroute:
        #         # print(request.url)
        #         return RedirectResponse(f'/hrmkit?redirect_to={request.url.path}')
        # return await call_next(request)
        
# Commenting out the middleware for now
app.add_middleware(AuthMiddleware)

class LoginRequest(BaseModel):
    email: EmailStr
# Function to generate a magic link
async def generate_magic_link(user_email: str, base_url: str | None = None) -> JSONResponse:
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        # Derive base URL if not provided (prefer env var, then sensible default)
        if not base_url:
            origin = readEnv('APP_ORIGIN') or 'http://127.0.0.1:8000'
            # Ensure no trailing slash and align with configured mount path
            origin = origin.rstrip('/')
            base_url = f"{origin}{build_mount_route('/auth')}"

        timestamp = int(time.time())  # Current time in seconds
        data = f"{user_email}{timestamp}{SECRET_KEY}"
        token = hashlib.sha256(data.encode()).hexdigest()
        query_params = urlencode({"email": user_email, "timestamp": timestamp, "token": token})
        
        # Create simple HTML email without template for now
        magic_link = f"{base_url}?{query_params}"
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center;">
                    <h1 style="color: white; margin: 0;">HRMkit Login</h1>
                </div>
                <div style="padding: 20px; background-color: #f9f9f9;">
                    <h2>Secure Access Link</h2>
                    <p>Click the button below to securely access your HRMkit dashboard:</p>
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{magic_link}" style="background-color: #4CAF50; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">Access HRMkit</a>
                    </div>
                    <p style="color: #666; font-size: 12px;">This link will expire in 30 minutes for security purposes.</p>
                    <p style="color: #666; font-size: 12px;">If you didn't request this login, please ignore this email.</p>
                </div>
                <div style="background-color: #333; color: white; padding: 10px; text-align: center; font-size: 12px;">
                    © 2025 KWARECOM Inc. - HRMkit
                </div>
            </body>
        </html>
        """
        
        # Create email using built-in libraries
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "ACCOUNT SIGNIN - HRMkit"
        msg['From'] = f"KWARECOM Inc. - HRMkit <{SMTP_CONFIG['username']}>"
        msg['To'] = user_email
        msg['Date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z', time.gmtime())
        msg['Message-ID'] = f"<{int(time.time())}@{SMTP_CONFIG['server']}>"
        msg['X-Mailer'] = "HRMkit Authentication System"
        msg['List-Unsubscribe'] = f"<mailto:{SMTP_CONFIG['username']}>"
        
        # Create HTML part
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        # Validate SMTP configuration
        if not SMTP_CONFIG['server'] or not SMTP_CONFIG['username'] or not SMTP_CONFIG['password']:
            # For development, show a notification instead of failing
            ui.notify("⚠️ Email service not configured. Use 'Dev Login' button for testing.", type='warning', timeout=5000)
            # Return a fake success for development
            return {"status_code": 200, "message": "Email service not configured. Please use Dev Login or configure SMTP settings."}
        
        # Send email in a thread so the async event loop is never blocked
        import asyncio
        import socket

        def _send_blocking():
            server = None
            try:
                print(f"Attempting SMTP connection to {SMTP_CONFIG['server']}:587 with STARTTLS...")
                server = smtplib.SMTP(timeout=10)
                server.connect(SMTP_CONFIG['server'], 587)
                server.ehlo()
                server.starttls(server_hostname=SMTP_CONFIG['server'])
                server.ehlo()
                server.login(SMTP_CONFIG['username'], SMTP_CONFIG['password'])
                server.send_message(msg)
                print("Email sent successfully via STARTTLS")
                return True
            except Exception as e1:
                print(f"STARTTLS failed: {e1}, trying SSL on port 465...")
                if server:
                    try: server.quit()
                    except: pass
                try:
                    server = smtplib.SMTP_SSL(SMTP_CONFIG['server'], 465, timeout=10)
                    server.login(SMTP_CONFIG['username'], SMTP_CONFIG['password'])
                    server.send_message(msg)
                    print("Email sent successfully via SSL")
                    return True
                except Exception as e2:
                    print(f"SSL also failed: {e2}")
                    raise e2
            finally:
                if server:
                    try: server.quit()
                    except: pass

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, _send_blocking)

        return {"status_code": 200, "message": "email has been sent"}
    except Exception as e:
        print(f"Email sending error: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return {"status_code": 500, "message": f"Failed to send email: {str(e)}"}

    # return f"{base_url}?{query_params}"

# Function to validate a magic link on the server side
def validate_magic_link_server(user_email: str, timestamp: str, token: str):
    try:
        # Check if the link is expired (30 minutes)
        current_time = int(time.time())
        if current_time - int(timestamp) > 1800:  # 1800 seconds = 30 minutes
            return False, "Link expired"

        # Recreate the token and compare
        data = f"{user_email}{timestamp}{SECRET_KEY}"
        expected_token = hashlib.sha256(data.encode()).hexdigest()
        if token != expected_token:
            return False, "Invalid token"

        # Valid magic link - return user data to be set in UI context
        user_data = {
            "email": user_email,
            "timestamp": timestamp,
            "username": user_email.split('@')[0].title()
        }
        print(user_data)
        userToken = create_jwt_token(user_data)
        print(userToken)
        if userToken:
            return True, userToken  # Return token instead of setting storage here
        else:
            return False, "Failed to create authentication token"
        
    except Exception as e:
        return False, f"Authentication failed: {str(e)}"

# Function to validate a magic link from URL parameters
async def validate_magic_link_from_url(redirect_to: str = '/hrmkit/reporting/dashboard'):
    try:
        # Get URL parameters from the request context
        from fastapi import Request
        from nicegui import context
        
        # Try to get URL parameters from NiceGUI context
        if hasattr(context, 'client') and context.client and hasattr(context.client, 'request'):
            request = context.client.request
            if request and hasattr(request, 'query_params'):
                query_params = dict(request.query_params)
                user_email = query_params.get("email")
                timestamp = query_params.get("timestamp")
                token = query_params.get("token")

                if user_email and timestamp and token:
                    # Check if the link is expired (30 minutes)
                    current_time = int(time.time())
                    if current_time - int(timestamp) > 1800:  # 1800 seconds = 30 minutes
                        ui.notify("Magic link has expired. Please request a new one.", color='negative')
                        ui.navigate.to('/hrmkit/')
                        return

                    # Recreate the token and compare
                    data = f"{user_email}{timestamp}{SECRET_KEY}"
                    expected_token = hashlib.sha256(data.encode()).hexdigest()
                    if token != expected_token:
                        ui.notify("Invalid magic link. Please request a new one.", color='negative')
                        ui.navigate.to('/hrmkit/')
                        return

                    # Valid magic link - authenticate user
                    try:
                        user_data = {
                            "email": user_email,
                            "timestamp": timestamp,
                            "username": user_email.split('@')[0].title()
                        }
                        userToken = create_jwt_token(user_data)
                        set_auth_data({'token': userToken, 'authenticated': True})
                        ui.notify(f"Welcome {user_data['username']}! You have been successfully logged in.", color='positive')
                        
                        # Redirect to clean dashboard URL
                        ui.navigate.to('/hrmkit/reporting/dashboard')
                        
                    except Exception as e:
                        ui.notify("Authentication failed. Please try again.", color='negative')
                        ui.navigate.to('/hrmkit/')
    except Exception as e:
        print(f"Error in magic link validation: {e}")
    # Don't show error to user, just continue to dashboard if they're authenticated

# Function to validate a magic link
def validate_magic_link(redirect_to: str = '/'):
    # url = await ui.run_javascript('window.location.href')
    # print(current_url)
    if current_url:
        parsed_url = urlparse(current_url)
        query_params = parse_qs(parsed_url.query)
        user_email = query_params.get("email", [None])[0]
        timestamp = query_params.get("timestamp", [None])[0]
        token = query_params.get("token", [None])[0]

        if not user_email or not timestamp or not token:
            return False, "Invalid link"

        # Check if the link is expired (e.g., 15 minutes)
        current_time = int(time.time())
        if current_time - int(timestamp) > 1800:  # 1800 seconds = 30 minutes
            return False, "Link expired"

        # Recreate the token and compare
        data = f"{user_email}{timestamp}{SECRET_KEY}"
        expected_token = hashlib.sha256(data.encode()).hexdigest()
        if token != expected_token:
            return False, "Invalid token"

        try:
            user_data = {
                "email": user_email,
                "timestamp": timestamp,
                "username": 'John Doe'
            }
            userToken = create_jwt_token(user_data)
            set_auth_data({'token': userToken, 'authenticated': True})
            # app.add_route(redirect_to)
            return RedirectResponse(url=redirect_to)
        
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

def create_jwt_token(data: dict):
    try:
        import jwt as PyJWT
        payload = {
            "email": data['email'],
            "iat": int(time.time()),
            "exp": int(time.time() + JWT_TOKEN_LIFETIME.total_seconds()),
            "username": data['username']
        }

        token = PyJWT.encode(payload, JWT_TOKEN_KEY, algorithm="HS256")
        return token
    except Exception as e:
        print(f"PyJWT encoding error: {e}")
        # Fallback to simple encoding if jwt library not available
        try:
            date = datetime.fromtimestamp(int(data['timestamp']))
            payload = {
                "email": data['email'],
                "iat": int(date.timestamp()),
                "exp": int((date + JWT_TOKEN_LIFETIME).timestamp()),
                "username": data['username']
            }

            # Use simple JWT encoding for now
            token = encode_jwt_simple(payload)
            return token
        except Exception as e:
            print(f"JWT encoding error: {e}")
            return None
    except Exception as e:
        print(f"JWT encoding error: {e}")
        return None

def decode_jwt_token(token: str):
    try:
        import jwt as PyJWT
        # Try PyJWT first
        data = PyJWT.decode(token, JWT_TOKEN_KEY, algorithms=["HS256"])
        return data if (data and "email" in data) else None
    except Exception as e:
        print(f"PyJWT decode error: {e}")
        # Fallback to simple decoding
        try:
            if not token or '.' not in token:
                return None

            parts = token.split('.')
            if len(parts) < 2:
                return None

            # Decode payload (add padding if needed)
            payload_b64 = parts[1]
            padding = 4 - len(payload_b64) % 4
            if padding != 4:
                payload_b64 += '=' * padding

            payload_str = base64.urlsafe_b64decode(payload_b64).decode()
            data = json.loads(payload_str)

            # Check expiration
            if 'exp' in data and int(time.time()) > data['exp']:
                print("JWT token has expired")
                return None

            return data if (data and "email" in data) else None
        except Exception as e:
            print(f"Simple JWT decode error: {e}")
            return None
    except Exception as e:
        print(f"JWT token decode error: {e}")
        return None
    #     return None
    
def extract_user() -> None:
      if is_authenticated():
          return RedirectResponse('/')

      token = get_auth_value(JWT_TOKEN_KEY)
      if not token:
          return None
      data = decode_jwt_token(token)
      if not data:
          return None

      if not (datetime.time(data['exp']) - datetime.now().time()) > 0:
          clear_auth_data()
          return RedirectResponse('/')
      return data

# Example usage
# magic_link = generate_magic_link("user@example.com")
# print("Generated Magic Link:", magic_link)

# is_valid, message = validate_magic_link(magic_link)
# print("Validation Result:", message)


# import jwt

# JWT_TOKEN_KEY = 'espressotoken'
# JWT_TOKEN_LIFETIME = timedelta(days=7)

# def create_jwt_token(email: str):
#     data = {
#         "email": email,
#         "iat": datetime.now(),
#         "exp": datetime.now() + JWT_TOKEN_LIFETIME
#     }
#     return jwt.encode(data, APP_STORAGE_SECRET, algorithm="HS256")

# def login_user(user: dict|User):
#     email = user.email if isinstance(user, User) else user['email']
#     app.storage.browser[JWT_TOKEN_KEY] = create_jwt_token(email)

# def extract_user() -> User:
#     token = app.storage.browser.get(JWT_TOKEN_KEY)
#     if not token:
#         return None
#     data = decode_jwt_token(token)
#     if not data:
#         del app.storage.browser[JWT_TOKEN_KEY]
#         return None
#     user = user_db.get_user(data["email"])
#     if not user:
#         del app.storage.browser[JWT_TOKEN_KEY]
#         return None
#     return user

# Development bypass function for testing
def create_dev_auth_token(email: str = "dev@hrmkit.com"):
    """Create a development authentication token for testing purposes"""
    user_data = {
        "email": email,
        "timestamp": int(time.time()),
        "username": email.split('@')[0].title()
    }
    return create_jwt_token(user_data)