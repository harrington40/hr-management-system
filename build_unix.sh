#!/bin/bash

# HRMS Build Script for Linux/macOS
# This script builds the application executable

set -e  # Exit on any error

echo "Building HRMS Application..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.9"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "ERROR: Python $REQUIRED_VERSION or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi

echo "Using Python $PYTHON_VERSION"

# Upgrade pip
echo "Upgrading pip..."
python3 -m pip install --upgrade pip

# Install PyInstaller
echo "Installing PyInstaller..."
pip3 install pyinstaller

# Install project dependencies
echo "Installing project dependencies..."
pip3 install -r requirement.txt

# Create output directory
mkdir -p dist

# Detect platform
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PLATFORM="linux"
    EXECUTABLE_NAME="hrms_app_linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macos"
    EXECUTABLE_NAME="hrms_app_macos"
else
    echo "Unsupported platform: $OSTYPE"
    exit 1
fi

echo "Building for $PLATFORM..."

# Build with PyInstaller
echo "Building executable..."
pyinstaller \
    --clean \
    --onefile \
    --name "$EXECUTABLE_NAME" \
    --hidden-import fastapi \
    --hidden-import uvicorn \
    --hidden-import nicegui \
    --hidden-import sqlalchemy \
    --hidden-import grpc \
    --hidden-import pydantic \
    --hidden-import starlette \
    --hidden-import components.attendance.attendance_rules \
    --hidden-import components.attendance.shift_timetable \
    --hidden-import components.authentication.auth \
    --hidden-import components.reports.dashboard \
    --hidden-import helperFuns.helperFuns \
    --hidden-import layout.sidebar \
    --hidden-import apis.db \
    --hidden-import apis.userModel \
    --add-data "assets:assets" \
    --add-data "config:config" \
    --add-data "database:database" \
    --exclude-module tkinter \
    --exclude-module matplotlib \
    --exclude-module numpy \
    main.py

echo
echo "Build completed successfully!"
echo
echo "Output file: dist/$EXECUTABLE_NAME"
echo
echo "To run the application:"
echo "  ./dist/$EXECUTABLE_NAME"
echo
echo "Note: Make sure PostgreSQL is running and properly configured."
echo "The application will use the configuration in config/ directory."