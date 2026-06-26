import streamlit as st
from dotenv import load_dotenv

from services.ai_service import generate_ai_response
from services.document_service import (
    save_uploaded_file,
    process_document,
)

load_dotenv()

st.set_page_config(
    page_title="EduMentor AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #F8FAFC 0%, #EEF2FF 45%, #ECFDF5 100%); }
.main .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1300px; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%); }
[data-testid="stSidebar"] * { color: #F8FAFC !important; }

.hero-title { color:#0F172A; font-size:58px; font-weight:850; line-height:1.08; margin-bottom:16px; }
.hero-subtitle { color:#334155; font-size:21px; line-height:1.6; max-width:900px; margin-bottom:32px; }
.section-title { color:#0F172A; font-size:34px; font-weight:800; margin-top:36px; margin-bottom:20px; }

.premium-card {
    background:rgba(255,255,255,0.92);
    border:1px solid rgba(15,23,42,0.08);
    border-radius:24px;
    padding:28px;
    min-height:170px;
    box-shadow:0 18px 45px rgba(15,23,42,0.08);
}

.card-title { color:#0F172A; font-size:23px; font-weight:800; margin-bottom:12px; }
.card-text { color:#475569; font-size:16px; line-height:1.7; }

.upload-card {
    background:#FFFFFF;
    border:2px dashed rgba(16,185,129,0.45);
    border-radius:26px;
    padding:32px;
    margin-bottom:22px;
    box-shadow:0 16px 40px rgba(15,23,42,0.08);
}

.upload-title { color:#0F172A; font-size:26px; font-weight:800; margin-bottom:10px; }
.upload-text { color:#475569; font-size:17px; line-height:1.6; }

.preview-box {
    background:#FFFFFF;
    border:1px solid rgba(15,23,42,0.10);
    border-radius:20px;
    padding:24px;
    max-height:420px;
    overflow-y:auto;
    box-shadow:0 14px 35px rgba(15,23,42,0.08);
    color:#0F172A;
    white-space:pre-wrap;
    line-height:1.7;
}

[data-testid="stAlert"] { border-radius:16px; border:1px solid rgba(16,185,129,0.35); }
[data-testid="stAlert"] * { color:#0F172A !important; }

.stButton > button {
    background:linear-gradient(135deg,#2563EB,#10B981);
    color:white;
    border:none;
    border-radius:14px;
    padding:0.75rem 1.3rem;
    font-weight:700;
}

[data-testid="stFileUploader"] {
    background:#FFFFFF;
    border-radius:18px;
    padding:10px;
    border:1px solid rgba(15,23,42,0.08);
}

header { background:transparent !important; }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    if "extracted_text" not in st.session_state:
        st.session_state["extracted_text"] = ""

    if "uploaded_file_name" not in st.session_state:
        st.session_state["uploaded_file_name"] = ""

    if "uploaded_file_signature" not in st.session_state:
        st.session_state["uploaded_file_signature"] = ""

    if "ai_outputs" not in st.session_state:
        st.session_state["ai_outputs"] = {}

    if "ai_errors" not in st.session_state:
        st.session_state["ai_errors"] = {}


def render_dashboard():
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
            Upload your university notes and generate explanations, summaries,
            MCQs, flashcards, and viva questions.
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
            <div class="card-text">Understand difficult topics in beginner-friendly language.</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="premium-card">
            <div class="card-title">📝 Smart Summary</div>
            <div class="card-text">Convert long notes into summaries and revision points.</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="premium-card">
            <div class="card-title">❓ Exam Practice</div>
            <div class="card-text">Generate MCQs, flashcards, and viva questions.</div>
        </div>
        """, unsafe_allow_html=True)


def render_upload_page():
    st.markdown('<div class="hero-title">Upload Notes</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero-subtitle">
            Upload PDFs, DOCX files, PPTs, TXT files, or images.
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

    if uploaded_file is None:
        st.info("Please upload a file to continue.")
        return

    file_signature = f"{uploaded_file.name}_{uploaded_file.size}"
    saved_path = save_uploaded_file(uploaded_file)

    st.success("✅ File uploaded and saved successfully!")

    with st.spinner("Processing and cleaning document..."):
        extracted_text = process_document(saved_path)

    if extracted_text:
        if st.session_state["uploaded_file_signature"] != file_signature:
            st.session_state["ai_outputs"] = {}
            st.session_state["ai_errors"] = {}

        st.session_state["extracted_text"] = extracted_text
        st.session_state["uploaded_file_name"] = uploaded_file.name
        st.session_state["uploaded_file_signature"] = file_signature

        st.markdown('<div class="section-title">Cleaned Text Preview</div>', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="preview-box">
            {extracted_text[:4000]}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.success("✅ Document processed and ready for all AI tools!")

    elif saved_path.suffix.lower() in [".pdf", ".txt", ".docx", ".pptx"]:
        st.warning("No readable text was found in this file.")

    else:
        st.info("Text extraction for images will be added in the OCR module.")


def render_ai_page(title, subtitle, mode, button_text):
    st.markdown(f'<div class="hero-title">{title}</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="hero-subtitle">
            {subtitle}
        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state["extracted_text"]:
        st.warning("Please upload and process a document first from the Upload Notes page.")
        return

    st.markdown('<div class="section-title">Uploaded Document</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="premium-card">
        <div class="card-title">📄 {st.session_state["uploaded_file_name"]}</div>
        <div class="card-text">Your document is processed and ready.</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button(button_text):
        with st.spinner("EduMentor AI is generating your result..."):
            success, response = generate_ai_response(
                mode,
                st.session_state["extracted_text"]
            )

        if success:
            st.session_state["ai_outputs"][mode] = response
            st.session_state["ai_errors"].pop(mode, None)
        else:
            st.session_state["ai_errors"][mode] = response

    if st.session_state["ai_errors"].get(mode):
        st.warning(st.session_state["ai_errors"][mode])

    if st.session_state["ai_outputs"].get(mode):
        st.markdown('<div class="section-title">Generated Output</div>', unsafe_allow_html=True)
        st.markdown(st.session_state["ai_outputs"][mode])


initialize_session_state()

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
    render_dashboard()

elif page == "📂 Upload Notes":
    render_upload_page()

elif page == "🤖 AI Explanation":
    render_ai_page(
        "AI Explanation",
        "Explain uploaded notes in simple, beginner-friendly language.",
        "explain",
        "✨ Generate Explanation"
    )

elif page == "📝 Summary":
    render_ai_page(
        "Smart Summary",
        "Generate clean summaries, key points, and revision notes.",
        "summary",
        "📝 Generate Summary"
    )

elif page == "❓ MCQs":
    render_ai_page(
        "MCQ Generator",
        "Generate exam-style MCQs from uploaded notes.",
        "mcq",
        "❓ Generate MCQs"
    )

elif page == "🧠 Flashcards":
    render_ai_page(
        "Flashcards",
        "Create question-answer flashcards for quick revision.",
        "flashcards",
        "🧠 Generate Flashcards"
    )

elif page == "🎤 Viva":
    render_ai_page(
        "Viva Questions",
        "Generate viva questions with answers for oral exams.",
        "viva",
        "🎤 Generate Viva Questions"
    )

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