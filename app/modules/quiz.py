from ..gemini_service import (
    extract_json,
    generate_text,
)


def generate_quiz(text: str) -> list[dict]:

    prompt = f"""
You are an educational quiz generator.

Read the passage below and create EXACTLY 3
multiple-choice questions.

Every question must contain:

- question
- options
- answer

Rules:

1. There must be exactly 3 questions.
2. Every question must have exactly 4 options.
3. All 4 options must be different.
4. The answer must exactly match one option.
5. Questions must be based only on the supplied passage.
6. Return ONLY valid JSON.
7. Do not use Markdown.
8. Do not add explanations outside the JSON.

Required format:

[
  {{
    "question": "Question here",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Option A"
  }}
]

Passage:

{text}
"""

    raw_response = generate_text(
        prompt,
        temperature=0.2,
        max_output_tokens=1400,
    )

    data = extract_json(raw_response)

    if not isinstance(data, list):
        raise ValueError(
            "Gemini quiz response must be a JSON list."
        )

    if len(data) != 3:
        raise ValueError(
            "Gemini must generate exactly 3 questions."
        )

    result = []

    for item in data:

        if not isinstance(item, dict):
            raise ValueError(
                "Invalid quiz question object."
            )

        question = str(
            item.get("question", "")
        ).strip()

        options = item.get("options")

        answer = str(
            item.get("answer", "")
        ).strip()

        if not question:
            raise ValueError(
                "Quiz question cannot be empty."
            )

        if not isinstance(options, list):
            raise ValueError(
                "Quiz options must be a list."
            )

        if len(options) != 4:
            raise ValueError(
                "Every quiz question must have 4 options."
            )

        options = [
            str(option).strip()
            for option in options
        ]

        if len(set(options)) != 4:
            raise ValueError(
                "Quiz options must be unique."
            )

        if answer not in options:
            raise ValueError(
                "Quiz answer must match one option."
            )

        result.append(
            {
                "question": question,
                "options": options,
                "answer": answer,
            }
        )

    return result