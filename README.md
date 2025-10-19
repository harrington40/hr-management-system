# HR Management System (HRMS)

A modern, scalable HR management system built with FastAPI, NiceGUI, and integrated with MQTT, Backblaze B2, gRPC, and **OrientDB** for enterprise-grade workforce management using multi-model database architecture.

## 🚀 Features

### Core HR Management
- **Employee Management**: Complete employee lifecycle management
- **Attendance Tracking**: Real-time attendance with AI-powered insights
- **Leave Management**: Sophisticated vacation and leave policy management
- **Document Management**: Secure document storage and retrieval

### Technology Integration
- **Real-time Communication**: MQTT for live updates and notifications
- **Large File Storage**: Backblaze B2 integration for document storage
- **High-Performance APIs**: gRPC for efficient service communication
- **Multi-Model Database**: OrientDB combining document, graph, and key-value models

### Modern Dashboard
- **Responsive Design**: Modern UI with Tailwind CSS
- **Real-time Analytics**: Live workforce metrics and insights
- **Hardware Integration**: Biometric device and access control support
- **Mobile Friendly**: Responsive design for all devices

### Security & Performance
- **SSL/TLS Encryption**: Secure database connections with certificate verification
- **Connection Pooling**: Optimized database performance
- **Environment Security**: Secure credential management
- **Audit Logging**: Comprehensive security and access logging

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **NiceGUI**: Python-based web framework for interactive UIs
- **OrientDB**: Multi-model NoSQL database (Document + Graph + Key-Value)
- **MQTT**: Real-time messaging protocol
- **gRPC**: High-performance RPC framework
- **Backblaze B2**: Cloud object storage for files

### Frontend
- **Vue.js**: Progressive JavaScript framework
- **Tailwind CSS**: Utility-first CSS framework
- **WebSockets**: Real-time bidirectional communication

## 📋 Prerequisites

- Python 3.8+
- **OrientDB Server** (Remote or Local)
- MQTT Broker (optional, e.g., Mosquitto)
- Backblaze B2 Account (optional)

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone <repository-url>
cd hrms-main

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration
Create a `.env` file in the root directory:
```env
# OrientDB Configuration (Required)
ORIENTDB_HOST=orientdb.transtechologies.com
ORIENTDB_PORT=2424
ORIENTDB_USER=root
ORIENTDB_PASSWORD=your_password
ORIENTDB_DATABASE=hrms

# MQTT Configuration (Optional)
MQTT_BROKER_HOST=localhost
MQTT_BROKER_PORT=1883
MQTT_USERNAME=your_username
MQTT_PASSWORD=your_password

# Backblaze B2 Configuration (Optional)
B2_APPLICATION_KEY_ID=your_key_id
B2_APPLICATION_KEY=your_application_key
B2_BUCKET_NAME=hrms-documents

# gRPC Configuration (Optional)
GRPC_HOST=localhost
GRPC_PORT=50051

# Application Configuration
SECRET_KEY=your-secret-key
JWT_TOKEN_KEY=your-jwt-key
APP_ORIGIN=http://127.0.0.1:8081
```

### 3. Database Setup
```bash
# Initialize database schema and sample data
python3 database/init_database_rest.py

# Verify database setup
python3 database/verify_schema.py

# Test secure connection
python3 database/secure_connection_example.py
```

### 4. Start the Application
```bash
# Development mode
uvicorn main:app --host 0.0.0.0 --port 8081 --reload

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8081 --workers 4
```

### 5. Access the Application
- **Web Interface**: http://localhost:8081/hrmkit
- **API Health Check**: http://localhost:8081/health
- **Default Admin**: `admin@hrmkit.com` / `admin123`

## 📁 Project Structure

```
hrms-main/
├── config/                 # Configuration management
│   └── services.py        # Service configuration with OrientDB
├── services/              # Core services
│   ├── mqtt_service.py    # MQTT communication
│   ├── backblaze_service.py # Backblaze B2 integration
│   ├── grpc_service.py    # gRPC services
│   ├── database_service.py # MySQL service (legacy)
│   └── service_manager.py # Service coordination
├── components/            # UI components
│   ├── dashboard/         # Dashboard components
│   ├── administration/    # Admin components
│   └── attendance/        # Attendance components
├── apis/                  # API endpoints
│   ├── db.py             # OrientDB connection management
│   ├── userModel.py      # User model definitions
│   └── database_service.py # OrientDB service layer
├── database/              # Database scripts and schema
│   ├── hrms_schema.sql   # Complete OrientDB schema
│   ├── init_database_rest.py # REST API database setup
│   ├── verify_schema.py  # Schema verification
│   ├── secure_connection_example.py # Security example
│   └── test_rest_connection.py # Connection testing
├── assets/                # Static assets
├── helperFuns/            # Utility functions
├── layout/                # Layout components
├── main.py               # Application entry point
├── frontend.py           # Frontend initialization
├── SECURITY_GUIDE.md     # Security documentation
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🗄️ OrientDB Multi-Model Architecture

The HRMS uses OrientDB's powerful multi-model database combining document, graph, and key-value capabilities for enterprise-grade data management:

### Multi-Model Features
- **Document Model**: Schema-flexible documents with rich querying
- **Graph Model**: Relationships and traversals for organizational hierarchies
- **Key-Value Model**: Fast lookups for frequently accessed data
- **SQL-like Queries**: Extended SQL with graph traversal capabilities

### Database Components
```
database/
├── hrms_schema.sql       # Complete OrientDB schema with vertex/edge classes
├── init_database_rest.py # REST API database setup with SSL security
├── verify_schema.py      # Schema verification with secure connections
├── secure_connection_example.py # SSL/TLS security demonstration
├── test_rest_connection.py # Connection testing utilities
└── .env                  # Environment configuration
```

### Vertex Classes (Entities)
- **User**: Authentication and basic user information
- **Employee**: Extended user profiles with employment details
- **Department**: Organizational structure and hierarchy
- **Position**: Job roles and responsibilities
- **Schedule**: Work schedules and shift management
- **AttendanceRecord**: Time tracking and presence data
- **LeaveRequest**: Vacation and leave management
- **LeaveType**: Different types of leave policies
- **Institution**: Organization information
- **SystemSetting**: Application configuration

### Edge Classes (Relationships)
- **WorksIn**: Employee-department relationships
- **ReportsTo**: Organizational reporting hierarchy
- **Manages**: Department management relationships
- **AssignedTo**: Position assignments
- **WorksIn**: Employee-department associations

### Embedded Classes
- **OAddress**: Address information
- **OContact**: Contact details
- **OCertification**: Certification records
- **ORange**: Salary ranges

### Integration
The `apis/db.py` provides a clean Python interface for all OrientDB operations:
- REST API communication with SSL/TLS security
- Document operations (CRUD) for all vertex types
- Graph traversals for relationship queries
- SQL-like queries with graph extensions
- Connection pooling and error handling

### Security Features
- **SSL/TLS Encryption**: All connections use HTTPS with certificate verification
- **HTTP Basic Authentication**: Secure credential transmission
- **Request Timeouts**: Protection against hanging connections
- **Retry Logic**: Automatic retry for transient network issues
- **Environment Variables**: Secure credential storage

See `database/secure_connection_example.py` for examples of secure OrientDB integration.

## 🔧 Service Architecture

### OrientDB Service
- **Multi-model database operations** with SSL/TLS security
- **Document CRUD** with schema flexibility
- **Graph traversals** for complex relationship queries
- **REST API integration** with connection pooling
- **Secure authentication** over HTTPS
- **Performance optimization** with retry logic and timeouts

### MQTT Service (Optional)
- Real-time messaging for live updates
- Topic-based publish/subscribe
- Automatic reconnection and error handling

### Backblaze B2 Service (Optional)
- Cloud storage for large files
- Document management with metadata
- Secure file upload/download

### gRPC Service (Optional)
- High-performance service communication
- Protocol buffers for efficient serialization
- Service discovery and registration

## 🎯 API Endpoints

### Health Check
- `GET /health` - Service status and health monitoring

### Dashboard
- `GET /dashboard` - Modern dashboard interface
- `GET /menu-integration` - Integrated menu system

### Administration
- `GET /administration/institution` - Institution profile
- `GET /administration/enroll-staff` - Staff enrollment
- `GET /administration/departments` - Department management

## 🔒 Security Features

- Environment-based configuration
- Secure credential management
- OrientDB connection pooling
- Input validation and sanitization
- Graph-based access control

## 📊 Monitoring

- Service health monitoring
- Real-time system metrics
- Error logging and tracking
- Performance monitoring
- OrientDB query performance metrics

## 🚀 Deployment

### Development
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the code examples

## 🔄 Recent Updates

### Version 2.2.0 - OrientDB Migration
- **Migrated from MySQL to OrientDB**: Complete multi-model database migration
- **Enhanced Data Architecture**: Document, graph, and key-value model integration
- **Improved Relationship Management**: Graph-based organizational hierarchies
- **Flexible Schema Design**: Schema-less documents with embedded classes
- **Advanced Querying**: SQL-like queries with graph traversal capabilities
- **Performance Optimization**: Connection pooling and query optimization
- **Comprehensive Testing**: Updated test suite for OrientDB operations
- **Integration Examples**: Complete examples for component integration

---

**Built with ❤️ for modern HR management using OrientDB's multi-model architecture**

## 🚀 Features

### Core HR Management
- **Employee Management**: Complete employee lifecycle management
- **Attendance Tracking**: Real-time attendance with AI-powered insights
- **Leave Management**: Sophisticated vacation and leave policy management
- **Document Management**: Secure document storage and retrieval

### Technology Integration
- **Real-time Communication**: MQTT for live updates and notifications
- **Large File Storage**: Backblaze B2 integration for document storage
- **High-Performance APIs**: gRPC for efficient service communication
- **Multi-Model Database**: OrientDB combining document, graph, and key-value models

### Modern Dashboard
- **Responsive Design**: Modern UI with Tailwind CSS
- **Real-time Analytics**: Live workforce metrics and insights
- **Hardware Integration**: Biometric device and access control support
- **Mobile Friendly**: Responsive design for all devices

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **NiceGUI**: Python-based web framework for interactive UIs
- **OrientDB**: Multi-model NoSQL database (Document + Graph + Key-Value)
- **MQTT**: Real-time messaging protocol
- **gRPC**: High-performance RPC framework
- **Backblaze B2**: Cloud object storage for files

### Frontend
- **Vue.js**: Progressive JavaScript framework
- **Tailwind CSS**: Utility-first CSS framework
- **WebSockets**: Real-time bidirectional communication

## 📋 Prerequisites

- Python 3.8+
- **OrientDB 3.2+** (Community or Enterprise Edition)
- MQTT Broker (e.g., Mosquitto)
- Backblaze B2 Account (optional)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hrms-main
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory:
   ```env
   # MQTT Configuration
   MQTT_BROKER_HOST=localhost
   MQTT_BROKER_PORT=1883
   MQTT_USERNAME=your_username
   MQTT_PASSWORD=your_password

   # Backblaze B2 Configuration
   B2_APPLICATION_KEY_ID=your_key_id
   B2_APPLICATION_KEY=your_application_key
   B2_BUCKET_NAME=hrms-documents

   # OrientDB Configuration
   ORIENTDB_HOST=localhost
   ORIENTDB_PORT=2424
   ORIENTDB_USERNAME=root
   ORIENTDB_PASSWORD=your_password
   ORIENTDB_DATABASE=hrms

   # gRPC Configuration
   GRPC_HOST=localhost
   GRPC_PORT=50051
   ```

5. **Database Setup**
   ```bash
   # Navigate to database directory
   cd database

   # Copy environment template
   cp .env.example .env

   # Edit .env with your OrientDB credentials
   nano .env  # or your preferred editor

   # Run automated database setup
   python3 init_database.py

   # Test the database setup
   python3 test_database.py

   # Return to main directory
   cd ..
   ```

6. **Start the Application**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📁 Project Structure

```
hrms-main/
├── config/                 # Configuration files
│   └── services.py        # Service configuration
├── services/              # Core services
│   ├── mqtt_service.py    # MQTT communication
│   ├── backblaze_service.py # Backblaze B2 integration
│   ├── grpc_service.py    # gRPC services
│   ├── database_service.py # OrientDB database service
│   └── service_manager.py # Service coordination
├── components/            # UI components
│   ├── dashboard/         # Dashboard components
│   ├── administration/    # Admin components
│   └── attendance/        # Attendance components
├── apis/                  # API endpoints
│   ├── db.py             # OrientDB connection management
│   ├── userModel.py      # User model definitions
│   ├── database_service.py # OrientDB service layer
│   └── database_integration_example.py # Integration examples
├── assets/                # Static assets
├── helperFuns/            # Utility functions
├── layout/                # Layout components
├── main.py               # Application entry point
├── frontend.py           # Frontend initialization
└── requirements.txt      # Python dependencies
```

## �️ Database Architecture

The HRMS uses a comprehensive MySQL database with 15+ tables supporting all HR functions:

### Core Features
- **Complete Schema**: User management, employees, attendance, leave, scheduling
- **Automated Setup**: One-command database initialization with sample data
- **Performance Optimized**: Connection pooling, indexing, and query optimization
- **Security Focused**: Row-level security, audit logging, encrypted sensitive data

### Database Components
```
database/
├── hrms_schema.sql       # Complete MySQL schema with relationships
├── init_database.py      # Automated setup script
├── test_database.py      # Comprehensive testing suite
├── data_flow_map.md      # Architecture documentation
└── .env.example          # Configuration template
```

### Integration
The `apis/database_service.py` provides a clean Python interface for all database operations:
- Connection pooling for performance
- Context managers for safe transactions
- Comprehensive CRUD operations for all entities
- Reporting and analytics queries

See `apis/database_integration_example.py` for examples of integrating database operations with existing components.

## �🔧 Service Architecture

### MQTT Service
- Real-time messaging for live updates
- Topic-based publish/subscribe
- Automatic reconnection and error handling

### Backblaze B2 Service
- Cloud storage for large files
- Document management with metadata
- Secure file upload/download

### gRPC Service
- High-performance service communication
- Protocol buffers for efficient serialization
- Service discovery and registration

### OrientDB Service
- Multi-model database operations
- Document CRUD with schema flexibility
- Graph traversals for complex relationships
- Optimized queries and transactions

## 🎯 API Endpoints

### Health Check
- `GET /health` - Service status and health monitoring

### Dashboard
- `GET /dashboard` - Modern dashboard interface
- `GET /menu-integration` - Integrated menu system

### Administration
- `GET /administration/institution` - Institution profile
- `GET /administration/enroll-staff` - Staff enrollment
- `GET /administration/departments` - Department management

## 🔒 Security Features

- Environment-based configuration
- Secure credential management
- OrientDB connection pooling
- Input validation and sanitization
- Graph-based access control

## 📊 Monitoring

- Service health monitoring
- Real-time system metrics
- Error logging and tracking
- Performance monitoring
- OrientDB query performance metrics

## 🚀 Deployment

### Development
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the code examples

## 🔄 Recent Updates

### Version 2.2.0 - OrientDB Migration
- **Migrated from MySQL to OrientDB**: Complete multi-model database migration
- **Enhanced Data Architecture**: Document, graph, and key-value model integration
- **Improved Relationship Management**: Graph-based organizational hierarchies
- **Flexible Schema Design**: Schema-less documents with embedded classes
- **Advanced Querying**: SQL-like queries with graph traversal capabilities
- **Performance Optimization**: Connection pooling and query optimization
- **Comprehensive Testing**: Updated test suite for OrientDB operations
- **Integration Examples**: Complete examples for component integration

---

**Built with ❤️ for modern HR management using OrientDB's multi-model architecture**