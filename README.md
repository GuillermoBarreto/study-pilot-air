# study-pilot-air

AI-powered study assistant built with FastAPI.

## Run locally

```bash
pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload
```

## Test

```bash
pytest -q
```

## API example

```bash
curl -X POST http://127.0.0.1:8000/study-plan \
  -H "Content-Type: application/json" \
  -d '{"topic":"Python Basics","days":3,"hours_per_day":2}'
```
