import streamlit as st


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