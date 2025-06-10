from dataclasses import dataclass
from typing import List


@dataclass
class ResumeTemplateSettings:
    """Settings specific to resume template generation."""
    
    # Template settings
    template_file_path: str = "templates/resume_template.tex"
    
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
