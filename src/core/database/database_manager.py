from typing import Optional, Dict, Any, List, Tuple

from config.settings import Settings
from core.database.db_connection_manager import DatabaseConnectionManager
from core.database.db_schema_manager import DatabaseSchema
from core.repositories.application_repository import JobApplicationRepository
from core.repositories.user_repository import UserRepository


class DatabaseManager:
    """Main database manager that orchestrates all database operations"""
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or self._get_default_db_path()
        self.connection_manager = DatabaseConnectionManager(self.db_path)
        self.schema = DatabaseSchema()
        self.user_repository = UserRepository(self.connection_manager)
        self.job_application_repository = JobApplicationRepository(self.connection_manager)
        
        self.init_database()
    
    def _get_default_db_path(self) -> str:
        """Get default database path from settings"""
        return Settings.DB_PATH

    
    def init_database(self):
        """Initialize database with required tables"""
        self.schema.create_all_tables(self.connection_manager)
    
    # User operations
    def create_user(self, user_data: Dict[str, Any]) -> int:
        """Create a new user"""
        return self.user_repository.create_user(user_data)
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        return self.user_repository.get_user_by_id(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        return self.user_repository.get_user_by_username(username)
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        return self.user_repository.get_user_by_email(email)
    
    def update_last_login(self, user_id: int) -> None:
        """Update user's last login"""
        self.user_repository.update_last_login(user_id)
    
    def deactivate_user(self, user_id: int) -> None:
        """Deactivate a user"""
        self.user_repository.deactivate_user(user_id)
    
    # Job application operations
    def save_job_application(self, company_info: Dict[str, Any], ats_score: Optional[int] = None) -> int:
        """Save job application to database"""
        return self.job_application_repository.save_job_application(company_info, ats_score)
    
    def get_applications_summary(self, user_id: Optional[int] = None) -> List[Tuple]:
        """Get summary of all applications"""
        return self.job_application_repository.get_applications_summary(user_id)
    
    def update_application_status(self, application_id: int, status: str, notes: Optional[str] = None) -> None:
        """Update application status"""
        self.job_application_repository.update_application_status(application_id, status, notes)
    
    def get_application_by_id(self, application_id: int) -> Optional[Dict[str, Any]]:
        """Get application by ID"""
        return self.job_application_repository.get_application_by_id(application_id)
    
    def get_applications_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all applications for a specific user"""
        return self.job_application_repository.get_applications_by_user(user_id)