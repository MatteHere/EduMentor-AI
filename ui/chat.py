import streamlit as st

from services.chat_service import generate_chat_response


SUGGESTED_PROMPTS = [
    "Explain this document in simple language.",
    "Summarize this document for exam revision.",
    "Give me important viva questions from this document.",
    "Explain this like I am 10 years old.",
    "Give me real-life examples related to this topic.",
    "Create 5 important exam questions from this document.",
]


def initialize_chat_state():
    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = []

    if "selected_suggested_prompt" not in st.session_state:
        st.session_state["selected_suggested_prompt"] = ""


def send_chat_message(user_question):
    document_text = st.session_state.get("extracted_text", "")
    provider = st.session_state.get("selected_provider", "auto")

    if not user_question.strip():
        return

    st.session_state["chat_messages"].append(
        {
            "role": "user",
            "content": user_question,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner("EduMentor AI is thinking..."):
            success, response = generate_chat_response(
                document_text=document_text,
                user_question=user_question,
                chat_history=st.session_state["chat_messages"],
                provider=provider,
            )

        if success:
            st.markdown(response)
            st.session_state["chat_messages"].append(
                {
                    "role": "assistant",
                    "content": response,
                }
            )
        else:
            st.warning(response)


def render_document_header(document_name, provider):
    st.markdown(
        f"""
        <div class="premium-card">
            <div class="card-title">💬 Chat with Notes</div>
            <div class="card-text">
                <b>Document:</b> {document_name}<br>
                <b>AI Provider:</b> {provider.upper()}<br><br>
                Ask questions directly from your uploaded study material.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_suggested_prompts():
    st.markdown('<div class="section-title">Suggested Questions</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    for index, prompt in enumerate(SUGGESTED_PROMPTS):
        column = [col1, col2, col3][index % 3]

        with column:
            if st.button(prompt, key=f"suggested_prompt_{index}"):
                send_chat_message(prompt)
                st.rerun()


def render_chat_messages():
    for message in st.session_state["chat_messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def render_chat_page():
    initialize_chat_state()

    st.markdown('<div class="hero-title">AI Chat</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero-subtitle">
            Ask questions, get explanations, examples, viva questions, and exam-focused answers from your uploaded notes.
        </div>
        """,
        unsafe_allow_html=True,
    )

    document_text = st.session_state.get("extracted_text", "")
    document_name = st.session_state.get("uploaded_file_name", "")
    provider = st.session_state.get("selected_provider", "auto")

    if not st.session_state.get("document_id") or not document_text:
        st.warning("Please open a document from Workspace and click 📚 Learn first.")
        return

    render_document_header(document_name, provider)

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("🧹 Clear Chat"):
            st.session_state["chat_messages"] = []
            st.rerun()

    with col2:
        st.caption("Tip: Use suggested prompts for faster studying.")

    render_suggested_prompts()

    st.markdown('<div class="section-title">Conversation</div>', unsafe_allow_html=True)

    render_chat_messages()

    user_question = st.chat_input("Ask anything about your notes...")

    if user_question:
        send_chat_message(user_question)