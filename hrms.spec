# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent

# Define paths
main_script = project_root / 'main.py'
assets_dir = project_root / 'assets'
components_dir = project_root / 'components'
helper_dir = project_root / 'helperFuns'
layout_dir = project_root / 'layout'
config_dir = project_root / 'config'
database_dir = project_root / 'database'
grpc_services_dir = project_root / 'grpc_services'
services_dir = project_root / 'services'

block_cipher = None

a = Analysis(
    [str(main_script)],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        # Include all necessary data files
        (str(assets_dir), 'assets'),
        (str(config_dir), 'config'),
        (str(database_dir / 'hrms_schema.sql'), 'database'),
        (str(database_dir / 'hrms_schema_clean.sql'), 'database'),
        ('requirements.txt', '.'),
        ('frontend.py', '.'),
        ('run_dual_services.py', '.'),
        ('run_grpc_only.py', '.'),
        ('__init__.py', '.'),
    ],
    hiddenimports=[
        # FastAPI and related
        'fastapi',
        'uvicorn',
        'uvicorn.workers',
        'starlette',
        'pydantic',
        'pydantic_settings',

        # NiceGUI
        'nicegui',
        'nicegui.elements',
        'nicegui.events',
        'nicegui.binding',
        'nicegui.storage',

        # Database
        'sqlalchemy',
        'psycopg2',
        'mysql.connector',
        'pyorient',

        # gRPC
        'grpc',
        'grpc_services',
        'services.hrms_pb2',
        'services.hrms_pb2_grpc',

        # Email
        'aiosmtplib',
        'fastapi_mail',

        # Other dependencies
        'bcrypt',
        'cryptography',
        'jwt',
        'python-dotenv',
        'pyyaml',
        'rich',
        'click',
        'websockets',
        'python-socketio',
        'paho.mqtt',

        # Component modules
        'components.attendance',
        'components.attendance.attendance_rules',
        'components.attendance.shift_timetable',
        'components.authentication',
        'components.authentication.auth',
        'components.authentication.authHelper',
        'components.reports',
        'components.reports.dashboard',
        'components.administration',
        'components.administration.admin_management',
        'components.dashboard',
        'components.dashboard.dashboard_main',
        'components.employees',
        'components.employees.employee_management',

        # Helper modules
        'helperFuns.helperFuns',
        'layout.sidebar',

        # Database modules
        'apis.db',
        'apis.userModel',
        'database.init_database',
        'database.test_database',

        # Service modules
        'services.auth_service',
        'services.hrms_service',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce size
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'sklearn',
        'tensorflow',
        'torch',
        'PIL',
        'opencv',
        'cv2',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='HRMS_Application',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to False for windowed app, True for console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/images/icons/app_icon.ico' if os.path.exists('assets/images/icons/app_icon.ico') else None,
)