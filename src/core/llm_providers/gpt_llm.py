import json
import time
import openai
from openai import OpenAI

from config.settings import Settings
from core.llm_providers.llm_interface import LLMInterface


class GPTLLM(LLMInterface):
    """GPT-4.1 implementation with robust API handling and optimized prompts."""
    def __init__(self, model: str, api_key: str = None):
        if not api_key:
            api_key = Settings.MODEL_PROVIDERS["openai"]["key"]
        self.model = model
        self.client = OpenAI()
        self.max_retries = 3
        self.max_ouptut_tokens = 3000


    def _call_gpt(self, system_prompt: str, user_prompt: str, temperature: float = 0.4) -> str:
        """Make API call to GPT-4.1 with retry logic and error handling."""
        for attempt in range(self.max_retries):
            try:
                response = self.client.responses.create(
                    model = self.model,
                    input= [
                        {"role": "system", "content": system_prompt.strip()},
                        {"role": "user", "content": user_prompt.strip()}
                    ],
                    max_output_tokens = self.max_ouptut_tokens,
                    temperature= temperature,
                    top_p = 0.9 
                )
                
                # Extract the content of the response
                return response.output_text
            except openai.OpenAIError as e:
                if attempt == self.max_retries - 1:
                    raise Exception(f"GPT-4.1 API error after {self.max_retries} attempts: {str(e)}")
                time.sleep(2 ** attempt)  # Exponential backoff
            except Exception as e:
                raise Exception(f"Unexpected error: {str(e)}")
    
    def extract_job_info(self, job_description: str) -> dict:
        """Extract job information with GPT-4.1's strong comprehension."""
        system_prompt = ("You are an expert job description analyst. "
        "Extract key information and respond with ONLY a valid JSON object. "
        "No explanations, no markdown, no code blocks.")
        
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
        
        response = self._call_gpt(system_prompt, user_prompt, temperature=0.2)
        try:
            cleaned_response = self._clean_json_response(response)
            return json.loads(cleaned_response)
        except json.JSONDecodeError:
            return self._fallback_job_info()
    
    def generate_resume_content(self, job_description: str, user_data: dict) -> dict:
        """Generate resume content with GPT-4.1's creative optimization."""
        system_prompt = (
            "You are a top-tier career coach and resume optimization expert. "
            "You understand how to make technical professionals stand out in competitive job markets.\n\n"
            f"STRICT RULES:\n"
            f"- Max {Settings.MAX_WORK_EXPERIENCE} work experiences\n"
            f"- Max {Settings.MAX_PROJECT_EXPERIENCE} projects\n"
            f"- First project: max {Settings.MAX_BULLET_POINTS_FIRST_PROJECT} bullets\n"
            f"- Other projects: max {Settings.MAX_BULLET_POINTS_OTHER_PROJECTS} bullets\n"
            f"- Max {Settings.MAX_WORDS_PER_BULLET} words per bullet\n"
            f"- Never invent facts - only enhance and optimize existing content\n"
            f"- Make every word count for maximum impact\n"
            f"- Use action verbs and quantifiable results\n"
        )

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
        
        response = self._call_gpt(system_prompt, user_prompt, temperature=0.3)
        try:
            cleaned_response = self._clean_json_response(response)
            return json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse GPT-4.1 resume JSON: {str(e)}")
    

 
    def generate_cover_letter(self, job_description: str, user_data: dict, company_info: dict) -> str:
        """Generate compelling cover letter"""
        system_prompt = (
            "You are an expert cover letter writer for ML/Data Science positions. Write compelling, personalized cover letters that:\n"
            "- Show genuine interest in the specific company and role\n"
            "- Highlight relevant experience and achievements\n"
            "- Demonstrate cultural fit\n"
            "- Are concise yet impactful (300-400 words)\n"
            "- Use a professional but engaging tone\n"
            "- Include specific examples and quantifiable results"
        )


        user_prompt = f"""
        Write a cover letter for this application:
        
        Job Description:
        {job_description}
        
        Company Info:
        {json.dumps(company_info, indent=2)}
        
        Applicant Info:
        {json.dumps(user_data['applicant_info'], indent=2)}
        
        Relevant Experience:
        Work: {json.dumps(user_data['work_experience'], indent=2)}
        Projects: {json.dumps(user_data['project_experience'], indent=2)}
        
        Generate a compelling cover letter that connects the applicant's experience to this specific role and company.
        """
        
        return self._call_gpt(system_prompt, user_prompt)


    def _clean_json_response(self, response: str) -> str:
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