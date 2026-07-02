RESUME_FACTS = [
    {
        "id": "profile",
        "company": "Lu Wang · 汪露",
        "title": "AI Software Engineer — Profile",
        "summary_en": (
            "Lu Wang is an AI Software Engineer focused on building production-grade LLM applications and AI Agent systems. "
            "Experienced in Python and Java backend development, Agent Workflows, Tool Calling, Streaming, "
            "personalization, product decision support, Text2SQL, and observability-driven performance diagnostics. "
            "Led AI product capabilities across e-commerce (Zalando) and financial services (Thoughtworks / major domestic bank), "
            "including personalized shopping assistance, real-time response optimization, and enterprise data analysis agents. "
            "End-to-end experience from system design to production rollout."
        ),
        "summary_zh": (
            "汪露是一名 AI 软件工程师，专注于生产级 LLM 应用与 AI Agent 系统建设。"
            "擅长 Python/Java 后端开发，在 Agent Workflow、Tool Calling、Streaming、个性化推荐、"
            "商品决策辅助及 Text2SQL 等方向具备丰富实践经验。"
            "主导电商（Zalando）与金融（Thoughtworks / 国内知名银行）领域 AI 产品研发，"
            "负责个性化导购、实时响应优化、企业级数据分析 Agent 等核心能力建设，"
            "具备从系统设计到生产落地的完整经验。"
        ),
        "evidence": ["Zalando", "Thoughtworks", "e-commerce", "financial services", "production LLM systems"],
        "skills": ["LLM Agent", "Agent Workflow", "Tool Calling", "Streaming", "Java", "FastAPI"],
    },
    {
        "id": "personalization",
        "company": "Zalando",
        "title": "Personalized Conversation Starters & Guided Shopping",
        "summary_en": (
            "Built personalization and guided-shopping capabilities for Zalando Assistant. "
            "Designed a personalization input pipeline combining user behavior history, conversation context, and profile signals — "
            "replacing prior reliance on static behavioral data and increasing Conversation Starter engagement by 15%+. "
            "Added a cache layer for the downstream user profile service with TTL control, field-level invalidation, "
            "failure-safe handling, and null-value filtering, cutting profile-service calls by 70%+ and lowering P99 latency by ~60% under high concurrency. "
            "Implemented an async Warm-Up architecture using a Redis registry and in-memory fallback, decoupling first-screen "
            "suggestion generation from user requests and reducing cold-start time by 60%+. "
            "Redesigned the product-detail-page recommendation strategy with a multi-layer decision flow: "
            "behavior-signal recognition → recommendation routing → fallback generation, improving stability across diverse user and product scenarios. "
            "Built an evaluation process based on ~800 real product-detail-page scenarios to identify coverage gaps and repeated angles, "
            "translating findings into recommendation rules and safety controls."
        ),
        "summary_zh": (
            "面向 Zalando Assistant 构建个性化推荐与导购能力。"
            "构建「历史行为 + 对话上下文 + 用户画像」个性化输入链路，推动推荐入口互动率提升 15%+。"
            "为下游用户画像服务增加缓存层，支持 TTL、字段级失效、异常隔离和空值过滤，"
            "使画像服务调用量减少 70%+，高并发场景下 P99 延迟下降约 60%。"
            "设计并落地基于 Redis 注册表 + 内存回退机制的异步 Warm-Up 架构，"
            "将首屏建议生成与用户主请求解耦，首屏冷启动时间降低 60%+。"
            "主导商品详情页推荐策略重构，设计「行为信号识别 -> 推荐方向决策 -> 兜底生成」多层决策框架。"
            "基于约 800 个真实商品详情页场景建立推荐效果分析体系，将分析结果转化为推荐规则与安全门控策略。"
        ),
        "evidence": ["+15% engagement", "-60% cold start", "-70% profile calls", "800+ scenarios", "-60% P99 latency"],
        "skills": ["Personalization", "LLM", "Redis", "Caching", "Warm-Up", "Evaluation"],
    },
    {
        "id": "agent-runtime",
        "company": "Zalando",
        "title": "Agent Runtime Upgrade & Real-Time Response Optimization",
        "summary_en": (
            "Upgraded the main Zalando Assistant Agent Runtime by integrating product-detail tools, "
            "redesigning Streaming response handling, and migrating to the OpenAI Responses API. "
            "Integrated product-detail Tool Calling, enabling the Agent to retrieve real-time product information "
            "based on user intent and produce more grounded shopping responses. "
            "Designed Streaming processing for multi-step Agent flows using a state machine to separate process states, "
            "business events, and final response text — preventing duplicated display and event-ordering issues in multi-tool scenarios. "
            "Reduced Suggestions API average TTFT by ~25% in benchmark tests vs the prior synchronous interface. "
            "Migrated the main Agent Runtime from Chat Completions to OpenAI Responses API, "
            "unifying Tool Calling and Streaming and reducing P95 TTFT by ~25% in validated flows."
        ),
        "summary_zh": (
            "负责 Zalando Assistant Agent 主链路升级：商品详情 Tool 接入、Streaming 架构优化及 OpenAI Responses API 迁移。"
            "设计并实现商品详情 Tool 接入方案，使 Agent 能动态触发工具调用并整合实时商品信息。"
            "设计基于状态机的 Streaming 处理与分发机制，区分过程状态、业务事件和最终回复文本，"
            "解决多工具调用场景下的重复展示与时序错乱问题。"
            "基准测试中 Suggestions API 流式输出 TTFT 平均降低约 25%。"
            "完成 Agent 主链路从 Chat Completions 向 Responses API 的迁移，P95 TTFT 降低约 25%。"
        ),
        "evidence": ["-25% avg TTFT", "-25% P95 TTFT", "Streaming stability", "OpenAI Responses API", "Tool Calling"],
        "skills": ["Agent Runtime", "Tool Calling", "Streaming", "OpenAI Responses API", "Observability", "State Machine"],
    },
    {
        "id": "product-comparison",
        "company": "Zalando",
        "title": "Product Comparison Skill",
        "summary_en": (
            "Designed and launched the Product Comparison Skill for Zalando Assistant, enabling users to compare "
            "multiple products through natural language and make purchase decisions more efficiently. "
            "Increased comparison-scenario engagement by 20%+. "
            "Built context-aware product reference parsing to resolve product selections across multi-turn conversations, "
            "including position-based, range-based, and follow-up comparison requests. "
            "Developed dynamic comparison-dimension selection based on user intent, product attributes, and category characteristics. "
            "Separated model reasoning from table generation: the model handles intent understanding and summary recommendations, "
            "while deterministic code owns field parsing, discount calculation, layout, and rendering markers — "
            "eliminating LLM table formatting instability."
        ),
        "summary_zh": (
            "设计并上线 Product Comparison Skill，帮助用户通过自然语言完成多商品比较与决策，"
            "上线后对比场景用户互动率提升 20%+。"
            "构建上下文商品解析机制，解决用户通过序号、范围或追加表达引用商品时的对象定位问题。"
            "动态选择比较维度，结合用户关注点、商品属性和品类特征展示差异化信息。"
            "拆分模型推理与表格生成职责，由代码负责字段解析、折扣计算、布局和渲染标记，"
            "解决纯 LLM 生成表格格式不稳定、字段缺失和前端难以渲染的问题。"
        ),
        "evidence": ["+20% engagement", "Multi-turn references", "Structured output", "Stable rendering"],
        "skills": ["Product Comparison", "Structured Output", "Tool Calling", "Multi-turn"],
    },
    {
        "id": "text2sql",
        "company": "Thoughtworks · Major Domestic Bank",
        "title": "Text2SQL AI Agent — Pricing Management System",
        "summary_en": (
            "Built an enterprise data-analysis Agent for a major domestic bank to empower non-technical staff "
            "with self-service natural-language querying of structured data and internal policy Q&A. "
            "Designed and implemented a multi-stage intelligent agent workflow: "
            "intent clarification → SQL generation → query execution → result summarization and visualization. "
            "Created and optimized prompt templates for complex business queries, improving model accuracy by ~20% "
            "and enhancing handling of nested conditions and multi-field constraints. "
            "Built a test suite with 1,000+ real-world business cases for evaluation and regression. "
            "Engineered a dual-layer reranking mechanism (field + value) using vector search (FAISS), "
            "and integrated SQL validation, exception handling, and automatic retry logic to improve robustness."
        ),
        "summary_zh": (
            "为国内知名银行构建企业数据分析 Agent，支持非技术人员通过自然语言查询结构化数据和政策问答。"
            "设计并实现「意图澄清 -> SQL 生成 -> 查询执行 -> 结果总结与可视化」多阶段 Agent 工作流。"
            "持续迭代 Prompt 模板，构建 1000+ 条真实业务测试集，提升端到端问答准确率 20%+。"
            "基于向量数据库构建字段 + 值双层 Rerank 机制；引入 SQL 校验、异常重试等机制增强链路稳定性。"
        ),
        "evidence": ["+20% accuracy", "1,000+ eval cases", "Dual-layer rerank", "Multi-stage pipeline", "SQL validation"],
        "skills": ["Text2SQL", "RAG", "Reranking", "FAISS", "Evaluation", "Prompt Engineering", "LlamaIndex"],
    },
    {
        "id": "rag-chatbot",
        "company": "Thoughtworks",
        "title": "RAG Enterprise Chatbot — Knowledge Q&A System",
        "summary_en": (
            "Built a reusable RAG pipeline using LlamaIndex and FAISS, covering document chunking, vectorization, "
            "retrieval, and answer generation. "
            "Introduced RAGAS to evaluate answer relevance and context coverage, "
            "forming a reusable RAG development and evaluation template for enterprise knowledge Q&A."
        ),
        "summary_zh": (
            "基于 LlamaIndex + FAISS 构建文档切片、向量化、召回与答案生成链路，"
            "引入 RAGAS 评估答案相关性和上下文覆盖率，形成可复用的 RAG 研发与评估模板。"
        ),
        "evidence": ["LlamaIndex + FAISS pipeline", "RAGAS evaluation", "Reusable RAG template"],
        "skills": ["RAG", "LlamaIndex", "FAISS", "Embedding", "RAGAS", "Prompt Engineering"],
    },
    {
        "id": "pricing-system",
        "company": "Thoughtworks · Major Domestic Bank",
        "title": "Pricing Management System — Access Control & Reporting",
        "summary_en": (
            "Led access-control module design based on Hexagonal Architecture and Domain-Driven Design (DDD). "
            "Built a Tablesaw-based in-memory data processing solution for reporting, improving reporting development efficiency by ~40%. "
            "Drove a zero-impact MySQL database migration supporting millions of daily pricing requests. "
            "Also owned the after-sales management module backend architecture and API integration across headquarters, "
            "platform services, and WMS — delivered 100% on time, resolved 98% of integration blockers, "
            "supporting tens of thousands of daily spare-part transactions after launch."
        ),
        "summary_zh": (
            "主导基于六边形架构 + DDD 的权限模块设计，自研 Tablesaw 内存数据加工方案，报表开发效率提升约 40%。"
            "推动 MySQL 到新架构的数据库迁移，实现 0 业务感知、每日数百万笔定价请求稳定运行。"
            "负责售后模块后端架构与 API 对接，协调总部、中台、WMS 多系统集成；"
            "联调阻塞修复率约 98%，系统上线后支撑日均数万级备件交易流转。"
        ),
        "evidence": ["+40% reporting efficiency", "Zero-impact DB migration", "Millions of daily pricing requests", "98% blocker resolution"],
        "skills": ["Hexagonal Architecture", "DDD", "Java", "Spring Cloud", "MySQL", "Tablesaw"],
    },
]

SUGGESTED_QUESTIONS = {
    "en": [
        "What AI Agent systems has Lu built?",
        "Show Lu's Streaming and Tool Calling experience.",
        "What measurable impact does Lu have?",
        "Explain Lu's Text2SQL experience.",
    ],
    "zh": [
        "汪露做过哪些 AI Agent 系统？",
        "展示 Streaming 和 Tool Calling 经验。",
        "有哪些可量化结果？",
        "介绍 Text2SQL 项目经验。",
    ],
}
