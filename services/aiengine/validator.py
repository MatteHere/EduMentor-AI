def validate_mcq_data(data):
    if not isinstance(data, dict):
        return False

    questions = data.get("questions")

    if not isinstance(questions, list) or not questions:
        return False

    for question in questions:
        if not isinstance(question, dict):
            return False

        required_keys = ["question", "options", "answer", "explanation"]

        for key in required_keys:
            if key not in question:
                return False

        options = question["options"]

        if not isinstance(options, dict):
            return False

        for option_key in ["A", "B", "C", "D"]:
            if option_key not in options:
                return False

        if question["answer"] not in ["A", "B", "C", "D"]:
            return False

    return True


def validate_flashcard_data(data):
    if not isinstance(data, dict):
        return False

    flashcards = data.get("flashcards")

    if not isinstance(flashcards, list) or not flashcards:
        return False

    for card in flashcards:
        if not isinstance(card, dict):
            return False

        required_keys = ["question", "answer", "key_point"]

        for key in required_keys:
            if key not in card:
                return False

    return True


def validate_viva_data(data):
    if not isinstance(data, dict):
        return False

    viva_questions = data.get("viva_questions")

    if not isinstance(viva_questions, list) or not viva_questions:
        return False

    for viva in viva_questions:
        if not isinstance(viva, dict):
            return False

        required_keys = ["question", "answer", "explanation"]

        for key in required_keys:
            if key not in viva:
                return False

    return True


def validate_structured_data(mode, data):
    if mode == "mcq":
        return validate_mcq_data(data)

    if mode == "flashcards":
        return validate_flashcard_data(data)

    if mode == "viva":
        return validate_viva_data(data)

    return True