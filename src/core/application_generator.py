import logging
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass

from core.database.database import DatabaseManager
from core.services.document_service import DocumentService
from core.services.job_analysis_service import JobAnalysisService
from core.services.user_data_service import UserDataService


logger = logging.getLogger(__name__)

@dataclass
class ApplicationResult:
    """Result of application generation"""
    success: bool
    application_id: Optional[str] = None
    company_info: Optional[Dict[str, Any]] = None
    output_directory: Optional[Path] = None
    ats_score: Optional[float] = None
    error: Optional[str] = None

@dataclass
class ResumeResult:
    """Result of resume generation"""
    success: bool
    latex_content: Optional[str] = None
    latex_file_path: Optional[Path] = None
    pdf_file_path: Optional[Path] = None
    error: Optional[str] = None

class ApplicationGenerator:
    """
    Main orchestrator for resume and application generation.
    """
    
    def __init__(
        self,
        user_data_service: UserDataService,
        document_service: DocumentService,
        job_analysis_service: JobAnalysisService,
        database_manager: DatabaseManager
    ):
        self.user_data_service = user_data_service
        self.document_service = document_service
        self.job_analysis_service = job_analysis_service
        self.database_manager = database_manager
        
        logger.info("ResumeGenerator initialized")
    
    
    def generate_application(self, job_description: str) -> ApplicationResult:
        """
        Generate complete application package.
        
        Args:
            job_description: Job description to tailor application for
            
        Returns:
            ApplicationResult with generation details
        """
        try:
            # Load and validate user data
            user_data = self.user_data_service.load_user_data()
            
            # Analyze job and extract information
            company_info = self.job_analysis_service.extract_job_info(job_description)
            
            # Generate tailored content
            resume_content = self.job_analysis_service.generate_tailored_resume(
                job_description, user_data
            )
            cover_letter = self.job_analysis_service.generate_cover_letter(
                job_description, user_data, company_info
            )

            # Save to database
            app_id = self.database_manager.save_job_application(company_info)
            
            # Generate all documents
            output_dir = self.document_service.generate_application_package(
                resume_content, cover_letter, user_data, company_info, job_description
            )
            
            return ApplicationResult(
                success=True,
                application_id=app_id,
                company_info=company_info,
                output_directory=output_dir,
            )
            
        except Exception as e:
            logger.error(f"Application generation failed: {e}")
            return ApplicationResult(success=False, error=str(e))


# Usage example and factory function
# def create_resume_generator(llm_provider: str = None) -> ApplicationGenerator:
#     """Factory function to create ResumeGenerator with all dependencies"""
#     user_data_service = UserDataService()
#     document_service = DocumentService()
#     job_analysis_service = JobAnalysisService(llm_provider)
#     database_manager = DatabaseManager()
    
#     return ApplicationGenerator(
#         user_data_service=user_data_service,
#         document_service=document_service,
#         job_analysis_service=job_analysis_service,
#         database_manager=database_manager
#     )