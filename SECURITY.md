# Security Policy

## Reporting a vulnerability

Please do not open a public issue for a suspected security vulnerability.
Contact the repository owner privately with a description, reproduction steps,
and any suggested mitigation. Do not include real API keys or student data.

## Handling secrets

- Set `OPENAI_API_KEY` through the operating system or deployment provider's
  secret manager.
- Keep `.env` files local; they are ignored by Git.
- Never expose API keys in browser code, screenshots, issues, pull requests,
  logs, or test fixtures.
- Revoke and replace a key immediately if it is exposed.

## Data handling

The current application does not persist user accounts or uploaded files. Text
submitted to AI-enabled endpoints may be sent to the configured AI provider.
Avoid submitting personal, confidential, or regulated student information.
