# HRMS RethinkDB Schema Design

## Overview
This document maps the HRMS application data requirements to RethinkDB table structure.

## Data Sources Analyzed
- OrientDB Schema (orientdb_schema.json)
- YAML Configuration Files (15+ files in config/)
- Application Components (employees, attendance, leaves, etc.)

---

## Core Tables (Primary Entities)

### 1. **employees**
Primary table for employee master data
```javascript
{
  id: "EMP001001",  // Primary key
  employeeId: "EMP001001",
  firstName: "John",
  lastName: "Smith",
  email: "john.smith@company.com",
  phone: "+1-555-0101",
  dateOfBirth: "1990-05-15",
  gender: "Male",
  ssn: "123-45-6789",
  address: {
    street: "123 Main St",
    city: "Tech City",
    state: "CA",
    zipCode: "90210",
    country: "USA"
  },
  departmentId: "DEPT_ENG_001",
  position: "Senior Software Engineer",
  employmentType: "full_time", // full_time, part_time, contract, temporary
  startDate: "2023-01-15",
  endDate: null,
  status: "active", // active, inactive, on_leave, probation, terminated
  salary: 95000.00,
  salaryGrade: "E4",
  reportingManagerId: "EMP001005",
  workLocation: "Floor 3",
  biometricId: "BIO001001",
  rfidCard: "RFID001001",
  emergencyContact: {
    name: "Jane Smith",
    relationship: "Spouse",
    phone: "+1-555-0102",
    email: "jane.smith@email.com"
  },
  benefits: {
    healthInsurance: true,
    dentalInsurance: true,
    retirement401k: true,
    vacationDays: 20,
    sickDays: 10
  },
  performanceRating: 4.2,
  role: "employee",
  createdAt: r.now(),
  updatedAt: r.now(),
  createdBy: "SYSTEM",
  updatedBy: "SYSTEM"
}
```
**Indexes**: 
- `id` (primary)
- `employeeId` (unique)
- `email` (unique)
- `status`
- `departmentId`

---

### 2. **departments**
Department organizational structure
```javascript
{
  id: "DEPT_ENG_001",
  departmentId: "DEPT_ENG_001",
  name: "Engineering",
  code: "ENG",
  description: "Software development and technical innovation",
  headId: "EMP001005",  // Link to employee
  capacity: 20,
  currentStaff: 15,
  budget: 1500000.00,
  location: "Floor 3",
  floor: 3,
  budgetCode: "ENG001",
  costCenter: "CC-ENG-001",
  establishedDate: "2020-01-15",
  status: "active",
  staffCount: {
    total: 15,
    active: 14,
    onLeave: 1,
    onDuty: 12,
    offDuty: 1,
    onBreak: 2,
    remoteWork: 0
  },
  positions: [
    {
      title: "Senior Software Engineer",
      count: 4,
      salaryRange: [90000, 120000]
    }
  ],
  annualBudget: 1500000,
  currentSpending: 1250000,
  budgetUtilization: 0.833,
  contact: {
    email: "engineering@company.com",
    phone: "+1-555-0301"
  },
  createdAt: r.now(),
  updatedAt: r.now()
}
```
**Indexes**:
- `id` (primary)
- `departmentId` (unique)
- `code` (unique)
- `status`

---

### 3. **leave_requests**
Employee leave/vacation requests
```javascript
{
  id: "LR2025001",
  requestId: "LR2025001",
  employeeId: "EMP001001",
  leaveType: "annual", // annual, sick, casual, maternity, paternity, unpaid
  startDate: "2025-02-10",
  endDate: "2025-02-14",
  numberOfDays: 5,
  reason: "Family vacation",
  status: "pending", // pending, approved, rejected, cancelled
  approverId: null,
  approvalDate: null,
  comments: null,
  attachmentUrls: [],
  createdAt: r.now(),
  updatedAt: r.now()
}
```
**Indexes**:
- `id` (primary)
- `requestId` (unique)
- `employeeId`
- `status`
- `startDate`

---

### 4. **attendance_records**
Daily employee attendance tracking
```javascript
{
  id: "ATT20250117001",
  attendanceId: "ATT20250117001",
  employeeId: "EMP001001",
  attendanceDate: "2025-01-17",
  checkInTime: "2025-01-17T09:00:00Z",
  checkOutTime: "2025-01-17T17:00:00Z",
  breakStart: "2025-01-17T12:00:00Z",
  breakEnd: "2025-01-17T13:00:00Z",
  hoursWorked: 7.0,
  status: "present", // present, absent, late, leave, holiday
  departmentId: "DEPT_ENG_001",
  remarks: "",
  isApproved: true,
  approvedBy: "EMP001005",
  approvalDate: "2025-01-17",
  location: "office", // office, remote, field
  createdAt: r.now()
}
```
**Indexes**:
- `id` (primary)
- `employeeId`
- `attendanceDate`
- `[employeeId, attendanceDate]` (compound)

---

### 5. **timesheets**
Weekly employee timesheets
```javascript
{
  id: "TS2025W03001",
  timesheetId: "TS2025W03001",
  employeeId: "EMP001001",
  weekStartDate: "2025-01-13",
  weekEndDate: "2025-01-19",
  totalHours: 40.0,
  days: [
    {
      date: "2025-01-13",
      dayOfWeek: "Monday",
      hoursWorked: 8.0,
      taskDescription: "Feature development",
      projectId: "PROJ001",
      status: "approved"
    }
  ],
  status: "submitted", // draft, submitted, approved, rejected
  approverId: "EMP001005",
  approvalDate: null,
  comments: "",
  createdAt: r.now(),
  updatedAt: r.now()
}
```
**Indexes**:
- `id` (primary)
- `employeeId`
- `weekStartDate`
- `status`

---

### 6. **transfer_requests**
Employee department/position transfer requests
```javascript
{
  id: "TR2025001",
  transferId: "TR2025001",
  employeeId: "EMP001001",
  currentDepartmentId: "DEPT_ENG_001",
  requestedDepartmentId: "DEPT_HR_001",
  requestedPosition: "HR Specialist",
  reason: "Career growth opportunity",
  eligibilityScore: 85.5,
  status: "pending", // pending, approved, rejected, transferred
  approverId: null,
  approvalDate: null,
  transferDate: null,
  comments: "",
  createdAt: r.now(),
  updatedAt: r.now()
}
```
**Indexes**:
- `id` (primary)
- `employeeId`
- `status`

---

### 7. **probation_records**
Employee probation period tracking
```javascript
{
  id: "PROB2025001",
  probationId: "PROB2025001",
  employeeId: "EMP001001",
  startDate: "2023-01-15",
  endDate: "2023-04-15",
  duration: "3 months", // 3 months, 6 months, 1 year
  performanceRating: 4.2,
  status: "completed", // active, completed, extended, failed
  reviews: [
    {
      reviewId: "REV001",
      reviewerId: "EMP001005",
      reviewDate: "2023-02-15",
      performanceScore: 4.0,
      attendance: 95.0,
      behavioralAssessment: "Excellent team player",
      technicalSkills: 4.5,
      teamwork: 4.0,
      communication: 4.0,
      comments: "Good progress",
      recommendation: "pass"
    }
  ],
  recommendations: "Confirm employment",
  comments: "",
  createdAt: r.now(),
  updatedAt: r.now()
}
```
**Indexes**:
- `id` (primary)
- `employeeId`
- `status`

---

### 8. **termination_records**
Employee termination records
```javascript
{
  id: "TERM2025001",
  terminationId: "TERM2025001",
  employeeId: "EMP001001",
  terminationType: "resignation", // resignation, dismissal, retirement, contract_end, death
  terminationDate: "2025-02-28",
  noticePeriod: 30,
  reason: "Personal reasons",
  exitInterview: {
    interviewDate: "2025-02-25",
    interviewer: "HR Manager",
    feedback: "Positive experience",
    wouldRehire: true
  },
  finalPayment: {
    salary: 7916.67,
    benefits: 1000.00,
    gratuity: 5000.00,
    total: 13916.67,
    paidDate: "2025-03-01"
  },
  status: "completed", // pending, completed, appealed
  documentUrls: [],
  createdAt: r.now(),
  updatedAt: r.now()
}
```
**Indexes**:
- `id` (primary)
- `employeeId`
- `status`

---

### 9. **assets**
Company asset inventory
```javascript
{
  id: "ASSET001",
  assetId: "ASSET001",
  name: "MacBook Pro 16\"",
  category: "it_equipment", // it_equipment, furniture, office_supplies, vehicles, machinery, other
  serialNumber: "C02XYZ12345",
  location: "Floor 3",
  assignedToId: "EMP001001",
  purchaseDate: "2023-01-01",
  purchaseCost: 2500.00,
  status: "active", // active, in_maintenance, retired, damaged, lost
  condition: "excellent", // excellent, good, fair, poor
  depreciationRate: 20.0,
  currentValue: 2000.00,
  qrCode: "QR_ASSET001",
  barcode: "BAR_ASSET001",
  attachmentUrls: [],
  createdAt: r.now(),
  updatedAt: r.now()
}
```
**Indexes**:
- `id` (primary)
- `assetId` (unique)
- `serialNumber` (unique)
- `assignedToId`
- `status`

---

### 10. **projects**
Company projects
```javascript
{
  id: "PROJ001",
  projectId: "PROJ001",
  name: "HRMS Development",
  description: "Enterprise HR Management System",
  startDate: "2023-01-01",
  endDate: "2023-12-31",
  status: "active", // planning, active, on_hold, completed, cancelled
  projectManagerId: "EMP001005",
  budget: 500000.00,
  teamIds: ["EMP001001", "EMP001002", "EMP001003"],
  createdAt: r.now(),
  updatedAt: r.now()
}
```
**Indexes**:
- `id` (primary)
- `projectId` (unique)
- `status`

---

### 11. **users**
System authentication users
```javascript
{
  id: "USER001",
  userId: "USER001",
  username: "john.smith",
  email: "john.smith@company.com",
  passwordHash: "$2b$10$...",
  employeeId: "EMP001001",
  role: "employee", // admin, manager, employee, hr, finance
  permissions: ["view_attendance", "request_leave"],
  isActive: true,
  lastLogin: "2025-01-17T09:00:00Z",
  loginAttempts: 0,
  isLocked: false,
  createdAt: r.now(),
  updatedAt: r.now()
}
```
**Indexes**:
- `id` (primary)
- `username` (unique)
- `email` (unique)
- `employeeId`

---

### 12. **documents**
File attachments and documents
```javascript
{
  id: "DOC001",
  documentId: "DOC001",
  documentType: "contract", // id, passport, contract, certificate, medical, other
  fileName: "employment_contract.pdf",
  fileUrl: "https://s3.us-east-005.backblazeb2.com/...",
  fileSize: 245678,
  mimeType: "application/pdf",
  uploadedBy: "USER001",
  relatedEmployeeId: "EMP001001",
  relatedAssetId: null,
  issuanceDate: "2023-01-15",
  expiryDate: null,
  isExpired: false,
  createdAt: r.now()
}
```
**Indexes**:
- `id` (primary)
- `documentId` (unique)
- `relatedEmployeeId`
- `documentType`

---

### 13. **holidays**
Company holidays and calendar
```javascript
{
  id: "HOL2025001",
  holidayId: "HOL2025001",
  name: "New Year's Day",
  date: "2025-01-01",
  type: "public", // public, company, optional
  isRecurring: true,
  description: "New Year holiday",
  appliesToDepartments: [], // Empty = all departments
  createdAt: r.now()
}
```
**Indexes**:
- `id` (primary)
- `date`

---

### 14. **audit_logs**
System audit trail
```javascript
{
  id: "LOG123456",
  logId: "LOG123456",
  userId: "USER001",
  action: "UPDATE",
  module: "employees",
  entityType: "Employee",
  entityId: "EMP001001",
  oldValues: {"status": "active"},
  newValues: {"status": "on_leave"},
  ipAddress: "192.168.1.100",
  userAgent: "Mozilla/5.0...",
  status: "success", // success, failure
  errorMessage: null,
  timestamp: r.now()
}
```
**Indexes**:
- `id` (primary)
- `userId`
- `timestamp`
- `[userId, timestamp]` (compound)

---

### 15. **institution_profile**
Organization information
```javascript
{
  id: "INST001",
  institutionId: "INST001",
  name: "Tech Corporation",
  abbreviation: "TECHCORP",
  type: "corporation", // corporation, ngo, government, educational, healthcare, other
  registrationNumber: "REG123456",
  taxId: "TAX789012",
  address: {
    street: "1000 Main Street",
    city: "Tech City",
    state: "CA",
    zipCode: "90001",
    country: "USA"
  },
  phoneNumber: "+1-555-0100",
  email: "info@techcorp.com",
  website: "https://techcorp.com",
  ceo: "Jane Doe",
  hroId: "EMP001006",
  establishedDate: "2000-01-01",
  totalEmployees: 150,
  totalDepartments: 10,
  financialYear: "2025",
  businessHours: {
    startTime: "09:00",
    endTime: "17:00",
    workDays: "Monday-Friday"
  },
  logoUrl: "https://...",
  policyUrls: [],
  createdAt: r.now(),
  updatedAt: r.now()
}
```
**Indexes**:
- `id` (primary)

---

### 16. **system_settings**
Application configuration
```javascript
{
  id: "settings",
  attendanceRules: {
    lateThresholdMinutes: 15,
    overtimeThresholdHours: 8,
    weeklyHoursLimit: 40
  },
  leaveRules: {
    annualLeaveAccrual: 20,
    sickLeaveAccrual: 10,
    carryOverLimit: 5
  },
  workingHours: {
    standardHours: 8,
    startTime: "09:00",
    endTime: "17:00",
    breakDuration: 60
  },
  updatedAt: r.now(),
  updatedBy: "ADMIN"
}
```

---

## RethinkDB Advantages for HRMS

1. **Real-time Updates**: Changefeeds for live attendance, notifications
2. **JSON Native**: Direct storage of complex nested structures
3. **Flexible Schema**: Easy to add new fields without migration
4. **Scalable**: Distributed architecture for growth
5. **Query Performance**: Efficient indexes and compound queries

---

## Migration Path from OrientDB to RethinkDB

1. Export OrientDB data as JSON
2. Transform link references to ID strings
3. Import into RethinkDB tables
4. Create indexes
5. Update application data access layer

---

## Next Steps

1. Create RethinkDB database initialization script
2. Write table creation with proper indexes
3. Create seed data for testing
4. Update application services to use RethinkDB
5. Test data operations and performance
