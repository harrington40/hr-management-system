#!/bin/bash
# =============================================================================
# HRMS Development Mode — auto-reloads on code changes
# Uses watchfiles via uvicorn --reload (HRMS_DEV=true)
# =============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

export HRMS_DEV=true

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║       HRMS — DEVELOPMENT MODE (hot-reload ON)                ║"
echo "║       Watching *.py *.yaml *.yml *.html for changes          ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Quick dependency check
if ! python3 -c "import uvicorn; import watchfiles" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt --quiet
fi

python3 __main__.py
