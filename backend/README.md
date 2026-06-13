# Resume Agent Backend

FastAPI backend skeleton for the resume agent.

The current implementation is intentionally local and deterministic. It answers from structured resume data without calling an LLM. Later, `app/main.py` can be extended to call OpenAI through Cloudflare AI Gateway or another provider.

## Run Locally

```bash
cd backend
uv run uvicorn app.main:app --reload --port 8787
```

Health check:

```bash
curl http://localhost:8787/health
```

## Cloudflare Python Workers

Cloudflare supports FastAPI in Python Workers. This backend includes:

- `app/main.py` - FastAPI app and API routes
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

Ask a question:

```bash
curl -X POST http://localhost:8787/api/chat \
  -H 'content-type: application/json' \
  -d '{"message":"What AI Agent experience does Lu have?","language":"en"}'
```
