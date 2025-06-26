import json
from typing import Dict, Any


class DataValidator:
    """Handles data validation and sanitization"""
    
    @staticmethod
    def validate_user_data(user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and sanitize user data"""
        required_fields = ['username', 'email', 'password_hash']
        
        for field in required_fields:
            if not user_data.get(field):
                raise ValueError(f"Required field '{field}' is missing or empty")
        
        # Validate email format (basic validation)
        email = user_data['email']
        if '@' not in email or '.' not in email:
            raise ValueError("Invalid email format")
        
        # Sanitize optional fields
        sanitized_data = {
            'username': str(user_data['username']).strip(),
            'email': str(user_data['email']).strip().lower(),
            'password_hash': str(user_data['password_hash']),
            'first_name': str(user_data.get('first_name', '')).strip() or None,
            'last_name': str(user_data.get('last_name', '')).strip() or None,
            'is_active': bool(user_data.get('is_active', True))
        }
        
        return sanitized_data
    
    @staticmethod
    def validate_job_application_data(company_info: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and sanitize job application data"""
        sanitized_data = {
            'company_name': str(company_info.get('company_name', 'Unknown')).strip(),
            'job_title': str(company_info.get('job_title', 'Unknown')).strip(),
            'location': str(company_info.get('location', 'Not specified')).strip(),
            'salary_range': str(company_info.get('salary_range', 'Not specified')).strip(),
            'job_type': str(company_info.get('job_type', 'Not specified')).strip(),
            'benefits': json.dumps(company_info.get('benefits', [])),
            'country': str(company_info.get('country', 'Not specified')).strip(),
            'user_id': company_info.get('user_id', 1)  # Default user_id for backward compatibility
        }
        
        return sanitized_data
