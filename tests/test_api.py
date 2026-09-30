from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():

    response = client.get(
        "/api/health"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "ok"

    assert "model" in body

    assert "gemini_configured" in body


def test_home():

    response = client.get("/")

    assert response.status_code == 200

    assert "EduGenie" in response.text


def test_explain_validation():

    response = client.post(
        "/api/explain",
        json={
            "topic": ""
        },
    )

    assert response.status_code == 422


def test_summarize_validation():

    response = client.post(
        "/api/summarize",
        json={
            "text": ""
        },
    )

    assert response.status_code == 422


def test_quiz_validation():

    response = client.post(
        "/api/quiz",
        json={
            "text": ""
        },
    )

    assert response.status_code == 422