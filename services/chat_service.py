from services.provider_manager import get_default_provider
from services.groq_service import call_groq
from services.gemini_service import call_gemini


def build_chat_prompt(document_text, user_question, chat_history=None):
    chat_history = chat_history or []

    history_text = ""

    for message in chat_history[-6:]:
        role = message.get("role", "user")
        content = message.get("content", "")
        history_text += f"{role.upper()}: {content}\n"

    return f"""
You are EduMentor AI, an expert tutor.

Answer the student's question using ONLY the uploaded notes below.
If the answer is not available in the notes, say:
"I could not find this clearly in the uploaded notes."

Be simple, clear, exam-focused, and helpful.

Uploaded Notes:
{document_text[:12000]}

Previous Conversation:
{history_text}

Student Question:
{user_question}

Answer:
"""


def call_provider(prompt, provider):
    if provider == "groq":
        return call_groq(prompt)

    if provider == "gemini":
        return call_gemini(prompt)

    if provider == "auto":
        try:
            return call_groq(prompt)
        except Exception:
            return call_gemini(prompt)

    return call_groq(prompt)


def generate_chat_response(document_text, user_question, chat_history=None, provider=None):
    if provider is None:
        provider = get_default_provider()

    prompt = build_chat_prompt(
        document_text=document_text,
        user_question=user_question,
        chat_history=chat_history
    )

    try:
        response = call_provider(prompt, provider)

        if response and response.strip():
            return True, response

        return False, "No response generated."

    except Exception as error:
        return False, f"Chat response failed: {error}"