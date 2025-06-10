import jsonschema
from typing import Dict, Any
from jsonschema import validate, ValidationError

class ResumeDataValidator:
    """Validates resume JSON data against a predefined schema."""
    
    SCHEMA = {
        "type": "object",
        "required": ["name", "professional_title", "email"],
        "properties": {
            "name": {"type": "string", "minLength": 1},
            "professional_title": {"type": "string", "minLength": 1},
            "email": {
                "type": "string",
                "pattern": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            },
            "phone": {"type": "string"},
            "github_link": {"type": "string"},
            "linkedin_link": {"type": "string"},
            "personal_website": {"type": "string"},
            "executive_summary": {"type": "string"},
            "certifications": {"type": "string"},
            
            "projects": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["project_title"],
                    "properties": {
                        "project_title": {"type": "string", "minLength": 1},
                        "project_links": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["name", "link"],
                                "properties": {
                                    "name": {"type": "string"},
                                    "link": {"type": "string"}
                                }
                            }
                        },
                        "project_description": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    }
                }
            },
            
            "work_experience": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["company_name", "role_title", "working_from"],
                    "properties": {
                        "company_name": {"type": "string", "minLength": 1},
                        "company_location": {"type": "string"},
                        "working_from": {"type": "string"},
                        "working_to": {"type": "string"},
                        "role_title": {"type": "string", "minLength": 1},
                        "experience": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    }
                }
            },
            
            "skills": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["category", "skills_list"],
                    "properties": {
                        "category": {"type": "string"},
                        "skills_list": {"type": "string"}
                    }
                }
            },
            
            "education": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["institution_name", "degree_name", "studied_from"],
                    "properties": {
                        "institution_name": {"type": "string", "minLength": 1},
                        "degree_name": {"type": "string", "minLength": 1},
                        "studied_from": {"type": "string"},
                        "studied_to": {"type": "string"},
                        "honors": {"type": "string"}
                    }
                }
            }
        }
    }
    
    @classmethod
    def validate(cls, data: Dict[str, Any]) -> None:
        """Validate resume data against the schema."""
        try:
            validate(instance=data, schema=cls.SCHEMA)
        except ValidationError as e:
            raise ValidationError(f"Resume data validation failed: {e.message}")
    
    @classmethod
    def is_valid(cls, data: Dict[str, Any]) -> bool:
        """Check if resume data is valid without raising exceptions."""
        try:
            cls.validate(data)
            return True
        except ValidationError:
            return False