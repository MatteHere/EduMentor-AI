PROMPTS = {
    "explain": """
You are EduMentor AI, an expert AI tutor for Indian university students.

Create a clear, beginner-friendly explanation using proper Markdown.

Format:
# 📘 Topic Overview
# 🧠 Simple Explanation
# 🔑 Important Concepts
# 📝 Exam Tips
# ⚡ Quick Revision Points
""",

    "summary": """
Create a clean exam-focused summary using proper Markdown.

Format:
# 📝 Short Summary
# 📚 Detailed Summary
# 🔑 Key Points
# 📌 Important Terms
# ⚡ Quick Revision Notes
""",

    "mcq": """
Generate 15 MCQs from the uploaded notes using proper Markdown.

Format:
# ❓ MCQs

## Question 1

**Question:**  

**Options:**  
A)  
B)  
C)  
D)  

**Correct Answer:**  

**Explanation:**  
""",

    "flashcards": """
Create flashcards from the uploaded notes using proper Markdown.

Format:
# 🧠 Flashcards

## Flashcard 1

**Question:**  

**Answer:**  

**Key Point:**  
""",

    "viva": """
Generate viva questions and answers from the uploaded notes using proper Markdown.

Format:
# 🎤 Viva Questions

## Question 1

**Question:**  

**Answer:**  

**Important Point:**  

# 📌 Important Viva Topics
"""
}


def build_prompt(mode, text):
    safe_text = text[:10000]

    return f"""
{PROMPTS[mode]}

Uploaded Notes:
{safe_text}
"""