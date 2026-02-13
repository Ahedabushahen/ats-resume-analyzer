<div align="center">

# AI ATS Resume Analyzer  
### Built by **Shahen-Tech House** 🚀

AI-powered resume analyzer that **simulates ATS screening** by comparing a resume PDF to a job description and generating:
**match score**, **missing keywords**, and **actionable feedback**.

[🌐 Live Demo](https://ai-ats-resume-analyzer-by-shahen-tech.streamlit.app) •
[💻 GitHub Repo](https://github.com/Ahedabushahen/AI-ATS-Resume-Analyzer)

</div>

---

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Gemini](https://img.shields.io/badge/Google-Gemini-black)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

## ✨ Features

- 📄 Upload a **PDF resume**
- 📝 Paste a **job description**
- 🧠 AI generates **HR-style evaluation**
- 📊 **ATS match percentage**
- 🔎 **Missing keywords** + improvement notes
- 🌍 Deployed as a **live web app**

---

## 🖼️ Demo

> Add screenshots to `assets/` and update paths below.

<div align="center">

**Home**
<br/>
<img src="assets/demo-home.png" width="800" />

<br/><br/>

**Results**
<br/>
<img src="assets/demo-result.png" width="800" />

</div>

<!-- Optional GIF -->
<!--
<div align="center">
  <img src="assets/demo.gif" width="800" />
</div>
-->

---

## 🧠 How it works

1. Upload resume (PDF)
2. The app renders the first page of the PDF into an image (cloud-safe)
3. Gemini (multimodal) compares resume + job description
4. Output includes:
   - Match %
   - Missing keywords
   - Final thoughts & improvement suggestions

---

## 🧰 Tech Stack

- **Python**
- **Streamlit**
- **Google Gemini API** (multimodal)
- **PyMuPDF** (PDF → image)
- **python-dotenv** (local env)

---

## 🚀 Run locally

### 1) Clone & install
```bash
git clone https://github.com/Ahedabushahen/AI-ATS-Resume-Analyzer.git
cd AI-ATS-Resume-Analyzer
pip install -r requirements.txt
