import os
from functools import lru_cache

from ai_client import generate_text


# ---------------------------------------------------------
# Optional local model
# ---------------------------------------------------------

@lru_cache(maxsize=1)
def get_local_pipeline():

    from transformers import pipeline

    model_name = os.getenv(
        "LOCAL_EXPLANATION_MODEL",
        "MBZUAI/LaMini-Flan-T5-783M"
    )

    return pipeline(
        "text2text-generation",
        model=model_name,
        device=-1
    )


# ---------------------------------------------------------
# Explain concept
# ---------------------------------------------------------

def explain_topic(
    topic: str,
    level: str = "beginner"
) -> str:

    allowed_levels = {
        "beginner",
        "intermediate",
        "advanced"
    }

    if level not in allowed_levels:

        level = "beginner"

    use_local = os.getenv(
        "USE_LOCAL_EXPLANATION_MODEL",
        "false"
    ).lower() == "true"

    # -----------------------------------------------------
    # Local LaMini model
    # -----------------------------------------------------

    if use_local:

        try:

            model = get_local_pipeline()

            prompt = (
                f"Explain {topic} to a {level} learner "
                "using simple language and one example."
            )

            result = model(
                prompt,
                max_new_tokens=350,
                do_sample=False
            )

            return result[0][
                "generated_text"
            ].strip()

        except Exception:

            # Fall back to Gemini
            pass

    # -----------------------------------------------------
    # Gemini explanation
    # -----------------------------------------------------

    prompt = f"""
You are EduGenie, a patient teacher.

Explain the following topic to a {level} learner.

Topic:
{topic}

Use this structure:

1. Simple definition
2. Key points
3. How it works
4. Simple example
5. Short recap

Avoid unnecessary technical language.
"""

    return generate_text(
        prompt,
        temperature=0.35
    )