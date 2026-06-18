import streamlit as st
import re
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import pdfplumber
from PIL import Image
import pytesseract


# -----------------------------
# APP CONFIG
# -----------------------------
st.set_page_config(page_title="AI Resume Optimizer", layout="centered")
st.title("📄 AI Resume Optimizer (Final Stable Version)")


# -----------------------------
# INPUT
# -----------------------------
st.subheader("📥 Input Resume")

input_type = st.radio("Choose input type:", ["✍️ Text", "📄 PDF", "🖼️ Image"])

resume_text = ""


# TEXT INPUT
if input_type == "✍️ Text":
    resume_text = st.text_area("Enter Resume Text")


# PDF INPUT
elif input_type == "📄 PDF":
    file = st.file_uploader("Upload PDF Resume", type=["pdf"])
    if file:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                resume_text += page.extract_text() or ""
        st.success("PDF extracted successfully")


# IMAGE INPUT
elif input_type == "🖼️ Image":
    img_file = st.file_uploader("Upload Image Resume", type=["png", "jpg", "jpeg"])
    if img_file:
        img = Image.open(img_file)
        resume_text = pytesseract.image_to_string(img)
        st.success("Image extracted successfully")


if resume_text:
    st.subheader("📄 Extracted Resume")
    st.write(resume_text)


# -----------------------------
# EXPANSIONS
# -----------------------------
expansions = {
    "cse": "Computer Science Engineering",
    "cs": "Computer Science",
    "it": "Information Technology",
    "ece": "Electronics and Communication Engineering",
    "eee": "Electrical and Electronics Engineering",
    "mech": "Mechanical Engineering",
    "civil": "Civil Engineering",
    "aiml": "Artificial Intelligence and Machine Learning",
    "ai": "Artificial Intelligence",
    "ds": "Data Science",

    "btech": "Bachelor of Technology",
    "mtech": "Master of Technology",
    "be": "Bachelor of Engineering",

    "ml": "Machine Learning",
    "dl": "Deep Learning",
    "nlp": "Natural Language Processing",
    "cv": "Computer Vision",
    "os": "Operating Systems",
    "dbms": "Database Management Systems",
    "sql": "Structured Query Language",
    "oops": "Object Oriented Programming System",
    "cn": "Computer Networks",

    "cpp": "C++",
    "py": "Python",
    "js": "JavaScript",

    "cgpa": "Cumulative Grade Point Average",
    "gpa": "Grade Point Average",

    "engg": "Engineering"
}


# -----------------------------
# GRAMMAR FIX (SAFE OFFLINE)
# -----------------------------
def fix_grammar(text):

    text = text.strip()

    # fix lowercase "i"
    text = re.sub(r'\bi\b', 'I', text)

    # contractions
    text = text.replace(" dont ", " do not ")
    text = text.replace(" didnt ", " did not ")
    text = text.replace(" cant ", " cannot ")

    # spacing cleanup
    text = re.sub(r'\s+', ' ', text)

    return text


# -----------------------------
# OPTIMIZER (FIXED PUNCTUATION)
# -----------------------------
def optimize_resume(text):

    text = fix_grammar(text)

    # expansions
    for k, v in expansions.items():
        text = re.sub(rf"\b{k}\b", v, text, flags=re.IGNORECASE)

    # IMPORTANT FIX: preserve punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text)

    fixed = []
    for s in sentences:
        s = s.strip()
        if not s:
            continue

        # only fix first letter
        s = s[0].upper() + s[1:]
        fixed.append(s)

    return " ".join(fixed)


# -----------------------------
# ATS SCORE (IMPROVED)
# -----------------------------
def calculate_ats(text):

    text = text.lower()

    keywords = {
        "python": 10,
        "machine learning": 10,
        "artificial intelligence": 10,
        "data science": 10,
        "sql": 8,
        "java": 6,
        "c++": 6,
        "javascript": 6,
        "computer science engineering": 10,
        "project": 6,
        "internship": 6,
        "problem solving": 6
    }

    score = 0

    for k, v in keywords.items():
        if k in text:
            score += v

    words = len(text.split())
    if words > 80:
        score += 10
    if words > 150:
        score += 10

    return min(score, 100)


# -----------------------------
# PDF GENERATOR
# -----------------------------
def generate_pdf(text):

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    y = 750
    p.setFont("Helvetica", 10)

    for line in text.split("\n"):
        if y < 40:
            p.showPage()
            y = 750
            p.setFont("Helvetica", 10)

        p.drawString(40, y, line[:100])
        y -= 15

    p.save()
    buffer.seek(0)
    return buffer


# -----------------------------
# RUN
# -----------------------------
if resume_text and st.button("🚀 Optimize Resume"):

    optimized = optimize_resume(resume_text)

    st.subheader("📊 Before vs After")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ❌ Original")
        st.write(resume_text)

    with col2:
        st.markdown("### ✅ Optimized")
        st.write(optimized)


    # ATS SCORE
    score = calculate_ats(optimized)

    st.subheader("🎯 ATS Score")
    st.progress(score)
    st.write(f"Score: {score}/100")


    # PDF DOWNLOAD
    pdf_file = generate_pdf(optimized)

    st.download_button(
        "📥 Download Optimized Resume PDF",
        pdf_file,
        file_name="optimized_resume.pdf",
        mime="application/pdf"
    )
