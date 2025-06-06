import json

import anthropic
from config.settings import Settings
from core.llm_interface import LLMInterface


class ClaudeLLM(LLMInterface):
    """Claude API implementation"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=Settings.GEMINI_API_KEY)
        self.model = Settings.CLAUDE_MODEL
        pass
    
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
        system_prompt = """You are an expert at parsing job descriptions with exceptional attention to detail. Extract key information and return ONLY a valid JSON object with no additional text, markdown formatting, or code blocks."""
        
        user_prompt = f"""
        Extract the following information from this job description and return as JSON:
        - company_name (string)
        - job_title (string)
        - location (string, if provided, otherwise "Not specified")
        - salary_range (string, if provided, otherwise "Not specified")
        - job_type (string, e.g., "Full-time", "Part-time", "Contract", or "Not specified")
        - benefits (string delimited by a slash)
        - country (string, if determinable, otherwise "Not specified")

        Job Description:
        {job_description}
        
        Return only the JSON object:
        """
        
        response = self._call_claude(system_prompt, user_prompt)
        try:
            # Clean the response to ensure valid JSON
            cleaned_response = response.strip()
            if cleaned_response.startswith('```'):
                cleaned_response = cleaned_response.split('\n', 1)[1].rsplit('\n', 1)[0]
            return json.loads(cleaned_response)
        except json.JSONDecodeError:
            return self._fallback_job_info()
    
    def generate_resume_content(self, job_description: str, user_data: dict) -> dict:
        """Generate tailored resume content"""
        # Experiment with adding this line to prompt: The ultimate goal is to best position the candidate to be shortlisted for an interview
        system_prompt = f"""You are an elite career strategist with deep expertise in ML/Data Science recruitment. You understand what recruiters look for and optimize resumes for both ATS systems and human reviewers.

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
            cleaned_response = response.strip()
            if cleaned_response.startswith('```'):
                cleaned_response = cleaned_response.split('\n', 1)[1].rsplit('\n', 1)[0]
            return json.loads(cleaned_response)
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