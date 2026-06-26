from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from app.config import load_local_env
from app.harness import ResumeAgent
from app.harness.events import stream_chat_response
from app.harness.observability import with_request_logging
from app.models import ChatRequest, ChatResponse


load_local_env()
app = FastAPI(title="Lu Wang Resume Agent API")
app.state.ai_binding = None
agent = ResumeAgent()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

_static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "static"))
if not os.path.isdir(_static_dir):
    _static_dir = "/code/static"
_index_html = os.path.join(_static_dir, "index.html") if os.path.isdir(_static_dir) else None


@app.get("/", response_class=HTMLResponse)
@app.get("/index.html", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    if _index_html and os.path.isfile(_index_html):
        with open(_index_html, encoding="utf-8") as f:
            # Use application/xhtml+xml — FC only injects Content-Disposition: attachment
            # on text/html, but browsers still render xhtml+xml as a webpage
            return HTMLResponse(
                content=f.read(),
                media_type="application/xhtml+xml",
                headers={"Content-Disposition": "inline"},
            )
    return HTMLResponse(content="<h1>Not found</h1>", status_code=404)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    ai = app.state.ai_binding
    return await with_request_logging(
        route="/api/chat",
        handler=lambda: agent.answer(request, ai),
        base_fields={"language": request.language},
    )


@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest) -> StreamingResponse:
    ai = app.state.ai_binding
    response = await with_request_logging(
        route="/api/chat/stream",
        handler=lambda: agent.answer(request, ai),
        base_fields={"language": request.language},
    )
    return StreamingResponse(stream_chat_response(response), media_type="text/event-stream")


if os.path.isdir(_static_dir):
    app.mount("/", StaticFiles(directory=_static_dir, html=True), name="static")
