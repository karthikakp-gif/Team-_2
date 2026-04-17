import streamlit as st
import pdfplumber
import docx
import nltk
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Page config
st.set_page_config(page_title="Resume ATS", layout="wide")

nltk.download('stopwords')

# -------------------------------
# FUNCTIONS
# -------------------------------
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return text

def extract_resume_text(file):
    if file.name.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif file.name.endswith(".docx"):
        return extract_text_from_docx(file)
    return ""

def preprocess_text(text):
    text = text.lower()
    words = text.split()
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if w not in stop_words]
    return " ".join(words)

skills = [
    "python", "machine learning", "ml",
    "sql", "data analysis",
    "communication", "deep learning",
    "pandas", "numpy"
]

def skill_match_score(resume_text, jd_text):
    matched = []
    for skill in skills:
        if skill in resume_text and skill in jd_text:
            matched.append(skill)
    score = (len(matched) / len(skills)) * 100
    return score, matched

def calculate_similarity(resume_text, jd_text):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])
    return similarity[0][0] * 100

def final_score(resume_text, jd_text):
    sim, skill, matched = 0, 0, []
    sim = calculate_similarity(resume_text, jd_text)
    skill, matched = skill_match_score(resume_text, jd_text)
    final = (0.6 * sim) + (0.4 * skill)
    return final, sim, skill, matched

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("⚙️ Settings")

threshold = st.sidebar.slider("Minimum Score", 0, 100, 50)

st.sidebar.markdown("### 📌 Instructions")
st.sidebar.write("1. Enter Job Description")
st.sidebar.write("2. Upload resumes")
st.sidebar.write("3. Click Analyze")

# -------------------------------
# MAIN UI
# -------------------------------
st.title("📄 AI Resume Screening Dashboard")
st.markdown("### Smart Candidate Evaluation System")

jd_text = st.text_area("📌 Job Description", height=150)

uploaded_files = st.file_uploader(
    "📂 Upload Resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

# -------------------------------
# ANALYZE BUTTON
# -------------------------------
if st.button("🚀 Analyze Resumes"):

    if not jd_text:
        st.warning("Please enter a Job Description")
    elif not uploaded_files:
        st.warning("Please upload resumes")
    else:
        results = []

        for file in uploaded_files:
            text = extract_resume_text(file)
            clean_resume = preprocess_text(text)
            clean_jd = preprocess_text(jd_text)

            final, sim, skill, matched = final_score(clean_resume, clean_jd)

            status = "Selected" if final >= threshold else "Rejected"

            results.append({
                "Name": file.name,
                "Score": round(final, 2),
                "Similarity": round(sim, 2),
                "Skill Score": round(skill, 2),
                "Skills": ", ".join(matched),
                "Status": status
            })

        # Sort results
        results = sorted(results, key=lambda x: x["Score"], reverse=True)

        df = pd.DataFrame(results)

        # -------------------------------
        # SUMMARY METRICS
        # -------------------------------
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Candidates", len(df))
        col2.metric("Selected", len(df[df["Status"] == "Selected"]))
        col3.metric("Rejected", len(df[df["Status"] == "Rejected"]))

        st.markdown("---")

        # -------------------------------
        # TABLE VIEW
        # -------------------------------
        st.subheader("📊 Candidate Ranking")
        st.dataframe(df, use_container_width=True)

        st.markdown("---")

        # -------------------------------
        # CARD VIEW
        # -------------------------------
        st.subheader("📄 Detailed Results")

        for i, row in df.iterrows():
            with st.container():
                col1, col2 = st.columns([3,1])

                with col1:
                    st.markdown(f"### {row['Name']}")
                    st.write(f"Score: *{row['Score']}*")
                    st.write(f"Matched Skills: {row['Skills']}")

                with col2:
                    if row["Status"] == "Selected":
                        st.success("✅ Selected")
                    else:
                        st.error("❌ Rejected")

                st.markdown("---")