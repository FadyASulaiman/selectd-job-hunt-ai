import logging
from typing import Dict, Any
from config.settings import Settings
from core.llm_providers.factory.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class JobAnalysisService:
    """Service for job analysis and content generation"""
    
    def __init__(self, llm_provider: str = None):
        provider = llm_provider or Settings.DEFAULT_LLM_PROVIDER
        self.main_llm = LLMFactory.create_llm(provider)
        self.small_llm = LLMFactory.create_llm(provider, Settings.MODEL_PROVIDERS[provider]["small_model"])
        
        logger.info(f"JobAnalysisService initialized with provider: {provider}")
    
    def extract_job_info(self, job_description: str) -> Dict[str, Any]:
        """Extract structured information from job description"""
        try:
            return self.small_llm.extract_job_info(job_description)
        except Exception as e:
            logger.error(f"Job info extraction failed: {e}")
            raise
    
    def generate_tailored_resume(self, job_description: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate tailored resume content"""
        try:
            return self.main_llm.generate_resume_content(job_description, user_data)
        except Exception as e:
            logger.error(f"Resume content generation failed: {e}")
            raise
    
    def generate_cover_letter(
        self,
        job_description: str,
        user_data: Dict[str, Any],
        company_info: Dict[str, Any]
    ) -> str:
        """Generate tailored cover letter"""
        try:
            return self.main_llm.generate_cover_letter(job_description, user_data, company_info)
        except Exception as e:
            logger.error(f"Cover letter generation failed: {e}")
            raise