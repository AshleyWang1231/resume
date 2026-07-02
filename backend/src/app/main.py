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
            period="2025–2026",
            summary_en="Redesigned the Zalando Assistant Agent Runtime — Streaming architecture, Tool Calling integration, OpenAI Responses API migration.",
            summary_zh="重新设计 Zalando Assistant Agent Runtime，覆盖 Streaming 架构、Tool Calling 接入和 OpenAI Responses API 迁移。",
            star_s_en="The assistant returned full responses only after all tool calls completed, giving users no visibility into agent progress and making interactions feel sluggish.",
            star_a_en="Introduced a state-machine Streaming layer separating process states, business events, and user-visible text into typed SSE events. Integrated product-detail Tool Calling so answers are grounded in live catalogue data. Migrated the runtime from Chat Completions to OpenAI Responses API, unifying the Tool Calling + Streaming path.",
            star_r_en="Average TTFT –25% (Suggestions API benchmark). P95 TTFT –25% in validated flows. Users see real-time tool progress instead of a blank wait.",
            star_s_zh="助手需等所有工具调用完成后才整体输出，用户看不到任何进度，体验偏慢。",
            star_a_zh="引入状态机 Streaming 层，将过程状态、业务事件和用户可见文本拆分为类型化 SSE 事件。接入商品详情 Tool Calling，让回答基于实时商品数据。将主链路从 Chat Completions 迁移至 OpenAI Responses API，统一 Tool Calling + Streaming 路径。",
            star_r_zh="平均 TTFT 降低 25%（Suggestions API 基准测试），P95 TTFT 降低 25%，用户实时可见工具调用进度。",
            impact=["-25% avg TTFT", "-25% P95 TTFT", "Typed SSE events", "OpenAI Responses API"],
            skills=["Agent Runtime", "Tool Calling", "Streaming", "State Machine", "OpenAI Responses API"],
            highlight=True,
        ),
        ProjectCard(
            id="personalization",
            title="Personalization & Warm-Up Architecture",
            company="Zalando",
            period="2025–2026",
            summary_en="Built personalization pipeline and async Warm-Up architecture for Zalando Assistant Conversation Starters.",
            summary_zh="为 Zalando Assistant Conversation Starters 构建个性化链路和异步 Warm-Up 架构。",
            star_s_en="Conversation Starters used static signals only, called the profile service on every request, and had noticeable cold-start latency under traffic spikes.",
            star_a_en="(1) Rebuilt the input pipeline to fuse real-time conversation context, user profile, and behaviour history. (2) Added a TTL cache layer with field-level invalidation in front of the profile service. (3) Designed an async Warm-Up: a Redis registry tracks pending first-screen requests; a background worker pre-generates suggestions; in-memory fallback handles cache misses.",
            star_r_en="Conversation Starter engagement +15%. Cold-start time –60%. Profile-service calls –70%; P99 latency –60% under high concurrency. Validated across 800+ real product-detail-page scenarios.",
            star_s_zh="Conversation Starters 仅依赖静态信号，每次请求都调用画像服务，高峰期冷启动延迟明显。",
            star_a_zh="(1) 重建输入链路，融合实时对话上下文、用户画像和历史行为。(2) 在画像服务前加 TTL 缓存层，支持字段级失效。(3) 设计异步 Warm-Up：Redis 注册表追踪待处理首屏请求，后台 Worker 提前生成建议，内存降级兜底。",
            star_r_zh="推荐入口互动率 +15%，冷启动时间 -60%，画像服务调用量 -70%，高并发下 P99 延迟 -60%。基于 800+ 真实商品页面场景验证。",
            impact=["+15% engagement", "-60% cold-start", "-70% profile calls", "-60% P99 latency"],
            skills=["Personalization", "Redis", "Async Warm-Up", "Caching", "Eval-Driven"],
            highlight=True,
        ),
        ProjectCard(
            id="product-comparison",
            title="Product Comparison Skill",
            company="Zalando",
            period="2025–2026",
            summary_en="Designed and shipped a multi-turn product comparison capability for Zalando Assistant.",
            summary_zh="为 Zalando Assistant 设计并上线多轮商品对比能力。",
            star_s_en="Users asked to compare browsed products, but free-form LLM output was unreliable: table layouts broke, discount fields went missing, and multi-turn references (\"compare the first two\") were frequently misresolved.",
            star_a_en="Split responsibilities: the model handles intent, conversation-state tracking, and summary copy; deterministic code owns product-reference resolution, field selection, discount calculation, and layout rendering. This gave the frontend a stable contract independent of model version.",
            star_r_en="Comparison-scenario engagement +20%. Eliminated LLM formatting instability; frontend rendering is stable across model updates.",
            star_s_zh="用户要求对比已浏览商品，但 LLM 直接输出格式不稳定：布局错乱、折扣字段缺失，多轮引用频繁解析错误。",
            star_a_zh="责任拆分：模型负责意图理解、对话状态追踪和总结文案；确定性代码负责商品引用解析、字段选择、折扣计算和布局渲染，向前端提供与模型版本无关的稳定契约。",
            star_r_zh="对比场景互动率 +20%，消除 LLM 格式不稳定问题，前端渲染跨模型版本保持稳定。",
            impact=["+20% engagement", "Stable rendering", "Multi-turn references", "Model/code split"],
            skills=["Structured Output", "Tool Calling", "Multi-turn", "Deterministic Rendering"],
            highlight=True,
        ),
        ProjectCard(
            id="text2sql",
            title="Text2SQL AI Agent — Enterprise Data Analysis",
            company="Thoughtworks · Major Domestic Bank",
            period="2021–2025",
            summary_en="Built an enterprise data-analysis Agent for a major domestic bank, enabling natural-language querying of complex structured data.",
            summary_zh="为国内知名银行构建企业数据分析 Agent，支持复杂结构化数据的自然语言查询。",
            star_s_en="Non-technical pricing analysts needed self-service access to complex structured data. Naive LLM prompts failed on nested conditions and ambiguous schema fields, bad SQL could corrupt pricing decisions, and there was no evaluation baseline.",
            star_a_en="Designed a multi-stage agent pipeline: intent clarification → SQL generation → automated SQL validation → exception retry → result summarisation with visualisations. Built dual-layer vector reranking (field + value) to reduce schema hallucination. Created a 1,000+ case evaluation suite from real business queries as a regression baseline for all prompt changes.",
            star_r_en="End-to-end query accuracy +20%. SQL validation + retry loop eliminated silent failures. 1,000+ eval cases became the team's standard regression baseline.",
            star_s_zh="非技术定价分析师需自助查询复杂结构化数据，但直接 prompt LLM 在嵌套条件和歧义字段上错误率高，且缺乏评估基线。",
            star_a_zh="设计多阶段 Agent 流水线：意图澄清 → SQL 生成 → 自动 SQL 校验 → 异常重试 → 结果总结与可视化。构建字段+值双层向量 Rerank 减少 schema 幻觉。从真实业务查询积累 1,000+ 条评估用例作为回归基线。",
            star_r_zh="端到端查询准确率 +20%，SQL 校验+重试消除静默失败，1,000+ 评估用例成为团队标准回归基线。",
            impact=["+20% accuracy", "1,000+ eval cases", "Dual-layer rerank", "Auto SQL validation"],
            skills=["Text2SQL", "Multi-stage Agent", "FAISS", "Reranking", "SQL Validation", "Evaluation"],
            highlight=False,
        ),
        ProjectCard(
            id="pricing-management",
            title="Pricing Management System — Access Control & Data Pipeline",
            company="Thoughtworks · Major Domestic Bank",
            period="2021–2025",
            summary_en="Backend module owner for a bank-wide interest-rate product pricing platform — access control, reporting, and database migration.",
            summary_zh="负责国内知名银行利率类金融产品定价管理系统的权限模块、报表模块及数据库迁移等核心工作。",
            star_s_en="The pricing platform needed fine-grained access control across complex role hierarchies and multiple business lines, high-performance in-memory multi-dimensional aggregation for reporting, and a MySQL architecture struggling under millions of daily pricing transactions.",
            star_a_en="(1) Led access control module design and implementation using Hexagonal Architecture and DDD — modelled complex role hierarchies and fine-grained permissions as a reusable domain layer adopted across multiple sub-systems. (2) Designed a custom in-memory data processing pipeline (Tablesaw + custom toolchain) for the reporting module to replace external dependencies. (3) Spearheaded the database migration strategy, delivering a zero-downtime production switchover for large-scale business tables.",
            star_r_en="Reporting module dev efficiency +40%; delivery cycle shortened by 2+ weeks. Database migration achieved zero business impact, sustaining stable operation under millions of daily pricing requests. Access control module reused across multiple sub-systems.",
            star_s_zh="定价平台需跨多业务线支持复杂角色层级与细粒度权限管理；报表模块需内存中多维聚合与计算；原 MySQL 架构在海量业务数据下存在性能瓶颈。",
            star_a_zh="(1) 基于六边形架构与 DDD 主导权限模块设计与落地，构建可复用领域模型，在多个子系统中复用。(2) 针对报表模块自研内存数据加工方案（Tablesaw + 自定义工具链），替代外部依赖。(3) 主导数据库迁移方案设计与实施，完成生产环境平滑切换。",
            star_r_zh="报表模块开发效率提升约 40%，开发工期缩短 2 周以上。数据库迁移实现 0 业务感知，系统在每日数百万笔定价请求下稳定运行。权限模块在多个子系统中复用。",
            impact=["+40% dev efficiency", "–2 weeks cycle", "0-downtime DB migration", "Multi-system reuse"],
            skills=["Java", "Spring Cloud", "DDD", "Hexagonal Architecture", "Tablesaw", "MySQL", "Redis", "RabbitMQ"],
            highlight=False,
        ),
        ProjectCard(
            id="rag-chatbot",
            title="RAG Knowledge Q&A System",
            company="Thoughtworks",
            period="2021–2025",
            summary_en="Built a production RAG pipeline for enterprise policy Q&A alongside the Text2SQL agent.",
            summary_zh="与 Text2SQL Agent 并行，构建企业政策问答生产级 RAG 流水线。",
            star_s_en="The bank needed a reliable Q&A system over internal policy documents, with no existing retrieval infrastructure or quality measurement.",
            star_a_en="Built a full RAG pipeline with LlamaIndex and FAISS — chunking strategy, embedding, vector retrieval, and answer generation. Introduced RAGAS evaluation (faithfulness, relevance, context coverage) as the quality gate, creating a reusable eval harness the team adopted for all subsequent RAG work.",
            star_r_en="Established RAGAS as the team's standard RAG quality framework. Reusable pipeline template shortened onboarding time for subsequent RAG projects.",
            star_s_zh="银行需要基于内部政策文档的可靠问答系统，无现有检索基础设施，也没有质量度量方式。",
            star_a_zh="基于 LlamaIndex + FAISS 构建完整 RAG 流水线——切片策略、Embedding、向量检索和答案生成。引入 RAGAS（忠实性、相关性、上下文覆盖率）作为质量门控，形成团队后续 RAG 工作的可复用评估框架。",
            star_r_zh="RAGAS 成为团队 RAG 质量标准框架，可复用流水线模板缩短后续项目上线周期。",
            impact=["RAGAS eval harness", "Faithfulness + relevance metrics", "Reusable RAG template"],
            skills=["RAG", "LlamaIndex", "FAISS", "Embedding", "RAGAS"],
            highlight=False,
        ),
    ]


@app.get("/api/architecture", response_model=ArchitectureResponse)
async def architecture() -> ArchitectureResponse:
    nodes = [
        ArchitectureNode(id="agent", label="Agent Runtime", type="backend",
                         description="Multi-turn stateful agent. Manages session history, drives the tool-calling loop, and streams typed events back to the client."),
        ArchitectureNode(id="workflow", label="Agent Workflow", type="backend",
                         description="Intent routing → Tool Calling → evidence retrieval → answer synthesis. Each stage is a discrete step; the agent decides the path at runtime."),
        ArchitectureNode(id="tools", label="Tool Calling", type="backend",
                         description="Pydantic-validated tool schemas: search_resume_facts, get_project_detail, list_capabilities. The LLM selects and calls tools; results feed back into the next reasoning step."),
        ArchitectureNode(id="llm", label="LLM (Multi-provider)", type="llm",
                         description="Primary: Qwen-Turbo. Auto-fallback: Qwen → DeepSeek → OpenAI. All providers share the same async client and tool schema — switching is config-only."),
        ArchitectureNode(id="sse", label="Streaming (SSE)", type="infra",
                         description="Typed event stream: tool_call → answer_delta → evidence → done. Client renders each event type independently, giving real-time visibility into agent reasoning."),
    ]
    edges = [
        ArchitectureEdge(from_id="agent", to_id="workflow", label="drives"),
        ArchitectureEdge(from_id="workflow", to_id="tools", label="tool dispatch"),
        ArchitectureEdge(from_id="tools", to_id="llm", label="tool_result"),
        ArchitectureEdge(from_id="llm", to_id="workflow", label="tool_call / delta"),
        ArchitectureEdge(from_id="agent", to_id="sse", label="stream events"),
    ]
    return ArchitectureResponse(
        nodes=nodes,
        edges=edges,
        summary_en=(
            "A stateful multi-turn Agent Runtime with a four-stage workflow: intent routing, "
            "Tool Calling (Pydantic schemas), evidence retrieval, and answer synthesis. "
            "Multi-provider LLM fallback (Qwen → DeepSeek → OpenAI) with typed SSE streaming "
            "so every reasoning step is visible to the client in real time."
        ),
        summary_zh=(
            "多轮有状态 Agent Runtime，四阶段工作流：意图路由 → Tool Calling（Pydantic Schema）"
            "→ 证据检索 → 答案合成。多 Provider LLM 降级链（Qwen → DeepSeek → OpenAI），"
            "类型化 SSE Streaming 让每个推理步骤实时可见。"
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
