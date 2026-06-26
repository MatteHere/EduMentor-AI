def is_valid_flashcard_json(data):
    if not isinstance(data, dict):
        return False

    flashcards = data.get("flashcards")

    if not isinstance(flashcards, list) or len(flashcards) == 0:
        return False

    for card in flashcards:
        if not isinstance(card, dict):
            return False

        if "question" not in card:
            return False

        if "answer" not in card:
            return False

        if "key_point" not in card:
            return False

    return True