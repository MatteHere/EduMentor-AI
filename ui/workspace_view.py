import streamlit as st

from services.database_service import get_workspaces
from ui.workspace_cards import render_workspace_card
from ui.workspace_dialogs import (
    render_create_workspace_dialog,
    render_delete_workspace_confirmation,
)


def open_workspace(workspace_id, workspace_name):
    st.session_state["workspace_id"] = workspace_id
    st.session_state["workspace_name"] = workspace_name
    st.session_state["subject_id"] = None
    st.session_state["subject_name"] = ""
    st.session_state["unit_id"] = None
    st.session_state["unit_name"] = ""


def render_workspace_view():
    st.markdown('<div class="hero-title">My Workspaces</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero-subtitle">
            Choose a semester workspace or create a new one.
        </div>
        """,
        unsafe_allow_html=True
    )

    render_create_workspace_dialog()

    workspaces = get_workspaces()

    if not workspaces:
        st.info("No workspaces found. Create your first workspace above.")
        return

    st.markdown('<div class="section-title">Available Workspaces</div>', unsafe_allow_html=True)

    for workspace in workspaces:
        workspace_id, name, university, stream, semester, created_at = workspace

        open_clicked, edit_clicked, delete_clicked = render_workspace_card(workspace)

        if open_clicked:
            open_workspace(workspace_id, name)
            st.rerun()

        if edit_clicked:
            st.info("✏ Edit Workspace will be added later.")

        if delete_clicked:
            st.session_state["delete_workspace_id"] = workspace_id
            st.session_state["delete_workspace_name"] = name

        if st.session_state.get("delete_workspace_id") == workspace_id:
            render_delete_workspace_confirmation(workspace_id, name)