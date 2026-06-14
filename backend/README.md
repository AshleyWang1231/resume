# Resume Agent Backend

FastAPI backend skeleton for the resume agent.

The current implementation is intentionally local and deterministic. It answers from structured resume data without calling an LLM. Later, `app/main.py` can be extended to call OpenAI through Cloudflare AI Gateway or another provider.

## Run Locally

```bash
cd backend
uv run uvicorn app.main:app --app-dir src --reload --port 8787
```

Health check:

```bash
curl http://localhost:8787/health
```

## Cloudflare Python Workers

Cloudflare supports FastAPI in Python Workers. This backend includes:

- `src/app/main.py` - FastAPI app and API routes
- `src/worker.py` - Cloudflare Worker entrypoint that mounts the FastAPI ASGI app
- `wrangler.jsonc` - Cloudflare Worker configuration
- `pyproject.toml` - Python dependencies for Cloudflare Python Workers
- `package.json` - `pywrangler` dev/deploy commands

Run locally with Cloudflare Worker runtime:

```bash
cd backend
uv run pywrangler dev
```

Deploy:

```bash
cd backend
uv run pywrangler deploy
```

## GitHub Actions Deployment

Backend deployment is automated by `.github/workflows/deploy-backend.yml`.
The workflow runs when code is pushed to `main` and files under `backend/**` change.

Add these repository secrets in GitHub before relying on automatic deployment:

- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ACCOUNT_ID`

Recommended Cloudflare API token permissions:

- Account: `Cloudflare Workers Scripts:Edit`
- Account: `Account Settings:Read`

After the secrets are added, pushing backend changes to `main` will deploy the Worker and verify:

```text
https://resume-agent-api.wanglu-ashley.workers.dev/health
```

Ask a question:

```bash
curl -X POST http://localhost:8787/api/chat \
  -H 'content-type: application/json' \
  -d '{"message":"What AI Agent experience does Lu have?","language":"en"}'
```
