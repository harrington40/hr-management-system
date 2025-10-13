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
from helperFuns import readEnv
import jwt as PyJWT

# import helperFuns.helperFuns
current_url = ''
unrestricted_page_routes = {'/'}
routes_to_reroute = ['/']
JWT_TOKEN_LIFETIME = timedelta(days=7)
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
# app.add_middleware(AuthMiddleware)

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
            origin = readEnv('APP_ORIGIN') or 'http://127.0.0.1:8080'
            # Ensure no trailing slash
            origin = origin.rstrip('/')
            base_url = f"{origin}/auth"

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
        msg['From'] = SMTP_CONFIG['username']
        msg['To'] = user_email
        
        # Create HTML part
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        # Send email using SMTP
        server = smtplib.SMTP(SMTP_CONFIG['server'], SMTP_CONFIG['port'])
        server.starttls()
        server.login(SMTP_CONFIG['username'], SMTP_CONFIG['password'])
        server.send_message(msg)
        server.quit()
        
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
    except Exception as e:
        print(f"Email sending error: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"message": f"Failed to send email: {str(e)}"})

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
        userToken = create_jwt_token(user_data)
        
        if userToken:
            return True, userToken  # Return token instead of setting storage here
        else:
            return False, "Failed to create authentication token"
        
    except Exception as e:
        return False, f"Authentication failed: {str(e)}"

# Function to validate a magic link from URL parameters
async def validate_magic_link_from_url(redirect_to: str = '/hrmkit/dashboard'):
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
                        app.storage.user.update({'token': userToken, 'authenticated': True})
                        ui.notify(f"Welcome {user_data['username']}! You have been successfully logged in.", color='positive')
                        
                        # Redirect to clean dashboard URL
                        ui.navigate.to('/hrmkit/dashboard')
                        
                    except Exception as e:
                        ui.notify("Authentication failed. Please try again.", color='negative')
                        ui.navigate.to('/hrmkit/')
    except Exception as e:
        print(f"Error in magic link validation: {e}")
    # Don't show error to user, just continue to dashboard if they're authenticated

# Function to validate a magic link
def validate_magic_link(redirect_to: str = '/'):
    # url = await ui.run_javascript('window.location.href')
    print(current_url)
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
            app.storage.user.update({'token': userToken, 'authenticated': True})
            # app.add_route(redirect_to)
            return RedirectResponse(url=redirect_to)
        
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

def create_jwt_token(data: dict):
    try:
        date = datetime.fromtimestamp(int(data['timestamp']))
        payload = {
            "email": data['email'],
            "iat": int(date.timestamp()),
            "exp": int((date + JWT_TOKEN_LIFETIME).timestamp()),
            "username": data['username']
        }
        # Use PyJWT encode function
        token = PyJWT.encode(payload, SECRET_KEY, algorithm="HS256")
        return token
    except Exception as e:
        print(f"JWT encoding error: {e}")
        return None

def decode_jwt_token(token: str):
    try:
        # Use PyJWT decode function
        data = PyJWT.decode(token, SECRET_KEY, algorithms=["HS256"])
        return data if (data and "email" in data) else None
    except PyJWT.ExpiredSignatureError:
        print("JWT token has expired")
        return None
    except PyJWT.InvalidTokenError as err:
        print(f"JWT token decode error: {str(err)}")
        return None
    
def extract_user() -> None:
     if app.storage.user.get('authenticated', False):
        return RedirectResponse('/')
     
     token = app.storage.user.get(JWT_TOKEN_KEY)
     if not token:
        return None
     data = decode_jwt_token(token)
     if not data:
        del app.storage.browser[JWT_TOKEN_KEY]
        return None

     if not (datetime.time(data['exp']) - datetime.now().time()) > 0:
        app.storage.user.clear()
        return RedirectResponse('/')
        # return None
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