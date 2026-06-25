import streamlit as st
from pathlib import Path
import pdfplumber

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
        text = file.read()

    return text.strip()


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

        extracted_text = ""

        if saved_path.suffix.lower() == ".pdf":
            with st.spinner("Extracting text from PDF..."):
                extracted_text = extract_text_from_pdf(saved_path)

        elif saved_path.suffix.lower() == ".txt":
            with st.spinner("Reading TXT file..."):
                extracted_text = extract_text_from_txt(saved_path)

        if extracted_text:
            st.markdown('<div class="section-title">Extracted Text Preview</div>', unsafe_allow_html=True)

            preview_text = extracted_text[:4000]

            st.markdown(
                f"""
                <div class="preview-box">
                {preview_text}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.success("✅ Text extracted successfully!")

        elif saved_path.suffix.lower() in [".pdf", ".txt"]:
            st.warning("No readable text was found in this file.")

    else:
        st.info("Please upload a file to continue.")

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