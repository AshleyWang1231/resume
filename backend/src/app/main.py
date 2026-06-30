from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from app.config import load_local_env
from app.harness import ResumeAgent
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
            period="2024",
            summary_en="Upgraded Agent Runtime with product-detail Tool Calling, Streaming handling, and OpenAI Responses API migration. Reduced latency by 25% while improving Streaming stability across high-traffic shopping sessions.",
            summary_zh="升级商品详情 Tool Calling、Streaming 处理和 OpenAI Responses API 链路，响应延迟降低 25%，Streaming 稳定性显著提升。",
            impact=["-25% avg TTFT", "-25% P95 TTFT", "Streaming stability", "OpenAI Responses API"],
            skills=["Agent Runtime", "Tool Calling", "Streaming", "OpenAI Responses API", "Observability", "Python"],
            highlight=True,
        ),
        ProjectCard(
            id="personalization",
            title="Personalized Conversation Starters",
            company="Zalando",
            period="2024",
            summary_en="Built personalized starter suggestions combining user profile, purchase history, conversation context, and real-time product signals. Replaced cold-start generic suggestions with context-aware, precomputed warm-up cache.",
            summary_zh="结合用户画像、购买历史、对话上下文和商品信号，替换冷启动通用推荐，引入预计算 Warm-Up 缓存，提升首屏相关性。",
            impact=["+15% engagement", "-60% cold start", "-70% profile calls", "800+ scenarios"],
            skills=["Personalization", "LLM", "Redis", "Caching", "Evaluation", "Python"],
            highlight=True,
        ),
        ProjectCard(
            id="product-comparison",
            title="Product Comparison Skill",
            company="Zalando",
            period="2023",
            summary_en="Launched natural-language product comparison. Model handles intent and reference resolution; deterministic code owns field selection, discount computation, and table rendering contract — separating reasoning from execution.",
            summary_zh="上线自然语言商品对比，模型负责意图理解和引用解析，确定性代码控制字段选择、折扣计算和表格渲染，实现推理与执行解耦。",
            impact=["+20% engagement", "Multi-turn references", "Structured output", "Stable rendering"],
            skills=["Product Comparison", "Structured Output", "Tool Calling", "Python"],
            highlight=False,
        ),
        ProjectCard(
            id="text2sql",
            title="Text2SQL AI Agent",
            company="Thoughtworks · Leading Domestic Bank",
            period="2022–2023",
            summary_en="Enterprise data-analysis Agent for a major bank. Multi-stage pipeline: intent clarification → schema linking → field/value reranking → SQL generation → validation → retry → natural-language summary. Built 1,000+ evaluation cases.",
            summary_zh="为国内知名银行构建企业数据分析 Agent，多阶段流水线：意图澄清 → Schema 关联 → 字段/值重排序 → SQL 生成 → 校验 → 重试 → 自然语言总结。积累 1,000+ 评估用例。",
            impact=["+20% accuracy", "1,000+ eval cases", "Field + value rerank", "Multi-stage pipeline"],
            skills=["Text2SQL", "RAG", "Reranking", "SQL Validation", "Evaluation", "LlamaIndex", "Python"],
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
        ArchitectureNode(id="deepseek", label="DeepSeek API", type="llm",
                         description="DeepSeek V4 Flash via OpenAI-compatible Chat Completions. Multi-provider fallback: DeepSeek → Qwen → OpenAI."),
        ArchitectureNode(id="sse", label="SSE Stream", type="infra",
                         description="Server-Sent Events with typed event names: metadata, tool_call, tool_result, answer_delta, evidence, done."),
    ]
    edges = [
        ArchitectureEdge(from_id="github-pages", to_id="aliyun-fc", label="HTTPS POST /api/chat/stream"),
        ArchitectureEdge(from_id="aliyun-fc", to_id="agent", label="routes request"),
        ArchitectureEdge(from_id="agent", to_id="session", label="read/write history"),
        ArchitectureEdge(from_id="agent", to_id="tools", label="tool call dispatch"),
        ArchitectureEdge(from_id="agent", to_id="deepseek", label="chat completions"),
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
async def chat_stream(request: ChatRequest) -> StreamingResponse:
    ai = app.state.ai_binding
    return StreamingResponse(agent.stream(request, ai), media_type="text/event-stream")
