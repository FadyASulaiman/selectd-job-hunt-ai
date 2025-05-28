# 🚀 Selectd Job Hunt AI

*The no-BS open-source resume tailoring system fo True professionals*

[[License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[[Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[[LaTeX](https://img.shields.io/badge/LaTeX-PDF%20Generation-green.svg)](https://www.latex-project.org/)
[[Claude API](https://img.shields.io/badge/Powered%20by-Claude%203.5%20Sonnet-purple.svg)](https://www.anthropic.com/)

## 📋 Table of Contents
- [Overview](#overview)
- [Why This System?](#why-this-system)
- [Key Features](#key-features)
- [Technical Architecture](#technical-architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage](#usage)
- [System Requirements](#system-requirements)
- [Performance Metrics](#performance-metrics)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

A production ready **AI Resume Tailoring System**, eliminates the tedious process of manually tailoring resumes for every job application. Built specifically for the Job hunt, this system leverages Claude 3.7-Sonnet's advanced reasoning capabilities to generate ATS-optimized, recruiter-friendly resumes and cover letters in seconds.

### The Problem
- Manual resume tailoring takes 30-45 minutes per application
- Generic resumes have <5% response rates
- ATS systems filter out 75% of applications
- Inconsistent formatting and messaging across applications
- No systematic tracking of application performance

### The Solution
**One-click resume generation** that produces:
- ✅ ATS-optimized resumes with keyword matching scores
- ✅ Compelling, personalized cover letters
- ✅ Professional LaTeX-generated PDFs
- ✅ Systematic application tracking and analytics
- ✅ **10x faster** than manual processes

## 🏆 Why This System?

### 🎯 **Built for True Professionals**
Unlike generic resume builders, this system understands the nuances of roles in the specific field, specific terminology, and what recruiters in the field actually look for.

### ⚡ **Lightning Fast Performance**
- **Average generation time**: 15-20 seconds
- **Smart caching**: Reuse optimized components across similar roles

### 🧠 **AI-Powered Intelligence**
- **Claude 3.7 Sonnet integration**: State-of-the-art language model
- **ATS optimization**: Automatic keyword matching and scoring
- **Context-aware tailoring**: Understands job requirements and company culture
- **Constraint adherence**: Strict word limits, formatting rules, and content guidelines

### 🔧 **Developer-First Design**
- **Modular architecture**: Easily extensible and maintainable
- **Clean separation of concerns**: Database, LLM, LaTeX, and GUI layers
- **Type safety**: Comprehensive error handling and validation
- **Production-ready**: Logging, monitoring, and performance optimization

## ✨ Key Features

### 🎨 **Intelligent Content Generation**
- **Dynamic experience selection**: Automatically chooses most relevant work/project experiences
- **Bullet point optimization**: Rewrites content for maximum impact while preserving facts
- **Skills prioritization**: Highlights relevant technical skills based on job requirements
- **Executive summary tailoring**: Customizes professional summary for each application

### 📊 **ATS Optimization Engine**
- **Keyword density analysis**: Ensures optimal keyword placement
- **Formatting compliance**: ATS-friendly LaTeX templates
- **Scoring system**: Provides quantitative feedback on application strength
- **Industry-specific optimization**: Tailored for ML/DS role requirements

### 🗄️ **Application Management**
- **SQLite database**: Lightweight, embedded database for application tracking
- **Status monitoring**: Track interview invitations, rejections, and responses
- **Performance analytics**: Analyze which resume versions perform best
- **Export capabilities**: Generate reports and insights

### 📱 **User Experience**
- **Clean GUI**: Intuitive tkinter interface with progress indicators
- **Error handling**: Comprehensive validation and user feedback
- **Cross-platform**: Works on Windows, macOS, and Linux

## 🏗️ Technical Architecture

### **Modular Design Pattern**
```
┌─────────────────────────────────────────────────────────┐
│                    GUI Layer (tkinter)                  │
├─────────────────────────────────────────────────────────┤
│                 Resume Generator (Core)                 │
├─────────────────────────────────────────────────────────┤
│  LLM Interface  │  Database Mgr  │  LaTeX Processor    │
├─────────────────────────────────────────────────────────┤
│     Claude API  │    SQLite      │     pdflatex        │
└─────────────────────────────────────────────────────────┘
```

### **Core Components**

#### 🤖 **LLM Interface Layer**
- **Abstract base class**: `LLMInterface` for easy provider switching
- **Claude implementation**: Optimized prompts for resume generation
- **Error handling**: Robust API failure management and retries
- **Response validation**: JSON schema validation and sanitization

#### 🗃️ **Database Management**
- **Schema design**: Optimized for application tracking and analytics
- **Migration support**: Version-controlled database updates
- **Query optimization**: Indexed searches and efficient data retrieval
- **Backup functionality**: Automated database backup and recovery

#### 📄 **LaTeX Processing Engine**
- **Template system**: Professional, customizable resume templates
- **Dynamic content injection**: Safe placeholder replacement
- **PDF compilation**: Automated LaTeX → PDF pipeline
- **Error recovery**: Handles compilation failures gracefully

#### 🎛️ **Configuration Management**
- **Environment-based config**: Secure API key management
- **Constraint enforcement**: Customizable resume generation rules
- **Path management**: Automated directory structure creation
- **Settings validation**: Comprehensive configuration validation

## 🛠️ Installation

### **Prerequisites**
- Python 3.8+ 
- LaTeX distribution (MiKTeX, TeX Live, or MacTeX)
- Claude API key from Anthropic

### **LaTeX Installation**

**Windows (MiKTeX):**
```bash
# Option 1: Direct download
# Visit: https://miktex.org/download

# Option 2: Chocolatey
choco install miktex

# Option 3: Winget
winget install MiKTeX.MiKTeX
```

**macOS (MacTeX):**
```bash
# Homebrew
brew install --cask mactex

# MacPorts
sudo port install texlive +full
```

**Linux (TeX Live):**
```bash
# Ubuntu/Debian
sudo apt-get update && sudo apt-get install texlive-full

# CentOS/RHEL
sudo yum install texlive-scheme-full

# Arch
sudo pacman -S texlive-most
```

### **Python Dependencies**
```bash
# Clone the repository
git clone https://github.com/yourusername/ai-resume-automation.git
cd ai-resume-automation

# Install dependencies
pip install anthropic

# Verify LaTeX installation
pdflatex --version
```

### **Environment Setup**
```bash
# Set Claude API key
export CLAUDE_API_KEY='your-claude-api-key-here'

# Windows PowerShell
$env:CLAUDE_API_KEY = 'your-claude-api-key-here'

# Windows Command Prompt
set CLAUDE_API_KEY=your-claude-api-key-here
```

## 🚀 Quick Start

### **1. Configure Your Profile**
Edit `data/user_data.json` with your information:

```json
{
  "applicant_info": {
    "name": "Your Name",
    "email": "your.email@example.com",
    "phone": "+1 (555) 123-4567",
    "github": "github.com/yourusername",
    "linkedin": "linkedin.com/in/yourprofile"
  },
  "work_experience": [
    {
      "priority_ranking": 1,
      "company_name": "Tech Company",
      "job_title": "Senior ML Engineer",
      "location": "San Francisco, CA",
      "date_range": "Jan 2022 -- Present",
      "bullet_points": [
        "Built production ML systems serving 10M+ users",
        "Improved model accuracy by 15% using advanced feature engineering",
        "Led team of 4 engineers in developing real-time recommendation engine"
      ]
    }
  ],
  // ... additional sections
}
```

### **2. Launch the Application**
```bash
python main.py
```

### **3. Generate Your First Application**
1. Paste job description in the text area
2. Click "Generate Resume & Cover Letter"
3. Wait 15-20 seconds for AI processing
4. Review generated files in `applications/` directory

### **4. Output Structure**
```
applications/
└── 05-26-25-TechCorp-MLEngineer/
    ├── YourName_Resume-TechCorp.tex
    ├── YourName_Resume-TechCorp.pdf
    ├── YourName_CoverLetter-TechCorp.tex
    ├── YourName_CoverLetter-TechCorp.pdf
    └── TechCorp-MLEngineer-JD.md
```

## ⚙️ Configuration

### **Resume Generation Constraints**
```python
# config/settings.py
MAX_WORK_EXPERIENCE = 2        # Maximum work experiences to include
MAX_PROJECT_EXPERIENCE = 3     # Maximum projects to include
MAX_BULLET_POINTS_FIRST_PROJECT = 3  # Bullets for primary project
MAX_BULLET_POINTS_OTHER_PROJECTS = 2 # Bullets for other projects
MAX_WORDS_PER_BULLET = 30      # Word limit per bullet point
```

### **LLM Provider Configuration**
```python
# Easy switching between LLM providers
def get_llm_interface(provider: str = "claude") -> LLMInterface:
    if provider.lower() == "claude":
        return ClaudeLLM()
    elif provider.lower() == "openai":
        return OpenAILLM()  # Future implementation
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
```

### **Database Schema**
```sql
CREATE TABLE job_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    job_title TEXT NOT NULL,
    application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    location TEXT,
    salary_range TEXT,
    job_type TEXT,
    benefits TEXT,
    country TEXT,
    status TEXT DEFAULT 'Applied',
    interview_date TIMESTAMP,
    notes TEXT,
    ats_keywords_score INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 📖 Usage

### **Basic Workflow**
```python
from core.resume_generator import ResumeGenerator

# Initialize generator
generator = ResumeGenerator()

# Generate application
result = generator.generate_application(job_description)

if result['success']:
    print(f"ATS Score: {result['ats_score']}%")
    print(f"Files saved to: {result['output_directory']}")
else:
    print(f"Error: {result['error']}")
```

#### **Custom LLM Provider**
```python
# Implement custom LLM provider
class CustomLLM(LLMInterface):
    def generate_resume_content(self, job_description, user_data):
        # Custom implementation
        pass

# Use custom provider
generator = ResumeGenerator(llm_provider="custom")
```

#### **Database Queries**
```python
from core.database import DatabaseManager

db = DatabaseManager()

# Get application statistics
applications = db.get_applications_summary()
for app in applications:
    print(f"{app[0]} - {app[1]} - {app[3]}")  # Company, Role, Status
```


### **Dependencies**
```txt
anthropic>=0.25.0     # Claude API client
openai               # OpenAI API client
tkinter              # GUI framework (usually included with Python)
sqlite3              # Database (included with Python)
subprocess           # Process management (included with Python)
json                 # JSON handling (included with Python)
datetime             # Date/time utilities (included with Python)
os                   # Operating system interface (included with Python)
shutil               # File operations (included with Python)
re                   # Regular expressions (included with Python)
threading            # Multi-threading support (included with Python)
```


## 🤝 Contributing

Contributions are truly welcome! I built this system to use during my job hunt and published it only in the hope that it would benefit others looking for a job, so, if you feel like you can add anything to improve this project, plase do not hesitate to do so.

### **Development Setup**
```bash
# Fork and clone the repository
git clone https://github.com/yourusername/ai-resume-automation.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

### **Code Style**
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write comprehensive docstrings
- Maintain test coverage >80%

### **Submitting Changes**
1. Create a feature branch
2. Make your changes
3. Add tests for new functionality
4. Run the test suite
5. Submit a pull request


## 📞 Contact

- **Email**: Sulaiman.a.fady@gmail.com

---

**⭐ Star this repository if it helped you during your job search!**

*Built by Fady A. Sulaiman*