# HRMS gRPC Services

This document describes the comprehensive gRPC services for the HRMS (Human Resource Management System) application.

## Overview

The HRMS gRPC services provide high-performance, type-safe APIs for all HRMS operations including user management, employee management, attendance tracking, leave management, and system administration.

## Architecture

- **Protocol**: gRPC with Protocol Buffers
- **Transport**: HTTP/2
- **Serialization**: Protocol Buffers (protobuf)
- **Authentication**: JWT tokens
- **Database**: OrientDB (via REST API)

## Service Structure

### Core Services

1. **User Service** - User authentication and management
2. **Employee Service** - Employee data management
3. **Department Service** - Department management
4. **Position Service** - Job position management
5. **Attendance Service** - Time tracking and attendance
6. **Leave Service** - Leave request and management
7. **Audit Service** - System audit logging
8. **System Service** - System configuration and settings

### Dashboard Services

- **Dashboard Stats** - Real-time system statistics
- **Employee Stats** - Employee-related analytics
- **Attendance Stats** - Attendance analytics
- **Leave Stats** - Leave management analytics

## API Endpoints

### User Operations

```protobuf
rpc GetUser(UserRequest) returns (UserResponse);
rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
rpc CreateUser(CreateUserRequest) returns (UserResponse);
rpc UpdateUser(UpdateUserRequest) returns (UserResponse);
rpc DeleteUser(DeleteUserRequest) returns (DeleteResponse);
rpc AuthenticateUser(AuthenticateRequest) returns (AuthenticateResponse);
```

### Employee Operations

```protobuf
rpc GetEmployee(EmployeeRequest) returns (EmployeeResponse);
rpc ListEmployees(ListEmployeesRequest) returns (ListEmployeesResponse);
rpc CreateEmployee(CreateEmployeeRequest) returns (EmployeeResponse);
rpc UpdateEmployee(UpdateEmployeeRequest) returns (EmployeeResponse);
rpc DeleteEmployee(DeleteEmployeeRequest) returns (DeleteResponse);
```

### Attendance Operations

```protobuf
rpc GetAttendance(AttendanceRequest) returns (AttendanceResponse);
rpc ListAttendance(ListAttendanceRequest) returns (ListAttendanceResponse);
rpc RecordAttendance(RecordAttendanceRequest) returns (AttendanceResponse);
rpc UpdateAttendance(UpdateAttendanceRequest) returns (AttendanceResponse);
rpc ClockIn(ClockInRequest) returns (AttendanceResponse);
rpc ClockOut(ClockOutRequest) returns (AttendanceResponse);
```

### Leave Operations

```protobuf
rpc GetLeaveType(LeaveTypeRequest) returns (LeaveTypeResponse);
rpc ListLeaveTypes(ListLeaveTypesRequest) returns (ListLeaveTypesResponse);
rpc CreateLeaveType(CreateLeaveTypeRequest) returns (LeaveTypeResponse);
rpc UpdateLeaveType(UpdateLeaveTypeRequest) returns (LeaveTypeResponse);
rpc DeleteLeaveType(DeleteLeaveTypeRequest) returns (DeleteResponse);

rpc GetLeaveRequest(LeaveRequestRequest) returns (LeaveRequestResponse);
rpc ListLeaveRequests(ListLeaveRequestsRequest) returns (ListLeaveRequestsResponse);
rpc CreateLeaveRequest(CreateLeaveRequestRequest) returns (LeaveRequestResponse);
rpc UpdateLeaveRequest(UpdateLeaveRequestRequest) returns (LeaveRequestResponse);
rpc ApproveLeaveRequest(ApproveLeaveRequestRequest) returns (LeaveRequestResponse);
rpc RejectLeaveRequest(RejectLeaveRequestRequest) returns (LeaveRequestResponse);

rpc GetLeaveBalance(LeaveBalanceRequest) returns (LeaveBalanceResponse);
rpc ListLeaveBalances(ListLeaveBalancesRequest) returns (ListLeaveBalancesResponse);
rpc UpdateLeaveBalance(UpdateLeaveBalanceRequest) returns (LeaveBalanceResponse);
```

## Data Models

### User
```protobuf
message User {
  string id = 1;
  string username = 2;
  string email = 3;
  string password_hash = 4;
  string role = 5;
  bool is_active = 6;
  string created_at = 7;
  string updated_at = 8;
  string last_login = 9;
  Employee employee = 10;
}
```

### Employee
```protobuf
message Employee {
  string id = 1;
  string employee_number = 2;
  string first_name = 3;
  string last_name = 4;
  string email = 5;
  string phone = 6;
  string address = 7;
  string date_of_birth = 8;
  string hire_date = 9;
  string termination_date = 10;
  string status = 11;
  string department_id = 12;
  string position_id = 13;
  double salary = 14;
  string manager_id = 15;
  string created_at = 16;
  string updated_at = 17;
  Department department = 18;
  Position position = 19;
  Employee manager = 20;
}
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Login**: Use `AuthenticateUser` to get a JWT token
2. **Authorization**: Include the token in gRPC metadata as `authorization: Bearer <token>`
3. **Validation**: Tokens are validated on each request

## Usage Examples

### Python Client

```python
from grpc.client.hrms_client import HRMSGrpcClient

# Connect to server
client = HRMSGrpcClient()
client.connect()

# Authenticate
auth = client.authenticate_user('admin', 'password')
if auth['success']:
    token = auth['token']
    # Use token for subsequent requests

# Get employee
employee = client.get_employee('employee_id')

# List employees
employees = client.list_employees(page=1, limit=10)

client.disconnect()
```

### Starting the Server

```bash
# Start the gRPC server
python -m grpc.services.hrms_service

# Or through the service manager
python -c "from services.service_manager import service_manager; service_manager.initialize_services()"
```

### Testing

```bash
# Run gRPC service tests
python test_grpc_services.py
```

## Configuration

Configure the gRPC server through environment variables:

- `GRPC_HOST`: Server host (default: localhost)
- `GRPC_PORT`: Server port (default: 50051)
- `JWT_SECRET_KEY`: Secret key for JWT tokens
- `JWT_EXPIRY_HOURS`: Token expiry time in hours (default: 24)

## Error Handling

The API returns standard gRPC status codes:

- `OK` (0): Success
- `NOT_FOUND` (5): Resource not found
- `INVALID_ARGUMENT` (3): Invalid request parameters
- `INTERNAL` (13): Internal server error
- `UNAUTHENTICATED` (16): Authentication required

## Performance

- **Connection**: Persistent HTTP/2 connections
- **Serialization**: Efficient protobuf binary format
- **Streaming**: Support for streaming responses
- **Load Balancing**: Built-in gRPC load balancing support

## Development

### Generating Code

```bash
# Generate Python code from proto files
python -m grpc_tools.protoc --proto_path=grpc/proto --python_out=grpc/proto --grpc_python_out=grpc/proto grpc/proto/hrms.proto
```

### Adding New Services

1. Update `grpc/proto/hrms.proto`
2. Regenerate Python code
3. Implement service methods in `grpc/services/hrms_service.py`
4. Update client in `grpc/client/hrms_client.py`
5. Add tests in `test_grpc_services.py`

## Dependencies

- grpcio>=1.70.0
- grpcio-tools>=1.70.0
- bcrypt>=4.2.0
- PyJWT>=2.0.0

## File Structure

```
grpc/
├── proto/
│   ├── hrms.proto          # Protocol buffer definitions
│   ├── hrms_pb2.py         # Generated protobuf code
│   └── hrms_pb2_grpc.py    # Generated gRPC code
├── services/
│   └── hrms_service.py     # gRPC service implementation
└── client/
    └── hrms_client.py      # gRPC client for testing
```