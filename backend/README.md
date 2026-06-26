# Resume Agent Backend

FastAPI backend for the resume agent.

The current implementation uses a lightweight AI harness with Pydantic AI tool schemas, local resume tools, provider adapters, fallback evidence search, and SSE streaming. It can call OpenAI Responses API, or OpenAI-compatible Chat Completions providers such as Qwen and DeepSeek. If no provider key is configured, the backend still answers from deterministic structured resume evidence.

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
- `src/app/harness/` - lightweight Resume Agent harness with Pydantic AI tool schema validation, provider adapters, streaming events, and fallback
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

## AI Provider Configuration

The backend supports multiple AI providers:

- `openai` - OpenAI Responses API
- `qwen` - Alibaba Cloud Model Studio / Qwen OpenAI-compatible Chat Completions API
- `deepseek` - DeepSeek OpenAI-compatible Chat Completions API

If the selected provider key is missing or the model request fails, the API falls back to deterministic resume evidence search.

Pydantic AI is used for tool schema generation and argument validation. The provider HTTP adapters stay lightweight because Cloudflare Python Workers currently cannot install `pydantic-ai-slim[openai]` due to the `tiktoken` wheel requirement.

Local development reads provider settings from `backend/.env`. Start from the example file:

```bash
cd backend
cp .env.example .env
```

OpenAI:

```dotenv
AI_PROVIDER=openai
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-4.1-mini
```

Qwen:

```dotenv
AI_PROVIDER=qwen
QWEN_API_KEY=...
QWEN_MODEL=qwen-plus
QWEN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

`DASHSCOPE_API_KEY` is also accepted as an alias for `QWEN_API_KEY`.

DeepSeek:

```dotenv
AI_PROVIDER=deepseek
DEEPSEEK_API_KEY=...
DEEPSEEK_MODEL=deepseek-v4-flash
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

Cloudflare Worker secrets:

```bash
cd backend
uv run pywrangler secret put AI_PROVIDER
uv run pywrangler secret put OPENAI_API_KEY
uv run pywrangler secret put OPENAI_MODEL
```

Only configure the secrets for the provider you use. Model and base URL values are optional unless you want to override defaults.

Streaming endpoint:

```bash
curl -N -X POST http://localhost:8787/api/chat/stream \
  -H 'content-type: application/json' \
  -d '{"message":"Show Streaming and Tool Calling experience.","language":"en"}'
```

## GitHub Actions Deployment

Backend deployment is automated by `.github/workflows/deploy-backend.yml`.
The workflow runs when code is pushed to `main` and files under `backend/**` change.

Add these repository secrets in GitHub before relying on automatic deployment:

- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ACCOUNT_ID`

If you want GitHub Actions to update Worker secrets in the future, add that as a separate explicit step.
The current workflow deploys code only; Cloudflare Worker secrets are configured directly through `pywrangler secret put`.

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
