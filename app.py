from flask import Flask, render_template, request, redirect, url_for, send_file, session
import os
import re
from docx import Document
from PyPDF2 import PdfReader
import pandas as pd
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '1'
import os
CORS(app)  # כדי לאפשר בקשות ממקורות שונים, אם יש צורך
app.config['UPLOAD_FOLDER'] = 'uploads/'  # תיקיית העלאת קבצים
bcrypt = Bcrypt(app) 
# הגדרת מסד נתונים (במקרה זה, SQLite - קובץ במסלול הזה)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # מסד נתונים מסוג SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # כדי להפסיק התראות מיותרות
db = SQLAlchemy(app)

# יצירת תיקיית העלאת קבצים אם היא לא קיימת
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# דף הבית
@app.route('/')
def index():
    return render_template('index.html')

# דף הרשמה
# יצירת מודל של משתמשים
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

# יצירת מסד הנתונים כאשר היישום רץ
with app.app_context():
    db.create_all()


# דוגמה לנתיב הרשמה
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # בדוק אם שם המשתמש כבר קיים
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists, please choose a different one.", 400

        # אם שם המשתמש אינו קיים, הצפן את הסיסמה והכנס למסד הנתונים
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')



#qa
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # חפש את המשתמש במסד הנתונים לפי אימייל
        #להוסיף זהה לסיסמא לבדיקה 
        user = User.query.filter_by(email=email).first()

        if user:
            session['user_id'] = user.id  # כניסה מוצלחת ללא בדיקת סיסמה
            return redirect(url_for('upload'))
        else:
            error = "Invalid email or user not found"

    return render_template('login.html', error=error)

# מאובטח יותר 
#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    error = None
#    if request.method == 'POST':
#        email = request.form.get('email')
#        password = request.form.get('password')

        # חפש את המשתמש במסד הנתונים
#        user = User.query.filter_by(email=email).first()

#        if user and bcrypt.check_password_hash(user.password, password):
#            session['user_id'] = user.id  # כניסה מוצלחת
#            return redirect(url_for('dashboard'))
#        else:
#            error = "Invalid email or password"

#   return render_template('login.html', error=error)


# File upload route
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # קבלת כל הקבצים מהטופס (השם של תיבת הקובץ נשאר 'files')
        files = request.files.getlist('files')

        # בדיקה אם קיים חלק הקובץ בבקשה
        if not files or len(files) == 0:
            return "No files part"

        saved_files = []
        
        for file in files:
            if file.filename == '':
                return "No selected file"
            
            # שמירת הקובץ בספרייה
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            saved_files.append(filename)

        # הנחיה להמשיך לדף job_requirements
        return redirect(url_for('job_requirements', filename=saved_files[0]))  # השתמש בקובץ הראשון שנשמר לדוגמה

    return render_template('upload.html')

# Job requirements page
@app.route('/search/<filename>', methods=['GET', 'POST'])
def job_requirements(filename):
    if request.method == 'POST':
        # קבלת טקסט הדרישות מהטופס
        job_requirements_text = request.form.get('search')
        if not job_requirements_text:
            return "Missing search text", 400

        # בדיקת הקובץ והנתיב
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(file_path):
            return "File not found", 404

        # ניתוח הקובץ
        file_text = analyze_file(file_path)

        # חילוץ מידע מועמדים
        candidates_data = extract_candidate_info(file_text)

        # סיווג מועמדים לפי הדרישות
        passed_candidates, failed_candidates = categorize_candidates([candidates_data], job_requirements_text)

        # במידה ואין מועמד שעבר, נעדכן רשימה ריקה
        if not passed_candidates:
            passed_candidates = []

        # במידה ואין מועמד שנכשל, נעדכן רשימה ריקה ונוסיף את נתיב הקובץ
        if not failed_candidates:
            failed_candidates = []
        for candidate in failed_candidates:
            candidate['file_path'] = file_path

        # הצגת התוצאות בעמוד HTML
        return render_template('results.html', passed=passed_candidates, failed=failed_candidates, filename=filename)
    
    return render_template('search.html', filename=filename)


# Analyze job requirements
def analyze_job_requirements(text):
    return [req.strip() for req in text.split('\n') if req]

# Analyze the file (PDF or DOCX)
def analyze_file(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    return ""

# Extract text from PDF
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text

# Extract text from DOCX
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

# Extract candidate information
def extract_candidate_info(text):
    job_title = extract_job_title(text)
    full_name = extract_full_name(text)
    phone = extract_phone(text)
    email = extract_email(text)
    return {'job_title': job_title, 'full_name': full_name, 'phone': phone, 'email': email}

# Extract job title
def extract_job_title(text):
    job_title_match = re.search(r'(?i)job title:\s*(.*)', text)
    return job_title_match.group(1) if job_title_match else "לא נמצא"

# Extract full name
def extract_full_name(text):
    name_match = re.search(r'(?i)name:\s*(.*)', text)
    return name_match.group(1) if name_match else "לא נמצא"

# Extract phone number
def extract_phone(text):
    phone_match = re.search(r'\b\d{2,3}-?\d{7,8}\b', text)
    return phone_match.group() if phone_match else "לא נמצא"

# Extract email
def extract_email(text):
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return email_match.group() if email_match else "לא נמצא"

# Categorize candidates
def categorize_candidates(candidates_data, search):
    passed_candidates = []
    failed_candidates = []
    
    for candidate in candidates_data:
        if meets_requirements(candidate, search):
            passed_candidates.append(candidate)
        else:
            failed_candidates.append(candidate)
    
    return passed_candidates, failed_candidates

# Check if candidate meets the requirements
def meets_requirements(candidate, search):
    for req in search:
        if req.lower() in candidate['job_title'].lower() or req.lower() in candidate['full_name'].lower():
            return True
    return False

if __name__ == '__main__':
    app.run(debug=True)