# AI Mailbox

Monorepo scaffold containing the API service and a placeholder for the web app.

- API path: `apps/api`
- Web path: `apps/web` (placeholder)

## Getting Started

1. Start Postgres and Redis (Docker Desktop required)

```powershell
cd .\deploy
docker compose up -d db redis
```

2. Install API deps and run migrations

```powershell
cd ..\apps\api
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -e .
$env:DATABASE_URL = "postgresql+psycopg://user:pass@localhost:5432/ai_mailbox"
alembic upgrade head
```

3. Run API locally

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Alternative: from `apps/api/app` you can run `python -m app.main` (module form keeps imports working).

4. Seed demo data (optional)

```powershell
cd ..\..\scripts
python .\seed_demo_data.py
```

Health check: http://localhost:8000/api/v1/health

### Triage demo data
- Run the seed script above to create a demo user and messages.
- Use the returned/known demo user email `demo@example.com` with `/api/v1/auth/demo-login` to get the `user_id`.
- Call `/api/v1/mail/triage?user_id=<uuid>` to see the seeded threads and classifications.

## Notes for local API usage

- Use `/api/v1/auth/demo-login` to create a dev user record (stores only email + display name).
- Pass `user_id` (UUID from the demo login response) to `/api/v1/mail/triage`, `/api/v1/mail/thread/{id}`, and `/api/v1/analytics/overview` to query data.
