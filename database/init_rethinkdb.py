#!/usr/bin/env python3
"""
HRMS RethinkDB Database Initialization Script
Creates database, tables, and indexes for the HRMS application
"""

from rethinkdb import RethinkDB
from rethinkdb.errors import ReqlDriverError, ReqlRuntimeError
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

# Initialize RethinkDB
r = RethinkDB()

# Configuration
DB_CONFIG = {
    'host': os.getenv('RETHINKDB_HOST', 'localhost'),
    'port': int(os.getenv('RETHINKDB_PORT', 28015)),
    'db': os.getenv('RETHINKDB_DATABASE', 'hrms'),
    'user': os.getenv('RETHINKDB_USER', 'admin'),
    'password': os.getenv('RETHINKDB_PASSWORD', '')
}

# Define all tables and their indexes
TABLES_CONFIG = {
    'employees': {
        'primary_key': 'id',
        'indexes': ['employeeId', 'email', 'status', 'departmentId']
    },
    'departments': {
        'primary_key': 'id',
        'indexes': ['departmentId', 'code', 'status']
    },
    'leave_requests': {
        'primary_key': 'id',
        'indexes': ['requestId', 'employeeId', 'status', 'startDate']
    },
    'attendance_records': {
        'primary_key': 'id',
        'indexes': ['employeeId', 'attendanceDate', ['employeeId', 'attendanceDate']]
    },
    'timesheets': {
        'primary_key': 'id',
        'indexes': ['employeeId', 'weekStartDate', 'status']
    },
    'transfer_requests': {
        'primary_key': 'id',
        'indexes': ['employeeId', 'status']
    },
    'probation_records': {
        'primary_key': 'id',
        'indexes': ['employeeId', 'status']
    },
    'termination_records': {
        'primary_key': 'id',
        'indexes': ['employeeId', 'status']
    },
    'assets': {
        'primary_key': 'id',
        'indexes': ['assetId', 'serialNumber', 'assignedToId', 'status']
    },
    'projects': {
        'primary_key': 'id',
        'indexes': ['projectId', 'status']
    },
    'users': {
        'primary_key': 'id',
        'indexes': ['username', 'email', 'employeeId']
    },
    'documents': {
        'primary_key': 'id',
        'indexes': ['documentId', 'relatedEmployeeId', 'documentType']
    },
    'holidays': {
        'primary_key': 'id',
        'indexes': ['date']
    },
    'audit_logs': {
        'primary_key': 'id',
        'indexes': ['userId', 'timestamp', ['userId', 'timestamp']]
    },
    'institution_profile': {
        'primary_key': 'id',
        'indexes': []
    },
    'system_settings': {
        'primary_key': 'id',
        'indexes': []
    }
}


def connect_to_server():
    """Connect to RethinkDB server"""
    try:
        print("🔌 Connecting to RethinkDB server...")
        print(f"   Host: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
        
        conn = r.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG.get('user'),
            password=DB_CONFIG.get('password')
        )
        
        print("✅ Connected to RethinkDB server successfully")
        return conn
    
    except ReqlDriverError as e:
        print(f"❌ Connection failed: {e}")
        print("\nPlease ensure:")
        print("  1. RethinkDB server is running")
        print("  2. Host and port are correct")
        print("  3. Network connectivity is available")
        return None


def create_database(conn):
    """Create database if it doesn't exist"""
    try:
        print(f"\n📦 Creating database '{DB_CONFIG['db']}'...")
        
        # Check if database exists
        existing_dbs = r.db_list().run(conn)
        
        if DB_CONFIG['db'] in existing_dbs:
            print(f"   ℹ️  Database '{DB_CONFIG['db']}' already exists")
            return True
        
        # Create database
        r.db_create(DB_CONFIG['db']).run(conn)
        print(f"✅ Database '{DB_CONFIG['db']}' created successfully")
        return True
    
    except ReqlRuntimeError as e:
        print(f"❌ Database creation failed: {e}")
        return False


def create_tables(conn):
    """Create all tables"""
    try:
        print(f"\n📊 Creating tables...")
        
        # Get existing tables
        existing_tables = r.db(DB_CONFIG['db']).table_list().run(conn)
        
        created_count = 0
        skipped_count = 0
        
        for table_name, config in TABLES_CONFIG.items():
            if table_name in existing_tables:
                print(f"   ⏭️  Table '{table_name}' already exists")
                skipped_count += 1
                continue
            
            # Create table
            r.db(DB_CONFIG['db']).table_create(
                table_name,
                primary_key=config.get('primary_key', 'id')
            ).run(conn)
            
            print(f"   ✅ Created table '{table_name}'")
            created_count += 1
        
        print(f"\n📈 Summary: {created_count} created, {skipped_count} already existed")
        return True
    
    except ReqlRuntimeError as e:
        print(f"❌ Table creation failed: {e}")
        return False


def create_indexes(conn):
    """Create indexes for all tables"""
    try:
        print(f"\n🔍 Creating indexes...")
        
        created_count = 0
        skipped_count = 0
        
        for table_name, config in TABLES_CONFIG.items():
            indexes = config.get('indexes', [])
            
            if not indexes:
                continue
            
            # Get existing indexes for this table
            existing_indexes = r.db(DB_CONFIG['db']).table(table_name).index_list().run(conn)
            
            for index in indexes:
                # Handle compound indexes (tuple/list)
                if isinstance(index, (list, tuple)):
                    index_name = '_'.join(index)
                    
                    if index_name in existing_indexes:
                        skipped_count += 1
                        continue
                    
                    # Create compound index
                    r.db(DB_CONFIG['db']).table(table_name).index_create(
                        index_name,
                        lambda doc: [doc[field] for field in index]
                    ).run(conn)
                    
                    print(f"   ✅ Created compound index '{index_name}' on '{table_name}'")
                    created_count += 1
                
                else:
                    # Simple index
                    if index in existing_indexes:
                        skipped_count += 1
                        continue
                    
                    r.db(DB_CONFIG['db']).table(table_name).index_create(index).run(conn)
                    print(f"   ✅ Created index '{index}' on '{table_name}'")
                    created_count += 1
        
        print(f"\n📈 Summary: {created_count} indexes created, {skipped_count} already existed")
        
        # Wait for indexes to be ready
        print("\n⏳ Waiting for indexes to be ready...")
        for table_name in TABLES_CONFIG.keys():
            r.db(DB_CONFIG['db']).table(table_name).index_wait().run(conn)
        
        print("✅ All indexes are ready")
        return True
    
    except ReqlRuntimeError as e:
        print(f"❌ Index creation failed: {e}")
        return False


def insert_sample_data(conn):
    """Insert sample/seed data for testing"""
    try:
        print(f"\n🌱 Inserting sample data...")
        
        # Check if data already exists
        employee_count = r.db(DB_CONFIG['db']).table('employees').count().run(conn)
        
        if employee_count > 0:
            print(f"   ℹ️  Sample data already exists ({employee_count} employees)")
            return True
        
        # Sample institution profile
        institution = {
            'id': 'INST001',
            'institutionId': 'INST001',
            'name': 'Tech Corporation',
            'abbreviation': 'TECHCORP',
            'type': 'corporation',
            'email': 'info@techcorp.com',
            'establishedDate': r.expr('2000-01-01'),
            'totalEmployees': 0,
            'totalDepartments': 0,
            'createdAt': r.now(),
            'updatedAt': r.now()
        }
        
        r.db(DB_CONFIG['db']).table('institution_profile').insert(institution).run(conn)
        print("   ✅ Created institution profile")
        
        # Sample department
        department = {
            'id': 'DEPT_ENG_001',
            'departmentId': 'DEPT_ENG_001',
            'name': 'Engineering',
            'code': 'ENG',
            'description': 'Software development and technical innovation',
            'capacity': 20,
            'currentStaff': 0,
            'status': 'active',
            'createdAt': r.now(),
            'updatedAt': r.now()
        }
        
        r.db(DB_CONFIG['db']).table('departments').insert(department).run(conn)
        print("   ✅ Created sample department")
        
        # Sample admin user
        admin_employee = {
            'id': 'EMP000001',
            'employeeId': 'EMP000001',
            'firstName': 'Admin',
            'lastName': 'User',
            'email': 'admin@hrmkit.com',
            'phone': '+1-555-0001',
            'departmentId': 'DEPT_ENG_001',
            'position': 'System Administrator',
            'employmentType': 'full_time',
            'startDate': r.expr('2023-01-01'),
            'status': 'active',
            'role': 'admin',
            'createdAt': r.now(),
            'updatedAt': r.now()
        }
        
        r.db(DB_CONFIG['db']).table('employees').insert(admin_employee).run(conn)
        print("   ✅ Created admin employee")
        
        # Sample system user
        admin_user = {
            'id': 'USER000001',
            'userId': 'USER000001',
            'username': 'admin',
            'email': 'admin@hrmkit.com',
            'passwordHash': '$2b$10$dummyhashfordev',  # Should be properly hashed in production
            'employeeId': 'EMP000001',
            'role': 'admin',
            'permissions': ['*'],
            'isActive': True,
            'loginAttempts': 0,
            'isLocked': False,
            'createdAt': r.now(),
            'updatedAt': r.now()
        }
        
        r.db(DB_CONFIG['db']).table('users').insert(admin_user).run(conn)
        print("   ✅ Created admin user")
        
        # Sample system settings
        settings = {
            'id': 'settings',
            'attendanceRules': {
                'lateThresholdMinutes': 15,
                'overtimeThresholdHours': 8,
                'weeklyHoursLimit': 40
            },
            'leaveRules': {
                'annualLeaveAccrual': 20,
                'sickLeaveAccrual': 10,
                'carryOverLimit': 5
            },
            'workingHours': {
                'standardHours': 8,
                'startTime': '09:00',
                'endTime': '17:00',
                'breakDuration': 60
            },
            'updatedAt': r.now(),
            'updatedBy': 'SYSTEM'
        }
        
        r.db(DB_CONFIG['db']).table('system_settings').insert(settings).run(conn)
        print("   ✅ Created system settings")
        
        print("\n✅ Sample data inserted successfully")
        return True
    
    except ReqlRuntimeError as e:
        print(f"❌ Sample data insertion failed: {e}")
        return False


def verify_setup(conn):
    """Verify the database setup"""
    try:
        print(f"\n🔍 Verifying database setup...")
        
        # Check tables
        tables = r.db(DB_CONFIG['db']).table_list().run(conn)
        print(f"   ✅ Found {len(tables)} tables")
        
        # Check counts
        for table_name in ['employees', 'departments', 'users']:
            count = r.db(DB_CONFIG['db']).table(table_name).count().run(conn)
            print(f"   📊 {table_name}: {count} records")
        
        print("\n✅ Database setup verified successfully")
        return True
    
    except ReqlRuntimeError as e:
        print(f"❌ Verification failed: {e}")
        return False


def main():
    """Main initialization function"""
    print("🚀 HRMS RethinkDB Database Initialization")
    print("=" * 60)
    
    # Connect to server
    conn = connect_to_server()
    if not conn:
        print("\n❌ Failed to connect to RethinkDB server")
        return False
    
    try:
        # Create database
        if not create_database(conn):
            return False
        
        # Create tables
        if not create_tables(conn):
            return False
        
        # Create indexes
        if not create_indexes(conn):
            return False
        
        # Insert sample data
        if not insert_sample_data(conn):
            return False
        
        # Verify setup
        if not verify_setup(conn):
            return False
        
        print("\n" + "=" * 60)
        print("🎉 Database initialization completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Access RethinkDB admin UI: http://localhost:8080")
        print("   2. Update application config to use RethinkDB")
        print("   3. Test HRMS application with new database")
        print(f"   4. Default admin: admin@hrmkit.com")
        print("\n" + "=" * 60)
        
        return True
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False
    
    finally:
        conn.close()
        print("\n🔌 Connection closed")


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
