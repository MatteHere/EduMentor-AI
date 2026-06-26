import streamlit as st

from services.database_service import (
    create_workspace,
    create_subject,
    delete_workspace,
    delete_subject,
)


def render_create_workspace_dialog():
    with st.expander("➕ Create New Workspace", expanded=False):
        workspace_name = st.text_input(
            "Workspace Name",
            placeholder="Example: Semester III",
            key="new_workspace_name"
        )

        university = st.text_input(
            "University",
            placeholder="Example: SPPU",
            key="new_workspace_university"
        )

        stream = st.text_input(
            "Stream",
            placeholder="Example: AI & DS",
            key="new_workspace_stream"
        )

        semester = st.text_input(
            "Semester",
            placeholder="Example: Semester III",
            key="new_workspace_semester"
        )

        if st.button("Create Workspace", key="create_workspace_button"):
            if not workspace_name.strip():
                st.warning("Please enter a workspace name.")
                return

            workspace_id = create_workspace(
                workspace_name.strip(),
                university.strip(),
                stream.strip(),
                semester.strip()
            )

            st.session_state["workspace_id"] = workspace_id
            st.session_state["workspace_name"] = workspace_name.strip()
            st.session_state["subject_id"] = None
            st.session_state["subject_name"] = ""

            st.success("✅ Workspace created successfully!")
            st.rerun()


def render_create_subject_dialog(workspace_id):
    with st.expander("➕ Add Subject", expanded=False):
        subject_name = st.text_input(
            "Subject Name",
            placeholder="Example: Computer Organization",
            key="new_subject_name"
        )

        if st.button("Create Subject", key="create_subject_button"):
            if not subject_name.strip():
                st.warning("Please enter a subject name.")
                return

            subject_id = create_subject(workspace_id, subject_name.strip())

            st.session_state["subject_id"] = subject_id
            st.session_state["subject_name"] = subject_name.strip()

            st.success("✅ Subject created successfully!")
            st.rerun()


def render_delete_workspace_confirmation(workspace_id, workspace_name):
    st.warning(f"⚠️ Are you sure you want to delete workspace: **{workspace_name}**?")

    st.markdown(
        """
        This will permanently delete:
        - Subjects
        - Units
        - Documents
        - AI outputs
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Cancel", key=f"cancel_delete_workspace_{workspace_id}"):
            st.session_state["delete_workspace_id"] = None
            st.session_state["delete_workspace_name"] = ""
            st.rerun()

    with col2:
        if st.button("🗑 Delete Workspace", key=f"confirm_delete_workspace_{workspace_id}"):
            delete_workspace(workspace_id)

            st.session_state["workspace_id"] = None
            st.session_state["workspace_name"] = ""
            st.session_state["subject_id"] = None
            st.session_state["subject_name"] = ""
            st.session_state["unit_id"] = None
            st.session_state["unit_name"] = ""
            st.session_state["delete_workspace_id"] = None
            st.session_state["delete_workspace_name"] = ""

            st.success("Workspace deleted successfully.")
            st.rerun()


def render_delete_subject_confirmation(subject_id, subject_name):
    st.warning(f"⚠️ Are you sure you want to delete subject: **{subject_name}**?")

    st.markdown(
        """
        This will permanently delete:
        - Units
        - Documents
        - AI outputs
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Cancel", key=f"cancel_delete_subject_{subject_id}"):
            st.session_state["delete_subject_id"] = None
            st.session_state["delete_subject_name"] = ""
            st.rerun()

    with col2:
        if st.button("🗑 Delete Subject", key=f"confirm_delete_subject_{subject_id}"):
            delete_subject(subject_id)

            st.session_state["subject_id"] = None
            st.session_state["subject_name"] = ""
            st.session_state["unit_id"] = None
            st.session_state["unit_name"] = ""
            st.session_state["delete_subject_id"] = None
            st.session_state["delete_subject_name"] = ""

            st.success("Subject deleted successfully.")
            st.rerun()