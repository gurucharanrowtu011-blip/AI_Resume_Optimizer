import streamlit as st
import re
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import pdfplumber
from PIL import Image
import pytesseract


# OPTIONAL (Windows only)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# -----------------------------
# APP CONFIG
# -----------------------------
st.set_page_config(page_title="AI Resume Optimizer", layout="centered")
st.title("📄 AI Resume Optimizer (Stable Version)")


# -----------------------------
# INPUT
# -----------------------------
st.subheader("📥 Input Resume")

input_type = st.radio("Choose input type:", ["✍️ Text", "📄 PDF", "🖼️ Image"])

resume_text = ""


if input_type == "✍️ Text":
    resume_text = st.text_area("Enter Resume Text")

elif input_type == "📄 PDF":
    file = st.file_uploader("Upload PDF Resume", type=["pdf"])
    if file:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                resume_text += page.extract_text() or ""
        st.success("PDF extracted successfully")

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
# EXPANSIONS (ALL ABBREVIATIONS)
# -----------------------------
expansions = {
    # Branches
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

    # Degrees
    "btech": "Bachelor of Technology",
    "mtech": "Master of Technology",
    "be": "Bachelor of Engineering",

    # Tech terms
    "ml": "Machine Learning",
    "dl": "Deep Learning",
    "nlp": "Natural Language Processing",
    "cv": "Computer Vision",
    "ds": "Data Structures",
    "os": "Operating Systems",
    "dbms": "Database Management Systems",
    "sql": "Structured Query Language",
    "oops": "Object Oriented Programming System",
    "cn": "Computer Networks",

    # Languages
    "cpp": "C++",
    "py": "Python",
    "js": "JavaScript",

    # Academic
    "cgpa": "Cumulative Grade Point Average",
    "gpa": "Grade Point Average",

    "engg": "Engineering",
}


# -----------------------------
# SIMPLE GRAMMAR FIX (STABLE)
# -----------------------------
def fix_grammar(text):

    text = text.strip()

    # fix lowercase "i"
    text = re.sub(r'\bi\b', 'I', text)

    # basic contractions
    text = text.replace(" dont ", " do not ")
    text = text.replace(" didnt ", " did not ")
    text = text.replace(" cant ", " cannot ")

    # spacing cleanup
    text = re.sub(r'\s+', ' ', text)

    return text


# -----------------------------
# OPTIMIZATION ENGINE
# -----------------------------
def optimize_resume(text):

    # STEP 1: grammar fix
    text = fix_grammar(text)

    # STEP 2: expansions
    for k, v in expansions.items():
        text = re.sub(rf"\b{k}\b", v, text, flags=re.IGNORECASE)

    # STEP 3: sentence formatting
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip().capitalize() for s in sentences if s.strip()]
    text = ". ".join(sentences)

    return text


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
# RUN BUTTON
# -----------------------------
if resume_text and st.button("🚀 Optimize Resume"):

    optimized = optimize_resume(resume_text)

    # BEFORE vs AFTER
    st.subheader("📊 Before vs After")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ❌ Original")
        st.write(resume_text)

    with col2:
        st.markdown("### ✅ Optimized")
        st.write(optimized)


    # -------------------------
    # ATS SCORE
    # -------------------------
    keywords = [
        "python", "machine learning", "artificial intelligence",
        "data", "analysis", "project",
        "java", "c++", "computer science engineering",
        "sql"
    ]

    score = sum(12 for k in keywords if k in optimized.lower())
    score = min(score, 100)

    st.subheader("🎯 ATS Score")
    st.progress(score)
    st.write(f"Score: {score}/100")


    # -------------------------
    # PDF DOWNLOAD
    # -------------------------
    pdf_file = generate_pdf(optimized)

    st.download_button(
        "📥 Download Optimized Resume PDF",
        pdf_file,
        file_name="optimized_resume.pdf",
        mime="application/pdf"
    )
