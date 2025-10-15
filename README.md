# HR Management System

A comprehensive, enterprise-grade HR management dashboard with real-time analytics, hardware integration, and modern UI.

## Features
- Modern dashboard for HR, managers, and employees
- Real-time attendance, performance, and compliance metrics
- Hardware integration (biometric, card reader, face recognition)
- AI-powered analytics and predictions
- Role-based access and management

## Folder Structure
- `main.py` / `frontend.py`: Main entry point
- `components/`: Modular UI and logic (dashboard, timesheets, auth, etc.)
- `assets/`: Images, icons, styles
- `config/`: YAML config files for dashboard, hardware, employees, etc.
- `apis/`: Database and user models
- `helperFuns/`, `layout/`: Utility and layout modules

## Quick Start
1. **Clone the repository**
   ```bash
   git clone https://github.com/harrington40/hr-management-system.git
   cd hr-management-system
   ```
2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirement.txt
   ```
4. **Run the application**
   ```bash
   python main.py
   # or
   python frontend.py
   ```

## Notes
- Do **not** commit your local `venv/` folder or `.DS_Store` files.
- All configuration is in the `config/` folder. Edit YAML files as needed.
- For hardware integration, ensure your devices are configured in `config/hardware_devices.yaml`.

## License
MIT
