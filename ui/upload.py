import streamlit as st

from services.document_service import save_uploaded_file, process_document


def render_upload_page():
    st.markdown('<div class="hero-title">Upload Notes</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero-subtitle">
            Upload PDFs, DOCX files, PPTs, TXT files, or images.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="upload-card">
        <div class="upload-title">☁️ Drag & Drop Study Material</div>
        <div class="upload-text">
            Supported formats: PDF • DOCX • PPTX • TXT • PNG • JPG • JPEG
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose your study material",
        type=["pdf", "docx", "pptx", "txt", "png", "jpg", "jpeg"]
    )

    if uploaded_file is None:
        st.info("Please upload a file to continue.")
        return

    file_signature = f"{uploaded_file.name}_{uploaded_file.size}"
    saved_path = save_uploaded_file(uploaded_file)

    st.success("✅ File uploaded and saved successfully!")

    with st.spinner("Processing and cleaning document..."):
        extracted_text = process_document(saved_path)

    if extracted_text:
        if st.session_state["uploaded_file_signature"] != file_signature:
            st.session_state["ai_outputs"] = {}
            st.session_state["ai_errors"] = {}

        st.session_state["extracted_text"] = extracted_text
        st.session_state["uploaded_file_name"] = uploaded_file.name
        st.session_state["uploaded_file_signature"] = file_signature

        st.markdown('<div class="section-title">Cleaned Text Preview</div>', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="preview-box">
            {extracted_text[:4000]}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.success("✅ Document processed and ready for all AI tools!")

    elif saved_path.suffix.lower() in [".pdf", ".txt", ".docx", ".pptx"]:
        st.warning("No readable text was found in this file.")

    else:
        st.info("Text extraction for images will be added in the OCR module.")