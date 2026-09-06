import streamlit as st
import google.generativeai as genai
import pypdf
from fpdf import FPDF
import io

# Page Configuration
st.set_page_config(page_title="AI Resume Assistant", page_icon="📄", layout="wide")

st.title("📄 AI Resume Assistant & ATS Analyzer")
st.write("Upload your resume and analyze it against job descriptions or get AI-powered improvements.")

# Gemini API Key Input
api_key = st.sidebar.text_input("Enter Google Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.sidebar.warning("Please enter your Gemini API Key to proceed.")

# File Upload Section
uploaded_file = st.file_uploader("Upload your Resume (PDF or TXT)", type=["pdf", "txt"])

resume_text = ""
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        pdf_reader = pypdf.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            resume_text += page.extract_text() or ""
    else:
        resume_text = uploaded_file.read().decode("utf-8")
    
    st.success("Resume uploaded successfully!")

# Text input for manual resume or Job Description
job_description = st.text_area("Paste Job Description (Optional for ATS match):", height=150)

# Action Buttons
col1, col2 = st.columns(2)

with col1:
    analyze_btn = st.button("🔍 Analyze Resume (ATS Match)")

with col2:
    improve_btn = st.button("✨ Generate Improved Resume")

if analyze_btn:
    if not api_key:
        st.error("Please enter a valid Gemini API Key in the sidebar.")
    elif not resume_text:
        st.error("Please upload a resume first.")
    else:
        with st.spinner("Analyzing resume..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"""
                You are an expert ATS (Applicant Tracking System) scanner. 
                Analyze the following resume against the job description (if provided).
                Provide:
                1. ATS Match Percentage (Estimate)
                2. Key Missing Keywords
                3. Detailed Strengths & Weaknesses
                4. Formatting & Actionable Suggestions
                
                Resume:
                {resume_text}
                
                Job Description:
                {job_description if job_description else 'N/A'}
                """
                response = model.generate_content(prompt)
                st.subheader("📊 Analysis Results")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error during API call: {e}")

if improve_btn:
    if not api_key:
        st.error("Please enter a valid Gemini API Key in the sidebar.")
    elif not resume_text:
        st.error("Please upload a resume first.")
    else:
        with st.spinner("Rewriting & improving resume..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"""
                You are a professional resume writer. Rewrite and improve the following resume to make it professional, ATS-friendly, and impact-driven using strong action verbs.
                
                Resume:
                {resume_text}
                """
                response = model.generate_content(prompt)
                improved_text = response.text
                
                st.subheader("📝 Improved Resume")
                st.write(improved_text)
                
                # Download Options
                st.download_button(
                    label="📥 Download as TXT",
                    data=improved_text,
                    file_name="improved_resume.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Error during API call: {e}")
