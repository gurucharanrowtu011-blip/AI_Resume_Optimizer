import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import pdfplumber
from PIL import Image
import pytesseract

# OPTIONAL: set path if needed
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# -----------------------------
# APP CONFIG
# -----------------------------
st.set_page_config(page_title="AI Resume Optimizer", layout="centered")
st.title("📄 AI Resume Optimizer (Full Offline System)")


# -----------------------------
# INPUT METHOD
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
    file = st.file_uploader("Upload PDF", type=["pdf"])

    if file:
        with pdfplumber.open(file) as pdf:
            resume_text = ""
            for page in pdf.pages:
                resume_text += page.extract_text() or ""
        st.success("PDF extracted successfully")


# -----------------------------
# IMAGE INPUT (OCR)
# -----------------------------
elif input_type == "🖼️ Image":
    img_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    if img_file:
        img = Image.open(img_file)
        resume_text = pytesseract.image_to_string(img)
        st.success("Image text extracted successfully")


# -----------------------------
# SHOW EXTRACTED TEXT
# -----------------------------
if resume_text:
    st.subheader("📄 Original Resume")
    st.write(resume_text)


# -----------------------------
# SIMPLE OFFLINE AI ENGINE
# -----------------------------
def optimize_resume(text):

    fixes = {
        " i ": " I ",
        " im ": " I am ",
        " dont ": " do not ",
        " didnt ": " did not ",
        " little bit": "basic knowledge of",
        " some college": "a college",
        " engg": "Engineering",
        " ml ": " Machine Learning ",
    }

    output = text

    for k, v in fixes.items():
        output = output.replace(k, v)

    sentences = output.split(".")
    sentences = [s.strip().capitalize() for s in sentences if s.strip()]
    output = ". ".join(sentences) + "."

    return output


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
# RUN OPTIMIZATION
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
        "python", "machine learning", "sql",
        "data", "analysis", "project",
        "java", "c++", "engineering"
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
