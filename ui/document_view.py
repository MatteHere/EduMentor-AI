import streamlit as st

from services.database_service import get_documents, get_document_by_id
from services.document_service import upload_document_to_unit
from ui.document_cards import render_document_card
from ui.document_dialogs import (
    render_rename_document_dialog,
    render_delete_document_confirmation,
)


def open_document_for_learning(document_id):
    document = get_document_by_id(document_id)

    if not document:
        st.error("Document not found.")
        return

    doc_id, file_name, file_path, extracted_text, created_at = document

    st.session_state["document_id"] = doc_id
    st.session_state["uploaded_file_name"] = file_name
    st.session_state["extracted_text"] = extracted_text or ""
    st.session_state["ai_outputs"] = {}
    st.session_state["ai_errors"] = {}

    st.success(f"📚 Loaded {file_name} into Learn Hub. Go to 🧠 Learn.")


def render_document_view(render_breadcrumb):
    st.markdown(
        f'<div class="hero-title">{st.session_state["unit_name"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-subtitle">
            Upload and manage study material for this unit.
        </div>
        """,
        unsafe_allow_html=True
    )

    render_breadcrumb()

    if st.button("⬅ Back to Units"):
        st.session_state["unit_id"] = None
        st.session_state["unit_name"] = ""
        st.rerun()

    st.markdown('<div class="section-title">Upload Notes</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose your study material",
        type=["pdf", "docx", "pptx", "txt", "png", "jpg", "jpeg"],
        key=f"unit_upload_{st.session_state['unit_id']}"
    )

    if uploaded_file is not None:
        if st.button("📤 Process & Save Document", key="process_save_document"):
            with st.spinner("Processing and saving document..."):
                success, message, document_id = upload_document_to_unit(
                    uploaded_file,
                    st.session_state["unit_id"]
                )

            if success:
                st.session_state["document_id"] = document_id
                st.success(f"✅ {message}")
                st.rerun()
            else:
                st.error(message)

    st.markdown('<div class="section-title">Documents</div>', unsafe_allow_html=True)

    documents = get_documents(st.session_state["unit_id"])

    if not documents:
        st.info("No documents uploaded for this unit yet.")
        return

    for document in documents:
        document_id, file_name, file_path, created_at = document

        learn_clicked, rename_clicked, delete_clicked = render_document_card(document)

        if learn_clicked:
            open_document_for_learning(document_id)

        if rename_clicked:
            st.session_state["edit_document_id"] = document_id

        if st.session_state.get("edit_document_id") == document_id:
            render_rename_document_dialog(document_id, file_name)

        if delete_clicked:
            st.session_state["delete_document_id"] = document_id
            st.session_state["delete_document_name"] = file_name

        if st.session_state.get("delete_document_id") == document_id:
            render_delete_document_confirmation(document_id, file_name)