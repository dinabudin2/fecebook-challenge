# Job Matching and Resume Analysis System

This project is a powerful web application designed to assist in matching candidates to job requirements by analyzing resumes and comparing them to job criteria. Users can upload multiple resumes in PDF or DOCX formats, enter job requirements, and the system will categorize candidates based on their fit to the role. 

## Features

- **Upload Multiple Resumes:** Upload multiple files at once in PDF or DOCX format.
- **Automated Resume Parsing:** Extracts key candidate details like name, email, phone number, and job title.
- **Job Matching:** Automatically compares resumes to job requirements and categorizes them as "passed" or "failed" based on the match.
- **Result Display:** Displays results in an organized table with links to download the uploaded files, even if no candidate data was detected.
- **Responsive UI:** A user-friendly interface for uploading, searching, and viewing results.
- **Secure Registration and Login System:** Secure login and registration with password hashing.
- **Error Handling:** Clear error messages if the system encounters any issues during upload or analysis.

## Technologies Used

- **Frontend:**
  - HTML, CSS, JavaScript
  - Tailwind CSS for styling
  - GSAP for animations
  - Flask Jinja2 for templating

- **Backend:**
  - Python with Flask framework
  - SQLAlchemy for database management
  - PyPDF2 for parsing PDF files
  - `python-docx` for DOCX file analysis

## Setup Instructions

### Prerequisites

Make sure you have the following installed on your system:
- Python 3.8+
- Flask
- Git
- Virtualenv (optional but recommended)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/dinabudin2/fecebook-challenge--gil-gvirts.git
   cd your-repository
