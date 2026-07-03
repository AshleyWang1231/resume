# Resume Agent Backend AI V1 Design

## Goal

Build the first real AI version of the Resume Agent backend. V1 should prove that the resume site is not a static FAQ:

- It can answer questions from resume evidence.
- It can call internal tools instead of relying only on model memory.
- It can stream useful events to the frontend.
- It exposes clean APIs that can be tested and deployed through the existing Cloudflare Worker pipeline.
- It has a small harness layer that shows AI engineering discipline: routing, tool execution, evidence grounding, fallback, evaluation, and observability.

V1 should stay lightweight. Do not introduce LangGraph or a full multi-agent framework yet. The recommended stack is:

```text
FastAPI on Cloudflare Python Workers
  -> Resume Agent Harness
  -> Pydantic AI Tool Registry
  -> Provider Adapters
      -> OpenAI Responses API
      -> Qwen / DeepSeek Chat Completions API
  -> Local resume tools
  -> SSE streaming response
```

## Non-goals

- No long-term conversation memory in V1.
- No user login or private user data.
- No vector database in V1; structured resume facts are enough.
- No multi-agent graph orchestration.
- No public secret exposure in frontend code.

## Runtime Choice

Use **a small custom harness + Pydantic AI tool schema layer**.

Why:

- Pydantic AI gives the backend typed tool schema generation and argument validation without introducing a heavy graph framework.
- OpenAI stays on the Responses API through a lightweight Worker-compatible HTTP adapter.
- Qwen and DeepSeek use the same harness contract through OpenAI-compatible `/chat/completions` endpoints.
- A small custom harness keeps the product behavior understandable and lets this project demonstrate the same ideas as the resume: Tool Calling, Streaming, structured output, evaluation, fallback, and observability.
- This project only needs 4-6 focused tools, so a heavy orchestration framework would add more complexity than value.
- Cloudflare Python Workers currently cannot install `pydantic-ai-slim[openai]` because that optional group depends on `tiktoken`, which has no usable Worker/Pyodide wheel in this environment.

## Backend API

### `GET /health`

Existing health check.

### `POST /api/chat`

Non-streaming endpoint for simple clients and regression tests.

Request:

```json
{
  "message": "Show Lu's Streaming and Tool Calling experience.",
  "language": "en"
}
```

Response:

```json
{
  "answer": "...",
  "evidence": [
    {
      "title": "Agent Runtime Upgrade",
      "company": "Zalando",
      "summary": "...",
      "evidence": ["-25% avg TTFT", "-25% P95 TTFT"],
      "skills": ["Tool Calling", "Streaming"]
    }
  ],
  "suggested_questions": ["..."]
}
```

### `POST /api/chat/stream`

Primary endpoint for the website. Use Server-Sent Events.

Request is the same as `/api/chat`.

Response content type:

```text
text/event-stream
```

Event contract:

```text
event: metadata
data: {"request_id":"...","language":"en"}

event: tool_call
data: {"name":"search_resume_facts","arguments":{"query":"Streaming Tool Calling"}}

event: tool_result
data: {"name":"search_resume_facts","count":1}

event: answer_delta
data: {"text":"Lu has worked on..."}

event: evidence
data: [{"title":"Agent Runtime Upgrade","company":"Zalando", "...": "..."}]

event: done
data: {"request_id":"...","latency_ms":1234}
```

Error event:

```text
event: error
data: {"message":"The resume agent is temporarily unavailable."}
```

The frontend should render only `answer_delta` as chat text. `tool_call`, `tool_result`, `metadata`, and `done` can be used for subtle status UI or debugging, but should not be shown as raw model output.

## Harness Responsibilities

The harness is the core engineering layer. It should be a small module, not a framework.

### 1. Request Normalization

- Trim and validate message.
- Normalize language to `en` or `zh`.
- Generate `request_id`.
- Apply max length guard.

### 2. Intent Routing

Classify the question into one of:

- `experience_lookup`
- `project_detail`
- `impact_metrics`
- `interview_answer`
- `role_fit`
- `general_profile`

This can start as rules and move to model-assisted routing later.

### 3. Tool Registry

V1 tools should be deterministic Python functions:

| Tool | Purpose |
|---|---|
| `search_resume_facts` | Find the most relevant resume facts by query and keywords. |
| `get_project_detail` | Return full structured detail for one project. |
| `list_capabilities` | Return skill groups and project-to-skill mapping. |
| `build_interview_answer` | Compose a STAR-style answer from selected evidence. |
| `compare_role_fit` | Compare a role description against resume capabilities. |

These tools are callable by the model through Responses API function calling, but the backend owns execution and validation.

### 4. Tool Result Validation

Every tool returns a typed object. Invalid or empty results must be handled by fallback:

- No matching project -> return top 2 representative projects.
- Question too broad -> return concise profile answer plus suggested questions.
- Tool failure -> degrade to structured resume search, not a generic apology.

### 5. Evidence Grounding

The model should answer from tool results only. Prompt should require:

- Do not invent employers, metrics, tools, or dates.
- Mention only evidence returned by tools.
- Keep answers concise.
- Use Chinese if `language=zh`, English if `language=en`.

### 6. Streaming Adapter

The adapter converts model/tool events into frontend-safe SSE events:

- Tool call event
- Tool result event
- Answer delta event
- Evidence event
- Done event
- Error event

The adapter should hide raw reasoning and any intermediate JSON fragments from the user-facing answer.

## OpenAI Integration

Environment variables:

```text
AI_PROVIDER=openai
OPENAI_API_KEY
OPENAI_MODEL
```

Recommended default model:

```text
gpt-4.1-mini
```

Rationale:

- The resume agent is retrieval/tool-heavy, not deep reasoning-heavy.
- Lower latency matters on a public website.
- Responses can later switch to a stronger model for interview-answer generation if needed.

Initial request shape:

```json
{
  "model": "gpt-4.1-mini",
  "input": [
    {
      "role": "system",
      "content": "You are Lu Wang's resume agent..."
    },
    {
      "role": "user",
      "content": "Show Streaming and Tool Calling experience."
    }
  ],
  "tools": [
    {
      "type": "function",
      "name": "search_resume_facts",
      "description": "Search Lu Wang's structured resume facts.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {"type": "string"}
        },
        "required": ["query"],
        "additionalProperties": false
      }
    }
  ],
  "tool_choice": "auto",
  "stream": true
}
```

For V1 implementation, Pydantic AI owns tool schema generation and argument validation. The custom harness owns provider calls, routing, evidence grounding, fallback behavior, and frontend-safe SSE events.

## OpenAI-compatible Chat Completions Providers

Qwen and DeepSeek use Worker-compatible HTTP adapters pointed at each provider's OpenAI-compatible Chat Completions endpoint. Their tool schemas and argument validation come from the same Pydantic AI registry. The harness contract stays the same:

```text
model selects tool
  -> backend executes tool
  -> backend appends tool result
  -> model writes grounded final answer
```

Qwen environment:

```text
AI_PROVIDER=qwen
QWEN_API_KEY or DASHSCOPE_API_KEY
QWEN_MODEL=qwen-plus
QWEN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

DeepSeek environment:

```text
AI_PROVIDER=deepseek
DEEPSEEK_API_KEY
DEEPSEEK_MODEL=deepseek-v4-flash
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

Provider-specific notes:

- Qwen regional base URLs differ by Alibaba Cloud region, so `QWEN_BASE_URL` must stay configurable.
- DeepSeek currently documents `deepseek-v4-flash` and `deepseek-v4-pro` as primary models; older `deepseek-chat` compatibility names are marked for deprecation.
- Tool schemas are generated through Pydantic AI, while the backend still validates and executes local tools before returning grounded final answers.

## Observability

Log one structured line per request:

```json
{
  "request_id": "...",
  "route": "/api/chat/stream",
  "intent": "experience_lookup",
  "language": "en",
  "tools_called": ["search_resume_facts"],
  "evidence_count": 2,
  "latency_ms": 1234,
  "status": "success"
}
```

Track at least:

- Request count
- Error count
- Latency
- Tool call count
- Fallback count
- Empty evidence count
- Streaming first-token latency if feasible

## Evaluation

The backend uses a three-layer evaluation strategy.  Each layer has a
different cost profile and failure signal:

```
Layer 1 — Retrieval Eval   (no LLM, always runs in CI)
Layer 2 — Agent Regression (LLM, always runs in CI, answers must contain key facts)
Layer 3 — LLM-as-Judge     (LLM, gated by JUDGE_EVAL=1, scores quality)
```

---

### Layer 1 — Retrieval Evaluation (`test_retrieval_eval.py`)

**What it tests:** BM25 + FAISS hybrid search quality.  No LLM calls.
Safe to run in every CI job.

**How it works:**

Maintains a `GOLD` set of (query, language, expected_doc_ids) tuples.
For each query it checks that at least one expected document appears in the
top-K results, then reports aggregate P@K, R@K, and MRR.

```python
# example GOLD entry
("TTFT latency optimization streaming", "en", {"agent-runtime"})
```

**Synthetic question augmentation (RAGAS-inspired):**

Run `scripts/generate_synthetic_questions.py` once to produce
`tests/synthetic_gold.json`.  The script reads every `RESUME_FACT`,
calls an LLM to reverse-engineer realistic recruiter questions for each
fact (4 EN + 4 ZH per fact), and saves them as structured test cases.

```bash
cd backend
AI_PROVIDER=qwen QWEN_API_KEY=sk-... \
    uv run python scripts/generate_synthetic_questions.py
```

`test_retrieval_eval.py` auto-loads `synthetic_gold.json` when present,
adding ~60 generated queries on top of the ~20 hand-curated ones.
The synthetic tests are skipped in CI if the file has not been generated.

This mirrors RAGAS's core insight: **start from the answer (document
content), have an LLM reverse-engineer what questions that content
would answer**, giving you ground-truth (query → expected doc) pairs
without manual labelling.

**Metrics reported:**

| Metric | Description |
|---|---|
| P@K | Fraction of top-K results that are relevant |
| R@K | Fraction of relevant docs found in top-K |
| MRR | Mean Reciprocal Rank (position of first hit) |
| Hit rate | % of queries where at least one expected doc appears |

---

### Layer 2 — Agent Regression (`test_agent_eval.py`)

**What it tests:** End-to-end agent behavior — does the full pipeline
(intent routing → retrieval → LLM answer → evidence) produce the right
output for known questions?

**How it works:**

Each case in `tests/eval_cases.json` specifies:

```json
{
  "id": "streaming_tool_calling_en",
  "message": "Show Lu's Streaming and Tool Calling experience.",
  "language": "en",
  "must_include": ["Agent Runtime Upgrade", "Tool Calling", "Streaming", "25%"],
  "expected_project_ids": ["agent-runtime"]
}
```

The test asserts that `expected_project_ids` appear in the evidence and
that `must_include` keywords appear in the answer or evidence text.

These are deterministic keyword assertions — fast, cheap, and reliable
as CI gates.  They catch regressions when retrieval or prompts change.

**V1 target:** 20–30 cases covering EN + ZH and each major project.

---

### Layer 3 — LLM-as-Judge (`test_llm_judge_eval.py`)

**What it tests:** Answer quality on two axes borrowed from RAGAS:

| Metric | Question | Score |
|---|---|---|
| **Faithfulness** | Does the answer stay grounded in the evidence? Does it invent facts? | 0.0 / 0.5 / 1.0 |
| **Answer relevance** | Does the answer actually address the question asked? | 0.0 / 0.5 / 1.0 |

**How it works:**

For each eval case the test:
1. Runs the full `ResumeAgent` to get `(answer, evidence)`.
2. Calls a judge LLM with two separate scoring prompts.
3. Asserts both scores meet the per-case thresholds.

```
faithfulness judge prompt:
  Given the evidence provided to the AI and the AI's answer,
  score whether every factual claim is supported by evidence.
  Return {"score": <0.0|0.5|1.0>, "reason": "..."}

relevance judge prompt:
  Given the user's question and the AI's answer,
  score whether the answer actually addresses the question.
  Return {"score": <0.0|0.5|1.0>, "reason": "..."}
```

The `hallucination_probe` case specifically asks about Kubernetes and
LangChain (absent from the resume) to verify the agent does not fabricate
experience with technologies Lu has not used.

**Gate:** Only runs when `JUDGE_EVAL=1` is set.  Not part of standard CI.
Run manually or in a periodic eval workflow:

```bash
cd backend
JUDGE_EVAL=1 AI_PROVIDER=qwen QWEN_API_KEY=sk-... \
    uv run pytest tests/test_llm_judge_eval.py -v

# Full report (all cases, printed table):
JUDGE_EVAL=1 AI_PROVIDER=qwen QWEN_API_KEY=sk-... \
    uv run python tests/test_llm_judge_eval.py
```

**Why not use RAGAS directly?**

- RAGAS's `TestsetGenerator` uses a Knowledge Graph pipeline designed for
  large document corpora (hundreds of pages).  This backend has 8 highly
  structured resume facts — the graph overhead adds no value.
- RAGAS's library depends on `tiktoken` and other packages incompatible
  with the Cloudflare Python Workers environment.
- The approach here borrows RAGAS's two core ideas (reverse question
  generation + LLM-as-judge scoring) and implements them in ~250 lines
  that integrate directly with the existing harness.

---

### Summary

| Layer | File | LLM calls | Runs in CI | Purpose |
|---|---|---|---|---|
| Retrieval | `test_retrieval_eval.py` | No | Always | Catch search regressions |
| Agent regression | `test_agent_eval.py` | Yes (agent) | Always | Catch answer regressions |
| LLM-as-judge | `test_llm_judge_eval.py` | Yes (agent + judge) | `JUDGE_EVAL=1` | Score answer quality |
| Question generator | `scripts/generate_synthetic_questions.py` | Yes (one-time) | Manual | Expand GOLD set |

## Suggested File Structure

```text
backend/src/app/
  main.py
  models.py
  resume_data.py
  harness/
    __init__.py
    agent.py
    events.py
    prompts.py
    router.py
    tools.py
    openai_client.py
    observability.py
backend/tests/
  eval_cases.json
  test_eval_cases.py
```

## Implementation Plan

### Phase 1: Harness Without OpenAI

- Move request/response Pydantic models into `models.py`.
- Move search logic into `harness/tools.py`.
- Add `harness/agent.py` that returns the current deterministic answer.
- Keep `/api/chat` behavior unchanged.
- Add eval tests for deterministic path.

### Phase 2: Real OpenAI Non-streaming

- Add `OPENAI_API_KEY` and `OPENAI_MODEL`.
- Add `openai_client.py`.
- Let the model call `search_resume_facts`.
- Execute tool calls in backend.
- Return grounded final answer and evidence.
- Fallback to deterministic answer if OpenAI key is missing.

### Phase 3: Streaming

- Add `/api/chat/stream`.
- Implement SSE event schema.
- Frontend consumes `answer_delta` and `evidence`.
- Keep `/api/chat` for fallback and testing.

V1 implementation note: the website receives real SSE streaming events from the backend. The first production cut may stream the harness-level answer chunks after tool execution. Token-level OpenAI streaming can be added inside `openai_client.py` without changing the frontend event contract.

### Phase 4: CI/CD and Secrets

- Add GitHub secret `OPENAI_API_KEY`.
- Add Cloudflare Worker secret:

```bash
cd backend
uv run pywrangler secret put OPENAI_API_KEY
uv run pywrangler secret put OPENAI_MODEL
```

- Extend GitHub Actions to run eval tests before deploy.

## V1 Acceptance Criteria

- Website chat calls `/api/chat/stream` by default.
- API supports non-streaming fallback through `/api/chat`.
- At least one tool call is executed for normal experience questions.
- The answer cites structured resume evidence.
- Streaming events do not expose raw tool JSON or reasoning text to the user.
- Missing `OPENAI_API_KEY` degrades to deterministic resume answers.
- GitHub Actions deploys the backend after tests pass.
