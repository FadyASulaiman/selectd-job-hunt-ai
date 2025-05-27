# core/resume_generator.py
import os
import json
from datetime import datetime
from config.settings import Settings
from core.llm_interface import get_llm_interface
from core.database import DatabaseManager
from core.latex_processor import LaTeXProcessor

class ResumeGenerator:
    """Main class that orchestrates the resume generation process"""
    
    def __init__(self):
        self.llm = get_llm_interface("claude")
        self.db = DatabaseManager()
        self.latex_processor = LaTeXProcessor()
        Settings.setup_directories()
    
    def load_user_data(self) -> dict:
        """Load user data from JSON file"""
        try:
            with open(Settings.USER_DATA_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception(f"User data file not found at {Settings.USER_DATA_PATH}")
        except json.JSONDecodeError:
            raise Exception("Invalid JSON format in user data file")
    
    def calculate_ats_score(self, job_description: str, resume_content: dict) -> int:
        """Calculate ATS keyword matching score (simplified)"""
        job_words = set(job_description.lower().split())
        resume_text = json.dumps(resume_content).lower()
        resume_words = set(resume_text.split())
        
        # Common ML/DS keywords
        important_keywords = {
            'python', 'machine learning', 'deep learning', 'tensorflow', 'pytorch',
            'scikit-learn', 'pandas', 'numpy', 'sql', 'data science', 'nlp',
            'computer vision', 'statistics', 'algorithms', 'git', 'docker'
        }
        
        job_keywords = job_words.intersection(important_keywords)
        matched_keywords = job_keywords.intersection(resume_words)
        
        if not job_keywords:
            return 0
        
        return int((len(matched_keywords) / len(job_keywords)) * 100)
    
    def generate_application(self, job_description: str) -> dict:
        """Generate complete application package"""
        try:
            # Load user data
            user_data = self.load_user_data()
            
            # Extract job information
            print("Extracting job information...")
            company_info = self.llm.extract_job_info(job_description)
            
            # Generate resume content
            print("Generating tailored resume content...")
            resume_content = self.llm.generate_resume_content(job_description, user_data)
            
            # Generate cover letter
            print("Writing cover letter...")
            cover_letter = self.llm.generate_cover_letter(job_description, user_data, company_info)
            
            # Calculate ATS score
            ats_score = self.calculate_ats_score(job_description, resume_content)
            
            # Save to database
            app_id = self.db.save_job_application(company_info, ats_score)
            
            # Create output directory
            output_dir = self._create_output_directory(company_info)
            
            # Generate LaTeX and PDFs
            self._generate_documents(resume_content, cover_letter, user_data, company_info, output_dir, job_description)
            
            return {
                'success': True,
                'application_id': app_id,
                'company_info': company_info,
                'output_directory': output_dir,
                'ats_score': ats_score
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _create_output_directory(self, company_info: dict) -> str:
        """Create output directory with naming convention"""
        date_str = datetime.now().strftime("%m-%d-%y")
        company_name = company_info.get('company_name', 'Unknown').replace(' ', '-')
        job_title = company_info.get('job_title', 'Position').replace(' ', '-')
        
        dir_name = f"{date_str}-{company_name}-{job_title}"
        output_dir = os.path.join(Settings.APPLICATIONS_DIR, dir_name)
        os.makedirs(output_dir, exist_ok=True)
        
        return output_dir
    
    def _generate_documents(self, resume_content: dict, cover_letter: str, user_data: dict, 
                          company_info: dict, output_dir: str, job_description: str):
        """Generate all documents (LaTeX and PDF)"""
        user_name = user_data['applicant_info']['name'].replace(' ', '')
        company_name = company_info.get('company_name', 'Company').replace(' ', '')
        
        # Generate resume
        resume_latex = self.latex_processor.fill_resume_template(resume_content, user_data)
        resume_latex_path = os.path.join(output_dir, f"{user_name}_Resume-{company_name}.tex")
        resume_pdf_path = os.path.join(output_dir, f"{user_name}_Resume-{company_name}.pdf")
        
        with open(resume_latex_path, 'w', encoding='utf-8') as f:
            f.write(resume_latex)
        
        self.latex_processor.compile_latex_to_pdf(resume_latex, resume_pdf_path)
        
        # Generate cover letter
        cover_letter_latex = self.latex_processor.fill_cover_letter_template(cover_letter, user_data, company_info)
        cover_letter_latex_path = os.path.join(output_dir, f"{user_name}_CoverLetter-{company_name}.tex")
        cover_letter_pdf_path = os.path.join(output_dir, f"{user_name}_CoverLetter-{company_name}.pdf")
        
        with open(cover_letter_latex_path, 'w', encoding='utf-8') as f:
            f.write(cover_letter_latex)
        
        self.latex_processor.compile_latex_to_pdf(cover_letter_latex, cover_letter_pdf_path)
        
        # Save job description
        job_title = company_info.get('job_title', 'Position').replace(' ', '-')
        jd_path = os.path.join(output_dir, f"{company_name}-{job_title}-JD.md")
        with open(jd_path, 'w', encoding='utf-8') as f:
            f.write(f"# {company_info.get('company_name', 'Company')} - {company_info.get('job_title', 'Position')}\n\n")
            f.write(job_description)