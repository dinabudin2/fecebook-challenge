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
CORS(app)  
app.config['UPLOAD_FOLDER'] = 'uploads/' 
bcrypt = Bcrypt(app) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
db = SQLAlchemy(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

with app.app_context():
    db.create_all()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists, please choose a different one.", 400
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user:
            session['user_id'] = user.id  
            return redirect(url_for('upload'))
        else:
            error = "Invalid email or user not found"

    return render_template('login.html', error=error)

# More Secure Login
#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    error = None
#    if request.method == 'POST':
#        email = request.form.get('email')
#        password = request.form.get('password')

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
        files = request.files.getlist('files')

        if not files or len(files) == 0:
            return "No files part"

        saved_files = []
        
        for file in files:
            if file.filename == '':
                return "No selected file"
            
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            saved_files.append(filename)

        return redirect(url_for('job_requirements', filename=saved_files[0])) 

    return render_template('upload.html')

# Job requirements page
@app.route('/search/<filename>', methods=['GET', 'POST'])
def job_requirements(filename):
    if request.method == 'POST':
        job_requirements_text = request.form.get('search')
        if not job_requirements_text:
            return "Missing search text", 400

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(file_path):
            return "File not found", 404

        file_text = analyze_file(file_path)

        candidates_data = extract_candidate_info(file_text)

        passed_candidates, failed_candidates = categorize_candidates([candidates_data], job_requirements_text)

        if not passed_candidates:
            passed_candidates = []

        if not failed_candidates:
            failed_candidates = []
        for candidate in failed_candidates:
            candidate['file_path'] = file_path

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