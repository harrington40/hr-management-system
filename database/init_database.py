#!/usr/bin/env python3
"""
HRMS OrientDB Database Initialization Script
Creates and initializes the OrientDB database for the HRMS application
"""

import os
import sys
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    import orientdb
    from orientdb.client import OrientDB
except ImportError:
    print("❌ Error: orientdb-python not installed")
    print("Install with: pip install orientdb-python")
    sys.exit(1)

def get_db_config():
    """Get database configuration from environment variables"""
    return {
        'host': os.getenv('ORIENTDB_HOST', 'localhost'),
        'port': int(os.getenv('ORIENTDB_PORT', 2424)),
        'user': os.getenv('ORIENTDB_USER', 'root'),
        'password': os.getenv('ORIENTDB_PASSWORD', 'root'),
        'database': os.getenv('ORIENTDB_DATABASE', 'hrms_db')
    }

def test_connection(config):
    """Test OrientDB server connection"""
    try:
        print("🔌 Testing OrientDB server connection...")
        client = OrientDB(host=config['host'], port=config['port'])
        client.connect(user=config['user'], password=config['password'])

        # Get server info
        info = client.get_server_info()
        print(f"✅ Connected to OrientDB Server version {info.get('version', 'unknown')}")

        client.close()
        return True, client

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False, None

def create_database_if_not_exists(client, config):
    """Create database if it doesn't exist"""
    try:
        print(f"📦 Checking if database '{config['database']}' exists...")

        # List existing databases
        databases = client.list_databases()

        if config['database'] in databases:
            print(f"✅ Database '{config['database']}' already exists")
            return True
        else:
            print(f"📦 Creating database '{config['database']}'...")

            # Create database
            client.create_database(
                name=config['database'],
                type='graph',
                storage='plocal'
            )

            print(f"✅ Database '{config['database']}' created successfully")
            return True

    except Exception as e:
        print(f"❌ Failed to create/check database: {e}")
        return False

def connect_to_database(client, config):
    """Connect to the specific database"""
    try:
        print(f"🔗 Connecting to database '{config['database']}'...")

        # Open database connection
        db = client.open_database(
            name=config['database'],
            user=config['user'],
            password=config['password']
        )

        print("✅ Connected to database successfully")
        return db

    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")
        return None

def execute_schema_file(db, schema_file):
    """Execute the OrientDB schema file"""
    try:
        print("📋 Executing schema file...")

        if not schema_file.exists():
            print(f"❌ Schema file not found: {schema_file}")
            return False

        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_content = f.read()

        # Split schema into individual commands (by semicolon)
        commands = [cmd.strip() for cmd in schema_content.split(';') if cmd.strip()]

        executed_count = 0
        for command in commands:
            if command and not command.startswith('--'):
                try:
                    # Execute command
                    result = db.command(command)
                    executed_count += 1

                    # Show progress for major commands
                    if any(keyword in command.upper() for keyword in ['CREATE CLASS', 'CREATE PROPERTY', 'INSERT INTO']):
                        print(f"   ✓ Executed: {command[:50]}...")

                except Exception as e:
                    # Some commands might fail if they already exist, continue
                    if "already exists" not in str(e).lower():
                        print(f"   ⚠️  Warning on command: {e}")
                        print(f"      Command: {command[:100]}...")

        print(f"✅ Executed {executed_count} schema commands")
        return True

    except Exception as e:
        print(f"❌ Failed to execute schema: {e}")
        return False

def verify_schema(db):
    """Verify that the schema was created correctly"""
    try:
        print("🔍 Verifying schema creation...")

        # Check if main classes exist
        required_classes = [
            'User', 'Employee', 'Department', 'Position',
            'ShiftTemplate', 'Schedule', 'AttendanceRecord',
            'LeaveType', 'LeaveRequest', 'LeaveBalance',
            'Institution', 'SystemSetting', 'AuditLog'
        ]

        missing_classes = []
        for class_name in required_classes:
            try:
                # Try to count records in the class
                result = db.query(f"SELECT COUNT(*) FROM {class_name}")
                count = result[0].get('COUNT', 0) if result else 0
                print(f"   ✓ Class '{class_name}': {count} records")
            except Exception:
                missing_classes.append(class_name)

        if missing_classes:
            print(f"❌ Missing classes: {missing_classes}")
            return False

        # Check edge classes
        edge_classes = ['WorksIn', 'ReportsTo', 'AssignedTo', 'Manages']
        for edge_name in edge_classes:
            try:
                result = db.query(f"SELECT COUNT(*) FROM {edge_name}")
                count = result[0].get('COUNT', 0) if result else 0
                print(f"   ✓ Edge '{edge_name}': {count} relationships")
            except Exception:
                print(f"   ⚠️  Edge '{edge_name}' not found or empty")

        print("✅ Schema verification completed")
        return True

    except Exception as e:
        print(f"❌ Schema verification failed: {e}")
        return False

def load_initial_data(db):
    """Ensure initial data is loaded"""
    try:
        print("📊 Checking initial data...")

        # Check admin user
        admin_users = db.query("SELECT FROM User WHERE email = 'admin@hrmkit.com'")
        if admin_users:
            print("   ✓ Admin user exists")
        else:
            print("   ⚠️  Admin user not found")

        # Check departments
        dept_count = db.query("SELECT COUNT(*) FROM Department")
        dept_num = dept_count[0].get('COUNT', 0) if dept_count else 0
        print(f"   ✓ {dept_num} departments")

        # Check leave types
        leave_count = db.query("SELECT COUNT(*) FROM LeaveType")
        leave_num = leave_count[0].get('COUNT', 0) if leave_count else 0
        print(f"   ✓ {leave_num} leave types")

        # Check shift templates
        shift_count = db.query("SELECT COUNT(*) FROM ShiftTemplate")
        shift_num = shift_count[0].get('COUNT', 0) if shift_count else 0
        print(f"   ✓ {shift_num} shift templates")

        print("✅ Initial data check completed")
        return True

    except Exception as e:
        print(f"❌ Initial data check failed: {e}")
        return False

def create_indexes(db):
    """Create additional indexes for performance"""
    try:
        print("🔍 Creating performance indexes...")

        # These should already be created by the schema, but let's verify
        indexes_created = 0

        # Check if indexes exist by trying to create them (they'll fail if they exist)
        index_commands = [
            "CREATE INDEX User.email UNIQUE",
            "CREATE INDEX Employee.employee_id UNIQUE",
            "CREATE INDEX Department.name UNIQUE",
            "CREATE INDEX Schedule.employee_date ON Schedule (employee_id, date) UNIQUE",
            "CREATE INDEX AttendanceRecord.employee_date ON AttendanceRecord (employee_id, date) UNIQUE",
            "CREATE INDEX LeaveBalance.employee_year ON LeaveBalance (employee_id, year)",
            "CREATE INDEX SystemSetting.key UNIQUE"
        ]

        for cmd in index_commands:
            try:
                db.command(cmd)
                indexes_created += 1
                print(f"   ✓ Created index: {cmd.split(' ')[2]}")
            except Exception as e:
                if "already exists" in str(e).lower():
                    print(f"   ✓ Index already exists: {cmd.split(' ')[2]}")
                else:
                    print(f"   ⚠️  Index creation warning: {e}")

        print(f"✅ Index creation completed ({indexes_created} new indexes)")
        return True

    except Exception as e:
        print(f"❌ Index creation failed: {e}")
        return False

def main():
    """Main initialization function"""
    print("🚀 HRMS OrientDB Database Initialization")
    print("=" * 50)

    # Get configuration
    config = get_db_config()
    print(f"📍 Target: {config['host']}:{config['port']}/{config['database']}")

    # Test connection
    connection_success, client = test_connection(config)
    if not connection_success:
        print("\n❌ Cannot proceed without OrientDB server connection")
        print("Please ensure OrientDB is running and credentials are correct")
        return False

    try:
        # Create database if needed
        if not create_database_if_not_exists(client, config):
            return False

        # Connect to database
        db = connect_to_database(client, config)
        if not db:
            return False

        # Execute schema
        schema_file = Path(__file__).parent / "hrms_schema.sql"
        if not execute_schema_file(db, schema_file):
            return False

        # Create indexes
        if not create_indexes(db):
            return False

        # Verify schema
        if not verify_schema(db):
            return False

        # Check initial data
        if not load_initial_data(db):
            return False

        print("\n" + "=" * 50)
        print("🎉 Database initialization completed successfully!")
        print("=" * 50)

        print("\n📋 Next steps:")
        print("   1. Update your application configuration to use OrientDB")
        print("   2. Set environment variables in .env file:")
        print("      ORIENTDB_HOST=localhost")
        print("      ORIENTDB_PORT=2424")
        print("      ORIENTDB_USER=root")
        print("      ORIENTDB_PASSWORD=your_password")
        print("      ORIENTDB_DATABASE=hrms_db")
        print("   3. Test your application with the new database")
        print("   4. Run the database test script: python3 test_database.py")

        print("\n🔐 Default login credentials:")
        print("   Email: admin@hrmkit.com")
        print("   Password: admin123")

        return True

    except Exception as e:
        print(f"\n❌ Initialization failed with error: {e}")
        return False

    finally:
        if 'client' in locals():
            try:
                client.close()
            except:
                pass

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

def get_db_config():
    """Get database configuration from environment or defaults"""
    return {
        'host': os.getenv('MYSQL_HOST', 'localhost'),
        'port': int(os.getenv('MYSQL_PORT', 3306)),
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', ''),
        'database': os.getenv('MYSQL_DATABASE', 'hrms_db'),
        'autocommit': True
    }

def create_database_if_not_exists(config):
    """Create database if it doesn't exist"""
    try:
        # Connect without specifying database
        temp_config = config.copy()
        del temp_config['database']

        connection = mysql.connector.connect(**temp_config)
        cursor = connection.cursor()

        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['database']} "
                      "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")

        print(f"✅ Database '{config['database']}' created or already exists")
        cursor.close()
        connection.close()
        return True

    except Error as e:
        print(f"❌ Error creating database: {e}")
        return False

def run_schema_script(config):
    """Execute the schema SQL script"""
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Read and execute schema file
        schema_path = Path(__file__).parent / 'hrms_schema.sql'
        with open(schema_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()

        # Split script into individual statements
        statements = []
        current_statement = []
        in_multiline_comment = False

        for line in sql_script.split('\n'):
            line = line.strip()

            # Skip empty lines and single-line comments
            if not line or line.startswith('--') or line.startswith('#'):
                continue

            # Handle multi-line comments
            if '/*' in line:
                in_multiline_comment = True
            if '*/' in line:
                in_multiline_comment = False
                continue
            if in_multiline_comment:
                continue

            # Handle statement delimiters
            if line.endswith(';'):
                current_statement.append(line[:-1])  # Remove semicolon
                statements.append(' '.join(current_statement))
                current_statement = []
            else:
                current_statement.append(line)

        # Execute each statement
        executed_count = 0
        for statement in statements:
            if statement.strip():
                try:
                    cursor.execute(statement)
                    executed_count += 1
                except Error as e:
                    print(f"⚠️  Warning executing statement: {e}")
                    print(f"   Statement: {statement[:100]}...")

        print(f"✅ Executed {executed_count} SQL statements successfully")
        cursor.close()
        connection.close()
        return True

    except Error as e:
        print(f"❌ Error executing schema: {e}")
        return False
    except FileNotFoundError:
        print("❌ Schema file 'hrms_schema.sql' not found")
        return False

def verify_database_setup(config):
    """Verify that the database was set up correctly"""
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Check if key tables exist
        tables_to_check = [
            'users', 'employees', 'departments', 'positions',
            'shift_templates', 'attendance_records', 'leave_requests'
        ]

        print("\n🔍 Verifying database setup:")
        for table in tables_to_check:
            cursor.execute(f"SHOW TABLES LIKE '{table}'")
            if cursor.fetchone():
                print(f"   ✅ Table '{table}' exists")
            else:
                print(f"   ❌ Table '{table}' missing")

        # Check initial data
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"   📊 Users: {user_count}")

        cursor.execute("SELECT COUNT(*) FROM departments")
        dept_count = cursor.fetchone()[0]
        print(f"   📊 Departments: {dept_count}")

        cursor.execute("SELECT COUNT(*) FROM leave_types")
        leave_count = cursor.fetchone()[0]
        print(f"   📊 Leave Types: {leave_count}")

        cursor.close()
        connection.close()
        return True

    except Error as e:
        print(f"❌ Error verifying database: {e}")
        return False

def main():
    """Main initialization function"""
    print("🚀 HRMS Database Initialization")
    print("=" * 40)

    # Get database configuration
    config = get_db_config()
    print(f"📍 Target Database: {config['host']}:{config['port']}/{config['database']}")

    # Step 1: Create database
    print("\n📁 Step 1: Creating database...")
    if not create_database_if_not_exists(config):
        print("❌ Failed to create database. Exiting.")
        sys.exit(1)

    # Step 2: Run schema
    print("\n🛠️  Step 2: Executing schema...")
    if not run_schema_script(config):
        print("❌ Failed to execute schema. Exiting.")
        sys.exit(1)

    # Step 3: Verify setup
    print("\n✅ Step 3: Verifying setup...")
    if verify_database_setup(config):
        print("\n🎉 Database initialization completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Update your application configuration with database credentials")
        print("   2. Test database connection in your application")
        print("   3. Run any additional data migrations if needed")
        print("   4. Set up automated backups")
        print("\n🔐 Default admin credentials:")
        print("   Email: admin@hrmkit.com")
        print("   Password: admin123 (change immediately in production!)")
    else:
        print("❌ Database verification failed. Please check the setup.")
        sys.exit(1)

if __name__ == "__main__":
    main()