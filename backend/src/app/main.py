from __future__ import annotations

import json
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, StreamingResponse

from app.config import load_local_env
from app.harness import ResumeAgent
from app.harness.events import stream_chat_response
from app.harness.observability import with_request_logging
from app.models import (
    ArchitectureEdge,
    ArchitectureNode,
    ArchitectureResponse,
    ChatRequest,
    ChatResponse,
    ProjectCard,
)


load_local_env()
app = FastAPI(title="Lu Wang Resume Agent API", version="2.0.0")
app.state.ai_binding = None
agent = ResumeAgent()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_log_middleware(request: Request, call_next):
    start = time.monotonic()
    response = await call_next(request)
    elapsed_ms = round((time.monotonic() - start) * 1000)
    print(json.dumps({
        "event": "http_request",
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
        "elapsed_ms": elapsed_ms,
    }))
    return response


@app.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "version": "2.0.0",
        "capabilities": ["multi-turn", "streaming", "tool-calling", "evidence-cards"],
    }


@app.get("/api/projects", response_model=list[ProjectCard])
async def projects() -> list[ProjectCard]:
    return [
        ProjectCard(
            id="agent-runtime",
            title="Agent Runtime & Streaming Architecture",
            company="Zalando",
            period="2025",
            summary_en=(
                "The original Zalando Assistant replied in bulk after every tool call, making the experience "
                "feel slow and giving users no visibility into what the agent was doing. "
                "I redesigned the streaming layer with a state machine that separates process states, "
                "business events, and user-visible text — so tool progress, intermediate results, and "
                "final answers each arrive as distinct typed events. Alongside this, I migrated the main runtime "
                "from Chat Completions to OpenAI Responses API, unified the Tool Calling path, and integrated "
                "product-detail tool retrieval so answers are grounded in live catalogue data rather than "
                "model memory. Benchmark result: average TTFT down ~25%, P95 TTFT down ~25%."
            ),
            summary_zh=(
                "原有链路在每次工具调用结束后整体输出，用户看不到任何过程状态，体验偏慢。"
                "我用状态机重新设计了 Streaming 层，将过程状态、业务事件和用户可见文本拆分为独立的类型化事件，"
                "进度、中间结果和最终回答各自按时序到达前端，解决了多工具调用下的重复展示与时序错乱问题。"
                "同步完成主链路从 Chat Completions 到 OpenAI Responses API 的迁移，统一 Tool Calling 路径，"
                "接入商品详情 Tool 使回答有实时商品数据支撑。基准测试：平均 TTFT 降低约 25%，P95 TTFT 降低约 25%。"
            ),
            impact=["-25% avg TTFT", "-25% P95 TTFT", "Typed SSE events", "OpenAI Responses API"],
            skills=["Agent Runtime", "Tool Calling", "Streaming", "State Machine", "OpenAI Responses API", "Python"],
            highlight=True,
        ),
        ProjectCard(
            id="personalization",
            title="Personalization & Warm-Up Architecture",
            company="Zalando",
            period="2025",
            summary_en=(
                "Zalando Assistant's Conversation Starters relied on static behavioural signals and called the "
                "user-profile service on every request — causing cold-start latency spikes and high downstream load "
                "under traffic peaks. I tackled three problems in parallel: "
                "(1) Rebuilt the recommendation input pipeline to combine real-time conversation context, "
                "user profile, and behaviour history — lifting Conversation Starter engagement by 15%+. "
                "(2) Added a cache layer in front of the profile service with TTL control, field-level invalidation, "
                "and null-value filtering, reducing profile-service calls by 70%+ and cutting P99 latency ~60% "
                "under high concurrency. "
                "(3) Designed an async Warm-Up architecture: a Redis registry tracks pending first-screen requests, "
                "a background worker pre-generates suggestions, and an in-memory fallback handles cache misses "
                "gracefully — decoupling expensive LLM generation from the critical path and reducing cold-start "
                "time by 60%+. Validated recommendation quality across 800+ real product-detail-page scenarios."
            ),
            summary_zh=(
                "Conversation Starters 依赖静态行为信号，每次请求都调用用户画像服务，高峰期冷启动延迟明显且下游压力大。"
                "我同时解决了三个问题：(1) 重建推荐输入链路，融合实时对话上下文、用户画像和历史行为，"
                "推荐入口互动率提升 15%+；"
                "(2) 为画像服务增加缓存层，支持 TTL、字段级失效、异常隔离和空值过滤，"
                "调用量减少 70%+，高并发下 P99 延迟降低约 60%；"
                "(3) 设计异步 Warm-Up 架构：Redis 注册表追踪待处理首屏请求，后台 Worker 提前生成建议，"
                "内存降级兜底，将耗时 LLM 生成从主路径解耦，首屏冷启动时间降低 60%+。"
                "基于 800+ 真实商品详情页场景验证推荐质量。"
            ),
            impact=["+15% engagement", "-60% cold-start", "-70% profile calls", "-60% P99 latency"],
            skills=["Personalization", "Redis", "Async Warm-Up", "Caching", "Eval-Driven", "Python"],
            highlight=True,
        ),
        ProjectCard(
            id="product-comparison",
            title="Product Comparison Skill",
            company="Zalando",
            period="2025",
            summary_en=(
                "Users frequently asked Zalando Assistant to compare products they had browsed, "
                "but free-form LLM comparison outputs were unstable: table layouts broke, discount "
                "fields went missing, and multi-turn references (\"compare the first two\", "
                "\"add the third one\") were often resolved incorrectly. "
                "I split the problem into model responsibility and code responsibility: "
                "the model handles intent understanding, conversation-state tracking, and "
                "summary copy; deterministic code owns product-reference resolution, field selection, "
                "discount calculation, two-product vs multi-product layout, and rendering markers. "
                "This separation eliminated LLM formatting instability and gave the frontend a stable "
                "contract regardless of model updates. Comparison-scenario engagement increased 20%+ after launch."
            ),
            summary_zh=(
                "用户频繁要求对比已浏览商品，但 LLM 直接生成的对比表格格式不稳定：布局错乱、折扣字段缺失，"
                "且多轮引用（\"比较前两个\"、\"再加第三个\"）常被错误解析。"
                "我将问题拆分为模型职责和代码职责两部分：模型负责意图理解、对话状态追踪和总结文案；"
                "确定性代码负责商品引用解析、字段选择、折扣计算、两商品/多商品布局和渲染标记。"
                "这一拆分消除了 LLM 格式不稳定问题，并向前端提供与模型版本无关的稳定契约。"
                "上线后对比场景用户互动率提升 20%+。"
            ),
            impact=["+20% engagement", "Stable rendering", "Multi-turn references", "Model/code split"],
            skills=["Structured Output", "Tool Calling", "Multi-turn", "Deterministic Rendering", "Python"],
            highlight=True,
        ),
        ProjectCard(
            id="text2sql",
            title="Text2SQL AI Agent — Enterprise Data Analysis",
            company="Thoughtworks · Major Domestic Bank",
            period="2022–2024",
            summary_en=(
                "A major domestic bank needed to give non-technical pricing analysts self-service access "
                "to complex structured data — without writing SQL. The hard problems: business queries "
                "involve deeply nested conditions and ambiguous field names that naive LLM prompts get wrong; "
                "a single bad SQL can corrupt downstream pricing decisions; and there was no evaluation "
                "baseline to know if changes helped or hurt. "
                "I designed a multi-stage agent pipeline: intent clarification → SQL generation → "
                "automated SQL validation → exception handling and retry → result summarisation with "
                "auto-generated visualisations. For retrieval accuracy, I built a dual-layer reranking "
                "mechanism that first matches on schema field names, then on representative values — "
                "substantially reducing schema hallucination. I also built a 1,000+ case evaluation suite "
                "from real business queries, which drove a ~20% accuracy lift and became the regression "
                "baseline for all subsequent prompt changes."
            ),
            summary_zh=(
                "某国内知名银行需要让非技术定价分析师自助查询复杂结构化数据，但业务查询含多层嵌套条件和歧义字段，"
                "直接 prompt LLM 错误率高；错误 SQL 会影响下游定价决策；且缺乏评估基线无法量化改进。"
                "我设计了多阶段 Agent 流水线：意图澄清 → SQL 生成 → 自动 SQL 校验 → 异常重试 → "
                "结果总结与自动可视化。在检索精度上，构建字段+值双层 Rerank 机制，大幅减少 schema 幻觉。"
                "从真实业务查询中积累 1,000+ 条评估用例，驱动准确率提升约 20%，并成为后续 Prompt 变更的回归基线。"
            ),
            impact=["+20% accuracy", "1,000+ eval cases", "Dual-layer rerank", "Auto SQL validation"],
            skills=["Text2SQL", "Multi-stage Agent", "FAISS", "Reranking", "SQL Validation", "Evaluation", "Python"],
            highlight=False,
        ),
        ProjectCard(
            id="rag-chatbot",
            title="RAG Knowledge Q&A System",
            company="Thoughtworks",
            period="2022–2024",
            summary_en=(
                "Built a production RAG pipeline for enterprise policy Q&A alongside the Text2SQL agent. "
                "Designed document chunking strategy, embedding pipeline, FAISS vector retrieval, "
                "and answer generation with LlamaIndex. Introduced RAGAS evaluation covering answer "
                "faithfulness, relevance, and context coverage — creating a reusable evaluation harness "
                "that the team adopted as the standard for all subsequent RAG work."
            ),
            summary_zh=(
                "与 Text2SQL Agent 并行，为企业政策问答构建生产级 RAG 流水线。"
                "设计文档切片策略、Embedding 流水线、FAISS 向量检索和 LlamaIndex 答案生成。"
                "引入 RAGAS 评估答案忠实性、相关性和上下文覆盖率，"
                "形成团队后续所有 RAG 工作的可复用评估框架。"
            ),
            impact=["RAGAS eval harness", "Faithfulness + relevance metrics", "Reusable RAG template"],
            skills=["RAG", "LlamaIndex", "FAISS", "Embedding", "RAGAS", "Python"],
            highlight=False,
        ),
    ]


@app.get("/api/architecture", response_model=ArchitectureResponse)
async def architecture() -> ArchitectureResponse:
    nodes = [
        ArchitectureNode(id="frontend", label="Static Frontend", type="frontend",
                         description="Vanilla HTML/CSS/JS on GitHub Pages. No build step, global CDN. SSE reader handles typed event streams and progressive text rendering in-browser."),
        ArchitectureNode(id="aliyun-fc", label="Aliyun FC Serverless", type="backend",
                         description="FastAPI on Aliyun Function Compute custom runtime (Python 3.10, uvicorn). Challenge: FC terminates streaming responses early — solved by collecting all SSE chunks before flushing, keeping SSE semantics for the client."),
        ArchitectureNode(id="agent", label="ResumeAgent", type="backend",
                         description="Multi-turn stateful agent with in-process LRU session store (500 sessions, 30 min TTL). Pydantic-validated tool schemas. Tool calling loop: search_resume_facts → get_project_detail → answer with evidence."),
        ArchitectureNode(id="llm", label="LLM + Fallback", type="llm",
                         description="Primary: Qwen-Turbo via OpenAI-compatible API. Automatic fallback chain: Qwen → DeepSeek → OpenAI. Each provider shares the same async httpx client and tool schema — swapping is config-only."),
        ArchitectureNode(id="sse", label="Typed SSE Stream", type="infra",
                         description="Five event types: metadata (session bootstrap), tool_call (agent reasoning visibility), answer_delta (streaming text), evidence (structured project cards), done. Client renders each type differently."),
    ]
    edges = [
        ArchitectureEdge(from_id="frontend", to_id="aliyun-fc", label="POST /api/chat/stream"),
        ArchitectureEdge(from_id="aliyun-fc", to_id="agent", label="dispatch request"),
        ArchitectureEdge(from_id="agent", to_id="llm", label="chat completions (async)"),
        ArchitectureEdge(from_id="llm", to_id="agent", label="tool_call / answer_delta"),
        ArchitectureEdge(from_id="aliyun-fc", to_id="frontend", label="SSE events"),
    ]
    return ArchitectureResponse(
        nodes=nodes,
        edges=edges,
        summary_en=(
            "Serverless FastAPI on Aliyun FC with multi-turn session state, Pydantic tool schemas, "
            "and a multi-provider LLM fallback chain (Qwen → DeepSeek → OpenAI). "
            "The main engineering challenge: FC terminates streaming responses early, "
            "so the backend collects all SSE chunks then flushes in one response — "
            "the client still receives full typed events and renders progressively."
        ),
        summary_zh=(
            "基于阿里云函数计算 Custom Runtime 的 Serverless FastAPI，支持多轮对话、进程内会话存储、"
            "Pydantic 工具 Schema 和多 Provider LLM 降级链（Qwen → DeepSeek → OpenAI）。"
            "核心工程挑战：FC 会提前终止流式响应，解决方案是后端收集所有 SSE chunk 后一次性 flush，"
            "客户端仍收到完整类型化事件并逐步渲染。"
        ),
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    ai = app.state.ai_binding
    return await with_request_logging(
        route="/api/chat",
        handler=lambda: agent.answer(request, ai),
        base_fields={"language": request.language, "session_id": request.session_id},
    )


@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest) -> Response:
    ai = app.state.ai_binding
    chunks = []
    async for chunk in agent.stream(request, ai):
        chunks.append(chunk)
    return Response(content="".join(chunks), media_type="text/event-stream")
