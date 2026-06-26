# Lu Wang — AI Engineer Portfolio

**Live site:** https://ashleywang1231.github.io/resume/

Bilingual (EN/ZH) portfolio and resume website with an AI chat agent powered by DeepSeek.

## Stack

| Layer | Tech | Deploy |
|---|---|---|
| Frontend | Static HTML/CSS/JS | GitHub Pages |
| Backend API | Python FastAPI | Aliyun Function Compute (`cn-hangzhou`) |

## Local Preview

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Backend Dev

```bash
cd backend
cp .env.example .env  # fill in AI_PROVIDER + API key
uv run uvicorn app.main:app --reload --port 8787
```

## Deploy

- **Frontend**: auto-deploys to GitHub Pages on push to `main`
- **Backend**: auto-deploys to Aliyun FC on push to `backend/**`
