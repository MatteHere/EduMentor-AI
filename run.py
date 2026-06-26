import streamlit as st
from dotenv import load_dotenv

from services.database_service import initialize_database
from services.provider_manager import get_default_provider

from ui.dashboard import render_dashboard
from ui.workspace import render_workspace_page
from ui.learn import render_learn_page
from ui.settings import render_settings_page

load_dotenv()
initialize_database()

st.set_page_config(
    page_title="EduMentor AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


def initialize_session_state():
    defaults = {
        "extracted_text": "",
        "uploaded_file_name": "",
        "uploaded_file_signature": "",
        "document_id": None,

        "workspace_id": None,
        "workspace_name": "",

        "subject_id": None,
        "subject_name": "",

        "unit_id": None,
        "unit_name": "",

        "delete_workspace_id": None,
        "delete_workspace_name": "",

        "delete_subject_id": None,
        "delete_subject_name": "",

        "selected_provider": get_default_provider(),

        "ai_outputs": {},
        "ai_errors": {},
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


initialize_session_state()

st.markdown("""
<style>
.stApp{
    background:linear-gradient(135deg,#F8FAFC,#EEF2FF,#ECFDF5);
}

.main .block-container{
    padding-top:2rem;
    padding-bottom:2rem;
    max-width:1400px;
}

[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#0F172A,#1E293B);
}

[data-testid="stSidebar"] *{
    color:white !important;
}

.hero-title{
    font-size:58px;
    font-weight:800;
    color:#0F172A;
    line-height:1.1;
    margin-bottom:16px;
}

.hero-subtitle{
    font-size:20px;
    color:#475569;
    margin-bottom:25px;
    line-height:1.6;
}

.section-title{
    font-size:30px;
    font-weight:700;
    margin-top:25px;
    margin-bottom:15px;
    color:#0F172A;
}

.premium-card{
    background:white;
    border-radius:20px;
    padding:25px;
    box-shadow:0 10px 25px rgba(0,0,0,.08);
    margin-bottom:20px;
    border:1px solid rgba(15,23,42,0.08);
}

.card-title{
    font-size:22px;
    font-weight:800;
    color:#0F172A;
    margin-bottom:10px;
}

.card-text{
    font-size:16px;
    color:#475569;
    line-height:1.7;
}

.upload-card{
    background:white;
    border:2px dashed rgba(16,185,129,0.45);
    border-radius:24px;
    padding:28px;
    margin-bottom:20px;
}

.upload-title{
    color:#0F172A;
    font-size:24px;
    font-weight:800;
}

.upload-text{
    color:#475569;
    font-size:16px;
}

.preview-box{
    background:white;
    border:1px solid rgba(15,23,42,0.10);
    border-radius:20px;
    padding:24px;
    max-height:420px;
    overflow-y:auto;
    color:#0F172A;
    white-space:pre-wrap;
    line-height:1.7;
}

.stButton > button{
    background:linear-gradient(135deg,#2563EB,#10B981);
    color:white;
    border:none;
    border-radius:14px;
    padding:0.7rem 1.2rem;
    font-weight:700;
}

[data-testid="stAlert"]{
    border-radius:16px;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🎓 EduMentor AI")
st.sidebar.caption("AI Learning Platform")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📂 Workspace",
        "🧠 Learn",
        "📅 Study Planner",
        "📈 Progress",
        "🎓 University Hub",
        "⚙ Settings",
    ]
)

if page == "🏠 Dashboard":
    render_dashboard()

elif page == "📂 Workspace":
    render_workspace_page()

elif page == "🧠 Learn":
    render_learn_page()

elif page == "⚙ Settings":
    render_settings_page()

elif page == "📅 Study Planner":
    st.markdown('<div class="hero-title">Study Planner</div>', unsafe_allow_html=True)
    st.info("🚧 Coming in Phase 2")

elif page == "📈 Progress":
    st.markdown('<div class="hero-title">Progress</div>', unsafe_allow_html=True)
    st.info("🚧 Coming in Phase 2")

elif page == "🎓 University Hub":
    st.markdown('<div class="hero-title">University Hub</div>', unsafe_allow_html=True)
    st.info("🚧 Coming in Phase 4")