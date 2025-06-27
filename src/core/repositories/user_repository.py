
from datetime import datetime
from typing import Optional, Dict, Any

from core.repositories.base_repository import BaseRepository
from core.validators.db_data_validator import DataValidator


class UserRepository(BaseRepository):
    """Repository for user-related database operations"""
    
    def get_table_name(self) -> str:
        return "users"
    
    def create_user(self, user_data: Dict[str, Any]) -> int:
        """Create a new user and return the user ID"""
        validated_data = DataValidator.validate_user_data(user_data)
        
        with self.connection_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, first_name, last_name, is_active)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                validated_data['username'],
                validated_data['email'],
                validated_data['password_hash'],
                validated_data['first_name'],
                validated_data['last_name'],
                validated_data['is_active']
            ))
            
            conn.commit()
            return cursor.lastrowid
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        with self.connection_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        with self.connection_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        with self.connection_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ?', (email.lower(),))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def update_last_login(self, user_id: int) -> None:
        """Update user's last login timestamp"""
        with self.connection_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users 
                SET last_login = ?, updated_at = ?
                WHERE user_id = ?
            ''', (datetime.now(), datetime.now(), user_id))
            conn.commit()
    
    def deactivate_user(self, user_id: int) -> None:
        """Deactivate a user"""
        with self.connection_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users 
                SET is_active = 0, updated_at = ?
                WHERE user_id = ?
            ''', (datetime.now(), user_id))
            conn.commit()