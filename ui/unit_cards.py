import streamlit as st


def render_unit_card(unit):
    unit_id, unit_name, created_at = unit

    with st.expander(f"📄 {unit_name}", expanded=False):
        st.markdown(
            f"""
            <div class="card-text">
                <b>Created:</b> {created_at}
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            open_clicked = st.button("📂 Open", key=f"open_unit_{unit_id}")

        with col2:
            edit_clicked = st.button("✏ Edit", key=f"edit_unit_{unit_id}")

        with col3:
            delete_clicked = st.button("🗑 Delete", key=f"delete_unit_{unit_id}")

        return open_clicked, edit_clicked, delete_clicked

    return False, False, False