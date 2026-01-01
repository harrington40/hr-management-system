"""
Backblaze B2 Service for Large File Storage
Handles file uploads, downloads, and management in Backblaze B2
"""

import logging
import os
from typing import Optional, BinaryIO
from b2sdk.v2 import B2Api, InMemoryAccountInfo, Bucket
from config.services import config

logger = logging.getLogger(__name__)

class BackblazeService:
    """Backblaze B2 service for file storage"""
    
    def __init__(self):
        self.api = None
        self.bucket = None
        self.is_connected = False
    
    def connect(self):
        """Connect to Backblaze B2"""
        try:
            if not config.B2_APPLICATION_KEY_ID or not config.B2_APPLICATION_KEY:
                logger.warning("Backblaze B2 credentials not configured")
                return False
            
            # Initialize B2 API
            info = InMemoryAccountInfo()
            self.api = B2Api(info)
            
            # Authorize account
            self.api.authorize_account(
                "production",
                config.B2_APPLICATION_KEY_ID,
                config.B2_APPLICATION_KEY
            )
            
            # Get or create bucket
            try:
                self.bucket = self.api.get_bucket_by_name(config.B2_BUCKET_NAME)
            except Exception:
                logger.info(f"Bucket {config.B2_BUCKET_NAME} not found, creating new bucket")
                self.bucket = self.api.create_bucket(config.B2_BUCKET_NAME, "allPrivate")
            
            self.is_connected = True
            logger.info("Connected to Backblaze B2 successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to Backblaze B2: {e}")
            return False
    
    def upload_file(self, file_path: str, file_name: Optional[str] = None) -> Optional[str]:
        """Upload file to Backblaze B2"""
        if not self.is_connected:
            logger.error("Backblaze B2 not connected")
            return None
        
        try:
            if not file_name:
                file_name = os.path.basename(file_path)
            
            # Upload file
            uploaded_file = self.bucket.upload_local_file(
                local_file=file_path,
                file_name=file_name
            )
            
            logger.info(f"File uploaded successfully: {file_name}")
            return uploaded_file.id_
            
        except Exception as e:
            logger.error(f"Failed to upload file {file_path}: {e}")
            return None
    
    def upload_bytes(self, data: bytes, file_name: str, content_type: str = "application/octet-stream") -> Optional[str]:
        """Upload bytes data to Backblaze B2"""
        if not self.is_connected:
            logger.error("Backblaze B2 not connected")
            return None
        
        try:
            uploaded_file = self.bucket.upload_bytes(
                data_bytes=data,
                file_name=file_name,
                content_type=content_type
            )
            
            logger.info(f"Bytes uploaded successfully: {file_name}")
            return uploaded_file.id_
            
        except Exception as e:
            logger.error(f"Failed to upload bytes for {file_name}: {e}")
            return None
    
    def download_file(self, file_id: str, download_path: str) -> bool:
        """Download file from Backblaze B2"""
        if not self.is_connected:
            logger.error("Backblaze B2 not connected")
            return False
        
        try:
            file_info = self.api.get_file_info(file_id)
            
            # Download file
            self.bucket.download_file_by_id(
                file_id=file_id,
                local_file=download_path
            )
            
            logger.info(f"File downloaded successfully: {download_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to download file {file_id}: {e}")
            return False
    
    def download_bytes(self, file_id: str) -> Optional[bytes]:
        """Download file as bytes from Backblaze B2"""
        if not self.is_connected:
            logger.error("Backblaze B2 not connected")
            return None
        
        try:
            # Download to bytes
            download = self.bucket.download_file_by_id(file_id)
            data = download.get_bytes()
            
            logger.info(f"Bytes downloaded successfully for file: {file_id}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to download bytes for file {file_id}: {e}")
            return None
    
    def delete_file(self, file_id: str) -> bool:
        """Delete file from Backblaze B2"""
        if not self.is_connected:
            logger.error("Backblaze B2 not connected")
            return False
        
        try:
            self.api.delete_file_version(file_id=file_id, file_name="")
            logger.info(f"File deleted successfully: {file_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete file {file_id}: {e}")
            return False
    
    def get_file_url(self, file_id: str) -> Optional[str]:
        """Get download URL for file"""
        if not self.is_connected:
            logger.error("Backblaze B2 not connected")
            return None
        
        try:
            file_info = self.api.get_file_info(file_id)
            download_url = self.api.get_download_url_for_fileid(file_id)
            return download_url
            
        except Exception as e:
            logger.error(f"Failed to get URL for file {file_id}: {e}")
            return None
    
    def list_files(self, prefix: str = "") -> list:
        """List files in bucket"""
        if not self.is_connected:
            logger.error("Backblaze B2 not connected")
            return []
        
        try:
            files = []
            for file_version, folder_name in self.bucket.ls(prefix=prefix):
                files.append({
                    'id': file_version.id_,
                    'name': file_version.file_name,
                    'size': file_version.size,
                    'upload_timestamp': file_version.upload_timestamp,
                    'content_type': file_version.content_type
                })
            
            return files
            
        except Exception as e:
            logger.error(f"Failed to list files: {e}")
            return []

# Global Backblaze service instance
backblaze_service = BackblazeService()

def get_backblaze_service():
    """Get global Backblaze service instance"""
    return backblaze_service