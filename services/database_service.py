"""
MySQL Database Service for Data Persistence
Handles database connections, queries, and operations
"""

import logging
import mysql.connector
from mysql.connector import Error, pooling
from typing import List, Dict, Any, Optional
from config.services import config

logger = logging.getLogger(__name__)

class DatabaseService:
    """MySQL Database service for data persistence"""
    
    def __init__(self):
        self.connection_pool = None
        self.is_connected = False
    
    def connect(self, pool_size: int = 5):
        """Connect to MySQL database with connection pooling"""
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="hrms_pool",
                pool_size=pool_size,
                host=config.MYSQL_HOST,
                port=config.MYSQL_PORT,
                user=config.MYSQL_USER,
                password=config.MYSQL_PASSWORD,
                database=config.MYSQL_DATABASE,
                autocommit=True
            )
            
            # Test connection
            conn = self.connection_pool.get_connection()
            conn.close()
            
            self.is_connected = True
            logger.info("Connected to MySQL database successfully")
            return True
            
        except Error as e:
            logger.error(f"Failed to connect to MySQL database: {e}")
            return False
    
    def get_connection(self):
        """Get database connection from pool"""
        if not self.is_connected:
            logger.error("Database not connected")
            return None
        
        try:
            return self.connection_pool.get_connection()
        except Error as e:
            logger.error(f"Failed to get database connection: {e}")
            return None
    
    def execute_query(self, query: str, params: tuple = None) -> Optional[List[Dict[str, Any]]]:
        """Execute SELECT query and return results"""
        conn = self.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            cursor.close()
            return result
            
        except Error as e:
            logger.error(f"Query execution failed: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    def execute_update(self, query: str, params: tuple = None) -> bool:
        """Execute INSERT, UPDATE, DELETE query"""
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
            cursor.close()
            return True
            
        except Error as e:
            logger.error(f"Update execution failed: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()
    
    def execute_many(self, query: str, params_list: List[tuple]) -> bool:
        """Execute multiple INSERT/UPDATE operations"""
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
            cursor.close()
            return True
            
        except Error as e:
            logger.error(f"Bulk execution failed: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()
    
    def create_tables(self):
        """Create necessary database tables"""
        tables = [
            """
            CREATE TABLE IF NOT EXISTS employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                employee_id VARCHAR(50) UNIQUE NOT NULL,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                department VARCHAR(100),
                position VARCHAR(100),
                hire_date DATE,
                status ENUM('active', 'inactive', 'terminated') DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS attendance (
                id INT AUTO_INCREMENT PRIMARY KEY,
                employee_id VARCHAR(50) NOT NULL,
                check_in TIMESTAMP NULL,
                check_out TIMESTAMP NULL,
                date DATE NOT NULL,
                status ENUM('present', 'absent', 'late', 'early_departure') DEFAULT 'present',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS documents (
                id INT AUTO_INCREMENT PRIMARY KEY,
                employee_id VARCHAR(50) NOT NULL,
                document_name VARCHAR(255) NOT NULL,
                document_type VARCHAR(100),
                b2_file_id VARCHAR(255),
                file_size BIGINT,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                description TEXT,
                FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS mqtt_messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                topic VARCHAR(255) NOT NULL,
                payload JSON,
                qos INT DEFAULT 0,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                direction ENUM('incoming', 'outgoing') DEFAULT 'incoming'
            )
            """
        ]
        
        for table_sql in tables:
            if not self.execute_update(table_sql):
                logger.error("Failed to create tables")
                return False
        
        logger.info("Database tables created successfully")
        return True

# Global database service instance
database_service = DatabaseService()

def get_database_service():
    """Get global database service instance"""
    return database_service