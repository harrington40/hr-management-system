# HRMS OrientDB Data Flow Map
# Multi-model data architecture for Human Resource Management System

## OrientDB Multi-Model Architecture

OrientDB combines three models in a single database:
- **Document Model**: Schema-less documents with properties
- **Graph Model**: Vertices (entities) connected by edges (relationships)
- **Key-Value Model**: Fast key-based lookups

## Core Vertex Classes (Entities)

### 1. USER MANAGEMENT & AUTHENTICATION
```
User (Vertex Class - Document Model)
├── @rid (Record ID - unique identifier)
├── email (String, indexed, unique)
├── password_hash (String)
├── role (String: 'admin', 'manager', 'employee')
├── is_active (Boolean, default: true)
├── created_at (Datetime)
├── updated_at (Datetime)
└── last_login (Datetime)

Employee (Vertex Class - extends User)
├── @rid (Record ID)
├── employee_id (String, indexed, unique)
├── first_name (String)
├── last_name (String)
├── date_of_birth (Date)
├── gender (String)
├── phone (String)
├── address (Embedded OAddress)
├── hire_date (Date)
├── salary (Decimal)
├── position (String)
├── emergency_contact (Embedded OContact)
├── skills (EmbeddedList<String>)
├── certifications (EmbeddedList<OCertification>)
└── Inherits all User properties
```

### 2. ORGANIZATIONAL STRUCTURE
```
Department (Vertex Class)
├── @rid (Record ID)
├── name (String, indexed, unique)
├── description (String)
├── manager_id (Link<Employee>)
├── budget (Decimal)
├── location (String)
├── is_active (Boolean, default: true)
└── created_at (Datetime)

Position (Vertex Class)
├── @rid (Record ID)
├── title (String)
├── description (String)
├── level (String)
├── salary_range (Embedded ORange)
├── department_id (Link<Department>)
├── is_active (Boolean, default: true)
└── created_at (Datetime)
```

## Edge Classes (Relationships)

### 1. ORGANIZATIONAL RELATIONSHIPS
```
WorksIn (Edge Class)
├── @rid (Edge ID)
├── out (Employee vertex)
├── in (Department vertex)
├── start_date (Date)
├── end_date (Date, nullable)
└── is_primary (Boolean, default: true)

ReportsTo (Edge Class)
├── @rid (Edge ID)
├── out (Employee vertex - subordinate)
├── in (Employee vertex - manager)
├── relationship_type (String: 'direct', 'dotted')
├── start_date (Date)
├── end_date (Date, nullable)
└── created_at (Datetime)

AssignedTo (Edge Class)
├── @rid (Edge ID)
├── out (Employee vertex)
├── in (Position vertex)
├── start_date (Date)
├── end_date (Date, nullable)
└── is_current (Boolean, default: true)

Manages (Edge Class)
├── @rid (Edge ID)
├── out (Employee vertex - manager)
├── in (Department vertex)
├── start_date (Date)
├── end_date (Date, nullable)
└── responsibilities (EmbeddedList<String>)
```

### 2. WORK MANAGEMENT RELATIONSHIPS
```
Schedule (Vertex Class - with relationships)
├── @rid (Record ID)
├── employee_id (Link<Employee>)
├── shift_template_id (Link<ShiftTemplate>)
├── date (Date)
├── status (String: 'scheduled', 'completed', 'cancelled')
└── notes (String)

ShiftTemplate (Vertex Class)
├── @rid (Record ID)
├── name (String)
├── description (String)
├── start_time (String - HH:MM format)
├── end_time (String - HH:MM format)
├── duration_hours (Decimal)
├── break_duration (Integer - minutes)
├── is_active (Boolean, default: true)
└── created_at (Datetime)
```

## Embedded Classes (Complex Data Types)

### 1. CONTACT & ADDRESS INFORMATION
```
OAddress (Embedded Class)
├── street (String)
├── city (String)
├── state (String)
├── zip_code (String)
└── country (String, default: 'USA')

OContact (Embedded Class)
├── name (String)
├── relationship (String)
├── phone (String)
└── email (String)

OCertification (Embedded Class)
├── name (String)
├── issuing_authority (String)
├── issue_date (Date)
├── expiry_date (Date)
└── certification_number (String)

ORange (Embedded Class)
├── min (Decimal)
└── max (Decimal)
```

## Time & Attendance Data Model

### 1. ATTENDANCE TRACKING
```
AttendanceRecord (Vertex Class)
├── @rid (Record ID)
├── employee_id (Link<Employee>)
├── date (Date)
├── clock_in_time (Datetime)
├── clock_out_time (Datetime)
├── break_start_time (Datetime)
├── break_end_time (Datetime)
├── hours_worked (Decimal - calculated)
├── status (String: 'present', 'absent', 'late', 'half-day')
├── location (String)
└── notes (String)
```

### 2. LEAVE MANAGEMENT
```
LeaveType (Vertex Class)
├── @rid (Record ID)
├── name (String)
├── description (String)
├── days_per_year (Integer)
├── is_paid (Boolean, default: true)
├── requires_approval (Boolean, default: true)
├── is_active (Boolean, default: true)
└── created_at (Datetime)

LeaveRequest (Vertex Class)
├── @rid (Record ID)
├── employee_id (Link<Employee>)
├── leave_type_id (Link<LeaveType>)
├── start_date (Date)
├── end_date (Date)
├── days_requested (Decimal)
├── reason (String)
├── status (String: 'pending', 'approved', 'rejected', 'cancelled')
├── approved_by (Link<Employee>)
├── approved_at (Datetime)
├── created_at (Datetime)
└── comments (String)

LeaveBalance (Vertex Class)
├── @rid (Record ID)
├── employee_id (Link<Employee>)
├── leave_type_id (Link<LeaveType>)
├── year (Integer)
├── balance_days (Decimal)
├── used_days (Decimal, default: 0)
└── carried_forward (Decimal, default: 0)
```

## System & Audit Data Model

### 1. SYSTEM CONFIGURATION
```
Institution (Vertex Class)
├── @rid (Record ID)
├── name (String)
├── description (String)
├── address (Embedded OAddress)
├── phone (String)
├── email (String)
├── website (String)
├── tax_id (String)
└── founded_date (Date)

SystemSetting (Vertex Class)
├── @rid (Record ID)
├── key (String, indexed, unique)
├── value (String)
├── category (String)
├── description (String)
├── updated_at (Datetime)
└── updated_by (Link<User>)
```

### 2. AUDIT & LOGGING
```
AuditLog (Vertex Class)
├── @rid (Record ID)
├── entity_type (String: 'User', 'Employee', 'Department', etc.)
├── entity_id (String - RID or external ID)
├── action (String: 'CREATE', 'UPDATE', 'DELETE')
├── user_id (Link<User> - who performed action)
├── timestamp (Datetime)
├── old_values (String - JSON representation)
├── new_values (String - JSON representation)
├── ip_address (String)
└── user_agent (String)
```

## Data Flow Patterns

### 1. EMPLOYEE ONBOARDING FLOW
```
Graph Traversal: Employee → WorksIn → Department
Document Operations: Create User → Create Employee → Create Relationships

1. User Creation
   ├── Create User vertex with authentication data
   └── Set initial role and status

2. Employee Profile Creation
   ├── Create Employee vertex extending User
   ├── Set personal and employment details
   └── Embed complex data (address, contacts, skills)

3. Organizational Assignment
   ├── Create WorksIn edge to Department
   ├── Create ReportsTo edge to Manager
   └── Create AssignedTo edge to Position

4. Initial Setup
   ├── Create LeaveBalance vertices for each LeaveType
   └── Set initial balances based on company policy
```

### 2. DAILY ATTENDANCE FLOW
```
Graph Query: Employee → AttendanceRecord (by date)
Real-time Updates: Clock events trigger document updates

1. Clock In Event
   ├── Find or create AttendanceRecord for today
   ├── Set clock_in_time
   └── Update status to 'present'

2. Break Management
   ├── Update break_start_time when break begins
   └── Update break_end_time when break ends

3. Clock Out Event
   ├── Set clock_out_time
   ├── Calculate hours_worked automatically
   └── Update attendance status
```

### 3. LEAVE REQUEST WORKFLOW
```
Graph Traversal: Employee → LeaveRequest → LeaveType
State Management: Status updates with audit logging

1. Request Submission
   ├── Create LeaveRequest vertex
   ├── Link to Employee and LeaveType
   └── Set initial status as 'pending'

2. Approval Process
   ├── Manager traverses ReportsTo edges to find requests
   ├── Update status to 'approved'/'rejected'
   └── Create audit log entry

3. Balance Updates
   ├── Query LeaveBalance for employee and leave type
   ├── Update used_days when approved
   └── Trigger notifications if needed
```

### 4. REPORTING & ANALYTICS FLOW
```
Complex Traversals: Multi-hop graph queries with aggregations
Document Aggregation: Combine data from multiple vertex types

1. Attendance Reports
   ├── Traverse Employee → AttendanceRecord relationships
   ├── Filter by date ranges and departments
   └── Aggregate hours and presence data

2. Organizational Charts
   ├── Traverse ReportsTo edges from top-level managers
   ├── Build hierarchical structures
   └── Include department assignments via WorksIn edges

3. Leave Analytics
   ├── Query LeaveRequest vertices with aggregations
   ├── Group by department, leave type, and time periods
   └── Calculate utilization rates and trends
```

## Performance Optimization Strategies

### 1. INDEXING STRATEGY
```
Property Indexes:
├── User.email (UNIQUE)
├── Employee.employee_id (UNIQUE)
├── Department.name (UNIQUE)
├── Schedule.employee_date (COMPOSITE)
├── AttendanceRecord.employee_date (COMPOSITE)
└── LeaveBalance.employee_year (COMPOSITE)

Edge Indexes:
├── WorksIn.out_in (for fast traversals)
├── ReportsTo.out_in (organizational hierarchy)
└── Manages.out_in (department management)
```

### 2. QUERY OPTIMIZATION
```
Traversal Queries:
├── Use GREMLIN for complex graph traversals
├── Leverage edge indexes for relationship queries
└── Cache frequently accessed subgraphs

Document Queries:
├── Use SQL-like syntax for document operations
├── Leverage property indexes for filtered queries
└── Use projections to limit returned data
```

### 3. DATA PARTITIONING
```
Time-based Partitioning:
├── AttendanceRecord partitioned by month
├── AuditLog partitioned by quarter
└── LeaveRequest partitioned by year

Department-based Clustering:
├── Group related data by department RID
├── Optimize for department-specific queries
└── Support multi-tenant isolation
```

## Security & Access Control

### 1. ROW-LEVEL SECURITY
```
Graph-based Permissions:
├── Users can only access their own data
├── Managers can traverse their report structures
├── Admins have full graph access
└── Department isolation via edge restrictions

Document-level Security:
├── Property-level encryption for sensitive data
├── Audit logging for all data access
└── Temporal versioning for compliance
```

### 2. RELATIONSHIP SECURITY
```
Edge-based Access Control:
├── ReportsTo edges define management chains
├── WorksIn edges define department membership
├── Manages edges define administrative rights
└── Audit trails for relationship changes
```

## Integration Patterns

### 1. APPLICATION LAYER INTEGRATION
```
Service Layer (database_service.py):
├── Connection management with OrientDB client
├── CRUD operations for all vertex types
├── Graph traversal methods for relationships
└── Query builders for complex operations

Component Integration:
├── Replace YAML file operations with OrientDB calls
├── Use RID-based references instead of integer IDs
├── Leverage embedded documents for complex data
└── Implement real-time updates via graph traversals
```

### 2. EXTERNAL SYSTEM INTEGRATION
```
API Endpoints:
├── RESTful interface for document operations
├── GraphQL support for complex traversals
├── WebSocket support for real-time updates
└── Batch operations for bulk data imports

Third-party Integrations:
├── MQTT for real-time event publishing
├── Backblaze B2 for document attachments
├── gRPC for high-performance service calls
└── Webhooks for external system notifications
```

## Migration Strategy

### 1. FROM RELATIONAL DATABASE
```
Data Migration:
├── Export relational data to JSON format
├── Transform foreign keys to OrientDB RIDs
├── Create vertices and edges in dependency order
└── Validate data integrity post-migration

Application Updates:
├── Replace SQL queries with OrientDB operations
├── Update data models to use document structures
├── Implement graph traversal logic
└── Add connection handling for OrientDB client
```

### 2. FROM YAML CONFIGURATION
```
Configuration Migration:
├── Parse existing YAML files
├── Create corresponding OrientDB vertices
├── Establish relationship edges
└── Update component code to use database queries

Gradual Migration:
├── Start with read operations from OrientDB
├── Implement write operations incrementally
├── Maintain YAML fallback during transition
└── Validate data consistency throughout
```

## Monitoring & Maintenance

### 1. PERFORMANCE MONITORING
```
Query Performance:
├── Track query execution times
├── Monitor index usage statistics
├── Identify slow traversal patterns
└── Optimize frequently used paths

System Health:
├── Monitor connection pool utilization
├── Track vertex and edge growth
├── Alert on index fragmentation
└── Monitor disk space usage
```

### 2. BACKUP & RECOVERY
```
Automated Backups:
├── Full database exports on schedule
├── Incremental backup of recent changes
├── Point-in-time recovery capabilities
└── Encrypted backup storage

Disaster Recovery:
├── Multi-datacenter replication
├── Automatic failover mechanisms
├── Data consistency validation
└── Recovery time objective (RTO) monitoring
```

This OrientDB data architecture provides a flexible, scalable foundation for the HRMS while maintaining data integrity and supporting complex organizational relationships through its multi-model capabilities.
├── parent_department_id (FK to self)
├── budget
├── location
└── created_at

Positions
├── id
├── title
├── department_id (FK)
├── level (junior, senior, lead, manager)
├── salary_range_min, salary_range_max
├── responsibilities (JSON)
├── required_skills (JSON)
└── created_at
```

### 3. SHIFT & TIMETABLE MANAGEMENT
```
Shift Templates
├── id
├── name
├── code (Unique)
├── start_time, end_time
├── break_duration_minutes
├── break_start_time
├── working_hours
├── color (for UI)
├── is_active
├── department_id (FK, nullable for global templates)
├── overtime_threshold
├── weekend_applicable
├── shift_allowance_percentage
└── created_at

Employee Shift Assignments
├── id
├── employee_id (FK)
├── shift_template_id (FK)
├── date
├── status (scheduled, completed, cancelled)
├── actual_start_time, actual_end_time
├── break_taken_minutes
├── overtime_hours
├── notes
└── created_at, updated_at

Weekly Schedules
├── id
├── employee_id (FK)
├── week_start_date
├── monday_shift_id (FK to Shift Templates)
├── tuesday_shift_id (FK)
├── wednesday_shift_id (FK)
├── thursday_shift_id (FK)
├── friday_shift_id (FK)
├── saturday_shift_id (FK)
├── sunday_shift_id (FK)
├── status (draft, published, archived)
└── created_at, updated_at
```

### 4. ATTENDANCE & TIME TRACKING
```
Attendance Records
├── id
├── employee_id (FK)
├── date
├── scheduled_shift_id (FK to Shift Templates)
├── clock_in_time
├── clock_out_time
├── break_start_time, break_end_time
├── total_hours_worked
├── overtime_hours
├── status (present, absent, late, early_departure)
├── location (office, remote, client_site)
├── notes
└── created_at, updated_at

Leave Requests
├── id
├── employee_id (FK)
├── leave_type_id (FK)
├── start_date, end_date
├── total_days
├── reason
├── status (pending, approved, rejected, cancelled)
├── approved_by_id (FK to Employees)
├── approved_at
├── comments
└── created_at, updated_at

Leave Types
├── id
├── name (vacation, sick, personal, maternity, etc.)
├── code (Unique)
├── days_per_year
├── carry_forward_allowed
├── max_consecutive_days
├── requires_approval
├── paid_leave
└── created_at

Time Off Balances
├── id
├── employee_id (FK)
├── leave_type_id (FK)
├── year
├── allocated_days
├── used_days
├── carried_forward_days
├── remaining_days
└── updated_at
```

### 5. SCHEDULE REQUESTS & APPROVALS
```
Schedule Change Requests
├── id
├── employee_id (FK)
├── request_type (shift_change, time_off, overtime)
├── requested_date
├── current_shift_id (FK to Shift Templates)
├── requested_shift_id (FK to Shift Templates)
├── reason
├── priority (low, medium, high)
├── status (pending, approved, rejected)
├── reviewed_by_id (FK to Employees)
├── reviewed_at
├── comments
└── created_at, updated_at
```

### 6. ORGANIZATION & INSTITUTION
```
Institution Profile
├── id
├── name, legal_name
├── registration_number
├── tax_id
├── founded_date
├── industry
├── company_size
├── status
├── headquarters_address
├── phone, email, website
├── fiscal_year_start
├── currency, timezone
├── business_hours
├── working_days (JSON array)
└── created_at, updated_at

Business Rules
├── id
├── rule_type (attendance, leave, scheduling)
├── name
├── description
├── conditions (JSON)
├── actions (JSON)
├── is_active
├── priority
└── created_at, updated_at
```

### 7. REPORTING & ANALYTICS
```
Coverage Analysis
├── id
├── date
├── department_id (FK)
├── required_staff_count
├── scheduled_staff_count
├── actual_staff_count
├── status (understaffed, optimal, overstaffed)
├── coverage_percentage
└── created_at

Performance Metrics
├── id
├── employee_id (FK)
├── metric_type (attendance_rate, punctuality, overtime_hours)
├── period_start, period_end
├── value
├── target_value
├── status (below_target, on_target, above_target)
└── calculated_at

Audit Logs
├── id
├── user_id (FK)
├── action (CREATE, UPDATE, DELETE, LOGIN, etc.)
├── table_name
├── record_id
├── old_values (JSON)
├── new_values (JSON)
├── ip_address
├── user_agent
└── created_at
```

## Data Flow Patterns

### 1. Employee Onboarding Flow
```
HR Admin → Create User Account → Create Employee Profile → Assign Department/Position → Set Initial Leave Balances → Create Default Schedule
```

### 2. Daily Attendance Flow
```
Employee → Clock In → System Records Start Time → Break Tracking → Clock Out → Calculate Hours → Update Balances → Generate Reports
```

### 3. Schedule Management Flow
```
Manager → Create Weekly Schedule → Assign Shifts to Employees → Publish Schedule → Employees View Schedule → Submit Change Requests → Manager Approves/Rejects → Update Schedule
```

### 4. Leave Management Flow
```
Employee → Submit Leave Request → Auto-check Balances → Manager Approval → Update Leave Balances → Update Schedule → Send Notifications
```

### 5. Reporting Flow
```
System → Collect Attendance Data → Calculate Metrics → Generate Reports → Store Analytics → Send Alerts (if thresholds breached)
```

## Database Design Principles

### Normalization
- 3NF compliance for data integrity
- Proper foreign key relationships
- Avoid data redundancy

### Indexing Strategy
- Primary keys on all tables
- Foreign key indexes
- Composite indexes on frequently queried columns (employee_id + date)
- Full-text indexes on searchable fields

### Performance Considerations
- Connection pooling for high concurrency
- Read replicas for reporting queries
- Caching layer for frequently accessed data
- Partitioning for large tables (attendance records by month)

### Security
- Row-level security for multi-tenant data
- Encryption for sensitive data (salaries, PII)
- Audit logging for all changes
- Role-based access control

### Backup & Recovery
- Daily automated backups
- Point-in-time recovery capability
- Encrypted backup storage
- Regular restore testing