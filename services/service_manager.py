"""
Service Manager for HR Management System
Coordinates all services (MQTT, Backblaze, gRPC, MySQL)
"""

import logging
from services.mqtt_service import mqtt_service
from services.backblaze_service import backblaze_service
from services.grpc_service import grpc_service
from services.database_service import database_service

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
        self.is_initialized = False
    
    def initialize_services(self):
        """Initialize all services"""
        try:
            logger.info("Initializing services...")
            
            # Initialize database first
            if not database_service.connect():
                logger.error("Failed to initialize database service")
                return False
            
            # Create database tables
            if not database_service.create_tables():
                logger.error("Failed to create database tables")
                return False
            
            # Initialize Backblaze B2
            if not backblaze_service.connect():
                logger.warning("Backblaze B2 service initialization failed - continuing without file storage")
            
            # Initialize MQTT
            try:
                mqtt_service.connect()
            except Exception as e:
                logger.warning(f"MQTT service initialization failed - continuing without real-time messaging: {e}")
            
            # Initialize gRPC server
            if not grpc_service.start_server():
                logger.warning("gRPC service initialization failed - continuing without gRPC")
            
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
            
            logger.info("All services shut down successfully")
            
        except Exception as e:
            logger.error(f"Service shutdown failed: {e}")
    
    def get_service(self, service_name: str):
        """Get service by name"""
        return self.services.get(service_name)
    
    def is_service_available(self, service_name: str) -> bool:
        """Check if service is available"""
        service = self.get_service(service_name)
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