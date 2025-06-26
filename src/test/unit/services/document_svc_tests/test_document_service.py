import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

# Correct imports based on your project structure
from core.latex_processor import LaTeXProcessor
from core.services.document_service import DocumentService


# Test data fixtures
@pytest.fixture
def sample_user_data():
    return {
        "applicant_info": {
            "name": "John Smith",
            "email": "jsmith@gmail.com", 
            "phone": "(+10) 178 6633 234",
            "github": "github.com/JSmith",
            "linkedin": "linkedin.com/in/john-smith-mcdonald"
        },
        "education": [
            {
                "school_name": "Michigan University",
                "degree": "B.Sc. in Mechanical Engineering",
                "date_range": "2018 -- 2023",
                "achievements": "Dean's List - 6 semesters"
            }
        ]
    }


@pytest.fixture
def sample_resume_content():
    return {
        "executive_summary": "Senior Software Engineer with 5+ years of hands-on Python expertise...",
        "selected_work_experience": [
            {
                "company_name": "Company 1",
                "job_title": "Backend Engineer",
                "location": "Toronto, Ontario, Canada",
                "start_date": "March 2023",
                "end_date": "December 2024",
                "bullet_points": [
                    "Engineered scalable backend for Lightspeed, enabling high-speed internet for 14M+ users via ACP initiative.",
                    "Designed RESTful APIs handling 10,000+ req/sec, leveraging GCP CloudSQL, Storage, and Sentry analytics."
                ]
            }
        ],
        "selected_project_experience": [
            {
                "project_name": "Sentiment Analysis on Financial News Headlines",
                "project_stack": "Python, TensorFlow, LSTM, NLP, MLflow, GCP",
                "bullet_points": [
                    "Engineered LSTM-based NLP pipeline (F1: 0.71, AUC: 0.86) for real-time sentiment scoring.",
                    "Deployed on GCP with MLflow for robust model tracking, ensuring reproducibility."
                ],
                "documentation_link": "https://github.com/JSmith/sentiment-analysis/README.md",
                "github_link": "https://github.com/JSmith/sentiment-analysis",
                "demo_link": "https://youtube.com/watch?v=demo123",
                "live_link": "https://sentiment-app.herokuapp.com"
            }
        ],
        "relevant_skills": {
            "technical": ["Python", "React", "JavaScript", "AWS", "GCP", "Docker", "CI/CD", "SQL"],
            "machine_learning": ["TensorFlow", "scikit-learn", "MLflow", "NLP", "Deep Learning"],
            "tools": ["Git", "Terraform", "Sentry", "Pandas", "NumPy"]
        }
    }


@pytest.fixture
def sample_company_info():
    return {
        "company_name": "TechCorp Inc",
        "job_title": "Senior Software Engineer"
    }


@pytest.fixture
def sample_cover_letter():
    return """I am excited to apply for the Senior Software Engineer position at TechCorp Inc. 
    Your commitment to building innovative software solutions deeply resonates with my passion 
    for impactful, scalable engineering."""


@pytest.fixture
def sample_job_description():
    return """We are looking for a Senior Software Engineer to join our team. 
    The ideal candidate will have experience with Python, React, and cloud technologies."""


# Unit Tests - Mock LaTeXProcessor entirely
@pytest.mark.unit
class TestDocumentServiceUnit:
    """Unit tests for DocumentService - LaTeXProcessor is mocked"""
    
    @pytest.fixture
    def mock_latex_processor(self):
        return Mock(spec=LaTeXProcessor)
    
    @pytest.fixture
    def document_service(self, mock_latex_processor):
        with patch('core.services.document_service.Settings') as mock_settings:
            mock_settings.setup_directories.return_value = None
            # Fix: Return Path objects instead of strings
            mock_settings.APPLICATIONS_DIR = Path("/mock/applications")
            mock_settings.TEMPLATES_DIR = Path("/mock/templates")
            return DocumentService(latex_processor=mock_latex_processor)
    
    @patch('core.services.document_service.Settings.APPLICATIONS_DIR', Path("/mock/applications"))
    @patch('core.services.document_service.datetime')
    def test_create_application_output_directory(self, mock_datetime, document_service, sample_company_info):
        """Test directory creation logic"""
        mock_datetime.now.return_value.strftime.return_value = "06-18-25"
        
        with patch.object(Path, 'mkdir') as mock_mkdir:
            result = document_service._create_application_output_directory(sample_company_info)
            
            expected_path = Path("/mock/applications/06-18-25-TechCorp-Inc-Senior-Software-Engineer")
            assert result == expected_path
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
    
    
    def test_generate_resume_files(self, document_service, sample_resume_content, 
                                  sample_user_data, sample_company_info):
        """Test resume file generation"""
        output_dir = Path("/test/output")
        expected_latex = "\\documentclass{article}..."
        
        document_service.latex_processor.fill_resume_template.return_value = expected_latex
        document_service.latex_processor.compile_latex_to_pdf.return_value = True
        
        with patch.object(document_service, '_save_text_file') as mock_save:
            document_service._generate_resume_files(
                sample_resume_content, sample_user_data, sample_company_info, output_dir
            )
            
            # Verify LaTeX processor calls
            document_service.latex_processor.fill_resume_template.assert_called_once_with(
                sample_resume_content, sample_user_data
            )
            document_service.latex_processor.compile_latex_to_pdf.assert_called_once()
            
            # Verify file saving
            expected_latex_path = output_dir / "JohnSmith_Resume-TechCorpInc.tex"
            mock_save.assert_called_once_with(expected_latex_path, expected_latex)
    
    def test_generate_cover_letter_files(self, document_service, sample_cover_letter,
                                       sample_user_data, sample_company_info):
        """Test cover letter file generation"""
        output_dir = Path("/test/output")
        expected_latex = "\\documentclass{letter}..."
        
        document_service.latex_processor.fill_cover_letter_template.return_value = expected_latex
        document_service.latex_processor.compile_latex_to_pdf.return_value = True
        
        with patch.object(document_service, '_save_text_file') as mock_save:
            document_service._generate_cover_letter_files(
                sample_cover_letter, sample_user_data, sample_company_info, output_dir
            )
            
            # Verify LaTeX processor calls
            document_service.latex_processor.fill_cover_letter_template.assert_called_once_with(
                sample_cover_letter, sample_user_data, sample_company_info
            )
            document_service.latex_processor.compile_latex_to_pdf.assert_called_once()
            
            # Verify file saving
            expected_latex_path = output_dir / "JohnSmith_CoverLetter-TechCorpInc.tex"
            mock_save.assert_called_once_with(expected_latex_path, expected_latex)
    
    def test_save_job_description(self, document_service, sample_job_description, sample_company_info):
        """Test job description saving"""
        output_dir = Path("/test/output")
        
        with patch.object(document_service, '_save_text_file') as mock_save:
            document_service._save_job_description(
                sample_job_description, sample_company_info, output_dir
            )
            
            expected_content = f"# TechCorp Inc - Senior-Software-Engineer\n\n{sample_job_description}"
            expected_path = output_dir / "TechCorp Inc-Senior-Software-Engineer-JD.md"
            mock_save.assert_called_once_with(expected_path, expected_content)
            
    
    def test_generate_application_package_success(self, document_service, sample_resume_content,
                                                sample_cover_letter, sample_user_data, 
                                                sample_company_info, sample_job_description):
        """Test successful application package generation"""
        expected_output_dir = Path("/test/output")
        
        with patch.object(document_service, '_create_application_output_directory', 
                         return_value=expected_output_dir) as mock_create_dir, \
             patch.object(document_service, '_generate_resume_files') as mock_resume, \
             patch.object(document_service, '_generate_cover_letter_files') as mock_cover, \
             patch.object(document_service, '_save_job_description') as mock_job_desc:
            
            result = document_service.generate_application_package(
                sample_resume_content, sample_cover_letter, sample_user_data,
                sample_company_info, sample_job_description
            )
            
            assert result == expected_output_dir
            mock_create_dir.assert_called_once_with(sample_company_info)
            mock_resume.assert_called_once_with(
                sample_resume_content, sample_user_data, sample_company_info, expected_output_dir
            )
            mock_cover.assert_called_once_with(
                sample_cover_letter, sample_user_data, sample_company_info, expected_output_dir
            )
            mock_job_desc.assert_called_once_with(
                sample_job_description, sample_company_info, expected_output_dir
            )
    
    def test_generate_application_package_failure(self, document_service, sample_resume_content,
                                                sample_cover_letter, sample_user_data,
                                                sample_company_info, sample_job_description):
        """Test application package generation failure"""
        with patch.object(document_service, '_create_application_output_directory',
                         side_effect=Exception("Directory creation failed")), \
             patch('core.services.document_service.logger') as mock_logger:
            
            with pytest.raises(Exception):
                document_service.generate_application_package(
                    sample_resume_content, sample_cover_letter, sample_user_data,
                    sample_company_info, sample_job_description
                )
            
            mock_logger.error.assert_called_once()
    
    def test_invalid_data_structures(self, document_service):
        """Test handling of invalid data structures"""
        invalid_user_data = {
            "applicant_info": None  # Invalid structure
        }
        invalid_company_info = "not_a_dict"  # Invalid type
        
        output_dir = Path("/test/output")
        
        with pytest.raises((AttributeError, TypeError)):
            document_service._generate_resume_files(
                {}, invalid_user_data, {}, output_dir
            )
        
        with pytest.raises((AttributeError, TypeError)):
            document_service._create_application_output_directory(invalid_company_info)


# Integration Tests - Real LaTeXProcessor, mocked file operations
@pytest.mark.integration
class TestDocumentServiceIntegration:
    """Integration tests for DocumentService with real LaTeXProcessor"""
    
    @pytest.fixture
    def document_service(self):
        with patch('core.services.document_service.Settings') as mock_settings:
            mock_settings.setup_directories.return_value = None
            # Fix: Return Path objects instead of strings
            mock_settings.APPLICATIONS_DIR = Path("/mock/applications")
            mock_settings.TEMPLATES_DIR = Path("/mock/templates")
            return DocumentService()
    
    def test_integration_with_latex_processor(self, document_service, sample_resume_content,
                                            sample_user_data, sample_company_info):
        """Test integration between DocumentService and LaTeXProcessor"""
        output_dir = Path("/test/output")
        
        # Mock the LaTeXProcessor methods to return expected values
        with patch.object(document_service.latex_processor, 'fill_resume_template',
                         return_value="\\documentclass{article}...") as mock_fill, \
             patch.object(document_service.latex_processor, 'compile_latex_to_pdf',
                         return_value=True) as mock_compile, \
             patch.object(document_service, '_save_text_file') as mock_save:
            
            document_service._generate_resume_files(
                sample_resume_content, sample_user_data, sample_company_info, output_dir
            )
            
            # Verify that LaTeXProcessor methods are called with correct arguments
            mock_fill.assert_called_once_with(sample_resume_content, sample_user_data)
            mock_compile.assert_called_once()
            
            # Verify the call order
            assert mock_fill.call_count == 1
            assert mock_compile.call_count == 1
            assert mock_save.call_count == 1
    
    def test_latex_processor_error_handling(self, document_service, sample_resume_content,
                                          sample_user_data, sample_company_info):
        """Test error handling when LaTeXProcessor fails"""
        output_dir = Path("/test/output")
        
        with patch.object(document_service.latex_processor, 'fill_resume_template',
                         side_effect=Exception("Template error")) as mock_fill:
            
            with pytest.raises(Exception):
                document_service._generate_resume_files(
                    sample_resume_content, sample_user_data, sample_company_info, output_dir
                )
    
    def test_pdf_compilation_failure(self, document_service, sample_resume_content,
                                   sample_user_data, sample_company_info):
        """Test handling of PDF compilation failure"""
        output_dir = Path("/test/output")
        
        with patch.object(document_service.latex_processor, 'fill_resume_template',
                         return_value="\\documentclass{article}..."), \
             patch.object(document_service.latex_processor, 'compile_latex_to_pdf',
                         return_value=False) as mock_compile, \
             patch.object(document_service, '_save_text_file'):
            
            # Should not raise exception even if PDF compilation fails
            document_service._generate_resume_files(
                sample_resume_content, sample_user_data, sample_company_info, output_dir
            )
            
            mock_compile.assert_called_once()


# End-to-End Tests - Real file operations
@pytest.mark.e2e
class TestDocumentServiceE2E:
    """End-to-end tests for DocumentService with real file operations"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def document_service_e2e(self, temp_dir):
        """Create DocumentService with real file system"""
        with patch('core.services.document_service.Settings') as mock_settings:
            mock_settings.setup_directories.return_value = None
            mock_settings.APPLICATIONS_DIR = temp_dir / "applications"
            mock_settings.TEMPLATES_DIR = temp_dir / "templates"
            
            # Create the directories
            mock_settings.APPLICATIONS_DIR.mkdir(parents=True, exist_ok=True)
            mock_settings.TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
            
            # Create mock template files
            resume_template = mock_settings.TEMPLATES_DIR / "resume_template.tex"
            cover_letter_template = mock_settings.TEMPLATES_DIR / "cover_letter_template.tex"
            
            with open(resume_template, 'w') as f:
                f.write("\\documentclass{article}\n\\begin{document}\n((( name )))\n\\end{document}")
            
            with open(cover_letter_template, 'w') as f:
                f.write("\\documentclass{letter}\n\\begin{document}\n{{APPLICANT_NAME}}\n\\end{document}")
            
            return DocumentService()
    
    def test_end_to_end_application_package_generation(self, document_service_e2e, temp_dir,
                                                      sample_resume_content, sample_cover_letter,
                                                      sample_user_data, sample_company_info,
                                                      sample_job_description):
        """Test complete end-to-end application package generation"""
        # Mock PDF compilation to avoid LaTeX dependency
        with patch.object(document_service_e2e.latex_processor, 'compile_latex_to_pdf',
                         return_value=True):
            
            result_dir = document_service_e2e.generate_application_package(
                sample_resume_content, sample_cover_letter, sample_user_data,
                sample_company_info, sample_job_description
            )
            
            # Verify directory was created
            assert result_dir.exists()
            assert result_dir.is_dir()
            
            # Verify files were created
            files = list(result_dir.glob("*"))
            file_names = [f.name for f in files]
            
            # Should have LaTeX files and job description
            assert any("Resume" in name and name.endswith(".tex") for name in file_names)
            assert any("CoverLetter" in name and name.endswith(".tex") for name in file_names)
            assert any("JD.md" in name for name in file_names)
            
            # Check job description content
            job_desc_files = [f for f in files if f.name.endswith("JD.md")]
            assert len(job_desc_files) == 1
            
            with open(job_desc_files[0], 'r') as f:
                content = f.read()
                assert "TechCorp Inc - Senior-Software-Engineer" in content
                assert sample_job_description in content
    
    def test_real_file_operations(self, document_service_e2e, temp_dir):
        """Test real file operations"""
        test_file = temp_dir / "test.txt"
        test_content = "This is test content with special chars: àáâãäåæçèé"
        
        document_service_e2e._save_text_file(test_file, test_content)
        
        # Verify file was created and content is correct
        assert test_file.exists()
        with open(test_file, 'r', encoding='utf-8') as f:
            saved_content = f.read()
            assert saved_content == test_content
    
    def test_directory_structure_creation(self, document_service_e2e, sample_company_info):
        """Test real directory structure creation"""
        with patch('core.services.document_service.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "06-18-25"
            
            result_dir = document_service_e2e._create_application_output_directory(sample_company_info)
            
            # Verify directory was actually created
            assert result_dir.exists()
            assert result_dir.is_dir()
            assert "TechCorp-Inc" in result_dir.name
            assert "Senior-Software-Engineer" in result_dir.name
    
    def test_file_permission_errors(self, document_service_e2e, temp_dir):
        """Test handling of file permission errors"""
        # Create a directory and make it read-only
        readonly_dir = temp_dir / "readonly"
        readonly_dir.mkdir()
        readonly_dir.chmod(0o444)  # Read-only
        
        try:
            test_file = readonly_dir / "test.txt"
            
            with pytest.raises(PermissionError):
                document_service_e2e._save_text_file(test_file, "test content")
        finally:
            # Restore permissions for cleanup
            readonly_dir.chmod(0o755)
    
    def test_large_content_handling(self, document_service_e2e, temp_dir):
        """Test handling of large file content"""
        large_content = "Lorem ipsum " * 10000  # Large content
        test_file = temp_dir / "large_file.txt"
        
        document_service_e2e._save_text_file(test_file, large_content)
        
        assert test_file.exists()
        with open(test_file, 'r', encoding='utf-8') as f:
            saved_content = f.read()
            assert len(saved_content) == len(large_content)
            assert saved_content == large_content

    def test_real_latex_compilation_integration(self, document_service_e2e, temp_dir,
                                            sample_resume_content, sample_cover_letter,
                                            sample_user_data, sample_company_info,
                                            sample_job_description):
        """Test real LaTeX compilation and PDF generation with existing templates"""
        # Run the full pipeline WITHOUT mocking LaTeX compilation
        result_dir = document_service_e2e.generate_application_package(
            sample_resume_content, sample_cover_letter, sample_user_data,
            sample_company_info, sample_job_description
        )
        
        # Verify all files were created
        files = list(result_dir.glob("*"))
        file_names = [f.name for f in files]
        
        # Check that both LaTeX and PDF files exist
        latex_files = [f for f in files if f.name.endswith(".tex")]
        pdf_files = [f for f in files if f.name.endswith(".pdf")]
        
        assert len(latex_files) >= 2, "Should have resume and cover letter LaTeX files"
        assert len(pdf_files) >= 2, "Should have resume and cover letter PDF files"
        
        # Verify PDF files are actual PDF files (not empty or corrupted)
        for pdf_file in pdf_files:
            assert pdf_file.stat().st_size > 1000, f"PDF file {pdf_file.name} seems too small"
            
            # Read first few bytes to verify it's a real PDF
            with open(pdf_file, 'rb') as f:
                header = f.read(4)
                assert header == b'%PDF', f"File {pdf_file.name} is not a valid PDF"
        
        # Verify LaTeX files contain processed template content
        resume_latex_file = next((f for f in latex_files if "Resume" in f.name), None)
        cover_letter_latex_file = next((f for f in latex_files if "CoverLetter" in f.name), None)
        
        assert resume_latex_file is not None, "Resume LaTeX file not found"
        assert cover_letter_latex_file is not None, "Cover letter LaTeX file not found"
        
        # Check that template processing actually occurred
        with open(resume_latex_file, 'r', encoding='utf-8') as f:
            resume_content = f.read()
            # Verify it's using altacv documentclass from the template
            assert "\\documentclass[10pt,a4paper,ragged2e,withhyper]{altacv}" in resume_content
            # Verify template placeholders were replaced
            assert "(((" not in resume_content, "Jinja2 template placeholders should be replaced"
            assert sample_user_data['applicant_info']['name'] in resume_content
        
        with open(cover_letter_latex_file, 'r', encoding='utf-8') as f:
            cover_letter_content = f.read()
            # Verify it's using letter documentclass from the template
            assert "\\documentclass[11pt,a4paper]{letter}" in cover_letter_content
            # Verify template placeholders were replaced
            assert "{{" not in cover_letter_content, "Template placeholders should be replaced"
            assert sample_user_data['applicant_info']['name'] in cover_letter_content
            assert sample_company_info['company_name'] in cover_letter_content


    def test_template_processing_and_content_verification(self, document_service_e2e, temp_dir,
                                                        sample_resume_content, sample_cover_letter,
                                                        sample_user_data, sample_company_info,
                                                        sample_job_description):
        """Test that existing templates are correctly processed and contain expected content"""
        # Mock PDF compilation to focus on template processing verification
        with patch.object(document_service_e2e.latex_processor, 'compile_latex_to_pdf',
                        return_value=True):
            
            result_dir = document_service_e2e.generate_application_package(
                sample_resume_content, sample_cover_letter, sample_user_data,
                sample_company_info, sample_job_description
            )
        
        # Get generated files
        latex_files = list(result_dir.glob("*.tex"))
        resume_file = next((f for f in latex_files if "Resume" in f.name), None)
        cover_letter_file = next((f for f in latex_files if "CoverLetter" in f.name), None)
        
        assert resume_file is not None, "Resume LaTeX file should exist"
        assert cover_letter_file is not None, "Cover letter LaTeX file should exist"
        
        # Verify resume template processing
        with open(resume_file, 'r', encoding='utf-8') as f:
            resume_content = f.read()
        
        # Check that the altacv template structure is preserved
        assert "\\documentclass[10pt,a4paper,ragged2e,withhyper]{altacv}" in resume_content
        assert "\\name{" in resume_content
        assert "\\tagline{" in resume_content
        assert "\\personalinfo{" in resume_content
        assert "\\makecvheader" in resume_content
        
        # Check personal information was filled from user_data
        user_info = sample_user_data['applicant_info']
        assert f"\\name{{{user_info['name']}}}" in resume_content
        assert f"\\email{{{user_info['email']}}}" in resume_content
        
        # Check conditional fields are handled properly
        if 'phone' in user_info and user_info['phone']:
            assert f"\\phone{{{user_info['phone']}}}" in resume_content
        
        # Check that resume content sections are processed
        if 'work_experience' in sample_resume_content:
            assert "\\cvsection{Experience}" in resume_content
            for exp in sample_resume_content['work_experience']:
                assert exp['company_name'] in resume_content
                assert exp['role_title'] in resume_content
        
        if 'education' in sample_resume_content:
            assert "\\cvsection{Higher Education}" in resume_content
            for edu in sample_resume_content['education']:
                assert edu['institution_name'] in resume_content
                assert edu['degree_name'] in resume_content
        
        if 'skills' in sample_resume_content:
            assert "\\cvsection{Skills}" in resume_content
            for skill in sample_resume_content['skills']:
                assert skill['category'] in resume_content
        
        if 'projects' in sample_resume_content:
            assert "\\cvsection{Notable ML Projects}" in resume_content
            for project in sample_resume_content['projects']:
                assert project['project_title'] in resume_content
        
        # Verify no template syntax remains
        assert "(((" not in resume_content, "Jinja2 syntax should be completely processed"
        assert ")))" not in resume_content, "Jinja2 syntax should be completely processed"
        assert "((*" not in resume_content, "Jinja2 conditional syntax should be processed"
        assert "*-))" not in resume_content, "Jinja2 conditional syntax should be processed"
        
        # Verify cover letter template processing
        with open(cover_letter_file, 'r', encoding='utf-8') as f:
            cover_letter_content = f.read()
        
        # Check that the letter template structure is preserved
        assert "\\documentclass[11pt,a4paper]{letter}" in cover_letter_content
        assert "\\signature{" in cover_letter_content
        assert "\\address{" in cover_letter_content
        assert "\\begin{letter}{" in cover_letter_content
        assert "\\opening{Dear Hiring Manager,}" in cover_letter_content
        assert "\\closing{Sincerely,}" in cover_letter_content
        
        # Check all placeholders were replaced with actual data
        assert f"\\signature{{{user_info['name']}}}" in cover_letter_content
        assert f"{user_info['email']}" in cover_letter_content
        assert f"{user_info['phone']}" in cover_letter_content
        assert f"{sample_company_info['company_name']}" in cover_letter_content
        assert sample_cover_letter in cover_letter_content
        
        # Verify no template syntax remains
        assert "{{NAME}}" not in cover_letter_content, "NAME placeholder should be replaced"
        assert "{{EMAIL}}" not in cover_letter_content, "EMAIL placeholder should be replaced"
        assert "{{PHONE}}" not in cover_letter_content, "PHONE placeholder should be replaced"
        assert "{{COMPANY_NAME}}" not in cover_letter_content, "COMPANY_NAME placeholder should be replaced"
        assert "{{COVER_LETTER_CONTENT}}" not in cover_letter_content, "COVER_LETTER_CONTENT placeholder should be replaced"



# # Run only unit tests
# pytest src/test/unit/services/document_svc_tests/test_document_service.py -m unit -xvs

# # Run only integration tests
# pytest src/test/unit/services/document_svc_tests/test_document_service.py -m integration -xvs

# # Run only end-to-end tests
# pytest src/test/unit/services/document_svc_tests/test_document_service.py -m e2e -xvs

# # Run all tests
# pytest src/test/unit/services/document_svc_tests/test_document_service.py -xvs

# # Run specific test method
# pytest src/test/unit/services/document_svc_tests/test_document_service.py::TestDocumentServiceUnit::test_create_application_output_directory -xvs

# # Run specific test class
# pytest ssrc/test/unit/services/document_svc_tests/test_document_service.py::TestDocumentServiceUnit -xvs

# # Run tests with coverage
# pytest src/test/unit/services/document_svc_tests/test_document_service.py -m unit --cov=core.services.document_service -xvs

# # Run tests and stop on first failure
# pytest src/test/unit/services/document_svc_tests/test_document_service.py -m integration -x