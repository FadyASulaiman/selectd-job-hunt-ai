from typing import Optional, Protocol
from core.llm_providers.deepseek_llm import DeepSeekLLM
from core.llm_providers.gemini_llm import GeminiLLM
from core.llm_providers.gpt_llm import GPTLLM
from config.settings import Settings

class LLMProvider(Protocol):
    """Protocol for LLM providers"""
    def generate_resume_content(self, job_description: str, user_data: dict) -> dict: ...
    def generate_cover_letter(self, job_description: str, user_data: dict, company_info: dict) -> str: ...
    def extract_job_info(self, job_description: str) -> dict: ...

class LLMFactory:
    """Factory for creating LLM instances"""
    
    @staticmethod
    def create_llm(provider: str, model: Optional[str] = None) -> LLMProvider:
        """Create an LLM instance based on provider"""
        if provider not in Settings.MODEL_PROVIDERS.keys():
            raise ValueError(f"Unknown provider: {provider}")
        
        selected_model = model or Settings.MODEL_PROVIDERS[provider]["model"]
        
        if provider == "openai":
            return GPTLLM(model=selected_model)
        elif provider == "deepseek":
            return DeepSeekLLM(model=selected_model)
        elif provider == "google":
            return GeminiLLM(model=selected_model)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
