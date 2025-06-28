import pytest
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

from core.application_generator import ApplicationGenerator



def create_application_generator(llm_provider: str = None) -> ApplicationGenerator:
    """Factory function to create ApplicationGenerator with all dependencies"""
    from core.database.database_manager import DatabaseManager
    from core.services.document_service import DocumentService
    from core.services.job_analysis_service import JobAnalysisService
    from core.services.user_data_service import UserDataService

    
    user_data_service = UserDataService()
    document_service = DocumentService()
    job_analysis_service = JobAnalysisService(llm_provider)
    database_manager = DatabaseManager()
    
    return ApplicationGenerator(
        user_data_service=user_data_service,
        document_service=document_service,
        job_analysis_service=job_analysis_service,
        database_manager=database_manager
    )


@pytest.fixture
def sample_job_description() -> str:
    """Sample job description for testing"""
    return """
Software Engineer - Backend Development

TechCorp Inc. is seeking a talented Backend Software Engineer to join our growing engineering team. 

About the Role:
We are looking for an experienced software engineer to design, develop, and maintain scalable backend systems that power our platform serving millions of users worldwide.

Key Responsibilities:
- Design and implement robust, scalable backend services using Python, Java, or Go
- Collaborate with cross-functional teams to deliver high-quality software solutions
- Optimize database performance and ensure data integrity
- Implement monitoring, logging, and alerting systems
- Participate in code reviews and maintain high coding standards
- Troubleshoot and resolve production issues

Required Qualifications:
- Bachelor's degree in Computer Science or related field
- 3+ years of experience in backend software development
- Strong proficiency in at least one backend programming language (Python, Java, Go)
- Experience with relational databases (PostgreSQL, MySQL) and NoSQL databases
- Knowledge of RESTful API design and microservices architecture
- Experience with cloud platforms (AWS, GCP, or Azure)
- Understanding of CI/CD pipelines and DevOps practices

Preferred Qualifications:
- Experience with containerization technologies (Docker, Kubernetes)
- Knowledge of message queuing systems (RabbitMQ, Apache Kafka)
- Experience with monitoring tools (Prometheus, Grafana)
- Familiarity with agile development methodologies

What We Offer:
- Competitive salary and equity package
- Comprehensive health, dental, and vision insurance
- Flexible work arrangements
- Professional development opportunities
- Modern office in downtown San Francisco

Company: TechCorp Inc.
Location: San Francisco, CA
Employment Type: Full-time
Experience Level: Mid-level (3-5 years)
"""


@pytest.mark.prod
def test_application_generator_full_workflow(sample_job_description: str):
    """
    Production test for ApplicationGenerator - tests the complete workflow
    with actual services and produces real output files and database entries.
    
    This test exercises the happy path scenario where all services work correctly
    and verifies that the complete application package is generated successfully.
    """
    # Arrange
    app_generator = create_application_generator()
    
    # Act
    result = app_generator.generate_application(sample_job_description)
    
    # Assert - Check that the operation was successful
    assert result.success is True, f"Application generation failed: {result.error}"
    assert result.error is None, "No error should be present on successful generation"
    
    # Assert - Check that application ID was generated and saved to database
    assert result.application_id is not None, "Application ID should be generated"
    assert isinstance(result.application_id, int), "Application ID should be an integer"
    
    # Assert - Check that company info was extracted
    assert result.company_info is not None, "Company info should be extracted"
    assert isinstance(result.company_info, dict), "Company info should be a dictionary"
    assert 'company_name' in result.company_info, "Company name should be present"
    assert 'job_title' in result.company_info, "Job title should be present"
    
    # Assert - Check that output directory was created
    assert result.output_directory is not None, "Output directory should be created"
    assert isinstance(result.output_directory, Path), "Output directory should be a Path object"
    assert result.output_directory.exists(), "Output directory should exist on filesystem"
    assert result.output_directory.is_dir(), "Output directory should be a directory"
    
    # Verify directory structure and naming convention
    dir_name = result.output_directory.name
    assert dir_name.startswith(f"app_{result.application_id}"), f"Directory should start with application ID"
    
    # Assert - Check that resume files were generated
    company_name = result.company_info.get('company_name', 'Company').replace(' ', '')
    user_name_pattern = "*_Resume-*.tex"  # Using pattern since we don't know exact user name
    
    resume_latex_files = list(result.output_directory.glob(user_name_pattern))
    assert len(resume_latex_files) >= 1, "Resume LaTeX file should be generated"
    
    resume_pdf_pattern = "*_Resume-*.pdf"
    resume_pdf_files = list(result.output_directory.glob(resume_pdf_pattern))
    assert len(resume_pdf_files) >= 1, "Resume PDF file should be generated"
    
    # Verify resume files exist and have content
    resume_latex_file = resume_latex_files[0]
    resume_pdf_file = resume_pdf_files[0]
    
    assert resume_latex_file.exists(), "Resume LaTeX file should exist"
    assert resume_latex_file.stat().st_size > 0, "Resume LaTeX file should not be empty"
    
    assert resume_pdf_file.exists(), "Resume PDF file should exist"
    assert resume_pdf_file.stat().st_size > 0, "Resume PDF file should not be empty"
    
    # Assert - Check that cover letter files were generated
    cover_letter_latex_pattern = "*_CoverLetter-*.tex"
    cover_letter_latex_files = list(result.output_directory.glob(cover_letter_latex_pattern))
    assert len(cover_letter_latex_files) >= 1, "Cover letter LaTeX file should be generated"
    
    cover_letter_pdf_pattern = "*_CoverLetter-*.pdf"
    cover_letter_pdf_files = list(result.output_directory.glob(cover_letter_pdf_pattern))
    assert len(cover_letter_pdf_files) >= 1, "Cover letter PDF file should be generated"
    
    # Verify cover letter files exist and have content
    cover_letter_latex_file = cover_letter_latex_files[0]
    cover_letter_pdf_file = cover_letter_pdf_files[0]
    
    assert cover_letter_latex_file.exists(), "Cover letter LaTeX file should exist"
    assert cover_letter_latex_file.stat().st_size > 0, "Cover letter LaTeX file should not be empty"
    
    assert cover_letter_pdf_file.exists(), "Cover letter PDF file should exist"
    assert cover_letter_pdf_file.stat().st_size > 0, "Cover letter PDF file should not be empty"
    
    # Assert - Check that job description file was generated
    job_description_pattern = "*-JD.md"
    job_description_files = list(result.output_directory.glob(job_description_pattern))
    assert len(job_description_files) >= 1, "Job description markdown file should be generated"
    
    job_description_file = job_description_files[0]
    assert job_description_file.exists(), "Job description file should exist"
    assert job_description_file.stat().st_size > 0, "Job description file should not be empty"
    
    # Verify job description content
    with open(job_description_file, 'r', encoding='utf-8') as f:
        jd_content = f.read()
    assert len(jd_content) > 0, "Job description file should have content"
    assert result.company_info.get('company_name', '') in jd_content, "Job description should contain company name"
    
    # Assert - Verify all expected files are present (should have at least 5 files total)
    all_files = list(result.output_directory.iterdir())
    file_count = len([f for f in all_files if f.is_file()])
    assert file_count >= 5, f"Should have at least 5 files (2 resume, 2 cover letter, 1 JD), found {file_count}"
    
    print(f"✅ Production test completed successfully!")
    print(f"📁 Output directory: {result.output_directory}")
    print(f"🆔 Application ID: {result.application_id}")
    print(f"🏢 Company: {result.company_info.get('company_name')}")
    print(f"💼 Position: {result.company_info.get('job_title')}")
    print(f"📄 Generated files: {file_count}")


# Usage example
# pytest -m prod src/test/unit/application_generation/application_generation_prod_tests.py -xsvv
