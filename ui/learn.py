import streamlit as st

from services.ai_service import generate_ai_response


LEARN_TOOLS = {
    "explain": ("🤖 AI Explanation", "✨ Generate Explanation"),
    "summary": ("📝 Summary", "📝 Generate Summary"),
    "mcq": ("❓ MCQs", "❓ Generate MCQs"),
    "flashcards": ("🧠 Flashcards", "🧠 Generate Flashcards"),
    "viva": ("🎤 Viva", "🎤 Generate Viva Questions"),
}


def render_learn_page():
    st.markdown('<div class="hero-title">Learn</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero-subtitle">
            Use one uploaded document to generate explanations, summaries, MCQs,
            flashcards, and viva questions from one place.
        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state["extracted_text"]:
        st.warning("Please upload and process a document first from the Workspace page.")
        return

    st.markdown('<div class="section-title">Current Document</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="premium-card">
        <div class="card-title">📄 {st.session_state["uploaded_file_name"]}</div>
        <div class="card-text">
            Current AI Provider: <b>{st.session_state["selected_provider"].upper()}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    selected_mode = st.selectbox(
        "Choose what you want to generate",
        list(LEARN_TOOLS.keys()),
        format_func=lambda mode: LEARN_TOOLS[mode][0]
    )

    title, button_text = LEARN_TOOLS[selected_mode]

    if st.button(button_text):
        with st.spinner(f"EduMentor AI is generating {title}..."):
            success, response = generate_ai_response(
                selected_mode,
                st.session_state["extracted_text"],
                provider=st.session_state["selected_provider"]
            )

        if success:
            st.session_state["ai_outputs"][selected_mode] = response
            st.session_state["ai_errors"].pop(selected_mode, None)
        else:
            st.session_state["ai_errors"][selected_mode] = response

    if st.session_state["ai_errors"].get(selected_mode):
        st.warning(st.session_state["ai_errors"][selected_mode])

    if st.session_state["ai_outputs"].get(selected_mode):
        st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(st.session_state["ai_outputs"][selected_mode])