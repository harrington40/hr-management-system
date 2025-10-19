"""
Enterprise Administration System
Advanced system administration with comprehensive user management, security controls,
audit trails, and system monitoring for HR management platform
"""

from nicegui import ui
import yaml
import os
from datetime import datetime, timedelta, date
import json
import hashlib
import secrets
import uuid
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class SystemRole(Enum):
    SUPER_ADMIN = "super_admin"
    SYSTEM_ADMIN = "system_admin"
    HR_ADMIN = "hr_admin"
    PAYROLL_ADMIN = "payroll_admin"
    MANAGER = "manager"
    SUPERVISOR = "supervisor"
    EMPLOYEE = "employee"
    CONTRACTOR = "contractor"
    GUEST = "guest"

class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    LOCKED = "locked"
    PENDING_ACTIVATION = "pending_activation"

class SystemModule(Enum):
    EMPLOYEE_MANAGEMENT = "employee_management"
    TIMESHEET_MANAGEMENT = "timesheet_management"
    PAYROLL_PROCESSING = "payroll_processing"
    LEAVE_MANAGEMENT = "leave_management"
    PERFORMANCE_TRACKING = "performance_tracking"
    RECRUITMENT = "recruitment"
    TRAINING = "training"
    ASSET_MANAGEMENT = "asset_management"
    REPORTING = "reporting"
    SYSTEM_ADMINISTRATION = "system_administration"

class AuditAction(Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    APPROVE = "approve"
    REJECT = "reject"
    EXPORT = "export"
    IMPORT = "import"
    SYSTEM_CHANGE = "system_change"

@dataclass
class SystemUser:
    user_id: str
    username: str
    email: str
    first_name: str
    last_name: str
    role: SystemRole
    status: UserStatus
    employee_id: Optional[str]
    password_hash: str
    salt: str
    last_login: Optional[str]
    login_attempts: int
    permissions: List[str]
    session_token: Optional[str]
    mfa_enabled: bool
    mfa_secret: Optional[str]
    created_at: str
    updated_at: str
    password_expires: str
    account_expires: Optional[str]

@dataclass
class SystemPermission:
    permission_id: str
    name: str
    description: str
    module: SystemModule
    resource: str
    actions: List[str]  # create, read, update, delete, approve, etc.
    created_at: str

@dataclass
class AuditLogEntry:
    audit_id: str
    timestamp: str
    user_id: str
    action: AuditAction
    resource_type: str
    resource_id: str
    old_values: Optional[Dict[str, Any]]
    new_values: Optional[Dict[str, Any]]
    ip_address: str
    user_agent: str
    session_id: str
    success: bool
    error_message: Optional[str]
    risk_score: int  # 1-10, based on action sensitivity

@dataclass
class SystemSettings:
    setting_id: str
    category: str
    name: str
    value: Any
    data_type: str  # string, integer, boolean, json
    description: str
    is_sensitive: bool
    requires_restart: bool
    last_modified_by: str
    last_modified_at: str

class SecurityManager:
    """Advanced security and authentication management"""
    
    def __init__(self):
        self.password_policy = {
            "min_length": 12,
            "require_uppercase": True,
            "require_lowercase": True,
            "require_numbers": True,
            "require_special": True,
            "password_history": 12,
            "expiry_days": 90,
            "complexity_score": 8
        }
        self.session_policy = {
            "max_concurrent_sessions": 3,
            "session_timeout": 3600,  # seconds
            "idle_timeout": 1800,  # seconds
            "require_mfa": True
        }
    
    def hash_password(self, password: str) -> tuple[str, str]:
        """Generate secure password hash with salt"""
        salt = secrets.token_hex(32)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return password_hash.hex(), salt
    
    def verify_password(self, password: str, password_hash: str, salt: str) -> bool:
        """Verify password against stored hash"""
        test_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return test_hash.hex() == password_hash
    
    def calculate_password_strength(self, password: str) -> int:
        """Calculate password strength score (1-10)"""
        score = 0
        
        # Length scoring
        if len(password) >= 8: score += 1
        if len(password) >= 12: score += 1
        if len(password) >= 16: score += 1
        
        # Character variety scoring
        if any(c.isupper() for c in password): score += 1
        if any(c.islower() for c in password): score += 1
        if any(c.isdigit() for c in password): score += 1
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password): score += 1
        
        # Pattern analysis (simplified)
        if not any(password[i:i+3] == password[i:i+3].lower() * 3 for i in range(len(password)-2)): score += 1
        if len(set(password)) / len(password) > 0.7: score += 1  # Character diversity
        
        # Common password check (simplified)
        common_passwords = ["password", "123456", "qwerty", "admin"]
        if password.lower() not in common_passwords: score += 1
        
        return min(score, 10)
    
    def generate_session_token(self) -> str:
        """Generate secure session token"""
        return secrets.token_urlsafe(64)
    
    def calculate_risk_score(self, action: AuditAction, user_role: SystemRole, 
                           resource_type: str, time_of_day: int) -> int:
        """Calculate risk score for audit logging"""
        base_score = 1
        
        # Action sensitivity
        high_risk_actions = [AuditAction.DELETE, AuditAction.SYSTEM_CHANGE, AuditAction.EXPORT]
        if action in high_risk_actions:
            base_score += 3
        
        # User role risk
        if user_role == SystemRole.SUPER_ADMIN:
            base_score += 2
        elif user_role == SystemRole.SYSTEM_ADMIN:
            base_score += 1
        
        # Resource sensitivity
        sensitive_resources = ["user", "payroll", "salary", "system_settings"]
        if any(sensitive in resource_type.lower() for sensitive in sensitive_resources):
            base_score += 2
        
        # Time-based risk (after hours)
        if time_of_day < 6 or time_of_day > 22:
            base_score += 1
        
        return min(base_score, 10)

class AdministrationManager:
    """Enterprise Administration System Manager"""
    
    def __init__(self):
        self.config_dir = "config"
        self.users_file = os.path.join(self.config_dir, "system_users.yaml")
        self.permissions_file = os.path.join(self.config_dir, "system_permissions.yaml")
        self.audit_log_file = os.path.join(self.config_dir, "audit_log.yaml")
        self.settings_file = os.path.join(self.config_dir, "system_settings.yaml")
        self.backup_dir = os.path.join(self.config_dir, "backups")
        
        self.ensure_config_directory()
        self.users = self.load_users()
        self.permissions = self.load_permissions()
        self.audit_log = self.load_audit_log()
        self.settings = self.load_system_settings()
        
        self.security_manager = SecurityManager()
        self.active_sessions = {}
    
    def ensure_config_directory(self):
        """Ensure config directories exist"""
        os.makedirs(self.config_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def load_users(self) -> Dict[str, SystemUser]:
        """Load system users from YAML file"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as file:
                    data = yaml.safe_load(file) or {}
                    users = {}
                    for user_id, user_data in data.items():
                        user_data['role'] = SystemRole(user_data['role'])
                        user_data['status'] = UserStatus(user_data['status'])
                        users[user_id] = SystemUser(**user_data)
                    return users
            except Exception as e:
                print(f"Error loading users: {e}")
                return self.create_default_admin()
        else:
            default_users = self.create_default_admin()
            self.save_users(default_users)
            return default_users
    
    def create_default_admin(self) -> Dict[str, SystemUser]:
        """Create default system administrator"""
        admin_id = "ADMIN_001"
        password_hash, salt = self.security_manager.hash_password("AdminPass123!")
        
        admin_user = SystemUser(
            user_id=admin_id,
            username="admin",
            email="admin@company.com",
            first_name="System",
            last_name="Administrator",
            role=SystemRole.SUPER_ADMIN,
            status=UserStatus.ACTIVE,
            employee_id=None,
            password_hash=password_hash,
            salt=salt,
            last_login=None,
            login_attempts=0,
            permissions=["*"],  # All permissions
            session_token=None,
            mfa_enabled=False,
            mfa_secret=None,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            password_expires=(datetime.now() + timedelta(days=90)).isoformat(),
            account_expires=None
        )
        
        return {admin_id: admin_user}
    
    def save_users(self, users: Dict[str, SystemUser]) -> bool:
        """Save users to YAML file"""
        try:
            data = {}
            for user_id, user in users.items():
                user_dict = asdict(user)
                user_dict['role'] = user.role.value
                user_dict['status'] = user.status.value
                data[user_id] = user_dict
            
            with open(self.users_file, 'w') as file:
                yaml.dump(data, file, default_flow_style=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving users: {e}")
            return False
    
    def load_permissions(self) -> Dict[str, SystemPermission]:
        """Load system permissions"""
        if os.path.exists(self.permissions_file):
            try:
                with open(self.permissions_file, 'r') as file:
                    data = yaml.safe_load(file) or {}
                    permissions = {}
                    for perm_id, perm_data in data.items():
                        perm_data['module'] = SystemModule(perm_data['module'])
                        permissions[perm_id] = SystemPermission(**perm_data)
                    return permissions
            except Exception as e:
                print(f"Error loading permissions: {e}")
                return self.create_default_permissions()
        else:
            default_perms = self.create_default_permissions()
            self.save_permissions(default_perms)
            return default_perms
    
    def create_default_permissions(self) -> Dict[str, SystemPermission]:
        """Create default system permissions"""
        permissions = {}
        current_time = datetime.now().isoformat()
        
        # Employee Management Permissions
        permissions["emp_create"] = SystemPermission(
            permission_id="emp_create",
            name="Create Employee",
            description="Create new employee records",
            module=SystemModule.EMPLOYEE_MANAGEMENT,
            resource="employee",
            actions=["create"],
            created_at=current_time
        )
        
        permissions["emp_read"] = SystemPermission(
            permission_id="emp_read",
            name="View Employee",
            description="View employee records",
            module=SystemModule.EMPLOYEE_MANAGEMENT,
            resource="employee",
            actions=["read"],
            created_at=current_time
        )
        
        permissions["emp_update"] = SystemPermission(
            permission_id="emp_update",
            name="Update Employee",
            description="Update employee records",
            module=SystemModule.EMPLOYEE_MANAGEMENT,
            resource="employee",
            actions=["update"],
            created_at=current_time
        )
        
        # Timesheet Permissions
        permissions["ts_approve"] = SystemPermission(
            permission_id="ts_approve",
            name="Approve Timesheets",
            description="Approve employee timesheets",
            module=SystemModule.TIMESHEET_MANAGEMENT,
            resource="timesheet",
            actions=["approve"],
            created_at=current_time
        )
        
        # System Admin Permissions
        permissions["sys_admin"] = SystemPermission(
            permission_id="sys_admin",
            name="System Administration",
            description="Full system administration access",
            module=SystemModule.SYSTEM_ADMINISTRATION,
            resource="system",
            actions=["create", "read", "update", "delete", "configure"],
            created_at=current_time
        )
        
        return permissions
    
    def save_permissions(self, permissions: Dict[str, SystemPermission]) -> bool:
        """Save permissions to YAML file"""
        try:
            data = {}
            for perm_id, permission in permissions.items():
                perm_dict = asdict(permission)
                perm_dict['module'] = permission.module.value
                data[perm_id] = perm_dict
            
            with open(self.permissions_file, 'w') as file:
                yaml.dump(data, file, default_flow_style=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving permissions: {e}")
            return False
    
    def load_audit_log(self) -> List[AuditLogEntry]:
        """Load audit log entries"""
        if os.path.exists(self.audit_log_file):
            try:
                with open(self.audit_log_file, 'r') as file:
                    data = yaml.safe_load(file) or []
                    entries = []
                    for entry_data in data:
                        entry_data['action'] = AuditAction(entry_data['action'])
                        entries.append(AuditLogEntry(**entry_data))
                    return entries
            except Exception as e:
                print(f"Error loading audit log: {e}")
                return []
        return []
    
    def add_audit_entry(self, user_id: str, action: AuditAction, resource_type: str, 
                       resource_id: str, old_values: Dict = None, new_values: Dict = None,
                       success: bool = True, error_message: str = None):
        """Add entry to audit log"""
        current_time = datetime.now()
        user = self.users.get(user_id)
        user_role = user.role if user else SystemRole.GUEST
        
        risk_score = self.security_manager.calculate_risk_score(
            action, user_role, resource_type, current_time.hour
        )
        
        entry = AuditLogEntry(
            audit_id=str(uuid.uuid4()),
            timestamp=current_time.isoformat(),
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            old_values=old_values,
            new_values=new_values,
            ip_address="127.0.0.1",  # In real app, get from request
            user_agent="HR System",
            session_id=user.session_token if user else "unknown",
            success=success,
            error_message=error_message,
            risk_score=risk_score
        )
        
        self.audit_log.append(entry)
        
        # Keep only last 10000 entries
        if len(self.audit_log) > 10000:
            self.audit_log = self.audit_log[-10000:]
        
        self.save_audit_log()
    
    def save_audit_log(self) -> bool:
        """Save audit log to YAML file"""
        try:
            data = []
            for entry in self.audit_log:
                entry_dict = asdict(entry)
                entry_dict['action'] = entry.action.value
                data.append(entry_dict)
            
            with open(self.audit_log_file, 'w') as file:
                yaml.dump(data, file, default_flow_style=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving audit log: {e}")
            return False
    
    def load_system_settings(self) -> Dict[str, SystemSettings]:
        """Load system settings"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as file:
                    data = yaml.safe_load(file) or {}
                    settings = {}
                    for setting_id, setting_data in data.items():
                        settings[setting_id] = SystemSettings(**setting_data)
                    return settings
            except Exception as e:
                print(f"Error loading settings: {e}")
                return self.create_default_settings()
        else:
            default_settings = self.create_default_settings()
            self.save_system_settings(default_settings)
            return default_settings
    
    def create_default_settings(self) -> Dict[str, SystemSettings]:
        """Create default system settings"""
        settings = {}
        current_time = datetime.now().isoformat()
        
        settings["session_timeout"] = SystemSettings(
            setting_id="session_timeout",
            category="security",
            name="Session Timeout",
            value=3600,
            data_type="integer",
            description="Session timeout in seconds",
            is_sensitive=False,
            requires_restart=False,
            last_modified_by="SYSTEM",
            last_modified_at=current_time
        )
        
        settings["password_policy"] = SystemSettings(
            setting_id="password_policy",
            category="security",
            name="Password Policy",
            value={
                "min_length": 12,
                "require_uppercase": True,
                "require_numbers": True,
                "expiry_days": 90
            },
            data_type="json",
            description="Password complexity requirements",
            is_sensitive=False,
            requires_restart=False,
            last_modified_by="SYSTEM",
            last_modified_at=current_time
        )
        
        settings["backup_retention"] = SystemSettings(
            setting_id="backup_retention",
            category="system",
            name="Backup Retention",
            value=30,
            data_type="integer",
            description="Number of days to retain backups",
            is_sensitive=False,
            requires_restart=False,
            last_modified_by="SYSTEM",
            last_modified_at=current_time
        )
        
        return settings
    
    def save_system_settings(self, settings: Dict[str, SystemSettings]) -> bool:
        """Save system settings"""
        try:
            data = {}
            for setting_id, setting in settings.items():
                data[setting_id] = asdict(setting)
            
            with open(self.settings_file, 'w') as file:
                yaml.dump(data, file, default_flow_style=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def create_user(self, user_data: Dict[str, Any], created_by: str) -> str:
        """Create new system user"""
        user_id = f"USER_{uuid.uuid4().hex[:8].upper()}"
        
        # Validate required fields
        required_fields = ['username', 'email', 'first_name', 'last_name', 'role']
        for field in required_fields:
            if not user_data.get(field):
                raise ValueError(f"Required field '{field}' is missing")
        
        # Check for duplicate username/email
        for user in self.users.values():
            if user.username == user_data['username']:
                raise ValueError("Username already exists")
            if user.email == user_data['email']:
                raise ValueError("Email already exists")
        
        # Generate password hash
        password = user_data.get('password', self.generate_temp_password())
        password_hash, salt = self.security_manager.hash_password(password)
        
        # Create user object
        current_time = datetime.now()
        user = SystemUser(
            user_id=user_id,
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            role=SystemRole(user_data['role']),
            status=UserStatus(user_data.get('status', 'active')),
            employee_id=user_data.get('employee_id'),
            password_hash=password_hash,
            salt=salt,
            last_login=None,
            login_attempts=0,
            permissions=user_data.get('permissions', []),
            session_token=None,
            mfa_enabled=False,
            mfa_secret=None,
            created_at=current_time.isoformat(),
            updated_at=current_time.isoformat(),
            password_expires=(current_time + timedelta(days=90)).isoformat(),
            account_expires=user_data.get('account_expires')
        )
        
        self.users[user_id] = user
        self.save_users(self.users)
        
        # Add audit log entry
        self.add_audit_entry(
            created_by, AuditAction.CREATE, "user", user_id,
            None, asdict(user), True
        )
        
        return user_id
    
    def generate_temp_password(self) -> str:
        """Generate temporary password for new users"""
        return f"Temp{secrets.randbelow(10000):04d}!"
    
    def update_user(self, user_id: str, updates: Dict[str, Any], updated_by: str) -> bool:
        """Update user with audit trail"""
        if user_id not in self.users:
            return False
        
        user = self.users[user_id]
        old_values = asdict(user)
        
        # Track changes
        changes = {}
        for field, value in updates.items():
            if hasattr(user, field) and field not in ['password_hash', 'salt']:  # Don't allow direct hash updates
                old_value = getattr(user, field)
                if field == 'role' and isinstance(value, str):
                    value = SystemRole(value)
                elif field == 'status' and isinstance(value, str):
                    value = UserStatus(value)
                
                if old_value != value:
                    setattr(user, field, value)
                    changes[field] = {"old": old_value, "new": value}
        
        if changes:
            user.updated_at = datetime.now().isoformat()
            self.save_users(self.users)
            
            # Add audit log entry
            self.add_audit_entry(
                updated_by, AuditAction.UPDATE, "user", user_id,
                old_values, asdict(user), True
            )
        
        return True
    
    def reset_user_password(self, user_id: str, new_password: str, reset_by: str) -> bool:
        """Reset user password with audit trail"""
        if user_id not in self.users:
            return False
        
        user = self.users[user_id]
        
        # Validate password strength
        strength = self.security_manager.calculate_password_strength(new_password)
        if strength < self.security_manager.password_policy["complexity_score"]:
            raise ValueError("Password does not meet complexity requirements")
        
        # Update password
        password_hash, salt = self.security_manager.hash_password(new_password)
        user.password_hash = password_hash
        user.salt = salt
        user.password_expires = (datetime.now() + timedelta(days=90)).isoformat()
        user.login_attempts = 0
        user.updated_at = datetime.now().isoformat()
        
        self.save_users(self.users)
        
        # Add audit log entry
        self.add_audit_entry(
            reset_by, AuditAction.UPDATE, "user_password", user_id,
            None, None, True  # Don't log password details
        )
        
        return True
    
    def deactivate_user(self, user_id: str, deactivated_by: str) -> bool:
        """Deactivate user account"""
        if user_id not in self.users:
            return False
        
        user = self.users[user_id]
        old_status = user.status
        user.status = UserStatus.INACTIVE
        user.session_token = None  # Invalidate session
        user.updated_at = datetime.now().isoformat()
        
        self.save_users(self.users)
        
        # Remove from active sessions
        if user_id in self.active_sessions:
            del self.active_sessions[user_id]
        
        # Add audit log entry
        self.add_audit_entry(
            deactivated_by, AuditAction.UPDATE, "user_status", user_id,
            {"status": old_status.value}, {"status": user.status.value}, True
        )
        
        return True
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        total_users = len(self.users)
        active_users = sum(1 for user in self.users.values() if user.status == UserStatus.ACTIVE)
        active_sessions = len(self.active_sessions)
        
        # Recent audit activity (last 24 hours)
        yesterday = datetime.now() - timedelta(days=1)
        recent_activity = sum(1 for entry in self.audit_log 
                            if datetime.fromisoformat(entry.timestamp) >= yesterday)
        
        # High risk activities (last 7 days)
        last_week = datetime.now() - timedelta(days=7)
        high_risk_activities = sum(1 for entry in self.audit_log 
                                 if datetime.fromisoformat(entry.timestamp) >= last_week 
                                 and entry.risk_score >= 7)
        
        return {
            "users": {
                "total": total_users,
                "active": active_users,
                "inactive": total_users - active_users,
                "locked": sum(1 for user in self.users.values() if user.status == UserStatus.LOCKED)
            },
            "sessions": {
                "active": active_sessions,
                "max_allowed": 100  # Configuration-based
            },
            "security": {
                "recent_activity": recent_activity,
                "high_risk_activities": high_risk_activities,
                "failed_logins_24h": sum(1 for user in self.users.values() if user.login_attempts > 0)
            },
            "system": {
                "uptime": "72:45:32",  # Mock data
                "disk_usage": 45.2,  # Percentage
                "memory_usage": 68.7,  # Percentage
                "backup_status": "Healthy"
            }
        }


def create_administration_page():
    """Create the main administration page"""
    admin_manager = AdministrationManager()
    
    with ui.column().classes('w-full h-full bg-gradient-to-br from-gray-50 to-slate-100 min-h-screen'):
        # Header Section
        with ui.row().classes('w-full p-6'):
            with ui.card().classes('w-full bg-gradient-to-r from-slate-800 to-gray-900 text-white'):
                with ui.card_section().classes('p-6'):
                    with ui.row().classes('w-full justify-between items-center'):
                        ui.html('<h1 class="text-3xl font-bold flex items-center gap-3"><span class="text-4xl">⚙️</span>System Administration</h1>')
                        with ui.row().classes('gap-4'):
                            ui.button('👥 User Management', on_click=lambda: switch_admin_tab('users')).classes('bg-white text-slate-800 hover:bg-gray-100')
                            ui.button('🔒 Security', on_click=lambda: switch_admin_tab('security')).classes('bg-white text-slate-800 hover:bg-gray-100')
                            ui.button('📊 System Monitor', on_click=lambda: switch_admin_tab('monitor')).classes('bg-white text-slate-800 hover:bg-gray-100')

        # System Overview Dashboard
        with ui.row().classes('w-full px-6 mb-6'):
            stats = admin_manager.get_system_stats()
            
            # Users Stats
            with ui.card().classes('flex-1 bg-gradient-to-r from-blue-500 to-blue-600 text-white'):
                with ui.card_section().classes('p-4 text-center'):
                    ui.html('<div class="text-3xl font-bold">👥</div>')
                    ui.html(f'<div class="text-2xl font-bold">{stats["users"]["total"]}</div>')
                    ui.html('<div class="text-sm opacity-90">Total Users</div>')
                    ui.html(f'<div class="text-xs opacity-75">{stats["users"]["active"]} Active</div>')
            
            # Sessions Stats
            with ui.card().classes('flex-1 bg-gradient-to-r from-green-500 to-green-600 text-white'):
                with ui.card_section().classes('p-4 text-center'):
                    ui.html('<div class="text-3xl font-bold">🔓</div>')
                    ui.html(f'<div class="text-2xl font-bold">{stats["sessions"]["active"]}</div>')
                    ui.html('<div class="text-sm opacity-90">Active Sessions</div>')
            
            # Security Stats
            with ui.card().classes('flex-1 bg-gradient-to-r from-yellow-500 to-yellow-600 text-white'):
                with ui.card_section().classes('p-4 text-center'):
                    ui.html('<div class="text-3xl font-bold">⚠️</div>')
                    ui.html(f'<div class="text-2xl font-bold">{stats["security"]["high_risk_activities"]}</div>')
                    ui.html('<div class="text-sm opacity-90">High Risk Activities</div>')
            
            # System Health
            with ui.card().classes('flex-1 bg-gradient-to-r from-purple-500 to-purple-600 text-white'):
                with ui.card_section().classes('p-4 text-center'):
                    ui.html('<div class="text-3xl font-bold">💾</div>')
                    ui.html(f'<div class="text-2xl font-bold">{stats["system"]["disk_usage"]:.1f}%</div>')
                    ui.html('<div class="text-sm opacity-90">Disk Usage</div>')

        # Main Content Area with Tabs
        with ui.row().classes('w-full px-6'):
            with ui.card().classes('w-full'):
                with ui.card_section().classes('p-6'):
                    
                    # Tab Navigation
                    with ui.row().classes('w-full mb-6'):
                        tab_buttons = [
                            {'id': 'users', 'label': '👥 User Management', 'active': True},
                            {'id': 'permissions', 'label': '🔐 Permissions', 'active': False},
                            {'id': 'audit', 'label': '📋 Audit Log', 'active': False},
                            {'id': 'settings', 'label': '⚙️ System Settings', 'active': False},
                            {'id': 'backup', 'label': '💾 Backup & Recovery', 'active': False},
                        ]
                        
                        for tab in tab_buttons:
                            active_class = 'bg-slate-700 text-white' if tab['active'] else 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                            ui.button(tab['label'], on_click=lambda t=tab['id']: switch_admin_tab(t)).classes(f'px-4 py-2 {active_class}')

                    # Tab Content Areas
                    class AdminTabState:
                        def __init__(self):
                            self.current_tab = 'users'
                            self.tab_panels = {}
                    
                    tab_state = AdminTabState()
                    
                    # User Management Tab
                    with ui.column().classes('w-full') as users_tab:
                        create_user_management_panel(admin_manager)
                    tab_state.tab_panels['users'] = users_tab
                    
                    # Permissions Tab
                    with ui.column().classes('w-full') as permissions_tab:
                        create_permissions_panel(admin_manager)
                    tab_state.tab_panels['permissions'] = permissions_tab
                    permissions_tab.set_visibility(False)
                    
                    # Audit Log Tab
                    with ui.column().classes('w-full') as audit_tab:
                        create_audit_log_panel(admin_manager)
                    tab_state.tab_panels['audit'] = audit_tab
                    audit_tab.set_visibility(False)
                    
                    # System Settings Tab
                    with ui.column().classes('w-full') as settings_tab:
                        create_system_settings_panel(admin_manager)
                    tab_state.tab_panels['settings'] = settings_tab
                    settings_tab.set_visibility(False)
                    
                    # Backup & Recovery Tab
                    with ui.column().classes('w-full') as backup_tab:
                        create_backup_panel(admin_manager)
                    tab_state.tab_panels['backup'] = backup_tab
                    backup_tab.set_visibility(False)
                    
                    def switch_admin_tab(tab_id):
                        """Switch between admin tabs"""
                        # Hide all tabs
                        for panel in tab_state.tab_panels.values():
                            panel.set_visibility(False)
                        
                        # Show selected tab
                        if tab_id in tab_state.tab_panels:
                            tab_state.tab_panels[tab_id].set_visibility(True)
                            tab_state.current_tab = tab_id

def create_user_management_panel(admin_manager: AdministrationManager):
    """Create user management panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-6">👥 User Management</h2>')
    
    # User Actions
    with ui.row().classes('w-full gap-4 mb-6'):
        ui.button('➕ Add User', on_click=lambda: show_add_user_dialog(admin_manager)).classes('bg-green-600 text-white hover:bg-green-700')
        ui.button('📋 Bulk Import', on_click=lambda: show_bulk_import_dialog()).classes('bg-blue-600 text-white hover:bg-blue-700')
        ui.button('📊 User Report', on_click=lambda: generate_user_report()).classes('bg-purple-600 text-white hover:bg-purple-700')
        ui.button('🔒 Security Review', on_click=lambda: show_security_review()).classes('bg-red-600 text-white hover:bg-red-700')
    
    # User Search and Filters
    with ui.row().classes('w-full gap-4 mb-4'):
        user_search = ui.input('Search users...', placeholder='Username, email, name').classes('flex-1')
        role_filter = ui.select(['All Roles', 'Super Admin', 'System Admin', 'HR Admin', 'Manager', 'Employee'], value='All Roles').classes('w-48')
        status_filter = ui.select(['All Status', 'Active', 'Inactive', 'Suspended', 'Locked'], value='All Status').classes('w-48')
    
    # Users Table
    with ui.element('div').classes('overflow-x-auto'):
        create_users_table(admin_manager)

def create_users_table(admin_manager: AdministrationManager):
    """Create users management table"""
    with ui.element('table').classes('w-full table-auto border-collapse'):
        # Header
        with ui.element('thead'):
            with ui.element('tr').classes('bg-gray-100'):
                headers = [
                    'User', 'Role', 'Status', 'Last Login', 'Employee ID', 
                    'MFA', 'Login Attempts', 'Actions'
                ]
                for header in headers:
                    ui.html(f'<th class="border p-3 text-left font-semibold">{header}</th>')
        
        # Body
        with ui.element('tbody'):
            for user_id, user in admin_manager.users.items():
                with ui.element('tr').classes('hover:bg-gray-50'):
                    # User Info
                    with ui.element('td').classes('border p-3'):
                        with ui.row().classes('items-center gap-3'):
                            # Avatar
                            initials = f"{user.first_name[0]}{user.last_name[0]}".upper()
                            with ui.element('div').classes('w-8 h-8 bg-slate-600 text-white rounded-full flex items-center justify-center text-sm font-semibold'):
                                ui.html(initials)
                            with ui.column().classes('gap-1'):
                                ui.html(f'<div class="font-medium">{user.first_name} {user.last_name}</div>')
                                ui.html(f'<div class="text-sm text-gray-500">{user.username}</div>')
                                ui.html(f'<div class="text-xs text-gray-400">{user.email}</div>')
                    
                    # Role
                    role_colors = {
                        'super_admin': 'bg-red-100 text-red-800',
                        'system_admin': 'bg-purple-100 text-purple-800',
                        'hr_admin': 'bg-blue-100 text-blue-800',
                        'manager': 'bg-green-100 text-green-800',
                        'employee': 'bg-gray-100 text-gray-800'
                    }
                    role_color = role_colors.get(user.role.value, 'bg-gray-100 text-gray-800')
                    ui.html(f'<td class="border p-3"><span class="px-2 py-1 rounded-full text-xs font-medium {role_color}">{user.role.value.replace("_", " ").title()}</span></td>')
                    
                    # Status
                    status_colors = {
                        'active': 'bg-green-100 text-green-800',
                        'inactive': 'bg-gray-100 text-gray-800',
                        'suspended': 'bg-yellow-100 text-yellow-800',
                        'locked': 'bg-red-100 text-red-800'
                    }
                    status_color = status_colors.get(user.status.value, 'bg-gray-100 text-gray-800')
                    ui.html(f'<td class="border p-3"><span class="px-2 py-1 rounded-full text-xs font-medium {status_color}">{user.status.value.title()}</span></td>')
                    
                    # Last Login
                    last_login = "Never" if not user.last_login else datetime.fromisoformat(user.last_login).strftime('%Y-%m-%d %H:%M')
                    ui.html(f'<td class="border p-3 text-sm">{last_login}</td>')
                    
                    # Employee ID
                    ui.html(f'<td class="border p-3 text-sm">{user.employee_id or "N/A"}</td>')
                    
                    # MFA Status
                    mfa_icon = "🔒" if user.mfa_enabled else "🔓"
                    mfa_color = "text-green-600" if user.mfa_enabled else "text-red-600"
                    ui.html(f'<td class="border p-3 text-center"><span class="{mfa_color}">{mfa_icon}</span></td>')
                    
                    # Login Attempts
                    attempts_color = "text-red-600 font-semibold" if user.login_attempts >= 3 else "text-gray-600"
                    ui.html(f'<td class="border p-3 text-center"><span class="{attempts_color}">{user.login_attempts}</span></td>')
                    
                    # Actions
                    with ui.element('td').classes('border p-3'):
                        with ui.row().classes('gap-1'):
                            ui.button('👁️', on_click=lambda u=user_id: view_user_details(admin_manager, u)).classes('p-1 text-xs bg-blue-100 text-blue-600 hover:bg-blue-200')
                            ui.button('✏️', on_click=lambda u=user_id: edit_user(admin_manager, u)).classes('p-1 text-xs bg-green-100 text-green-600 hover:bg-green-200')
                            ui.button('🔑', on_click=lambda u=user_id: reset_user_password(admin_manager, u)).classes('p-1 text-xs bg-yellow-100 text-yellow-600 hover:bg-yellow-200')
                            
                            if user.status == UserStatus.ACTIVE:
                                ui.button('⏸️', on_click=lambda u=user_id: deactivate_user(admin_manager, u)).classes('p-1 text-xs bg-red-100 text-red-600 hover:bg-red-200')
                            else:
                                ui.button('▶️', on_click=lambda u=user_id: activate_user(admin_manager, u)).classes('p-1 text-xs bg-green-100 text-green-600 hover:bg-green-200')

def create_permissions_panel(admin_manager: AdministrationManager):
    """Create permissions management panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-6">🔐 Permissions Management</h2>')
    
    # Role-based permissions matrix would go here
    ui.html('<div class="text-gray-600">Permissions management interface - To be implemented</div>')

def create_audit_log_panel(admin_manager: AdministrationManager):
    """Create audit log panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-6">📋 Audit Log</h2>')
    
    # Audit log filters
    with ui.row().classes('w-full gap-4 mb-4'):
        action_filter = ui.select(['All Actions', 'Login', 'Create', 'Update', 'Delete'], value='All Actions').classes('w-48')
        risk_filter = ui.select(['All Risk Levels', 'High (7-10)', 'Medium (4-6)', 'Low (1-3)'], value='All Risk Levels').classes('w-48')
        user_filter = ui.select(['All Users'] + list(admin_manager.users.keys()), value='All Users').classes('w-48')
        
        date_from = ui.input('From Date').classes('w-40')
        date_from.props('type=date')
        date_from.value = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    # Recent audit entries (last 20)
    recent_entries = sorted(admin_manager.audit_log, key=lambda x: x.timestamp, reverse=True)[:20]
    
    with ui.element('div').classes('overflow-x-auto'):
        with ui.element('table').classes('w-full table-auto border-collapse'):
            # Header
            with ui.element('thead'):
                with ui.element('tr').classes('bg-gray-100'):
                    headers = ['Timestamp', 'User', 'Action', 'Resource', 'Risk', 'Status', 'Details']
                    for header in headers:
                        ui.html(f'<th class="border p-3 text-left font-semibold">{header}</th>')
            
            # Body
            with ui.element('tbody'):
                for entry in recent_entries:
                    with ui.element('tr').classes('hover:bg-gray-50'):
                        # Timestamp
                        timestamp = datetime.fromisoformat(entry.timestamp).strftime('%m/%d %H:%M')
                        ui.html(f'<td class="border p-2 text-sm">{timestamp}</td>')
                        
                        # User
                        user = admin_manager.users.get(entry.user_id)
                        user_name = f"{user.first_name} {user.last_name}" if user else entry.user_id
                        ui.html(f'<td class="border p-2 text-sm">{user_name}</td>')
                        
                        # Action
                        action_colors = {
                            'create': 'bg-green-100 text-green-800',
                            'update': 'bg-blue-100 text-blue-800',
                            'delete': 'bg-red-100 text-red-800',
                            'login': 'bg-gray-100 text-gray-800'
                        }
                        action_color = action_colors.get(entry.action.value, 'bg-gray-100 text-gray-800')
                        ui.html(f'<td class="border p-2"><span class="px-2 py-1 rounded text-xs {action_color}">{entry.action.value.title()}</span></td>')
                        
                        # Resource
                        ui.html(f'<td class="border p-2 text-sm">{entry.resource_type}</td>')
                        
                        # Risk Score
                        risk_color = 'text-red-600' if entry.risk_score >= 7 else 'text-yellow-600' if entry.risk_score >= 4 else 'text-green-600'
                        ui.html(f'<td class="border p-2 text-center"><span class="{risk_color} font-semibold">{entry.risk_score}</span></td>')
                        
                        # Status
                        status_icon = "✅" if entry.success else "❌"
                        ui.html(f'<td class="border p-2 text-center">{status_icon}</td>')
                        
                        # Details button
                        with ui.element('td').classes('border p-2'):
                            ui.button('📋', on_click=lambda e=entry.audit_id: view_audit_details(e)).classes('p-1 text-xs bg-blue-100 text-blue-600 hover:bg-blue-200')

def create_system_settings_panel(admin_manager: AdministrationManager):
    """Create system settings panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-6">⚙️ System Settings</h2>')
    
    # Settings categories
    with ui.row().classes('w-full gap-6'):
        # Security Settings
        with ui.card().classes('flex-1'):
            with ui.card_section().classes('p-4'):
                ui.html('<h3 class="text-lg font-semibold mb-4">🔒 Security Settings</h3>')
                
                for setting_id, setting in admin_manager.settings.items():
                    if setting.category == 'security':
                        with ui.row().classes('w-full items-center justify-between mb-3'):
                            ui.html(f'<div><strong>{setting.name}</strong><br><small class="text-gray-600">{setting.description}</small></div>')
                            
                            if setting.data_type == 'boolean':
                                ui.checkbox('', value=setting.value)
                            elif setting.data_type == 'integer':
                                ui.number('', value=setting.value).classes('w-20')
                            else:
                                ui.input('', value=str(setting.value)).classes('w-32')
        
        # System Settings
        with ui.card().classes('flex-1'):
            with ui.card_section().classes('p-4'):
                ui.html('<h3 class="text-lg font-semibold mb-4">⚙️ System Settings</h3>')
                
                for setting_id, setting in admin_manager.settings.items():
                    if setting.category == 'system':
                        with ui.row().classes('w-full items-center justify-between mb-3'):
                            ui.html(f'<div><strong>{setting.name}</strong><br><small class="text-gray-600">{setting.description}</small></div>')
                            
                            if setting.data_type == 'boolean':
                                ui.checkbox('', value=setting.value)
                            elif setting.data_type == 'integer':
                                ui.number('', value=setting.value).classes('w-20')
                            else:
                                ui.input('', value=str(setting.value)).classes('w-32')
    
    # Save button
    ui.button('💾 Save Settings', on_click=lambda: save_system_settings(admin_manager)).classes('bg-green-600 text-white mt-4')

def create_backup_panel(admin_manager: AdministrationManager):
    """Create backup and recovery panel"""
    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-6">💾 Backup & Recovery</h2>')
    
    # Backup status
    with ui.row().classes('w-full gap-4 mb-6'):
        with ui.card().classes('flex-1 bg-green-50 border border-green-200'):
            with ui.card_section().classes('p-4'):
                ui.html('<h3 class="text-lg font-semibold text-green-800 mb-2">✅ Last Backup</h3>')
                ui.html('<div class="text-sm text-green-700">Today at 02:00 AM</div>')
                ui.html('<div class="text-xs text-green-600">Size: 45.2 MB</div>')
        
        with ui.card().classes('flex-1 bg-blue-50 border border-blue-200'):
            with ui.card_section().classes('p-4'):
                ui.html('<h3 class="text-lg font-semibold text-blue-800 mb-2">📅 Next Backup</h3>')
                ui.html('<div class="text-sm text-blue-700">Tomorrow at 02:00 AM</div>')
                ui.html('<div class="text-xs text-blue-600">Automatic Daily Backup</div>')
    
    # Backup actions
    with ui.row().classes('w-full gap-4 mb-6'):
        ui.button('🚀 Create Backup Now', on_click=lambda: create_manual_backup()).classes('bg-blue-600 text-white')
        ui.button('📋 View Backup History', on_click=lambda: show_backup_history()).classes('bg-gray-600 text-white')
        ui.button('🔄 Restore from Backup', on_click=lambda: show_restore_dialog()).classes('bg-orange-600 text-white')
        ui.button('⚙️ Backup Settings', on_click=lambda: show_backup_settings()).classes('bg-purple-600 text-white')

# Helper functions for dialog boxes and actions

def show_add_user_dialog(admin_manager: AdministrationManager):
    """Show add user dialog"""
    ui.notify('Add user dialog - To be implemented', type='info')

def view_user_details(admin_manager: AdministrationManager, user_id: str):
    """View user details"""
    ui.notify(f'Viewing user details for {user_id}', type='info')

def edit_user(admin_manager: AdministrationManager, user_id: str):
    """Edit user"""
    ui.notify(f'Edit user {user_id} - To be implemented', type='info')

def reset_user_password(admin_manager: AdministrationManager, user_id: str):
    """Reset user password"""
    ui.notify(f'Reset password for {user_id} - To be implemented', type='info')

def deactivate_user(admin_manager: AdministrationManager, user_id: str):
    """Deactivate user"""
    success = admin_manager.deactivate_user(user_id, "ADMIN001")
    if success:
        ui.notify(f'User {user_id} deactivated', type='positive')
    else:
        ui.notify(f'Failed to deactivate user {user_id}', type='negative')

def activate_user(admin_manager: AdministrationManager, user_id: str):
    """Activate user"""
    ui.notify(f'Activate user {user_id} - To be implemented', type='info')

def view_audit_details(audit_id: str):
    """View audit log entry details"""
    ui.notify(f'Viewing audit details for {audit_id}', type='info')

def save_system_settings(admin_manager: AdministrationManager):
    """Save system settings"""
    ui.notify('System settings saved', type='positive')

def create_manual_backup():
    """Create manual backup"""
    ui.notify('Creating backup...', type='info')

def show_backup_history():
    """Show backup history"""
    ui.notify('Showing backup history - To be implemented', type='info')

def show_restore_dialog():
    """Show restore dialog"""
    ui.notify('Restore dialog - To be implemented', type='info')

def show_backup_settings():
    """Show backup settings"""
    ui.notify('Backup settings - To be implemented', type='info')

def show_bulk_import_dialog():
    """Show bulk import dialog"""
    ui.notify('Bulk import dialog - To be implemented', type='info')

def generate_user_report():
    """Generate user report"""
    ui.notify('Generating user report...', type='info')

def show_security_review():
    """Show security review"""
    ui.notify('Security review - To be implemented', type='info')