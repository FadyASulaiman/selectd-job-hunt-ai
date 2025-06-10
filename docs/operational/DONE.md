Jun 5 2025
Obtain API keys for all the four LLM APIs.
Note: Claude turned out to be the most expensive, while not providing critical advantage over the rest in our use case, would leave it in the MVP, for its inclusion/exclusion to be decided on first launch.

Jun 6 2025
Implementations for the APIs of the four major LLMs (Claude - GPT - Gemini - Deepseek), using a unified abstract class.

Jun 7 2025
- Dubugged and tested LLM API calls, gemini now verified working(✅) through the API call for Job description.
- Unit & integration tests created & passed.
- Tested models: Gemini-2.5-Pro and Gemini-2.5-flash. Test focus: GeminiLLM class.

Jun 9 2025
- Created a dropdown for LLM choice (GPT-4.1, Gemini-2.5-Pro, DeepSeek) and mapped user's choice to submit function.
- Improved prompts.
- Configuring thinking/resume budget for gemini models

Jun 10 2025
- Converted LaTex template to jinja2 template
- Updated resume generator and latex processor to handle the new template
- Added json schema validator for user data (processed and returned from the LLM)
- Add dynamic model selection to ResumeGenerator class, mapping resume & cover letter creation to main models and detail extraction to small (flash/nano) models. Plus, updating MODEL_PROVIDER map in settings for dynamic selection.