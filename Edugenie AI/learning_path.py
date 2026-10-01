from ai_client import generate_text


def get_learning_recommendations(
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

    prompt = f"""
You are EduGenie, a personalized learning advisor.

Create a structured learning path for:

{topic}

Current learner level:

{level}

Create the roadmap from foundational concepts
towards advanced concepts.

Use this structure:

# Learning Goal

Explain what the learner should eventually be able to do.

# Stage 1 — Foundations

Topics:
- ...

Estimated time:
- ...

Practice:
- ...

# Stage 2 — Intermediate

Topics:
- ...

Estimated time:
- ...

Practice:
- ...

# Stage 3 — Advanced

Topics:
- ...

Estimated time:
- ...

Practice:
- ...

# Projects

Give practical projects that reinforce learning.

# Recommended Resources

Suggest useful types of resources such as:

- Official documentation
- Books
- Tutorials
- Videos
- Practice platforms

# Milestones

Give clear checkpoints for determining whether
the learner is ready to move to the next stage.

Make the roadmap realistic and easy to follow.
"""

    return generate_text(
        prompt,
        temperature=0.4
    )