# Study Pilot

A practical study companion for students who want a clearer way to organize classes, prepare for quizzes, and make dense reading material easier to work through.

![Study Pilot Dashboard](https://via.placeholder.com/1200x600.png?text=Study+Pilot+Dashboard)

## What it does

- Generates a simple study plan for any topic
- Creates quick practice questions for review
- Offers course-focused study tips for class preparation
- Breaks long reading material into short, easier-to-follow points
- Provides a lightweight web dashboard for everyday studying

## Tech stack

- FastAPI for the backend API
- Python for the app logic
- HTML/CSS for the browser dashboard
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

### Summarize reading content

```bash
curl -X POST http://127.0.0.1:8000/zybooks \
  -H "Content-Type: application/json" \
  -d '{"text":"Functions are reusable blocks of code that help organize programs."}'
```

## Project goal

This project is designed to grow into a practical study companion for college students, especially for class prep, reading review, and quick study sessions.

## Copyright and licensing

This project is the intellectual property of Guillermo Barreto. All rights reserved.
See [LICENSE](LICENSE) and [NOTICE](NOTICE) for details.
