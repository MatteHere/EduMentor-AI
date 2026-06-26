import streamlit as st


def render_workspace_card(workspace):
    workspace_id, name, university, stream, semester, created_at = workspace

    with st.expander(f"🎓 {name}", expanded=False):
        st.markdown(
            f"""
            <div class="card-text">
                {university or "University not specified"} • {stream or "Stream not specified"}<br>
                {semester or "Semester not specified"}<br><br>
                <b>Created:</b> {created_at}
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            open_clicked = st.button("📂 Open", key=f"open_workspace_{workspace_id}")

        with col2:
            edit_clicked = st.button("✏ Edit", key=f"edit_workspace_{workspace_id}")

        with col3:
            delete_clicked = st.button("🗑 Delete", key=f"delete_workspace_{workspace_id}")

        return open_clicked, edit_clicked, delete_clicked

    return False, False, False


def render_subject_card(subject, workspace_name):
    subject_id, subject_name, created_at = subject

    with st.expander(f"📘 {subject_name}", expanded=False):
        st.markdown(
            f"""
            <div class="card-text">
                Subject inside <b>{workspace_name}</b><br><br>
                <b>Created:</b> {created_at}
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            open_clicked = st.button("📂 Open", key=f"open_subject_{subject_id}")

        with col2:
            edit_clicked = st.button("✏ Edit", key=f"edit_subject_{subject_id}")

        with col3:
            delete_clicked = st.button("🗑 Delete", key=f"delete_subject_{subject_id}")

        return open_clicked, edit_clicked, delete_clicked

    return False, False, False