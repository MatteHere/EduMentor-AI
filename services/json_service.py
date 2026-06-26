import json
import re


def extract_json_from_text(text):
    """
    Extract JSON from an AI response.

    Handles:
    - pure JSON
    - JSON inside ```json blocks
    - JSON mixed with explanation text
    """

    if not text:
        return None

    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    code_block_match = re.search(
        r"```(?:json)?\s*(.*?)```",
        text,
        re.DOTALL | re.IGNORECASE
    )

    if code_block_match:
        json_text = code_block_match.group(1).strip()

        try:
            return json.loads(json_text)
        except json.JSONDecodeError:
            pass

    object_match = re.search(
        r"(\{.*\}|\[.*\])",
        text,
        re.DOTALL
    )

    if object_match:
        json_text = object_match.group(1).strip()

        try:
            return json.loads(json_text)
        except json.JSONDecodeError:
            pass

    return None


def is_valid_mcq_json(data):
    if not isinstance(data, dict):
        return False

    questions = data.get("questions")

    if not isinstance(questions, list) or len(questions) == 0:
        return False

    for question in questions:
        if not isinstance(question, dict):
            return False

        if "question" not in question:
            return False

        if "options" not in question:
            return False

        if "answer" not in question:
            return False

        if "explanation" not in question:
            return False

        options = question["options"]

        if not isinstance(options, dict):
            return False

        for key in ["A", "B", "C", "D"]:
            if key not in options:
                return False

        if question["answer"] not in ["A", "B", "C", "D"]:
            return False

    return True