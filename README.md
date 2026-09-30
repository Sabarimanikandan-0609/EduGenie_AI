# 🧠 EduGenie

EduGenie is an AI-powered educational learning assistant built using **Python, FastAPI, JavaScript, HTML, CSS, and Google Gemini AI**.

It helps students learn faster by providing AI-powered question answering, topic explanations, text summarization, quiz generation, and personalized learning recommendations.

---

## ✨ Features

- 💬 **Ask EduGenie** – Ask educational questions and receive AI-generated answers.
- 📚 **Topic Explanation** – Get difficult concepts explained in simple language.
- 📝 **Text Summarizer** – Convert long study material into concise summaries.
- 🧠 **Quiz Generator** – Generate multiple-choice questions from study material.
- 🚀 **Learning Recommendations** – Get a structured beginner-to-advanced learning path.
- ⚡ **FastAPI Backend** – REST API for all AI features.
- 🎨 **Responsive Web Interface** – Simple and student-friendly frontend.
- 🤖 **Google Gemini Integration** – AI responses powered by Gemini.

---

## 🛠️ Technologies Used

### Frontend

- HTML5
- CSS3
- JavaScript

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic

### AI

- Google Gemini API
- `google-genai`

### Testing

- Pytest
- HTTPX

---

## 📁 Project Structure

```text
EduGenie/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── gemini_service.py
│   ├── main.py
│   ├── models.py
│   │
│   └── modules/
│       ├── __init__.py
│       ├── qa.py
│       ├── explanation.py
│       ├── summarizer.py
│       ├── quiz.py
│       └── learning.py
│
├── static/
│   ├── index.html
│   ├── app.js
│   └── styles.css
│
├── tests/
│   └── test_api.py
│
├── .env.example
├── .gitignore
├── requirements.txt
├── pytest.ini
└── README.md