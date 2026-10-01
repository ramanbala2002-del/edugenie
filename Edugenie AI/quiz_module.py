from ai_client import (
    generate_text,
    parse_json_response
)


def generate_quiz(
    source_text: str
) -> list[dict]:

    prompt = f"""
You are EduGenie, an educational quiz generator.

Create exactly 3 multiple-choice questions.

Base the questions ONLY on the following topic or text:

{source_text}

Return ONLY valid JSON.

Required JSON format:

[
  {{
    "question": "Question text",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "correct_answer": "Exact correct option",
    "explanation": "Short explanation"
  }}
]

Rules:

1. Exactly 3 questions.
2. Exactly 4 options per question.
3. Only one correct answer.
4. correct_answer must exactly match one option.
5. Make distractors plausible.
6. Do not include Markdown.
7. Do not include anything outside the JSON.
"""

    raw_response = generate_text(
        prompt,
        temperature=0.2
    )

    data = parse_json_response(
        raw_response
    )

    # -----------------------------------------------------
    # Handle {"questions": [...]}
    # -----------------------------------------------------

    if isinstance(data, dict):

        data = data.get(
            "questions",
            []
        )

    # -----------------------------------------------------
    # Validate
    # -----------------------------------------------------

    if not isinstance(data, list):

        raise ValueError(
            "Quiz response must be a list."
        )

    if len(data) != 3:

        raise ValueError(
            "Quiz must contain exactly 3 questions."
        )

    final_questions = []

    for item in data:

        if not isinstance(item, dict):

            raise ValueError(
                "Invalid quiz question."
            )

        question = item.get(
            "question"
        )

        options = item.get(
            "options"
        )

        correct_answer = item.get(
            "correct_answer"
        )

        explanation = item.get(
            "explanation",
            ""
        )

        if not question:

            raise ValueError(
                "Quiz question is missing."
            )

        if (
            not isinstance(options, list)
            or len(options) != 4
        ):

            raise ValueError(
                "Every quiz question must have 4 options."
            )

        if correct_answer not in options:

            raise ValueError(
                "Correct answer must match an option."
            )

        final_questions.append(
            {
                "question": str(question),
                "options": [
                    str(option)
                    for option in options
                ],
                "correct_answer": str(
                    correct_answer
                ),
                "explanation": str(
                    explanation
                )
            }
        )

    return final_questions