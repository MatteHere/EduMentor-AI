import streamlit as st

from services.database_service import get_subjects
from ui.workspace_cards import render_subject_card
from ui.workspace_dialogs import (
    render_create_subject_dialog,
    render_delete_subject_confirmation,
)


def open_subject(subject_id, subject_name):
    st.session_state["subject_id"] = subject_id
    st.session_state["subject_name"] = subject_name
    st.session_state["unit_id"] = None
    st.session_state["unit_name"] = ""


def render_subject_view(render_breadcrumb):
    st.markdown(
        f'<div class="hero-title">{st.session_state["workspace_name"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-subtitle">
            Select a subject inside this workspace.
        </div>
        """,
        unsafe_allow_html=True
    )

    render_breadcrumb()

    if st.button("⬅ Back to Workspaces"):
        st.session_state["workspace_id"] = None
        st.session_state["workspace_name"] = ""
        st.session_state["subject_id"] = None
        st.session_state["subject_name"] = ""
        st.session_state["unit_id"] = None
        st.session_state["unit_name"] = ""
        st.rerun()

    render_create_subject_dialog(st.session_state["workspace_id"])

    subjects = get_subjects(st.session_state["workspace_id"])

    if not subjects:
        st.info("No subjects found. Add your first subject.")
        return

    st.markdown(
        '<div class="section-title">Subjects</div>',
        unsafe_allow_html=True
    )

    for subject in subjects:
        subject_id, subject_name, created_at = subject

        open_clicked, edit_clicked, delete_clicked = render_subject_card(
            subject,
            st.session_state["workspace_name"]
        )

        if open_clicked:
            open_subject(subject_id, subject_name)
            st.rerun()

        if edit_clicked:
            st.info("✏ Edit Subject will be added next.")

        if delete_clicked:
            st.session_state["delete_subject_id"] = subject_id
            st.session_state["delete_subject_name"] = subject_name

        if st.session_state.get("delete_subject_id") == subject_id:
            render_delete_subject_confirmation(subject_id, subject_name)