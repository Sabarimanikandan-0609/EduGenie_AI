from ..gemini_service import generate_text


def summarize_text(text: str) -> str:

    prompt = f"""
Summarize the following text.

Rules:
- Keep the main ideas.
- Remove unnecessary repetition.
- Use simple language.
- Do not add information that is not present in the source.
- Use bullet points when helpful.
- Keep the summary concise.

Source text:

{text}
"""

    return generate_text(
        prompt,
        temperature=0.2,
        max_output_tokens=1000,
    )