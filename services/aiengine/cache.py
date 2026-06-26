from services.database_service import get_ai_output, save_ai_output


def load_cached_response(document_id, mode):
    cached = get_ai_output(document_id, mode)

    if not cached:
        return None

    output_text, provider, created_at = cached

    return {
        "output": output_text,
        "provider": provider,
        "created_at": created_at,
    }


def save_response_to_cache(document_id, mode, output_text, provider):
    save_ai_output(
        document_id=document_id,
        mode=mode,
        output_text=output_text,
        provider=provider,
    )