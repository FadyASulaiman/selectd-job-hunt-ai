from core.llm_providers.gemini_llm import GeminiLLM

class TestIntegrationGeminiLLM:

    def test_real_api_call(self):
        """This WOULD make a real API call - use sparingly"""
        # No mocking - uses real client
        llm = GeminiLLM()
        result = llm.extract_job_info("""
Want to join a Canadian leader? Love to work with experienced professionals? Eager to make a valued contribution to a team of some 250 colleagues? Sounds like you’re ready for a job at ACME inc., Canada’s number one translation provider.

ACME inc. is seeking an AI Specialist – Content Management/Localization, NLP & Large Language Models (LLMs) to lead the deployment and training of LLMs tailored to specific use cases in content creation, transformation, and localization workflows. This role ensures that AI technologies are strategically selected, effectively integrated into existing systems, and consistently monitored for reliability and performance improvements. The AI Specialist will work closely with DevOps, engineering, and operations teams to design, implement, and optimize AI-powered solutions for content creation, transformation, and localization.

Your Daily Routine

AI Engine Design: Design the AI solution that solves given business challenges or use cases.
AI Deployment & Training: Select, fine-tune, and deploy LLMs for specific localization use cases, ensuring optimal performance and efficiency.
Technology Selection: Assess and recommend AI technologies that best address given use cases and business requirements.
Solution Integration: Collaborate with DevOPS team to ensure seamless integration of AI-powered workflows into existing systems (e.g., TMS), tools (e.g., CAT), and workflows.
Reliability & Performance Monitoring: Develop methodologies to track AI system reliability and continuously enhance model performance.
Collaboration with DevOps: Define infrastructure requirements, including hardware and software needs, to support AI solutions.
Workflow Optimization: Work with stakeholders to refine and improve AI-driven workflows, maximizing automation and efficiency.
User Story & Requirement Definition: Document technical requirements and user stories to guide engineering teams in solution development.

You Will Need

AI & NLP Expertise: 3+ years of experience in NLP working with LLMs, machine translation, and AI-driven solutions.
Machine Learning: Strong understanding of machine learning operations to establish and manage machine learning pipelines for each use case.
Technical Background: Strong understanding of AI model training, fine-tuning, and deployment methodologies.
AI Model Evaluation: Experience in setting up and evaluating AI models to ensure continued performance up to the standards.
Integration Experience: Hands-on experience in integrating AI solutions with existing platforms via APIs and automation scripts.
Data & Performance Analysis: Ability to analyse model performance, optimize datasets, and implement continuous improvements.
Collaboration & Communication: Strong ability to work cross-functionally with technical and non-technical teams to define and execute AI strategies.
Problem-Solving Skills: Proficiency in troubleshooting AI-related challenges and optimizing performance for scalability.

This position may be ideal for you if you have:

Experience with AI frameworks: TensorFlow, PyTorch, Hugging Face, Azure, OpenAI API, or similar AI toolkits.
Exposure to MLOps/DevOps practices for AI deployment (e.g., MLOps, cloud-based AI infrastructures).
Knowledge of Agile/Scrum methodologies like Jira or Confluence.
Understanding of AI ethics: Grasp of bias mitigation strategies.
Localization and/or Content Management Industry Knowledge
Familiarity with Tools and Systems: Python, Translation Management Systems (TMS), Computer-Assisted Translation (CAT) tools, content management, and localization workflows.

Why join us?

Work at the intersection of AI and content management systems, shaping the future of content management services.
Collaborate with a dynamic and innovative team driving cutting-edge AI solutions.
Opportunity to influence and build AI-powered workflows for global enterprise clients.

We value our teams and offer working conditions to match:

Competitive salary
Comprehensive group insurance
Group RRSP
Flexible work arrangements
Fitness benefit
Payment of dues to your professional order
Referral program
Public transit credit
Paid vacation on your birthday
""")
        print(result)
        assert isinstance(result, dict)


# To run:
# from the project's root: $ pytest -xvs src/test/int_test_gemini.py::TestIntegrationGeminiLLM::test_real_api_call
# Average call to a flash/nano model consumes ~1500 tokens