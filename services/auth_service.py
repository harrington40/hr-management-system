"""
Authentication Service for HRMS
Handles user authentication, password hashing, and JWT token management
"""

import os
import jwt
import bcrypt
import logging
from datetime import datetime, timedelta
from typing import Tuple, Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class AuthService:
    """Authentication service for user management"""

    def __init__(self, db_service):
        self.db_service = db_service
        self.secret_key = os.getenv('JWT_SECRET_KEY', 'your-secret-key-here')
        self.algorithm = 'HS256'
        self.token_expiry_hours = int(os.getenv('JWT_EXPIRY_HOURS', '24'))

    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    def generate_token(self, user_data: Dict[str, Any]) -> str:
        """Generate a JWT token for the user"""
        payload = {
            'user_id': user_data.get('id'),
            'username': user_data.get('username'),
            'role': user_data.get('role'),
            'exp': datetime.utcnow() + timedelta(hours=self.token_expiry_hours),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            return None

    def authenticate_user(self, username: str, password: str) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """Authenticate a user with username and password"""
        try:
            # Query user by username or email
            query = f"SELECT FROM User WHERE username = '{username}' OR email = '{username}'"
            result = self.db_service.execute_query(query)

            if not result:
                logger.warning(f"User not found: {username}")
                return False, None, None

            user_data = result[0]

            # Check if user is active
            if not user_data.get('is_active', True):
                logger.warning(f"Inactive user attempted login: {username}")
                return False, None, None

            # Verify password
            stored_hash = user_data.get('password_hash', '')
            if not self.verify_password(password, stored_hash):
                logger.warning(f"Invalid password for user: {username}")
                return False, None, None

            # Update last login
            user_id = user_data.get('id')
            update_query = f"UPDATE User SET last_login = '{datetime.now().isoformat()}' WHERE id = '{user_id}'"
            self.db_service.execute_query(update_query)

            # Generate token
            token = self.generate_token(user_data)

            return True, token, user_data

        except Exception as e:
            logger.error(f"Error authenticating user {username}: {e}")
            return False, None, None

    def get_user_from_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Get user data from JWT token"""
        try:
            payload = self.verify_token(token)
            if not payload:
                return None

            user_id = payload.get('user_id')
            if not user_id:
                return None

            query = f"SELECT FROM User WHERE id = '{user_id}'"
            result = self.db_service.execute_query(query)

            if result:
                return result[0]
            return None

        except Exception as e:
            logger.error(f"Error getting user from token: {e}")
            return None

    def validate_token(self, token: str) -> bool:
        """Validate if a token is valid and not expired"""
        payload = self.verify_token(token)
        return payload is not None

    def refresh_token(self, old_token: str) -> Optional[str]:
        """Refresh an existing token if it's still valid"""
        user_data = self.get_user_from_token(old_token)
        if user_data:
            return self.generate_token(user_data)
        return None

    def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
        """Change a user's password"""
        try:
            # Get current user data
            query = f"SELECT FROM User WHERE id = '{user_id}'"
            result = self.db_service.execute_query(query)

            if not result:
                return False

            user_data = result[0]
            stored_hash = user_data.get('password_hash', '')

            # Verify old password
            if not self.verify_password(old_password, stored_hash):
                return False

            # Hash new password
            new_hash = self.hash_password(new_password)

            # Update password
            update_query = f"UPDATE User SET password_hash = '{new_hash}', updated_at = '{datetime.now().isoformat()}' WHERE id = '{user_id}'"
            self.db_service.execute_query(update_query)

            return True

        except Exception as e:
            logger.error(f"Error changing password for user {user_id}: {e}")
            return False

    def reset_password(self, user_id: str, new_password: str) -> bool:
        """Reset a user's password (admin function)"""
        try:
            new_hash = self.hash_password(new_password)

            update_query = f"UPDATE User SET password_hash = '{new_hash}', updated_at = '{datetime.now().isoformat()}' WHERE id = '{user_id}'"
            result = self.db_service.execute_query(update_query)

            return result is not None

        except Exception as e:
            logger.error(f"Error resetting password for user {user_id}: {e}")
            return False