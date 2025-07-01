import json
from typing import Optional
from google.genai import types
from google import genai
from config.settings import Settings
from core.llm_providers.llm_interface import LLMInterface
from llm_prompts.llm_prompts import LLMPrompts

class GeminiLLM(LLMInterface):
    """Gemini API implementation"""

    def __init__(self, model: str, prompts: LLMPrompts = None):
        
        self.model_name = model
        self.client = genai.Client(api_key=Settings.MODEL_PROVIDERS['google']['key'])

        # Inject prompts dependency
        self.prompts = prompts or LLMPrompts()


    def _call_gemini(self, system_prompt: str, user_prompt: str, thinking_budget: Optional[int] = None) -> str:
        """Make API call to Gemini"""
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                    thinking_config=types.ThinkingConfig(
                    thinking_budget=thinking_budget
                    )),
                contents=user_prompt
                )
            print(response) # debug: remove
            
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")


    def extract_job_info(self, job_description: str) -> dict:
        """Extract job information"""
        system_prompt = self.prompts.get_job_extraction_system_prompt()
        user_prompt = self.prompts.get_job_extraction_user_prompt(job_description)
        
        response = self._call_gemini(system_prompt, user_prompt, thinking_budget=0)
        try:
            cleaned_response = self._clean_json_response(response)
            return json.loads(cleaned_response)
        except json.JSONDecodeError:
            return self._fallback_job_info()
        

    def generate_resume_content(self, job_description: str, user_data: dict) -> dict:
        """Generate resume content """
        system_prompt = self.prompts.get_resume_generation_system_prompt()
        user_prompt = self.prompts.get_resume_generation_user_prompt(job_description, user_data)
        
        response = self._call_gemini(system_prompt, user_prompt)
        try:
            cleaned_response = self._clean_json_response(response)
            return json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse GPT-4.1 resume JSON: {str(e)}")



    def generate_cover_letter(self, job_description: str, user_data: dict, company_info: dict) -> str:
        """Generate compelling cover letter"""
        system_prompt = self.prompts.get_cover_letter_system_prompt()
        user_prompt = self.prompts.get_cover_letter_user_prompt(job_description, user_data, company_info)
        
        response = self._call_gemini(system_prompt, user_prompt)
        try:
            cleaned_response = self._clean_json_response(response)
            cleaned_response = cleaned_response.replace('&', '\&').replace('%', '\%')
            return cleaned_response
        except Exception as e:
            raise Exception(f"Failed to parse GPT cover letter content: {str(e)}")


    def _clean_json_response(self, response: str) -> str:
        """Clean and prepare response text for reliable JSON parsing."""
        # Remove markdown code blocks
        cleaned = response.strip()
        if '```json' in cleaned:
            cleaned = cleaned.split('```json')[1].split('```')[0]
        elif '```' in cleaned:
            cleaned = cleaned.split('```')[1].split('```')[0]
        
        # Remove newlines and normalize whitespace
        cleaned = cleaned.replace('\n', ' ').replace('\r', ' ')
        cleaned = ' '.join(cleaned.split())
        
        # Fix common JSON issues
        import re
        cleaned = re.sub(r',(\s*[}\]])', r'\1', cleaned)
        
        def fix_quotes_in_strings(match):
            content = match.group(1)
            content = re.sub(r'(?<!\\)"', r'\\"', content)
            return f'"{content}"'
        
        cleaned = re.sub(r'"([^"]*(?:\\"[^"]*)*)"(?=\s*[,\]}])', fix_quotes_in_strings, cleaned)
        
        return cleaned.strip()


    def _fallback_job_info(self) -> dict:
        """Fallback job info when parsing fails"""
        return {
            "company_name": "Unclear input",
            "job_title": "Unclear input", 
            "location": "Not specified",
            "salary_range": "Not specified",
            "job_type": "Not specified",
            "benefits": [],
            "country": "Not specified"
        }