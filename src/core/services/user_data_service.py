import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from config.settings import Settings
from core.validators.json_data_validator import ResumeDataValidator

logger = logging.getLogger(__name__)

class UserDataService:
    """Service for managing user data operations"""
    
    def __init__(self, data_path: Optional[Path] = None):
        self.data_path = data_path or Settings.USER_DATA_PATH
    
    def load_user_data(self) -> Dict[str, Any]:
        """Load user data from JSON file"""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if self._should_validate():
                self.validate_user_data(data)
            
            return data
        except FileNotFoundError:
            raise FileNotFoundError(f"User data file not found at {self.data_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in user data file: {e}")
    
    def validate_user_data(self, user_data: Dict[str, Any]) -> bool:
        """Validate user data format"""
        try:
            applicant_info = user_data.get('applicant_info', {})
            
            validation_data = {
                'name': applicant_info.get('name', ''),
                'professional_title': 'Sample Title',
                'email': applicant_info.get('email', '')
            }
            
            return ResumeDataValidator.is_valid(validation_data)
        except Exception as e:
            logger.error(f"User data validation failed: {e}")
            return False
    
    def _should_validate(self) -> bool:
        """Check if validation should be performed"""
        return getattr(Settings, 'VALIDATE_USER_DATA', False)
