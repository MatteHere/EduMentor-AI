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

    code_block_match = re.search(
        r"```(?:json)?\s*(.*?)```",
        text,
        re.DOTALL | re.IGNORECASE
    )

    if code_block_match:
        try:
            return json.loads(code_block_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    json_match = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)

    if json_match:
        try:
            return json.loads(json_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    return None


def parse_markdown_flashcards(text):
    if not text:
        return None

    cards = []

    blocks = re.split(
        r"(?:^|\n)\s*(?:#{1,6}\s*)?(?:\*\*)?Flashcard\s+\d+(?:\*\*)?\s*",
        text,
        flags=re.IGNORECASE
    )

    for block in blocks:
        block = block.strip()

        if not block:
            continue

        question_match = re.search(
            r"(?:\*\*)?\s*Question\s*:?\s*(?:\*\*)?\s*(.*?)(?=\n\s*(?:\*\*)?\s*Answer\s*:?\s*(?:\*\*)?)",
            block,
            re.DOTALL | re.IGNORECASE
        )

        answer_match = re.search(
            r"(?:\*\*)?\s*Answer\s*:?\s*(?:\*\*)?\s*(.*?)(?=\n\s*(?:\*\*)?\s*Key\s*Point\s*:?\s*(?:\*\*)?|\Z)",
            block,
            re.DOTALL | re.IGNORECASE
        )

        key_point_match = re.search(
            r"(?:\*\*)?\s*Key\s*Point\s*:?\s*(?:\*\*)?\s*(.*)",
            block,
            re.DOTALL | re.IGNORECASE
        )

        if question_match and answer_match:
            question = question_match.group(1).strip()
            answer = answer_match.group(1).strip()
            key_point = key_point_match.group(1).strip() if key_point_match else ""

            if question and answer:
                cards.append({
                    "question": question,
                    "answer": answer,
                    "key_point": key_point
                })

    if not cards:
        return None

    return {"flashcards": cards}


def parse_response(mode, raw_output):
    json_data = extract_json_from_text(raw_output)

    if json_data:
        return json_data

    if mode == "flashcards":
        return parse_markdown_flashcards(raw_output)

    return None