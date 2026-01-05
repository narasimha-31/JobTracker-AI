# JobTracker AI

## The Problem

When applying to jobs at scale, tracking applications becomes **manual, repetitive, error-prone, and ultimately wastes valuable time**.

For every job:
- Copy company name, role, location
- Extract required skills & responsibilities
- Manually store everything
- Search for the job description again when prepping for interviews

## Time 

| Scenario | Manual |
|--------|--------|
| Time per job | 3–5 min | 
| 50 jobs | ~2.5 hrs | 
| Effort | High |

This work adds **zero value** to your job search focus.

---

## The Solution

An **AI-powered, zero-click Google Sheets tracker** that:
- Detects pasted job descriptions
- Automatically structures 13 fields of data
- Fills the row in **6–10 seconds**
- Provides clean data you can query, sort, and analyze

No buttons. No manual formatting. No re-searching later.

---

## Why This Is Useful (Beyond Time Saved)

- **Instant interview prep:** See required skills and job summary at a glance instead of searching the original posting.
- **Consistent data:** Every job logged with the same schema.
- **Analysis-ready:** Build dashboards or run trends on your applied jobs.
- **Context-rich tracking:** Helps you understand which roles and skills lead to interviews.

---

## Time & Effort Reduction (Measured Impact)

| Scenario | Manual | Automated | Reduction |
|--------|--------|-----------|-----------|
| Time per job | 3–5 min | 6–10 sec | **~94%** |
| 50 jobs | ~2.5 hrs | ~8 min | **~2h 22m saved** |
| Effort | High | Near zero | **Eliminated** |

---

## What Data Is Extracted (Horizontal)

| Company | Location | Role | Type | Salary | Exp | Key Skills | Extra Skills | Responsibilities | Summary | Projects | Term | Posted |
|---------|----------|------|------|--------|-----|------------|--------------|------------------|---------|----------|------|--------|

- **13 structured fields**
- Missing info handled with `-`
- Output is analysis-ready

---


## How It Works (High Level)
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



## Free Tier & API Usage Limits

**Model:** Google Gemini 2.5 Flash (text-to-text extraction)

Free tier limitations:
- **5 requests per minute (RPM)**
- **20 requests per day (RPD)**
- **250,000 tokens per minute**

These limits make the free tier suitable for light users (≤20 jobs/day).  
If you apply to **more than ~20 jobs/day**, free tier isn’t sufficient, you may hit the RPM/RPD limits even if token quota remains.

**Paid tier benefits:**
- Much higher requests per day
- Higher RPM limits
- More throughput for high-velocity applicants

👉 **Why this matters:**  
If you’re applying >20 jobs/day, the free tier will throttle you, the tracker still works, but you’ll wait for rate limits or need paid API capacity.

---

## Technical Implementation

### Architecture
- Event-driven automation (no click required)
- Google Apps Script trigger
- Flask API backend
- AI extraction with strict JSON enforcement
- Production deployment (WSGI)

---

## Tech Stack

**Backend**
- Python 3.10
- Flask
- Gemini 2.5 Flash
- Google Sheets API (OAuth2 Service Account)

**Automation**
- Google Apps Script

**Deployment**
- PythonAnywhere (Cloud)

---

## Skills Demonstrated

**Technical**
- REST & OAuth2 APIs
- AI prompt engineering
- Event-driven automation
- Backend production deployment
- Error handling & rate limiting

**Engineering impact**
- Reduced manual workload by ~94%
- Built analysis-ready structured dataset
- Enabled interview prep with consistent job metadata

---

## Future Enhancements (Data-Focused)

- **Application Metrics**
  - Jobs applied / day, week, company, location
- **Sheets Dashboards**
  - Salary distribution
  - Skill frequency charts
  - Top companies applied
- **AI Summaries & Insights**
  - Weekly application summary
  - Skill gap reports
  - Resume targeting suggestions
- **Trend Views**
  - Which roles → interviews
  - Skill sets with highest responses

Goal: save even more time, from **data entry** → **decision support**.

---

## Status

- Production-ready
- Actively used
- Free-tier friendly (limited use)

---

## One-Line Summary

AI-powered job tracking that turns a 3-minute manual task into a 10-second automated system while creating clean data you can analyze and reuse.

---
## Connect with Me

**LinkedIn:** https://www.linkedin.com/in/narasimha31
**Portfolio:** https://narasimharoyal.com

