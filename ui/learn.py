import json

import streamlit as st

from services.ai_service import generate_ai_response
from services.database_service import get_ai_output, save_ai_output
from services.json_service import extract_json_from_text, is_valid_mcq_json


LEARN_TOOLS = {
    "explain": {
        "title": "🧠 Explain",
        "description": "Understand the document in simple, beginner-friendly language.",
        "button": "Generate Explanation",
    },
    "summary": {
        "title": "📝 Summary",
        "description": "Create exam-ready notes, key points, and quick revision material.",
        "button": "Generate Summary",
    },
    "mcq": {
        "title": "❓ MCQ Quiz",
        "description": "Generate an interactive quiz from your notes.",
        "button": "Generate Quiz",
    },
    "flashcards": {
        "title": "🃏 Flashcards",
        "description": "Create question-answer cards for fast revision.",
        "button": "Generate Flashcards",
    },
    "viva": {
        "title": "🎤 Viva",
        "description": "Prepare for oral exams with viva-style questions and answers.",
        "button": "Generate Viva",
    },
    "resources": {
        "title": "📚 Resources",
        "description": "Get free study resources related to this document.",
        "button": "Generate Resources",
    },
}


def set_active_tool(mode):
    st.session_state["active_learn_tool"] = mode


def load_cached_output(document_id, mode):
    cached = get_ai_output(document_id, mode)

    if cached:
        output_text, provider, created_at = cached
        return output_text, provider, created_at

    return None, None, None


def generate_or_load_output(mode):
    document_id = st.session_state.get("document_id")
    extracted_text = st.session_state.get("extracted_text", "")
    provider = st.session_state.get("selected_provider", "auto")

    if not document_id:
        st.warning("Please select a document from Workspace first.")
        return

    cached_output, cached_provider, created_at = load_cached_output(document_id, mode)

    if cached_output:
        st.session_state["ai_outputs"][mode] = cached_output
        st.session_state["ai_errors"].pop(mode, None)
        st.success(f"✅ Loaded from cache. Provider: {cached_provider}. Created: {created_at}")
        return

    if not extracted_text:
        st.warning("No readable text found for this document.")
        return

    with st.spinner("EduMentor AI is generating your study material..."):
        success, response = generate_ai_response(
            mode,
            extracted_text,
            provider=provider
        )

    if success:
        save_ai_output(
            document_id=document_id,
            mode=mode,
            output_text=response,
            provider=provider
        )

        st.session_state["ai_outputs"][mode] = response
        st.session_state["ai_errors"].pop(mode, None)
        st.success("✅ Generated and saved.")
    else:
        st.session_state["ai_errors"][mode] = response


def render_document_header():
    st.markdown(
        f"""
        <div class="premium-card">
            <div class="card-title">📄 {st.session_state["uploaded_file_name"]}</div>
            <div class="card-text">
                This document is loaded from your Workspace.<br>
                Current AI Provider: <b>{st.session_state["selected_provider"].upper()}</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_tool_grid():
    st.markdown('<div class="section-title">Choose Learning Mode</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    modes = list(LEARN_TOOLS.keys())

    for index, mode in enumerate(modes):
        config = LEARN_TOOLS[mode]

        if index % 3 == 0:
            column = col1
        elif index % 3 == 1:
            column = col2
        else:
            column = col3

        with column:
            st.markdown(
                f"""
                <div class="premium-card">
                    <div class="card-title">{config["title"]}</div>
                    <div class="card-text">{config["description"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(config["title"], key=f"select_learn_tool_{mode}"):
                set_active_tool(mode)
                st.rerun()


def render_mcq_quiz(raw_output):
    data = extract_json_from_text(raw_output)

    if not is_valid_mcq_json(data):
        st.warning("The MCQ output could not be converted into quiz format.")
        st.markdown(raw_output)
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


def render_output(mode):
    if st.session_state["ai_errors"].get(mode):
        st.warning(st.session_state["ai_errors"][mode])

    output = st.session_state["ai_outputs"].get(mode)

    if not output:
        return

    if mode == "mcq":
        render_mcq_quiz(output)
    else:
        st.markdown('<div class="section-title">Generated Output</div>', unsafe_allow_html=True)
        st.markdown(output)


def render_active_tool():
    mode = st.session_state.get("active_learn_tool", "explain")
    config = LEARN_TOOLS[mode]

    st.markdown(
        f"""
        <div class="premium-card">
            <div class="card-title">{config["title"]}</div>
            <div class="card-text">{config["description"]}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(config["button"], key=f"generate_active_tool_{mode}"):
        if mode == "mcq":
            st.session_state["mcq_answers"] = {}
            st.session_state["mcq_submitted"] = False
            st.session_state["mcq_score"] = 0

        generate_or_load_output(mode)

    render_output(mode)


def render_learn_page():
    st.markdown('<div class="hero-title">Learn Hub</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero-subtitle">
            Study your selected document with AI-powered explanation, summary,
            MCQs, flashcards, viva questions, and resources.
        </div>
        """,
        unsafe_allow_html=True
    )

    if "active_learn_tool" not in st.session_state:
        st.session_state["active_learn_tool"] = "explain"

    if not st.session_state.get("document_id") or not st.session_state.get("extracted_text"):
        st.warning("Please go to Workspace, open a unit, choose a document, and click 📚 Learn.")
        return

    render_document_header()
    render_tool_grid()
    render_active_tool()