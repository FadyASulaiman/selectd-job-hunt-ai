import json
import time
import openai
from config.settings import Settings
from core.llm_interface import LLMInterface


class DeepSeekLLM(LLMInterface):
    """DeepSeek R1 implementation using OpenAI-compatible SDK"""
    
    def __init__(self):
        
        openai.base_url = "https://api.deepseek.com/v1"
        openai.api_key = Settings.DEEPSEEK_API_KEY
        self.model = Settings.DEEPSEEK_MODEL
        self.max_retries = 3
        self.max_tokens = 3000
    
    def _call_deepseek(self, system_prompt: str, user_prompt: str, temperature: float = 0.4) -> str:
        """Make API call to DeepSeek R1 with OpenAI-compatible SDK"""
        for attempt in range(self.max_retries):
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=self.max_tokens,
                    temperature=temperature,
                    top_p=0.9
                )
                return response.choices[0].message.content
            except openai.error.APIError as e:
                if attempt == self.max_retries - 1:
                    raise Exception(f"DeepSeek API error: {str(e)}")
                time.sleep(2 ** attempt)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise Exception(f"Unexpected error: {str(e)}")
                time.sleep(1)
    
    def extract_job_info(self, job_description: str) -> dict:
        """Extract job information from description"""
        system_prompt = """You are an expert job description analyst. Extract key information and respond with ONLY a valid JSON object. No explanations, no markdown, no code blocks."""
        
        user_prompt = f"""
        Parse this job description and extract information as JSON:
        
        Required format:
        {{
            "company_name": "string",
            "job_title": "string", 
            "location": "string or 'Not specified'",
            "salary_range": "string or 'Not specified'",
            "job_type": "string or 'Not specified'",
            "benefits": ["array", "of", "strings"],
            "country": "string or 'Not specified'"
        }}

        Job Description:
        {job_description}
        """
        
        response = self._call_deepseek(system_prompt, user_prompt, temperature=0.2)
        try:
            cleaned_response = self._clean_json_response(response)
            return json.loads(cleaned_response)
        except json.JSONDecodeError:
            return self._fallback_job_info()
    
    def generate_resume_content(self, job_description: str, user_data: dict) -> dict:
        """Generate optimized resume content"""
        system_prompt = f"""You are a top-tier career coach and resume optimization expert. You understand how to make technical professionals stand out in competitive job markets.

STRICT RULES:
- Max {Settings.MAX_WORK_EXPERIENCE} work experiences
- Max {Settings.MAX_PROJECT_EXPERIENCE} projects
- First project: max {Settings.MAX_BULLET_POINTS_FIRST_PROJECT} bullets
- Other projects: max {Settings.MAX_BULLET_POINTS_OTHER_PROJECTS} bullets  
- Max {Settings.MAX_WORDS_PER_BULLET} words per bullet
- Never invent facts - only enhance and optimize existing content
- Make every word count for maximum impact
- Use action verbs and quantifiable results
"""

        user_prompt = f"""
        JOB DESCRIPTION:
        {job_description}
        
        CANDIDATE DATA:
        {json.dumps(user_data, indent=2)}
        
        Generate an optimized resume JSON:
        {{
            "executive_summary": "compelling 150-word summary showcasing perfect fit",
            "selected_work_experience": [
                {{
                    "company_name": "",
                    "job_title": "", 
                    "location": "",
                    "date_range": "",
                    "bullet_points": ["impact-driven bullet 1", "achievement bullet 2", "technical bullet 3"]
                }}
            ],
            "selected_project_experience": [
                {{
                    "project_name": "",
                    "project_stack": "",
                    "bullet_points": ["technical achievement", "business impact", "innovation highlight"],
                    "documentation_link": "",
                    "github_link": "",
                    "demo_link": "",
                    "live_link": ""
                }}
            ],
            "relevant_skills": {{
                "technical": ["prioritized technical skills"],
                "machine_learning": ["ML expertise"],
                "tools": ["relevant tools"]
            }}
        }}
        """
        
        response = self._call_deepseek(system_prompt, user_prompt, temperature=0.3)
        try:
            cleaned_response = self._clean_json_response(response)
            return json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse resume JSON: {str(e)}")
    
    def _clean_json_response(self, response: str) -> str:
        """Clean response to extract JSON"""
        cleaned = response.strip()
        if '```json' in cleaned:
            cleaned = cleaned.split('```json')[1].split('```')[0]
        elif '```' in cleaned:
            cleaned = cleaned.split('```')[1].split('```')[0]
        return cleaned.strip()
    
    def _fallback_job_info(self) -> dict:
        return {
            "company_name": "Unclear input",
            "job_title": "Unclear input",
            "location": "Not specified", 
            "salary_range": "Not specified",
            "job_type": "Not specified",
            "benefits": [],
            "country": "Not specified"
        }