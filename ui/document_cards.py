import streamlit as st


def get_file_icon(file_name):
    file_name = file_name.lower()

    if file_name.endswith(".pdf"):
        return "📕 PDF"

    if file_name.endswith(".docx"):
        return "📘 DOCX"

    if file_name.endswith(".pptx"):
        return "📙 PPTX"

    if file_name.endswith(".txt"):
        return "📄 TXT"

    if file_name.endswith((".png", ".jpg", ".jpeg")):
        return "🖼 IMAGE"

    return "📁 FILE"


def render_document_card(document):
    document_id, file_name, file_path, created_at = document
    file_icon = get_file_icon(file_name)

    with st.expander(f"{file_icon} • {file_name}", expanded=False):
        st.markdown(
            f"""
            <div class="card-text">
                <b>Uploaded:</b> {created_at}<br>
                <b>Path:</b> {file_path}
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            learn_clicked = st.button("📚 Learn", key=f"learn_document_{document_id}")

        with col2:
            rename_clicked = st.button("✏ Rename", key=f"rename_document_{document_id}")

        with col3:
            delete_clicked = st.button("🗑 Delete", key=f"delete_document_{document_id}")

        return learn_clicked, rename_clicked, delete_clicked

    return False, False, False