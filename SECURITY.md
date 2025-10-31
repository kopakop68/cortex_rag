# Security Policy

- Never commit secrets; use `.env` locally and GitHub Actions **Secrets** in CI.
- Enable branch protection on `main` (PR reviews + passing checks).
- Add prompt‑injection and PII‑redaction guards in API middleware.
- Report vulnerabilities privately via Security Advisories.
