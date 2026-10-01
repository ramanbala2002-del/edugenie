from ai_client import generate_text


def summarize_text(
    text: str
) -> str:

    prompt = f"""
You are EduGenie, an educational summarization assistant.

Summarize the following educational text.

Requirements:

1. Preserve the main ideas.
2. Preserve important facts.
3. Remove repetition.
4. Use simple language.
5. Do not introduce facts that are not present.
6. Make the result useful for revision.
7. Use headings and bullet points where appropriate.

Educational text:

{text}
"""

    return generate_text(
        prompt,
        temperature=0.25
    )