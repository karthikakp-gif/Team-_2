# AI Resume Screening System (Mini ATS)

## Project Overview

This project is a **Resume Screening System** built using Python and Streamlit.
It simulates an **Applicant Tracking System (ATS)** used by companies to filter and rank candidates based on their resumes.

The system compares uploaded resumes with a given job description and:

* Extracts text from PDF/DOCX files
* Matches skills
* Calculates similarity
* Generates a score
* Classifies candidates as **Selected** or **Rejected**

---

## Features

* 📂 Upload multiple resumes (PDF & DOCX)
* 📌 Enter job description
* 🧹 Automatic text preprocessing (stopword removal)
* 🧠 Skill matching system
* 📊 TF-IDF + Cosine Similarity scoring
* 📈 Final weighted score calculation
* ✅ Candidate selection based on threshold
* 📋 Table view + detailed card view
* 📊 Dashboard metrics (Selected / Rejected count)

---

## How It Works

### 1. Resume Upload

Users upload resumes in:

* PDF format (handled by `pdfplumber`)
* DOCX format (handled by `python-docx`)

---

### 2. Text Extraction

* Extracts readable text from resumes
* Converts job description into comparable format

---

### 3. Text Preprocessing

* Converts text to lowercase
* Removes stopwords (e.g., “the”, “and”, “is”)
* Cleans and prepares data for analysis

---

### 4. Skill Matching

* Compares predefined skills with:

  * Resume content
  * Job description
* Calculates **Skill Match Score**

---

### 5. Similarity Calculation

* Uses **TF-IDF Vectorization**
* Applies **Cosine Similarity** to measure text similarity

---

### 6. Final Score Calculation

```
Final Score = (0.6 × Similarity Score) + (0.4 × Skill Score)
```

---

### 7. Candidate Selection

* If Final Score ≥ Threshold → ✅ Selected
* Else → ❌ Rejected

---

## Technologies Used

* Python
* Streamlit
* pdfplumber
* python-docx
* NLTK
* Scikit-learn
* Pandas

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/resume-ats.git
cd resume-ats
```

---

### 2. Install dependencies

```bash
pip install streamlit pandas scikit-learn nltk pdfplumber python-docx
```

---

### 3. Download NLTK data

Run this once:

```python
import nltk
nltk.download('stopwords')
```

---

## Running the App

```bash
streamlit run resume.py
```

Then open in browser:

```
http://localhost:8501
```

---

## Usage

1. Enter Job Description
2. Upload one or more resumes
3. Click **Analyze Resumes**
4. View:

   * Candidate scores
   * Selected vs Rejected
   * Matched skills

---

## Output

* Ranked candidates table
* Individual candidate cards
* Dashboard metrics

---

## Test Cases

The system handles:

* Strong candidates (high match)
* Weak candidates (low match)
* Edge cases (empty or minimal data)

---

## Future Improvements

* Upload resumes via drag-and-drop UI
* Add charts (score visualization)
* Use advanced NLP (Named Entity Recognition)
* Improve skill extraction dynamically
* Deploy app online (Streamlit Cloud)

---

## Author

**Karthika K Pillai**

---

## Project Purpose

This project is built as a **learning implementation of an ATS system** and demonstrates skills in:

* Python
* NLP basics
* Data processing
* Streamlit app development

---

## License

This project is for educational purposes.
