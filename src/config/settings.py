# config/settings.py
import os
from dotenv import load_dotenv
import os

class Settings:
    load_dotenv("src/env/api_keys.env")


    # LLM API config
    MODEL_PROVIDERS = {
        "openai": {"model":"GPT-4.1", "key": os.environ.get('OPENAI_API_KEY', '')}, 
        "google": {"model": "gemini-2.5-flash-preview-04-17", "key": os.environ.get('GEMINI_API_KEY', '')},
        "deepseek": {"model":"deepseek-reasoner", "key": os.environ.get('DEEPSEEK_API_KEY', '')},
        "small_model": {"model": "gemini-2.5-flash-preview-04-17", "key": os.environ.get('GEMINI_API_KEY', '')} }

    # small model
    SMALL_MODEL_PROVIDER = "google" # alt: openai - GPT-4.1-nano
    SMALL_MODEL = "gemini-2.5-flash-preview-04-17"

    # default
    DEFAULT_LLM_PROVIDER = "openai"

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

    # LLM providers
    SUPPORTED_PROVIDERS = ['claude', 'gpt4', 'gpt-4', 'openai', 'gemini', 'google', 'deepseek', 'deep-seek']
    
    # Ensure directories exist
    @classmethod
    def setup_directories(cls):
        for directory in [cls.DATA_DIR, cls.APPLICATIONS_DIR]:
            os.makedirs(directory, exist_ok=True)