import streamlit as st

from services.database_service import (
    create_unit,
    update_unit,
    delete_unit,
)


def render_create_unit_dialog(subject_id):
    with st.expander("➕ Add Unit", expanded=False):
        unit_name = st.text_input(
            "Unit Name",
            placeholder="Example: Unit 1 - Introduction",
            key="new_unit_name"
        )

        if st.button("Create Unit", key="create_unit_button"):
            if not unit_name.strip():
                st.warning("Please enter a unit name.")
                return

            unit_id = create_unit(subject_id, unit_name.strip())

            st.session_state["unit_id"] = unit_id
            st.session_state["unit_name"] = unit_name.strip()

            st.success("✅ Unit created successfully!")
            st.rerun()


def render_edit_unit_dialog(unit_id, current_name):
    with st.expander("✏ Edit Unit", expanded=True):
        updated_name = st.text_input(
            "Unit Name",
            value=current_name,
            key=f"edit_unit_name_{unit_id}"
        )

        if st.button("Save Unit", key=f"save_unit_{unit_id}"):
            if not updated_name.strip():
                st.warning("Unit name cannot be empty.")
                return

            update_unit(unit_id, updated_name.strip())

            st.session_state["unit_name"] = updated_name.strip()
            st.session_state["edit_unit_id"] = None

            st.success("✅ Unit updated successfully!")
            st.rerun()


def render_delete_unit_confirmation(unit_id, unit_name):
    st.warning(f"⚠️ Are you sure you want to delete unit: **{unit_name}**?")

    st.markdown(
        """
        This will permanently delete:
        - Documents
        - AI outputs
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Cancel", key=f"cancel_delete_unit_{unit_id}"):
            st.session_state["delete_unit_id"] = None
            st.session_state["delete_unit_name"] = ""
            st.rerun()

    with col2:
        if st.button("🗑 Delete Unit", key=f"confirm_delete_unit_{unit_id}"):
            delete_unit(unit_id)

            st.session_state["unit_id"] = None
            st.session_state["unit_name"] = ""
            st.session_state["delete_unit_id"] = None
            st.session_state["delete_unit_name"] = ""

            st.success("Unit deleted successfully.")
            st.rerun()