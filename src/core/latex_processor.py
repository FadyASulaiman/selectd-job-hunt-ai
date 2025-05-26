# core/latex_processor.py
from datetime import datetime
import os
import subprocess
import shutil
from config.settings import Settings

class LaTeXProcessor:
    """Handles LaTeX template processing and PDF compilation"""
    
    def __init__(self):
        self.templates_dir = Settings.TEMPLATES_DIR
    
    def fill_resume_template(self, resume_data: dict, user_data: dict) -> str:
        """Fill resume template with generated content"""
        
        # Read the template
        template_path = os.path.join(self.templates_dir, 'resume_template.tex')
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Replace placeholders
        replacements = {
            '{{NAME}}': user_data['applicant_info']['name'],
            '{{EMAIL}}': user_data['applicant_info']['email'],
            '{{PHONE}}': user_data['applicant_info']['phone'],
            '{{GITHUB}}': user_data['applicant_info']['github'],
            '{{LINKEDIN}}': user_data['applicant_info']['linkedin'],
            '{{EXECUTIVE_SUMMARY}}': resume_data['executive_summary'],
            '{{WORK_EXPERIENCE}}': self._format_work_experience(resume_data['selected_work_experience']),
            '{{PROJECT_EXPERIENCE}}': self._format_project_experience(resume_data['selected_project_experience']),
            '{{SKILLS}}': self._format_skills(resume_data['relevant_skills']),
            '{{EDUCATION}}': self._format_education(user_data['education'])
        }
        
        for placeholder, value in replacements.items():
            template = template.replace(placeholder, value)
        
        return template
    
    def fill_cover_letter_template(self, cover_letter_content: str, user_data: dict, company_info: dict) -> str:
        """Fill cover letter template"""
        template_path = os.path.join(self.templates_dir, 'cover_letter_template.tex')
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        replacements = {
            '{{NAME}}': user_data['applicant_info']['name'],
            '{{EMAIL}}': user_data['applicant_info']['email'],
            '{{PHONE}}': user_data['applicant_info']['phone'],
            '{{COMPANY_NAME}}': company_info.get('company_name', 'Hiring Team'),
            '{{JOB_TITLE}}': company_info.get('job_title', 'Position'),
            '{{COVER_LETTER_CONTENT}}': cover_letter_content,
            '{{DATE}}': self._get_formatted_date()
        }
        
        for placeholder, value in replacements.items():
            template = template.replace(placeholder, value)
        
        return template
    
    def compile_latex_to_pdf(self, latex_content: str, output_path: str) -> bool:
        """Compile LaTeX content to PDF"""
        try:
            # Create temporary directory for compilation
            temp_dir = os.path.join(os.path.dirname(output_path), 'temp_latex')
            os.makedirs(temp_dir, exist_ok=True)
            
            # Write LaTeX content to temporary file
            tex_filename = os.path.splitext(os.path.basename(output_path))[0] + '.tex'
            temp_tex_path = os.path.join(temp_dir, tex_filename)
            
            with open(temp_tex_path, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            # Compile with pdflatex
            result = subprocess.run([
                'pdflatex', 
                '-interaction=nonstopmode',
                '-output-directory', temp_dir,
                temp_tex_path
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                # Move PDF to final location
                temp_pdf = os.path.join(temp_dir, tex_filename.replace('.tex', '.pdf'))
                if os.path.exists(temp_pdf):
                    shutil.move(temp_pdf, output_path)
                    # Cleanup
                    shutil.rmtree(temp_dir)
                    return True
            
            # Cleanup on failure
            shutil.rmtree(temp_dir, ignore_errors=True)
            return False
            
        except Exception as e:
            print(f"LaTeX compilation error: {str(e)}")
            return False
    
    def _format_work_experience(self, experiences: list) -> str:
        """Format work experience for LaTeX"""
        formatted = ""
        for exp in experiences:
            formatted += f"""
\\cvevent{{{exp['job_title']}}}{{{exp['company_name']}}}{{{exp['date_range']}}}{{{exp['location']}}}
\\begin{{itemize}}
"""
            for bullet in exp['bullet_points']:
                formatted += f"    \\item {bullet}\n"
            formatted += "\\end{itemize}\n\n"
        
        return formatted
    
    def _format_project_experience(self, projects: list) -> str:
        """Format project experience for LaTeX"""
        formatted = ""
        for project in projects:
            formatted += f"""
\\cvevent{{}}{{{project['project_name']}}}{{}}{{}}
\\begin{{itemize}}
"""
            for bullet in project['bullet_points']:
                formatted += f"    \\item {bullet}\n"
            formatted += "\\end{itemize}\n\n"
        
        return formatted
    
    def _format_skills(self, skills: dict) -> str:
        """Format skills for LaTeX"""
        formatted = "\\begin{itemize}\n"
        for category, skill_list in skills.items():
            if skill_list:
                skills_str = ", ".join(skill_list)
                formatted += f"    \\item \\textbf{{{category.title()}:}} {skills_str}\n"
        formatted += "\\end{itemize}"
        return formatted
    
    def _format_education(self, education: list) -> str:
        """Format education for LaTeX"""
        formatted = ""
        for edu in education:
            formatted += f"""
\\cvevent{{{edu['degree']}}}{{{edu['school_name']}\\\\• [{edu.get('achievements', '')}]}}{{{edu['date_range']}}}{{}}{{}}
"""
        return formatted
    
    def _get_formatted_date(self) -> str:
        """Get current date in readable format"""
        return datetime.now().strftime("%B %d, %Y")