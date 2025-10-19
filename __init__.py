# my_package/__init__.py

__version__ = "1.0.0"
__author__ = "KWARECOM Inc."

# Note: Relative imports removed to avoid pytest collection issues
# Import modules directly when needed instead of through root __init__.py  

print(f"Initializing HRkit version {__version__}")
