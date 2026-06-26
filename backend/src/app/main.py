from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
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


_static_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "static")
_static_dir = os.path.abspath(_static_dir)
if not os.path.isdir(_static_dir):
    # FC runtime: code is at /code/
    _static_dir = "/code/static"
if os.path.isdir(_static_dir):
    app.mount("/", StaticFiles(directory=_static_dir, html=True), name="static")
