import re
from PyPDF2 import PdfReader
from docx import Document

# פונקציה לקליטת קובץ מהמשתמש ושמירתו בתיקייה ייעודית
def save_file(file, upload_folder):
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)
    return file_path

# פונקציה לניתוח דרישות המשרה (קבלת טקסט חופשי)
def analyze_job_requirements(text):
    requirements = [req.strip() for req in text.split('\n') if req]
    return requirements

def analyze_files(files):
    results = []
    for file_path in files:
        file_content = analyze_file(file_path)
        result = extract_candidate_info(file_content)
        results.append(result)
    return results

# פונקציה לניתוח קובץ מועמד (PDF או DOCX)
def analyze_file(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    else:
        return ""

# פונקציה להוצאת טקסט מקובץ PDF
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text

# פונקציה להוצאת טקסט מקובץ DOCX
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

# פונקציה להוצאת המידע מהמועמד (כותרת משרה, שם מלא, טלפון, מייל)
def extract_candidate_info(text):
    job_title = extract_job_title(text)
    full_name = extract_full_name(text)
    phone = extract_phone(text)
    email = extract_email(text)
    return {'job_title': job_title, 'full_name': full_name, 'phone': phone, 'email': email}

# פונקציה לזיהוי כותרת המשרה
def extract_job_title(text):
    # לוגיקה לזיהוי כותרת המשרה מתוך הטקסט (לדוגמה, חיפוש מילות מפתח או דפוסים)
    job_title_match = re.search(r'(?i)job title:\s*(.*)', text)
    return job_title_match.group(1) if job_title_match else "לא נמצא"

# פונקציה לזיהוי שם מלא
def extract_full_name(text):
    # לוגיקה לזיהוי שם מלא מתוך הטקסט
    name_match = re.search(r'(?i)name:\s*(.*)', text)
    return name_match.group(1) if name_match else "לא נמצא"

# פונקציה לזיהוי מספר טלפון
def extract_phone(text):
    phone_match = re.search(r'\b\d{2,3}-?\d{7,8}\b', text)
    return phone_match.group() if phone_match else "לא נמצא"

# פונקציה לזיהוי מייל
def extract_email(text):
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return email_match.group() if email_match else "לא נמצא"

# פונקציה לסיווג מועמדים - מי עמד בדרישות המשרה ומי לא
def categorize_candidates(candidates, requirements):
    passed = []
    failed = []

    for candidate in candidates:
        if meets_requirements(candidate, requirements):
            passed.append(candidate)
        else:
            failed.append(candidate)
    
    return passed, failed

# פונקציה לבדיקת התאמת המועמד לדרישות המשרה
def meets_requirements(candidate, requirements):
    # נניח שהמועמד עומד בדרישות אם כותרת המשרה או שם המועמד תואמים לדרישות
    for req in requirements:
        if req.lower() in candidate['job_title'].lower() or req.lower() in candidate['full_name'].lower():
            return True
    return False
