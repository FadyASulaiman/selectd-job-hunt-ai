import os
import subprocess
import shutil
import tempfile
from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import logging

from config.resume_generation_settings import ResumeTemplateSettings
# from core.validators import ResumeDataValidator

logger = logging.getLogger(__name__)

class LaTeXProcessor:
    """LaTeX processor with template-based resume generation."""
    
    def __init__(self):
        """Initialize the LaTeX processor."""
        self.settings = ResumeTemplateSettings()
        self._setup_jinja_environment()
        self._validate_latex_compiler()
        self._ensure_latex_dependencies()
    
    def _setup_jinja_environment(self) -> None:
        """Setup Jinja2 environment with LaTeX-friendly settings."""
        template_dir = Path(self.settings.TEMPLATE_DIR)
        template_dir.mkdir(exist_ok=True)
        
        # Use custom delimiters to avoid conflicts with LaTeX
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            block_start_string='((*',
            block_end_string='*))',
            variable_start_string='(((',
            variable_end_string=')))',
            comment_start_string='((#',
            comment_end_string='#))',
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def _validate_latex_compiler(self) -> None:
        """Validate that the LaTeX compiler is available."""
        if not shutil.which(self.settings.latex_compiler):
            logger.warning(f"LaTeX compiler '{self.settings.latex_compiler}' not found in PATH")

    def _ensure_latex_dependencies(self) -> None:
        """Ensure required LaTeX class files are available."""
        template_dir = Path(self.settings.TEMPLATE_DIR)
        altacv_path = template_dir / "altacv.cls"
        
        if not altacv_path.exists():
            logger.info(f"AltaCV class file not found, altacv.cls should be placed in {template_dir}")

    def fill_resume_template(self, resume_content: dict, user_data: dict) -> str:
        """
        Fill resume template with content using modern template system.
        
        Args:
            resume_content: LLM-generated resume content
            user_data: User's personal information
            
        Returns:
            Filled LaTeX content
        """
        try:
            # Convert LLM content to template format
            template_data = self._convert_to_template_format(resume_content, user_data)
            
            # Validate data if requested
            # if self.settings.validate_json_schema:
            #     ResumeDataValidator.validate(template_data)
            #     logger.info("Resume data validation passed")
            
            # Process data to handle missing fields gracefully
            processed_data = self._process_resume_data(template_data)
            
            # Render template
            template = self.env.get_template(Path(self.settings.RESUME_TEMPLATE_FILE_PATH).name)
            return template.render(**processed_data)
            
        except TemplateNotFound:
            logger.error(f"Resume template not found: {self.settings.template_file_path}")
            # Fallback to legacy method if template not found
            return self._legacy_fill_resume_template(resume_content, user_data)
        except Exception as e:
            logger.error(f"Error rendering resume template: {e}")
            # Fallback to legacy method on error
            return self._legacy_fill_resume_template(resume_content, user_data)
    
    def _convert_to_template_format(self, resume_content: dict, user_data: dict) -> dict:
        """Convert LLM-generated content to template format."""
        applicant_info = user_data.get('applicant_info', {})
        # Map LLM content to template structure
        template_data = {
            # Basic info
            'name': applicant_info.get('name', ''),
            'email': applicant_info.get('email', ''),
            'phone': applicant_info.get('phone', ''),
            'github_link': applicant_info.get('github', ''),
            'linkedin_link': applicant_info.get('linkedin', ''),
            'personal_website': applicant_info.get('website', ''),
            'professional_title': resume_content.get('professional_title', ''),
            'executive_summary': resume_content.get('executive_summary', ''),
            
            # Projects
            'projects': self._convert_projects(resume_content.get('selected_project_experience', [])),
            
            # Work experience
            'work_experience': self._convert_work_experience(resume_content.get('selected_work_experience', [])),
            
            # Skills
            'skills': self._convert_skills(resume_content.get('relevant_skills', {})),
            
            # Education
            'education': self._convert_education(user_data.get('education', [])),
            
            # Certifications
            'certifications': resume_content.get('certifications', '')
        }
        
        return template_data
    
    def _convert_projects(self, projects: list) -> list:
        """Convert projects to template format."""
        converted = []

        for project in projects:
            if isinstance(project, dict):
                converted_project = {
                    'project_title': project.get('project_name', ''),
                    'documentation_link': project.get('documentation_link', ''),
                    'github_link': project.get('github_link', ''),
                    'live_link': project.get('live_link', ''),
                    'demo_link': project.get('demo_link', ''),
                    'project_description': project.get('bullet_points', []),
                    'project_stack': project.get('project_stack', [])

                }
                converted.append(converted_project)
        return converted
    
    def _convert_work_experience(self, experience: list) -> list:
        """Convert work experience to template format."""
        converted = []

        for exp in experience:
            if isinstance(exp, dict):
                converted_exp = {
                    'company_name': exp.get('company_name', ''),
                    'company_location': exp.get('location', ''),
                    'working_from': exp.get('start_date', ''),
                    'working_to': exp.get('end_date', ''),
                    'role_title': exp.get('job_title', ''),
                    'experience': exp.get('bullet_points', [])
                }
                converted.append(converted_exp)
        return converted
    
    def _convert_skills(self, skills: dict) -> list:
        """Convert skills to template format."""
        converted = []
        for category, skills_list in skills.items():
            if isinstance(skills_list, list):
                skills_str = ', '.join(skills_list)
            else:
                skills_str = str(skills_list)
            
            converted.append({
                'category': category,
                'skills_list': skills_str
            })
        return converted
    
    def _convert_education(self, education: list) -> list:
        """Convert education to template format."""
        converted = []
        for edu in education:
            if isinstance(edu, dict):
                converted_edu = {
                    'institution_name': edu.get('institution', ''),
                    'degree_name': edu.get('degree', ''),
                    'studied_from': edu.get('start_year', ''),
                    'studied_to': edu.get('end_year', ''),
                    'honors': edu.get('honors', '')
                }
                converted.append(converted_edu)
        return converted
    
    def _process_resume_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process resume data to handle missing fields gracefully."""
        processed = data.copy()
        
        # Ensure lists exist even if empty
        list_fields = ['projects', 'work_experience', 'skills', 'education']
        for field in list_fields:
            if field not in processed:
                processed[field] = []
        
        # Ensure nested lists exist
        for project in processed.get('projects', []):
            if 'project_links' not in project:
                project['project_links'] = []
            if 'project_description' not in project:
                project['project_description'] = []
        
        for experience in processed.get('work_experience', []):
            if 'experience' not in experience:
                experience['experience'] = []
        
        return processed
    
    def _legacy_fill_resume_template(self, resume_content: dict, user_data: dict) -> str:
        """Legacy template filling method as fallback."""
        # Original template filling logic
        # This ensures backward compatibility
        template_path = self.settings.TEMPLATE_DIR / "resume_template_legacy.tex"
        
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Simple string replacement for legacy templates
            # Replace with your original logic
            return template_content
        
        raise FileNotFoundError("No resume template found")
    
    def fill_cover_letter_template(self, cover_letter: str, user_data: dict, company_info: dict) -> str:
        """Fill cover letter template (existing method)."""

        try:
            template_name = Path(self.settings.COVER_LETTER_FILE_PATH).name
            template = self.env.get_template(template_name)
            
            # Prepare template data
            template_data = {
                'APPLICANT_NAME': user_data.get('applicant_info', {}).get('name', ''),
                'APPLICANT_EMAIL': user_data.get('applicant_info', {}).get('email', ''),
                'APPLICANT_PHONE': user_data.get('applicant_info', {}).get('phone', ''),
                'COMPANY_NAME': company_info.get('company_name', ''),
                'JOB_TITLE': company_info.get('job_title', ''),
                'COVER_LETTER_CONTENT': cover_letter,
            }
            
            return template.render(**template_data)
            
        except TemplateNotFound:
            logger.error(f"Cover letter template not found: {self.settings.COVER_LETTER_FILE_PATH}")
            raise
        except Exception as e:
            logger.error(f"Error rendering cover letter template: {e}")
            raise
    
    def compile_latex_to_pdf(self, latex_content: str, output_path: str) -> bool:
        """
        Compile LaTeX content to PDF.

        """
        if not shutil.which(self.settings.latex_compiler):
            logger.error(f"LaTeX compiler '{self.settings.latex_compiler}' not found")
            return False
        
        output_path = Path(output_path)
        output_dir = output_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            temp_tex_file = temp_dir / f"{output_path.stem}.tex"

            # Copy required class files to temp directory
            self._copy_latex_dependencies(temp_dir)
            
            # Write LaTeX content to temporary file
            with open(temp_tex_file, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            # Build compilation command
            cmd = [
                self.settings.latex_compiler,
                *self.settings.latex_compiler_args,
                f"-output-directory={temp_dir}",
                str(temp_tex_file)
            ]
            
            try:
                logger.info(f"Compiling LaTeX to PDF: {output_path}")
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    cwd=temp_dir,
                    timeout=60
                )
                
                if result.returncode != 0:
                    logger.error(f"LaTeX compilation failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}")
                    return False
                
                # Move PDF to final location
                temp_pdf = temp_dir / f"{output_path.stem}.pdf"
                if temp_pdf.exists():
                    shutil.move(str(temp_pdf), str(output_path))
                    logger.info(f"PDF generated successfully: {output_path}")
                    return True
                else:
                    logger.error("PDF file was not generated")
                    return False
                
            except subprocess.TimeoutExpired:
                logger.error("LaTeX compilation timed out")
                return False
            except Exception as e:
                logger.error(f"LaTeX compilation error: {e}")
                return False
            
    def _copy_latex_dependencies(self, temp_dir: Path) -> None:
        """Copy required LaTeX class files to compilation directory."""
        template_dir = Path(self.settings.TEMPLATE_DIR)
        
        # List of class files that might be needed
        class_files = ["altacv.cls", "pubs-num.tex"]
        
        for class_file in class_files:
            source_path = template_dir / class_file
            if source_path.exists():
                dest_path = temp_dir / class_file
                shutil.copy2(source_path, dest_path)
                logger.debug(f"Copied {class_file} to compilation directory")
            else:
                logger.warning(f"Class file {class_file} not found in template directory")