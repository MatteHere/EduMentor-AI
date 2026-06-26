import streamlit as st
from dotenv import load_dotenv

from services.provider_manager import get_default_provider
from ui.dashboard import render_dashboard
from ui.upload import render_upload_page
from ui.learn import render_learn_page
from ui.ai_pages import render_ai_page
from ui.settings import render_settings_page

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
    defaults = {
        "extracted_text": "",
        "uploaded_file_name": "",
        "uploaded_file_signature": "",
        "ai_outputs": {},
        "ai_errors": {},
        "selected_provider": get_default_provider(),
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


initialize_session_state()

st.sidebar.markdown("## 🎓 EduMentor AI")
st.sidebar.markdown("AI Learning Assistant")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📂 Workspace",
        "🧠 Learn",
        "📅 Study Planner",
        "📈 Progress",
        "🎓 University Resources",
        "⚙ Settings"
    ],
    key="navigation"
)

if page == "🏠 Dashboard":
    render_dashboard()

elif page == "📂 Workspace":
    render_upload_page()

elif page == "🧠 Learn":
    render_learn_page()

elif page == "⚙ Settings":
    render_settings_page()

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