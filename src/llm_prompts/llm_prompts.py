# llm_prompts.py
import json
from config.settings import Settings

class LLMPrompts:
    """Centralized prompt management for LLM operations."""
    
    def __init__(self):
        pass
    
    def get_job_extraction_system_prompt(self) -> str:
        """System prompt for job description extraction."""
        return ("You are an expert job description analyst. "
                "Extract key information and respond with ONLY a valid JSON object. "
                "No explanations, no markdown, no code blocks and no line breaks or new lines).")
    
    def get_job_extraction_user_prompt(self, job_description: str) -> str:
        """User prompt for job description extraction."""
        return f"""
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
    
    def get_resume_generation_system_prompt(self) -> str:
        """System prompt for resume content generation."""
        return (
            "You are a top-tier career coach and resume optimization expert. You understand what recruiters look for and optimize resumes for both ATS systems and human reviewers."
            "You understand how to make technical professionals stand out in competitive job markets.\n\n"
            f"STRICT RULES:\n"
            f"- Max {Settings.MAX_WORK_EXPERIENCE} work experiences\n"
            f"- Max {Settings.MAX_PROJECT_EXPERIENCE} projects\n"
            f"- First project: max {Settings.MAX_BULLET_POINTS_FIRST_PROJECT} bullets\n"
            f"- Other projects: max {Settings.MAX_BULLET_POINTS_OTHER_PROJECTS} bullets\n"
            f"- Max {Settings.MAX_WORDS_PER_BULLET} words per bullet\n"
            f"- Max 130 words for the executive summary\n"
            f"- Include all project links"
            f"- Never invent facts or skills - only enhance and optimize existing content\n"
            f"- Make every word count for maximum impact\n"
            f"- Return certifications as is."
            "- Include ATS-friendly keywords from job description, if applicable"
            "- Focus on quantifiable achievements, Use action verbs."
            """For experience selection:
            - If priority_ranking = 0, select most relevant experiences automatically
            - If priority_ranking > 0, respect the ranking (1 = highest priority)
            - If two items hold the same ranking, choose according to job description relatability
            """
        )
    
    def get_resume_generation_user_prompt(self, job_description: str, user_data: dict) -> str:
        """User prompt for resume content generation."""
        return f"""
        JOB DESCRIPTION:
        {job_description}
        
        CANDIDATE DATA:
        {json.dumps(user_data, indent=2)}
        
        Generate an optimized resume JSON with this exact structure, without adding any extra markings, line breaks or anything rather than the json keys and values:
        {{
            "executive_summary": "compelling 130-word summary showcasing perfect fit for the position",
            "selected_work_experience": [
                {{
                    "company_name": "",
                    "job_title": "", 
                    "location": "",
                    "start_date": "",
                    "end_date": "",
                    "bullet_points": ["impact-driven bullet 1", "achievement bullet 2", "technical bullet 3"]
                }}
            ],
            "selected_project_experience": [
                {{
                    "project_name": "",
                    "project_stack": "",
                    "bullet_points": ["technical achievement", "business impact", "innovation highlight"],
                    "project_links": [
                        {{"name": "<link name. ex: Documentation, GitHub, Live Demo, Video Demo, ...>", "link": ""}},
                    ]
                }}
            ],
            "relevant_skills": {{
                "technical": ["prioritized technical skills"],
                "machine_learning": ["ML expertise"],
                "tools": ["relevant tools"]
            }},
            "certifications": ""
        }}
        """
    

    def get_cover_letter_system_prompt(self) -> str:
        """System prompt for cover letter generation."""
        return (
            "You are an expert cover letter writer for ML/Data Science positions. Write a compelling, personalized cover letter that:\n"
            "- Show genuine interest in the specific company and role\n"
            "- Highlight relevant experience and achievements\n"
            "- Demonstrate cultural fit\n"
            "- Are concise yet impactful (300-400 words)\n"
            "- Use a professional but engaging tone\n"
            "- Include specific examples and quantifiable results"
        )
    
    def get_cover_letter_user_prompt(self, job_description: str, user_data: dict, company_info: dict) -> str:
        """User prompt for cover letter generation."""
        return f"""
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
        The writing needs to be professional, yet human. tapping into the candidate's forte and strength points and positioning the candiate to be a top applicant for the job and the company.

        Write and return the letter content only, skip greetings, info, signature, text marking or anything other than the letter itself.
        """
    

# Replacement Resume Prompt - for A/B testing
# f"""You are an elite career strategist with deep expertise in ML/Data Science recruitment. You understand what recruiters look for and optimize resumes for both ATS systems and human reviewers.

# CRITICAL CONSTRAINTS:
# - Maximum {Settings.MAX_WORK_EXPERIENCE} work experience blocks
# - Maximum {Settings.MAX_PROJECT_EXPERIENCE} project experience blocks  
# - First project: max {Settings.MAX_BULLET_POINTS_FIRST_PROJECT} bullet points
# - Other projects: max {Settings.MAX_BULLET_POINTS_OTHER_PROJECTS} bullet points
# - Maximum {Settings.MAX_WORDS_PER_BULLET} words per bullet point
# - NEVER fabricate information - only rephrase/optimize provided content
# - Prioritize experiences based on relevance to job description
# - Include ATS-friendly keywords from job description
# - Focus on quantifiable achievements

# For experience selection:
# - If priority_ranking = 0, select most relevant experiences automatically
# - If priority_ranking > 0, respect the ranking (1 = highest priority)

# Return ONLY a valid JSON object with no additional text."""