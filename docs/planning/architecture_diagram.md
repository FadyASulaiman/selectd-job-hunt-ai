
**Application Creation workflow**

you get a job description, now you use it to create an application.

first job description gets parsed, you get a json with job details.
why do you need this json details, one for application tracking
- country, job title and so on,two you need job details 

    |
    v
Then you parse the job application so that it helps with the resume creation flow, you need to tailor the resume to the job description yjann means you have to modify the experience details to match the job description, so if we present the same project to all (Fin-Sentiment for example), the details of the project would not be the same to all. only the most relevant would show.

    |
    v
Now you get another json from the job description parsing and project details matching to the job requirements, now what you do is to fill the resume template with the user details json you got.

    |
    v
Now you also write the cover letter, which also gets tailored according to the user's experience and the job description, this is a one prompt job no more.

    |
    v
The output is: 1. you get a file saved that would contain the resume and cover letter (following a predefined naming convention) 2. Two PDFs, the tailored resume and the cover letter 3. Two LaTex file, the ones that were previously compuled to the PDFs 4. you get a record saved to the database that tracks the job application. 

    |
    v
That's all you need for the MVP.


---

**Technical overview for application creation flow:**

Job description pasted into the text area of the UI, click "Generate"

    |
    v
function *on_generate_click()* is called
    - starts a progress meter
    - calls *generate_application_thread()* to start resume creation on a separate thread
    
    |
    v
function *generate_application_thread()* is called
    - It calls *create_application_generator()* which is a factory function to create an insance of ApplicationGenerator, which is then saved as self.generator, this instance is used to invoke *generate_application()*
    - To create an instance of ApplicationGenerator, you need four services, namely: *UserDataService()*, *DocumentService()*, *JobAnalysisService(llm_provider)*, *DatabaseManager()*. A description of these services is provided below.

    |
    v
function *generate_application()* is called w\ param job description
    - It calls *self.user_data_service.load_user_data()* to load user data
    - Then calls *self.job_analysis_service.extract_job_info(job_description)* to get job info
    - Then calls *self.job_analysis_service.generate_tailored_resume(job_description, user_data)* to generate the resume content
    - Then *self.job_analysis_service.generate_cover_letter(job_description, user_data, company_info)* to generate the cover letter content
    - Then it saves the application details to the DB by calling *self.database_manager.save_job_application(company_info)* which returns an application id
    - Finally, it creates the documents (resume & cover letter) through *self.document_service.generate_application_package(resume_content, cover_letter, user_data, company_info, job_description)*
    - And returns an *ApplicationResult(success=True application_id=app_id, company_info=company_info output_directory=output_dir)*

    |
    v
*generate_application()* returns an *ApplicationResult(success=True application_id=app_id, company_info=company_info output_directory=output_dir)* to *generate_application_thread()* and that signals the progress to stop and tailored application generation is complete.





```Services Description:```
- UserDataService: manages user data operations (loading, validation, etc ...)
- DocumentService: Handles document generation and file operations
- JobAnalysisService: Handles job analysis and content generation
- DatabaseManager: Handles DB operations
- 