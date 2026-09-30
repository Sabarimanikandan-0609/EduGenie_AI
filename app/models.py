from pydantic import BaseModel, Field, field_validator


class TopicRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=500,
    )

    @field_validator("topic")
    @classmethod
    def clean_topic(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "Topic cannot be empty."
            )

        return value


class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=20000,
    )

    @field_validator("text")
    @classmethod
    def clean_text(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "Text cannot be empty."
            )

        return value


class QuizQuestion(BaseModel):
    question: str

    options: list[str] = Field(
        min_length=4,
        max_length=4,
    )

    answer: str

    @field_validator("answer")
    @classmethod
    def answer_must_be_option(
        cls,
        value: str,
        info,
    ):

        options = info.data.get(
            "options",
            [],
        )

        if options and value not in options:
            raise ValueError(
                "Answer must exactly match one of the options."
            )

        return value


class QuizResponse(BaseModel):
    quiz: list[QuizQuestion]