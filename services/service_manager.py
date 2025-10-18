"""
Service Manager for HR Management System
Coordinates all services (MQTT, Backblaze, gRPC, OrientDB)
"""

import logging
import sys
import os
from services.mqtt_service import mqtt_service
from services.backblaze_service import backblaze_service
from services.grpc_service import grpc_service
from services.database_service import database_service
from services.auth_service import AuthService

logger = logging.getLogger(__name__)

class ServiceManager:
    """Manages all services for the HR management system"""
    
    def __init__(self):
        self.services = {
            'mqtt': mqtt_service,
            'backblaze': backblaze_service,
            'grpc': grpc_service,
            'database': database_service
        }
        self.auth_service = None
        self.hrms_grpc_service = None
        self.is_initialized = False
    
    def initialize_services(self):
        """Initialize all services"""
        try:
            logger.info("Initializing services...")
            
            # Initialize database service (optional for now)
            if not database_service.connect():
                logger.warning("OrientDB database service initialization failed - continuing without database")
                # return False  # Commented out to allow testing without database
            else:
                logger.info("OrientDB database service initialized successfully")
            
            # Initialize auth service
            self.auth_service = AuthService(database_service)
            logger.info("Auth service initialized successfully")
            
            # Initialize Backblaze B2
            if not backblaze_service.connect():
                logger.warning("Backblaze B2 service initialization failed - continuing without file storage")
            
            # Initialize MQTT service
            # Temporarily disable MQTT service for testing
            # if not mqtt_service.connect():
            #     logger.warning("MQTT service initialization failed - continuing without MQTT")
            # else:
            #     logger.info("MQTT service connected successfully")
            logger.info("MQTT service temporarily disabled for testing")
            
            # Initialize HRMS gRPC service
            try:
                from grpc_services.services.hrms_service import HRMSService
                from grpc_services.proto import hrms_pb2_grpc
                
                self.hrms_grpc_service = HRMSService(database_service, self.auth_service)
                grpc_service.register_service(
                    'hrms',
                    hrms_pb2_grpc.add_HRMSServiceServicer_to_server,
                    lambda: self.hrms_grpc_service
                )
                logger.info("HRMS gRPC service registered successfully")
            except ImportError as e:
                logger.warning(f"gRPC service import failed: {e} - gRPC services will not be available")
            except Exception as e:
                logger.warning(f"HRMS gRPC service registration failed: {e}")
            
            # Initialize gRPC server on port 50051
            try:
                if not grpc_service.start_server(port=50051):
                    logger.warning("gRPC service initialization failed - continuing without gRPC")
                else:
                    logger.info("gRPC server started successfully on port 50051")
            except Exception as e:
                logger.warning(f"gRPC server initialization failed: {e}")
            
            self.is_initialized = True
            logger.info("All services initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Service initialization failed: {e}")
            return False
    
    def shutdown_services(self):
        """Shutdown all services"""
        try:
            logger.info("Shutting down services...")
            
            # Stop gRPC server
            grpc_service.stop_server()
            
            # Disconnect MQTT
            mqtt_service.disconnect()
            
            # Clear service references
            self.auth_service = None
            self.hrms_grpc_service = None
            
            logger.info("All services shut down successfully")
            
        except Exception as e:
            logger.error(f"Service shutdown failed: {e}")
    
    def get_service(self, service_name: str):
        """Get service by name"""
        if service_name == 'auth':
            return self.auth_service
        elif service_name == 'hrms_grpc':
            return self.hrms_grpc_service
        return self.services.get(service_name)
    
    def is_service_available(self, service_name: str) -> bool:
        """Check if service is available"""
        if service_name == 'auth':
            return self.auth_service is not None
        elif service_name == 'hrms_grpc':
            return self.hrms_grpc_service is not None
        
        service = self.services.get(service_name)
        if not service:
            return False
        
        if service_name == 'mqtt':
            return service.is_connected
        elif service_name == 'backblaze':
            return service.is_connected
        elif service_name == 'grpc':
            return service.is_running
        elif service_name == 'database':
            return service.is_connected
        
        return False

# Global service manager instance
service_manager = ServiceManager()

def get_service_manager():
    """Get global service manager instance"""
    return service_manager