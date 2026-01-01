# HRMS Windows Build Guide

This guide explains how to build Windows executable and installer for the HRMS application.

## Prerequisites

### For Windows Builds
- **Python 3.9+** - Download from [python.org](https://python.org)
- **Git** - For cloning the repository
- **NSIS** (Optional but recommended) - For creating installers
  - Download from [nsis.sourceforge.io](https://nsis.sourceforge.io/)
  - Or install via Chocolatey: `choco install nsis`

### For Linux/macOS Builds
- **Python 3.9+**
- **Git**
- Bash shell

## Quick Start

### Windows
1. Clone the repository:
   ```cmd
   git clone https://github.com/harrington40/hr-management-system.git
   cd hr-management-system
   ```

2. Run the build script:
   ```cmd
   build_windows.bat
   ```

### Linux/macOS
1. Clone the repository:
   ```bash
   git clone https://github.com/harrington40/hr-management-system.git
   cd hr-management-system
   ```

2. Make the build script executable:
   ```bash
   chmod +x build_unix.sh
   ```

3. Run the build script:
   ```bash
   ./build_unix.sh
   ```

## Manual Build Process

### Step 1: Install Dependencies
```bash
pip install -r requirement.txt
pip install pyinstaller
```

### Step 2: Build Executable (Windows)
```cmd
pyinstaller --clean hrms.spec
```

### Step 3: Create Installer (Windows)
```cmd
makensis installer.nsi
```

## Output Files

After successful build, you'll find:

### Windows
- `dist/HRMS_Application.exe` - Standalone executable
- `HRMS_Application_installer.exe` - Windows installer (if NSIS is available)

### Linux/macOS
- `dist/hrms_app_linux` or `dist/hrms_app_macos` - Standalone executable

## Running the Application

### From Executable
1. Double-click the executable file
2. Or run from command line:
   ```cmd
   HRMS_Application.exe
   ```

### From Installer (Windows)
1. Run `HRMS_Application_installer.exe`
2. Follow the installation wizard
3. Launch from Start Menu or Desktop shortcut

## Configuration

The executable includes all necessary configuration files. Before running:

1. **Database Setup**: Ensure PostgreSQL is installed and running
2. **Configuration**: Edit `config/production.env` or create your own config file
3. **Environment Variables**: Set required environment variables

### Default Configuration
The application looks for configuration in this order:
1. Environment variables
2. `config/production.env`
3. `config/staging.env`
4. `config/test.env`

## Troubleshooting

### Common Issues

#### "Python is not recognized"
- Ensure Python is installed and added to PATH
- Try `python` instead of `python3`

#### "PyInstaller not found"
```bash
pip install pyinstaller
```

#### "NSIS not found"
- Install NSIS from the official website
- Or use Chocolatey: `choco install nsis`

#### "Build fails with import errors"
- Ensure all dependencies are installed: `pip install -r requirement.txt`
- Check that all required modules are listed in `hrms.spec`

#### "Application won't start"
- Check database connection
- Verify configuration files exist
- Check logs for error messages

#### Large executable size
- The executable includes all dependencies
- Size is typically 50-100MB depending on included libraries
- Use UPX compression (enabled by default in spec file)

### Build Logs
- Check the console output for detailed error messages
- PyInstaller logs are saved in the `build/` directory

## CI/CD Integration

The Windows build is automatically included in the GitHub Actions CI/CD pipeline:

- **Trigger**: On pushes to `main` or `dev` branches
- **Platform**: `windows-latest`
- **Artifacts**: Executable and installer uploaded as build artifacts
- **Dependencies**: Runs after unit, integration, and regression tests pass

### Manual Release Build
To create a release build manually:

1. Go to GitHub Actions
2. Select "CI/CD Pipeline"
3. Click "Run workflow"
4. Choose the appropriate branch
5. Download artifacts after completion

## Advanced Configuration

### Customizing the Spec File
Edit `hrms.spec` to:
- Add/remove hidden imports
- Include additional data files
- Modify build options
- Change output name

### Customizing the Installer
Edit `installer.nsi` to:
- Change installation directory
- Add/remove shortcuts
- Modify registry entries
- Add custom installation steps

### Reducing Size
To reduce executable size:
1. Exclude unnecessary modules in the spec file
2. Use `--exclude-module` options
3. Enable UPX compression
4. Strip debug information

### Adding an Icon
1. Create or obtain an `.ico` file
2. Place it in `assets/images/icons/app_icon.ico`
3. The spec file will automatically include it

## Distribution

### For End Users
- Provide the installer (`HRMS_Application_installer.exe`) for easy installation
- Or distribute the executable (`HRMS_Application.exe`) for portable use

### System Requirements
- **OS**: Windows 10/11, Linux (Ubuntu 18.04+), macOS 10.15+
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: 500MB free space
- **Database**: PostgreSQL 13+ (can be installed separately)

## Support

For build-related issues:
1. Check this documentation
2. Review build logs
3. Check GitHub Issues
4. Create a new issue with build logs and error messages

## File Structure

```
hrms-main/
├── hrms.spec              # PyInstaller specification
├── installer.nsi          # NSIS installer script
├── build_windows.bat      # Windows build script
├── build_unix.sh          # Linux/macOS build script
├── dist/                  # Build output directory
│   └── HRMS_Application.exe
├── assets/                # Application assets
├── config/                # Configuration files
└── database/              # Database files
```