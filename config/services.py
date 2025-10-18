"""
Service Configuration for HR Management System
Configuration for MQTT, Backblaze B2, gRPC, and MySQL
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional

class ServiceConfig(BaseSettings):
    """Service configuration settings"""
    
    # MQTT Configuration
    MQTT_BROKER_HOST: str = "localhost"
    MQTT_BROKER_PORT: int = 1883
    MQTT_USERNAME: Optional[str] = None
    MQTT_PASSWORD: Optional[str] = None
    MQTT_KEEPALIVE: int = 60
    MQTT_CLIENT_ID: str = "hrms_backend"
    
    # Backblaze B2 Configuration
    B2_APPLICATION_KEY_ID: Optional[str] = None
    B2_APPLICATION_KEY: Optional[str] = None
    B2_BUCKET_NAME: Optional[str] = "hrms-documents"
    
    # MySQL Configuration
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = ""
    MYSQL_DATABASE: str = "hrms"
    
    # OrientDB Configuration
    ORIENTDB_HOST: str = "orientdb.transtechologies.com"
    ORIENTDB_PORT: int = 2424
    ORIENTDB_USER: str = "root"
    ORIENTDB_PASSWORD: str = "Namu2025"
    ORIENTDB_DATABASE: str = "hrms"
    
    # gRPC Configuration
    GRPC_HOST: str = "localhost"
    GRPC_PORT: int = 50051
    
    # SMTP Configuration
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # JWT Configuration
    SECRET_KEY: str = "your-secret-key"
    JWT_TOKEN_KEY: str = "your-jwt-key"
    APP_ORIGIN: str = "http://127.0.0.1:8081"
    
    # Additional Oracle fields (if .env uses lowercase)
    PORT: int = 1521
    SID: str = "XE"
    USERNAME: str = "system"
    PASSWORD: str = ""
    HOST: str = "127.0.0.1"
    PASSWORK: str = ""  # Likely a typo for PASSWORD
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Allow extra environment variables

# Global configuration instance
config = ServiceConfig()