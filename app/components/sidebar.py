import streamlit as st

from ..config.theme import SIDEBAR_TITLE, SIDEBAR_SUBTITLE, NAVIGATION_ITEMS


def show_sidebar():
    st.sidebar.markdown(f"## 🎓 {SIDEBAR_TITLE}")
    st.sidebar.markdown(SIDEBAR_SUBTITLE)
    st.sidebar.divider()

    selected_page = st.sidebar.radio(
        "Navigation",
        NAVIGATION_ITEMS
    )

    st.sidebar.divider()
    st.sidebar.info(
        "Built for Indian university students, starting with SPPU and AI & DS."
    )

    return selected_page