from __future__ import annotations

from fastapi import FastAPI
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
            title="Agent Runtime Upgrade",
            company="Zalando",
            period="2025",
            summary_en="Upgraded Agent Runtime with product-detail Tool Calling, Streaming handling, and OpenAI Responses API migration. Reduced average TTFT by 25% and P95 TTFT by 25% in validated flows.",
            summary_zh="升级商品详情 Tool Calling、Streaming 处理和 OpenAI Responses API 链路，平均 TTFT 降低 25%，P95 TTFT 降低 25%。",
            impact=["-25% avg TTFT", "-25% P95 TTFT", "Streaming stability", "OpenAI Responses API"],
            skills=["Agent Runtime", "Tool Calling", "Streaming", "OpenAI Responses API", "Observability", "Python"],
            highlight=True,
        ),
        ProjectCard(
            id="personalization",
            title="Personalized Conversation Starters & Guided Shopping",
            company="Zalando",
            period="2025",
            summary_en="Built personalization input pipeline combining user behavior, conversation context, and profile signals. Designed async Warm-Up architecture with Redis registry and in-memory fallback. Added profile-service cache layer with TTL control and field-level invalidation.",
            summary_zh="构建「历史行为 + 对话上下文 + 用户画像」个性化输入链路，设计基于 Redis 注册表的异步 Warm-Up 架构，并为用户画像服务增加 TTL 缓存层。",
            impact=["+15% engagement", "-60% cold start", "-70% profile calls", "800+ scenarios"],
            skills=["Personalization", "LLM", "Redis", "Caching", "Warm-Up", "Evaluation", "Python"],
            highlight=True,
        ),
        ProjectCard(
            id="product-comparison",
            title="Product Comparison Skill",
            company="Zalando",
            period="2025",
            summary_en="Designed and launched Product Comparison Skill. Model handles intent and multi-turn reference resolution; deterministic code owns field selection, discount computation, and table rendering — separating reasoning from execution.",
            summary_zh="设计并上线 Product Comparison Skill，模型负责意图理解和多轮引用解析，确定性代码控制字段选择、折扣计算和表格渲染，实现推理与执行解耦。",
            impact=["+20% engagement", "Multi-turn references", "Structured output", "Stable rendering"],
            skills=["Product Comparison", "Structured Output", "Tool Calling", "Multi-turn", "Python"],
            highlight=False,
        ),
        ProjectCard(
            id="text2sql",
            title="Text2SQL AI Agent",
            company="Thoughtworks · Major Domestic Bank",
            period="2022–2023",
            summary_en="Enterprise data-analysis Agent for a major bank. Multi-stage pipeline: intent clarification → SQL generation → validation → retry → result summarization. Dual-layer vector reranking (field + value). Built 1,000+ evaluation cases, improved accuracy by 20%.",
            summary_zh="为国内知名银行构建企业数据分析 Agent，多阶段流水线：意图澄清 → SQL 生成 → 校验 → 重试 → 结果总结。构建字段 + 值双层 Rerank 机制，积累 1,000+ 评估用例，准确率提升 20%。",
            impact=["+20% accuracy", "1,000+ eval cases", "Dual-layer rerank", "Multi-stage pipeline"],
            skills=["Text2SQL", "RAG", "Reranking", "FAISS", "SQL Validation", "Evaluation", "LlamaIndex", "Python"],
            highlight=False,
        ),
        ProjectCard(
            id="rag-chatbot",
            title="RAG Enterprise Chatbot",
            company="Thoughtworks",
            period="2022–2023",
            summary_en="Built a reusable RAG pipeline with LlamaIndex and FAISS covering document chunking, vectorization, retrieval, and answer generation. Introduced RAGAS to evaluate answer relevance and context coverage.",
            summary_zh="基于 LlamaIndex + FAISS 构建文档切片、向量化、召回与答案生成链路，引入 RAGAS 评估答案相关性和上下文覆盖率，形成可复用 RAG 研发与评估模板。",
            impact=["LlamaIndex + FAISS pipeline", "RAGAS evaluation", "Reusable RAG template"],
            skills=["RAG", "LlamaIndex", "FAISS", "Embedding", "RAGAS", "Prompt Engineering", "Python"],
            highlight=False,
        ),
    ]


@app.get("/api/architecture", response_model=ArchitectureResponse)
async def architecture() -> ArchitectureResponse:
    nodes = [
        ArchitectureNode(id="github-pages", label="GitHub Pages", type="frontend",
                         description="Static HTML/CSS/JS served from GitHub CDN. Zero build step, instant global deploy."),
        ArchitectureNode(id="aliyun-fc", label="Aliyun FC (cn-hangzhou)", type="backend",
                         description="Python FastAPI on Function Compute. Serverless, scales to zero, <1s cold start."),
        ArchitectureNode(id="agent", label="ResumeAgent", type="backend",
                         description="Multi-turn stateful agent. Session store with LRU + TTL eviction. Tool calling orchestration."),
        ArchitectureNode(id="session", label="Session Store", type="data",
                         description="In-process LRU session store. Bounded at 500 sessions, 30min TTL. No Redis needed at this scale."),
        ArchitectureNode(id="tools", label="Tool Dispatcher", type="backend",
                         description="Pydantic-validated tool schema. Three tools: search_resume_facts, get_project_detail, list_capabilities."),
        ArchitectureNode(id="deepseek", label="Qwen3 API", type="llm",
                         description="Qwen3.6-27B via OpenAI-compatible Chat Completions. Multi-provider fallback: Qwen → DeepSeek → OpenAI. Embedding via text-embedding-v3 for FAISS hybrid retrieval."),
        ArchitectureNode(id="sse", label="SSE Stream", type="infra",
                         description="Server-Sent Events with typed event names: metadata, tool_call, tool_result, answer_delta, evidence, done."),
    ]
    edges = [
        ArchitectureEdge(from_id="github-pages", to_id="aliyun-fc", label="HTTPS POST /api/chat/stream"),
        ArchitectureEdge(from_id="aliyun-fc", to_id="agent", label="routes request"),
        ArchitectureEdge(from_id="agent", to_id="session", label="read/write history"),
        ArchitectureEdge(from_id="agent", to_id="tools", label="tool call dispatch"),
        ArchitectureEdge(from_id="agent", to_id="deepseek", label="chat completions (Qwen3.6-27B)"),
        ArchitectureEdge(from_id="aliyun-fc", to_id="github-pages", label="SSE events"),
        ArchitectureEdge(from_id="deepseek", to_id="tools", label="function_call"),
        ArchitectureEdge(from_id="tools", to_id="deepseek", label="tool_result"),
    ]
    return ArchitectureResponse(
        nodes=nodes,
        edges=edges,
        summary_en="Serverless Python FastAPI on Aliyun Function Compute. Multi-turn agent with in-process session store, Pydantic tool schemas, multi-provider LLM fallback, and typed SSE streaming.",
        summary_zh="基于阿里云函数计算的 Serverless Python FastAPI，支持多轮对话、进程内会话存储、Pydantic 工具 Schema、多 Provider LLM 降级和类型化 SSE 流式响应。",
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
    response = await with_request_logging(
        route="/api/chat/stream",
        handler=lambda: agent.answer(request, ai),
        base_fields={"language": request.language, "session_id": request.session_id},
    )
    body = "".join([chunk async for chunk in stream_chat_response(response)])
    return Response(content=body, media_type="text/event-stream")
