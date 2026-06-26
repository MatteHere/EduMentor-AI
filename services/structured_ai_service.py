import json
import re


def extract_json_from_text(text):
    if not text:
        return None

    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    code_block = re.search(
        r"```(?:json)?\s*(.*?)```",
        text,
        re.DOTALL | re.IGNORECASE
    )

    if code_block:
        try:
            return json.loads(code_block.group(1).strip())
        except json.JSONDecodeError:
            pass

    json_match = re.search(
        r"(\{.*\}|\[.*\])",
        text,
        re.DOTALL
    )

    if json_match:
        try:
            return json.loads(json_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    return None


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


def parse_structured_response(mode, raw_output):
    data = extract_json_from_text(raw_output)

    if mode == "mcq":
        if validate_mcq_data(data):
            return True, data
        return False, None

    if mode == "flashcards":
        if validate_flashcard_data(data):
            return True, data
        return False, None

    return False, None