import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

load_dotenv()  # Load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text


# Prompt Template
input_prompt = """
Hey! Act like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of the tech field, software engineering, data science, data analysis,
and big data engineering. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive, and you should provide
the best assistance for improving the resumes. Assign the percentage matching based
on JD and
the missing keywords with high accuracy.
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords":[],"Profile Summary":""}}
"""

# Streamlit app
st.title("Smart Resume ATS")
st.markdown(
    """
    <style>
        body {
            background-color: #F2F2F2;
        }
        .big-font {
            font-size: 24px !important;
            color: white;
        }
        .highlight {
            color: #FF6347;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="big-font">
        <p>Improve Your Resume ATS</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Job Description input
jd = st.text_area("Paste the Job Description")

# Resume file uploader
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

# Submit button
submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        # Process uploaded PDF
        st.info("Processing your resume... Please wait.")
        text = input_pdf_text(uploaded_file)

        # Generate response
        st.info("Analyzing your resume... Please wait.")
        response = get_gemini_response(input_prompt.format(text=text, jd=jd))

        # Display result
        st.subheader("Resume Analysis Result:")
        st.json(response)



