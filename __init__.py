# my_package/__init__.py

# Read version from VERSION file
import os
from pathlib import Path

def _get_version():
    version_file = Path(__file__).parent / 'VERSION'
    if version_file.exists():
        return version_file.read_text().strip()
    return "1.0.0"

__version__ = _get_version()
__author__ = "KWARECOM Inc."

# from .helperFuns import *
# from .components import *
# from .assets import *
# from .layout import *
from frontend import init  
# from .services import *
# Note: Relative imports removed to avoid pytest collection issues
# Import modules directly when needed instead of through root __init__.py  

print(f"Initializing HRkit version {__version__}")
