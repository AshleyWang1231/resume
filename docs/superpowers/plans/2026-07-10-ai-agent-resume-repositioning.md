# AI Agent Resume Repositioning Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reposition the resume site from a general AI software portfolio into a senior AI Agent / AI Engineer portfolio that demonstrates production agent architecture, evaluation, reliability, full-stack ownership, and measurable impact.

**Architecture:** Keep the current static frontend + FastAPI/Python Worker backend. Add a structured backend content layer for market requirements, senior capability signals, project cards, and architecture/evaluation proof; then make the frontend consume and render those signals as an executive narrative instead of a flat resume page.

**Tech Stack:** Static HTML/CSS/JavaScript, FastAPI, Pydantic, Python Worker, pytest, BM25/FAISS retrieval fallback, Server-Sent Events.

## Global Constraints

- Do not read or commit `backend/.env`; use `.env.example` only for documented configuration.
- Preserve bilingual English/Chinese UX.
- Preserve `/api/chat`, `/api/chat/stream`, `/api/projects`, `/api/architecture`, and `/health` compatibility.
- Every implementation task ends with tests and a git commit.
- Use no new frontend framework or build step; keep GitHub Pages static deploy.
- Use no new backend dependency unless tests prove current dependencies cannot support the requirement.
- Resume claims must stay grounded in existing project facts: no invented employers, dates, credentials, or metrics.

---

## File Structure

- `docs/superpowers/plans/2026-07-10-ai-agent-resume-repositioning.md`: this implementation plan.
- `docs/research/ai-agent-engineer-jd-signals.md`: curated JD signal brief used to justify the redesign.
- `backend/src/app/resume_loader.py`: extend structured facts with senior-AI capability proof points and market-alignment signals.
- `backend/src/app/resume_data.py`: expose structured constants for JD signals, capabilities, architecture layers, and suggested questions.
- `backend/src/app/models.py`: add Pydantic response models for capabilities and market signals.
- `backend/src/app/main.py`: add `/api/capabilities` and `/api/market-signals`; update existing project and architecture endpoints to use shared content.
- `backend/src/app/harness/router.py`: add routing hints for market/JD/senior questions.
- `backend/src/app/harness/prompts.py`: update agent prompt to answer senior AI Engineer/JD fit questions from evidence.
- `backend/tests/test_content_endpoints.py`: new endpoint contract tests.
- `backend/tests/eval_cases.json`: add JD/senior-positioning eval cases.
- `script.js`: fetch new backend content, render new sections, update terminal suggestions, and keep static fallback data.
- `index.html`: update page structure for senior narrative sections.
- `styles.css`: redesign layout and components for stronger senior positioning.
- `README.md` and `backend/README.md`: document the new positioning and endpoints.

---

### Task 1: Research brief and backend content contract

**Files:**
- Create: `docs/research/ai-agent-engineer-jd-signals.md`
- Modify: `backend/src/app/models.py`
- Modify: `backend/src/app/resume_data.py`
- Modify: `backend/src/app/main.py`
- Test: `backend/tests/test_content_endpoints.py`

**Interfaces:**
- Produces: `MarketSignal`, `CapabilitySignal`, `MarketSignalsResponse`, `CapabilitiesResponse` Pydantic models.
- Produces: `JD_SIGNALS`, `SENIOR_CAPABILITIES` constants.
- Produces: `GET /api/market-signals` and `GET /api/capabilities`.

- [ ] **Step 1: Write research brief**

Create `docs/research/ai-agent-engineer-jd-signals.md` with these sections:

```markdown
# AI Agent / AI Engineer JD Signals — 2026-07-10

## High-frequency requirements

1. Production LLM applications: ship user-facing AI features, not just prototypes.
2. Agent orchestration: tool calling, multi-step workflows, state, memory, and planning loops.
3. Retrieval and grounding: RAG, hybrid search, embeddings, reranking, citations/evidence.
4. Evaluation: offline eval suites, regression tests, LLM-as-judge, quality metrics, human feedback loops.
5. Reliability and observability: latency, tracing, fallbacks, guardrails, error handling, and measurable SLIs.
6. Full-stack product sense: frontend UX for AI latency/progress plus backend APIs and data contracts.
7. Data and platform integration: SQL, structured data, enterprise systems, permissions, and safe execution.
8. Model/provider fluency: OpenAI/Anthropic-compatible APIs, streaming, structured outputs, provider trade-offs.
9. Senior ownership: ambiguous problem decomposition, architecture decisions, cross-functional leadership, mentoring.
10. Business impact: quantified outcomes tied to revenue, engagement, operational efficiency, risk reduction.

## Senior-level signals the site should surface

- Owns architecture end-to-end, including runtime, state, evaluation, deployment, and rollback/fallback strategy.
- Can translate vague product goals into reliable agent workflows and measurable acceptance criteria.
- Separates model reasoning from deterministic business logic where stability matters.
- Treats evaluation as a product system: curated test sets, CI regression, LLM-as-judge, and evidence grounding.
- Demonstrates production constraints: latency, P95/P99, streaming UX, caching, high concurrency, and observability.
- Shows business domains beyond demos: e-commerce user traffic and financial-services structured data.

## Resume-site implications

- Lead with senior positioning, not a generic title.
- Add a market-fit section that maps JD requirements to concrete evidence.
- Add architecture and evaluation proof sections before project details.
- Make projects comparable using Challenge → Architecture → Senior signal → Outcome.
- Make the chat agent itself part of the portfolio proof.

## Source themes

Public JD pages and hiring guides for AI Engineer / LLM Engineer / Agent Engineer roles consistently emphasize production LLM systems, RAG, tool use, evaluation, observability, and cross-functional product ownership. This brief is used as a synthesis baseline for the local portfolio rewrite; individual site copy remains grounded only in Lu Wang's resume facts.
```

- [ ] **Step 2: Add failing endpoint tests**

Create `backend/tests/test_content_endpoints.py`:

```python
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_market_signals_endpoint_maps_jd_requirements_to_resume_evidence():
    response = client.get("/api/market-signals")
    assert response.status_code == 200
    data = response.json()
    assert data["title_en"] == "What AI Agent roles are screening for"
    assert len(data["signals"]) >= 6
    ids = {item["id"] for item in data["signals"]}
    assert "agent-orchestration" in ids
    assert "evaluation" in ids
    orchestration = next(item for item in data["signals"] if item["id"] == "agent-orchestration")
    assert "Tool Calling" in orchestration["evidence_en"]
    assert orchestration["proof_project_ids"]


def test_capabilities_endpoint_exposes_senior_capability_signals():
    response = client.get("/api/capabilities")
    assert response.status_code == 200
    data = response.json()
    assert data["title_en"] == "Senior AI engineering capability map"
    assert len(data["capabilities"]) >= 5
    capability_ids = {item["id"] for item in data["capabilities"]}
    assert "runtime-architecture" in capability_ids
    assert "evaluation-systems" in capability_ids
    runtime = next(item for item in data["capabilities"] if item["id"] == "runtime-architecture")
    assert "Streaming" in runtime["evidence_en"]
    assert "agent-runtime" in runtime["proof_project_ids"]
```

- [ ] **Step 3: Run tests to verify failure**

Run: `cd backend && uv run pytest tests/test_content_endpoints.py -v`

Expected: FAIL because `/api/market-signals` and `/api/capabilities` do not exist.

- [ ] **Step 4: Add Pydantic models**

Append to `backend/src/app/models.py`:

```python
class MarketSignal(BaseModel):
    id: str
    requirement_en: str
    requirement_zh: str
    evidence_en: str
    evidence_zh: str
    senior_signal_en: str
    senior_signal_zh: str
    proof_project_ids: list[str]


class MarketSignalsResponse(BaseModel):
    title_en: str
    title_zh: str
    summary_en: str
    summary_zh: str
    signals: list[MarketSignal]


class CapabilitySignal(BaseModel):
    id: str
    title_en: str
    title_zh: str
    narrative_en: str
    narrative_zh: str
    evidence_en: str
    evidence_zh: str
    proof_project_ids: list[str]
    keywords: list[str]


class CapabilitiesResponse(BaseModel):
    title_en: str
    title_zh: str
    summary_en: str
    summary_zh: str
    capabilities: list[CapabilitySignal]
```

- [ ] **Step 5: Add structured content constants**

Append to `backend/src/app/resume_data.py`:

```python
JD_SIGNALS = [
    {
        "id": "agent-orchestration",
        "requirement_en": "Agent orchestration, tool calling, workflow design, and state management",
        "requirement_zh": "Agent 编排、工具调用、工作流设计与状态管理",
        "evidence_en": "Built Zalando Assistant Agent Runtime with Tool Calling, typed Streaming events, multi-turn state, and OpenAI Responses API migration.",
        "evidence_zh": "构建 Zalando Assistant Agent Runtime，覆盖 Tool Calling、类型化 Streaming 事件、多轮状态与 OpenAI Responses API 迁移。",
        "senior_signal_en": "Can design the runtime loop, not only prompt a model.",
        "senior_signal_zh": "不仅会写 Prompt，而是能设计 Agent Runtime 循环。",
        "proof_project_ids": ["agent-runtime", "product-comparison"],
    },
    {
        "id": "evaluation",
        "requirement_en": "Evaluation systems, regression suites, LLM-as-judge, and quality gates",
        "requirement_zh": "评估体系、回归测试集、LLM-as-Judge 与质量门控",
        "evidence_en": "Built 1,000+ Text2SQL eval cases, 800+ product-detail scenarios, RAGAS-inspired retrieval and judge tests for this site.",
        "evidence_zh": "构建 1,000+ Text2SQL 评估用例、800+ 商品场景，并为本站搭建 RAGAS 思路的检索与 Judge 测试。",
        "senior_signal_en": "Treats evals as production infrastructure and regression protection.",
        "senior_signal_zh": "将评估作为生产基础设施与回归保护。",
        "proof_project_ids": ["text2sql", "rag-chatbot", "agent-runtime"],
    },
    {
        "id": "grounding-rag",
        "requirement_en": "RAG, hybrid retrieval, embeddings, reranking, and grounded answers",
        "requirement_zh": "RAG、混合检索、Embedding、Rerank 与可信回答",
        "evidence_en": "Built LlamaIndex + FAISS RAG pipeline, dual-layer field/value reranking, and evidence-card retrieval in the resume agent.",
        "evidence_zh": "构建 LlamaIndex + FAISS RAG、字段+值双层 Rerank，以及本站 evidence-card 检索。",
        "senior_signal_en": "Understands retrieval as a reliability layer, not a demo add-on.",
        "senior_signal_zh": "把检索视为可靠性层，而不是 Demo 附件。",
        "proof_project_ids": ["rag-chatbot", "text2sql"],
    },
    {
        "id": "latency-observability",
        "requirement_en": "Latency, observability, streaming UX, fallbacks, and production reliability",
        "requirement_zh": "延迟、可观测性、Streaming 体验、降级与生产可靠性",
        "evidence_en": "Reduced TTFT by 25%, reduced cold-start by 60%, added request logging, SSE events, provider fallback, and deterministic evidence fallback.",
        "evidence_zh": "TTFT 降低 25%，冷启动降低 60%，并具备请求日志、SSE 事件、多 Provider 降级和确定性证据兜底。",
        "senior_signal_en": "Optimizes AI systems against user-perceived latency and failure modes.",
        "senior_signal_zh": "围绕用户感知延迟和失败模式优化 AI 系统。",
        "proof_project_ids": ["agent-runtime", "personalization"],
    },
    {
        "id": "product-fullstack",
        "requirement_en": "Full-stack AI product delivery and user-facing interaction design",
        "requirement_zh": "全栈 AI 产品交付与面向用户的交互设计",
        "evidence_en": "Owned backend runtime, API contracts, streaming frontend terminal, evidence rendering, and product decision flows.",
        "evidence_zh": "覆盖后端 Runtime、API 契约、前端流式终端、证据渲染与商品决策流程。",
        "senior_signal_en": "Can turn model capability into a shippable product surface.",
        "senior_signal_zh": "能把模型能力转化为可上线的产品体验。",
        "proof_project_ids": ["product-comparison", "personalization", "agent-runtime"],
    },
    {
        "id": "enterprise-data",
        "requirement_en": "Enterprise data integration, SQL, permissions, and domain constraints",
        "requirement_zh": "企业数据集成、SQL、权限与业务约束",
        "evidence_en": "Built bank Text2SQL agent, SQL validation/retry, access-control domain model, reporting pipeline, and zero-downtime migration.",
        "evidence_zh": "构建银行 Text2SQL Agent、SQL 校验重试、权限领域模型、报表流水线与零感知迁移。",
        "senior_signal_en": "Can operate AI features inside regulated and data-heavy enterprise systems.",
        "senior_signal_zh": "能在强约束、重数据的企业系统中落地 AI 能力。",
        "proof_project_ids": ["text2sql", "pricing-management"],
    },
]

SENIOR_CAPABILITIES = [
    {
        "id": "runtime-architecture",
        "title_en": "Agent runtime architecture",
        "title_zh": "Agent Runtime 架构",
        "narrative_en": "Designs the loop that coordinates tools, state, streaming, providers, and fallback behavior.",
        "narrative_zh": "设计协调工具、状态、Streaming、Provider 与降级行为的运行循环。",
        "evidence_en": "Zalando Assistant runtime: Tool Calling, typed SSE, multi-turn state, OpenAI Responses API migration, -25% TTFT.",
        "evidence_zh": "Zalando Assistant Runtime：Tool Calling、类型化 SSE、多轮状态、Responses API 迁移，TTFT -25%。",
        "proof_project_ids": ["agent-runtime"],
        "keywords": ["Agent Runtime", "Tool Calling", "Streaming", "State Machine"],
    },
    {
        "id": "evaluation-systems",
        "title_en": "Evaluation and regression systems",
        "title_zh": "评估与回归体系",
        "narrative_en": "Builds eval loops that make AI changes measurable and safe to ship.",
        "narrative_zh": "构建让 AI 改动可度量、可安全上线的评估闭环。",
        "evidence_en": "1,000+ Text2SQL cases, 800+ recommendation scenarios, retrieval MRR and LLM-as-judge tests in CI/manual gates.",
        "evidence_zh": "1,000+ Text2SQL 用例、800+ 推荐场景、检索 MRR 与 LLM-as-Judge 测试。",
        "proof_project_ids": ["text2sql", "rag-chatbot"],
        "keywords": ["Evaluation", "RAGAS", "LLM-as-Judge", "Regression"],
    },
    {
        "id": "latency-reliability",
        "title_en": "Latency and production reliability",
        "title_zh": "延迟与生产可靠性",
        "narrative_en": "Optimizes AI products for real user traffic, not only benchmark demos.",
        "narrative_zh": "面向真实用户流量优化 AI 产品，而不仅是 Demo Benchmark。",
        "evidence_en": "-25% TTFT, -60% cold-start, -70% profile calls, deterministic fallback when model providers fail.",
        "evidence_zh": "TTFT -25%、冷启动 -60%、画像调用 -70%，模型失败时有确定性兜底。",
        "proof_project_ids": ["agent-runtime", "personalization"],
        "keywords": ["TTFT", "P99", "Caching", "Fallback"],
    },
    {
        "id": "model-code-boundary",
        "title_en": "Model/code boundary design",
        "title_zh": "模型与代码边界设计",
        "narrative_en": "Keeps probabilistic reasoning and deterministic business logic in the right places.",
        "narrative_zh": "把概率式推理和确定性业务逻辑放在各自合适的位置。",
        "evidence_en": "Product Comparison Skill: model handles intent and summary; deterministic code owns product resolution, discount math, and rendering markers.",
        "evidence_zh": "Product Comparison：模型负责意图和总结，代码负责商品定位、折扣计算与渲染标记。",
        "proof_project_ids": ["product-comparison"],
        "keywords": ["Structured Output", "Deterministic Rendering", "Multi-turn"],
    },
    {
        "id": "enterprise-ai",
        "title_en": "Enterprise AI and data systems",
        "title_zh": "企业 AI 与数据系统",
        "narrative_en": "Connects agent workflows to SQL, permissions, reporting, and operational data constraints.",
        "narrative_zh": "将 Agent 工作流连接到 SQL、权限、报表和运营数据约束。",
        "evidence_en": "Bank Text2SQL, SQL validation/retry, DDD access control, Tablesaw reporting, zero-impact migration.",
        "evidence_zh": "银行 Text2SQL、SQL 校验重试、DDD 权限、Tablesaw 报表与零感知迁移。",
        "proof_project_ids": ["text2sql", "pricing-management"],
        "keywords": ["Text2SQL", "SQL Validation", "DDD", "Enterprise Data"],
    },
]
```

- [ ] **Step 6: Add endpoints**

Modify imports in `backend/src/app/main.py`:

```python
from app.models import (
    ArchitectureEdge,
    ArchitectureNode,
    ArchitectureResponse,
    CapabilitiesResponse,
    CapabilitySignal,
    ChatRequest,
    ChatResponse,
    MarketSignal,
    MarketSignalsResponse,
    ProjectCard,
)
from app.resume_data import JD_SIGNALS, SENIOR_CAPABILITIES
```

Add routes before `/api/projects`:

```python
@app.get("/api/market-signals", response_model=MarketSignalsResponse)
async def market_signals() -> MarketSignalsResponse:
    return MarketSignalsResponse(
        title_en="What AI Agent roles are screening for",
        title_zh="AI Agent 岗位正在筛选什么能力",
        summary_en=(
            "Current AI Agent / AI Engineer roles screen for production LLM systems, "
            "tool orchestration, grounding, evaluation, reliability, and senior ownership. "
            "This map connects those signals to concrete resume evidence."
        ),
        summary_zh=(
            "当前 AI Agent / AI Engineer 岗位重点筛选生产级 LLM 系统、工具编排、可信检索、"
            "评估体系、可靠性以及 senior ownership。这里把这些要求映射到具体项目证据。"
        ),
        signals=[MarketSignal(**item) for item in JD_SIGNALS],
    )


@app.get("/api/capabilities", response_model=CapabilitiesResponse)
async def capabilities() -> CapabilitiesResponse:
    return CapabilitiesResponse(
        title_en="Senior AI engineering capability map",
        title_zh="Senior AI 工程能力地图",
        summary_en=(
            "A senior AI engineer is evaluated by architecture judgment, production reliability, "
            "eval discipline, product ownership, and the ability to draw a clean boundary between "
            "model reasoning and deterministic systems."
        ),
        summary_zh=(
            "Senior AI Engineer 的核心不只是会调用模型，而是架构判断、生产可靠性、评估纪律、"
            "产品 ownership，以及能清晰划分模型推理与确定性系统边界。"
        ),
        capabilities=[CapabilitySignal(**item) for item in SENIOR_CAPABILITIES],
    )
```

- [ ] **Step 7: Run endpoint tests**

Run: `cd backend && uv run pytest tests/test_content_endpoints.py -v`

Expected: PASS.

- [ ] **Step 8: Commit backend content contract**

Run:

```bash
git add docs/research/ai-agent-engineer-jd-signals.md backend/src/app/models.py backend/src/app/resume_data.py backend/src/app/main.py backend/tests/test_content_endpoints.py
git commit -m "Add senior AI agent content endpoints"
```

---

### Task 2: Backend retrieval and agent answer alignment

**Files:**
- Modify: `backend/src/app/resume_loader.py`
- Modify: `backend/src/app/harness/router.py`
- Modify: `backend/src/app/harness/prompts.py`
- Modify: `backend/tests/eval_cases.json`
- Test: `backend/tests/test_agent_eval.py`

**Interfaces:**
- Consumes: `JD_SIGNALS`, `SENIOR_CAPABILITIES` from Task 1.
- Produces: resume facts with IDs `senior-ai-fit` and `resume-agent-site` searchable by the chat agent.

- [ ] **Step 1: Add eval cases first**

Append these cases to `backend/tests/eval_cases.json` before the closing array bracket:

```json
,
  {
    "id": "senior_ai_fit_en",
    "message": "How does Lu match Senior AI Agent Engineer job requirements?",
    "language": "en",
    "must_include": ["Agent Runtime", "evaluation", "production"],
    "expected_project_ids": ["senior-ai-fit"]
  },
  {
    "id": "resume_agent_site_zh",
    "message": "这个简历网站本身如何体现 AI Agent 工程能力？",
    "language": "zh",
    "must_include": ["本站", "Streaming", "评估"],
    "expected_project_ids": ["resume-agent-site"]
  }
```

- [ ] **Step 2: Run eval to verify failure**

Run: `cd backend && uv run pytest tests/test_agent_eval.py -v`

Expected: FAIL because expected project IDs do not exist.

- [ ] **Step 3: Add two resume facts**

In `backend/src/app/resume_loader.py`, add two facts before `return facts`:

```python
    facts.append({
        "id": "senior-ai-fit",
        "company": "Lu Wang · 汪露",
        "title": "Senior AI Agent Engineer Fit",
        "summary_en": _strip(
            "Lu's experience maps directly to senior AI Agent Engineer requirements: production Agent Runtime, "
            "Tool Calling, Streaming UX, RAG/Text2SQL grounding, evaluation systems, latency optimization, "
            "provider fallback, and enterprise data integration. The strongest evidence comes from Zalando's "
            "user-facing shopping assistant and Thoughtworks' bank Text2SQL/RAG systems."
        ),
        "summary_zh": _strip(
            "汪露的经验直接对应 Senior AI Agent Engineer 要求：生产级 Agent Runtime、Tool Calling、Streaming 体验、"
            "RAG/Text2SQL 可信检索、评估体系、延迟优化、多 Provider 降级以及企业数据集成。最强证据来自 "
            "Zalando 面向真实用户的购物助手，以及 Thoughtworks 银行 Text2SQL/RAG 系统。"
        ),
        "evidence": ["Agent Runtime", "Tool Calling", "Streaming", "evaluation", "production", "Text2SQL", "RAG"],
        "skills": ["Senior AI Engineer", "LLM Agent", "Evaluation", "Production Reliability", "Full-stack AI"],
    })

    facts.append({
        "id": "resume-agent-site",
        "company": "Lu Wang · 汪露",
        "title": "This Resume Site as an AI Agent System",
        "summary_en": _strip(
            "This resume site demonstrates the same engineering patterns it describes: FastAPI agent backend, "
            "Pydantic-validated tool schemas, hybrid retrieval over structured resume facts, multi-provider fallback, "
            "typed SSE Streaming, evidence cards, session state, and RAGAS-inspired retrieval and judge evaluations."
        ),
        "summary_zh": _strip(
            "本站本身展示了简历中描述的工程模式：FastAPI Agent 后端、Pydantic 校验工具 Schema、"
            "结构化简历事实的混合检索、多 Provider 降级、类型化 SSE Streaming、证据卡片、会话状态，"
            "以及 RAGAS 思路的检索与 Judge 评估。"
        ),
        "evidence": ["FastAPI", "Pydantic tool schemas", "Hybrid retrieval", "SSE Streaming", "evidence cards", "RAGAS-inspired evaluation"],
        "skills": ["Agent Runtime", "RAG", "Streaming", "Pydantic", "Evaluation", "Full-stack AI"],
    })
```

- [ ] **Step 4: Update router hints**

In `backend/src/app/harness/router.py`, ensure questions containing `senior`, `job`, `JD`, `岗位`, `要求`, `fit`, `match`, `简历网站`, or `本站` boost the new IDs. The returned intent should use `retrieval_hint=["senior-ai-fit", "resume-agent-site", "agent-runtime", "text2sql"]` for senior/JD fit questions and `retrieval_hint=["resume-agent-site", "agent-runtime"]` for site/backend questions.

- [ ] **Step 5: Update prompt focus**

In `backend/src/app/harness/prompts.py`, change the base rules sentence:

```python
"Prefer concise, hiring-manager-friendly answers with concrete evidence. "
```

to:

```python
"Prefer concise, hiring-manager-friendly answers with concrete evidence and senior-level framing when the question asks about role fit, job requirements, architecture, ownership, or production impact. "
```

- [ ] **Step 6: Run agent eval tests**

Run: `cd backend && uv run pytest tests/test_agent_eval.py -v`

Expected: PASS.

- [ ] **Step 7: Run backend regression tests**

Run: `cd backend && uv run pytest -v`

Expected: PASS.

- [ ] **Step 8: Commit backend retrieval alignment**

Run:

```bash
git add backend/src/app/resume_loader.py backend/src/app/harness/router.py backend/src/app/harness/prompts.py backend/tests/eval_cases.json
git commit -m "Align resume agent with senior AI role signals"
```

---

### Task 3: Frontend information architecture redesign

**Files:**
- Modify: `index.html`
- Modify: `script.js`
- Modify: `styles.css`
- Test: browser smoke test via local static server.

**Interfaces:**
- Consumes: `/api/market-signals`, `/api/capabilities`, `/api/projects`, `/api/architecture`.
- Produces: sections `#market`, `#capabilities`, `#proof`, `#projects`, `#system`, `#evaluation`, and `#contact`.

- [ ] **Step 1: Update navigation and hero markup**

In `index.html`:

- Change nav links to Market, Capabilities, Proof, System.
- Add a market section after hero with `<div class="market-grid" data-market-grid>`.
- Add a capability section with `<div class="senior-capability-grid" data-capability-grid>`.
- Rename current capabilities section copy to avoid duplicate `id="capabilities"`.
- Add a proof section before projects with a 3-card narrative: Runtime, Evaluation, Product/Business impact.

- [ ] **Step 2: Add static fallback data and fetchers**

In `script.js`, add `MARKET_SIGNALS_FALLBACK` and `SENIOR_CAPABILITIES_FALLBACK` matching backend response shape. Add:

```javascript
let cachedMarketSignals = null;
let cachedCapabilities = null;

async function loadMarketSignals() {
  try {
    const res = await fetch(`${API}/api/market-signals`);
    if (!res.ok) throw new Error("market failed");
    cachedMarketSignals = await res.json();
  } catch {
    cachedMarketSignals = MARKET_SIGNALS_FALLBACK;
  }
  renderMarketSignals(cachedMarketSignals);
}

async function loadCapabilities() {
  try {
    const res = await fetch(`${API}/api/capabilities`);
    if (!res.ok) throw new Error("capabilities failed");
    cachedCapabilities = await res.json();
  } catch {
    cachedCapabilities = SENIOR_CAPABILITIES_FALLBACK;
  }
  renderSeniorCapabilities(cachedCapabilities);
}
```

- [ ] **Step 3: Add renderers**

Add renderers that switch `*_en` vs `*_zh` by `lang`, escape all dynamic content, and render chips from keywords/project IDs:

```javascript
function renderMarketSignals(data) {
  const grid = $("[data-market-grid]");
  if (!grid || !data) return;
  grid.innerHTML = data.signals.map((item) => {
    const requirement = lang === "zh" ? item.requirement_zh : item.requirement_en;
    const evidence = lang === "zh" ? item.evidence_zh : item.evidence_en;
    const senior = lang === "zh" ? item.senior_signal_zh : item.senior_signal_en;
    return `<article class="market-card">
      <span class="market-id">${escapeHtml(item.id)}</span>
      <h3>${escapeHtml(requirement)}</h3>
      <p>${escapeHtml(evidence)}</p>
      <strong>${escapeHtml(senior)}</strong>
      <div class="proof-chips">${item.proof_project_ids.map((id) => `<span>${escapeHtml(id)}</span>`).join("")}</div>
    </article>`;
  }).join("");
}

function renderSeniorCapabilities(data) {
  const grid = $("[data-capability-grid]");
  if (!grid || !data) return;
  grid.innerHTML = data.capabilities.map((item, index) => {
    const title = lang === "zh" ? item.title_zh : item.title_en;
    const narrative = lang === "zh" ? item.narrative_zh : item.narrative_en;
    const evidence = lang === "zh" ? item.evidence_zh : item.evidence_en;
    return `<article class="senior-capability-card">
      <span>${String(index + 1).padStart(2, "0")}</span>
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(narrative)}</p>
      <small>${escapeHtml(evidence)}</small>
      <div class="skill-chips">${item.keywords.map((kw) => `<span>${escapeHtml(kw)}</span>`).join("")}</div>
    </article>`;
  }).join("");
}
```

- [ ] **Step 4: Add translations and commands**

Update `T.en` and `T.zh` with keys for market, proof, senior title, and new terminal suggestions. Update route map in `runCommand()`:

```javascript
const routes = {
  "/market": "market",
  "/capabilities": "capabilities",
  "/proof": "proof",
  "/projects": "projects",
  "/impact": "impact",
  "/system": "system",
  "/evaluation": "evaluation",
  "/contact": "contact",
};
```

- [ ] **Step 5: Add CSS components**

In `styles.css`, add styles for `.market-grid`, `.market-card`, `.senior-capability-grid`, `.senior-capability-card`, `.proof-grid`, `.proof-card`, `.proof-chips`, and update responsive breakpoints so all new grids collapse to one column under 800px.

- [ ] **Step 6: Initialize new loaders**

In `init()` call `loadMarketSignals()` and `loadCapabilities()` before `warmup()`.

- [ ] **Step 7: Smoke test frontend**

Run: `python3 -m http.server 8000`

Open: `http://localhost:8000`

Expected:
- Hero positions Lu as senior AI Agent / AI Engineer.
- Market section renders from fallback or backend.
- Capabilities section renders.
- Language toggle updates static and rendered dynamic content.
- Terminal still sends questions and routes `/market`, `/capabilities`, `/proof`, `/system`.

- [ ] **Step 8: Commit frontend redesign**

Run:

```bash
git add index.html script.js styles.css
git commit -m "Redesign frontend for senior AI agent positioning"
```

---

### Task 4: Documentation, review, evaluation, push

**Files:**
- Modify: `README.md`
- Modify: `backend/README.md`
- Test: full backend tests and git diff review.

**Interfaces:**
- Produces: documented endpoint list and local verification commands.

- [ ] **Step 1: Update README**

In `README.md`, change the description to mention senior AI Agent / AI Engineer positioning, JD-signal mapping, and the new content endpoints.

- [ ] **Step 2: Update backend README**

In `backend/README.md`, add:

```markdown
Additional content endpoints:

- `GET /api/market-signals` — maps current AI Agent / AI Engineer JD themes to resume evidence.
- `GET /api/capabilities` — senior AI engineering capability map used by the frontend.
```

- [ ] **Step 3: Run backend tests**

Run: `cd backend && uv run pytest -v`

Expected: PASS.

- [ ] **Step 4: Run frontend smoke commands**

Run: `python3 -m http.server 8000`

Expected: server starts without error. Manually verify homepage renders and browser console has no JavaScript syntax errors.

- [ ] **Step 5: Review diff**

Run:

```bash
git diff --stat
git diff --check
git status --short
```

Expected: no whitespace errors; only intended files changed.

- [ ] **Step 6: Commit docs/final verification**

Run:

```bash
git add README.md backend/README.md
git commit -m "Document senior AI resume repositioning"
```

- [ ] **Step 7: Push branch**

Run:

```bash
git push -u origin refactor-ai-agent-resume
```

Expected: branch pushed successfully.

---

## Self-Review

- Spec coverage: tasks cover JD synthesis, backend content contracts, retrieval/agent alignment, frontend IA redesign, docs, tests, commits, and push.
- Placeholder scan: no TBD/TODO/fill-later placeholders remain.
- Type consistency: `MarketSignal`, `CapabilitySignal`, `MarketSignalsResponse`, and `CapabilitiesResponse` are created before endpoint use; frontend renderer names match endpoint fields.
