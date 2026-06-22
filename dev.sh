#!/bin/bash
# =============================================================================
# HRMS Development Mode — hot-reload is ON by default now.
# This is a convenience wrapper; plain `python3 __main__.py` does the same.
# =============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║       HRMS — hot-reload ON  (default)                        ║"
echo "║       Watching *.py *.yaml *.yml *.html for changes          ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Quick dependency check
if ! python3 -c "import uvicorn; import watchfiles" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt --quiet
fi

python3 __main__.py
