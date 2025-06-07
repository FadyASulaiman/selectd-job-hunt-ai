from abc import ABC, abstractmethod

class LLMInterface(ABC):
    """Abstract base class for LLM interfaces"""
    
    @abstractmethod
    def generate_resume_content(self, job_description: str, user_data: dict) -> dict:
        pass
    
    @abstractmethod
    def generate_cover_letter(self, job_description: str, user_data: dict, company_info: dict) -> str:
        pass
    
    @abstractmethod
    def extract_job_info(self, job_description: str) -> dict:
        pass