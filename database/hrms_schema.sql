-- HRMS OrientDB Schema
-- This file contains OrientDB class definitions, indexes, and constraints
-- for the Human Resource Management System

-- ===========================================
-- ORIENTDB SCHEMA FOR HRMS
-- ===========================================

-- Enable strict mode for schema validation
ALTER DATABASE CUSTOM useLightweightEdges=false;
ALTER DATABASE CUSTOM useClassForEdgeLabel=false;
ALTER DATABASE CUSTOM useClassForVertexLabel=false;

-- ===========================================
-- VERTEX CLASSES (Entities)
-- ===========================================

-- User class for authentication and basic user info
CREATE CLASS User EXTENDS V;
CREATE PROPERTY User.email STRING;
CREATE PROPERTY User.password_hash STRING;
CREATE PROPERTY User.role STRING; -- 'admin', 'manager', 'employee'
CREATE PROPERTY User.is_active BOOLEAN DEFAULT true;
CREATE PROPERTY User.created_at DATETIME;
CREATE PROPERTY User.updated_at DATETIME;
CREATE PROPERTY User.last_login DATETIME;

-- Create unique index on email
CREATE INDEX User.email UNIQUE;

-- Employee class extending User with HR-specific data
CREATE CLASS Employee EXTENDS User;
CREATE PROPERTY Employee.employee_id STRING;
CREATE PROPERTY Employee.first_name STRING;
CREATE PROPERTY Employee.last_name STRING;
CREATE PROPERTY Employee.date_of_birth DATE;
CREATE PROPERTY Employee.gender STRING;
CREATE PROPERTY Employee.phone STRING;
CREATE PROPERTY Employee.address EMBEDDED OAddress;
CREATE PROPERTY Employee.hire_date DATE;
CREATE PROPERTY Employee.salary DECIMAL;
CREATE PROPERTY Employee.position STRING;
CREATE PROPERTY Employee.manager_id LINK Employee;
CREATE PROPERTY Employee.emergency_contact EMBEDDED OContact;
CREATE PROPERTY Employee.skills EMBEDDEDLIST STRING;
CREATE PROPERTY Employee.certifications EMBEDDEDLIST OCertification;

-- Create unique index on employee_id
CREATE INDEX Employee.employee_id UNIQUE;

-- Department class
CREATE CLASS Department EXTENDS V;
CREATE PROPERTY Department.name STRING;
CREATE PROPERTY Department.description STRING;
CREATE PROPERTY Department.manager_id LINK Employee;
CREATE PROPERTY Department.budget DECIMAL;
CREATE PROPERTY Department.location STRING;
CREATE PROPERTY Department.is_active BOOLEAN DEFAULT true;
CREATE PROPERTY Department.created_at DATETIME;

-- Create unique index on department name
CREATE INDEX Department.name UNIQUE;

-- Position class
CREATE CLASS Position EXTENDS V;
CREATE PROPERTY Position.title STRING;
CREATE PROPERTY Position.description STRING;
CREATE PROPERTY Position.level STRING;
CREATE PROPERTY Position.salary_range EMBEDDED ORange;
CREATE PROPERTY Position.department_id LINK Department;
CREATE PROPERTY Position.is_active BOOLEAN DEFAULT true;

-- Shift Template class
CREATE CLASS ShiftTemplate EXTENDS V;
CREATE PROPERTY ShiftTemplate.name STRING;
CREATE PROPERTY ShiftTemplate.description STRING;
CREATE PROPERTY ShiftTemplate.start_time STRING; -- HH:MM format
CREATE PROPERTY ShiftTemplate.end_time STRING; -- HH:MM format
CREATE PROPERTY ShiftTemplate.duration_hours DECIMAL;
CREATE PROPERTY ShiftTemplate.break_duration INTEGER; -- minutes
CREATE PROPERTY ShiftTemplate.is_active BOOLEAN DEFAULT true;
CREATE PROPERTY ShiftTemplate.created_at DATETIME;

-- Schedule class for shift assignments
CREATE CLASS Schedule EXTENDS V;
CREATE PROPERTY Schedule.employee_id LINK Employee;
CREATE PROPERTY Schedule.shift_template_id LINK ShiftTemplate;
CREATE PROPERTY Schedule.date DATE;
CREATE PROPERTY Schedule.status STRING DEFAULT 'scheduled'; -- 'scheduled', 'completed', 'cancelled'
CREATE PROPERTY Schedule.notes STRING;

-- Create composite index for efficient queries
CREATE INDEX Schedule.employee_date ON Schedule (employee_id, date) UNIQUE;

-- Attendance Record class
CREATE CLASS AttendanceRecord EXTENDS V;
CREATE PROPERTY AttendanceRecord.employee_id LINK Employee;
CREATE PROPERTY AttendanceRecord.date DATE;
CREATE PROPERTY AttendanceRecord.clock_in_time DATETIME;
CREATE PROPERTY AttendanceRecord.clock_out_time DATETIME;
CREATE PROPERTY AttendanceRecord.break_start_time DATETIME;
CREATE PROPERTY AttendanceRecord.break_end_time DATETIME;
CREATE PROPERTY AttendanceRecord.hours_worked DECIMAL;
CREATE PROPERTY AttendanceRecord.status STRING DEFAULT 'present'; -- 'present', 'absent', 'late', 'half-day'
CREATE PROPERTY AttendanceRecord.location STRING;
CREATE PROPERTY AttendanceRecord.notes STRING;

-- Create composite index for attendance queries
CREATE INDEX AttendanceRecord.employee_date ON AttendanceRecord (employee_id, date) UNIQUE;

-- Leave Type class
CREATE CLASS LeaveType EXTENDS V;
CREATE PROPERTY LeaveType.name STRING;
CREATE PROPERTY LeaveType.description STRING;
CREATE PROPERTY LeaveType.days_per_year INTEGER;
CREATE PROPERTY LeaveType.is_paid BOOLEAN DEFAULT true;
CREATE PROPERTY LeaveType.requires_approval BOOLEAN DEFAULT true;
CREATE PROPERTY LeaveType.is_active BOOLEAN DEFAULT true;

-- Leave Request class
CREATE CLASS LeaveRequest EXTENDS V;
CREATE PROPERTY LeaveRequest.employee_id LINK Employee;
CREATE PROPERTY LeaveRequest.leave_type_id LINK LeaveType;
CREATE PROPERTY LeaveRequest.start_date DATE;
CREATE PROPERTY LeaveRequest.end_date DATE;
CREATE PROPERTY LeaveRequest.days_requested DECIMAL;
CREATE PROPERTY LeaveRequest.reason STRING;
CREATE PROPERTY LeaveRequest.status STRING DEFAULT 'pending'; -- 'pending', 'approved', 'rejected', 'cancelled'
CREATE PROPERTY LeaveRequest.approved_by LINK Employee;
CREATE PROPERTY LeaveRequest.approved_at DATETIME;
CREATE PROPERTY LeaveRequest.created_at DATETIME;
CREATE PROPERTY LeaveRequest.comments STRING;

-- Leave Balance class
CREATE CLASS LeaveBalance EXTENDS V;
CREATE PROPERTY LeaveBalance.employee_id LINK Employee;
CREATE PROPERTY LeaveBalance.leave_type_id LINK LeaveType;
CREATE PROPERTY LeaveBalance.year INTEGER;
CREATE PROPERTY LeaveBalance.balance_days DECIMAL;
CREATE PROPERTY LeaveBalance.used_days DECIMAL DEFAULT 0;
CREATE PROPERTY LeaveBalance.carried_forward DECIMAL DEFAULT 0;

-- Create composite index for leave balance queries
CREATE INDEX LeaveBalance.employee_year ON LeaveBalance (employee_id, year);

-- ===========================================
-- EDGE CLASSES (Relationships)
-- ===========================================

-- WorksIn edge: Employee works in Department
CREATE CLASS WorksIn EXTENDS E;
CREATE PROPERTY WorksIn.start_date DATE;
CREATE PROPERTY WorksIn.end_date DATE;
CREATE PROPERTY WorksIn.is_primary BOOLEAN DEFAULT true;

-- ReportsTo edge: Employee reports to Manager
CREATE CLASS ReportsTo EXTENDS E;
CREATE PROPERTY ReportsTo.relationship_type STRING DEFAULT 'direct'; -- 'direct', 'dotted'
CREATE PROPERTY ReportsTo.start_date DATE;
CREATE PROPERTY ReportsTo.end_date DATE;

-- AssignedTo edge: Employee assigned to Position
CREATE CLASS AssignedTo EXTENDS E;
CREATE PROPERTY AssignedTo.start_date DATE;
CREATE PROPERTY AssignedTo.end_date DATE;
CREATE PROPERTY AssignedTo.is_current BOOLEAN DEFAULT true;

-- Manages edge: Manager manages Department
CREATE CLASS Manages EXTENDS E;
CREATE PROPERTY Manages.start_date DATE;
CREATE PROPERTY Manages.end_date DATE;
CREATE PROPERTY Manages.responsibilities EMBEDDEDLIST STRING;

-- ===========================================
-- EMBEDDED CLASSES (Complex Data Types)
-- ===========================================

-- Address embedded class
CREATE CLASS OAddress;
CREATE PROPERTY OAddress.street STRING;
CREATE PROPERTY OAddress.city STRING;
CREATE PROPERTY OAddress.state STRING;
CREATE PROPERTY OAddress.zip_code STRING;
CREATE PROPERTY OAddress.country STRING DEFAULT 'USA';

-- Contact embedded class
CREATE CLASS OContact;
CREATE PROPERTY OContact.name STRING;
CREATE PROPERTY OContact.relationship STRING;
CREATE PROPERTY OContact.phone STRING;
CREATE PROPERTY OContact.email STRING;

-- Certification embedded class
CREATE CLASS OCertification;
CREATE PROPERTY OCertification.name STRING;
CREATE PROPERTY OCertification.issuing_authority STRING;
CREATE PROPERTY OCertification.issue_date DATE;
CREATE PROPERTY OCertification.expiry_date DATE;
CREATE PROPERTY OCertification.certification_number STRING;

-- Salary Range embedded class
CREATE CLASS ORange;
CREATE PROPERTY ORange.min DECIMAL;
CREATE PROPERTY ORange.max DECIMAL;
CREATE PROPERTY ORange.currency STRING DEFAULT 'USD';

-- ===========================================
-- AUDIT AND LOGGING CLASSES
-- ===========================================

-- Audit Log class for tracking changes
CREATE CLASS AuditLog EXTENDS V;
CREATE PROPERTY AuditLog.entity_type STRING; -- 'User', 'Employee', 'Department', etc.
CREATE PROPERTY AuditLog.entity_id STRING; -- RID or external ID
CREATE PROPERTY AuditLog.action STRING; -- 'CREATE', 'UPDATE', 'DELETE'
CREATE PROPERTY AuditLog.user_id LINK User; -- Who performed the action
CREATE PROPERTY AuditLog.timestamp DATETIME;
CREATE PROPERTY AuditLog.old_values STRING; -- JSON string of old values
CREATE PROPERTY AuditLog.new_values STRING; -- JSON string of new values
CREATE PROPERTY AuditLog.ip_address STRING;
CREATE PROPERTY AuditLog.user_agent STRING;

-- Create index for audit queries
CREATE INDEX AuditLog.entity_timestamp ON AuditLog (entity_type, timestamp);

-- ===========================================
-- SYSTEM AND CONFIGURATION CLASSES
-- ===========================================

-- Institution class for organization info
CREATE CLASS Institution EXTENDS V;
CREATE PROPERTY Institution.name STRING;
CREATE PROPERTY Institution.description STRING;
CREATE PROPERTY Institution.address EMBEDDED OAddress;
CREATE PROPERTY Institution.phone STRING;
CREATE PROPERTY Institution.email STRING;
CREATE PROPERTY Institution.website STRING;
CREATE PROPERTY Institution.tax_id STRING;
CREATE PROPERTY Institution.founded_date DATE;

-- System Settings class
CREATE CLASS SystemSetting EXTENDS V;
CREATE PROPERTY SystemSetting.key STRING;
CREATE PROPERTY SystemSetting.value STRING;
CREATE PROPERTY SystemSetting.category STRING;
CREATE PROPERTY SystemSetting.description STRING;
CREATE PROPERTY SystemSetting.updated_at DATETIME;
CREATE PROPERTY SystemSetting.updated_by LINK User;

-- Create unique index on setting key
CREATE INDEX SystemSetting.key UNIQUE;

-- ===========================================
-- INDEXES FOR PERFORMANCE
-- ===========================================

-- Additional indexes for common queries
CREATE INDEX User.role_active ON User (role, is_active);
CREATE INDEX Employee.hire_date ON Employee (hire_date);
CREATE INDEX Employee.last_name ON Employee (last_name);
CREATE INDEX Department.manager_id ON Department (manager_id);
CREATE INDEX Position.department_id ON Position (department_id);
CREATE INDEX ShiftTemplate.is_active ON ShiftTemplate (is_active);
CREATE INDEX LeaveRequest.status ON LeaveRequest (status);
CREATE INDEX LeaveRequest.employee_status ON LeaveRequest (employee_id, status);
CREATE INDEX AttendanceRecord.status_date ON AttendanceRecord (status, date);

-- ===========================================
-- CONSTRAINTS AND VALIDATION
-- ===========================================

-- Add mandatory constraints
ALTER PROPERTY User.email MANDATORY true;
ALTER PROPERTY User.password_hash MANDATORY true;
ALTER PROPERTY User.role MANDATORY true;
ALTER PROPERTY Employee.employee_id MANDATORY true;
ALTER PROPERTY Employee.first_name MANDATORY true;
ALTER PROPERTY Employee.last_name MANDATORY true;
ALTER PROPERTY Department.name MANDATORY true;
ALTER PROPERTY Position.title MANDATORY true;
ALTER PROPERTY ShiftTemplate.name MANDATORY true;
ALTER PROPERTY Schedule.date MANDATORY true;
ALTER PROPERTY AttendanceRecord.date MANDATORY true;
ALTER PROPERTY LeaveType.name MANDATORY true;

-- ===========================================
-- INITIAL DATA SEEDING
-- ===========================================

-- Insert default institution
INSERT INTO Institution SET
  name = 'HR Management System',
  description = 'Modern HR management system with AI-powered analytics',
  address = {'street': '123 Business St', 'city': 'New York', 'state': 'NY', 'zip_code': '10001'},
  phone = '+1-555-0123',
  email = 'admin@hrmkit.com',
  website = 'https://hrmkit.com',
  founded_date = '2024-01-01';

-- Insert default admin user
INSERT INTO User SET
  email = 'admin@hrmkit.com',
  password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6fYzYXkqO', -- 'admin123'
  role = 'admin',
  is_active = true,
  created_at = sysdate(),
  updated_at = sysdate();

-- Insert default leave types
INSERT INTO LeaveType SET
  name = 'Annual Leave',
  description = 'Standard annual vacation leave',
  days_per_year = 25,
  is_paid = true,
  requires_approval = true,
  is_active = true;

INSERT INTO LeaveType SET
  name = 'Sick Leave',
  description = 'Medical leave for illness',
  days_per_year = 10,
  is_paid = true,
  requires_approval = false,
  is_active = true;

INSERT INTO LeaveType SET
  name = 'Personal Leave',
  description = 'Personal time off',
  days_per_year = 5,
  is_paid = true,
  requires_approval = true,
  is_active = true;

-- Insert default departments
INSERT INTO Department SET
  name = 'Information Technology',
  description = 'IT department responsible for technology infrastructure',
  budget = 500000.00,
  location = 'Floor 3',
  is_active = true,
  created_at = sysdate();

INSERT INTO Department SET
  name = 'Human Resources',
  description = 'HR department managing employee relations',
  budget = 200000.00,
  location = 'Floor 2',
  is_active = true,
  created_at = sysdate();

INSERT INTO Department SET
  name = 'Finance',
  description = 'Finance department handling accounting and budgeting',
  budget = 300000.00,
  location = 'Floor 4',
  is_active = true,
  created_at = sysdate();

-- Insert default shift templates
INSERT INTO ShiftTemplate SET
  name = 'Standard Day Shift',
  description = 'Regular 9-5 workday',
  start_time = '09:00',
  end_time = '17:00',
  duration_hours = 8.0,
  break_duration = 60,
  is_active = true,
  created_at = sysdate();

INSERT INTO ShiftTemplate SET
  name = 'Morning Shift',
  description = 'Early morning shift',
  start_time = '06:00',
  end_time = '14:00',
  duration_hours = 8.0,
  break_duration = 60,
  is_active = true,
  created_at = sysdate();

INSERT INTO ShiftTemplate SET
  name = 'Evening Shift',
  description = 'Evening shift',
  start_time = '14:00',
  end_time = '22:00',
  duration_hours = 8.0,
  break_duration = 60,
  is_active = true,
  created_at = sysdate();

-- Insert system settings
INSERT INTO SystemSetting SET
  key = 'timezone',
  value = 'America/New_York',
  category = 'system',
  description = 'Default timezone for the system',
  updated_at = sysdate();

INSERT INTO SystemSetting SET
  key = 'working_days_per_week',
  value = '5',
  category = 'work_schedule',
  description = 'Number of working days per week',
  updated_at = sysdate();

INSERT INTO SystemSetting SET
  key = 'default_leave_approval_required',
  value = 'true',
  category = 'leave_policy',
  description = 'Whether leave requests require approval by default',
  updated_at = sysdate();

-- ===========================================
-- FUNCTIONS AND TRIGGERS
-- ===========================================

-- Function to calculate leave balance
CREATE FUNCTION calculate_leave_balance(employee_id, leave_type_id, year)
{
  local balance = 0;
  local used = 0;

  -- Get leave type days per year
  local leaveType = SELECT FROM LeaveType WHERE @rid = leave_type_id;
  if (leaveType.size() > 0) {
    balance = leaveType[0].days_per_year;
  }

  -- Calculate used days for the year
  local usedDays = SELECT sum(days_requested) as total
    FROM LeaveRequest
    WHERE employee_id = employee_id
    AND leave_type_id = leave_type_id
    AND status = 'approved'
    AND year(start_date) = year;

  if (usedDays.size() > 0 && usedDays[0].total != null) {
    used = usedDays[0].total;
  }

  return balance - used;
}

-- Function to validate schedule conflicts
CREATE FUNCTION validate_schedule(employee_id, shift_template_id, date)
{
  -- Check if employee already has a schedule for this date
  local existing = SELECT FROM Schedule
    WHERE employee_id = employee_id
    AND date = date;

  return existing.size() == 0;
}

-- ===========================================
-- END OF SCHEMA
-- ===========================================

-- User Sessions for JWT management
CREATE TABLE user_sessions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_token_hash (token_hash),
    INDEX idx_expires_at (expires_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Departments
CREATE TABLE departments (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    manager_id BIGINT NULL,
    parent_department_id BIGINT NULL,
    budget DECIMAL(15,2) NULL,
    location VARCHAR(255),
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (manager_id) REFERENCES users(id),
    FOREIGN KEY (parent_department_id) REFERENCES departments(id),
    INDEX idx_code (code),
    INDEX idx_manager_id (manager_id),
    INDEX idx_parent_department (parent_department_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Positions/Job Titles
CREATE TABLE positions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    department_id BIGINT NOT NULL,
    level ENUM('junior', 'senior', 'lead', 'manager', 'director', 'executive') NOT NULL,
    salary_range_min DECIMAL(12,2),
    salary_range_max DECIMAL(12,2),
    responsibilities JSON,
    required_skills JSON,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    INDEX idx_department_id (department_id),
    INDEX idx_level (level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Employee Profiles
CREATE TABLE employees (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NULL UNIQUE,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    date_of_birth DATE,
    hire_date DATE NOT NULL,
    termination_date DATE NULL,
    employment_status ENUM('active', 'terminated', 'on_leave', 'suspended') DEFAULT 'active',
    department_id BIGINT NOT NULL,
    position_id BIGINT NOT NULL,
    manager_id BIGINT NULL,
    salary DECIMAL(12,2),
    benefits JSON,
    emergency_contact_name VARCHAR(255),
    emergency_contact_phone VARCHAR(20),
    address JSON,
    profile_picture VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (position_id) REFERENCES positions(id),
    FOREIGN KEY (manager_id) REFERENCES employees(id),
    INDEX idx_employee_id (employee_id),
    INDEX idx_user_id (user_id),
    INDEX idx_department_id (department_id),
    INDEX idx_position_id (position_id),
    INDEX idx_manager_id (manager_id),
    INDEX idx_employment_status (employment_status),
    INDEX idx_hire_date (hire_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Update users table to reference employee profile
ALTER TABLE users ADD CONSTRAINT fk_user_profile FOREIGN KEY (profile_id) REFERENCES employees(id);

-- =====================================================
-- SHIFT & TIMETABLE MANAGEMENT
-- =====================================================

-- Shift Templates
CREATE TABLE shift_templates (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    break_duration_minutes INT DEFAULT 60,
    break_start_time TIME,
    working_hours DECIMAL(4,2) NOT NULL,
    color VARCHAR(7) DEFAULT '#3B82F6',
    icon VARCHAR(10),
    is_active BOOLEAN DEFAULT TRUE,
    department_id BIGINT NULL,
    overtime_threshold DECIMAL(4,2) DEFAULT 8.00,
    weekend_applicable BOOLEAN DEFAULT FALSE,
    shift_allowance_percentage DECIMAL(5,2) DEFAULT 0.00,
    night_shift_bonus BOOLEAN DEFAULT FALSE,
    flexible_timing BOOLEAN DEFAULT FALSE,
    core_hours_start TIME,
    core_hours_end TIME,
    minimum_hours_per_day DECIMAL(4,2),
    maximum_hours_per_day DECIMAL(4,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    INDEX idx_code (code),
    INDEX idx_department_id (department_id),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Employee Shift Assignments (Daily assignments)
CREATE TABLE employee_shift_assignments (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    employee_id BIGINT NOT NULL,
    shift_template_id BIGINT NOT NULL,
    date DATE NOT NULL,
    status ENUM('scheduled', 'completed', 'cancelled', 'no_show') DEFAULT 'scheduled',
    actual_start_time TIME NULL,
    actual_end_time TIME NULL,
    break_taken_minutes INT DEFAULT 0,
    overtime_hours DECIMAL(4,2) DEFAULT 0.00,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (shift_template_id) REFERENCES shift_templates(id),
    UNIQUE KEY unique_employee_date (employee_id, date),
    INDEX idx_employee_id (employee_id),
    INDEX idx_shift_template_id (shift_template_id),
    INDEX idx_date (date),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Weekly Schedules (Template schedules)
CREATE TABLE weekly_schedules (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    employee_id BIGINT NOT NULL,
    week_start_date DATE NOT NULL,
    monday_shift_id BIGINT NULL,
    tuesday_shift_id BIGINT NULL,
    wednesday_shift_id BIGINT NULL,
    thursday_shift_id BIGINT NULL,
    friday_shift_id BIGINT NULL,
    saturday_shift_id BIGINT NULL,
    sunday_shift_id BIGINT NULL,
    status ENUM('draft', 'published', 'archived') DEFAULT 'draft',
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (monday_shift_id) REFERENCES shift_templates(id),
    FOREIGN KEY (tuesday_shift_id) REFERENCES shift_templates(id),
    FOREIGN KEY (wednesday_shift_id) REFERENCES shift_templates(id),
    FOREIGN KEY (thursday_shift_id) REFERENCES shift_templates(id),
    FOREIGN KEY (friday_shift_id) REFERENCES shift_templates(id),
    FOREIGN KEY (saturday_shift_id) REFERENCES shift_templates(id),
    FOREIGN KEY (sunday_shift_id) REFERENCES shift_templates(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    UNIQUE KEY unique_employee_week (employee_id, week_start_date),
    INDEX idx_employee_id (employee_id),
    INDEX idx_week_start_date (week_start_date),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- ATTENDANCE & TIME TRACKING
-- =====================================================

-- Attendance Records
CREATE TABLE attendance_records (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    employee_id BIGINT NOT NULL,
    date DATE NOT NULL,
    scheduled_shift_id BIGINT NULL,
    clock_in_time TIME NULL,
    clock_out_time TIME NULL,
    break_start_time TIME NULL,
    break_end_time TIME NULL,
    total_hours_worked DECIMAL(5,2) DEFAULT 0.00,
    overtime_hours DECIMAL(5,2) DEFAULT 0.00,
    status ENUM('present', 'absent', 'late', 'early_departure', 'half_day') DEFAULT 'present',
    location ENUM('office', 'remote', 'client_site', 'home') DEFAULT 'office',
    ip_address VARCHAR(45),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (scheduled_shift_id) REFERENCES shift_templates(id),
    UNIQUE KEY unique_employee_date (employee_id, date),
    INDEX idx_employee_id (employee_id),
    INDEX idx_date (date),
    INDEX idx_status (status),
    INDEX idx_location (location)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Leave Types
CREATE TABLE leave_types (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    days_per_year INT DEFAULT 0,
    carry_forward_allowed BOOLEAN DEFAULT FALSE,
    max_consecutive_days INT DEFAULT 30,
    requires_approval BOOLEAN DEFAULT TRUE,
    paid_leave BOOLEAN DEFAULT TRUE,
    color VARCHAR(7) DEFAULT '#10B981',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_code (code),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Leave Requests
CREATE TABLE leave_requests (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    employee_id BIGINT NOT NULL,
    leave_type_id BIGINT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_days DECIMAL(5,2) NOT NULL,
    reason TEXT,
    status ENUM('pending', 'approved', 'rejected', 'cancelled') DEFAULT 'pending',
    approved_by_id BIGINT NULL,
    approved_at TIMESTAMP NULL,
    comments TEXT,
    attachment_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (leave_type_id) REFERENCES leave_types(id),
    FOREIGN KEY (approved_by_id) REFERENCES employees(id),
    INDEX idx_employee_id (employee_id),
    INDEX idx_leave_type_id (leave_type_id),
    INDEX idx_start_date (start_date),
    INDEX idx_end_date (end_date),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Time Off Balances
CREATE TABLE time_off_balances (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    employee_id BIGINT NOT NULL,
    leave_type_id BIGINT NOT NULL,
    year YEAR NOT NULL,
    allocated_days DECIMAL(5,2) DEFAULT 0.00,
    used_days DECIMAL(5,2) DEFAULT 0.00,
    carried_forward_days DECIMAL(5,2) DEFAULT 0.00,
    remaining_days DECIMAL(5,2) DEFAULT 0.00,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (leave_type_id) REFERENCES leave_types(id),
    UNIQUE KEY unique_employee_leave_year (employee_id, leave_type_id, year),
    INDEX idx_employee_id (employee_id),
    INDEX idx_leave_type_id (leave_type_id),
    INDEX idx_year (year)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- SCHEDULE REQUESTS & APPROVALS
-- =====================================================

-- Schedule Change Requests
CREATE TABLE schedule_change_requests (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    employee_id BIGINT NOT NULL,
    request_type ENUM('shift_change', 'time_off', 'overtime', 'schedule_swap') NOT NULL,
    requested_date DATE NOT NULL,
    current_shift_id BIGINT NULL,
    requested_shift_id BIGINT NULL,
    reason TEXT,
    priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
    status ENUM('pending', 'approved', 'rejected', 'cancelled') DEFAULT 'pending',
    reviewed_by_id BIGINT NULL,
    reviewed_at TIMESTAMP NULL,
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (current_shift_id) REFERENCES shift_templates(id),
    FOREIGN KEY (requested_shift_id) REFERENCES shift_templates(id),
    FOREIGN KEY (reviewed_by_id) REFERENCES employees(id),
    INDEX idx_employee_id (employee_id),
    INDEX idx_request_type (request_type),
    INDEX idx_requested_date (requested_date),
    INDEX idx_status (status),
    INDEX idx_priority (priority)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- ORGANIZATION & INSTITUTION
-- =====================================================

-- Institution Profile
CREATE TABLE institution_profile (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    legal_name VARCHAR(255),
    registration_number VARCHAR(100),
    tax_id VARCHAR(100),
    founded_date DATE,
    industry VARCHAR(255),
    company_size VARCHAR(50),
    status ENUM('active', 'inactive', 'dissolved') DEFAULT 'active',
    headquarters_address TEXT,
    phone VARCHAR(20),
    email VARCHAR(255),
    website VARCHAR(255),
    fax VARCHAR(20),
    fiscal_year_start ENUM('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December') DEFAULT 'January',
    currency VARCHAR(3) DEFAULT 'USD',
    timezone VARCHAR(50) DEFAULT 'UTC',
    business_hours VARCHAR(100) DEFAULT '9:00 AM - 5:00 PM',
    working_days JSON,
    logo_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Business Rules
CREATE TABLE business_rules (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    rule_type ENUM('attendance', 'leave', 'scheduling', 'approval') NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    conditions JSON,
    actions JSON,
    is_active BOOLEAN DEFAULT TRUE,
    priority INT DEFAULT 0,
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_rule_type (rule_type),
    INDEX idx_is_active (is_active),
    INDEX idx_priority (priority)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- REPORTING & ANALYTICS
-- =====================================================

-- Coverage Analysis (Daily coverage metrics)
CREATE TABLE coverage_analysis (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    department_id BIGINT NULL,
    required_staff_count INT NOT NULL,
    scheduled_staff_count INT NOT NULL,
    actual_staff_count INT NOT NULL,
    status ENUM('understaffed', 'optimal', 'overstaffed') NOT NULL,
    coverage_percentage DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    INDEX idx_date (date),
    INDEX idx_department_id (department_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Performance Metrics
CREATE TABLE performance_metrics (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    employee_id BIGINT NOT NULL,
    metric_type ENUM('attendance_rate', 'punctuality', 'overtime_hours', 'leave_balance', 'productivity') NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    value DECIMAL(10,2) NOT NULL,
    target_value DECIMAL(10,2),
    status ENUM('below_target', 'on_target', 'above_target', 'not_applicable'),
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    INDEX idx_employee_id (employee_id),
    INDEX idx_metric_type (metric_type),
    INDEX idx_period_start (period_start),
    INDEX idx_period_end (period_end)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Audit Logs
CREATE TABLE audit_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NULL,
    action ENUM('CREATE', 'UPDATE', 'DELETE', 'LOGIN', 'LOGOUT', 'EXPORT', 'IMPORT') NOT NULL,
    table_name VARCHAR(100) NOT NULL,
    record_id BIGINT NULL,
    old_values JSON,
    new_values JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_id (user_id),
    INDEX idx_action (action),
    INDEX idx_table_name (table_name),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- INITIAL DATA SEEDING
-- =====================================================

-- Insert default institution profile
INSERT INTO institution_profile (name, legal_name, industry, company_size, status, email, website, fiscal_year_start, currency, timezone, working_days)
VALUES ('KWARECOM Inc.', 'KWARECOM Incorporated', 'Technology Services', '51-200', 'active', 'info@kwarecominc.com', 'https://kwarecominc.com', 'January', 'USD', 'America/New_York', '["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]');

-- Insert default departments
INSERT INTO departments (name, code, description) VALUES
('Information Technology', 'IT', 'Technology infrastructure and software development'),
('Human Resources', 'HR', 'Employee management and organizational development'),
('Finance', 'FIN', 'Financial planning and accounting'),
('Operations', 'OPS', 'Business operations and logistics'),
('Marketing', 'MKT', 'Brand management and customer acquisition'),
('Sales', 'SAL', 'Revenue generation and customer relationships');

-- Insert default leave types
INSERT INTO leave_types (name, code, days_per_year, carry_forward_allowed, requires_approval, paid_leave, color) VALUES
('Annual Leave', 'ANNUAL', 25, TRUE, TRUE, TRUE, '#10B981'),
('Sick Leave', 'SICK', 10, FALSE, TRUE, TRUE, '#EF4444'),
('Personal Leave', 'PERSONAL', 5, FALSE, TRUE, TRUE, '#F59E0B'),
('Maternity Leave', 'MATERNITY', 90, FALSE, TRUE, TRUE, '#EC4899'),
('Paternity Leave', 'PATERNITY', 10, FALSE, TRUE, TRUE, '#3B82F6'),
('Emergency Leave', 'EMERGENCY', 5, FALSE, TRUE, TRUE, '#8B5CF6');

-- Insert default shift templates
INSERT INTO shift_templates (name, code, start_time, end_time, break_duration_minutes, working_hours, color, icon) VALUES
('Morning Shift', 'MORNING', '08:00:00', '16:00:00', 60, 8.00, '#F59E0B', '🌅'),
('Afternoon Shift', 'AFTERNOON', '14:00:00', '22:00:00', 60, 8.00, '#F59E0B', '🌇'),
('Night Shift', 'NIGHT', '22:00:00', '06:00:00', 45, 8.00, '#1F2937', '🌙'),
('Regular Day Shift', 'REGULAR', '09:00:00', '17:00:00', 60, 8.00, '#22c55e', '☀️'),
('Part Time Shift', 'PART_TIME', '09:00:00', '13:00:00', 0, 4.00, '#06b6d4', '⏰');

-- Create default admin user (password should be hashed in production)
INSERT INTO users (email, password_hash, role, status) VALUES
('admin@hrmkit.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj8GqH5Qk7K', 'admin', 'active'); -- password: admin123

-- =====================================================
-- TRIGGERS FOR AUDIT LOGGING
-- =====================================================

-- Trigger for users table
DELIMITER ;;
CREATE TRIGGER audit_users_trigger AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    INSERT INTO audit_logs (user_id, action, table_name, record_id, old_values, new_values)
    VALUES (NEW.id, 'UPDATE', 'users', NEW.id,
        JSON_OBJECT('email', OLD.email, 'role', OLD.role, 'status', OLD.status),
        JSON_OBJECT('email', NEW.email, 'role', NEW.role, 'status', NEW.status));
END;;
DELIMITER ;

-- Trigger for employees table
DELIMITER ;;
CREATE TRIGGER audit_employees_trigger AFTER UPDATE ON employees
FOR EACH ROW
BEGIN
    INSERT INTO audit_logs (user_id, action, table_name, record_id, old_values, new_values)
    VALUES (NEW.user_id, 'UPDATE', 'employees', NEW.id,
        JSON_OBJECT('first_name', OLD.first_name, 'last_name', OLD.last_name, 'email', OLD.email, 'employment_status', OLD.employment_status),
        JSON_OBJECT('first_name', NEW.first_name, 'last_name', NEW.last_name, 'email', NEW.email, 'employment_status', NEW.employment_status));
END;;
DELIMITER ;

-- =====================================================
-- VIEWS FOR COMMON QUERIES
-- =====================================================

-- Employee summary view
CREATE VIEW employee_summary AS
SELECT
    e.id,
    e.employee_id,
    CONCAT(e.first_name, ' ', e.last_name) as full_name,
    e.email,
    e.employment_status,
    d.name as department_name,
    p.title as position_title,
    e.hire_date,
    e.salary,
    CONCAT(m.first_name, ' ', m.last_name) as manager_name
FROM employees e
LEFT JOIN departments d ON e.department_id = d.id
LEFT JOIN positions p ON e.position_id = p.id
LEFT JOIN employees m ON e.manager_id = m.id;

-- Attendance summary view
CREATE VIEW attendance_summary AS
SELECT
    a.employee_id,
    CONCAT(e.first_name, ' ', e.last_name) as employee_name,
    d.name as department_name,
    COUNT(CASE WHEN a.status = 'present' THEN 1 END) as present_days,
    COUNT(CASE WHEN a.status = 'absent' THEN 1 END) as absent_days,
    COUNT(CASE WHEN a.status = 'late' THEN 1 END) as late_days,
    ROUND(AVG(a.total_hours_worked), 2) as avg_hours_per_day,
    SUM(a.overtime_hours) as total_overtime_hours
FROM attendance_records a
JOIN employees e ON a.employee_id = e.id
JOIN departments d ON e.department_id = d.id
WHERE a.date >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
GROUP BY a.employee_id, e.first_name, e.last_name, d.name;

-- =====================================================
-- STORED PROCEDURES
-- =====================================================

-- Procedure to calculate leave balances
DELIMITER ;;
CREATE PROCEDURE calculate_leave_balances(IN emp_id BIGINT, IN calc_year YEAR)
BEGIN
    DECLARE allocated_days DECIMAL(5,2);
    DECLARE used_days DECIMAL(5,2);

    -- Get allocated days for each leave type
    INSERT INTO time_off_balances (employee_id, leave_type_id, year, allocated_days, remaining_days)
    SELECT emp_id, lt.id, calc_year, lt.days_per_year, lt.days_per_year
    FROM leave_types lt
    WHERE lt.is_active = TRUE
    ON DUPLICATE KEY UPDATE
        allocated_days = lt.days_per_year,
        remaining_days = lt.days_per_year - used_days;

    -- Update used days
    UPDATE time_off_balances tob
    JOIN (
        SELECT
            lr.employee_id,
            lr.leave_type_id,
            YEAR(lr.start_date) as year,
            SUM(lr.total_days) as used_days
        FROM leave_requests lr
        WHERE lr.status = 'approved'
        AND lr.employee_id = emp_id
        AND YEAR(lr.start_date) = calc_year
        GROUP BY lr.employee_id, lr.leave_type_id, YEAR(lr.start_date)
    ) usage ON tob.employee_id = usage.employee_id
        AND tob.leave_type_id = usage.leave_type_id
        AND tob.year = usage.year
    SET tob.used_days = usage.used_days,
        tob.remaining_days = tob.allocated_days - usage.used_days;
END;;
DELIMITER ;

-- =====================================================
-- DATABASE OPTIMIZATION
-- =====================================================

-- Create composite indexes for performance
CREATE INDEX idx_attendance_employee_date ON attendance_records (employee_id, date);
CREATE INDEX idx_leave_requests_employee_dates ON leave_requests (employee_id, start_date, end_date);
CREATE INDEX idx_shift_assignments_employee_date ON employee_shift_assignments (employee_id, date);
CREATE INDEX idx_performance_employee_period ON performance_metrics (employee_id, period_start, period_end);

-- Partition attendance_records by month for better performance
ALTER TABLE attendance_records
PARTITION BY RANGE (YEAR(date) * 100 + MONTH(date)) (
    PARTITION p202401 VALUES LESS THAN (202402),
    PARTITION p202402 VALUES LESS THAN (202403),
    PARTITION p202403 VALUES LESS THAN (202404),
    PARTITION p202404 VALUES LESS THAN (202405),
    PARTITION p202405 VALUES LESS THAN (202406),
    PARTITION p202406 VALUES LESS THAN (202407),
    PARTITION p202407 VALUES LESS THAN (202408),
    PARTITION p202408 VALUES LESS THAN (202409),
    PARTITION p202409 VALUES LESS THAN (202410),
    PARTITION p202410 VALUES LESS THAN (202411),
    PARTITION p202411 VALUES LESS THAN (202412),
    PARTITION p202412 VALUES LESS THAN (202501),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- =====================================================
-- FINAL NOTES
-- =====================================================

/*
Database Setup Instructions:

1. Create the database:
   CREATE DATABASE hrms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

2. Run this script to create all tables, indexes, and initial data.

3. Update connection settings in your application configuration.

4. For production:
   - Set up automated backups
   - Configure connection pooling
   - Implement proper security measures
   - Set up monitoring and alerting

5. Regular maintenance:
   - Update partitions monthly for attendance_records
   - Archive old audit logs
   - Update performance metrics regularly

Security Considerations:
- Use parameterized queries to prevent SQL injection
- Implement row-level security for multi-tenant scenarios
- Encrypt sensitive data (salaries, personal information)
- Regular security audits and updates
*/