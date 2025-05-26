# core/llm_interface.py
from abc import ABC, abstractmethod
import anthropic # type: ignore
from config.settings import Settings
import json

class LLMInterface(ABC):
    """Abstract base class for LLM interfaces"""
    
    @abstractmethod
    def generate_resume_content(self, job_description: str, user_data: dict) -> dict:
        pass
    
    @abstractmethod
    def generate_cover_letter(self, job_description: str, user_data: dict, company_info: dict) -> str:
        pass
    
    @abstractmethod
    def extract_job_info(self, job_description: str) -> dict:
        pass

class ClaudeLLM(LLMInterface):
    """Claude API implementation"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=Settings.CLAUDE_API_KEY)
        self.model = Settings.CLAUDE_MODEL
    
    def _call_claude(self, system_prompt: str, user_prompt: str) -> str:
        """Make API call to Claude"""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")
    
    def extract_job_info(self, job_description: str) -> dict:
        """Extract company and job information from job description"""
        system_prompt = """You are an expert at parsing job descriptions. Extract key information and return ONLY a valid JSON object with no additional text or formatting."""
        
        user_prompt = f"""
        Extract the following information from this job description and return as JSON:
        - company_name (string)
        - job_title (string)
        - location (string, if provided, otherwise "Not specified")
        - salary_range (string, if provided, otherwise "Not specified")
        - job_type (string, e.g., "Full-time", "Part-time", "Contract", or "Not specified")
        - benefits (array of strings, if mentioned, otherwise empty array)
        - country (string, if determinable, otherwise "Not specified")

        Job Description:
        {job_description}
        
        Return only the JSON object:
        """
        
        response = self._call_claude(system_prompt, user_prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "company_name": "Unclear input",
                "job_title": "Unclear input", 
                "location": "Not specified",
                "salary_range": "Not specified",
                "job_type": "Not specified",
                "benefits": [],
                "country": "Not specified"
            }
    
    def generate_resume_content(self, job_description: str, user_data: dict) -> dict:
        """Generate tailored resume content"""
        system_prompt = f"""You are an elite career coach and resume expert specializing in ML/Data Science roles. You understand what recruiters look for and optimize resumes for both ATS systems and human reviewers.

CRITICAL CONSTRAINTS:
- Maximum {Settings.MAX_WORK_EXPERIENCE} work experience blocks
- Maximum {Settings.MAX_PROJECT_EXPERIENCE} project experience blocks  
- First project: max {Settings.MAX_BULLET_POINTS_FIRST_PROJECT} bullet points
- Other projects: max {Settings.MAX_BULLET_POINTS_OTHER_PROJECTS} bullet points
- Maximum {Settings.MAX_WORDS_PER_BULLET} words per bullet point
- NEVER fabricate information - only rephrase/optimize provided content
- Prioritize experiences based on relevance to job description
- Include ATS-friendly keywords from job description
- Focus on quantifiable achievements

For experience selection:
- If priority_ranking = 0, select most relevant experiences automatically
- If priority_ranking > 0, respect the ranking (1 = highest priority)

Return ONLY a valid JSON object with no additional text."""

        user_prompt = f"""
        Job Description:
        {job_description}
        
        User Data:
        {json.dumps(user_data, indent=2)}
        
        Generate optimized resume content as JSON with this exact structure:
        {{
            "executive_summary": "tailored summary (max 150 words)",
            "selected_work_experience": [
                {{
                    "company_name": "",
                    "job_title": "", 
                    "location": "",
                    "date_range": "",
                    "bullet_points": ["optimized bullet 1", "optimized bullet 2", "optimized bullet 3"]
                }}
            ],
            "selected_project_experience": [
                {{
                    "project_name": "",
                    "project_stack": "",
                    "bullet_points": ["optimized bullet 1", "optimized bullet 2", "optimized bullet 3"],
                    "documentation_link": "",
                    "github_link": "",
                    "demo_link": "",
                    "live_link": ""
                }}
            ],
            "relevant_skills": {{
                "technical": ["skill1", "skill2"],
                "machine_learning": ["skill1", "skill2"],
                "tools": ["tool1", "tool2"]
            }}
        }}
        """
        
        response = self._call_claude(system_prompt, user_prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse resume content JSON: {str(e)}")
    
    def generate_cover_letter(self, job_description: str, user_data: dict, company_info: dict) -> str:
        """Generate compelling cover letter"""
        system_prompt = """You are an expert cover letter writer for ML/Data Science positions. Write compelling, personalized cover letters that:
- Show genuine interest in the specific company and role
- Highlight relevant experience and achievements
- Demonstrate cultural fit
- Are concise yet impactful (300-400 words)
- Use a professional but engaging tone
- Include specific examples and quantifiable results"""

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
        
        return self._call_claude(system_prompt, user_prompt)

# Factory function for easy LLM switching
def get_llm_interface(provider: str = "claude") -> LLMInterface:
    """Factory function to get LLM interface"""
    if provider.lower() == "claude":
        return ClaudeLLM()
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")