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

整体评估思路来自 RAGAS 的核心设计：**先有答案（文档内容），再用 LLM 逆推问题，
最后用 LLM 评判答案质量**。本站对这套思路做了裁剪适配，分三层落地。

```
Phase 0  构建 Knowledge Graph（一次性离线）
              ↓
Phase 1  从图逆向生成问题集（一次性离线，生成 synthetic_gold.json）
              ↓
Phase 2  用问题集跑检索评估（Layer 1，无 LLM，每次 CI 跑）
Phase 3  用问题集跑 Agent 端到端测试（Layer 2，每次 CI 跑）
Phase 4  LLM-as-Judge 打答案质量分（Layer 3，JUDGE_EVAL=1 手动跑）
```

---

### Phase 0 — 构建 Knowledge Graph

RAGAS 原版是为大规模文档设计的：先把上千页文本切 chunk，用 NER 提取实体，
再用实体重叠度建边，形成一个真实的图结构。

本站的数据规模是 8 条高度结构化的 `RESUME_FACTS`，每条已经包含了
`id`、`skills`、`evidence` 这些结构化字段，直接用字段作为节点和边，
不需要再跑 NER。

**节点（Node）**：每条 RESUME_FACT 是一个文档节点，属性包括：

```python
# 来自 resume_loader.py — build_resume_facts()
{
  "id":          "agent-runtime",          # 节点 ID
  "title":       "Agent Runtime Upgrade",  # 节点标签
  "company":     "Zalando",
  "summary_en":  "...",                    # 检索文本（EN）
  "summary_zh":  "...",                    # 检索文本（ZH）
  "skills":      ["Tool Calling", "Streaming", "OpenAI Responses API", ...],
  "evidence":    ["-25% avg TTFT", "-25% P95 TTFT", ...],
}
```

**边（Edge）**：两个节点如果共享同一个 skill，则建立一条关系边。
例如 `agent-runtime` 和 `product-comparison` 都有 `Tool Calling`，
二者之间就有一条 `shares_skill: Tool Calling` 的边。

```python
# 伪代码：边构建逻辑（在 generate_synthetic_questions.py 中实现）
edges = {}
for fact in RESUME_FACTS:
    for skill in fact["skills"]:
        edges.setdefault(skill, []).append(fact["id"])
# → {"Tool Calling": ["agent-runtime", "product-comparison", "profile"], ...}
# → {"Evaluation": ["personalization", "text2sql", "profile"], ...}
```

这样就得到了一个以 RESUME_FACT 为节点、以共享技能为边的 Knowledge Graph：

```
profile ──── Tool Calling ──── agent-runtime
                │
           product-comparison
                │
             Streaming ──── agent-runtime

text2sql ──── Evaluation ──── personalization
                │
            rag-chatbot
```

---

### Phase 1 — 从图逆向生成问题集

**RAGAS 的逻辑**：遍历图，挑出节点或节点对，用 LLM 根据内容逆推问题，
同时把"正确答案来自哪个节点"记录下来，得到带 ground truth 的测试集。

本站的实现在 `scripts/generate_synthetic_questions.py`，分两类问题：

**单节点问题（Single-hop）**：只看一个 fact，生成具体问题。
对应 RAGAS 的 `SingleHopSpecificQuerySynthesizer`。

```python
# 每个 fact 生成 4 EN + 4 ZH 问题
prompt = """
Resume fact:
  Title: Agent Runtime Upgrade and Real-Time Response Optimization
  Company: Zalando
  Summary: Upgraded the main Zalando Assistant Agent Runtime...
  Key evidence: -25% avg TTFT, -25% P95 TTFT, Streaming state machine

Generate 4 questions:
- 2 specific (ask about a concrete metric, technology, or decision)
- 1 multi-topic (reference 2 skills or outcomes from this fact)
- 1 follow-up (something a recruiter would naturally ask next)
"""
# → ["What specific latency improvement did Lu achieve for Streaming?",
#    "How did Lu handle event ordering in multi-step Agent flows?",
#    "How does Lu's Streaming work relate to Tool Calling?",
#    "What drove the decision to migrate to OpenAI Responses API?"]
```

**跨节点问题（Multi-hop）**：沿图中的边，把两个共享技能的 fact 合并，
生成需要同时引用两个 fact 的问题。对应 RAGAS 的 `MultiHopSpecificQuerySynthesizer`。

```python
# 找到通过 "Evaluation" 连接的 text2sql 和 personalization
# → 生成跨项目问题
prompt = """
Fact A: Text2SQL agent — developed 1,000+ eval cases from real business queries
Fact B: Personalization — built evaluation process based on ~800 real scenarios

Generate a question that requires knowledge from BOTH facts.
"""
# → "How has Lu approached building evaluation datasets across different AI projects?"
```

生成结果写入 `tests/synthetic_gold.json`，每条记录格式：

```json
{
  "id": "agent-runtime_en_0",
  "source_fact_id": "agent-runtime",        // single-hop: 一个来源
  "query": "What latency improvement did Lu achieve for Streaming TTFT?",
  "language": "en",
  "expected_doc_ids": ["agent-runtime"]     // 检索时应命中的节点
}
```

跨节点问题的 `expected_doc_ids` 会包含两个 fact：

```json
{
  "id": "multihop_evaluation_en_0",
  "source_fact_id": "text2sql+personalization",
  "query": "How has Lu approached building evaluation datasets across projects?",
  "language": "en",
  "expected_doc_ids": ["text2sql", "personalization"]
}
```

运行一次生成约 **64–80 条**问题（8 个 fact × 4 EN + 4 ZH，加若干跨节点问题）：

```bash
cd backend
AI_PROVIDER=qwen QWEN_API_KEY=sk-... \
    uv run python scripts/generate_synthetic_questions.py
```

---

### Phase 2 — 检索评估（Layer 1，`test_retrieval_eval.py`）

用生成的问题集测试 BM25 + FAISS 混合检索质量。**不需要 LLM，每次 CI 都跑。**

`synthetic_gold.json` 存在时自动加载，合并到 GOLD 集：

```python
# test_retrieval_eval.py
GOLD = [  # 手写的 19 条基准
    ("TTFT latency optimization streaming", "en", {"agent-runtime"}),
    ...
]
SYNTHETIC = _load_synthetic()   # 从 synthetic_gold.json 加载，不存在则 []
ALL_GOLD = GOLD + SYNTHETIC     # CI 跑 GOLD，本地可跑 ALL_GOLD
```

每条问题检索 top-3，断言 `expected_doc_ids` 中至少有一个命中：

```
✓ What latency improvement did Lu achieve... | expected: agent-runtime | got: [agent-runtime, profile, ...]
✓ 汪露怎么解决首屏冷启动问题？           | expected: personalization  | got: [personalization, ...]
✗ How has Lu approached eval datasets...    | expected: text2sql+perso | got: [rag-chatbot, ...]  ← 跨节点难
```

报告 P@K / R@K / MRR / Hit Rate，发现检索薄弱点后可以回头调整 BM25 权重
或补充 FAISS embedding。

---

### Phase 3 — Agent 端到端回归（Layer 2，`test_agent_eval.py`）

用手写的关键问题跑完整 Agent 链路（intent routing → retrieval → LLM → evidence），
做关键词级别的确定性断言。**每次 CI 跑，答案里缺关键词就报错。**

```json
{
  "id": "streaming_tool_calling_en",
  "message": "Show Lu's Streaming and Tool Calling experience.",
  "language": "en",
  "must_include": ["Agent Runtime Upgrade", "Tool Calling", "Streaming", "25%"],
  "expected_project_ids": ["agent-runtime"]
}
```

这一层不评价"答案好不好"，只检查"答案有没有漏掉关键事实"。
改了 prompt 或调了检索权重之后，这层是第一道保护网。

---

### Phase 4 — LLM-as-Judge 质量评分（Layer 3，`test_llm_judge_eval.py`）

用另一个 LLM 评判 Agent 答案的质量，借鉴 RAGAS 的两个核心指标：

| 指标 | 问的问题 | 评分 |
|---|---|---|
| **Faithfulness（忠实度）** | 答案里的每个事实声明，在 evidence 里都能找到依据吗？ | 0.0 / 0.5 / 1.0 |
| **Answer Relevance（相关性）** | 答案有没有回答用户的问题？有没有跑题？ | 0.0 / 0.5 / 1.0 |

**工作流程**：

```
用户问题
    ↓
ResumeAgent.answer()  →  (answer_text, evidence_cards)
    ↓                              ↓
relevance judge                faithfulness judge
  prompt:                        prompt:
  "Does this answer              "Does every claim in
   address the question?"         this answer appear
                                  in the evidence?"
    ↓                              ↓
  score 0/0.5/1.0              score 0/0.5/1.0
    ↓                              ↓
assert >= min_relevance      assert >= min_faithfulness
```

其中 `hallucination_probe` case 专门问 Kubernetes 和 LangChain（简历里没有），
期望 faithfulness=1.0（Agent 没有编造这些经历）、relevance=0.5（只能如实说没有）。

**只在手动跑时触发**，不进 CI：

```bash
cd backend
JUDGE_EVAL=1 AI_PROVIDER=qwen QWEN_API_KEY=sk-... \
    uv run pytest tests/test_llm_judge_eval.py -v

# 或打印完整报告表格：
JUDGE_EVAL=1 AI_PROVIDER=qwen QWEN_API_KEY=sk-... \
    uv run python tests/test_llm_judge_eval.py
```

---

### 完整流程图

```
RESUME_FACTS (8 个结构化 fact)
      │
      ▼
  [Phase 0] 构建 Knowledge Graph
      │  节点 = fact，边 = 共享 skill
      │
      ▼
  [Phase 1] LLM 逆向生成问题
      │  单节点问题（4 EN + 4 ZH / fact）
      │  跨节点问题（沿 skill 边，合并两个 fact）
      │  → synthetic_gold.json（~70 条，带 ground truth）
      │
      ├──▶ [Layer 1] 检索评估（test_retrieval_eval.py）
      │       BM25+FAISS 检索，断言 top-3 命中
      │       P@K / R@K / MRR / Hit Rate
      │       无 LLM，CI 每次跑
      │
      ├──▶ [Layer 2] Agent 回归（test_agent_eval.py）
      │       完整 Agent 链路，关键词断言
      │       每次 CI 跑
      │
      └──▶ [Layer 3] LLM-as-Judge（test_llm_judge_eval.py）
              Faithfulness + Answer Relevance
              手动跑（JUDGE_EVAL=1）
```

---

### 三层对比

| 层 | 文件 | LLM 调用 | CI 运行 | 发现的问题 |
|---|---|---|---|---|
| 检索 | `test_retrieval_eval.py` | 无 | 每次 | 检索漏召回、BM25 权重不对 |
| Agent 回归 | `test_agent_eval.py` | Agent | 每次 | Prompt 变更导致关键信息丢失 |
| LLM Judge | `test_llm_judge_eval.py` | Agent + Judge | 手动 | 答案编造事实、跑题、质量退化 |
| 问题生成 | `scripts/generate_synthetic_questions.py` | 一次性 | 手动 | 扩充测试集覆盖度 |

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
