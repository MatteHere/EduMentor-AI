import streamlit as st


def render_mcq_quiz(data):
    if not data or "questions" not in data:
        st.warning("MCQ data is not available.")
        return

    questions = data["questions"]

    st.markdown('<div class="section-title">Interactive MCQ Quiz</div>', unsafe_allow_html=True)

    if "mcq_answers" not in st.session_state:
        st.session_state["mcq_answers"] = {}

    if "mcq_submitted" not in st.session_state:
        st.session_state["mcq_submitted"] = False

    if st.button("🔄 Reset Quiz", key="reset_mcq_quiz"):
        st.session_state["mcq_answers"] = {}
        st.session_state["mcq_submitted"] = False
        st.session_state["mcq_score"] = 0
        st.rerun()

    for index, question in enumerate(questions):
        st.markdown(
            f"""
            <div class="premium-card">
                <div class="card-title">Question {index + 1}</div>
                <div class="card-text">{question["question"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        selected = st.radio(
            "Choose your answer",
            ["A", "B", "C", "D"],
            format_func=lambda option: f"{option}) {question['options'][option]}",
            key=f"mcq_question_{index}",
            index=None,
            disabled=st.session_state["mcq_submitted"]
        )

        if selected:
            st.session_state["mcq_answers"][index] = selected

        if st.session_state["mcq_submitted"]:
            correct_answer = question["answer"]
            user_answer = st.session_state["mcq_answers"].get(index)

            if user_answer == correct_answer:
                st.success(f"✅ Correct Answer: {correct_answer}")
            else:
                st.error(f"❌ Your Answer: {user_answer or 'Not answered'} | Correct Answer: {correct_answer}")

            st.info(question["explanation"])

    if not st.session_state["mcq_submitted"]:
        if st.button("✅ Submit Quiz", key="submit_mcq_quiz"):
            score = 0

            for index, question in enumerate(questions):
                if st.session_state["mcq_answers"].get(index) == question["answer"]:
                    score += 1

            st.session_state["mcq_score"] = score
            st.session_state["mcq_submitted"] = True
            st.rerun()

    if st.session_state["mcq_submitted"]:
        score = st.session_state.get("mcq_score", 0)
        total = len(questions)

        st.markdown(
            f"""
            <div class="premium-card">
                <div class="card-title">🏆 Final Score</div>
                <div class="card-text">
                    You scored <b>{score} / {total}</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )