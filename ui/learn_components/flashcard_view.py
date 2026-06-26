import streamlit as st


def render_flashcards(data):
    if not data or "flashcards" not in data:
        st.warning("Flashcard data is not available.")
        return

    flashcards = data["flashcards"]

    if "flashcard_index" not in st.session_state:
        st.session_state["flashcard_index"] = 0

    if "flashcard_show_answer" not in st.session_state:
        st.session_state["flashcard_show_answer"] = False

    index = st.session_state["flashcard_index"]
    index = max(0, min(index, len(flashcards) - 1))
    st.session_state["flashcard_index"] = index

    card = flashcards[index]

    st.markdown('<div class="section-title">Interactive Flashcards</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="premium-card">
            <div class="card-title">Card {index + 1} of {len(flashcards)}</div>
            <div class="card-text">
                <b>Question:</b><br>
                {card["question"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("🔄 Flip Card", key="flip_flashcard"):
        st.session_state["flashcard_show_answer"] = not st.session_state["flashcard_show_answer"]
        st.rerun()

    if st.session_state["flashcard_show_answer"]:
        st.markdown(
            f"""
            <div class="premium-card">
                <div class="card-title">Answer</div>
                <div class="card-text">
                    {card["answer"]}<br><br>
                    <b>Key Point:</b> {card["key_point"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⬅ Previous", key="previous_flashcard", disabled=index == 0):
            st.session_state["flashcard_index"] -= 1
            st.session_state["flashcard_show_answer"] = False
            st.rerun()

    with col2:
        if st.button("🔄 Reset", key="reset_flashcards"):
            st.session_state["flashcard_index"] = 0
            st.session_state["flashcard_show_answer"] = False
            st.rerun()

    with col3:
        if st.button("Next ➡", key="next_flashcard", disabled=index == len(flashcards) - 1):
            st.session_state["flashcard_index"] += 1
            st.session_state["flashcard_show_answer"] = False
            st.rerun()