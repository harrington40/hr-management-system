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

    prod_mode = os.environ.get("HRMS_PROD", "").lower() in ("1", "true", "yes")
    reload_enabled = not prod_mode

    print("""
    🚀 Starting HRMS (HR Management System)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    📍 Base URL:    http://127.0.0.1:8000
    📊 API Docs:    http://127.0.0.1:8000/docs
    📋 ReDoc:       http://127.0.0.1:8000/redoc
    🔁 Hot-reload:  {reload}
    🛑 To stop:     Press CTRL+C
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """.format(reload="ON  (default)" if reload_enabled else "OFF (HRMS_PROD=true)"))

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=reload_enabled,
        reload_dirs=[os.path.dirname(__file__)] if reload_enabled else None,
        reload_includes=["*.py", "*.yaml", "*.yml", "*.html"] if reload_enabled else None,
        log_level="info"
    )
