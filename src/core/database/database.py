from datetime import datetime
import sqlite3
import json
from config.settings import Settings

class DatabaseManager:
    """Handles all database operations"""
    
    def __init__(self):
        self.db_path = Settings.DB_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                first_name TEXT,
                last_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT NULL,
                last_login TIMESTAMP DEFAULT NULL,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS job_applications (
                    application_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    company_name TEXT NOT NULL,
                    job_title TEXT NOT NULL,
                    application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    location TEXT,
                    salary_range TEXT,
                    job_type TEXT,
                    benefits TEXT,
                    country TEXT,
                    status TEXT DEFAULT 'Applied',
                    interview_date TIMESTAMP,
                    notes TEXT,
                    ats_keywords_score INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            conn.commit()
    
    def save_job_application(self, company_info: dict, ats_score: int = None) -> int:
        """Save job application to database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO job_applications 
                (company_name, job_title, location, salary_range, job_type, benefits, country, ats_keywords_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                company_info.get('company_name', 'Unknown'),
                company_info.get('job_title', 'Unknown'),
                company_info.get('location', 'Not specified'),
                company_info.get('salary_range', 'Not specified'),
                company_info.get('job_type', 'Not specified'),
                json.dumps(company_info.get('benefits', [])),
                company_info.get('country', 'Not specified'),
                ats_score
            ))
            
            return cursor.lastrowid
    
    def get_applications_summary(self) -> list:
        """Get summary of all applications"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT company_name, job_title, application_date, status 
                FROM job_applications 
                ORDER BY application_date DESC
            ''')
            return cursor.fetchall()
    
    def update_application_status(self, application_id: int, status: str, notes: str = None):
        """Update application status"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE job_applications 
                SET status = ?, notes = ?, updated_at = ?
                WHERE id = ?
            ''', (status, notes, datetime.now(), application_id))