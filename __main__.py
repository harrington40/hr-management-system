"""
HRMS Main Entry Point
"""
import sys
import os

# Set up the path for the package
sys.path.insert(0, os.path.dirname(__file__))

import uvicorn

if __name__ == "__main__":
    from main import app
    print("""
    🚀 Starting HRMS (HR Management System)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    📍 Base URL:    http://127.0.0.1:8000
    📊 API Docs:    http://127.0.0.1:8000/docs
    📋 ReDoc:       http://127.0.0.1:8000/redoc
    🛑 To stop:     Press CTRL+C
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info"
    )
