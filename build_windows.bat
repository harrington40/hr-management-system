@echo off
REM HRMS Windows Build Script
REM This script builds the Windows executable and installer

echo Building HRMS Windows Application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ and add it to your PATH
    pause
    exit /b 1
)

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    pause
    exit /b 1
)

echo Installing/Upgrading build dependencies...
pip install --upgrade pip
pip install pyinstaller

echo.
echo Installing project dependencies...
pip install -r requirement.txt

echo.
echo Creating application icon...
if not exist "assets\images\icons" (
    mkdir "assets\images\icons"
)
REM For now, we'll skip icon creation
REM In production, you would convert an existing image to .ico format

echo.
echo Building executable with PyInstaller...
pyinstaller --clean hrms.spec

if errorlevel 1 (
    echo ERROR: PyInstaller build failed
    pause
    exit /b 1
)

echo.
echo Checking for NSIS...
where makensis >nul 2>&1
if errorlevel 1 (
    echo NSIS not found. Installing NSIS...
    REM Try to install NSIS using Chocolatey
    where choco >nul 2>&1
    if errorlevel 1 (
        echo Chocolatey not found. Please install NSIS manually from https://nsis.sourceforge.io/
        echo Or install Chocolatey and run: choco install nsis
        goto :skip_installer
    )
    choco install nsis -y
)

echo.
echo Creating Windows installer...
makensis installer.nsi

if errorlevel 1 (
    echo WARNING: NSIS installer creation failed
    goto :skip_installer
)

echo.
echo Build completed successfully!
echo.
echo Output files:
if exist "dist\HRMS_Application.exe" echo - Executable: dist\HRMS_Application.exe
if exist "HRMS_Application_installer.exe" echo - Installer: HRMS_Application_installer.exe
echo.
echo You can now run the executable or distribute the installer.
goto :end

:skip_installer
echo.
echo Build completed successfully!
echo.
echo Output files:
if exist "dist\HRMS_Application.exe" echo - Executable: dist\HRMS_Application.exe
echo.
echo NSIS installer was not created. You can still use the executable.
echo To create an installer, install NSIS from https://nsis.sourceforge.io/

:end
echo.
pause