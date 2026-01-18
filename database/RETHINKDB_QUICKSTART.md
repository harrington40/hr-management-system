# Quick Start: RethinkDB Setup for HRMS

## Prerequisites Check

```bash
# Check if RethinkDB is installed
rethinkdb --version

# If not installed, install it:
# Ubuntu/Debian:
sudo apt-get install rethinkdb

# macOS:
brew install rethinkdb

# Docker:
docker run -d -P --name rethinkdb rethinkdb
```

## Installation Python Dependencies

```bash
pip install rethinkdb
```

## Setup Steps

### 1. Start RethinkDB Server

```bash
# Default setup
rethinkdb

# Or with specific data directory
rethinkdb --directory /path/to/data

# Or with Docker
docker start rethinkdb
```

**Access Admin UI**: http://localhost:8080

### 2. Initialize Database

```bash
cd /mnt/c/Users/harri/designProject2020/hr/database
python3 init_rethinkdb.py
```

**Expected Output:**
```
🚀 HRMS RethinkDB Database Initialization
============================================================
🔌 Connecting to RethinkDB server...
   Host: localhost:28015
✅ Connected to RethinkDB server successfully

📦 Creating database 'hrms'...
✅ Database 'hrms' created successfully

📊 Creating tables...
   ✅ Created table 'employees'
   ✅ Created table 'departments'
   ... (14 more tables)
📈 Summary: 16 created, 0 already existed

🔍 Creating indexes...
   ✅ Created index 'employeeId' on 'employees'
   ... (40+ more indexes)
📈 Summary: 40+ indexes created, 0 already existed

⏳ Waiting for indexes to be ready...
✅ All indexes are ready

🌱 Inserting sample data...
   ✅ Created institution profile
   ✅ Created sample department
   ✅ Created admin employee
   ✅ Created admin user
   ✅ Created system settings

🔍 Verifying database setup...
   ✅ Found 16 tables
   📊 employees: 1 records
   📊 departments: 1 records
   📊 users: 1 records

🎉 Database initialization completed successfully!
```

### 3. Run Tests

```bash
python3 test_rethinkdb.py
```

**Expected Output:**
```
🚀 RethinkDB Connection and Operations Test
============================================================
🔌 Testing RethinkDB Connection...
✅ Connected to RethinkDB

📦 Testing Database Existence...
✅ Database 'hrms' exists

📊 Testing Tables...
   ✅ employees: 1 records
   ✅ departments: 1 records
   ... (14 more tables)

🔍 Testing Indexes...
   ✅ employees.employeeId
   ✅ employees.email
   ... (40+ more indexes)

✏️  Testing CRUD Operations...
   ✅ Insert successful
   ✅ Read successful
   ✅ Update successful
   ✅ Delete successful

📊 Test Summary
============================================================
   ✅ PASS - Connection
   ✅ PASS - Database Exists
   ✅ PASS - Tables
   ✅ PASS - Indexes
   ✅ PASS - CRUD Operations
   ✅ PASS - Complex Queries
   ✅ PASS - Changefeeds

📈 Results: 7/7 tests passed
🎉 All tests passed!
```

## Verify Setup

### Check via Admin UI
1. Open http://localhost:8080
2. Click "Tables" tab
3. You should see 16 tables in 'hrms' database

### Check via Python
```python
import rethinkdb as r

# Connect
conn = r.connect('localhost', 28015, db='hrms')

# List tables
tables = r.table_list().run(conn)
print(f"Tables: {tables}")

# Count employees
employee_count = r.table('employees').count().run(conn)
print(f"Employees: {employee_count}")

# Get sample employee
employee = r.table('employees').limit(1).run(conn)
for emp in employee:
    print(f"Sample: {emp['firstName']} {emp['lastName']}")

conn.close()
```

## Default Credentials

**Admin User:**
- Username: `admin`
- Email: `admin@hrmkit.com`
- Employee ID: `EMP000001`
- Password: Set when integrating with authentication system

## Common Issues & Solutions

### Issue: Connection Refused
**Solution:** Make sure RethinkDB server is running
```bash
rethinkdb
```

### Issue: Database Already Exists
**Solution:** Script will skip creation if database exists. This is normal.

### Issue: Tables Already Exist
**Solution:** Script will skip creation if tables exist. This is safe.

### Issue: Permission Denied
**Solution:** Check RethinkDB user permissions
```bash
# Reset RethinkDB data directory
rm -rf rethinkdb_data
rethinkdb --directory rethinkdb_data
```

## Configuration

All settings are in `.env` file:

```env
RETHINKDB_HOST=localhost
RETHINKDB_PORT=28015
RETHINKDB_DATABASE=hrms
RETHINKDB_USER=admin
RETHINKDB_PASSWORD=
```

## Next Steps

1. ✅ Database is ready
2. Create RethinkDB service layer in application
3. Update components to use RethinkDB instead of YAML files
4. Enable real-time changefeeds for live updates
5. Configure backups

## Backup & Restore

### Backup
```bash
# Dump all data
rethinkdb dump -c localhost:28015 -e hrms -f hrms_backup.tar.gz
```

### Restore
```bash
# Restore from dump
rethinkdb restore hrms_backup.tar.gz -c localhost:28015
```

## Performance Tips

1. **Use Indexes**: Already created for common queries
2. **Use Changefeeds**: For real-time updates instead of polling
3. **Batch Operations**: Use `insert([...])` for multiple records
4. **Connection Pooling**: Reuse connections in production

## Documentation

- **Schema**: `database/RETHINKDB_SCHEMA.md`
- **Setup Summary**: `DATABASE_SETUP_SUMMARY.md`
- **RethinkDB Docs**: https://rethinkdb.com/docs/

## Support

For issues:
1. Check RethinkDB server status
2. Review logs: `rethinkdb --log-file rethinkdb.log`
3. Check admin UI: http://localhost:8080
4. Run test suite: `python3 test_rethinkdb.py`

---

**Status**: ✅ Ready for Integration
**Created**: January 17, 2026
