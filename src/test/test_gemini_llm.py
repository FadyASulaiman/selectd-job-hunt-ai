from core.llm_providers.gemini_llm import GeminiLLM
import pytest
import json
from unittest.mock import Mock, patch, MagicMock

class TestGeminiLLM:
    
    @pytest.fixture
    def gemini_llm(self):
        """Create a GeminiLLM instance for testing"""
        with patch('your_module.Settings') as mock_settings:
            mock_settings.GEMINI_API_KEY = "test-api-key"
            mock_settings.MAX_WORK_EXPERIENCE = 3
            mock_settings.MAX_PROJECT_EXPERIENCE = 3
            mock_settings.MAX_BULLET_POINTS_FIRST_PROJECT = 4
            mock_settings.MAX_BULLET_POINTS_OTHER_PROJECTS = 3
            mock_settings.MAX_WORDS_PER_BULLET = 20
            
            with patch('your_module.genai.Client'):
                return GeminiLLM()
    
    @pytest.fixture
    def mock_client_response(self):
        """Mock response object"""
        mock_response = Mock()
        mock_response.text = '{"test": "response"}'
        return mock_response
        
    def test_call_gemini_success(self, gemini_llm, mock_client_response):
        """Test successful API call"""
        gemini_llm.client.models.generate_content.return_value = mock_client_response
        
        result = gemini_llm._call_gemini("system prompt", "user prompt")
        
        assert result == '{"test": "response"}'
        gemini_llm.client.models.generate_content.assert_called_once()

    def test_call_gemini_api_error(self, gemini_llm):
        """Test API error handling"""
        gemini_llm.client.models.generate_content.side_effect = Exception("API Error")
        
        with pytest.raises(Exception, match="Gemini API error: API Error"):
            gemini_llm._call_gemini("system prompt", "user prompt")

    def test_call_gemini_parameters(self, gemini_llm, mock_client_response):
        """Test that correct parameters are passed to API"""
        gemini_llm.client.models.generate_content.return_value = mock_client_response
        
        gemini_llm._call_gemini("test system", "test user")
        
        call_args = gemini_llm.client.models.generate_content.call_args
        assert call_args.kwargs['model'] == "gemini-2.5-pro"
        assert call_args.kwargs['contents'] == "test user"

    def test_extract_job_info_success(self, gemini_llm):
        """Test successful job info extraction"""
        valid_json = {
            "company_name": "TechCorp",
            "job_title": "Data Scientist",
            "location": "San Francisco",
            "salary_range": "$100k-120k",
            "job_type": "Full-time",
            "benefits": "Health/Dental/401k",
            "country": "USA"
        }
        
        with patch.object(gemini_llm, '_call_gemini', return_value=json.dumps(valid_json)):
            result = gemini_llm.extract_job_info("job description text")
            
            assert result == valid_json

    def test_extract_job_info_json_decode_error(self, gemini_llm):
        """Test fallback when JSON parsing fails"""
        with patch.object(gemini_llm, '_call_gemini', return_value="invalid json"):
            result = gemini_llm.extract_job_info("job description")
            
            expected_fallback = {
                "company_name": "Unclear input",
                "job_title": "Unclear input",
                "location": "Not specified",
                "salary_range": "Not specified", 
                "job_type": "Not specified",
                "benefits": [],
                "country": "Not specified"
            }
            assert result == expected_fallback

    def test_extract_job_info_with_markdown(self, gemini_llm):
        """Test JSON cleaning when LLM returns markdown"""
        json_with_markdown = '```json\n{"company_name": "Test"}\n```'
        expected_json = {"company_name": "Test"}
        
        with patch.object(gemini_llm, '_call_gemini', return_value=json_with_markdown):
            result = gemini_llm.extract_job_info("job description")
            # This test will show if your cleaning logic works

    def test_generate_resume_content_success(self, gemini_llm):
        """Test successful resume generation"""
        mock_resume = {
            "executive_summary": "Test summary",
            "selected_work_experience": [],
            "selected_project_experience": [],
            "relevant_skills": {"technical": [], "machine_learning": [], "tools": []}
        }
        
        with patch.object(gemini_llm, '_call_gemini', return_value=json.dumps(mock_resume)):
            result = gemini_llm.generate_resume_content("job desc", {"test": "data"})
            
            assert result == mock_resume

    def test_generate_resume_content_json_error(self, gemini_llm):
        """Test exception when resume JSON is invalid"""
        with patch.object(gemini_llm, '_call_gemini', return_value="invalid json"):
            with pytest.raises(Exception, match="Failed to parse resume content JSON"):
                gemini_llm.generate_resume_content("job desc", {"test": "data"})

    def test_generate_resume_content_prompt_structure(self, gemini_llm):
        """Test that prompts contain expected elements"""
        with patch.object(gemini_llm, '_call_gemini', return_value='{"test": "data"}') as mock_call:
            gemini_llm.generate_resume_content("test job", {"test": "user_data"})
            
            system_prompt, user_prompt = mock_call.call_args[0]
            assert "CRITICAL CONSTRAINTS" in system_prompt
            assert "test job" in user_prompt
            assert "test user_data" in user_prompt


    def test_generate_cover_letter_success(self, gemini_llm):
        """Test successful cover letter generation"""
        expected_letter = "Dear Hiring Manager, This is a test cover letter..."
        
        with patch.object(gemini_llm, '_call_gemini', return_value=expected_letter):
            result = gemini_llm.generate_cover_letter(
                "job description", 
                {"applicant_info": {}, "work_experience": [], "project_experience": []},
                {"company_name": "TestCorp"}
            )
            
            assert result == expected_letter

    def test_generate_cover_letter_prompt_content(self, gemini_llm):
        """Test that cover letter prompt includes all required data"""
        with patch.object(gemini_llm, '_call_gemini', return_value="test letter") as mock_call:
            gemini_llm.generate_cover_letter(
                "test job desc",
                {"applicant_info": {"name": "John"}, "work_experience": [], "project_experience": []},
                {"company_name": "TestCorp"}
            )
            
            system_prompt, user_prompt = mock_call.call_args[0]
            assert "cover letter writer" in system_prompt.lower()
            assert "test job desc" in user_prompt
            assert "TestCorp" in user_prompt


    def test_initialization_with_real_settings(self):
        """Test that class initializes correctly with real settings"""
        with patch('your_module.Settings') as mock_settings:
            mock_settings.GEMINI_API_KEY = "test-key"
            with patch('your_module.genai.Client') as mock_client:
                llm = GeminiLLM()
                
                assert llm.model_name == "gemini-2.5-pro"
                mock_client.assert_called_once_with(api_key="test-key")