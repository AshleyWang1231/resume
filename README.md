# Lu Wang — Senior AI Agent Engineer Portfolio

**Live site:** https://ashleywang1231.github.io/resume/

Bilingual (EN/ZH) senior AI Agent / AI Engineer portfolio and resume website with an AI chat agent. The site now maps current AI Agent / AI Engineer job-description signals to concrete evidence: production agent runtime architecture, tool orchestration, grounded retrieval, evaluation systems, latency/reliability work, enterprise data systems, and measurable business impact.

## Stack

| Layer | Tech | Deploy |
|---|---|---|
| Frontend | Static HTML/CSS/JS | GitHub Pages |
| Backend API | Python FastAPI / Python Workers | Cloudflare Workers |
| Agent backend | Hybrid BM25/FAISS retrieval, Pydantic tool schemas, SSE streaming, provider fallback | Cloudflare Workers |

## Key Endpoints

- `GET /api/market-signals` — maps AI Agent / AI Engineer JD themes to resume evidence.
- `GET /api/capabilities` — senior AI engineering capability map for the frontend.
- `GET /api/projects` — structured project cards.
- `GET /api/architecture` — resume agent architecture proof.
- `POST /api/chat` and `POST /api/chat/stream` — non-streaming and SSE resume-agent chat.

## Local Preview

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Backend Dev

```bash
cd backend
cp .env.example .env  # fill in AI_PROVIDER + API key only if testing live model calls
uv run uvicorn app.main:app --app-dir src --reload --port 8787
```

## Test

```bash
cd backend
uv run pytest -v
```

## Deploy

- **Frontend**: auto-deploys to GitHub Pages on push to `main`
- **Backend**: auto-deploys to Cloudflare Workers on push to `backend/**`
