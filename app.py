import streamlit as st
import re
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import pdfplumber
from PIL import Image
import pytesseract

# OPTIONAL (Windows path fix)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# -----------------------------
# APP CONFIG
# -----------------------------
st.set_page_config(page_title="AI Resume Optimizer", layout="centered")
st.title("📄 AI Resume Optimizer (Final Clean Version)")


# -----------------------------
# INPUT TYPE
# -----------------------------
st.subheader("📥 Input Resume")

input_type = st.radio(
    "Choose input type:",
    ["✍️ Text", "📄 PDF", "🖼️ Image"]
)

resume_text = ""


# -----------------------------
# TEXT INPUT
# -----------------------------
if input_type == "✍️ Text":
    resume_text = st.text_area("Enter Resume Text")


# -----------------------------
# PDF INPUT
# -----------------------------
elif input_type == "📄 PDF":
    file = st.file_uploader("Upload PDF Resume", type=["pdf"])

    if file:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                resume_text += page.extract_text() or ""
        st.success("PDF extracted successfully")


# -----------------------------
# IMAGE INPUT
# -----------------------------
elif input_type == "🖼️ Image":
    img_file = st.file_uploader("Upload Image Resume", type=["png", "jpg", "jpeg"])

    if img_file:
        img = Image.open(img_file)
        resume_text = pytesseract.image_to_string(img)
        st.success("Image text extracted successfully")


# -----------------------------
# SHOW RAW TEXT
# -----------------------------
if resume_text:
    st.subheader("📄 Extracted Resume")
    st.write(resume_text)


# -----------------------------
# STRONG GRAMMAR + EXPANSION ENGINE
# -----------------------------
def optimize_resume(text):

    text = text.strip()

    # FIX standalone "i"
    text = re.sub(r'\bi\b', 'I', text)

    # -----------------------------
    # FULL EXPANSIONS + FIXES
    # -----------------------------
    fixes = {
        "cse": "Computer Science Engineering",
        "c.s.e": "Computer Science Engineering",
        "cs": "Computer Science",
        "ml": "Machine Learning",
        "ai": "Artificial Intelligence",
        "i am": "I am",
        "i have": "I have",
        "i know": "I have knowledge of",
        "dont": "do not",
        "didnt": "did not",
        "engg": "Engineering",
        "btech": "Bachelor of Technology",
        "little bit": "basic knowledge of",
        "some college": "a college",
        "c++": "C++",
        "java": "Java",
        "sql": "SQL"
    }

    for k, v in fixes.items():
        text = text.replace(k, v)

    # Sentence formatting
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
    width, height = letter

    y = height - 40
    p.setFont("Helvetica", 10)

    for line in text.split("\n"):
        if y < 40:
            p.showPage()
            p.setFont("Helvetica", 10)
            y = height - 40

        p.drawString(40, y, line[:100])
        y -= 15

    p.save()
    buffer.seek(0)
    return buffer


# -----------------------------
# MAIN ACTION
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
        "sql", "data", "analysis", "project",
        "java", "c++", "computer science engineering"
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
        "📥 Download Optimized Resume (PDF)",
        pdf_file,
        file_name="optimized_resume.pdf",
        mime="application/pdf"
    )
