"""
Version management for HRMS Application
Automatically updated by CI/CD pipeline
"""
import os
from pathlib import Path

def get_version():
    """Get the current version from VERSION file"""
    version_file = Path(__file__).parent / 'VERSION'
    if version_file.exists():
        return version_file.read_text().strip()
    return "0.0.0"

def get_build_info():
    """Get build information from environment variables"""
    return {
        'version': get_version(),
        'build_number': os.getenv('BUILD_NUMBER', 'local'),
        'commit_sha': os.getenv('GIT_COMMIT', 'unknown')[:8],
        'branch': os.getenv('BRANCH_NAME', 'unknown'),
        'environment': os.getenv('ENVIRONMENT', 'development'),
    }

def get_full_version():
    """Get full version string with build info"""
    info = get_build_info()
    if info['build_number'] != 'local':
        return f"{info['version']}-{info['environment']}.{info['build_number']}"
    return info['version']

__version__ = get_version()
__build__ = get_build_info()

if __name__ == '__main__':
    print(f"Version: {get_version()}")
    print(f"Full Version: {get_full_version()}")
    print(f"Build Info: {get_build_info()}")
