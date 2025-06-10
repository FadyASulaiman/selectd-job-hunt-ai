# gui/main_window.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from core.resume_generator import ResumeGenerator

class MainWindow:
    """Main GUI window for the resume automation tool"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Resume Tailor")
        self.root.geometry("800x600")
        
        self.dropdown_options = {
            "GPT-4.1": "openai",
            "Gemini-2.5-Pro": "google", 
            "DeepSeek": "deepseek"
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Resume Automation Tool", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Dropdown frame
        dropdown_frame = ttk.Frame(main_frame)
        dropdown_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Dropdown label
        dropdown_label = ttk.Label(dropdown_frame, text="Select AI Model:")
        dropdown_label.grid(row=0, column=0, padx=(0, 10), sticky=tk.W)
        
        # Dropdown combobox
        self.dropdown_var = tk.StringVar()
        self.dropdown = ttk.Combobox(dropdown_frame, textvariable=self.dropdown_var,
                                    values=list(self.dropdown_options.keys()),
                                    state="readonly", width=20)
        self.dropdown.grid(row=0, column=1, sticky=tk.W)
        self.dropdown.set("One")  # Set default selection
        
        # Job description input
        jd_frame = ttk.LabelFrame(main_frame, text="Job Description", padding="5")
        jd_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        jd_frame.columnconfigure(0, weight=1)
        jd_frame.rowconfigure(0, weight=1)
        
        self.job_description_text = scrolledtext.ScrolledText(jd_frame, wrap=tk.WORD, 
                                                             height=15, width=70)
        self.job_description_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, pady=10)
        
        # Generate button
        self.generate_button = ttk.Button(button_frame, text="Generate Resume & Cover Letter",
                                         command=self.on_generate_click)
        self.generate_button.grid(row=0, column=0, padx=(0, 10))
        
        # Clear button
        clear_button = ttk.Button(button_frame, text="Clear", 
                                 command=self.clear_text)
        clear_button.grid(row=0, column=1)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready", foreground="green")
        self.status_label.grid(row=5, column=0, pady=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="5")
        results_frame.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=10)
        results_frame.columnconfigure(0, weight=1)
        
        self.results_text = tk.Text(results_frame, height=6, wrap=tk.WORD, state=tk.DISABLED)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Scrollbar for results
        results_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, 
                                         command=self.results_text.yview)
        results_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.results_text.configure(yscrollcommand=results_scrollbar.set)
    
    def get_selected_value_code(self):
        """Get the value code for the currently selected LLM"""
        selected_display_name = self.dropdown_var.get()
        return self.dropdown_options.get(selected_display_name, "gemini")  # Default fallback
    
    def clear_text(self):
        """Clear the job description text area"""
        self.job_description_text.delete(1.0, tk.END)
        self.update_results("")
        # Reset dropdown to default
        self.dropdown.set("GPT-4.1")
    
    def update_status(self, message: str, color: str = "black"):
        """Update status label"""
        self.status_label.config(text=message, foreground=color)
        self.root.update_idletasks()
    
    def update_results(self, message: str):
        """Update results text area"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, message)
        self.results_text.config(state=tk.DISABLED)
    
    def on_generate_click(self):
        """Handle generate button click"""
        job_description = self.job_description_text.get(1.0, tk.END).strip()
        selected_value_code = self.get_selected_value_code()
        
        if not job_description:
            messagebox.showerror("Error", "Please enter a job description")
            return
        
        # Show which option was selected
        selected_display_name = self.dropdown_var.get()
        print(f"Selected option: {selected_display_name} (Code: {selected_value_code})")
        
        # Disable button and start progress
        self.generate_button.config(state=tk.DISABLED)
        self.progress.start()
        
        # Run generation in separate thread, passing the selected value code
        thread = threading.Thread(target=self.generate_resume_thread, 
                                 args=(job_description, selected_value_code))
        thread.daemon = True
        thread.start()
    
    def generate_resume_thread(self, job_description: str, selected_value_code: str):
        """Generate resume in background thread"""
        try:
            self.update_status("Processing job description...", "blue")

            self.generator = ResumeGenerator(llm_provider=selected_value_code)
            # Pass the selected value code to your generator
            result = self.generator.generate_application(job_description)
            
            # Update UI in main thread
            self.root.after(0, self.on_generation_complete, result)
            
        except Exception as e:
            error_result = {'success': False, 'error': str(e)}
            self.root.after(0, self.on_generation_complete, error_result)
    
    def on_generation_complete(self, result: dict):
        """Handle generation completion"""
        # Stop progress and re-enable button
        self.progress.stop()
        self.generate_button.config(state=tk.NORMAL)
        
        if result['success']:
            self.update_status("Generation completed successfully!", "green")
            
            # Format results
            company_info = result['company_info']
            selected_option = self.dropdown_var.get()
            selected_code = self.get_selected_value_code()
            
            results_text = f"""✅ Resume and Cover Letter Generated Successfully!

Company: {company_info.get('company_name', 'Unknown')}
Position: {company_info.get('job_title', 'Unknown')}
Location: {company_info.get('location', 'Not specified')}
ATS Score: {result['ats_score']}%

Output Directory: {result['output_directory']}

Files Generated:
• Resume (LaTeX & PDF)
• Cover Letter (LaTeX & PDF)  
• Job Description (Markdown)

Application ID: {result['application_id']}
LLM Used: {selected_option} ({selected_code})
"""
            
            self.update_results(results_text)
            
            messagebox.showinfo("Success", 
                              f"Resume generated successfully!\nSelected: {selected_option}\n"
                              f"ATS Score: {result['ats_score']}%\n"
                              f"Files saved to: {result['output_directory']}")
        else:
            self.update_status("Generation failed", "red")
            self.update_results(f"❌ Error: {result['error']}")
            messagebox.showerror("Error", f"Generation failed: {result['error']}")
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()