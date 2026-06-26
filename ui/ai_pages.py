import streamlit as st

from services.ai_service import generate_ai_response


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
        <div class="card-text">
            Your document is processed and ready.<br>
            Current AI Provider: <b>{st.session_state["selected_provider"].upper()}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button(button_text):
        with st.spinner("EduMentor AI is generating your result..."):
            success, response = generate_ai_response(
                mode,
                st.session_state["extracted_text"],
                provider=st.session_state["selected_provider"]
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