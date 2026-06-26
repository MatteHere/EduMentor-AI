import streamlit as st

from services.database_service import get_units
from ui.unit_cards import render_unit_card
from ui.unit_dialogs import (
    render_create_unit_dialog,
    render_edit_unit_dialog,
    render_delete_unit_confirmation,
)


def open_unit(unit_id, unit_name):
    st.session_state["unit_id"] = unit_id
    st.session_state["unit_name"] = unit_name


def render_unit_view(render_breadcrumb):
    st.markdown(
        f'<div class="hero-title">{st.session_state["subject_name"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-subtitle">
            Manage units inside this subject.
        </div>
        """,
        unsafe_allow_html=True
    )

    render_breadcrumb()

    if st.button("⬅ Back to Subjects"):
        st.session_state["subject_id"] = None
        st.session_state["subject_name"] = ""
        st.session_state["unit_id"] = None
        st.session_state["unit_name"] = ""
        st.rerun()

    render_create_unit_dialog(st.session_state["subject_id"])

    units = get_units(st.session_state["subject_id"])

    if not units:
        st.info("No units found. Add your first unit.")
        return

    st.markdown('<div class="section-title">Units</div>', unsafe_allow_html=True)

    for unit in units:
        unit_id, unit_name, created_at = unit

        open_clicked, edit_clicked, delete_clicked = render_unit_card(unit)

        if open_clicked:
            open_unit(unit_id, unit_name)
            st.rerun()

        if edit_clicked:
            st.session_state["edit_unit_id"] = unit_id

        if st.session_state.get("edit_unit_id") == unit_id:
            render_edit_unit_dialog(unit_id, unit_name)

        if delete_clicked:
            st.session_state["delete_unit_id"] = unit_id
            st.session_state["delete_unit_name"] = unit_name

        if st.session_state.get("delete_unit_id") == unit_id:
            render_delete_unit_confirmation(unit_id, unit_name)