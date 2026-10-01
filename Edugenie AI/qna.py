"""
EduGenie - Question & Answer Module
"""

from ai_client import generate_text


def answer_question_with_gemini(question: str, level: str = "beginner") -> str:
    """
    Answer a student's question using Gemini.
    """

    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty.")

    prompt = f"""
You are EduGenie, an AI learning assistant.

Answer the following question for a {level}-level student.

Question:
{question}

Instructions:
- Give a clear and accurate answer.
- Explain the concept in simple language.
- Use examples when helpful.
- Break complicated ideas into smaller points.
- Use bullet points when appropriate.
- Avoid unnecessary technical jargon.
- Do not make up facts.
- Keep the answer educational and easy to understand.

Answer the question now.
"""

    return generate_text(prompt)