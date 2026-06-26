AI_PROVIDERS = {
    "auto": "Auto - Groq first, Gemini fallback",
    "groq": "Groq - Fast mode",
    "gemini": "Gemini - Backup mode",
}


DEFAULT_PROVIDER = "auto"


def get_available_providers():
    return AI_PROVIDERS


def get_default_provider():
    return DEFAULT_PROVIDER