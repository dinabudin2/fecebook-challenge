import pdfplumber
import pandas as pd
import os

def extract_text_from_pdf(pdf_path):
    """
    מחלץ טקסט מקובץ PDF.
    
    pdf_path: הנתיב לקובץ ה-PDF.
    """
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
    """
    מחלץ טבלאות מקובץ PDF.
    
    pdf_path: הנתיב לקובץ ה-PDF.
    """
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

def get_user_conversion_choice():
    print("Select the type of conversion you want:")
    print("1. Convert PDF to Text")
    print("2. Convert PDF to Tables")
    choice = input("Enter the number of your choice: ")
    return choice

def get_output_file_type():
    print("Select the type of output file you want:")
    print("1. Excel (.xlsx)")
    print("2. CSV (.csv)")
    print("3. JSON (.json)")
    file_type = input("Enter the number of your choice: ")
    return file_type

def save_to_file(data, file_type, file_name):
    """
    שומר את הנתונים לקובץ לפי סוג הקובץ שנבחר.
    """
    if file_type == '1':  # Excel
        df = pd.DataFrame(data)
        df.to_excel(file_name, index=False)
        print(f"Data saved to {file_name} as Excel file.")
    elif file_type == '2':  # CSV
        df = pd.DataFrame(data)
        df.to_csv(file_name, index=False)
        print(f"Data saved to {file_name} as CSV file.")
    elif file_type == '3':  # JSON
        with open(file_name, 'w') as f:
            import json
            json.dump(data, f)
        print(f"Data saved to {file_name} as JSON file.")
    else:
        print("Invalid file type chosen.")

def pdf_to_excel_pro(pdf_path, file_name, conversion_choice):
    """
    מבצע המרה של PDF לפי הבחירה של המשתמש (טקסט או טבלאות) ומבצע עיבוד בהתאם.
    
    pdf_path: הנתיב לקובץ ה-PDF.
    file_name: שם קובץ הפלט שיווצר.
    conversion_choice: הבחירה של המשתמש לגבי סוג ההמרה.
    """
    if conversion_choice == '1':  # המרת PDF לטקסט
        text_data = extract_text_from_pdf(pdf_path)
        if text_data is None:
            print("Failed to extract text from PDF.")
            return
        save_to_file(text_data, '1', file_name)  # שמירת טקסט
    
    elif conversion_choice == '2':  # המרת PDF לטבלאות
        tables_data = extract_tables_from_pdf(pdf_path)
        if tables_data is None or len(tables_data) == 0:
            print("No tables found in PDF.")
            return
        save_to_file(tables_data, '1', file_name)  # שמירת טבלאות

# דוגמה לשימוש:
pdf_file = input("Please enter the path to the PDF file: ")
output_file = input("Please enter the desired name for the output file (without extension): ")

# בדיקת סוג ההמרה שהמשתמש רוצה לבצע
conversion_choice = get_user_conversion_choice()

# בדיקת סוג קובץ הפלט שהמשתמש רוצה
file_type = get_output_file_type()

# שמירת קובץ ה-Excel/CSV/JSON
if file_type == '1':
    file_name = f"{output_file}.xlsx"
elif file_type == '2':
    file_name = f"{output_file}.csv"
elif file_type == '3':
    file_name = f"{output_file}.json"
else:
    print("Invalid file type chosen.")
    file_name = f"{output_file}.xlsx"

# קריאה לפונקציה עם הפרמטרים
pdf_to_excel_pro(pdf_file, file_name, conversion_choice)
