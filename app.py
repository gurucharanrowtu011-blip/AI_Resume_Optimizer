import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import pdfplumber
from PIL import Image
import pytesseract

from prompts import RESUME_IMPROVER_PROMPT

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="AI Resume Optimizer", layout="centered")
st.title("📄 AI Resume Optimizer (Upload + Text + PDF Export)")

# -----------------------------
# INPUT METHODS
# -----------------------------
st.subheader("📥 Input Your Resume")

input_type = st.radio(
    "Choose input type:",
    ["✍️ Type Text", "📄 Upload PDF", "🖼️ Upload Image"]
)

resume_text = ""

# -----------------------------
# TEXT INPUT
# -----------------------------
if input_type == "✍️ Type Text":
    resume_text = st.text_area("Enter Resume Text")

# -----------------------------
# PDF INPUT
# -----------------------------
elif input_type == "📄 Upload PDF":
    pdf_file = st.file_uploader("Upload PDF Resume", type=["pdf"])

    if pdf_file:
        with pdfplumber.open(pdf_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        resume_text = text
        st.success("PDF text extracted successfully!")

# -----------------------------
# IMAGE INPUT (OCR)
# -----------------------------
elif input_type == "🖼️ Upload Image":
    image_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    if image_file:
        img = Image.open(image_file)
        resume_text = pytesseract.image_to_string(img)
        st.success("Image text extracted successfully!")

# -----------------------------
# SHOW EXTRACTED TEXT
# -----------------------------
if resume_text:
    st.subheader("📄 Extracted Resume Text")
    st.write(resume_text)

# -----------------------------
# OPTIMIZER ENGINE (OFFLINE)
# -----------------------------
def fake_ai_engine(text):

    fixes = {
        " i ": " I ",
        " im ": " I am ",
        " dont ": " do not ",
        " didnt ": " did not ",
        " little bit": "basic knowledge of",
        " some college": "a college",
       
