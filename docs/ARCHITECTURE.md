# Architecture

Study Pilot Air is a small FastAPI web application with a server-rendered
dashboard and JSON API endpoints.

```text
Browser dashboard
  ├── templates/index.html
  └── static/app.css
          │ HTTP requests
          ▼
FastAPI application (app/main.py)
  ├── deterministic study helpers
  ├── optional OpenAI wrapper (app/ai_helper.py)
  └── in-memory course data (app/data.py)
```

## Request flow

1. The dashboard sends a request to a FastAPI endpoint.
2. The endpoint validates input with Pydantic.
3. When `OPENAI_API_KEY` is configured, the server asks OpenAI for a structured
   study response and validates it against the local response model.
4. If AI is not configured or returns an invalid response, the endpoint uses a
   deterministic fallback.
5. The browser renders the result.

## Current boundaries

- The app has no authentication or database yet.
- Course data is sample data stored in source code.
- API keys stay server-side and must never be sent to the browser.
- AI output is treated as untrusted and validated before it is returned.

See [ROADMAP.md](ROADMAP.md) for the path to a multi-user product.
