# my_package/__init__.py

__version__ = "1.0.0"
__author__ = "KWARECOM Inc."

from .helperFuns import *
from .components import *
from .assets import *
from .layout import *
from .frontend import init  

print(f"Initializing HRkit version {__version__}")
