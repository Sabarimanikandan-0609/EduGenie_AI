from ..gemini_service import generate_text


def get_learning_recommendations(topic: str) -> str:

    prompt = f"""
You are EduGenie, an AI learning assistant.

The student wants to learn:

{topic}

Create a structured learning path.

Use exactly these sections:

1. Beginner Level
   - Foundation concepts
   - Estimated learning time
   - Practice activities

2. Intermediate Level
   - Next concepts
   - Estimated learning time
   - Practice activities

3. Advanced Level
   - Advanced concepts
   - Projects
   - Practice activities

4. Suggested Weekly Order
   - Give a simple weekly learning sequence.

Make the plan practical and student-friendly.

Mention well-known learning resources only when
you are confident about them.

Do not invent URLs.
"""

    return generate_text(
        prompt,
        temperature=0.5,
        max_output_tokens=1800,
    )