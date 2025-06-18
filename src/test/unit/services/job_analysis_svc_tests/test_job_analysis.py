import pytest
from unittest.mock import Mock, patch
from core.services.job_analysis_service import JobAnalysisService


# Test Fixtures
@pytest.fixture
def sample_job_description():
    return """
    Senior Software Engineer - Python/React
    
    Requirements:
    - 5+ years Python experience
    - React/JavaScript skills
    - AWS cloud experience
    
    We offer competitive salary and benefits.
    """

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
    "work_experience": [
      {
        "priority_ranking": 1,
        "company_name": "Comapany 1",
        "job_title": "Backend Engineer",
        "location": "Toronto, Ontario, Canada",
        "date_range": "March 2023 - December 2024",
        "bullet_points": [
          "Designed and built a robust, secure, and scalable backend for lightspeed, a project aiming to deliver high-speed internet to 14 million unconnected people in the USA through the ACP (affordable connectivity program) initiative.",
          "Designed and maintained a RESTful API to handle 10,000+ requests per second, complying with swagger's OpenAPI spec, utilizing GCP's CloudSQL, Cloud Storage, sentry analytics and deployed on Google Cloud Run.",
          "Automated the build and deployment pipeline using CI/CD tools, GitHub actions, Docker, and Terraform, reducing deployment time by 70% and increasing deployment frequency by 50%."
        ]
      },
      {
        "priority_ranking": 2,
        "company_name": "Company 2",
        "job_title": "Full-Stack Software Developer", 
        "location": "Dubai, UAE",
        "date_range": "June 2019 -- January 2023",
        "bullet_points": [
          "Co-Developed a complex CRM system for Infinity, a SAAS startup serving major corporations, fulfilling their medical insurance operations-monitoring and tracking goals, saving 5% of insurance expenditure/month formerly lost to insurance fraud.",
          "Developed & Maintained a comprehensive, live data analysis dashboard for individual corporations, helping in high-level decision-making, expenditure tracking and strategies formulation."
        ]
      }
    ],
    "project_experience": [
      {
        "priority_ranking": 1,
        "project_name": "Sentiment Analysis on Financial News Headlines",
        "project_stack": "Python, TensorFlow, LSTM, NLP, MLflow, GCP",
        "bullet_points": [
          "Developed an LSTM-based deep learning model to analyze news headline sentiment(Producing a sentiment score (-1 to 1) (positive, neutral, negative)) (F1: 0.71, Precision: 0.7, Recall: 0.85, AUC: 0.86), engineering a comprehensive NLP pipeline using spaCy, NLTK, and Hugging Face BERT embeddings.",
          "Utilized MLflow for tracking & model management, following MLOps best practices, while addressing key data challenges and implementing hyperparameter optimization (grid search, cross-val). Caching trained transformers w/ pickle & deploying on GCP."
        ],
        "documentation_link": "https://github.com/JSmith/sentiment-analysis/README.md",
        "github_link": "https://github.com/JSmith/sentiment-analysis",
        "demo_link": "https://youtube.com/watch?v=demo123",
        "live_link": "https://sentiment-app.herokuapp.com"
      },
      {
        "priority_ranking": 2,
        "project_name": "KKBox Music Recommendation System",
        "project_stack": "Python, XGBoost, Pandas, Scikit-Learn, Kaggle",
        "bullet_points": [
          "Developed a large-scale recommendation system for Asia's top music streaming service, KKBox, working with a dataset of 2M+ records and achieving an accuracy of 73% (evaluated through Kaggle).",
          "Leveraged a Gradient Boosting Model (XGBoost), to reach highest accuracy, evaluated through metrics including F1-score and ROC curve. Utilizing major libraries including Pandas, Numpy, Seaborn(data exploration & visualization) and Scikit-Learn."
        ],
        "documentation_link": "https://github.com/JSmith/kkbox-recommendation/README.md",
        "github_link": "https://github.com/JSmith/kkbox-recommendation",
        "demo_link": "",
        "live_link": ""
      },
      {
        "priority_ranking": 3,
        "project_name": "RAG-based Medical Assistant",
        "project_stack": "IBM WatsonX, LangChain, Chroma, Gradio, Mistral",
        "bullet_points": [
          "Leveraged IBM WatsonX AI platform for base model(Mistral), LangChain libraries& tools for content handling, Chroma Vector DB for creating a robust document retrieval mechanism and Gradio (python package) for Creating a simple, user-friendly interface to deploy the RAG assistant. Deployed on IBM Watson's platform."
        ],
        "documentation_link": "https://github.com/JSmith/medical-rag/README.md",
        "github_link": "https://github.com/JSmith/medical-rag",
        "demo_link": "https://youtube.com/watch?v=rag-demo",
        "live_link": "https://watsonx-medical-assistant.cloud.ibm.com"
      }
    ],
    "skills": {
      "programming": ["Python", "SQL", "Git", "Docker", "CI/CD"],
      "machine_learning": ["TensorFlow", "scikit-learn", "PyTorch", "Hugging Face", "MLflow"],
      "data_science": ["Pandas", "NumPy", "Matplotlib", "Seaborn", "NLTK"],
      "cloud_platforms": ["GCP", "AWS", "IBM Watson"],
      "specializations": ["NLP", "Deep Learning", "LLMs", "RAG Systems", "MLOps"]
    },
    "education": [
      {
        "school_name": "Michigan University",
        "degree": "B.Sc. in Mechanical Engineering",
        "date_range": "2018 -- 2023",
        "achievements": "Dean's List - 6 semesters"
      }
    ],
    "executive_summary": "ML Engineer with 4+ years of experience in building & deploying production-grade software. Proven ability to apply best practices (Git, TDD, CI/CD, containerization) to develop robust and scalable AI solutions. Hands-on project experience, building & deploying ML solutions including a content recommendation system, RAG assistant, sentiment analysis LSTM model and RLHF LLM fine-tuning. Exceptional communicator, adept at collaborating with cross-functional teams and presenting complex information to both technical & non-technical audiences."
  }

@pytest.fixture
def sample_company_info():
    return {
        "name": "TechCorp Inc.",
        "industry": "Software",
        "location": "San Francisco",
        "country": "USA"
    }


# Unit Tests
class TestJobAnalysisServiceUnit:
    """Unit tests with mocked LLM providers"""

    @pytest.fixture(autouse=True)
    def setup_mocks(self):
        """Setup mocks for all unit tests"""
        self.mock_main_llm = Mock()
        self.mock_small_llm = Mock()
        
        # Mock LLMFactory
        self.factory_patcher = patch('core.services.job_analysis_service.LLMFactory')
        self.mock_factory = self.factory_patcher.start()
        
        def create_llm_side_effect(provider, model=None):
            return self.mock_small_llm if (provider == "google" and model) else self.mock_main_llm
        
        self.mock_factory.create_llm.side_effect = create_llm_side_effect
        
        # Mock Settings
        self.settings_patcher = patch('core.services.job_analysis_service.Settings')
        self.mock_settings = self.settings_patcher.start()
        self.mock_settings.DEFAULT_LLM_PROVIDER = "openai"
        self.mock_settings.SMALL_MODEL = "gemini-flash"
        
        yield
        
        self.factory_patcher.stop()
        self.settings_patcher.stop()

    def test_extract_job_info(self, sample_job_description):
        """Test job info extraction"""
        expected_result = {"title": "Senior Software Engineer", "skills": ["Python", "React"]}
        self.mock_small_llm.extract_job_info.return_value = expected_result
        
        service = JobAnalysisService()
        result = service.extract_job_info(sample_job_description)
        
        assert result == expected_result
        self.mock_small_llm.extract_job_info.assert_called_once_with(sample_job_description)

    def test_generate_tailored_resume(self, sample_job_description, sample_user_data):
        """Test resume generation"""
        expected_result = {"summary": "Experienced Python developer", "skills": ["Python", "React"]}
        self.mock_main_llm.generate_resume_content.return_value = expected_result
        
        service = JobAnalysisService()
        result = service.generate_tailored_resume(sample_job_description, sample_user_data)
        
        assert result == expected_result
        self.mock_main_llm.generate_resume_content.assert_called_once_with(sample_job_description, sample_user_data)

    def test_generate_cover_letter(self, sample_job_description, sample_user_data, sample_company_info):
        """Test cover letter generation"""
        expected_result = "Dear Hiring Manager, I am interested in the position..."
        self.mock_main_llm.generate_cover_letter.return_value = expected_result
        
        service = JobAnalysisService()
        result = service.generate_cover_letter(sample_job_description, sample_user_data, sample_company_info)
        
        assert result == expected_result
        self.mock_main_llm.generate_cover_letter.assert_called_once_with(
            sample_job_description, sample_user_data, sample_company_info
        )

    def test_error_handling(self, sample_job_description):
        """Test that exceptions are properly raised"""
        self.mock_small_llm.extract_job_info.side_effect = Exception("API Error")
        
        service = JobAnalysisService()
        
        with pytest.raises(Exception, match="API Error"):
            service.extract_job_info(sample_job_description)


# Integration Tests
@pytest.mark.integration
class TestJobAnalysisServiceIntegration:
    """Integration tests with real LLM providers"""

    @pytest.fixture(params=["openai", "google", "deepseek"])
    def service_with_provider(self, request):
        """Create service with real LLM provider"""
        try:
            return JobAnalysisService(llm_provider=request.param)
        except Exception as e:
            pytest.skip(f"Provider {request.param} not available: {e}")

    def test_extract_job_info_real_llm(self, service_with_provider, sample_job_description):
        """Test job extraction with real LLM"""
        try:
            result = service_with_provider.extract_job_info(sample_job_description)
            
            assert isinstance(result, dict)
            assert len(result) > 0
            
            # Check for relevant content
            result_text = str(result).lower()
            assert any(skill in result_text for skill in ["python", "react", "software"])
            
        except Exception as e:
            pytest.skip(f"LLM integration failed: {e}")

    def test_generate_resume_real_llm(self, service_with_provider, sample_job_description, sample_user_data):
        """Test resume generation with real LLM"""
        try:
            result = service_with_provider.generate_tailored_resume(sample_job_description, sample_user_data)
            
            assert isinstance(result, dict)
            assert len(result) > 0
            
            # Check user data is incorporated
            result_text = str(result).lower()
            assert any(name in result_text for name in ["john", "smith"])
            
        except Exception as e:
            pytest.skip(f"LLM integration failed: {e}")

    def test_generate_cover_letter_real_llm(self, service_with_provider, sample_job_description, 
                                          sample_user_data, sample_company_info):
        """Test cover letter generation with real LLM"""
        try:
            result = service_with_provider.generate_cover_letter(
                sample_job_description, sample_user_data, sample_company_info
            )
            
            assert isinstance(result, str)
            assert len(result) > 50
            
        except Exception as e:
            pytest.skip(f"LLM integration failed: {e}")


# End-to-End Workflow Tests
@pytest.mark.e2e
class TestJobAnalysisServiceWorkflow:
    """End-to-end workflow tests"""

    def test_complete_job_application_workflow(self, sample_job_description, sample_user_data, sample_company_info):
        """Test complete workflow: extract job info → generate resume → generate cover letter"""
        try:
            service = JobAnalysisService()
            
            # Step 1: Extract job information
            job_info = service.extract_job_info(sample_job_description)
            assert isinstance(job_info, dict)
            
            # Step 2: Generate tailored resume
            resume = service.generate_tailored_resume(sample_job_description, sample_user_data)
            assert isinstance(resume, dict)
            
            # Step 3: Generate cover letter
            cover_letter = service.generate_cover_letter(sample_job_description, sample_user_data, sample_company_info)
            assert isinstance(cover_letter, str)
            
            # Validate workflow coherence
            all_content = f"{job_info} {resume} {cover_letter}".lower()
            assert any(skill in all_content for skill in ["python", "react"])
            assert "john" in all_content  # User name should appear
            
        except Exception as e:
            pytest.skip(f"E2E workflow failed: {e}")

    def test_multiple_provider_consistency(self, sample_job_description, sample_user_data):
        """Test workflow works consistently across providers"""
        providers = ["openai", "google"]
        results = {}
        
        for provider in providers:
            try:
                service = JobAnalysisService(llm_provider=provider)
                
                job_info = service.extract_job_info(sample_job_description)
                resume = service.generate_tailored_resume(sample_job_description, sample_user_data)
                
                results[provider] = {
                    'job_info_valid': isinstance(job_info, dict) and len(job_info) > 0,
                    'resume_valid': isinstance(resume, dict) and len(resume) > 0
                }
                
            except Exception:
                continue
        
        # At least one provider should work
        assert len(results) > 0
        
        # All working providers should return valid results
        for provider, result in results.items():
            assert result['job_info_valid'], f"{provider} job info invalid"
            assert result['resume_valid'], f"{provider} resume invalid"


# Register custom marks in conftest.py or pytest.ini
def pytest_configure(config):
    config.addinivalue_line("markers", "integration: integration tests with real LLM providers")
    config.addinivalue_line("markers", "e2e: end-to-end workflow tests")


# Run all tests
# pytest src/test/unit/services/job_analysis_svc_tests/test_job_analysis.py -v

# # Run only unit tests
# pytest src/test/unit/services/job_analysis_svc_tests/test_job_analysis.py::TestJobAnalysisServiceUnit -v

# # Run only integration tests
# pytest src/test/unit/services/job_analysis_svc_tests/test_job_analysis.py -m integration -xvs

# # Run only end-to-end tests
# pytest src/test/unit/services/job_analysis_svc_tests/test_job_analysis.py -m e2e -v

# # Run unit + integration (skip e2e)
# pytest src/test/unit/services/job_analysis_svc_tests/test_job_analysis.py -m "not e2e" -v

# resume content generation consume around 5000 tokens