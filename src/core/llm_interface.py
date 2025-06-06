# core/llm_interface.py
from abc import ABC, abstractmethod
from config.settings import Settings
from core.llm_providers.claude_llm import ClaudeLLM

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


# Factory function for easy LLM switching
def get_llm_interface(provider: str = "claude") -> LLMInterface:
    """Factory function to get LLM interface"""
    if provider.lower() == "claude":
        return ClaudeLLM()
    if provider.lower() == "openai":
        return ClaudeLLM()
    if provider.lower() == "gemini":
        return ClaudeLLM()
    if provider.lower() == "deepseek":
        return ClaudeLLM()
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")