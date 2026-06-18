import streamlit as st
import requests
from prompts import RESUME_IMPROVER_PROMPT, ATS_OPTIMIZER_PROMPT, 
from dotenv import load_dotenv
load_dotenv()
ROLE_BASED_PROMPT

# ⚠️ BEST PRACTICE: store in environment variable later
import os
HF_API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

st.title("📄 AI Resume Optimizer (Free GenAI + Prompt Engineering)")

resume_text = st.text_area("Enter your Resume Text")

option = st.selectbox(
    "Choose Optimization Type",
    ["Basic Improvement", "ATS Optimization", "Role Based Optimization"]
)

role = ""
if option == "Role Based Optimization":
    role = st.text_input("Enter Job Role (e.g. Data Analyst, ML Engineer)")


def get_ai_response(prompt):
    payload = {"inputs": prompt}

    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()

    # Handle HuggingFace response formats
    if isinstance(result, list) and "generated_text" in result[0]:
        return result[0]["generated_text"]
    elif isinstance(result, dict) and "error" in result:
        return f"Error: {result['error']}"
    else:
        return str(result)


if st.button("Optimize Resume"):

    if resume_text.strip() == "":
        st.warning("Please enter resume text")
    else:

        if option == "Basic Improvement":
            prompt = RESUME_IMPROVER_PROMPT.format(text=resume_text)

        elif option == "ATS Optimization":
            prompt = ATS_OPTIMIZER_PROMPT.format(text=resume_text)

        else:
            prompt = ROLE_BASED_PROMPT.format(text=resume_text, role=role)

        st.subheader("📌 Generated Prompt")
        st.code(prompt)

        with st.spinner("Generating AI response..."):
            result = get_ai_response(prompt)

        st.subheader("📄 Final Optimized Resume")
        st.write(result)