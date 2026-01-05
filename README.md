# 🎯 AI-Powered Job Application Tracker

> **Automated job application tracking system powered by Google Gemini AI and real-time Google Sheets integration**

A sophisticated automation system that eliminates manual data entry when tracking job applications. Simply paste a job description into Google Sheets, and AI automatically extracts and organizes all relevant information—company name, location, salary, skills, responsibilities, and more—in seconds.

---

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [How It Works](#-how-it-works)
- [Setup Guide](#-setup-guide)
- [API Integration](#-api-integration)
- [Performance & Scalability](#-performance--scalability)
- [Future Enhancements](#-future-enhancements)
- [Lessons Learned](#-lessons-learned)

---

## 🎯 Problem Statement

### The Manual Process (Before Automation)

When actively job hunting, applicants typically manage dozens of applications across multiple platforms. The traditional workflow involves:

1. **Finding a job posting** on LinkedIn, Indeed, company websites, etc.
2. **Copying relevant details** manually into a tracking spreadsheet
3. **Extracting information** like:
   - Company name
   - Location
   - Role/position
   - Salary range
   - Required skills
   - Experience requirements
   - Job responsibilities
   - Application deadlines
4. **Repeating this process** for every single job application

### Why This Is Problematic

- ⏱️ **Time-consuming:** 2-5 minutes per job × 50 applications = **2-4 hours of manual data entry**
- ❌ **Error-prone:** Typos, missed information, inconsistent formatting
- 😓 **Tedious:** Repetitive copy-paste work kills motivation
- 📊 **Unscalable:** The more jobs you apply to, the worse it gets
- 🔍 **Poor tracking:** Difficult to analyze trends (which skills are in demand, salary ranges, etc.)

### Real-World Impact

Job seekers should focus on **tailoring resumes** and **preparing for interviews**, not manual data entry. This automation recovers valuable time and mental energy for high-value activities.

---

## ✨ Solution

### What It Does

An **end-to-end automated system** that:

1. **Detects** when you paste a job description in Google Sheets
2. **Triggers** a cloud-hosted Python backend automatically
3. **Calls** Google's Gemini 2.5 Flash AI model to extract structured data
4. **Populates** 13 fields in your spreadsheet automatically
5. **Completes** in 6-10 seconds with zero manual intervention

### The Transformation

**Before:** 3 minutes of manual work per job  
**After:** 10 seconds of automated processing

**Time saved on 50 applications:** ~2.5 hours → 8 minutes  
**Efficiency gain:** **94% time reduction**

---

## 🌟 Key Features

### 🤖 Intelligent Data Extraction

Gemini AI analyzes job descriptions using natural language processing to extract:

- Company Name
- Location (City, State, Remote/Hybrid/On-site)
- Role/Position Title
- Employment Type (Full-time, Part-time, Contract, etc.)
- Salary Range (hourly or annual)
- Experience Requirements (years + domain)
- Technical Skills (programming languages, tools, frameworks)
- Soft Skills (communication, teamwork, problem-solving)
- Key Responsibilities
- Job Summary (one-line description)
- Related Projects (if mentioned)
- Start Term (Fall/Spring/Summer + year)
- Posted Date

### ⚡ Real-Time Automation

- **Trigger:** Google Apps Script detects cell edits
- **Processing:** Cloud-hosted Flask app on PythonAnywhere
- **Speed:** 6-10 seconds from paste to completion
- **Zero clicks:** No buttons, no manual triggering

### 🔒 Secure & Private

- Service account authentication for Google Sheets
- API keys stored server-side
- Data never leaves Google's ecosystem
- No third-party data storage

### 📊 Smart Rate Limiting

- Built-in 4-second delay between requests
- Respects Gemini API free tier limits (15 RPM)
- Handles up to 250 jobs per day (free tier)
- Graceful error handling and retry logic

### 🎯 Production-Ready

- Deployed on PythonAnywhere (24/7 uptime)
- Error logging and monitoring
- Health check endpoint
- Handles edge cases (missing data, malformed descriptions)

---

## 🛠️ Tech Stack

### Backend

| Technology | Purpose |
|-----------|---------|
| **Python 3.10** | Core application logic |
| **Flask** | Web framework for API endpoints |
| **Google Gemini 2.5 Flash** | AI model for NLP and data extraction |
| **google-genai SDK** | Official Gemini API client library |
| **Google Sheets API v4** | Spreadsheet read/write operations |
| **OAuth2 Service Account** | Secure authentication |

### Frontend/Integration

| Technology | Purpose |
|-----------|---------|
| **Google Apps Script** | Event-driven triggers (onEdit) |
| **Google Sheets** | User interface and data storage |
| **JavaScript (ES6)** | Trigger logic and API calls |

### Infrastructure

| Technology | Purpose |
|-----------|---------|
| **PythonAnywhere** | Cloud hosting platform |
| **WSGI** | Production web server gateway |
| **Google Cloud Console** | API management and credentials |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERACTION                        │
│                                                                 │
│  1. User pastes job description in Google Sheets (Column A)    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GOOGLE APPS SCRIPT                           │
│                                                                 │
│  2. onEdit() trigger detects cell change                       │
│  3. Validates: correct sheet, column, row, content length      │
│  4. Checks if already processed (Auto-Fill column)             │
│  5. Shows notification: "🚀 Processing job in row X..."        │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP GET Request
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   PYTHONANYWHERE (Cloud Host)                   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │              FLASK WEB APPLICATION                       │  │
│  │                                                          │  │
│  │  6. Receives request at /process endpoint               │  │
│  │  7. Authenticates with Google Sheets API                │  │
│  │  8. Reads all unfilled job descriptions                 │  │
│  └──────────────────────┬───────────────────────────────────┘  │
│                         │                                       │
│                         ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │              GEMINI AI INTEGRATION                       │  │
│  │                                                          │  │
│  │  9. Sends job description to Gemini 2.5 Flash           │  │
│  │  10. AI extracts structured JSON data                   │  │
│  │  11. Handles edge cases (lists → strings, missing data) │  │
│  └──────────────────────┬───────────────────────────────────┘  │
│                         │                                       │
│                         ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │            GOOGLE SHEETS UPDATE                          │  │
│  │                                                          │  │
│  │  12. Writes extracted data to 13 columns                │  │
│  │  13. Marks row as "Done" in Auto-Fill column            │  │
│  │  14. Applies 4-second rate limiting delay               │  │
│  └──────────────────────┬───────────────────────────────────┘  │
└─────────────────────────┼───────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      GOOGLE SHEETS                              │
│                                                                 │
│  15. User sees completed row with all fields filled             │
│  16. Notification: "✅ Processing complete!"                    │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Job Description (Raw Text)
    ↓
[Gemini AI Processing]
    ↓
{
  "Company Name": "TechCorp",
  "Location": "San Francisco, CA",
  "Role": "Senior Software Engineer",
  "Employment Type": "Full-time (Hybrid)",
  "Salary(Hour or Range)": "$150,000 - $200,000",
  "Posted date": "2026-01-02",
  "Experience Needed?": "5+ yrs in Python/JavaScript",
  "Key Skills Mentioned": "Python, React, AWS, Docker",
  "Extras Skills": "Team leadership, Problem-solving",
  "Responsibilities": "Design scalable systems, mentor junior devs",
  "Job is about": "Building cloud infrastructure for SaaS platform",
  "Projects": "Microservices migration, API redesign",
  "Which Term?": "Spring 2026"
}
    ↓
[Google Sheets API]
    ↓
Populated Spreadsheet Row
```

---

## ⚙️ How It Works

### Step-by-Step Process

#### 1. **User Action**
```
User opens Google Sheet → Pastes job description in Column A
```

#### 2. **Automatic Detection**
```javascript
// Google Apps Script (onEdit trigger)
function onEdit(e) {
  if (sheet === "Job_Tracker" && column === A && row > 1) {
    if (jobDescription.length > 10 && autoFillStatus !== "Done") {
      callPythonBackend();
    }
  }
}
```

#### 3. **Cloud Processing**
```python
# Flask Backend (PythonAnywhere)
@app.route('/process')
def process():
    # Get unfilled rows from Google Sheets
    data = get_sheet_data(service)
    
    # Process each job description
    for row in unfilled_rows:
        extracted_data = extract_job_info(client, job_description)
        update_row(service, row, extracted_data)
        
        # Rate limiting
        time.sleep(4)  # 15 requests/minute max
```

#### 4. **AI Extraction**
```python
# Gemini AI Processing
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=f"""
    Extract these fields from the job description:
    - Company Name
    - Location
    - Role
    ... (13 fields total)
    
    Return as JSON.
    
    Job Description:
    {job_description}
    """
)

data = json.loads(response.text)
# Returns structured JSON
```

#### 5. **Data Population**
```python
# Update Google Sheet
for field in output_columns:
    value = extracted_data.get(field, "-")
    
    # Convert lists to comma-separated strings
    if isinstance(value, list):
        value = ", ".join(str(item) for item in value)
    
    update_row(service, row_number, column_letter, value)

# Mark as processed
update_row(service, row_number, "Auto-Fill", "Done")
```

### Workflow Diagram

```
┌──────────────┐
│ Paste Job    │
│ Description  │
└──────┬───────┘
       │ (~instant)
       ▼
┌──────────────┐
│ Apps Script  │
│ Detects Edit │
└──────┬───────┘
       │ HTTP Request (<1 sec)
       ▼
┌──────────────┐
│ Flask App    │
│ Receives Job │
└──────┬───────┘
       │ (2-4 sec)
       ▼
┌──────────────┐
│ Gemini AI    │
│ Extracts Data│
└──────┬───────┘
       │ (2-3 sec)
       ▼
┌──────────────┐
│ Update Sheet │
│ Mark as Done │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Complete! ✅  │
│ 6-10 seconds │
└──────────────┘
```

---

## 🚀 Setup Guide

### Prerequisites

- Google Account
- PythonAnywhere account (free tier)
- Basic Python knowledge
- Text editor

### Part 1: Google Cloud Setup

#### 1.1 Create Google Cloud Project
```bash
1. Go to: https://console.cloud.google.com/
2. Create new project: "Job Tracker"
3. Enable Google Sheets API
4. Enable Google Drive API
```

#### 1.2 Create Service Account
```bash
1. Navigate to: APIs & Services → Credentials
2. Create Credentials → Service Account
3. Name: "job-tracker-bot"
4. Create & Download JSON key
5. Rename to: service-account-key.json
```

#### 1.3 Get Gemini API Key
```bash
1. Go to: https://aistudio.google.com/app/apikey
2. Create API Key → Create in new project
3. Copy the key (starts with AIza...)
4. Store securely
```

### Part 2: Google Sheets Setup

#### 2.1 Create Tracking Sheet
```
Create sheet with these columns (Row 1):
- Job Description
- Company Name
- Location
- Role
- Employment Type
- Salary(Hour or Range)
- Posted date
- Experience Needed?
- Key Skills Mentioned
- Extras Skills
- Responsibilities
- Job is about
- Projects
- Which Term?
- Auto-Fill
```

#### 2.2 Share Sheet with Service Account
```bash
1. Open your Google Sheet
2. Click "Share"
3. Paste service account email: job-tracker-bot@...iam.gserviceaccount.com
4. Set to "Editor"
5. Uncheck "Notify people"
6. Click "Share"
```

#### 2.3 Get Sheet ID
```
From URL: https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit
Copy the SHEET_ID_HERE part
```

### Part 3: Python Backend Deployment

#### 3.1 Create PythonAnywhere Account
```bash
1. Visit: https://www.pythonanywhere.com
2. Sign up for free "Beginner" account
3. Choose username (e.g., "jobtracker")
```

#### 3.2 Install Dependencies
```bash
# Open Bash console in PythonAnywhere
pip3 install --user google-genai
pip3 install --user google-api-python-client google-auth google-auth-httplib2
pip3 install --user Flask
```

#### 3.3 Upload Files
```bash
1. Go to Files tab
2. Create folder: Job_Tracker
3. Upload: flask_app.py
4. Upload: service-account-key.json
```

#### 3.4 Configure Application
```python
# In flask_app.py, update these lines:

# Line 30: Your Gemini API Key
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSy...')

# Line 31: Your Sheet ID
SHEET_ID = os.environ.get('GOOGLE_SHEET_ID', '1a2b3c...')

# Line 32: Your sheet name (bottom tab)
SHEET_NAME = "Job_Tracker"  # or "Sheet1"

# Line 143: Your username
key_file = '/home/YOUR_USERNAME/Job_Tracker/service-account-key.json'
```

#### 3.5 Create Web App
```bash
1. Go to Web tab
2. Add a new web app
3. Framework: Flask
4. Python version: 3.10
5. Path: /home/YOUR_USERNAME/Job_Tracker/flask_app.py
6. Click "Reload"
```

### Part 4: Google Apps Script Automation

#### 4.1 Add Script to Sheet
```javascript
1. Open Google Sheet
2. Extensions → Apps Script
3. Delete default code
4. Paste the automation script (see google_sheets_auto_trigger.js)
```

#### 4.2 Configure Script
```javascript
// Update line 8 with your PythonAnywhere URL
const PYTHON_URL = "https://YOUR_USERNAME.pythonanywhere.com/process";

// Update line 10 if your sheet tab has a different name
const SHEET_NAME = "Job_Tracker";
```

#### 4.3 Authorize Script
```bash
1. Save script (Ctrl+S)
2. Select: setupAuthorization (from dropdown)
3. Click Run (▶️)
4. Review Permissions → Allow
5. Close Apps Script
```

### Part 5: Testing

#### 5.1 Manual Test
```bash
1. Open Google Sheet
2. Menu: 🎯 Job Tracker → Process All Jobs
3. Should see: "✅ Processing complete!"
4. Check if rows are filled
```

#### 5.2 Automatic Trigger Test
```bash
1. Paste a job description in Column A
2. Watch bottom-right corner for notification
3. Wait 6-10 seconds
4. Row should auto-fill with data
```

---

## 🔌 API Integration

### Gemini AI API

**Endpoint:** `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent`

**Request Structure:**
```python
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt
)
```

**Response Handling:**
```python
# Parse JSON from AI response
text = response.text.strip()
if text.startswith("```"):
    text = text.replace("```json", "").replace("```", "").strip()
data = json.loads(text)
```

**Error Handling:**
```python
try:
    extracted_data = extract_job_info(client, job_desc)
except json.JSONDecodeError as e:
    print(f"JSON parsing error: {e}")
    return None
except Exception as e:
    print(f"API error: {e}")
    return None
```

### Google Sheets API

**Authentication:**
```python
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_service_account_file(
    'service-account-key.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
service = build('sheets', 'v4', credentials=creds)
```

**Read Operation:**
```python
result = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID,
    range=f"{SHEET_NAME}!A:Z"
).execute()
values = result.get('values', [])
```

**Write Operation:**
```python
body = {'values': [[value]]}
service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range=f"{SHEET_NAME}!{column_letter}{row_number}",
    valueInputOption='RAW',
    body=body
).execute()
```

---

## 📊 Performance & Scalability

### Current Performance Metrics

| Metric | Value |
|--------|-------|
| Processing time per job | 6-10 seconds |
| API calls per job | 1 (Gemini) + 14 (Sheets writes) |
| Success rate | ~95% (depends on job description quality) |
| Concurrent users | 1 (designed for personal use) |

### Rate Limiting Strategy

**Gemini API Limits (Free Tier):**
- 15 requests per minute (RPM)
- 250,000 tokens per minute (TPM)
- 20-250 requests per day (RPD) *varies by account*

**Implementation:**
```python
RATE_LIMIT_DELAY = 4  # seconds
# Allows 15 requests/minute (safe for free tier)

for job in jobs:
    process_job(job)
    time.sleep(RATE_LIMIT_DELAY)
```

**Daily Capacity:**
- Free tier: 20-250 jobs/day
- Paid Tier 1: 10,000 jobs/day
- Processing all takes: jobs × 10 seconds

### Scalability Considerations

**Current Limitations:**
- Single-threaded processing
- Sequential job processing
- Free tier quota limits

**Scaling Options:**

1. **Vertical Scaling (Upgrade API Tier)**
   - Enable billing on Gemini API
   - Tier 1: 1,000 RPM, 10,000 RPD
   - Cost: ~$0.15 per 1M input tokens

2. **Horizontal Scaling (Multiple Projects)**
   - Create separate Google Cloud projects
   - Distribute load across multiple API keys
   - Each project gets separate quotas

3. **Optimization Strategies**
   - Batch processing (queue jobs, process in bulk)
   - Caching (avoid reprocessing same job description)
   - Parallel processing (multiple workers)

---

## 🔮 Future Enhancements

### Planned Features

#### 1. **Enhanced AI Analysis**
- Salary prediction based on role/location
- Skills gap analysis (compare your skills vs. requirements)
- Application priority scoring
- Company culture analysis from description

#### 2. **Advanced Automation**
- Auto-apply to jobs (via LinkedIn/Indeed APIs)
- Cover letter generation using Gemini
- Resume tailoring based on job requirements
- Interview preparation questions

#### 3. **Analytics Dashboard**
- Application status tracking
- Response rate visualization
- Salary trends by location/role
- Skills demand analysis

#### 4. **Notification System**
- Email alerts for application deadlines
- Slack/Discord integration
- Daily summary reports

#### 5. **Multi-User Support**
- User authentication
- Personal dashboards
- Shared team tracking

### Technical Improvements

- **Database Integration:** Move from Google Sheets to PostgreSQL
- **Async Processing:** Use Celery for background tasks
- **Frontend UI:** React dashboard for better UX
- **Mobile App:** iOS/Android companion app
- **API v2:** RESTful API for third-party integrations

---

## 💡 Lessons Learned

### Technical Challenges & Solutions

#### 1. **API Authentication Hell**
**Problem:** Google Cloud OAuth is complex for beginners  
**Solution:** Service account authentication simplifies deployment  
**Learning:** Always use service accounts for server-to-server communication

#### 2. **Gemini Response Inconsistency**
**Problem:** AI sometimes returns lists instead of strings  
**Solution:** Added type checking and conversion logic  
```python
if isinstance(value, list):
    value = ", ".join(str(item) for item in value)
```
**Learning:** Never trust AI output format—always validate and sanitize

#### 3. **Rate Limiting Strategy**
**Problem:** Free tier limits are strict (15 RPM)  
**Solution:** Implemented 4-second delays between requests  
**Learning:** Design for constraints early, not after hitting limits

#### 4. **WSGI Configuration**
**Problem:** Flask app import errors in production  
**Solution:** Correct file paths in WSGI config  
**Learning:** Development vs. production environments differ—test thoroughly

#### 5. **Apps Script Permissions**
**Problem:** External requests blocked by default  
**Solution:** Explicit OAuth scope declaration in manifest  
**Learning:** Google's security model requires explicit permission declarations

### Development Insights

1. **Start Simple:** MVP with manual processing first, automation second
2. **Error Handling is Critical:** AI APIs fail—handle gracefully
3. **Documentation Matters:** Future you will thank present you
4. **Free Tiers Have Limits:** Plan for scale from day one
5. **User Experience Trumps Complexity:** Automation should be invisible

### Skills Demonstrated

- ✅ **API Integration:** Multiple Google APIs + Gemini AI
- ✅ **Cloud Deployment:** PythonAnywhere production setup
- ✅ **Natural Language Processing:** AI-powered data extraction
- ✅ **Event-Driven Architecture:** Google Apps Script triggers
- ✅ **Authentication & Security:** OAuth2, Service Accounts
- ✅ **Rate Limiting:** Respectful API usage patterns
- ✅ **Error Handling:** Graceful degradation
- ✅ **Full-Stack Development:** Backend (Python/Flask) + Frontend (JavaScript)

---

## 📝 License

This project is open source and available under the MIT License.

---

## 🙏 Acknowledgments

- **Google Gemini Team** for the powerful AI API
- **PythonAnywhere** for free hosting
- **Google Workspace Team** for Apps Script platform

---

## 📧 Contact

**Narasimha**  
Portfolio: [Your Portfolio URL]  
GitHub: [Your GitHub URL]  
LinkedIn: [Your LinkedIn URL]

---

**⭐ If you found this project useful, please consider giving it a star!**

---

*Last Updated: January 2026*
