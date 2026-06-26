PROMPTS = {
    "explain": """
You are EduMentor AI, an expert AI tutor for Indian university students.

Your task is to explain the uploaded notes in a simple, beginner-friendly way.

Return the response in Markdown.

Format:

# 📘 Topic Overview

Brief introduction.

# 🧠 Simple Explanation

Explain every important concept in easy language.

# 🔑 Important Concepts

Use bullet points.

# 📝 Exam Tips

Mention important points for university exams.

# ⚡ Quick Revision

Provide a concise revision summary.
""",

    "summary": """
Create a high-quality exam summary.

Return Markdown only.

Format:

# 📝 Summary

# 📚 Key Concepts

# 📌 Important Definitions

# 🎯 Exam Points

# ⚡ One Minute Revision
""",

    "mcq": """
Generate exactly 10 multiple choice questions.

Return ONLY valid JSON.

Do NOT return Markdown.
Do NOT return explanations outside JSON.

Expected JSON:

{
  "questions": [
    {
      "question": "Question text",
      "options": {
        "A": "Option A",
        "B": "Option B",
        "C": "Option C",
        "D": "Option D"
      },
      "answer": "A",
      "explanation": "Why A is correct."
    }
  ]
}
""",

    "flashcards": """
Generate study flashcards from the uploaded notes.

Return ONLY valid JSON.

Do NOT return Markdown.
Do NOT return explanations outside JSON.

Expected JSON:

{
  "flashcards": [
    {
      "question": "Front side of flashcard",
      "answer": "Back side of flashcard",
      "key_point": "Short revision point"
    }
  ]
}
""",

    "viva": """
Generate exactly 10 viva questions from the uploaded notes.

Return ONLY valid JSON.

Do NOT return Markdown.
Do NOT return explanations outside JSON.

Expected JSON:

{
  "viva_questions": [
    {
      "question": "What is Machine Learning?",
      "answer": "Machine Learning is a subset of AI that enables systems to learn from data.",
      "explanation": "Explain the answer clearly"
    }
  ]
}
""",

    "resources": """
Recommend FREE study resources related to the uploaded document.

Return Markdown.

Include:

# 📚 YouTube Channels

# 🎓 Free Courses

# 🌐 Websites

# 📖 Books

# 💻 Practice Platforms

For every resource, explain why it is useful.
"""
}


def build_prompt(mode, extracted_text):
    extracted_text = extracted_text[:10000]

    return f"""
{PROMPTS[mode]}

Uploaded Notes:

{extracted_text}
"""