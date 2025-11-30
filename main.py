# import uvicorn
from fastapi.responses import RedirectResponse
from .frontend import init
from fastapi import FastAPI #Depends, HTTPException
# from contextlib import asynccontextmanager
import logging

# Import service manager
from .services import get_service_manager
from .components import validate_magic_link_server, create_jwt_token
    

# from sqlmodel import select
# from sqlmodel import Session, select

# from apis.db import get_session, init_db
# from apis.userModel import User

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()  # Remove lifespan for debugging
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
    return {"message": "Welcome to HRMkit! Visit /hrmkit for the application."}

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
        # Redirect to login page with error
        return RedirectResponse(url=f"http://127.0.0.1:8000/hrmkit/?error={message}", status_code=302)
    
    # Generate JWT token for the user
    user_data = {
        "email": email, 
        "username": email.split('@')[0],
        "timestamp": timestamp
    }
    jwt_token = create_jwt_token(user_data)
    
    if jwt_token is None:
        return RedirectResponse(url=f"http://127.0.0.1:8000/hrmkit/?error=Failed%20to%20generate%20token", status_code=302)
    
    # Redirect to dashboard with JWT token
    return RedirectResponse(url=f"http://127.0.0.1:8000/hrmkit/reporting/dashboard?jwt_token={jwt_token}&username={email.split('@')[0]}", status_code=302)

init(app)

if __name__ == '__main__':
    # uvicorn.run('main:fastapi_app', log_level='info', reload=True)
    print('Please start the app with the "uvicorn" command as shown in the start.sh script')