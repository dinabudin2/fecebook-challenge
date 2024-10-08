from flask import Flask, render_template, request, redirect, url_for, send_file
import pdfplumber
import pandas as pd
import os
import sqlite3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# חיבור למסד הנתונים
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    conn.close()

# דף הבית
@app.route('/')
def index():
    return render_template('index.html')

# דף העלאת קובץ
@app.route('/upload')
def upload():
    return render_template('upload.html')

# פונקציה שמבצעת את ההמרה
@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    conversion_type = request.form['conversion']
    output_format = request.form['format']

    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # ביצוע ההמרה בהתאם לבחירה של המשתמש
        if conversion_type == 'text':
            data = extract_text_from_pdf(file_path)
        elif conversion_type == 'tables':
            data = extract_tables_from_pdf(file_path)

        # שמירת הקובץ בפורמט הנבחר
        output_file = os.path.join(app.config['UPLOAD_FOLDER'], 'output.' + output_format)
        save_to_file(data, output_format, output_file)

        return send_file(output_file, as_attachment=True)

    return "Invalid file format. Please upload a PDF."

# פונקציות לחילוץ טקסט וטבלאות, ושמירת הפלט
def extract_text_from_pdf(pdf_path):
    text_data = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    lines = text.split('\n')
                    text_data.extend(lines)
        return text_data
    
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

def extract_tables_from_pdf(pdf_path):
    tables_data = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables_on_page = page.extract_tables()
                for table in tables_on_page:
                    tables_data.append(table)
        return tables_data
    
    except Exception as e:
        print(f"Error extracting tables: {e}")
        return None

def save_to_file(data, file_type, file_name):
    if file_type == 'xlsx':  # Excel
        df = pd.DataFrame(data)
        df.to_excel(file_name, index=False)
    elif file_type == 'csv':  # CSV
        df = pd.DataFrame(data)
        df.to_csv(file_name, index=False)
    elif file_type == 'json':  # JSON
        with open(file_name, 'w') as f:
            import json
            json.dump(data, f)

if __name__ == '__main__':
    init_db()
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
