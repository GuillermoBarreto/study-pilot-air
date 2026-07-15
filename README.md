# Study Pilot AI

Study Pilot AI is a personal study assistant built for students who want help organizing classes, preparing for quizzes, and breaking down dense reading material from platforms like ZyBooks.

## What it does

- Generates a simple study plan for any topic
- Creates quick quiz questions for practice
- Provides course-focused study tips for class preparation
- Summarizes long reading text into short, digestible points
- Offers a lightweight web dashboard for everyday studying

## Tech stack

- FastAPI for the backend API
- Python for the core app logic
- HTML/CSS for the browser-based dashboard
- Pytest for automated tests

## Run locally

```bash
pip install -r requirements.txt -r requirements-dev.txt
python3 -m uvicorn app.main:app --reload
```

## Start with the launcher script

```bash
./run.sh
```

## Test

```bash
pytest -q
```

## Example API usage

### Generate a study plan

```bash
curl -X POST http://127.0.0.1:8000/study-plan \
  -H "Content-Type: application/json" \
  -d '{"topic":"Functions","days":3,"hours_per_day":2}'
```

### Summarize ZyBooks-style content

```bash
curl -X POST http://127.0.0.1:8000/zybooks \
  -H "Content-Type: application/json" \
  -d '{"text":"Functions are reusable blocks of code that help organize programs."}'
```

## Project goal

This project is designed to grow into a practical AI study companion for college students, especially for class prep, reading comprehension, and quick review sessions.
