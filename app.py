import os
import re
from pathlib import Path

import pdfplumber
import streamlit as st
from docx import Document
from dotenv import load_dotenv
from google import genai
from pptx import Presentation

load_dotenv()

st.set_page_config(
    page_title="EduMentor AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #F8FAFC 0%, #EEF2FF 45%, #ECFDF5 100%);
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1300px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
}

[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}

.hero-title {
    color: #0F172A;
    font-size: 58px;
    font-weight: 850;
    line-height: 1.08;
    margin-bottom: 16px;
}

.hero-subtitle {
    color: #334155;
    font-size: 21px;
    line-height: 1.6;
    max-width: 900px;
    margin-bottom: 32px;
}

.section-title {
    color: #0F172A;
    font-size: 34px;
    font-weight: 800;
    margin-top: 36px;
    margin-bottom: 20px;
}

.premium-card {
    background: rgba(255,255,255,0.92);
    border: 1px solid rgba(15,23,42,0.08);
    border-radius: 24px;
    padding: 28px;
    min-height: 170px;
    box-shadow: 0 18px 45px rgba(15,23,42,0.08);
}

.card-title {
    color: #0F172A;
    font-size: 23px;
    font-weight: 800;
    margin-bottom: 12px;
}

.card-text {
    color: #475569;
    font-size: 16px;
    line-height: 1.7;
}

.upload-card {
    background: #FFFFFF;
    border: 2px dashed rgba(16,185,129,0.45);
    border-radius: 26px;
    padding: 32px;
    margin-bottom: 22px;
    box-shadow: 0 16px 40px rgba(15,23,42,0.08);
}

.upload-title {
    color: #0F172A;
    font-size: 26px;
    font-weight: 800;
    margin-bottom: 10px;
}

.upload-text {
    color: #475569;
    font-size: 17px;
    line-height: 1.6;
}

.upload-info {
    background: rgba(16,185,129,0.10);
    border: 1px solid rgba(16,185,129,0.35);
    border-radius: 20px;
    padding: 24px;
    margin-top: 20px;
}

.preview-box {
    background: #FFFFFF;
    border: 1px solid rgba(15,23,42,0.10);
    border-radius: 20px;
    padding: 24px;
    max-height: 420px;
    overflow-y: auto;
    box-shadow: 0 14px 35px rgba(15,23,42,0.08);
    color: #0F172A;
    white-space: pre-wrap;
    line-height: 1.7;
}

.ai-output {
    background: #FFFFFF;
    border-left: 6px solid #10B981;
    border-radius: 20px;
    padding: 28px;
    box-shadow: 0 14px 35px rgba(15,23,42,0.08);
    color: #0F172A;
    line-height: 1.8;
}

.ai-output h1, .ai-output h2, .ai-output h3 {
    color: #0F172A;
}

.ai-output p, .ai-output li {
    color: #334155;
    font-size: 17px;
}

[data-testid="stAlert"] {
    border-radius: 16px;
    border: 1px solid rgba(16,185,129,0.35);
}

[data-testid="stAlert"] * {
    color: #0F172A !important;
}

.stButton > button {
    background: linear-gradient(135deg, #2563EB, #10B981);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 0.75rem 1.3rem;
    font-weight: 700;
}

[data-testid="stFileUploader"] {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 10px;
    border: 1px solid rgba(15,23,42,0.08);
}

header {
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

UPLOAD_FOLDER = Path("data/uploads")


def get_unique_file_path(file_name):
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
    original_path = UPLOAD_FOLDER / file_name

    if not original_path.exists():
        return original_path

    file_stem = original_path.stem
    file_suffix = original_path.suffix
    counter = 1

    while True:
        new_file_name = f"{file_stem}_{counter}{file_suffix}"
        new_file_path = UPLOAD_FOLDER / new_file_name

        if not new_file_path.exists():
            return new_file_path

        counter += 1


def save_uploaded_file(uploaded_file):
    file_path = get_unique_file_path(uploaded_file.name)

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return file_path


def clean_text(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = "\n".join(line.strip() for line in text.split("\n"))
    return text.strip()


def extract_text_from_pdf(file_path):
    extracted_text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if text:
                extracted_text += text + "\n\n"

    return extracted_text.strip()


def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        return file.read().strip()


def extract_text_from_docx(file_path):
    document = Document(file_path)
    extracted_text = ""

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            extracted_text += paragraph.text + "\n\n"

    return extracted_text.strip()


def extract_text_from_pptx(file_path):
    presentation = Presentation(file_path)
    extracted_text = ""

    for slide_number, slide in enumerate(presentation.slides, start=1):
        slide_text = ""

        for shape in slide.shapes:
            if hasattr(shape, "text") and shape.text.strip():
                slide_text += shape.text + "\n"

        if slide_text.strip():
            extracted_text += f"Slide {slide_number}:\n{slide_text}\n\n"

    return extracted_text.strip()


def process_document(file_path):
    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif suffix == ".txt":
        text = extract_text_from_txt(file_path)
    elif suffix == ".docx":
        text = extract_text_from_docx(file_path)
    elif suffix == ".pptx":
        text = extract_text_from_pptx(file_path)
    else:
        text = ""

    return clean_text(text)


def generate_ai_explanation(text):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "❌ Gemini API key not found. Please add GEMINI_API_KEY to your .env file."

    client = genai.Client(api_key=api_key)

    safe_text = text[:12000]

    prompt = f"""
You are EduMentor AI, an expert AI learning assistant for Indian university students.

Your task:
Explain the uploaded notes in simple, beginner-friendly language.

Rules:
- Do NOT just repeat the notes.
- Explain concepts clearly.
- Use simple language suitable for college students.
- Add real-life examples.
- Add exam-oriented points.
- Add important definitions.
- Add key takeaways.
- Organize the answer with clear headings.
- If the notes contain multiple topics, explain them topic-wise.

Format the answer like this:

# Topic Overview
Explain what the uploaded notes are mainly about.

# Simple Explanation
Explain the concepts in easy language.

# Important Concepts
List and explain important concepts.

# Real-Life Examples
Give examples where useful.

# Exam Tips
Mention what students should remember for exams.

# Quick Revision Points
Give short bullet points for revision.

Uploaded Notes:
{safe_text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text

    except Exception as error:
        return f"❌ Gemini error: {error}"


if "extracted_text" not in st.session_state:
    st.session_state["extracted_text"] = ""

if "uploaded_file_name" not in st.session_state:
    st.session_state["uploaded_file_name"] = ""

if "ai_explanation" not in st.session_state:
    st.session_state["ai_explanation"] = ""


st.sidebar.markdown("## 🎓 EduMentor AI")
st.sidebar.markdown("AI Learning Assistant")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📂 Upload Notes",
        "🤖 AI Explanation",
        "📝 Summary",
        "❓ MCQs",
        "🧠 Flashcards",
        "🎤 Viva",
        "📚 Resources",
        "⚙ Settings"
    ],
    key="navigation"
)

if page == "🏠 Dashboard":
    st.markdown(
        """
        <div class="hero-title">
            Learn Smarter.<br>
            Understand Faster.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-subtitle">
            Upload your university notes and let EduMentor AI explain topics,
            generate summaries, create MCQs, build flashcards, prepare viva questions,
            and recommend free learning resources.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="section-title">Core Features</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="premium-card">
            <div class="card-title">🤖 AI Explanation</div>
            <div class="card-text">
                Understand difficult university topics in simple beginner-friendly language.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="premium-card">
            <div class="card-title">📝 Smart Summary</div>
            <div class="card-text">
                Convert long notes into clean summaries, key points, and revision notes.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="premium-card">
            <div class="card-title">❓ Exam Practice</div>
            <div class="card-text">
                Generate MCQs, flashcards, viva questions, and important exam questions.
            </div>
        </div>
        """, unsafe_allow_html=True)

elif page == "📂 Upload Notes":
    st.markdown('<div class="hero-title">Upload Notes</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero-subtitle">
            Upload PDFs, DOCX files, PPTs, TXT files, or images.
            EduMentor AI will prepare them for explanation, summaries, MCQs, flashcards, and revision.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="upload-card">
        <div class="upload-title">☁️ Drag & Drop Study Material</div>
        <div class="upload-text">
            Supported formats: PDF • DOCX • PPTX • TXT • PNG • JPG • JPEG
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose your study material",
        type=["pdf", "docx", "pptx", "txt", "png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        saved_path = save_uploaded_file(uploaded_file)

        st.success("✅ File uploaded and saved successfully!")

        st.markdown('<div class="section-title">File Details</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="premium-card">
                <div class="card-title">📄 File Name</div>
                <div class="card-text">{uploaded_file.name}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="premium-card">
                <div class="card-title">📦 File Size</div>
                <div class="card-text">{round(uploaded_file.size / 1024, 2)} KB</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="premium-card">
                <div class="card-title">🧾 File Type</div>
                <div class="card-text">{uploaded_file.type}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="upload-info">
            <div class="card-title">✅ Saved Location</div>
            <div class="card-text">{saved_path}</div>
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("Processing and cleaning document..."):
            extracted_text = process_document(saved_path)

        if extracted_text:
            st.session_state["extracted_text"] = extracted_text
            st.session_state["uploaded_file_name"] = uploaded_file.name
            st.session_state["ai_explanation"] = ""

            st.markdown('<div class="section-title">Cleaned Text Preview</div>', unsafe_allow_html=True)

            preview_text = extracted_text[:4000]

            st.markdown(
                f"""
                <div class="preview-box">
                {preview_text}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.success("✅ Document processed and stored for AI Explanation!")

        elif saved_path.suffix.lower() in [".pdf", ".txt", ".docx", ".pptx"]:
            st.warning("No readable text was found in this file.")

        else:
            st.info("Text extraction for images will be added in the OCR module.")

    else:
        st.info("Please upload a file to continue.")

elif page == "🤖 AI Explanation":
    st.markdown('<div class="hero-title">AI Explanation</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero-subtitle">
            Explain your uploaded notes in simple, beginner-friendly language using Gemini AI.
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state["extracted_text"]:
        st.markdown('<div class="section-title">Uploaded Document</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="premium-card">
            <div class="card-title">📄 {st.session_state["uploaded_file_name"]}</div>
            <div class="card-text">
                Your document is processed and ready for AI explanation.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-title">Text Preview</div>', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="preview-box">
            {st.session_state["extracted_text"][:2500]}
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("✨ Generate AI Explanation"):
            with st.spinner("Gemini is explaining your notes..."):
                st.session_state["ai_explanation"] = generate_ai_explanation(
                    st.session_state["extracted_text"]
                )

        if st.session_state["ai_explanation"]:
            st.markdown('<div class="section-title">AI Explanation Output</div>', unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="ai-output">
                {st.session_state["ai_explanation"]}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        st.warning("Please upload and process a document first from the Upload Notes page.")

else:
    st.markdown(f'<div class="hero-title">{page}</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="hero-subtitle">
            This module will be developed in upcoming lessons.
        </div>
        """,
        unsafe_allow_html=True
    )
    st.info("🚧 Module under development.")