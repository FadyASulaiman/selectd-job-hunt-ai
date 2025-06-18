import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
from config.settings import Settings
from core.latex_processor import LaTeXProcessor
from core.validators.json_data_validator import ResumeDataValidator

logger = logging.getLogger(__name__)

@dataclass
class DocumentGenerationResult:
    """Result of document generation"""
    latex_content: Optional[str] = None
    latex_path: Optional[Path] = None
    pdf_path: Optional[Path] = None

class DocumentService:
    """Service for document generation and file operations"""
    
    def __init__(self, latex_processor: Optional[LaTeXProcessor] = None):
        self.latex_processor = latex_processor or LaTeXProcessor()
        Settings.setup_directories()

    
    def generate_application_package(
        self,
        resume_content: Dict[str, Any],
        cover_letter: str,
        user_data: Dict[str, Any],
        company_info: Dict[str, Any],
        job_description: str
    ) -> Path:
        """Generate complete application package"""
        try:
            # Create output directory
            output_dir = self._create_application_output_directory(company_info)
            
            # Generate resume documents
            self._generate_resume_files(resume_content, user_data, company_info, output_dir)
            
            # Generate cover letter documents
            self._generate_cover_letter_files(cover_letter, user_data, company_info, output_dir)
            
            # Save job description
            self._save_job_description(job_description, company_info, output_dir)
            
            return output_dir
            
        except Exception as e:
            logger.error(f"Application package generation failed: {e}")
            raise

    
    def _create_application_output_directory(self, company_info: Dict[str, Any]) -> Path:
        """Create output directory for full application"""
        date_str = datetime.now().strftime("%m-%d-%y")
        company_name = company_info.get('company_name', 'Unknown').replace(' ', '-')
        job_title = company_info.get('job_title', 'Position').replace(' ', '-')
        
        dir_name = f"{date_str}-{company_name}-{job_title}"
        output_dir = Settings.APPLICATIONS_DIR / dir_name
        output_dir.mkdir(parents=True, exist_ok=True)
        
        return output_dir
    
    def _generate_resume_files(
        self,
        resume_content: Dict[str, Any],
        user_data: Dict[str, Any],
        company_info: Dict[str, Any],
        output_dir: Path
    ):
        """Generate resume LaTeX and PDF files"""
        user_name = user_data['applicant_info']['name'].replace(' ', '')
        company_name = company_info.get('company_name', 'Company').replace(' ', '')
        
        resume_latex = self.latex_processor.fill_resume_template(resume_content, user_data)
        
        latex_path = output_dir / f"{user_name}_Resume-{company_name}.tex"
        pdf_path = output_dir / f"{user_name}_Resume-{company_name}.pdf"
        
        self._save_text_file(latex_path, resume_latex)
        self.latex_processor.compile_latex_to_pdf(resume_latex, str(pdf_path))
    
    def _generate_cover_letter_files(
        self,
        cover_letter: str,
        user_data: Dict[str, Any],
        company_info: Dict[str, Any],
        output_dir: Path
    ):
        """Generate cover letter LaTeX and PDF files"""
        user_name = user_data['applicant_info']['name'].replace(' ', '')
        company_name = company_info.get('company_name', 'Company').replace(' ', '')
        
        cover_letter_latex = self.latex_processor.fill_cover_letter_template(
            cover_letter, user_data, company_info
        )
        
        latex_path = output_dir / f"{user_name}_CoverLetter-{company_name}.tex"
        pdf_path = output_dir / f"{user_name}_CoverLetter-{company_name}.pdf"
        
        self._save_text_file(latex_path, cover_letter_latex)
        self.latex_processor.compile_latex_to_pdf(cover_letter_latex, str(pdf_path))
    
    def _save_job_description(
        self,
        job_description: str,
        company_info: Dict[str, Any],
        output_dir: Path
    ):
        """Save job description as markdown file"""
        company_name = company_info.get('company_name', 'Company')
        job_title = company_info.get('job_title', 'Position').replace(' ', '-')
        
        content = f"# {company_name} - {job_title}\n\n{job_description}"
        file_path = output_dir / f"{company_name}-{job_title}-JD.md"
        
        self._save_text_file(file_path, content)
    
    def _save_text_file(self, file_path: Path, content: str):
        """Save text content to file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            logger.error(f"Failed to save file {file_path}: {e}")
            raise