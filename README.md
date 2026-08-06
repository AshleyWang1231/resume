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

## Homework Assignment Feature: Interactive Resume Visitor Board

This repo now includes a small AWS serverless assignment feature added to the existing static resume site.

Core assignment flow:

```text
S3 static frontend → Lambda Function URL → DynamoDB
```

The Visitor Board lets a public visitor submit a required `name` and `message`, stores the item in DynamoDB, and displays submitted messages on the S3-hosted resume page.

The existing AI resume agent, Aliyun backend, DeepSeek integration, and Cloudflare-related backend are portfolio functionality, not the core homework feature.

### Public static files to upload to S3

Upload only:

```text
index.html
styles.css
script.js
assets/
```

Before uploading, set `VISITOR_BOARD_API` in `script.js` to the deployed Lambda Function URL.

### AWS backend source

Lambda source and deployment notes live in:

```text
aws/
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
