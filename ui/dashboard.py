import streamlit as st

from services.database_service import (
    get_workspaces,
    get_subjects,
    get_units,
    get_documents,
)


def safe_count(items):
    return len(items) if items else 0


def get_dashboard_counts():
    workspaces = get_workspaces()
    total_subjects = 0
    total_units = 0
    total_documents = 0

    for workspace in workspaces:
        workspace_id = workspace[0]
        subjects = get_subjects(workspace_id)
        total_subjects += safe_count(subjects)

        for subject in subjects:
            subject_id = subject[0]
            units = get_units(subject_id)
            total_units += safe_count(units)

            for unit in units:
                unit_id = unit[0]
                documents = get_documents(unit_id)
                total_documents += safe_count(documents)

    return {
        "workspaces": safe_count(workspaces),
        "subjects": total_subjects,
        "units": total_units,
        "documents": total_documents,
    }


def render_stat_card(icon, title, value):
    st.markdown(
        f"""
        <div class="premium-card">
            <div class="card-title">{icon} {value}</div>
            <div class="card-text">{title}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_quick_action(title, description):
    st.markdown(
        f"""
        <div class="premium-card">
            <div class="card-title">{title}</div>
            <div class="card-text">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dashboard():
    counts = get_dashboard_counts()

    st.markdown('<div class="hero-title">🎓 EduMentor AI</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero-subtitle">
            Your personal AI study companion for uploading notes, learning concepts,
            practicing MCQs, revising with flashcards, preparing viva, and chatting with your study material.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-title">Overview</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_stat_card("📂", "Workspaces", counts["workspaces"])

    with col2:
        render_stat_card("📚", "Subjects", counts["subjects"])

    with col3:
        render_stat_card("🗂", "Units", counts["units"])

    with col4:
        render_stat_card("📄", "Documents", counts["documents"])

    st.markdown('<div class="section-title">Quick Start</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        render_quick_action(
            "📂 Workspace",
            "Create workspaces, add subjects and units, then upload your notes."
        )

    with col2:
        render_quick_action(
            "🧠 Learn Hub",
            "Generate explanations, summaries, MCQs, flashcards, viva questions, and resources."
        )

    with col3:
        render_quick_action(
            "💬 AI Chat",
            "Ask questions directly from the uploaded notes and get document-based answers."
        )

    st.markdown('<div class="section-title">Final Project Modules</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="premium-card">
            <div class="card-title">✅ Completed Scope</div>
            <div class="card-text">
                • Dashboard<br>
                • Workspace Management<br>
                • Subject and Unit Organization<br>
                • Document Upload and Processing<br>
                • Learn Hub<br>
                • Interactive MCQ Quiz<br>
                • Interactive Flashcards<br>
                • Interactive Viva Practice<br>
                • AI Chat with Notes<br>
                • AI Provider Settings<br>
                • SQLite Database Storage
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )