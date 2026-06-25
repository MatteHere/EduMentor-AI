import streamlit as st

st.set_page_config(
    page_title="EduMentor AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#020617,#0F172A,#111827);
}

[data-testid="stSidebar"] {
    background-color:#0F172A;
}

[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}

.hero-title {
    color:#FFFFFF;
    font-size:56px;
    font-weight:800;
    margin-bottom:12px;
}

.hero-subtitle {
    color:#E2E8F0;
    font-size:21px;
    margin-bottom:35px;
}

.feature-card {
    background:rgba(255,255,255,0.10);
    border-radius:20px;
    padding:28px;
    border:1px solid rgba(255,255,255,0.18);
    min-height:150px;
}

.feature-title {
    color:#FFFFFF;
    font-size:23px;
    font-weight:700;
    margin-bottom:12px;
}

.feature-text {
    color:#E2E8F0;
    font-size:16px;
    line-height:1.6;
}

.vision-title {
    color:#FFFFFF;
    font-size:32px;
    font-weight:800;
    margin-top:35px;
    margin-bottom:20px;
}

.vision-text {
    color:#E2E8F0 !important;
    font-size:18px;
    line-height:1.8;
}

.vision-text li {
    color:#FFFFFF !important;
    font-size:17px;
    margin-bottom:8px;
}

[data-testid="stAlert"] {
    background-color: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.35);
}

[data-testid="stAlert"] * {
    color: #F8FAFC !important;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🎓 EduMentor AI")
st.sidebar.write("AI Learning Assistant")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📂 Upload Notes",
        "📖 Explain Notes",
        "📝 Summaries",
        "❓ MCQs",
        "🧠 Flashcards",
        "📚 Resources"
    ],
    key="main_navigation"
)

if page == "🏠 Home":
    st.markdown('<div class="hero-title">EduMentor AI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">AI Learning Assistant for Indian University Students</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📂 Upload Notes</div>
            <div class="feature-text">Upload PDF, DOCX, PPTX, TXT or Images.</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🤖 AI Explanation</div>
            <div class="feature-text">Understand difficult topics in simple language.</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📝 Exam Preparation</div>
            <div class="feature-text">Generate summaries, MCQs, flashcards and viva questions.</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.markdown('<div class="vision-title">🚀 Vision</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="vision-text">
    EduMentor AI aims to become India's smartest AI learning platform for college students.
    <br><br>
    Students will be able to upload their notes and instantly receive:
    <ul>
        <li>📖 Easy-to-understand explanations</li>
        <li>📝 Smart summaries</li>
        <li>🎯 Important questions</li>
        <li>❓ MCQs</li>
        <li>🧠 Flashcards</li>
        <li>🎤 Viva questions</li>
        <li>📚 Free learning resources</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

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
            This module is currently under development.
            It will be available in the upcoming lessons as we build EduMentor AI step by step.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info("🚧 This module will be developed in upcoming lessons.")