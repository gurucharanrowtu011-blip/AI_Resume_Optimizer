import streamlit as st
import re
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pdfplumber
from PIL import Image
import pytesseract
import language_tool_python

# -----------------------------
# APP CONFIG
# -----------------------------
st.set_page_config(page_title="AI Resume Optimizer", layout="centered")
st.title("📄 AI Resume Optimizer")

# Initialize LanguageTool (cached to avoid reloading)
@st.cache_resource
def load_language_tool():
    return language_tool_python.LanguageTool('en-US')

tool = load_language_tool()

# -----------------------------
# INPUT
# -----------------------------
st.subheader("📥 Input Resume")
input_type = st.radio("Choose input type:", ["✍️ Text", "📄 PDF", "🖼️ Image"])
resume_text = ""

if input_type == "✍️ Text":
    resume_text = st.text_area("Enter Resume Text", height=300)

elif input_type == "📄 PDF":
    file = st.file_uploader("Upload PDF Resume", type=["pdf"])
    if file:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                resume_text += (page.extract_text() or "") + "\n"
        st.success("PDF extracted successfully")

elif input_type == "🖼️ Image":
    img_file = st.file_uploader("Upload Image Resume", type=["png", "jpg", "jpeg"])
    if img_file:
        img = Image.open(img_file)
        resume_text = pytesseract.image_to_string(img)
        st.success("Image extracted successfully")

if resume_text:
    st.subheader("📄 Extracted Resume")
    st.text_area("Original Text", resume_text, height=200, disabled=True)

# -----------------------------
# COMPREHENSIVE EXPANSIONS
# -----------------------------
expansions = {
    # Degrees
    "btech": "Bachelor of Technology",
    "b.tech": "Bachelor of Technology",
    "mtech": "Master of Technology",
    "m.tech": "Master of Technology",
    "be": "Bachelor of Engineering",
    "b.e": "Bachelor of Engineering",
    "me": "Master of Engineering",
    "m.e": "Master of Engineering",
    "bsc": "Bachelor of Science",
    "b.sc": "Bachelor of Science",
    "msc": "Master of Science",
    "m.sc": "Master of Science",
    "bca": "Bachelor of Computer Applications",
    "mca": "Master of Computer Applications",
    "bba": "Bachelor of Business Administration",
    "mba": "Master of Business Administration",
    "phd": "Doctor of Philosophy",
    "pg": "Post Graduate",
    "ug": "Under Graduate",
    
    # Branches
    "cse": "Computer Science and Engineering",
    "cs": "Computer Science",
    "it": "Information Technology",
    "ece": "Electronics and Communication Engineering",
    "eee": "Electrical and Electronics Engineering",
    "ee": "Electrical Engineering",
    "mech": "Mechanical Engineering",
    "civil": "Civil Engineering",
    "aiml": "Artificial Intelligence and Machine Learning",
    "ai": "Artificial Intelligence",
    "ds": "Data Science",
    "iot": "Internet of Things",
    
    # Technical terms
    "ml": "Machine Learning",
    "dl": "Deep Learning",
    "nlp": "Natural Language Processing",
    "cv": "Computer Vision",
    "os": "Operating Systems",
    "dbms": "Database Management Systems",
    "rdbms": "Relational Database Management Systems",
    "sql": "Structured Query Language",
    "nosql": "Not Only SQL",
    "oops": "Object-Oriented Programming",
    "oop": "Object-Oriented Programming",
    "cn": "Computer Networks",
    "dsa": "Data Structures and Algorithms",
    "api": "Application Programming Interface",
    "apis": "Application Programming Interfaces",
    "ui": "User Interface",
    "ux": "User Experience",
    "gui": "Graphical User Interface",
    "cli": "Command Line Interface",
    "ide": "Integrated Development Environment",
    "sdk": "Software Development Kit",
    "ci": "Continuous Integration",
    "cd": "Continuous Deployment",
    "devops": "Development Operations",
    "aws": "Amazon Web Services",
    "gcp": "Google Cloud Platform",
    "saas": "Software as a Service",
    "paas": "Platform as a Service",
    "iaas": "Infrastructure as a Service",
    "vm": "Virtual Machine",
    "vms": "Virtual Machines",
    "html": "HyperText Markup Language",
    "css": "Cascading Style Sheets",
    "js": "JavaScript",
    "ts": "TypeScript",
    "cpp": "C++",
    "py": "Python",
    
    # Academic
    "cgpa": "Cumulative Grade Point Average",
    "gpa": "Grade Point Average",
    "hsc": "Higher Secondary Certificate",
    "ssc": "Secondary School Certificate",
    "cbse": "Central Board of Secondary Education",
    "icse": "Indian Certificate of Secondary Education",
    
    # Professional
    "hr": "Human Resources",
    "ceo": "Chief Executive Officer",
    "cto": "Chief Technology Officer",
    "cfo": "Chief Financial Officer",
    "pm": "Project Manager",
    "sde": "Software Development Engineer",
    "swe": "Software Engineer",
    "qa": "Quality Assurance",
    "poc": "Proof of Concept",
    "mvp": "Minimum Viable Product",
    "kpi": "Key Performance Indicator",
    "roi": "Return on Investment",
    
    # General
    "engg": "Engineering",
    "eng": "Engineering",
    "govt": "Government",
    "pvt": "Private",
    "ltd": "Limited",
    "dept": "Department",
    "mgmt": "Management",
    "yr": "year",
    "yrs": "years",
    "no": "number",
    "nos": "numbers",
    "info": "information",
    "tech": "technology",
    "exp": "experience",
    "resp": "responsibilities",
    "req": "requirements",
    "approx": "approximately",
    "etc": "et cetera",
    "eg": "for example",
    "ie": "that is",
    "vs": "versus",
    "w": "with",
    "wo": "without",
    "b/w": "between",
    "thru": "through",
    "govt": "government",
}

# -----------------------------
# EXPAND ABBREVIATIONS
# -----------------------------
def expand_abbreviations(text):
    """Expand common abbreviations to full forms."""
    # Sort by length (longest first) to avoid partial replacements
    sorted_expansions = sorted(expansions.items(), key=lambda x: len(x[0]), reverse=True)
    
    for abbr, full in sorted_expansions:
        # Word boundary matching, case insensitive
        pattern = rf'\b{re.escape(abbr)}\b'
        text = re.sub(pattern, full, text, flags=re.IGNORECASE)
    
    return text

# -----------------------------
# FIX GRAMMAR WITH LANGUAGETOOL
# -----------------------------
def fix_grammar_advanced(text):
    """Use LanguageTool for comprehensive grammar correction."""
    # Get matches (errors)
    matches = tool.check(text)
    
    # Apply corrections
    corrected = language_tool_python.utils.correct(text, matches)
    
    return corrected

# -----------------------------
# CLEAN AND FORMAT TEXT
# -----------------------------
def clean_and_format(text):
    """Clean up formatting issues."""
    # Fix multiple spaces
    text = re.sub(r' +', ' ', text)
    
    # Fix spacing around punctuation
    text = re.sub(r'\s+([.,;:!?])', r'\1', text)
    text = re.sub(r'([.,;:!?])([A-Za-z])', r'\1 \2', text)
    
    # Fix multiple newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Capitalize after periods
    def capitalize_after_period(match):
        return match.group(1) + match.group(2).upper()
    
    text = re.sub(r'([.!?]\s+)([a-z])', capitalize_after_period, text)
    
    # Capitalize first letter of text
    if text:
        text = text[0].upper() + text[1:]
    
    # Fix common issues
    text = re.sub(r'\bi\b', 'I', text)  # Capitalize standalone "i"
    
    return text.strip()

# -----------------------------
# MAIN OPTIMIZER
# -----------------------------
def optimize_resume(text):
    """Full optimization pipeline."""
    # Step 1: Clean initial formatting
    text = clean_and_format(text)
    
    # Step 2: Expand abbreviations
    text = expand_abbreviations(text)
    
    # Step 3: Fix grammar with LanguageTool
    text = fix_grammar_advanced(text)
    
    # Step 4: Final cleanup
    text = clean_and_format(text)
    
    return text

# -----------------------------
# ATS SCORE CALCULATOR
# -----------------------------
def calculate_ats(text):
    """Calculate ATS compatibility score."""
    text_lower = text.lower()
    
    keywords = {
        # Technical skills
        "python": 8, "java": 7, "javascript": 7, "c++": 6, "sql": 7,
        "machine learning": 10, "artificial intelligence": 10,
        "data science": 10, "deep learning": 9, "natural language processing": 8,
        "computer vision": 8, "data structures": 7, "algorithms": 7,
        "database": 6, "cloud": 6, "aws": 7, "docker": 6, "kubernetes": 6,
        "git": 5, "linux": 5, "api": 5, "rest": 5,
        
        # Soft skills
        "leadership": 6, "communication": 6, "teamwork": 5, "problem solving": 7,
        "analytical": 5, "critical thinking": 5,
        
        # Experience indicators
        "project": 5, "internship": 6, "experience": 5, "developed": 5,
        "implemented": 5, "designed": 5, "managed": 5, "led": 5,
        "achieved": 5, "improved": 5, "created": 5,
        
        # Education
        "bachelor": 5, "master": 6, "degree": 4, "engineering": 5,
        "computer science": 8, "certification": 5,
    }
    
    score = 0
    matched_keywords = []
    
    for keyword, points in keywords.items():
        if keyword in text_lower:
            score += points
            matched_keywords.append(keyword)
    
    # Length bonus
    word_count = len(text.split())
    if word_count > 100:
        score += 5
    if word_count > 200:
        score += 5
    if word_count > 300:
        score += 5
    
    # Section detection bonus
    sections = ["education", "experience", "skills", "projects", "achievements"]
    for section in sections:
        if section in text_lower:
            score += 3
    
    return min(score, 100), matched_keywords

# -----------------------------
# PDF GENERATOR
# -----------------------------
def generate_pdf(text):
    """Generate PDF from text."""
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    y = height - 50
    margin = 50
    line_height = 14
    
    p.setFont("Helvetica", 11)
    
    lines = text.split('\n')
    for line in lines:
        # Wrap long lines
        words = line.split()
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if p.stringWidth(test_line, "Helvetica", 11) < (width - 2 * margin):
                current_line = test_line
            else:
                if y < 50:
                    p.showPage()
                    y = height - 50
                    p.setFont("Helvetica", 11)
                p.drawString(margin, y, current_line)
                y -= line_height
                current_line = word
        
        if current_line:
            if y < 50:
                p.showPage()
                y = height - 50
                p.setFont("Helvetica", 11)
            p.drawString(margin, y, current_line)
            y -= line_height
        
        # Extra space for empty lines (paragraph breaks)
        if not line.strip():
            y -= line_height // 2
    
    p.save()
    buffer.seek(0)
    return buffer

# -----------------------------
# RUN OPTIMIZATION
# -----------------------------
if resume_text and st.button("🚀 Optimize Resume"):
    with st.spinner("Optimizing your resume..."):
        optimized = optimize_resume(resume_text)
    
    st.subheader("📊 Before vs After")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ❌ Original")
        st.text_area("Original", resume_text, height=400, disabled=True, label_visibility="collapsed")
    
    with col2:
        st.markdown("### ✅ Optimized")
        st.text_area("Optimized", optimized, height=400, disabled=True, label_visibility="collapsed")
    
    # ATS Score
    score, matched = calculate_ats(optimized)
    
    st.subheader("🎯 ATS Score")
    st.progress(score / 100)
    st.write(f"**Score: {score}/100**")
    
    if matched:
        st.write("**Keywords detected:** " + ", ".join(matched[:15]))
    
    # PDF Download
    pdf_file = generate_pdf(optimized)
    
    st.download_button(
        "📥 Download Optimized Resume (PDF)",
        pdf_file,
        file_name="optimized_resume.pdf",
        mime="application/pdf"
    )
