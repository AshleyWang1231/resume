# Lu Wang AI Engineer Portfolio

Static bilingual AI Engineer portfolio and resume website for GitHub Pages.

## Files

- `index.html` - page content and structure
- `styles.css` - responsive layout and visual design
- `script.js` - Chinese/English language switcher
- `assets/lu-wang-resume-cn-en.pdf` - downloadable bilingual PDF resume
- `backend/` - Python FastAPI skeleton for the future Resume Agent API

## Sections

- Impact metrics
- AI systems capability map
- Workflow showcase for Agent Runtime, personalization, Product Comparison, and Text2SQL
- Engineering principles for LLM applications
- Work experience, projects, skills, and education

## Local Preview

Open `index.html` directly in a browser, or run a local server:

```bash
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

## Python Backend Preview

The backend is currently a deterministic resume-agent skeleton. It answers from structured resume data and does not call an LLM yet.

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8787
```

Then test:

```bash
curl http://localhost:8787/health
```

## Deploy to GitHub Pages

1. Create a GitHub repository, for example `resume`.
2. Copy the contents of this `resume-site` folder into the repository root.
3. Push to GitHub.
4. In the repository settings, go to **Pages**.
5. Set **Source** to `Deploy from a branch`.
6. Select the `main` branch and `/root`.
7. Save. GitHub will publish the site after the Pages build finishes.

For a personal GitHub Pages homepage, create a repository named:

```text
<github-username>.github.io
```

Then put these files in the repository root.
