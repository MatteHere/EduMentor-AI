import os
from groq import Groq


GROQ_MODEL = "llama-3.1-8b-instant"


def call_groq(prompt):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env file.")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    return response.choices[0].message.content