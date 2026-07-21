# 🚀 Study Pilot Air

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?logo=fastapi)
![License](https://img.shields.io/badge/License-Custom-lightgrey)
![Status](https://img.shields.io/badge/Status-In%20Development-success)

A practical study companion for students who want a clearer way to organize classes, prepare for quizzes, and make dense reading material easier to work through.

> **Project status:** MVP foundation. The current app has no user accounts or
> database yet; see the [roadmap](docs/ROADMAP.md) for the product plan.

![Study Pilot Air](https://dummyimage.com/1200x600/0f172a/ffffff&text=Study+Pilot+Air)

## Why Study Pilot Air??

Studying shouldn't mean juggling multiple apps, notes, and AI tools.

Study Pilot Air brings everything together into one place—from planning study sessions to generating practice questions and summarizing reading material.

The goal is to help students spend less time organizing and more time learning.

## What it does

- 📅 Personalized study plans
- 🧠 Quiz generation and practice questions
- 📚 Reading summaries and key-concept extraction
- ✍️ Course-focused study recommendations
- 📊 Weekly study planner
- 💻 Clean and responsive dashboard
- ⚡ FastAPI REST API
  
## Tech stack

- FastAPI for the backend API
- Python for the app logic
- HTML/CSS for the browser dashboard
- Pytest for automated tests

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Deployment guide](docs/DEPLOYMENT.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Product roadmap](docs/ROADMAP.md)

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
python3 -m uvicorn app.main:app --reload
```

On Windows PowerShell, activate the environment with
`\.venv\Scripts\Activate.ps1` and start with `uvicorn app.main:app --reload`.

## OpenAI-powered study help

Study Pilot Air uses the OpenAI Responses API for richer, course-specific study
plans, quizzes, course guidance, and reading summaries. If an API key is not
set or the service is unavailable, it keeps working with built-in study helpers.

When the integration is enabled, create an API key in the OpenAI dashboard and
store it only in your local environment—never commit it to the repository.

**Windows PowerShell**

```powershell
setx OPENAI_API_KEY "your_api_key_here"
```

Open a new terminal after running that command, then start the application as
usual. The OpenAI Python SDK reads `OPENAI_API_KEY` automatically.

For deployment, configure the same variable in your hosting provider's secret
manager rather than placing it in a source file or browser code.

## Start with the launcher script

```bash
./run.sh
```

## Test

```bash
pytest -q
```

GitHub Actions runs this test suite automatically for pull requests and pushes
to `main` and agent branches.

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

This project is designed to grow into a practical study companion for college students, especially for class prep, reading review, weekly planning, and faster study sessions.

## Copyright and licensing

This project is the intellectual property of Guillermo Barreto. All rights reserved.
See [LICENSE](LICENSE) and [NOTICE](NOTICE) for details.
