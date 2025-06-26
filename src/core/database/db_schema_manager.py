from core.database.db_connection_manager import DatabaseConnectionManager


class DatabaseSchema:
    """Handles database schema creation and management"""
    
    @staticmethod
    def get_users_table_sql() -> str:
        """Get SQL for users table creation"""
        return '''
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
        '''
    
    @staticmethod
    def get_job_applications_table_sql() -> str:
        """Get SQL for job_applications table creation"""
        return '''
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
        '''
    
    def create_all_tables(self, connection_manager: DatabaseConnectionManager):
        """Create all required tables"""
        with connection_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(self.get_users_table_sql())
            cursor.execute(self.get_job_applications_table_sql())
            conn.commit()

