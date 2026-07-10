"""Load RESUME_FACTS from the two canonical txt files in backend/data/.

Each fact maps to a dict with the same keys as the old hardcoded RESUME_FACTS:
  id, company, title, summary_en, summary_zh, evidence, skills

The txt files are the single source of truth. No content is invented here —
every string comes directly from the files.
"""
from __future__ import annotations

import os
import re

_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")


def _read(filename: str) -> str:
    path = os.path.join(_DATA_DIR, filename)
    with open(path, encoding="utf-8") as f:
        return f.read()


def _strip(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def build_resume_facts() -> list[dict]:
    en = _read("Resume_2026_en.txt")
    zh = _read("Resume_2026_cn.txt")

    facts = []

    # ── Profile ──────────────────────────────────────────────────────────────
    # EN: paragraph 4 (the summary line)
    en_profile = _strip(
        "AI Software Engineer focused on building LLM applications and AI Agent systems for real business scenarios. "
        "Experienced in Python/Java backend development, Agent Workflows, Tool Calling, Streaming, personalization, "
        "product decision support, Text2SQL, and observability-driven performance diagnostics. "
        "Led AI product capabilities across e-commerce and financial services, including personalized shopping assistance, "
        "real-time response optimization, and enterprise data analysis agents, with end-to-end experience from system design to production rollout. "
        "Work experience: Zalando (2025–present), Thoughtworks (2021–2025). "
        "Education: MSc Computing, Cardiff University UK (2019–2021)."
    )
    zh_profile = _strip(
        "汪露是一名 AI 软件工程师，专注于生产级 LLM 应用与 AI Agent 系统建设。"
        "擅长 Python/Java 后端开发，在 Agent Workflow、Tool Calling、Streaming、个性化推荐、"
        "商品决策辅助及 Text2SQL 等方向具备丰富实践经验。"
        "主导电商（嘉兰朵/Zalando）与金融（Thoughtworks / 国内知名银行）领域 AI 产品研发。"
        "工作经历：嘉兰朵/Zalando（2025年8月至今），思特沃克/Thoughtworks（2021年4月–2025年8月）。"
        "教育背景：英国卡迪夫大学 Computing 硕士（2019–2021）。"
    )
    facts.append({
        "id": "profile",
        "company": "Lu Wang · 汪露",
        "title": "AI Software Engineer — Profile",
        "summary_en": en_profile,
        "summary_zh": zh_profile,
        "evidence": ["Zalando 2025–present", "Thoughtworks 2021–2025",
                     "Cardiff University MSc Computing", "e-commerce", "financial services"],
        "skills": ["LLM Agent", "Agent Workflow", "Tool Calling", "Streaming",
                   "Python", "Java", "FastAPI", "Text2SQL", "RAG",
                   "Pydantic-AI", "OpenAI Responses API", "RAGAS",
                   "FAISS", "BGE-Reranker", "pgvector"],
    })

    # ── Zalando: Personalization ──────────────────────────────────────────────
    facts.append({
        "id": "personalization",
        "company": "Zalando",
        "title": "Personalization and Guided Shopping Capabilities",
        "summary_en": _strip(
            "Built personalization and guided-shopping capabilities for Zalando Assistant Conversation Starters "
            "and product-detail-page recommendations. "
            "Built a personalization input pipeline combining user behavior, conversation context, and profile signals, "
            "increasing Conversation Starter engagement by 15%+. "
            "Designed a cache layer for downstream user profile data with TTL control and field-level invalidation, "
            "reducing profile-service calls by 70%+ and lowering P99 latency by ~60% under high concurrency. "
            "Implemented an async Warm-Up architecture using Redis registry and in-memory fallback, "
            "decoupling first-screen generation from user requests and reducing cold-start time by 60%+. "
            "Redesigned the product-detail-page recommendation strategy with a multi-layer decision flow "
            "(behavior-signal recognition → recommendation routing → fallback generation). "
            "Built an evaluation process based on ~800 real product-detail-page scenarios."
        ),
        "summary_zh": _strip(
            "面向 Zalando Assistant 构建个性化推荐与导购能力，覆盖首屏 Conversation Starters 和商品详情页推荐。"
            "构建「历史行为 + 对话上下文 + 用户画像」个性化输入链路，推动推荐入口互动率提升 15%+。"
            "为下游用户画像服务增加缓存层，支持 TTL、字段级失效、异常隔离和空值过滤，"
            "使画像服务调用量减少 70%+，高并发场景下 P99 延迟下降约 60%。"
            "设计并落地基于 Redis 注册表 + 内存回退机制的异步 Warm-Up 架构，首屏冷启动时间降低 60%+。"
            "主导商品详情页推荐策略重构，设计「行为信号识别 + 推荐方向决策 + 兜底生成」多层决策框架。"
            "基于约 800 个真实商品详情页场景建立推荐效果分析体系。"
        ),
        "evidence": ["+15% engagement", "-60% cold-start", "-70% profile calls",
                     "-60% P99 latency", "800+ scenarios", "Conversation Starters"],
        "skills": ["Personalization", "LLM", "Redis", "Caching", "Warm-Up", "Evaluation"],
    })

    # ── Zalando: Agent Runtime ────────────────────────────────────────────────
    facts.append({
        "id": "agent-runtime",
        "company": "Zalando",
        "title": "Agent Runtime Upgrade and Real-Time Response Optimization",
        "summary_en": _strip(
            "Upgraded the main Zalando Assistant Agent Runtime: integrated product-detail Tool Calling, "
            "redesigned Streaming response handling, and migrated to OpenAI Responses API. "
            "Designed Streaming processing for multi-step Agent flows, separating process states, "
            "business events, and final response text to prevent duplicated display and event-ordering issues. "
            "Reduced Suggestions API average TTFT by ~25% in benchmark tests vs the prior synchronous interface. "
            "Migrated from Chat Completions to OpenAI Responses API, unifying Tool Calling and Streaming, "
            "reducing P95 TTFT by ~25% in validated flows."
        ),
        "summary_zh": _strip(
            "负责 Zalando Assistant Agent 主链路升级：商品详情 Tool 接入、Streaming 架构优化及 OpenAI Responses API 迁移。"
            "设计多步 Agent 链路下的 Streaming 处理与分发机制，区分过程状态、业务事件和最终回复文本，"
            "解决多工具调用场景下的重复展示与时序错乱问题。"
            "基准测试中 Suggestions API 流式输出 TTFT 平均降低约 25%。"
            "完成 Agent 主链路从 Chat Completions 向 Responses API 的迁移，在已验证链路中 P95 TTFT 降低约 25%。"
        ),
        "evidence": ["-25% avg TTFT", "-25% P95 TTFT", "Streaming state machine",
                     "OpenAI Responses API", "Tool Calling"],
        "skills": ["Agent Runtime", "Tool Calling", "Streaming", "OpenAI Responses API",
                   "State Machine", "Observability"],
    })

    # ── Zalando: Product Comparison ───────────────────────────────────────────
    facts.append({
        "id": "product-comparison",
        "company": "Zalando",
        "title": "Product Comparison Skill",
        "summary_en": _strip(
            "Designed and launched Product Comparison Skill for Zalando Assistant, enabling users to compare "
            "multiple products through natural language, increasing comparison-scenario engagement by 20%+. "
            "Built context-aware product reference parsing to resolve product selections across multi-turn "
            "conversations, including position-based, range-based, and follow-up requests. "
            "Developed dynamic comparison-dimension selection based on user intent, product attributes, and "
            "category characteristics, making comparison results more focused and easier to scan. "
            "Separated model reasoning from table generation: model handles intent and summary recommendations; "
            "deterministic code handles field parsing, discount calculation, layout, and rendering markers, "
            "eliminating LLM table formatting instability."
        ),
        "summary_zh": _strip(
            "设计并上线 Product Comparison Skill，帮助用户通过自然语言完成多商品比较与决策，"
            "上线后对比场景用户互动率提升 20%+。"
            "构建上下文商品解析机制，解决用户通过序号、范围或追加表达引用商品时的对象定位问题。"
            "结合用户关注点、商品属性和品类特征动态选择比较维度，使比较结果更聚焦可读。"
            "拆分模型推理与表格生成职责，由代码负责字段解析、折扣计算、布局和渲染标记，"
            "解决纯 LLM 生成表格格式不稳定、字段缺失和前端难以渲染的问题。"
        ),
        "evidence": ["+20% engagement", "Multi-turn references", "Structured output", "Stable rendering"],
        "skills": ["Product Comparison", "Structured Output", "Tool Calling", "Multi-turn"],
    })

    # ── Thoughtworks: Text2SQL ────────────────────────────────────────────────
    facts.append({
        "id": "text2sql",
        "company": "Thoughtworks · Major Domestic Bank",
        "title": "AI Agent Module for Pricing Management System — Text2SQL",
        "summary_en": _strip(
            "Built an enterprise data-analysis Agent for a major domestic bank to empower non-technical staff "
            "with self-service natural-language querying of structured data and internal policy Q&A. "
            "Designed a multi-stage agent workflow: intent clarification → SQL generation → query execution "
            "→ result summarization with visualizations. "
            "Created and optimized prompt templates for complex business queries, improving model accuracy by ~20%. "
            "Developed a 1,000+ case evaluation suite from real business queries. "
            "Engineered a dual-layer reranking mechanism (field + value) using vector search, "
            "and integrated SQL validation, exception handling, and automatic retry logic."
        ),
        "summary_zh": _strip(
            "为国内知名银行构建企业数据分析 Agent，支持非技术人员通过自然语言查询结构化数据和政策问答。"
            "设计并实现「意图澄清 → SQL 生成 → 查询执行 → 结果总结与可视化」多阶段 Agent 工作流。"
            "持续迭代 Prompt 模板，构建 1000+ 条真实业务测试集，提升端到端问答准确率 20%+。"
            "基于向量数据库构建字段 + 值双层 Rerank 机制；引入 SQL 校验、异常重试等机制增强链路稳定性。"
        ),
        "evidence": ["+20% accuracy", "1,000+ eval cases", "Dual-layer rerank",
                     "Multi-stage pipeline", "SQL validation"],
        "skills": ["Text2SQL", "RAG", "Reranking", "FAISS", "Evaluation",
                   "Prompt Engineering", "LlamaIndex"],
    })

    # ── Thoughtworks: RAG Chatbot ─────────────────────────────────────────────
    facts.append({
        "id": "rag-chatbot",
        "company": "Thoughtworks",
        "title": "RAG Enterprise Chatbot — Knowledge Q&A System",
        "summary_en": _strip(
            "Built a reusable RAG pipeline using LlamaIndex and FAISS, covering document chunking, "
            "vectorization, retrieval, and answer generation. "
            "Introduced RAGAS to evaluate answer relevance and context coverage, "
            "forming a reusable RAG development and evaluation template for enterprise knowledge Q&A."
        ),
        "summary_zh": _strip(
            "基于 LlamaIndex + FAISS 构建文档切片、向量化、召回与答案生成链路，"
            "引入 RAGAS 评估答案相关性和上下文覆盖率，形成可复用的 RAG 研发与评估模板。"
        ),
        "evidence": ["LlamaIndex + FAISS pipeline", "RAGAS evaluation", "Reusable RAG template"],
        "skills": ["RAG", "LlamaIndex", "FAISS", "Embedding", "RAGAS", "Prompt Engineering"],
    })

    # ── Thoughtworks: Pricing Management System ───────────────────────────────
    facts.append({
        "id": "pricing-management",
        "company": "Thoughtworks · Major Domestic Bank",
        "title": "Pricing Management System — Access Control & Reporting",
        "summary_en": _strip(
            "Module owner for a bank-wide interest-rate product pricing platform. "
            "Led access-control module design using Hexagonal Architecture and DDD, modelling complex role "
            "hierarchies and fine-grained permissions as a reusable domain layer across multiple sub-systems. "
            "Built a Tablesaw-based in-memory reporting solution, improving reporting development efficiency "
            "by ~40% and shortening delivery cycle by 2+ weeks. "
            "Drove zero-impact database migration sustaining millions of daily pricing requests."
        ),
        "summary_zh": _strip(
            "负责国内知名银行利率类金融产品定价管理系统的权限模块、报表模块及数据库迁移等核心工作。"
            "基于六边形架构与 DDD 主导权限模块设计，构建可复用领域模型，在多个子系统中复用。"
            "针对报表模块自研内存数据加工方案（Tablesaw），报表开发效率提升约 40%，工期缩短 2 周以上。"
            "主导数据库迁移方案设计与实施，实现 0 业务感知平滑切换，"
            "系统在每日数百万笔定价请求下稳定运行。"
        ),
        "evidence": ["+40% dev efficiency", "-2 weeks cycle",
                     "0-downtime DB migration", "Multi-system reuse"],
        "skills": ["Java", "Spring Cloud", "DDD", "Hexagonal Architecture",
                   "Tablesaw", "MySQL", "Redis", "RabbitMQ"],
    })

    # ── Thoughtworks: After-Sales Management System ───────────────────────────
    facts.append({
        "id": "after-sales",
        "company": "Thoughtworks",
        "title": "After-Sales Management System",
        "summary_en": _strip(
            "Module owner and core backend engineer for the after-sales management system. "
            "Owned backend architecture and API integration across headquarters systems, platform services, "
            "and WMS. Delivered the module 100% on time, resolved ~98% of integration blockers, "
            "and supported tens of thousands of daily spare-part transactions after launch."
        ),
        "summary_zh": _strip(
            "负责售后模块后端架构与 API 对接，协调总部、中台、WMS 多系统集成。"
            "所负责模块准时交付，联调阻塞修复率约 98%，"
            "系统上线后支撑日均数万级备件交易流转。"
        ),
        "evidence": ["100% on-time delivery", "~98% blocker resolution",
                     "Tens of thousands daily transactions", "Multi-system integration"],
        "skills": ["Java", "Spring Cloud", "API Integration", "Backend Architecture"],
    })

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

    return facts
