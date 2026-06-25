import streamlit as st
from pathlib import Path

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="EduMentor AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #F8FAFC 0%, #EEF2FF 45%, #ECFDF5 100%);
}

/* Main container */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1300px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
    border-right: 1px solid rgba(255,255,255,0.12);
}

[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}

/* Radio buttons */
[data-testid="stSidebar"] label {
    color: #E2E8F0 !important;
}

/* Headings */
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

/* Cards */
.premium-card {
    background: rgba(255,255,255,0.92);
    border: 1px solid rgba(15,23,42,0.08);
    border-radius: 24px;
    padding: 28px;
    min-height: 170px;
    box-shadow: 0 18px 45px rgba(15,23,42,0.08);
}

.premium-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 22px 55px rgba(15,23,42,0.12);
    transition: all 0.25s ease;
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

/* Upload card */
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

/* Success box */
.upload-info {
    background: rgba(16,185,129,0.10);
    border: 1px solid rgba(16,185,129,0.35);
    border-radius: 20px;
    padding: 24px;
    margin-top: 20px;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 16px;
    border: 1px solid rgba(16,185,129,0.35);
}

[data-testid="stAlert"] * {
    color: #0F172A !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #2563EB, #10B981);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 0.75rem 1.3rem;
    font-weight: 700;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 30px rgba(37,99,235,0.25);
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 10px;
    border: 1px solid rgba(15,23,42,0.08);
}

/* Hide Streamlit default menu spacing feel */
header {
    background: transparent !important;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# FILE STORAGE
# ==========================================================

UPLOAD_FOLDER = Path("data/uploads")


def save_uploaded_file(uploaded_file):
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

    file_path = UPLOAD_FOLDER / uploaded_file.name

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return file_path


# ==========================================================
# SIDEBAR
# ==========================================================

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

# ==========================================================
# DASHBOARD PAGE
# ==========================================================

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

    st.markdown('<div class="section-title">Future Vision</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="premium-card">
        <div class="card-text">
            EduMentor AI will start with SPPU and AI & Data Science students,
            then expand to Computer Engineering, IT, Mechanical, Civil, Electronics,
            MBA, BBA, BCA, MCA, Pharmacy, Law, Medical, and more Indian university streams.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================================
# UPLOAD NOTES PAGE
# ==========================================================

elif page == "📂 Upload Notes":

    st.markdown(
        """
        <div class="hero-title">
            Upload Notes
        </div>
        """,
        unsafe_allow_html=True
    )

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

        st.markdown('<div class="section-title">Next Actions</div>', unsafe_allow_html=True)

        col_a, col_b, col_c, col_d = st.columns(4)

        with col_a:
            st.button("🤖 Explain")

        with col_b:
            st.button("📝 Summary")

        with col_c:
            st.button("❓ MCQs")

        with col_d:
            st.button("🧠 Flashcards")

    else:
        st.info("Please upload a file to continue.")

# ==========================================================
# PLACEHOLDER PAGES
# ==========================================================

else:

    st.markdown(
        f"""
        <div class="hero-title">
            {page}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-subtitle">
            This module will be developed in upcoming lessons.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info("🚧 Module under development.")