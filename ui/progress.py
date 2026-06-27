import streamlit as st

from services.database_service import (
    get_workspaces,
    get_subjects,
    get_units,
    get_documents,
)


def count_all_items():
    workspaces = get_workspaces()
    subjects_count = 0
    units_count = 0
    documents_count = 0

    for workspace in workspaces:
        subjects = get_subjects(workspace[0])
        subjects_count += len(subjects)

        for subject in subjects:
            units = get_units(subject[0])
            units_count += len(units)

            for unit in units:
                documents = get_documents(unit[0])
                documents_count += len(documents)

    return len(workspaces), subjects_count, units_count, documents_count


def render_progress_card(title, value, icon):
    st.markdown(
        f"""
        <div class="premium-card">
            <div class="card-title">{icon} {value}</div>
            <div class="card-text">{title}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_progress_page():
    st.markdown('<div class="hero-title">Progress</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero-subtitle">
            Track your EduMentor AI study activity and learning progress.
        </div>
        """,
        unsafe_allow_html=True,
    )

    workspaces, subjects, units, documents = count_all_items()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_progress_card("Workspaces", workspaces, "📂")

    with col2:
        render_progress_card("Subjects", subjects, "📚")

    with col3:
        render_progress_card("Units", units, "🗂")

    with col4:
        render_progress_card("Documents", documents, "📄")

    total_score = workspaces + subjects + units + documents
    progress_value = min(total_score / 20, 1.0)

    st.markdown('<div class="section-title">Overall Study Setup Progress</div>', unsafe_allow_html=True)

    st.progress(progress_value)

    st.markdown(
        f"""
        <div class="premium-card">
            <div class="card-title">📈 Completion</div>
            <div class="card-text">
                Your current EduMentor setup progress is <b>{int(progress_value * 100)}%</b>.<br>
                Add more subjects, units, and documents to improve your study structure.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )