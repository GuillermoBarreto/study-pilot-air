# Contributing to Study Pilot Air

Thanks for helping improve Study Pilot Air. Keep changes focused, tested, and
safe for students' data.

## Local setup

1. Create and activate a Python 3.12 virtual environment.
2. Install dependencies with `pip install -r requirements.txt -r requirements-dev.txt`.
3. Copy `.env.example` to `.env` only if you need AI features, then set values
   locally. Never commit `.env` or API keys.
4. Start the app with `uvicorn app.main:app --reload`.

## Before opening a pull request

Run the following checks:

```bash
pytest -q
git diff --check
```

Update tests whenever an endpoint or response contract changes. Describe the
user-facing behavior and any environment variables needed in the pull request.

## Code guidelines

- Keep secrets on the server and out of browser JavaScript.
- Validate request data with Pydantic models.
- Preserve a useful non-AI fallback when external AI calls fail.
- Do not log study content, API keys, or credentials.
- Use clear, student-friendly language in the interface.
