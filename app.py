import streamlit as st

st.title("📄 Offline AI Resume Optimizer (GenAI + Prompt Engineering)")

resume_text = st.text_area("Enter your Resume Text")

option = st.selectbox(
    "Choose Optimization Type",
    ["Basic Improvement", "ATS Optimization", "Role Based Optimization"]
)

role = ""
if option == "Role Based Optimization":
    role = st.text_input("Enter Job Role (e.g. Data Analyst, ML Engineer)")


# ----------------------------
# SIMPLE ATS SCORE FUNCTION
# ----------------------------
def calculate_ats_score(text):
    keywords = [
        "python", "machine learning", "sql",
        "data", "project", "analysis",
        "java", "c++"
    ]

    score = 0
    for k in keywords:
        if k in text.lower():
            score += 12

    return min(score, 100)


# ----------------------------
# OFFLINE RESUME IMPROVER
# ----------------------------
def improve_resume(text, mode, role=""):

    text = text.strip()

    improved = text

    # Basic cleaning improvements
    improved = improved.replace("i ", "I ")
    improved = improved.replace(" ml ", " Machine Learning ")
    improved = improved.replace(" sql ", " SQL ")
    improved = improved.replace(" python", " Python")

    if mode == "ATS Optimization":
        improved = """
• Strong understanding of Python and Machine Learning  
• Experience in SQL database handling  
• Knowledge of Data Analysis and Data Preprocessing  
• Worked on academic projects including prediction systems  
• Familiar with C++ and Java programming fundamentals  
""" + improved

    elif mode == "Role Based Optimization":
        improved = f"""
• Resume optimized for role: {role}

• Strong technical foundation in Python, ML, and Data Science  
• Experience building academic projects and models  
• Good understanding of problem solving and analysis  
""" + improved

    else:
        improved = """
• Improved Professional Resume  
• Strong technical skills in programming and data science  
• Experience in academic ML projects  
""" + improved

    return improved


# ----------------------------
# UI LOGIC
# ----------------------------
if st.button("Optimize Resume"):

    if resume_text.strip() == "":
        st.warning("Please enter resume text")
    else:

        result = improve_resume(resume_text, option, role)

        st.subheader("📊 Before vs After")

        col1, col2 = st.columns(2)

        with col1:
            st.write("### Original Resume")
            st.write(resume_text)

        with col2:
            st.write("### Optimized Resume")
            st.write(result)

        score = calculate_ats_score(result)

        st.subheader("🎯 ATS Score")
        st.progress(score)
        st.write(f"Score: {score}/100")

        st.subheader("📄 Final Output")
        st.write(result)
