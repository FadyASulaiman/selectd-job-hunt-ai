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

Jun 12 2025
- Created LLM Provider & Factory classes to supply LLM instances
- Abstracted the services to a separate layer, living in the services folder. Created job_analysis, user_data and document services
- created, but did not run, unit tests for the application generation class.
- Minor refactoring.

Jun 13 2025
- Application Creation flow is clarified in detail, from both practical and technical view points, which is proving crucial in order to keep track of all the elements in play.
- Debugged the ```on_generate_click()``` method in the main window in order to adopt the new structure.

Jun 18 2025
- Debug DocumentService & LaTexProcessor classes
- Fix Resume Generation settings to supply correct paths
- Add a comprehensive testing suite for DocumentService (Unit/Integration/e2e) - Tests ran and passed

Jun 21 2025
- Update Cover letter template to jinja2
- Debugged latex compilation to PDF, verified cover letter generation. done. (yes, we are that close to the north star)
- updated sql db workflow, WIP.
- Added two cases to the e2e testing suite for DocumentService.

Jun 24 2025
- Fixed Resume Template, so that all placeholders are correctly named, line breaks are correctly rendered and elements are correctly stacked.
- Fixed faulty parameters in latex generator
- Fixed faulty parameters in LLM return (for the four providers)
- Added resume dependencies (altacv.cls, pubs-num.tex)
- Compiled a full resume PDf, with all elements, sections and points. (The north-star is a just a few steps away, I see it already)

Jun 26 2025
- Refactored whole DB operations, separated concerns to: UserRepository, JobApplicationRepository, DatabaseManager, DatabaseSchemaManager, DatabaseDataValidator and DBConnectionManager
- Added DB test suite (Ran Unit tests and verified, remaining to verify integration and e2e)
- Designed a Thread-safe singleton state manager, WIP

Jun 27 2025
- Implemented auth logic
- Implemented user state management, that is thread safe and singleton based (not for the MVP)
- Created and ran prod tests for the DB operations, refined and debugged the related code
- Created an e2e test for the full application generation workflow, needs very few tweaks to run seamlessly end-to-end