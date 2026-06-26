import re


def parse_mcqs_from_text(text):
    """
    Converts AI-generated MCQ markdown/text into structured quiz questions.

    Expected pattern:
    Question:
    Options:
    A)
    B)
    C)
    D)
    Correct Answer:
    Explanation:
    """

    questions = []

    blocks = re.split(r"##\s*Question\s*\d+|Question\s*\d+[:.)]", text)

    for block in blocks:
        block = block.strip()

        if not block:
            continue

        question_match = re.search(
            r"\*\*Question:\*\*\s*(.*?)(?=\*\*Options:\*\*|Options:)",
            block,
            re.DOTALL | re.IGNORECASE
        )

        options_match = re.search(
            r"(?:\*\*Options:\*\*|Options:)(.*?)(?=\*\*Correct Answer:\*\*|Correct Answer:)",
            block,
            re.DOTALL | re.IGNORECASE
        )

        answer_match = re.search(
            r"(?:\*\*Correct Answer:\*\*|Correct Answer:)\s*([A-D])",
            block,
            re.IGNORECASE
        )

        explanation_match = re.search(
            r"(?:\*\*Explanation:\*\*|Explanation:)\s*(.*)",
            block,
            re.DOTALL | re.IGNORECASE
        )

        if not question_match or not options_match or not answer_match:
            continue

        question_text = question_match.group(1).strip()
        options_text = options_match.group(1).strip()
        correct_answer = answer_match.group(1).upper()
        explanation = explanation_match.group(1).strip() if explanation_match else ""

        options = {}

        for letter in ["A", "B", "C", "D"]:
            option_match = re.search(
                rf"{letter}\)\s*(.*?)(?=\n[A-D]\)|$)",
                options_text,
                re.DOTALL
            )

            if option_match:
                options[letter] = option_match.group(1).strip()

        if question_text and len(options) == 4:
            questions.append({
                "question": question_text,
                "options": options,
                "correct_answer": correct_answer,
                "explanation": explanation
            })

    return questions


def initialize_quiz_state(mode_key, questions):
    if mode_key not in questions:
        return

    return {
        "questions": questions,
        "current_index": 0,
        "answers": {},
        "submitted": False,
        "score": 0
    }


def calculate_quiz_score(questions, answers):
    score = 0

    for index, question in enumerate(questions):
        selected_answer = answers.get(index)

        if selected_answer == question["correct_answer"]:
            score += 1

    return score