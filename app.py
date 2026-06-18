import streamlit as st
import pdfplumber
from PIL import Image
import pytesseract
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import re

from groq import Groq


# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="AI Resume Writer", layout="centered")
st.title("🧠 REAL AI Resume Writer (ChatGPT-Level)")


# -----------------------------
# GROQ CLIENT
# -----------------------------
client = Groq(api_key=st.secrets.get("GROQ_API_KEY", "YOUR_API_KEY"))


# -----------------------------
# INPUT
# -----------------------------
st.subheader("📥 Input Resume")

input_type = st.radio("Choose input type:", ["✍️ Text", "📄 PDF", "🖼️ Image"])

resume_text = ""

if input_type == "✍️ Text":
    resume_text = st.text_area("Enter Resume Text")

elif input_type == "📄 PDF":
    file = st.file_uploader("Upload PDF", type=["pdf"])
    if file:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                resume_text += page.extract_text() or ""

elif input_type == "🖼️ Image":
    img = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    if img:
        image = Image.open(img)
        resume_text = pytesseract.image_to_string(image)


# -----------------------------
# AI RESUME WRITER
# -----------------------------
def ai_optimize_resume(text):

    prompt = f"""
You are an expert HR resume writer.

Rewrite the resume below into a PROFESSIONAL, ATS-optimized resume.

Rules:
- Fix all grammar mistakes
- Capitalize names properly
- Expand abbreviations (CSE → Computer Science Engineering, ML → Machine Learning)
- Improve sentence structure
- Make it sound professional
- Keep meaning same
- Do NOT add fake experience
- Format in clean paragraphs or bullet points

Resume:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a professional resume writer."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# -----------------------------
# ATS SCORE (AI OUTPUT BASED)
# -----------------------------
def calculate_ats(text):

    text = text.lower()

    keywords = [
        "python", "machine learning", "data", "sql",
        "engineering", "project", "analysis",
        "computer science"
    ]

    score = sum(100 // len(keywords) for k in keywords if k in text)
    return min(score, 100)


# -----------------------------
# PDF
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
        p.drawString(40, y, line[:100])
        y -= 15

    p.save()
    buffer.seek(0)
    return buffer


# -----------------------------
# RUN
# -----------------------------
if resume_text and st.button("🚀 Generate Professional Resume"):

    optimized = ai_optimize_resume(resume_text)

    st.subheader("📊 Before vs After")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ❌ Original")
        st.write(resume_text)

    with col2:
        st.markdown("### ✅ AI Optimized")
        st.write(optimized)


    score = calculate_ats(optimized)

    st.subheader("🎯 ATS Score")
    st.progress(score)
    st.write(f"Score: {score}/100")


    pdf = generate_pdf(optimized)

    st.download_button(
        "📥 Download Resume PDF",
        pdf,
        file_name="AI_Resume.pdf",
        mime="application/pdf"
    )
