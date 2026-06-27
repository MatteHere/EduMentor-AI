import streamlit as st
from datetime import date


def render_planner_page():
    st.markdown('<div class="hero-title">Study Planner</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero-subtitle">
            Create a simple study plan for your upcoming exams.
        </div>
        """,
        unsafe_allow_html=True,
    )

    exam_date = st.date_input("Exam Date", min_value=date.today())
    study_hours = st.number_input("Study Hours Per Day", min_value=1, max_value=12, value=3)

    subjects = st.text_area(
        "Subjects / Topics",
        placeholder="Example:\nComputer Organization\nDBMS\nPython\nMathematics"
    )

    if st.button("Generate Study Plan"):
        if not subjects.strip():
            st.warning("Please enter at least one subject or topic.")
            return

        subject_list = [s.strip() for s in subjects.split("\n") if s.strip()]
        days_left = max((exam_date - date.today()).days, 1)

        st.markdown('<div class="section-title">Your Study Plan</div>', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="premium-card">
                <div class="card-title">📅 Plan Summary</div>
                <div class="card-text">
                    Exam Date: <b>{exam_date}</b><br>
                    Days Left: <b>{days_left}</b><br>
                    Study Time: <b>{study_hours} hours/day</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for index, subject in enumerate(subject_list, start=1):
            st.markdown(
                f"""
                <div class="premium-card">
                    <div class="card-title">Day {index}: {subject}</div>
                    <div class="card-text">
                        • Read notes<br>
                        • Generate summary in Learn Hub<br>
                        • Practice MCQs<br>
                        • Revise using flashcards<br>
                        • Practice viva questions
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )