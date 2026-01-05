import os
import json
import time
from datetime import datetime
from google import genai
from google.genai import types
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# ============================================
# CONFIGURATION
# ============================================


GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'GEMINI_KEY')
SHEET_ID = os.environ.get('GOOGLE_SHEET_ID', 'SHEET_ID')
SHEET_NAME = "Job_Application_Tracker"


RATE_LIMIT_DELAY = 4  

# ============================================
# GEMINI AI SETUP
# ============================================

def setup_gemini():
    
    client = genai.Client(api_key=GEMINI_API_KEY)
    return client


def extract_job_info(client, job_description):
  
    prompt = """
You are an expert at analyzing job descriptions and extracting clean, structured information.

Below is a job description. Based only on what's written, extract the following fields:

- "Company Name"
- "Location"
- "Role"
- "Employement Type" -> if mentioned, include the hybrid, on-site, online inside the brackets() next to the employment type like Full-time (Hybrid); if missing, return just the employment type
- "Salary(Hour or Range)"
- "Posted date"
- "Experience Needed?" → if mentioned, include number of years and domain (e.g., "2+ yrs in React"); if missing, return "-"
- "Key Skills Mentioned" → list all technical or relevant skills, comma separated.
- "Extras Skills" → include soft skills or candidate qualities (e.g., "team player", "detail-oriented") if described
- "Responsibilities" -> list the technologies and responsibilities of the person in this role if mentioned, if missing, return "-"
- "Job is about" → one-line summary of what the person will do in this role. Keep it short, clear, and to the point.
- "Projects" -> if they mention any projects like related to what they want and if they mention it give the short description of it if mentioned. keep it short, clear and to the point.
- "Which Term?" -> which term the job is gonna start like fall, spring and summer keep it one word and to the point and mention the year if mentioned.

IMPORTANT:
- If any information is missing, return "-" for that field.
- Return output strictly as JSON with keys matching the column headers exactly:
"Company Name", "Location", "Role", "Employement Type", "Salary(Hour or Range)", "Posted date", "Experience Needed?", "Key Skills Mentioned", "Extras Skills", "Responsibilities", "Job is about", "Projects", "Which Term?"
"""
    
    full_prompt = f"{prompt}\n\n{job_description}"
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt
        )
        text = response.text.strip()
    
        
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()
        
        data = json.loads(text)
        return data
        
    except Exception as e:
        print(f" Error calling Gemini: {e}")
        return None


# ============================================
# GOOGLE SHEETS SETUP
# ============================================

def get_sheets_service():
    """Connect to Google Sheets API"""
    
    # Path to your service account key file
    key_file = '/home/YOUR_USERNAME/mysite/__________'
    
    creds = Credentials.from_service_account_file(
        key_file,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    
    service = build('sheets', 'v4', credentials=creds)
    return service


def get_sheet_data(service):
    
    
    result = service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID,
        range=f"{SHEET_NAME}!A:Z"
    ).execute()
    
    return result.get('values', [])


def update_row(service, row_number, column_letter, value):
    
    
    cell_range = f"{SHEET_NAME}!{column_letter}{row_number}"
    
    body = {'values': [[value]]}
    
    service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID,
        range=cell_range,
        valueInputOption='RAW',
        body=body
    ).execute()


# ============================================
# MAIN PROCESSING LOGIC
# ============================================

def process_unfilled_rows():

    results = []
    results.append("Starting job tracker...<br>")
    
    try:
        
        client = setup_gemini()
        service = get_sheets_service()
        
        # Get all data from sheet
        data = get_sheet_data(service)
        
        if not data:
            return " No data found in sheet"
        
        headers = data[0]
        col_index = {header: idx for idx, header in enumerate(headers)}
        
        output_columns = [
            "Company Name", "Location", "Role", "Employement Type",
            "Salary(Hour or Range)", "Posted date", "Experience Needed?",
            "Key Skills Mentioned", "Extras Skills", "Responsibilities",
            "Job is about", "Projects", "Which Term?"
        ]
        
        jobs_processed = 0
        
        
        for row_idx in range(1, len(data)):
            row = data[row_idx]
            
            desc_col = col_index.get("Job Description", 0)
            job_desc = row[desc_col] if desc_col < len(row) else ""
            
            autofill_col = col_index.get("Auto-Fill", -1)
            autofill_status = row[autofill_col] if autofill_col < len(row) and autofill_col != -1 else ""
            
            if job_desc and autofill_status != "Done":
                results.append(f"<br>Processing row {row_idx + 1}...<br>")
                
                extracted_data = extract_job_info(client, job_desc)
                
                if not extracted_data:
                    results.append(f" Failed to extract data for row {row_idx + 1}<br>")
                    continue
                
                
                for field in output_columns:
                    if field in col_index:
                        value = extracted_data.get(field, "-")
                        column_letter = chr(65 + col_index[field])
                        update_row(service, row_idx + 1, column_letter, value)
                
               
                if autofill_col != -1:
                    done_column = chr(65 + autofill_col)
                    update_row(service, row_idx + 1, done_column, "Done")
                
                results.append(f" Row {row_idx + 1} completed!<br>")
                jobs_processed += 1
                
               
                results.append(f"Waiting {RATE_LIMIT_DELAY} seconds...<br>")
                time.sleep(RATE_LIMIT_DELAY)
        
        if jobs_processed == 0:
            results.append("<br> All rows are already processed!")
        else:
            results.append(f"<br> Processed {jobs_processed} job(s) successfully!")
        
        return ''.join(results)
        
    except Exception as e:
        return f" Error: {str(e)}"


# ============================================
# FLASK WEB APP (for PythonAnywhere)
# ============================================

from flask import Flask, render_template_string

app = Flask(__name__)


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Job Tracker</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
        }
        .button {
            background: #4285f4;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            text-decoration: none;
            display: inline-block;
        }
        .button:hover {
            background: #357ae8;
        }
        .output {
            margin-top: 20px;
            padding: 15px;
            background: #f9f9f9;
            border-left: 4px solid #4285f4;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1> Job Application Tracker</h1>
        <p>Click the button below to process unfilled job descriptions in your Google Sheet.</p>
        <a href="/process" class="button"> Process Jobs</a>
        {% if message %}
        <div class="output">
            {{ message | safe }}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    
    return render_template_string(HTML_TEMPLATE)

@app.route('/process')
def process():
    
    message = process_unfilled_rows()
    return render_template_string(HTML_TEMPLATE, message=message)


if __name__ == "__main__":
    app.run(debug=True)
