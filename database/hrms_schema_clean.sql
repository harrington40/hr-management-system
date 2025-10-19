ALTER DATABASE CUSTOM useLightweightEdges=false;
ALTER DATABASE CUSTOM useClassForEdgeLabel=false;
ALTER DATABASE CUSTOM useClassForVertexLabel=false;
CREATE CLASS User EXTENDS V;
CREATE PROPERTY User.email STRING;
CREATE PROPERTY User.password_hash STRING;
CREATE PROPERTY User.role STRING; 
CREATE PROPERTY User.is_active BOOLEAN DEFAULT true;
CREATE PROPERTY User.created_at DATETIME;
CREATE PROPERTY User.updated_at DATETIME;
CREATE PROPERTY User.last_login DATETIME;
CREATE INDEX User.email UNIQUE;
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
CREATE INDEX Employee.employee_id UNIQUE;
CREATE CLASS Department EXTENDS V;
CREATE PROPERTY Department.name STRING;
CREATE PROPERTY Department.description STRING;
CREATE PROPERTY Department.manager_id LINK Employee;
CREATE PROPERTY Department.budget DECIMAL;
CREATE PROPERTY Department.location STRING;
CREATE PROPERTY Department.is_active BOOLEAN DEFAULT true;
CREATE PROPERTY Department.created_at DATETIME;
CREATE INDEX Department.name UNIQUE;
CREATE CLASS Position EXTENDS V;
CREATE PROPERTY Position.title STRING;
CREATE PROPERTY Position.description STRING;
CREATE PROPERTY Position.level STRING;
CREATE PROPERTY Position.salary_range EMBEDDED ORange;
CREATE PROPERTY Position.department_id LINK Department;
CREATE PROPERTY Position.is_active BOOLEAN DEFAULT true;
CREATE CLASS ShiftTemplate EXTENDS V;
CREATE PROPERTY ShiftTemplate.name STRING;
CREATE PROPERTY ShiftTemplate.description STRING;
CREATE PROPERTY ShiftTemplate.start_time STRING; 
CREATE PROPERTY ShiftTemplate.end_time STRING; 
CREATE PROPERTY ShiftTemplate.duration_hours DECIMAL;
CREATE PROPERTY ShiftTemplate.break_duration INTEGER; 
CREATE PROPERTY ShiftTemplate.is_active BOOLEAN DEFAULT true;
CREATE PROPERTY ShiftTemplate.created_at DATETIME;
CREATE CLASS Schedule EXTENDS V;
CREATE PROPERTY Schedule.employee_id LINK Employee;
CREATE PROPERTY Schedule.shift_template_id LINK ShiftTemplate;
CREATE PROPERTY Schedule.date DATE;
CREATE PROPERTY Schedule.status STRING DEFAULT 'scheduled'; 
CREATE PROPERTY Schedule.notes STRING;
CREATE INDEX Schedule.employee_date ON Schedule (employee_id, date) UNIQUE;
CREATE CLASS AttendanceRecord EXTENDS V;
CREATE PROPERTY AttendanceRecord.employee_id LINK Employee;
CREATE PROPERTY AttendanceRecord.date DATE;
CREATE PROPERTY AttendanceRecord.clock_in_time DATETIME;
CREATE PROPERTY AttendanceRecord.clock_out_time DATETIME;
CREATE PROPERTY AttendanceRecord.break_start_time DATETIME;
CREATE PROPERTY AttendanceRecord.break_end_time DATETIME;
CREATE PROPERTY AttendanceRecord.hours_worked DECIMAL;
CREATE PROPERTY AttendanceRecord.status STRING DEFAULT 'present'; 
CREATE PROPERTY AttendanceRecord.location STRING;
CREATE PROPERTY AttendanceRecord.notes STRING;
CREATE INDEX AttendanceRecord.employee_date ON AttendanceRecord (employee_id, date) UNIQUE;
CREATE CLASS LeaveType EXTENDS V;
CREATE PROPERTY LeaveType.name STRING;
CREATE PROPERTY LeaveType.description STRING;
CREATE PROPERTY LeaveType.days_per_year INTEGER;
CREATE PROPERTY LeaveType.is_paid BOOLEAN DEFAULT true;
CREATE PROPERTY LeaveType.requires_approval BOOLEAN DEFAULT true;
CREATE PROPERTY LeaveType.is_active BOOLEAN DEFAULT true;
CREATE CLASS LeaveRequest EXTENDS V;
CREATE PROPERTY LeaveRequest.employee_id LINK Employee;
CREATE PROPERTY LeaveRequest.leave_type_id LINK LeaveType;
CREATE PROPERTY LeaveRequest.start_date DATE;
CREATE PROPERTY LeaveRequest.end_date DATE;
CREATE PROPERTY LeaveRequest.days_requested DECIMAL;
CREATE PROPERTY LeaveRequest.reason STRING;
CREATE PROPERTY LeaveRequest.status STRING DEFAULT 'pending'; 
CREATE PROPERTY LeaveRequest.approved_by LINK Employee;
CREATE PROPERTY LeaveRequest.approved_at DATETIME;
CREATE PROPERTY LeaveRequest.created_at DATETIME;
CREATE PROPERTY LeaveRequest.comments STRING;
CREATE CLASS LeaveBalance EXTENDS V;
CREATE PROPERTY LeaveBalance.employee_id LINK Employee;
CREATE PROPERTY LeaveBalance.leave_type_id LINK LeaveType;
CREATE PROPERTY LeaveBalance.year INTEGER;
CREATE PROPERTY LeaveBalance.balance_days DECIMAL;
CREATE PROPERTY LeaveBalance.used_days DECIMAL DEFAULT 0;
CREATE PROPERTY LeaveBalance.carried_forward DECIMAL DEFAULT 0;
CREATE INDEX LeaveBalance.employee_year ON LeaveBalance (employee_id, year);
CREATE CLASS WorksIn EXTENDS E;
CREATE PROPERTY WorksIn.start_date DATE;
CREATE PROPERTY WorksIn.end_date DATE;
CREATE PROPERTY WorksIn.is_primary BOOLEAN DEFAULT true;
CREATE CLASS ReportsTo EXTENDS E;
CREATE PROPERTY ReportsTo.relationship_type STRING DEFAULT 'direct'; 
CREATE PROPERTY ReportsTo.start_date DATE;
CREATE PROPERTY ReportsTo.end_date DATE;
CREATE CLASS AssignedTo EXTENDS E;
CREATE PROPERTY AssignedTo.start_date DATE;
CREATE PROPERTY AssignedTo.end_date DATE;
CREATE PROPERTY AssignedTo.is_current BOOLEAN DEFAULT true;
CREATE CLASS Manages EXTENDS E;
CREATE PROPERTY Manages.start_date DATE;
CREATE PROPERTY Manages.end_date DATE;
CREATE PROPERTY Manages.responsibilities EMBEDDEDLIST STRING;
CREATE CLASS OAddress;
CREATE PROPERTY OAddress.street STRING;
CREATE PROPERTY OAddress.city STRING;
CREATE PROPERTY OAddress.state STRING;
CREATE PROPERTY OAddress.zip_code STRING;
CREATE PROPERTY OAddress.country STRING DEFAULT 'USA';
CREATE CLASS OContact;
CREATE PROPERTY OContact.name STRING;
CREATE PROPERTY OContact.relationship STRING;
CREATE PROPERTY OContact.phone STRING;
CREATE PROPERTY OContact.email STRING;
CREATE CLASS OCertification;
CREATE PROPERTY OCertification.name STRING;
CREATE PROPERTY OCertification.issuing_authority STRING;
CREATE PROPERTY OCertification.issue_date DATE;
CREATE PROPERTY OCertification.expiry_date DATE;
CREATE PROPERTY OCertification.certification_number STRING;
CREATE CLASS ORange;
CREATE PROPERTY ORange.min DECIMAL;
CREATE PROPERTY ORange.max DECIMAL;
CREATE PROPERTY ORange.currency STRING DEFAULT 'USD';
CREATE CLASS AuditLog EXTENDS V;
CREATE PROPERTY AuditLog.entity_type STRING; 
CREATE PROPERTY AuditLog.entity_id STRING; 
CREATE PROPERTY AuditLog.action STRING; 
CREATE PROPERTY AuditLog.user_id LINK User; 
CREATE PROPERTY AuditLog.timestamp DATETIME;
CREATE PROPERTY AuditLog.old_values STRING; 
CREATE PROPERTY AuditLog.new_values STRING; 
CREATE PROPERTY AuditLog.ip_address STRING;
CREATE PROPERTY AuditLog.user_agent STRING;
CREATE INDEX AuditLog.entity_timestamp ON AuditLog (entity_type, timestamp);
CREATE CLASS Institution EXTENDS V;
CREATE PROPERTY Institution.name STRING;
CREATE PROPERTY Institution.description STRING;
CREATE PROPERTY Institution.address EMBEDDED OAddress;
CREATE PROPERTY Institution.phone STRING;
CREATE PROPERTY Institution.email STRING;
CREATE PROPERTY Institution.website STRING;
CREATE PROPERTY Institution.tax_id STRING;
CREATE PROPERTY Institution.founded_date DATE;
CREATE CLASS SystemSetting EXTENDS V;
CREATE PROPERTY SystemSetting.key STRING;
CREATE PROPERTY SystemSetting.value STRING;
CREATE PROPERTY SystemSetting.category STRING;
CREATE PROPERTY SystemSetting.description STRING;
CREATE PROPERTY SystemSetting.updated_at DATETIME;
CREATE PROPERTY SystemSetting.updated_by LINK User;
CREATE INDEX SystemSetting.key UNIQUE;
CREATE INDEX User.role_active ON User (role, is_active);
CREATE INDEX Employee.hire_date ON Employee (hire_date);
CREATE INDEX Employee.last_name ON Employee (last_name);
CREATE INDEX Department.manager_id ON Department (manager_id);
CREATE INDEX Position.department_id ON Position (department_id);
CREATE INDEX ShiftTemplate.is_active ON ShiftTemplate (is_active);
CREATE INDEX LeaveRequest.status ON LeaveRequest (status);
CREATE INDEX LeaveRequest.employee_status ON LeaveRequest (employee_id, status);
CREATE INDEX AttendanceRecord.status_date ON AttendanceRecord (status, date);
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
INSERT INTO Institution SET
  name = 'HR Management System',
  description = 'Modern HR management system with AI-powered analytics',
  address = {'street': '123 Business St', 'city': 'New York', 'state': 'NY', 'zip_code': '10001'},
  phone = '+1-555-0123',
  email = 'admin@hrmkit.com',
  website = 'https://hrmkit.com',
  founded_date = '2024-01-01';
INSERT INTO User SET
  email = 'admin@hrmkit.com',
  password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6fYzYXkqO', 
  role = 'admin',
  is_active = true,
  created_at = sysdate(),
  updated_at = sysdate();
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
CREATE FUNCTION calculate_leave_balance(employee_id, leave_type_id, year)
{
  local balance = 0;
  local used = 0;
  
  local leaveType = SELECT FROM LeaveType WHERE @rid = leave_type_id;
  if (leaveType.size() > 0) {
    balance = leaveType[0].days_per_year;
  }
  
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
CREATE FUNCTION validate_schedule(employee_id, shift_template_id, date)
{
  
  local existing = SELECT FROM Schedule
    WHERE employee_id = employee_id
    AND date = date;
  return existing.size() == 0;
}
