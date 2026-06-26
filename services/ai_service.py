import time

from services.prompt_service import build_prompt
from services.groq_service import call_groq
from services.gemini_service import call_gemini


MAX_RETRIES = 2


def generate_ai_response(mode, text):
    """
    Main AI Router

    Priority:
    1. Groq
    2. Gemini
    """

    prompt = build_prompt(mode, text)

    # -------------------------
    # Try Groq First
    # -------------------------
    for attempt in range(MAX_RETRIES):
        try:
            response = call_groq(prompt)

            if response and response.strip():
                return True, response

        except Exception as error:
            print(f"[Groq Attempt {attempt+1}] {error}")
            time.sleep(1)

    # -------------------------
    # Gemini Fallback
    # -------------------------
    for attempt in range(MAX_RETRIES):
        try:
            response = call_gemini(prompt)

            if response and response.strip():
                return True, response

        except Exception as error:
            print(f"[Gemini Attempt {attempt+1}] {error}")
            time.sleep(1)

    return False, (
        "⚠️ Unable to generate a response.\n\n"
        "Both AI providers are currently unavailable.\n\n"
        "Please try again in a few moments."
    )