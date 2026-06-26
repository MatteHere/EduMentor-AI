import streamlit as st

from ui.workspace_view import render_workspace_view
from ui.subject_view import render_subject_view
from ui.unit_view import render_unit_view
from ui.document_view import render_document_view


def render_breadcrumb():
    parts = []

    if st.session_state.get("workspace_name"):
        parts.append(f"🎓 {st.session_state['workspace_name']}")

    if st.session_state.get("subject_name"):
        parts.append(f"📘 {st.session_state['subject_name']}")

    if st.session_state.get("unit_name"):
        parts.append(f"📄 {st.session_state['unit_name']}")

    if parts:
        st.markdown(
            f"""
            <div style="color:#475569;font-size:16px;margin-bottom:20px;">
                {" &nbsp; > &nbsp; ".join(parts)}
            </div>
            """,
            unsafe_allow_html=True
        )


def render_workspace_page():
    if st.session_state.get("unit_id"):
        render_document_view(render_breadcrumb)

    elif st.session_state.get("subject_id"):
        render_unit_view(render_breadcrumb)

    elif st.session_state.get("workspace_id"):
        render_subject_view(render_breadcrumb)

    else:
        render_workspace_view()