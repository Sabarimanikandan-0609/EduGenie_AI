from fastapi import (
    FastAPI,
    HTTPException,
    Query,
)

from fastapi.responses import FileResponse

from fastapi.staticfiles import StaticFiles

from .config import get_settings

from .gemini_service import (
    GeminiConfigurationError,
)

from .models import (
    QuizResponse,
    TextRequest,
    TopicRequest,
)

from .modules.explanation import (
    explain_topic,
)

from .modules.learning import (
    get_learning_recommendations,
)

from .modules.qa import (
    answer_question,
)

from .modules.quiz import (
    generate_quiz,
)

from .modules.summarizer import (
    summarize_text,
)


settings = get_settings()


app = FastAPI(
    title=settings.app_name,
    description=(
        "Google Gemini powered educational "
        "learning assistant."
    ),
    version="1.0.0",
)


# Serve frontend files.
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)


@app.get(
    "/",
    include_in_schema=False,
)
async def home():

    return FileResponse(
        "static/index.html"
    )


@app.get("/api/health")
async def health():

    return {
        "status": "ok",
        "gemini_configured": bool(
            settings.gemini_api_key
        ),
        "model": settings.gemini_model,
    }


def ai_error(
    exc: Exception,
) -> HTTPException:

    if isinstance(
        exc,
        GeminiConfigurationError,
    ):
        return HTTPException(
            status_code=503,
            detail=str(exc),
        )

    return HTTPException(
        status_code=502,
        detail=f"AI service error: {exc}",
    )


# -----------------------------
# Q&A
# -----------------------------

@app.get("/api/qna")
async def qna(
    question: str = Query(
        ...,
        min_length=1,
        max_length=5000,
    )
):

    try:

        clean_question = question.strip()

        return {
            "question": clean_question,
            "answer": answer_question(
                clean_question
            ),
        }

    except Exception as exc:

        raise ai_error(exc) from exc


# -----------------------------
# Explanation
# -----------------------------

@app.post("/api/explain")
async def explain(
    request: TopicRequest,
):

    try:

        return {
            "topic": request.topic,
            "explanation": explain_topic(
                request.topic
            ),
        }

    except Exception as exc:

        raise ai_error(exc) from exc


# -----------------------------
# Summarizer
# -----------------------------

@app.post("/api/summarize")
async def summarize(
    request: TextRequest,
):

    try:

        return {
            "summary": summarize_text(
                request.text
            ),
        }

    except Exception as exc:

        raise ai_error(exc) from exc


# -----------------------------
# Quiz
# -----------------------------

@app.post(
    "/api/quiz",
    response_model=QuizResponse,
)
async def quiz(
    request: TextRequest,
):

    try:

        return {
            "quiz": generate_quiz(
                request.text
            ),
        }

    except Exception as exc:

        raise ai_error(exc) from exc


# -----------------------------
# Learning recommendations
# -----------------------------

@app.get(
    "/api/learn/recommendations"
)
async def learning_recommendations(
    topic: str = Query(
        ...,
        min_length=1,
        max_length=500,
    )
):

    try:

        clean_topic = topic.strip()

        return {
            "topic": clean_topic,
            "recommendation":
                get_learning_recommendations(
                    clean_topic
                ),
        }

    except Exception as exc:

        raise ai_error(exc) from exc