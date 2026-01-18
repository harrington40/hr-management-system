from services.rethinkdb_service import rethinkdb_service
from services.auth_service import AuthService

# Connect to database
if rethinkdb_service.connect():
    auth_service = AuthService(rethinkdb_service)
    
    # Create test users
    test_users = [
        {
            "username": "admin",
            "email": "admin@hrmkit.com",
            "password": "admin123",
            "role": "admin",
            "is_active": True
        },
        {
            "username": "manager", 
            "email": "manager@hrmkit.com",
            "password": "manager123",
            "role": "manager",
            "is_active": True
        },
        {
            "username": "employee",
            "email": "employee@hrmkit.com", 
            "password": "employee123",
            "role": "employee",
            "is_active": True
        }
    ]
    
    for user in test_users:
        # Hash password
        hashed = auth_service.hash_password(user["password"])
        user_data = {
            "id": user["username"],
            "username": user["username"],
            "email": user["email"],
            "password_hash": hashed,
            "role": user["role"],
            "is_active": user["is_active"]
        }
        
        try:
            # Insert user
            result = rethinkdb_service.r.table("users").insert(user_data, conflict="replace").run(rethinkdb_service.get_connection())
            print(f"Created user: {user['username']} - {result}")
        except Exception as e:
            print(f"Error creating user {user['username']}: {e}")
    
    print("Test users created successfully!")
else:
    print("Failed to connect to database")
