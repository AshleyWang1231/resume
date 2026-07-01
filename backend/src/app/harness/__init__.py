"""Harness package.

Six-layer structure (Harness Engineering):

  Layer 1 – Context Management
      prompts.py       system prompt construction, intent-aware focus injection
      router.py        intent classification → retrieval hints + prompt focus

  Layer 2 – Tool System
      tools.py         BM25 + FAISS hybrid retrieval, tool dispatch, Pydantic schemas
      pydantic_tools.py  tool schema generation for OpenAI / Responses API
      embedding.py     DashScope embedding API (sync + async)

  Layer 3 – Execution Orchestration
      agent.py         ResumeAgent: guard → intent → retrieval → LLM loop →
                       self-correction → fallback → SSE stream
      stream_types.py  StreamEvent dataclass

  Layer 4 – Memory & State
      (session.py is one level up at app/session.py — in-process LRU store)

  Layer 5 – Evaluation & Observability
      observability.py request-level structured logging + latency tracking

  Layer 6 – Constraints, Validation & Failure Recovery
      guard.py         rule-based input filter (zero API calls)
      utils.py         sanitise_answer, dedupe_evidence, parse_arguments, log

  Infrastructure
      events.py        SSE serialisation helpers
      provider_factory.py  multi-provider LLM client factory (Qwen/DeepSeek/OpenAI)
      chat_completions_client.py  OpenAI-compatible chat completions + streaming
      openai_client.py  OpenAI Responses API client
      workers_ai_client.py  Cloudflare Workers AI client
"""
from app.harness.agent import ResumeAgent

__all__ = ["ResumeAgent"]
