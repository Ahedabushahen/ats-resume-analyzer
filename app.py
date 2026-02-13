from dotenv import load_dotenv
load_dotenv()

import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image

# ✅ New Gemini SDK (replace deprecated google-generativeai)
from google import genai
from google.genai import types

# ----------------------------
# Config
# ----------------------------
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY. Put it in a .env file: GOOGLE_API_KEY=xxxx")

client = genai.Client(api_key=API_KEY)

# ✅ Your Poppler path (Windows)
POPPLER_PATH = r"C:\Program Files (x86)\Release-25.12.0-0\poppler-25.12.0\Library\bin"


# ----------------------------
# Gemini Helpers
# ----------------------------
def get_gemini_response(prompt, pdf_parts, job_description):
    """
    prompt: instructions (HR / ATS prompt)
    pdf_parts: list[types.Part] with the resume image
    job_description: text area content
    """
    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt, pdf_parts[0], job_description],
    )
    return resp.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is None:
        raise FileNotFoundError("No file uploaded")

    # Convert the PDF -> images (requires Poppler on Windows)
    images = pdf2image.convert_from_bytes(
        uploaded_file.read(),
        poppler_path=POPPLER_PATH
    )

    first_page = images[0]

    # Convert image to bytes
    buf = io.BytesIO()
    first_page.save(buf, format="JPEG")
    image_bytes = buf.getvalue()

    # Create Gemini Part from bytes (image input)
    pdf_parts = [types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")]
    return pdf_parts


# ----------------------------
# Streamlit App
# ----------------------------
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

job_description = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage match")

input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality.
Evaluate the resume against the provided job description.
Give the percentage match first, then missing keywords, and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, job_description)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, job_description)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
