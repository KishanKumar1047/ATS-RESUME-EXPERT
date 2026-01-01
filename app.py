# from dotenv import load_dotenv
# load_dotenv()

# import os
# import json
# import streamlit as st
# import google.generativeai as genai
# from PyPDF2 import PdfReader

# # ======================
# # CONFIG
# # ======================
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# model = genai.GenerativeModel("gemini-1.5-flash")

# # ======================
# # FUNCTIONS
# # ======================
# def get_gemini_response(input_prompt, text, jd):
#     response = model.generate_content(
#         input_prompt.format(text=text, jd=jd)
#     )
#     return response.text


# def extract_text_from_pdf(uploaded_file):
#     reader = PdfReader(uploaded_file)
#     text = ""
#     for page in reader.pages:
#         text += page.extract_text()
#     return text


# # ======================
# # PROMPT TEMPLATE
# # ======================
# input_prompt = """
# Hey Act Like a skilled or very experienced ATS (Application Tracking System)
# with a deep understanding of tech field, software engineering, data science,
# data analyst and big data engineer.

# Your task is to evaluate the resume based on the given job description.
# You must consider the job market is very competitive and you should provide
# best assistance for improving the resumes.

# Assign the percentage Matching based on JD and
# the missing keywords with high accuracy.

# resume: {text}
# description: {jd}

# Return ONLY valid JSON in this exact format:
# {{"JD Match":"%", "MissingKeywords":[], "Profile Summary":""}}
# """

# # ======================
# # STREAMLIT UI
# # ======================
# st.set_page_config(page_title="ATS Resume Expert", layout="centered")

# st.title("📄 ATS Resume Tracking System")
# st.subheader("Improve Your Resume Based on Job Description")

# jd = st.text_area("📌 Paste the Job Description")
# uploaded_file = st.file_uploader("📎 Upload Your Resume (PDF)", type=["pdf"])

# if st.button("🔍 Analyze Resume"):
#     if uploaded_file and jd.strip():
#         resume_text = extract_text_from_pdf(uploaded_file)
#         response = get_gemini_response(input_prompt, resume_text, jd)

#         try:
#             data = json.loads(response)

#             st.subheader("📊 ATS Analysis Result")

#             col1, col2 = st.columns(2)
#             with col1:
#                 st.metric("JD Match", data.get("JD Match", "N/A"))

#             with col2:
#                 st.metric("Missing Keywords", len(data.get("MissingKeywords", [])))

#             st.subheader("🧩 Missing Keywords")
#             if data.get("MissingKeywords"):
#                 for kw in data["MissingKeywords"]:
#                     st.write(f"- {kw}")
#             else:
#                 st.write("No critical keywords missing 🎉")

#             st.subheader("📝 Profile Summary")
#             st.write(data.get("Profile Summary", ""))

#         except Exception:
#             st.error("Model response was not valid JSON.")
#             st.write(response)

#     else:
#         st.warning("Please upload a resume and paste the job description.")

# from dotenv import load_dotenv
# load_dotenv()

import sys
st.write(sys.version)

import re
import json
import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# ======================
# CONFIG (Streamlit-only)
# ======================
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("GOOGLE_API_KEY is not set in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

@st.cache_resource
def load_model():
    return genai.GenerativeModel("gemini-1.5-flash")

model = load_model()

# ======================
# FUNCTIONS
# ======================
def get_gemini_response(prompt, resume_text, jd_text):
    response = model.generate_content(
        prompt.format(text=resume_text, jd=jd_text)
    )
    return response.text


@st.cache_data
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def calculate_resume_score(jd_match, missing_keywords):
    penalty = min(len(missing_keywords) * 2, 20)
    return max(jd_match - penalty, 0)


def parse_model_response(response_text):
    match = re.search(r"\{.*\}", response_text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in model response")
    return json.loads(match.group())


# ======================
# PROMPT TEMPLATE
# ======================
input_prompt = """
You are an expert ATS (Application Tracking System).

Evaluate the resume strictly against the job description.

Return ONLY valid JSON.
Do NOT use markdown.
Do NOT add explanations.

Exact JSON format:
{{
  "JD Match":"%",
  "MissingKeywords":[],
  "Profile Summary":""
}}

Resume:
{text}

Job Description:
{jd}
"""

# ======================
# STREAMLIT UI
# ======================
st.set_page_config(page_title="ATS Resume Scorer", layout="centered")

st.title("📄 ATS Resume Scoring System")
st.subheader("Score Your Resume Against Job Description")

jd = st.text_area("📌 Paste Job Description")
uploaded_file = st.file_uploader("📎 Upload Resume (PDF)", type=["pdf"])

if st.button("🔍 Analyze Resume"):
    if uploaded_file and jd.strip():
        resume_text = extract_text_from_pdf(uploaded_file)

        with st.spinner("Analyzing resume with ATS..."):
            response = get_gemini_response(input_prompt, resume_text, jd)

        try:
            data = parse_model_response(response)

            jd_match = int(data["JD Match"].replace("%", ""))
            missing_keywords = data.get("MissingKeywords", [])
            profile_summary = data.get("Profile Summary", "")

            resume_score = calculate_resume_score(jd_match, missing_keywords)

            st.subheader("📊 ATS Analysis Result")

            col1, col2, col3 = st.columns(3)
            col1.metric("JD Match", f"{jd_match}%")
            col2.metric("Resume Score", f"{resume_score}/100")
            col3.metric("Missing Keywords", len(missing_keywords))

            st.progress(resume_score / 100)

            st.subheader("🧩 Missing Keywords")
            if missing_keywords:
                for kw in missing_keywords:
                    st.write(f"- {kw}")
            else:
                st.success("No critical keywords missing 🎉")

            st.subheader("📝 Profile Summary")
            st.write(profile_summary)

        except Exception:
            st.error("❌ Unable to parse model response")
            st.text(response)

    else:
        st.warning("Please upload a resume and paste the job description.")
