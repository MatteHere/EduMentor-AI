import streamlit as st


def render_viva_questions(data):
    if not data or "viva_questions" not in data:
        st.warning("Viva data is not available.")
        return

    viva_questions = data["viva_questions"]

    if "viva_index" not in st.session_state:
        st.session_state["viva_index"] = 0

    if "viva_show_answer" not in st.session_state:
        st.session_state["viva_show_answer"] = False

    index = st.session_state["viva_index"]
    index = max(0, min(index, len(viva_questions) - 1))
    st.session_state["viva_index"] = index

    viva = viva_questions[index]

    st.markdown(
        '<div class="section-title">🎤 Interactive Viva Practice</div>',
        unsafe_allow_html=True,
    )

    st.markdown(f"## Question {index + 1}")

    st.info(viva["question"])

    if st.button("👁 Reveal Answer", key="reveal_viva_answer"):
        st.session_state["viva_show_answer"] = not st.session_state["viva_show_answer"]
        st.rerun()

    if st.session_state["viva_show_answer"]:

        st.markdown("### ✅ Answer")

        st.success(viva["answer"])

        st.markdown("### 💡 Explanation")

        st.markdown(viva["explanation"])

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(
            "⬅ Previous",
            disabled=index == 0,
            key="previous_viva",
        ):
            st.session_state["viva_index"] -= 1
            st.session_state["viva_show_answer"] = False
            st.rerun()

    with col2:
        if st.button("🔄 Reset", key="reset_viva"):
            st.session_state["viva_index"] = 0
            st.session_state["viva_show_answer"] = False
            st.rerun()

    with col3:
        if st.button(
            "Next ➡",
            disabled=index == len(viva_questions) - 1,
            key="next_viva",
        ):
            st.session_state["viva_index"] += 1
            st.session_state["viva_show_answer"] = False
            st.rerun()