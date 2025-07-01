import os
from pathlib import Path
from dotenv import load_dotenv
import os

class Settings:
    load_dotenv('src/env/api_keys.env')


    # LLM API config
    MODEL_PROVIDERS = {
        'openai': {'model':'gpt-4.1', 'small_model':'gpt-4.1-nano', 'key': os.environ.get('OPENAI_API_KEY', '')}, 
        'google': {'model': 'gemini-2.5-pro', 'small_model':'gemini-2.5-flash-lite-preview-06-17', 'key': os.environ.get('GEMINI_API_KEY', '')},
        'deepseek': {'model':'deepseek-reasoner', 'small_model':'deepseek-chat', 'key': os.environ.get('DEEPSEEK_API_KEY', '')},
        'anthropic': {'model': 'claude-sonnet-4', 'key': ''} }

    # small model
    SMALL_MODEL_PROVIDER = 'google' # alt: openai - GPT-4.1-nano
    SMALL_MODEL = 'gemini-2.5-flash-preview-04-17'

    # default
    DEFAULT_LLM_PROVIDER = 'openai'

    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
    APPLICATIONS_DIR = os.path.join(str(Path(BASE_DIR).parent.parent), "job_hunt_of_twenty_twenty_five/job_applications")
    
    # Database
    DB_PATH = os.path.join(DATA_DIR, 'applications.db')
    USER_DATA_PATH = os.path.join(DATA_DIR, 'user_data.json')
    
    # Resume constraints
    MAX_WORK_EXPERIENCE = 2
    MAX_PROJECT_EXPERIENCE = 3
    MAX_BULLET_POINTS_FIRST_PROJECT = 3
    MAX_BULLET_POINTS_OTHER_PROJECTS = 2
    MAX_WORDS_PER_BULLET = 30

    # LLM providers
    SUPPORTED_PROVIDERS = ['claude', 'anthropic', 'gpt', 'openai', 'gemini', 'google', 'deepseek']
    
    # Ensure directories exist
    @classmethod
    def setup_directories(cls):
        for directory in [cls.DATA_DIR, cls.APPLICATIONS_DIR]:
            os.makedirs(directory, exist_ok=True)