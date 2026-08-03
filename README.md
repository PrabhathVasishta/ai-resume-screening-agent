# AI Resume Screening Agent

An AI-powered Resume Screening Agent that compares multiple resumes against a Job Description using NLP and LLMs.

## Features

- Upload Job Description (PDF, DOCX, TXT)
- Upload Multiple Resumes
- Automatic Resume Parsing
- Skill Extraction
- TF-IDF + Cosine Similarity Matching
- AI-generated Recruiter Feedback
- Candidate Ranking
- Export Results to CSV and JSON

---

## Tech Stack

- Python
- Streamlit
- Scikit-learn
- pdfplumber
- python-docx
- OpenAI SDK (Groq)
- Pandas

---

## Project Structure

```
resume_screening_agent/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .env
│
├── data/
│   └── skills.txt
│
├── output/
│
├── src/
│   ├── parser.py
│   ├── processor.py
│   ├── matcher.py
│   ├── llm.py
│   ├── exporter.py
│   └── pipeline.py
```

---

## Installation

```bash
git clone <repository-url>

cd resume_screening_agent

pip install -r requirements.txt
```

---
## Sample Files

The repository contains sample files for quick evaluation.

### Sample Job Description

```
data/job_description/sample_jd.pdf
```

### Sample Resumes

```
data/resumes/
```

Run the application:

```bash
python -m streamlit run app.py
```

Upload the sample Job Description and sample resumes to immediately test the application.

## Configure API Key

Create a `.env` file

```
GROQ_API_KEY=your_api_key
```

---

## Run

```bash
streamlit run app.py
```

---

## Workflow

```
Upload JD
      ↓
Upload Resumes
      ↓
Resume Parsing
      ↓
Text Cleaning
      ↓
Skill Extraction
      ↓
Resume Matching
      ↓
AI Feedback
      ↓
Candidate Ranking
      ↓
Export Results
```

---

## Output

- Ranked Candidates
- Match Score
- Matched Skills
- Missing Skills
- AI Recommendation
- CSV Export
- JSON Export