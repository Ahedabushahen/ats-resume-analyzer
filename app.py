import os
import io
import streamlit as st
from google import genai
from google.genai import types

# --- Optional local .env support (won't crash if dotenv isn't installed on cloud) ---
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


# ----------------------------
# Config (Secrets first, then env)
# ----------------------------
API_KEY = None
if hasattr(st, "secrets"):
    API_KEY = st.secrets.get("GOOGLE_API_KEY", None)

if not API_KEY:
    API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("Missing GOOGLE_API_KEY. Add it in Streamlit Secrets or .env locally.")
    st.stop()

client = genai.Client(api_key=API_KEY)


# ----------------------------
# Gemini Helpers
# ----------------------------
def get_gemini_response(prompt: str, pdf_parts: list, job_description: str) -> str:
    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt, pdf_parts[0], job_description],
    )
    return resp.text


def input_pdf_setup(uploaded_file):
    """
    Cloud-safe PDF -> image conversion using PyMuPDF (no Poppler needed).
    """
    if uploaded_file is None:
        raise FileNotFoundError("No file uploaded")

    import fitz  # PyMuPDF

    pdf_bytes = uploaded_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    if doc.page_count == 0:
        raise ValueError("Empty PDF")

    page = doc.load_page(0)
    pix = page.get_pixmap(dpi=200)  # higher DPI helps quality
    img_bytes = pix.tobytes("jpeg")

    return [types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg")]


# ----------------------------
# Streamlit App
# ----------------------------
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

job_description = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage match")

input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of ATS functionality.
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
        st.warning("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, job_description)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.warning("Please upload the resume")
