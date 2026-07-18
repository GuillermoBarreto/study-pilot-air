# Deployment Guide

## Production checklist

1. Use a managed Python host that can run an ASGI application.
2. Install dependencies from `requirements.txt`.
3. Set `OPENAI_API_KEY` in the host's secret manager if AI features are needed.
4. Set `OPENAI_MODEL` only when you need to override the default.
5. Start the service with an ASGI server, for example:

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
   ```

6. Run the automated test suite before each deployment.

## Environment variables

| Variable | Required | Purpose |
| --- | --- | --- |
| `OPENAI_API_KEY` | No | Enables server-side OpenAI study features. |
| `OPENAI_MODEL` | No | Overrides the default AI model. |
| `PORT` | Usually | Port supplied by many hosting providers. |

## Important notes

- Do not use `--reload` in production.
- Configure HTTPS at the hosting provider or reverse proxy.
- Keep all secrets in the provider's secret manager.
- Before accepting real students, add authentication, a database, rate limits,
  privacy terms, and a data-retention policy.
