from dataclasses import dataclass
import os
from typing import List


@dataclass
class ResumeTemplateSettings:
    """Settings specific to resume template generation."""
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
    
    RESUME_TEMPLATE_FILE_PATH = os.path.join(TEMPLATE_DIR, 'resume_template.tex')
    COVER_LETTER_FILE_PATH = os.path.join(TEMPLATE_DIR, 'cover_letter_template.tex')

    ALTACV_PATH = os.path.join(TEMPLATE_DIR, 'altacv.cls')

    # Generation options
    generate_latex: bool = True
    generate_pdf: bool = True
    save_to_file: bool = True
    
    # PDF compilation settings
    latex_compiler: str = "pdflatex"
    latex_compiler_args: List[str] = None
    cleanup_temp_files: bool = True
    
    # Validation settings
    validate_json_schema: bool = True
    
    def __post_init__(self):
        if self.latex_compiler_args is None:
            self.latex_compiler_args = ["-interaction=nonstopmode"]
