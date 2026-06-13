# Resume Agent Backend

Python backend skeleton for the resume agent.

The current implementation is intentionally local and deterministic. It answers from structured resume data without calling an LLM. Later, `app/main.py` can be extended to call OpenAI through Cloudflare AI Gateway or another provider.

## Run Locally

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8787
```

Health check:

```bash
curl http://localhost:8787/health
```

Ask a question:

```bash
curl -X POST http://localhost:8787/api/chat \
  -H 'content-type: application/json' \
  -d '{"message":"What AI Agent experience does Lu have?","language":"en"}'
```

