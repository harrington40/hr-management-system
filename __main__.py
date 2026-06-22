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

    dev_mode = os.environ.get("HRMS_DEV", "").lower() in ("1", "true", "yes")

    print("""
    🚀 Starting HRMS (HR Management System)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    📍 Base URL:    http://127.0.0.1:8000
    📊 API Docs:    http://127.0.0.1:8000/docs
    📋 ReDoc:       http://127.0.0.1:8000/redoc
    🔁 Hot-reload:  {reload}
    🛑 To stop:     Press CTRL+C
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """.format(reload="ON  (HRMS_DEV=true)" if dev_mode else "OFF (use ./dev.sh for dev mode)"))

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=dev_mode,
        reload_dirs=[os.path.dirname(__file__)] if dev_mode else None,
        reload_includes=["*.py", "*.yaml", "*.yml", "*.html"] if dev_mode else None,
        log_level="info"
    )
