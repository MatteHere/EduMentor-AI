import streamlit as st


UNIVERSITIES = {
    "SPPU": {
        "description": "Savitribai Phule Pune University study support for syllabus, notes, question papers, and exam preparation.",
        "resources": [
            "Official SPPU syllabus",
            "Previous year question papers",
            "Subject-wise notes",
            "NPTEL lectures",
            "YouTube playlists",
        ],
    },
    "Deemed University": {
        "description": "Study support for deemed/private university students across different streams and subjects.",
        "resources": [
            "University syllabus",
            "Lecture notes",
            "Reference books",
            "Online tutorials",
            "Practice questions",
        ],
    },
}


def render_university_page():
    st.markdown('<div class="hero-title">University Hub</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero-subtitle">
            Find university-focused study direction, resources, and academic support.
        </div>
        """,
        unsafe_allow_html=True,
    )

    selected_university = st.selectbox(
        "Select University Type",
        list(UNIVERSITIES.keys()),
    )

    data = UNIVERSITIES[selected_university]

    st.markdown(
        f"""
        <div class="premium-card">
            <div class="card-title">🎓 {selected_university}</div>
            <div class="card-text">
                {data["description"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-title">Recommended Resources</div>', unsafe_allow_html=True)

    for resource in data["resources"]:
        st.markdown(
            f"""
            <div class="premium-card">
                <div class="card-title">📌 {resource}</div>
                <div class="card-text">
                    Use this as a starting point while preparing your subjects and uploading notes into EduMentor AI.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )