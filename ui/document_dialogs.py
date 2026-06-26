import streamlit as st

from services.database_service import (
    update_document_name,
    delete_document,
)


def render_rename_document_dialog(document_id, current_name):
    with st.expander("✏ Rename Document", expanded=True):

        new_name = st.text_input(
            "Document Name",
            value=current_name,
            key=f"rename_document_input_{document_id}"
        )

        if st.button("Save", key=f"save_document_{document_id}"):

            if not new_name.strip():
                st.warning("Document name cannot be empty.")
                return

            update_document_name(
                document_id,
                new_name.strip()
            )

            st.success("✅ Document renamed successfully.")

            st.session_state["edit_document_id"] = None

            st.rerun()


def render_delete_document_confirmation(document_id, file_name):

    st.warning(
        f"⚠️ Delete **{file_name}** ?"
    )

    st.write(
        "This will permanently delete the document and all cached AI outputs."
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Cancel",
            key=f"cancel_document_delete_{document_id}"
        ):

            st.session_state["delete_document_id"] = None
            st.rerun()

    with col2:

        if st.button(
            "🗑 Delete",
            key=f"confirm_document_delete_{document_id}"
        ):

            delete_document(document_id)

            st.session_state["delete_document_id"] = None
            st.session_state["document_id"] = None
            st.session_state["uploaded_file_name"] = ""
            st.session_state["extracted_text"] = ""

            st.success("Document deleted successfully.")

            st.rerun()