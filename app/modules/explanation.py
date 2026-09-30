from ..gemini_service import generate_text


def explain_topic(topic: str) -> str:

    prompt = f"""
You are EduGenie, an AI educational tutor.

Explain the following topic in a simple and clear way.

Topic:
{topic}

Structure your explanation like this:

1. Simple definition
2. Main idea
3. How it works
4. Small example
5. Important points to remember

Avoid unnecessary technical jargon.

Make the explanation useful for a college student.
"""

    return generate_text(
        prompt,
        temperature=0.4,
        max_output_tokens=1200,
    )