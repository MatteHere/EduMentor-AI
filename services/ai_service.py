import time

from services.prompt_service import build_prompt
from services.groq_service import call_groq
from services.gemini_service import call_gemini


MAX_RETRIES = 2


def try_provider(provider_name, prompt):
    for attempt in range(MAX_RETRIES):
        try:
            if provider_name == "groq":
                response = call_groq(prompt)

            elif provider_name == "gemini":
                response = call_gemini(prompt)

            else:
                return False, "Invalid provider selected."

            if response and response.strip():
                return True, response

        except Exception as error:
            print(f"[{provider_name.upper()} Attempt {attempt + 1}] {error}")
            time.sleep(1)

    return False, f"{provider_name} failed after retries."


def generate_ai_response(mode, text, provider="auto"):
    prompt = build_prompt(mode, text)

    if provider == "groq":
        return try_provider("groq", prompt)

    if provider == "gemini":
        return try_provider("gemini", prompt)

    if provider == "auto":
        success, response = try_provider("groq", prompt)

        if success:
            return True, response

        success, response = try_provider("gemini", prompt)

        if success:
            return True, response

    return False, (
        "⚠️ Unable to generate a response.\n\n"
        "All selected AI providers are currently unavailable.\n\n"
        "Please try again in a few moments."
    )