# HRMS Database Setup Guide

This directory contains the complete database schema and setup scripts for the Human Resource Management System (HRMS).

## 📁 Directory Structure

```
database/
├── data_flow_map.md      # Comprehensive data architecture documentation
├── hrms_schema.sql       # Complete MySQL database schema
├── init_database.py      # Python script for automated database setup
├── test_database.py      # Database connectivity and integrity tests
├── .env.example          # Environment configuration template
└── README.md            # This file
```

## 🚀 Quick Start

### Prerequisites

- MySQL 8.0 or higher
- Python 3.8+ (for automated setup)
- MySQL Connector/Python (`pip install mysql-connector-python`)

### Environment Variables

Set the following environment variables or update the defaults in `init_database.py`:

```bash
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_DATABASE=hrms_db
```

### Configuration File

Copy `.env.example` to `.env` and update with your database credentials:

```bash
cp .env.example .env
# Edit .env with your actual values
```

### Automated Setup

1. **Navigate to the database directory:**
   ```bash
   cd /mnt/c/Users/harri/designProject2020/hr-clock/hrms-main/database
   ```

2. **Run the initialization script:**
   ```bash
   python3 init_database.py
   ```

3. **Follow the on-screen instructions**

The script will:
- ✅ Create the database if it doesn't exist
- ✅ Execute the complete schema
- ✅ Insert initial data (departments, leave types, shifts, admin user)
- ✅ Verify the setup
- ✅ Provide next steps

### Testing the Setup

After setup, run the test script to verify everything is working:

```bash
python3 test_database.py
```

The test script will:
- ✅ Verify database connectivity
- ✅ Test basic queries
- ✅ Check data integrity
- ✅ Measure performance metrics

## 📋 Manual Setup

If you prefer manual setup:

1. **Create the database:**
   ```sql
   CREATE DATABASE hrms_db
       CHARACTER SET utf8mb4
       COLLATE utf8mb4_unicode_ci;
   ```

2. **Execute the schema:**
   ```bash
   mysql -u root -p hrms_db < hrms_schema.sql
   ```

## 🏗️ Database Architecture

### Core Entities

1. **Users & Authentication**
   - User accounts with role-based access
   - JWT session management
   - Password hashing and security

2. **Employee Management**
   - Employee profiles with comprehensive details
   - Department and position hierarchies
   - Manager relationships

3. **Shift & Timetable Management**
   - Flexible shift templates
   - Daily shift assignments
   - Weekly schedule templates

4. **Attendance & Time Tracking**
   - Clock in/out records
   - Leave requests and approvals
   - Time-off balances

5. **Organization Structure**
   - Institution profile
   - Departments and positions
   - Business rules and policies

6. **Reporting & Analytics**
   - Coverage analysis
   - Performance metrics
   - Comprehensive audit logging

### Key Features

- **Normalized Design**: 3NF compliance for data integrity
- **Performance Optimized**: Strategic indexing and partitioning
- **Security Focused**: Row-level security, encryption, audit trails
- **Scalable**: Connection pooling, read replicas support
- **Comprehensive**: Covers all HRMS functional areas

## 📊 Data Flow

See `data_flow_map.md` for detailed data flow diagrams and entity relationships.

### Main Data Flows

1. **Employee Onboarding**: User creation → Profile setup → Department assignment → Initial balances
2. **Daily Operations**: Clock in/out → Attendance recording → Schedule management
3. **Leave Management**: Request submission → Approval workflow → Balance updates
4. **Reporting**: Data aggregation → Analytics generation → Dashboard display

## 🔧 Configuration

### Connection Pooling

The database is configured for connection pooling. Update your application config:

```python
# In your application configuration
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'your_user',
    'password': 'your_password',
    'database': 'hrms_db',
    'pool_name': 'hrms_pool',
    'pool_size': 5,
    'autocommit': True
}
```

### Backup Strategy

1. **Daily Backups**: Automated full backups
2. **Transaction Logs**: Point-in-time recovery
3. **Encrypted Storage**: Secure backup storage
4. **Regular Testing**: Backup restoration validation

## 🔒 Security Considerations

### Data Protection
- Sensitive data encryption (salaries, PII)
- Parameterized queries to prevent SQL injection
- Row-level security for multi-tenant scenarios

### Access Control
- Role-based permissions
- Audit logging for all changes
- Secure password policies

### Compliance
- GDPR compliance for EU data
- Regular security audits
- Data retention policies

## 📈 Performance Optimization

### Indexing Strategy
- Primary keys on all tables
- Foreign key constraints with indexes
- Composite indexes for common queries
- Full-text indexes for searchable fields

### Partitioning
- Attendance records partitioned by month
- Historical data archiving
- Query optimization for large datasets

### Monitoring
- Query performance monitoring
- Connection pool utilization
- Disk space and growth tracking

## 🧪 Testing

### Database Test Suite

Run comprehensive tests to verify your database setup:

```bash
python3 test_database.py
```

The test suite includes:
- **Connection Test**: Verifies database connectivity
- **Basic Queries Test**: Tests core data retrieval
- **Data Integrity Test**: Checks referential constraints
- **Performance Test**: Measures query execution times

### Initial Data
The schema includes initial test data:
- Default admin user: `admin@hrmkit.com` / `admin123`
- Sample departments and positions
- Standard leave types and shift templates

### Data Validation
- Foreign key constraints
- Check constraints on data ranges
- Trigger-based audit logging

## 🚀 Production Deployment

### Pre-deployment Checklist
- [ ] Update database credentials
- [ ] Configure backup schedules
- [ ] Set up monitoring and alerting
- [ ] Review security settings
- [ ] Test backup restoration
- [ ] Configure connection pooling

### Migration Strategy
1. Set up staging environment
2. Run schema on staging
3. Migrate test data
4. Perform thorough testing
5. Schedule production deployment
6. Monitor post-deployment

## 📞 Support

For database-related issues:
1. Check the `data_flow_map.md` for entity relationships
2. Review the schema comments for table purposes
3. Examine the audit logs for data change tracking
4. Contact the development team for complex issues

## 📝 Change Log

### Version 1.0
- Initial database schema creation
- Complete HRMS data model
- Automated setup scripts
- Comprehensive documentation