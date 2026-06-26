import streamlit as st

from services.aiengine.engine import AIEngine
from services.aiengine.parser import parse_response

from ui.learn_components.mcq_view import render_mcq_quiz
from ui.learn_components.flashcard_view import render_flashcards
from ui.learn_components.viva_view import render_viva_questions


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
        "description": "Create interactive question-answer revision cards.",
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
        unsafe_allow_html=True,
    )


def render_tool_grid():
    st.markdown(
        '<div class="section-title">Choose Learning Mode</div>',
        unsafe_allow_html=True,
    )

    columns = st.columns(3)
    modes = list(LEARN_TOOLS.keys())

    for index, mode in enumerate(modes):
        config = LEARN_TOOLS[mode]
        column = columns[index % 3]

        with column:
            st.markdown(
                f"""
                <div class="premium-card">
                    <div class="card-title">{config["title"]}</div>
                    <div class="card-text">{config["description"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(config["title"], key=f"select_learn_tool_{mode}"):
                set_active_tool(mode)
                st.rerun()


def reset_interactive_state(mode):
    if mode == "mcq":
        st.session_state["mcq_answers"] = {}
        st.session_state["mcq_submitted"] = False
        st.session_state["mcq_score"] = 0

    if mode == "flashcards":
        st.session_state["flashcard_index"] = 0
        st.session_state["flashcard_show_answer"] = False

    if mode == "viva":
        st.session_state["viva_index"] = 0
        st.session_state["viva_show_answer"] = False


def generate_with_engine(mode):
    document_id = st.session_state.get("document_id")
    extracted_text = st.session_state.get("extracted_text", "")
    provider = st.session_state.get("selected_provider", "auto")

    if not document_id:
        st.warning("Please select a document from Workspace first.")
        return

    if not extracted_text:
        st.warning("No readable text found for this document.")
        return

    reset_interactive_state(mode)

    with st.spinner("EduMentor AI is preparing your learning material..."):
        result = AIEngine.generate(
            mode=mode,
            document_id=document_id,
            extracted_text=extracted_text,
            provider=provider,
            use_cache=True,
        )

    if not result.get("success"):
        st.session_state["ai_errors"][mode] = result.get(
            "error",
            "Something went wrong while generating content.",
        )
        return

    st.session_state["ai_errors"].pop(mode, None)

    st.session_state["ai_outputs"][mode] = {
        "raw": result.get("raw"),
        "structured": result.get("structured"),
        "cached": result.get("cached"),
        "provider": result.get("provider"),
    }

    if result.get("cached"):
        st.success(f"✅ Loaded from cache. Provider: {result.get('provider')}")
    else:
        st.success(f"✅ Generated and saved. Provider: {result.get('provider')}")


def render_generated_output(mode):
    error = st.session_state["ai_errors"].get(mode)

    if error:
        st.warning(error)
        return

    output = st.session_state["ai_outputs"].get(mode)

    if not output:
        return

    raw = output.get("raw")
    structured = output.get("structured")

    if mode == "mcq":
        mcq_data = structured

        if mcq_data is None:
            mcq_data = parse_response("mcq", raw)

        if mcq_data:
            render_mcq_quiz(mcq_data)
        else:
            st.warning("MCQ data could not be converted into interactive quiz format.")
            st.markdown(raw)

        return

    if mode == "flashcards":
        flashcard_data = structured

        if flashcard_data is None:
            flashcard_data = parse_response("flashcards", raw)

        if flashcard_data:
            render_flashcards(flashcard_data)
        else:
            st.warning("Flashcard data could not be converted into interactive format.")
            st.markdown(raw)

        return

    if mode == "viva":
        viva_data = structured

        if viva_data is None:
            viva_data = parse_response("viva", raw)

        if viva_data:
            render_viva_questions(viva_data)
        else:
            st.warning("Viva data could not be converted into interactive format.")
            st.markdown(raw)

        return

    st.markdown(
        '<div class="section-title">Generated Output</div>',
        unsafe_allow_html=True,
    )
    st.markdown(raw)


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
        unsafe_allow_html=True,
    )

    if st.button(config["button"], key=f"generate_active_tool_{mode}"):
        generate_with_engine(mode)

    render_generated_output(mode)


def render_learn_page():
    st.markdown('<div class="hero-title">Learn Hub</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero-subtitle">
            Study your selected document with AI-powered explanation, summary,
            MCQs, flashcards, viva questions, and resources.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "active_learn_tool" not in st.session_state:
        st.session_state["active_learn_tool"] = "explain"

    if "ai_outputs" not in st.session_state:
        st.session_state["ai_outputs"] = {}

    if "ai_errors" not in st.session_state:
        st.session_state["ai_errors"] = {}

    if not st.session_state.get("document_id") or not st.session_state.get("extracted_text"):
        st.warning("Please go to Workspace, open a unit, choose a document, and click 📚 Learn.")
        return

    render_document_header()
    render_tool_grid()
    render_active_tool()