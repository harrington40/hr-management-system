#!/bin/bash
# =============================================================================
# HRMS Startup Script
# Starts FastAPI (port 8000) + gRPC (port 50051) services
# =============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║       HRMS — HR Management System                            ║"
echo "║       Dual Service Mode (FastAPI + gRPC)                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# ── Check Python ──────────────────────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $PYTHON_VERSION detected"

# ── Check / install dependencies ──────────────────────────────────────────
if [ -f "requirements.txt" ]; then
    # Quick check: is the first key package installed?
    if ! python3 -c "import fastapi" 2>/dev/null; then
        echo ""
        echo "📦 Installing dependencies from requirements.txt..."
        pip3 install -r requirements.txt
    else
        echo "✅ Dependencies already installed"
    fi
else
    echo "⚠️  requirements.txt not found — skipping dependency check"
fi

# ── Load .env if present ──────────────────────────────────────────────────
if [ -f ".env" ]; then
    echo "✅ .env file found"
    export $(grep -v '^#' .env | grep -v '^$' | xargs)
else
    echo "⚠️  .env file not found — using defaults from config/services.py"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📱 Web UI:   http://localhost:8000/hrmkit/"
echo "  📊 API Docs: http://localhost:8000/docs"
echo "  🔧 gRPC:     localhost:50051"
echo "  🔁 Hot-reload: OFF (production mode)"
echo "  Stop:       Press CTRL+C"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

HRMS_PROD=true python3 run_dual_services.py
