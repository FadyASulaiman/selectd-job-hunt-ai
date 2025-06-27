
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from core.repositories.base_repository import BaseRepository
from core.validators.db_data_validator import DataValidator


class JobApplicationRepository(BaseRepository):
    """Repository for job application-related database operations"""
    
    def get_table_name(self) -> str:
        return "job_applications"
    
    def save_job_application(self, company_info: Dict[str, Any], ats_score: Optional[int] = None) -> int:
        """Save job application to database"""
        validated_data = DataValidator.validate_job_application_data(company_info)
        
        with self.connection_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO job_applications 
                (user_id, company_name, job_title, location, salary_range, job_type, benefits, country, ats_keywords_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                validated_data['user_id'],
                validated_data['company_name'],
                validated_data['job_title'],
                validated_data['location'],
                validated_data['salary_range'],
                validated_data['job_type'],
                validated_data['benefits'],
                validated_data['country'],
                ats_score
            ))
            
            conn.commit()
            return cursor.lastrowid
    
    def get_applications_summary(self, user_id: Optional[int] = None) -> List[Tuple]:
        """Get summary of applications, optionally filtered by user_id"""
        with self.connection_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            if user_id:
                cursor.execute('''
                    SELECT company_name, job_title, application_date, status 
                    FROM job_applications 
                    WHERE user_id = ?
                    ORDER BY application_date DESC
                ''', (user_id,))
            else:
                cursor.execute('''
                    SELECT company_name, job_title, application_date, status 
                    FROM job_applications 
                    ORDER BY application_date DESC
                ''')
            
            return cursor.fetchall()
    
    def update_application_status(self, application_id: int, status: str, notes: Optional[str] = None) -> None:
        """Update application status"""
        with self.connection_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE job_applications 
                SET status = ?, notes = ?, updated_at = ?
                WHERE application_id = ?
            ''', (status, notes, datetime.now(), application_id))
            conn.commit()
    
    def get_application_by_id(self, application_id: int) -> Optional[Dict[str, Any]]:
        """Get application by ID"""
        with self.connection_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM job_applications WHERE application_id = ?', (application_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_applications_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all applications for a specific user"""
        with self.connection_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM job_applications WHERE user_id = ? ORDER BY application_date DESC', (user_id,))
            return [dict(row) for row in cursor.fetchall()]

