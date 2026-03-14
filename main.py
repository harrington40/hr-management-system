# import uvicorn
from fastapi.responses import RedirectResponse
from frontend import init
from fastapi import FastAPI #Depends, HTTPException
# from contextlib import asynccontextmanager
import logging
from starlette.middleware.sessions import SessionMiddleware
import secrets

import urllib.parse

# Import service manager
from services import get_service_manager
from components import validate_magic_link_server, create_jwt_token
from helperFuns import readEnv, get_mount_path, build_mount_route
    

# from sqlmodel import select
# from sqlmodel import Session, select

# from apis.db import get_session, init_db
# from apis.userModel import User

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

APP_MOUNT_PATH = get_mount_path()


def mount_route(sub_path: str = '') -> str:
    return build_mount_route(sub_path, base=APP_MOUNT_PATH)


app = FastAPI()  # Remove lifespan for debugging

# Add health check endpoint for Jenkins smoke tests
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "HRMS Application",
        "version": "1.0.0",
        "timestamp": str(__import__("datetime").datetime.now())
    }

# Add SessionMiddleware for NiceGUI first (added in reverse order)
# Initialize session with required 'id' key
from starlette.middleware.base import BaseHTTPMiddleware

class SessionInitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if 'session' not in request.scope:
            request.scope['session'] = {}
        # Ensure 'id' exists in session
        if 'id' not in request.scope.get('session', {}):
            request.scope['session']['id'] = secrets.token_urlsafe(16)
        response = await call_next(request)
        return response

# Add in reverse order: SessionInitMiddleware first, then SessionMiddleware
app.add_middleware(SessionInitMiddleware)
app.add_middleware(SessionMiddleware, secret_key=secrets.token_urlsafe(32))

service_manager = get_service_manager()
# Initialize services immediately
logger.info("Initializing HRMS services...")
if not service_manager.initialize_services():
    logger.error("Failed to initialize some services - application may have limited functionality")
else:
    logger.info("All services initialized successfully")

# @app.liespan("startup")
# def on_startup():
#     init_db()

@app.get('/')
def read_root():
    return {"message": f"Welcome to HRMkit! Visit {APP_MOUNT_PATH} for the application."}

@app.get('/health')
def health_check():
    """Health check endpoint to verify services"""
    services_status = {
        'database': service_manager.is_service_available('database'),
        'mqtt': service_manager.is_service_available('mqtt'),
        'backblaze': service_manager.is_service_available('backblaze'),
        'grpc': service_manager.is_service_available('grpc'),
        'overall': service_manager.is_initialized
    }
    return {
        "status": "healthy" if service_manager.is_initialized else "degraded",
        "services": services_status
    }

@app.get('/auth')
def auth_endpoint(email: str, timestamp: str, token: str):
    """Handle magic link authentication"""
    # Validate the magic link
    is_valid, message = validate_magic_link_server(email, timestamp, token)

    if not is_valid:
        return RedirectResponse(url=f"{mount_route()}?error={message}", status_code=302)

    # Generate JWT token for the user
    user_data = {
        "email": email,
        "username": email.split('@')[0],
        "timestamp": timestamp
    }
    jwt_token = create_jwt_token(user_data)

    if jwt_token is None:
        return RedirectResponse(url=f"{mount_route()}?error=Failed%20to%20generate%20token", status_code=302)

    # Relative redirect so this works on any host (local or production)
    return RedirectResponse(
        url=f"{mount_route('/reporting/dashboard')}?jwt_token={jwt_token}&username={email.split('@')[0]}",
        status_code=302
    )

@app.get(mount_route('/auth'))
def hrmkit_auth_endpoint(email: str = '', timestamp: str = '', token: str = ''):
    """FastAPI HTTP handler for magic link auth — no WebSocket/NiceGUI context needed."""
    if not email or not timestamp or not token:
        return RedirectResponse(url=f"{mount_route()}?error=Missing+parameters", status_code=302)

    is_valid, result = validate_magic_link_server(email, timestamp, token)
    if not is_valid:
        return RedirectResponse(url=f"{mount_route()}?error={urllib.parse.quote(str(result))}", status_code=302)

    # result is the JWT token; pass it via URL so dashboard can consume it in a timer
    return RedirectResponse(
        url=f"{mount_route('/reporting/dashboard')}?jwt_token={urllib.parse.quote(result)}&email={urllib.parse.quote(email)}",
        status_code=302
    )

init(app)

if __name__ == '__main__':
    # uvicorn.run('main:fastapi_app', log_level='info', reload=True)
    print('Please start the app with the "uvicorn" command as shown in the start.sh script')