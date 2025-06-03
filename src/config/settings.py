# config/settings.py
import os
from dotenv import load_dotenv
import os

class Settings:
    load_dotenv("env/api_keys.env")

    # Gemini API Configuration
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
    GEMINI_MODEL = 'gemini-2.5-pro'

    # GPT API config
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    OPENAI_MODEL = 'gemini-2.5-pro'
    
    # DeepSeek API config
    DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', '')
    DEEPSEEK_MODEL = 'deepseek-reasoner' # R1

    # small model
    SMALL_MODEL = 'GPT-4.1-nano'

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