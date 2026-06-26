from services.provider_manager import get_default_provider
from services.ai_service import generate_ai_response

from services.aiengine.parser import parse_response
from services.aiengine.validator import validate_structured_data
from services.aiengine.cache import (
    load_cached_response,
    save_response_to_cache,
)


STRUCTURED_MODES = ["mcq", "flashcards", "viva"]


def build_retry_text(mode, extracted_text):
    if mode == "flashcards":
        return f"""
Your previous response was invalid.

Return ONLY valid JSON.
Do not include Markdown.
Do not include explanations outside JSON.

Required JSON schema:

{{
  "flashcards": [
    {{
      "question": "Question text",
      "answer": "Answer text",
      "key_point": "Short revision point"
    }}
  ]
}}

Uploaded Notes:
{extracted_text[:10000]}
"""

    if mode == "mcq":
        return f"""
Your previous response was invalid.

Return ONLY valid JSON.
Do not include Markdown.
Do not include explanations outside JSON.

Required JSON schema:

{{
  "questions": [
    {{
      "question": "Question text",
      "options": {{
        "A": "Option A",
        "B": "Option B",
        "C": "Option C",
        "D": "Option D"
      }},
      "answer": "A",
      "explanation": "Why the answer is correct"
    }}
  ]
}}

Uploaded Notes:
{extracted_text[:10000]}
"""

    return extracted_text


class AIEngine:

    @staticmethod
    def generate(
        mode,
        document_id,
        extracted_text,
        provider=None,
        use_cache=True,
    ):
        if provider is None:
            provider = get_default_provider()

        if use_cache:
            cached = load_cached_response(document_id, mode)

            if cached:
                structured = parse_response(mode, cached["output"])

                if mode in STRUCTURED_MODES:
                    if structured is not None and validate_structured_data(mode, structured):
                        return {
                            "success": True,
                            "cached": True,
                            "provider": cached["provider"],
                            "raw": cached["output"],
                            "structured": structured,
                        }

                else:
                    return {
                        "success": True,
                        "cached": True,
                        "provider": cached["provider"],
                        "raw": cached["output"],
                        "structured": structured,
                    }

        success, response = generate_ai_response(
            mode,
            extracted_text,
            provider=provider,
        )

        if not success:
            return {
                "success": False,
                "cached": False,
                "error": response,
            }

        structured = parse_response(mode, response)

        if mode in STRUCTURED_MODES:
            if structured is None or not validate_structured_data(mode, structured):
                retry_text = build_retry_text(mode, extracted_text)

                success, response = generate_ai_response(
                    mode,
                    retry_text,
                    provider=provider,
                )

                if not success:
                    return {
                        "success": False,
                        "cached": False,
                        "error": response,
                    }

                structured = parse_response(mode, response)

                if structured is None or not validate_structured_data(mode, structured):
                    return {
                        "success": True,
                        "cached": False,
                        "provider": provider,
                        "raw": response,
                        "structured": None,
                    }

        save_response_to_cache(
            document_id=document_id,
            mode=mode,
            output_text=response,
            provider=provider,
        )

        return {
            "success": True,
            "cached": False,
            "provider": provider,
            "raw": response,
            "structured": structured,
        }