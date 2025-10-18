
"""
gRPC Service for High-Performance Communication
Handles gRPC server and client communication
"""

import logging
import grpc
from concurrent import futures
from typing import Callable, Dict, Any
from config.services import config
# from services.hrms_service import hrms_servicer

logger = logging.getLogger(__name__)

class GRPCService:
    """gRPC Service for high-performance communication"""
    
    def __init__(self):
        self.server = None
        self.is_running = False
        self.services = {}
    
    def start_server(self, max_workers: int = 10, port: int = 50051):
        """Start gRPC server on specified port"""
        try:
            self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
            
            # Register HRMS service
            # Note: In a real implementation, you'd use generated code from proto files
            # For now, we'll keep it simple
            
            # Add registered services
            for service_name, service_config in self.services.items():
                add_service_func = service_config.get('add_func')
                servicer_class = service_config.get('servicer')
                
                if add_service_func and servicer_class:
                    servicer_instance = servicer_class()
                    add_service_func(servicer_instance, self.server)
                    logger.info(f"Registered gRPC service: {service_name}")
            
            # Start server on specified port
            self.server.add_insecure_port(f'[::]:{port}')
            self.server.start()
            self.is_running = True
            
            logger.info(f"gRPC server started on port {port}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start gRPC server: {e}")
            return False
    
    def register_service(self, service_name: str, add_func: Callable, servicer_class: Any):
        """Register a gRPC service"""
        self.services[service_name] = {
            'add_func': add_func,
            'servicer': servicer_class
        }
        logger.info(f"Registered gRPC service: {service_name}")
    
    def stop_server(self):
        """Stop gRPC server"""
        if self.server:
            self.server.stop(0)
            self.is_running = False
            logger.info("gRPC server stopped")
    
    def create_channel(self, target: str = None):
        """Create gRPC channel for client communication"""
        if not target:
            target = f'{config.GRPC_HOST}:{config.GRPC_PORT}'
        
        try:
            channel = grpc.insecure_channel(target)
            return channel
        except Exception as e:
            logger.error(f"Failed to create gRPC channel: {e}")
            return None

# Global gRPC service instance
grpc_service = GRPCService()

def get_grpc_service():
    """Get global gRPC service instance"""
    return grpc_service