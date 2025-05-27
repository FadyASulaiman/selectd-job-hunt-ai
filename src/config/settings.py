# config/settings.py
import os
from datetime import datetime

class Settings:
    # API Configuration
    CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY', '')
    CLAUDE_MODEL = 'claude-3-5-sonnet-20241022'
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
    APPLICATIONS_DIR = os.path.join(BASE_DIR, 'applications')
    
    # Database
    DB_PATH = os.path.join(DATA_DIR, 'applications.db')
    USER_DATA_PATH = os.path.join(DATA_DIR, 'user_data.json')
    
    # Resume constraints
    MAX_WORK_EXPERIENCE = 2
    MAX_PROJECT_EXPERIENCE = 3
    MAX_BULLET_POINTS_FIRST_PROJECT = 3
    MAX_BULLET_POINTS_OTHER_PROJECTS = 2
    MAX_WORDS_PER_BULLET = 30
    
    # Ensure directories exist
    @classmethod
    def setup_directories(cls):
        for directory in [cls.DATA_DIR, cls.APPLICATIONS_DIR]:
            os.makedirs(directory, exist_ok=True)