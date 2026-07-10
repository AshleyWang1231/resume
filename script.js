const API = "https://resume-gent-api-vtugquposb.cn-hangzhou.fcapp.run";
const STREAM_TIMEOUT_MS = 30000;
const TERMINAL_RENDER_DELAY_MS = 35;
const TERMINAL_RENDER_CHARS = 5;

const T = {
  en: {
    eyebrow: "Senior AI Agent Engineer",
    navMarket: "Market fit",
    navCapabilities: "Capabilities",
    navProof: "Proof",
    navSystem: "System",
    downloadResume: "PDF",
    heroKicker: "Senior AI Agent Engineer",
    heroTitle: "I build production AI agents that hiring teams can trust.",
    heroLead: "Senior AI engineering is no longer just prompt craft. It is runtime architecture, tool orchestration, grounded retrieval, evaluation systems, latency discipline, and product ownership. My work spans live e-commerce agents at Zalando and enterprise data agents at Thoughtworks.",
    heroAsk: "Ask the resume agent",
    heroWork: "View selected work",
    consoleLine1: "Profile loaded: Zalando · Thoughtworks · Agent Runtime · Streaming · Text2SQL",
    consoleLine2: "Ready. Ask naturally, or use commands like /projects.",
    commandPlaceholder: "Ask about Streaming, or type /projects",

    marketKicker: "Role fit",
    marketTitle: "What AI Agent roles screen for — mapped to evidence.",
    marketDesc: "Current AI Agent / AI Engineer roles evaluate production LLM systems, orchestration, grounding, evals, reliability, and senior ownership. This section maps those requirements to concrete work.",

    capKicker: "Senior capability map",
    capTitle: "A senior AI engineer owns the system around the model.",
    capDesc: "The strongest signal is not a list of model APIs; it is how the runtime, retrieval, evaluation, product UX, and business constraints work together.",

    proofKicker: "Proof of seniority",
    proofTitle: "Three signals beyond a normal resume.",
    proof1Title: "Architecture, not wrappers",
    proof1: "Designed the agent loop: intent routing, tool dispatch, typed Streaming events, session state, provider fallback, and evidence grounding.",
    proof2Title: "Quality gates, not vibes",
    proof2: "Built 1,000+ Text2SQL cases, 800+ recommendation scenarios, retrieval metrics, and LLM-as-Judge checks.",
    proof3Title: "Measured production outcomes",
    proof3: "Shipped improvements users and systems felt: -25% TTFT, -60% cold-start, -70% profile calls, and +20% Text2SQL accuracy.",
    cap1Title: "Agent Runtime & Tool Orchestration",
    cap1: "I design the runtime loop that makes agents reliable: tool dispatch with Pydantic-validated schemas, a Streaming layer that separates intermediate tool events from user-visible text, and multi-turn session management. Built at Zalando for a live shopping assistant handling real user traffic.",
    cap2Title: "Streaming UX & Real-Time Performance",
    cap2: "Typed SSE event streams that give users instant feedback: tool progress, intermediate states, and final text each arrive as distinct events. Reduced TTFT by ~25% on Zalando's Suggestions API. Solved FC-specific streaming termination bugs in production.",
    cap3Title: "Personalization & Recommendation Systems",
    cap3: "End-to-end personalization pipelines combining conversation context, user profiles, and behavioural signals. Designed async Warm-Up (Redis registry + in-memory fallback) to decouple LLM generation from request latency. Evaluation-driven iteration across 800+ real product scenarios.",
    cap4Title: "Text2SQL & Enterprise RAG",
    cap4: "Multi-stage agent workflows for structured data access: intent clarification → SQL generation → validation + retry → result summarisation. Dual-layer vector reranking (field + value) to reduce schema hallucination. Built 1,000+ case eval suites as regression baselines.",

    agentQ1: "What are Lu's strongest technical areas?",
    agentQ2: "What's the biggest performance win Lu has shipped to production?",
    agentQ3: "How did Lu build an LLM agent reliable enough for a real bank?",
    agentQ4: "How has Lu's work spanned both e-commerce and financial AI?",
    agentThinking: "Calling tools...",
    agentError: "The resume agent is temporarily unavailable. Please try again later.",

    impactKicker: "Selected outcomes",
    impactTitle: "Four numbers from four different problems.",
    impactCtx1: "Zalando Assistant · Streaming redesign",
    metric1: "TTFT reduction — Suggestions API benchmark after Streaming state-machine + OpenAI Responses API migration",
    impactCtx2: "Zalando Assistant · Personalization",
    metric2: "cold-start reduction — async Warm-Up architecture decoupled LLM generation from the request critical path",
    impactCtx3: "Zalando Assistant · Profile service",
    metric3: "profile-service calls eliminated after adding TTL cache layer with field-level invalidation",
    impactCtx4: "Thoughtworks · Text2SQL Agent",
    metric4: "accuracy improvement — from 1,000+ eval-case iteration cycle on real bank business queries",

    projectsKicker: "Related experience",
    projectsTitle: "Each case: problem → approach → outcome.",

    systemKicker: "This site's backend",
    systemTitle: "Agent Runtime · Agent Workflow · Tool Calling · Streaming",
    systemSummary: "A multi-turn agent built to demonstrate the same patterns I use professionally: a typed event stream that separates tool calls from answer text, Pydantic-validated tool schemas, a four-stage workflow loop, and multi-provider LLM fallback.",
    evalKicker: "How this backend is evaluated",
    evalTitle: "RAGAS-inspired: graph → questions → test.",
    evalDesc: "Each resume fact is a node; shared skills are edges. An LLM reverse-engineers questions from the graph — single-hop and multi-hop — producing a labelled test set that drives retrieval eval, agent regression, and LLM-as-Judge scoring.",
    evalFlow: `<span class="ef-src">RESUME_FACTS</span>  <span class="ef-note">(8 structured facts)</span>
      <span class="ef-tree">│</span>
      <span class="ef-tree">▼</span>
  <span class="ef-phase">[Graph]</span>  <span class="ef-note">node = fact,  edge = shared skill</span>
      <span class="ef-tree">│</span>    <span class="ef-note">e.g. "Tool Calling" links agent-runtime ↔ product-comparison</span>
      <span class="ef-tree">│</span>
      <span class="ef-tree">▼</span>
  <span class="ef-phase">[LLM reverse-engineering]</span>
      <span class="ef-tree">│</span>    <span class="ef-note">single-hop: 4 EN + 4 ZH questions per fact</span>
      <span class="ef-tree">│</span>    <span class="ef-note">multi-hop:  questions spanning 2 linked facts</span>
      <span class="ef-tree">│</span>    <span class="ef-arrow">→</span> <span class="ef-file">synthetic_gold.json</span>  <span class="ef-note">(~70 questions, with ground-truth doc IDs)</span>
      <span class="ef-tree">│</span>
      <span class="ef-tree">├──▶</span> <span class="ef-layer1">[Layer 1]</span>  Retrieval eval  <span class="ef-file">(test_retrieval_eval.py)</span>
      <span class="ef-tree">│</span>               <span class="ef-note">BM25+FAISS · assert top-3 hit · P@K / R@K / MRR · no LLM · CI every push</span>
      <span class="ef-tree">│</span>
      <span class="ef-tree">├──▶</span> <span class="ef-layer2">[Layer 2]</span>  Agent regression  <span class="ef-file">(test_agent_eval.py)</span>
      <span class="ef-tree">│</span>               <span class="ef-note">full pipeline · keyword + evidence-ID assertions · CI every push</span>
      <span class="ef-tree">│</span>
      <span class="ef-tree">└──▶</span> <span class="ef-layer3">[Layer 3]</span>  LLM-as-Judge  <span class="ef-file">(test_llm_judge_eval.py)</span>
                      <span class="ef-note">faithfulness + answer relevance · JUDGE_EVAL=1</span>`,
    evalMetric1: "19/19",
    evalMetric1Label: "retrieval hit rate",
    evalMetric2: "0.947",
    evalMetric2Label: "MRR (gold queries)",
    evalMetric3: "82",
    evalMetric3Label: "CI tests passing",

    contactKicker: "Contact",
    contactTitle: "Open to AI software engineering roles.",
    phone: "+86 13122038365",
    cmdUnknown: "Unknown command. Try /capabilities, /projects, /system, or /ask ...",
    cmdScrolled: "Navigated to",
    cmdAsking: "Forwarding to Resume Agent",
    pillsCommands: "Commands",
    pillsQuestions: "Questions",
  },
  zh: {
    eyebrow: "Senior AI Agent Engineer",
    navMarket: "岗位匹配",
    navCapabilities: "核心能力",
    navProof: "证据",
    navSystem: "系统",
    downloadResume: "简历 PDF",
    heroKicker: "Senior AI Agent Engineer",
    heroTitle: "我构建招聘团队真正信任的生产级 AI Agent。",
    heroLead: "Senior AI 工程不只是 Prompt，而是 Runtime 架构、工具编排、可信检索、评估体系、延迟纪律和产品 ownership。我的经验覆盖 Zalando 真实用户流量的电商 Agent，以及 Thoughtworks 金融企业数据 Agent。",
    heroAsk: "询问简历 Agent",
    heroWork: "查看项目",
    consoleLine1: "Profile loaded: Zalando · Thoughtworks · Agent Runtime · Streaming · Text2SQL",
    consoleLine2: "Ready. 可以直接提问，也可以使用 /projects 这类命令。",
    commandPlaceholder: "询问 Streaming 架构，或输入 /projects",

    marketKicker: "岗位匹配",
    marketTitle: "AI Agent 岗位筛选什么能力——逐项映射到证据。",
    marketDesc: "当前 AI Agent / AI Engineer 岗位看重生产级 LLM 系统、编排、可信检索、评估、可靠性和 senior ownership。这里把这些要求映射到具体项目。",

    capKicker: "Senior 能力地图",
    capTitle: "Senior AI Engineer 负责模型之外的整个系统。",
    capDesc: "最强信号不是会调用多少模型 API，而是 Runtime、检索、评估、产品体验和业务约束如何协同。",

    proofKicker: "Senior 证据",
    proofTitle: "普通简历之外的三个信号。",
    proof1Title: "是架构，不是 wrapper",
    proof1: "设计 Agent 循环：意图路由、工具分发、类型化 Streaming 事件、会话状态、多 Provider 降级和证据 grounding。",
    proof2Title: "是质量门控，不是感觉",
    proof2: "构建 1,000+ Text2SQL 用例、800+ 推荐场景、检索指标和 LLM-as-Judge 检查。",
    proof3Title: "是生产结果，不是 Demo",
    proof3: "交付用户和系统都能感知的结果：TTFT -25%、冷启动 -60%、画像调用 -70%、Text2SQL 准确率 +20%。",
    cap1Title: "Agent Runtime 与工具编排",
    cap1: "设计让 Agent 可靠运行的 Runtime 循环：Pydantic 校验工具 Schema、将工具中间事件与用户可见文本分离的 Streaming 分发层、多轮会话管理。在 Zalando 面向真实用户流量的购物助手上落地。",
    cap2Title: "Streaming 体验与实时性能",
    cap2: "类型化 SSE 事件流让用户即时获得反馈：工具进度、中间状态和最终文本各自独立到达。在 Zalando Suggestions API 上将 TTFT 降低约 25%。在生产环境解决了函数计算特有的 Streaming 终止问题。",
    cap3Title: "个性化与推荐系统",
    cap3: "融合对话上下文、用户画像和行为信号的端到端个性化链路。设计基于 Redis 注册表的异步 Warm-Up 架构，将 LLM 生成从请求关键路径解耦。基于 800+ 真实商品场景的评估驱动迭代。",
    cap4Title: "Text2SQL 与企业级 RAG",
    cap4: "面向结构化数据访问的多阶段 Agent 流水线：意图澄清 → SQL 生成 → 校验重试 → 结果总结。字段+值双层向量 Rerank 降低 schema 幻觉。构建 1,000+ 用例评估集作为回归基线。",

    agentQ1: "汪露最擅长哪些技术方向？",
    agentQ2: "汪露交付过最大的性能优化是什么？",
    agentQ3: "汪露是怎么让 LLM Agent 在银行生产环境可靠运行的？",
    agentQ4: "汪露的经验是怎么覆盖电商和金融两个领域的？",
    agentThinking: "正在调用工具...",
    agentError: "简历 Agent 暂时不可用，请稍后再试。",

    impactKicker: "典型结果",
    impactTitle: "四个数字，来自四个不同的工程问题。",
    impactCtx1: "Zalando Assistant · Streaming 重设计",
    metric1: "TTFT 降低 — Suggestions API 基准测试，Streaming 状态机 + OpenAI Responses API 迁移后",
    impactCtx2: "Zalando Assistant · 个性化",
    metric2: "冷启动降低 — 异步 Warm-Up 架构将 LLM 生成从请求关键路径解耦",
    impactCtx3: "Zalando Assistant · 画像服务",
    metric3: "画像服务调用消除 — TTL 缓存层 + 字段级失效",
    impactCtx4: "Thoughtworks · Text2SQL Agent",
    metric4: "准确率提升 — 基于银行真实业务查询的 1,000+ 用例迭代",

    projectsKicker: "相关项目经验",
    projectsTitle: "每个案例：问题 → 方案 → 结果。",

    systemKicker: "本站后端",
    systemTitle: "Agent Runtime · Agent Workflow · Tool Calling · Streaming",
    systemSummary: "一个多轮有状态 Agent，展示了我在工作中使用的相同模式：类型化事件流区分工具调用与回答文本，Pydantic 校验工具 Schema，四阶段工作流循环，多 Provider LLM 降级。",
    evalKicker: "本站后端如何评估",
    evalTitle: "RAGAS 思路：构建知识图谱，逆推问题，再来测试。",
    evalDesc: "每条简历 fact 是一个节点，共享技能是边。LLM 从图中逆向生成问题——单跳和多跳——产出带 ground-truth 的测试集，驱动检索评估、Agent 回归和 LLM-as-Judge 三层测试。",
    evalFlow: `<span class="ef-src">RESUME_FACTS</span>  <span class="ef-note">（8 条结构化 fact）</span>
      <span class="ef-tree">│</span>
      <span class="ef-tree">▼</span>
  <span class="ef-phase">[Graph]</span>  <span class="ef-note">节点 = fact，边 = 共享技能</span>
      <span class="ef-tree">│</span>    <span class="ef-note">例：「Tool Calling」连接 agent-runtime ↔ product-comparison</span>
      <span class="ef-tree">│</span>
      <span class="ef-tree">▼</span>
  <span class="ef-phase">[LLM 逆向生成问题]</span>
      <span class="ef-tree">│</span>    <span class="ef-note">单跳：每个 fact 生成 4 EN + 4 ZH 问题</span>
      <span class="ef-tree">│</span>    <span class="ef-note">多跳：跨两个相连 fact 的综合问题</span>
      <span class="ef-tree">│</span>    <span class="ef-arrow">→</span> <span class="ef-file">synthetic_gold.json</span>  <span class="ef-note">（约 70 条，含 ground-truth 文档 ID）</span>
      <span class="ef-tree">│</span>
      <span class="ef-tree">├──▶</span> <span class="ef-layer1">[Layer 1]</span>  检索评估  <span class="ef-file">(test_retrieval_eval.py)</span>
      <span class="ef-tree">│</span>               <span class="ef-note">BM25+FAISS · 断言 top-3 命中 · P@K / R@K / MRR · 无 LLM · CI 每次跑</span>
      <span class="ef-tree">│</span>
      <span class="ef-tree">├──▶</span> <span class="ef-layer2">[Layer 2]</span>  Agent 回归  <span class="ef-file">(test_agent_eval.py)</span>
      <span class="ef-tree">│</span>               <span class="ef-note">完整链路 · 关键词 + evidence ID 断言 · CI 每次跑</span>
      <span class="ef-tree">│</span>
      <span class="ef-tree">└──▶</span> <span class="ef-layer3">[Layer 3]</span>  LLM-as-Judge  <span class="ef-file">(test_llm_judge_eval.py)</span>
                      <span class="ef-note">忠实度 + 相关性 · JUDGE_EVAL=1 手动跑</span>`,
    evalMetric1: "19/19",
    evalMetric1Label: "检索命中率",
    evalMetric2: "0.947",
    evalMetric2Label: "MRR（gold 查询集）",
    evalMetric3: "82",
    evalMetric3Label: "CI 通过测试数",

    contactKicker: "联系",
    contactTitle: "正在寻找 AI 软件工程相关机会。",
    phone: "13122038365（微信同号）",
    cmdUnknown: "未知命令。可以试试 /capabilities、/projects、/system 或 /ask ...",
    cmdScrolled: "已跳转到",
    cmdAsking: "正在转交给简历 Agent",
    pillsCommands: "命令",
    pillsQuestions: "问题",
  },
};

const MARKET_SIGNALS_FALLBACK = {
  title_en: "What AI Agent roles are screening for",
  title_zh: "AI Agent 岗位正在筛选什么能力",
  summary_en: "Production LLM systems, orchestration, grounding, evals, reliability, and senior ownership.",
  summary_zh: "生产级 LLM 系统、编排、可信检索、评估、可靠性和 senior ownership。",
  signals: [
    {
      id: "agent-orchestration",
      requirement_en: "Agent orchestration, tool calling, workflow design, and state management",
      requirement_zh: "Agent 编排、工具调用、工作流设计与状态管理",
      evidence_en: "Built Zalando Assistant Agent Runtime with Tool Calling, typed Streaming events, multi-turn state, and OpenAI Responses API migration.",
      evidence_zh: "构建 Zalando Assistant Agent Runtime，覆盖 Tool Calling、类型化 Streaming 事件、多轮状态与 OpenAI Responses API 迁移。",
      senior_signal_en: "Can design the runtime loop, not only prompt a model.",
      senior_signal_zh: "不仅会写 Prompt，而是能设计 Agent Runtime 循环。",
      proof_project_ids: ["agent-runtime", "product-comparison"],
    },
    {
      id: "evaluation",
      requirement_en: "Evaluation systems, regression suites, LLM-as-judge, and quality gates",
      requirement_zh: "评估体系、回归测试集、LLM-as-Judge 与质量门控",
      evidence_en: "Built 1,000+ Text2SQL eval cases, 800+ product-detail scenarios, and RAGAS-inspired tests for this site.",
      evidence_zh: "构建 1,000+ Text2SQL 评估用例、800+ 商品场景，以及本站 RAGAS 思路测试。",
      senior_signal_en: "Treats evals as production infrastructure.",
      senior_signal_zh: "将评估作为生产基础设施。",
      proof_project_ids: ["text2sql", "rag-chatbot"],
    },
    {
      id: "latency-observability",
      requirement_en: "Latency, observability, streaming UX, fallbacks, and production reliability",
      requirement_zh: "延迟、可观测性、Streaming 体验、降级与生产可靠性",
      evidence_en: "Reduced TTFT by 25%, reduced cold-start by 60%, added SSE events and deterministic evidence fallback.",
      evidence_zh: "TTFT 降低 25%，冷启动降低 60%，并具备 SSE 事件和确定性证据兜底。",
      senior_signal_en: "Optimizes for user-perceived latency and failure modes.",
      senior_signal_zh: "围绕用户感知延迟和失败模式优化。",
      proof_project_ids: ["agent-runtime", "personalization"],
    },
  ],
};

const SENIOR_CAPABILITIES_FALLBACK = {
  title_en: "Senior AI engineering capability map",
  title_zh: "Senior AI 工程能力地图",
  summary_en: "Architecture judgment, reliability, eval discipline, product ownership, and model/code boundary design.",
  summary_zh: "架构判断、可靠性、评估纪律、产品 ownership 和模型/代码边界设计。",
  capabilities: [
    {
      id: "runtime-architecture",
      title_en: "Agent runtime architecture",
      title_zh: "Agent Runtime 架构",
      narrative_en: "Designs the loop that coordinates tools, state, streaming, providers, and fallback behavior.",
      narrative_zh: "设计协调工具、状态、Streaming、Provider 与降级行为的运行循环。",
      evidence_en: "Zalando Assistant runtime: Tool Calling, typed SSE Streaming, multi-turn state, Responses API migration, -25% TTFT.",
      evidence_zh: "Zalando Assistant Runtime：Tool Calling、类型化 SSE Streaming、多轮状态、Responses API 迁移，TTFT -25%。",
      proof_project_ids: ["agent-runtime"],
      keywords: ["Agent Runtime", "Tool Calling", "Streaming"],
    },
    {
      id: "evaluation-systems",
      title_en: "Evaluation and regression systems",
      title_zh: "评估与回归体系",
      narrative_en: "Builds eval loops that make AI changes measurable and safe to ship.",
      narrative_zh: "构建让 AI 改动可度量、可安全上线的评估闭环。",
      evidence_en: "1,000+ Text2SQL cases, 800+ recommendation scenarios, retrieval MRR and LLM-as-judge tests.",
      evidence_zh: "1,000+ Text2SQL 用例、800+ 推荐场景、检索 MRR 与 LLM-as-Judge 测试。",
      proof_project_ids: ["text2sql", "rag-chatbot"],
      keywords: ["Evaluation", "RAGAS", "LLM-as-Judge"],
    },
    {
      id: "enterprise-ai",
      title_en: "Enterprise AI and data systems",
      title_zh: "企业 AI 与数据系统",
      narrative_en: "Connects agent workflows to SQL, permissions, reporting, and operational data constraints.",
      narrative_zh: "将 Agent 工作流连接到 SQL、权限、报表和运营数据约束。",
      evidence_en: "Bank Text2SQL, SQL validation/retry, DDD access control, Tablesaw reporting, zero-impact migration.",
      evidence_zh: "银行 Text2SQL、SQL 校验重试、DDD 权限、Tablesaw 报表与零感知迁移。",
      proof_project_ids: ["text2sql", "pricing-management"],
      keywords: ["Text2SQL", "SQL Validation", "DDD"],
    },
  ],
};

let lang = localStorage.getItem("resume-lang") || "en";
let cachedProjects = null;
let cachedArch = null;
let cachedMarketSignals = null;
let cachedCapabilities = null;
let sessionId = null;
const warmupCache = {};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];
const t = (key) => T[lang][key] || T.en[key] || key;

function escapeHtml(value = "") {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

/**
 * Strip LLM formatting artifacts from a completed answer string.
 * Mirrors the server-side sanitise_answer() as a client-side safety net,
 * applied once to the full text after streaming completes.
 *   - XML/HTML tags: <error>…</error>
 *   - Markdown headers: ###, ##, #
 *   - Bold/italic: **x**, *x*, __x__, _x_
 *   - List markers: leading - or * or 1.
 */
function sanitiseAnswer(text) {
  if (!text) return text;
  text = text.replace(/<\/?[a-z][a-z0-9]*(?:\s[^>]*)?>/gi, "");  // XML tags
  text = text.replace(/^#{1,6}\s+/gm, "");                        // ### headers
  text = text.replace(/(\*{1,3}|_{1,3})(.+?)\1/gs, "$2");         // **bold** / *italic*
  text = text.replace(/^[\-\*]\s+/gm, "");                        // - list items (unordered only)
  // numbered sentences like "1. The problem was..." are kept as structured prose
  text = text.replace(/\n{3,}/g, "\n\n");                         // collapse blank lines
  return text.trim();
}

function applyLang() {
  const dictionary = T[lang];
  document.documentElement.lang = lang === "zh" ? "zh-CN" : "en";
  $$("[data-i18n]").forEach((el) => {
    const key = el.dataset.i18n;
    if (dictionary[key]) el.textContent = dictionary[key];
  });
  $$("[data-i18n-html]").forEach((el) => {
    const key = el.dataset.i18nHtml;
    if (dictionary[key]) el.innerHTML = dictionary[key];
  });
  $$("[data-i18n-placeholder]").forEach((el) => {
    const key = el.dataset.i18nPlaceholder;
    if (dictionary[key]) el.placeholder = dictionary[key];
  });
  const toggle = $("[data-lang-toggle]");
  if (toggle) toggle.textContent = lang === "zh" ? "EN" : "中文";
  localStorage.setItem("resume-lang", lang);
  renderProjects(cachedProjects);
  renderArchitecture(cachedArch);
  renderMarketSignals(cachedMarketSignals);
  renderSeniorCapabilities(cachedCapabilities);
}

function addConsoleLine(command, result) {
  const feed = $("[data-command-feed]");
  if (!feed) return;
  const cmd = document.createElement("p");
  cmd.innerHTML = `<span class="prompt">lu@resume</span> ${escapeHtml(command)}`;
  const out = document.createElement("span");
  out.className = "console-result";
  out.textContent = result;
  feed.append(cmd, out);
  feed.scrollTop = feed.scrollHeight;
}

function addTerminalMessage(role, text) {
  const feed = $("[data-command-feed]");
  if (!feed) return null;
  const article = document.createElement("article");
  article.className = `console-message console-${role}`;
  const label = role === "user" ? "you" : role === "tool" ? "tool" : "agent";
  article.innerHTML = `<span class="console-label">${label}</span><p>${escapeHtml(text)}</p>`;
  feed.append(article);
  feed.scrollTop = feed.scrollHeight;
  return article;
}

function openTerminal() {
  const float = $("#terminal-float");
  if (!float) return;
  float.classList.add("open");
  document.body.classList.add("terminal-open");
  window.setTimeout(() => $("[data-command-input]")?.focus({ preventScroll: true }), 80);
}

function closeTerminal() {
  const float = $("#terminal-float");
  if (float) float.classList.remove("open");
  document.body.classList.remove("terminal-open");
}

function focusTerminal() {
  openTerminal();
}

function scrollToSection(id) {
  if (id === "top") {
    window.scrollTo({ top: 0, behavior: "smooth" });
    return true;
  }
  const target = document.getElementById(id);
  if (!target) return false;
  target.scrollIntoView({ behavior: "smooth", block: "start" });
  return true;
}

function runCommand(rawCommand) {
  const raw = rawCommand.trim();
  if (!raw) return;
  const command = raw.startsWith("/") ? raw : raw;
  const lower = command.toLowerCase();
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

  if (lower === "/agent") {
    focusTerminal();
    return;
  }

  if (lower.startsWith("/ask ")) {
    const question = command.slice(5).trim();
    if (question) {
      addConsoleLine(command, t("cmdAsking"));
      sendMessage(question);
    }
    return;
  }

  if (!raw.startsWith("/")) {
    sendMessage(raw);
    return;
  }

  if (routes[lower]) {
    scrollToSection(routes[lower]);
    addConsoleLine(command, `${t("cmdScrolled")}: ${routes[lower]}`);
    return;
  }

  addConsoleLine(command, t("cmdUnknown"));
}

function bindCommandConsole() {
  const form = $("[data-command-form]");
  const input = $("[data-command-input]");
  if (input) input.value = "";
  form?.addEventListener("submit", (event) => {
    event.preventDefault();
    const command = input.value;
    input.value = "";
    runCommand(command);
  });
  $$("[data-run-command], [data-command], .pill-q").forEach((el) => {
    el.addEventListener("click", (event) => {
      if (el.classList.contains("pill-q")) {
        event.preventDefault();
        const question = lang === "zh" ? (el.dataset.qZh || el.textContent.trim()) : (el.dataset.qEn || el.textContent.trim());
        openTerminal();
        sendMessage(question);
        return;
      }
      const command = el.dataset.runCommand || el.dataset.command;
      if (!command) return;
      if (command.startsWith("/")) event.preventDefault();
      openTerminal();
      runCommand(command);
    });
  });
  $$("[data-focus-terminal]").forEach((el) => {
    el.addEventListener("click", () => openTerminal());
  });
}

function bindFab() {
  $("#terminal-toggle")?.addEventListener("click", () => closeTerminal());
  $("#terminal-launcher")?.addEventListener("click", () => openTerminal());
}

function bindBackground() {
  const root = document.documentElement;
  window.addEventListener("pointermove", (event) => {
    root.style.setProperty("--mouse-x", `${event.clientX}px`);
    root.style.setProperty("--mouse-y", `${event.clientY}px`);
  }, { passive: true });
}

function animateCounter(el) {
  const target = Number.parseInt(el.dataset.count, 10);
  const prefix = el.dataset.prefix || "";
  const suffix = el.dataset.suffix || "";
  const duration = 1200;
  const start = performance.now();
  const ease = (x) => 1 - Math.pow(1 - x, 3);
  function frame(now) {
    const progress = Math.min((now - start) / duration, 1);
    const value = Math.round(ease(progress) * target);
    el.textContent = `${prefix}${value.toLocaleString()}${suffix}`;
    if (progress < 1) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}

function bindMetricObserver() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting && !entry.target.dataset.animated) {
        entry.target.dataset.animated = "1";
        animateCounter(entry.target);
      }
    });
  }, { threshold: 0.5 });
  $$("[data-count]").forEach((el) => observer.observe(el));
}

const PROJECTS_DATA = [{"id":"agent-runtime","title":"Agent Runtime & Streaming Architecture","company":"Zalando","period":"2025–2026","summary_en":"Redesigned the Zalando Assistant Agent Runtime — Streaming architecture, Tool Calling integration, OpenAI Responses API migration.","summary_zh":"重新设计 Zalando Assistant Agent Runtime，覆盖 Streaming 架构、Tool Calling 接入和 OpenAI Responses API 迁移。","star_s_en":"The assistant returned full responses only after all tool calls completed, giving users no visibility into agent progress and making interactions feel sluggish.","star_a_en":"Introduced a Streaming layer separating process states, business events, and user-visible text into typed SSE events. Integrated product-detail Tool Calling so answers are grounded in live catalogue data. Migrated the runtime from Chat Completions to OpenAI Responses API, unifying the Tool Calling + Streaming path.","star_r_en":"Average TTFT –25% (Suggestions API benchmark). P95 TTFT –25% in validated flows. Users see real-time tool progress instead of a blank wait.","star_s_zh":"助手需等所有工具调用完成后才整体输出，用户看不到任何进度，体验偏慢。","star_a_zh":"引入 Streaming 分发层，将过程状态、业务事件和用户可见文本拆分为类型化 SSE 事件。接入商品详情 Tool Calling，让回答基于实时商品数据。将主链路从 Chat Completions 迁移至 OpenAI Responses API，统一 Tool Calling + Streaming 路径。","star_r_zh":"平均 TTFT 降低 25%（Suggestions API 基准测试），P95 TTFT 降低 25%，用户实时可见工具调用进度。","impact":["-25% avg TTFT","-25% P95 TTFT","Typed SSE events","OpenAI Responses API"],"skills":["Agent Runtime","Tool Calling","Streaming","State Machine","OpenAI Responses API"],"highlight":true},{"id":"personalization","title":"Personalization & Warm-Up Architecture","company":"Zalando","period":"2025–2026","summary_en":"Built personalization pipeline and async Warm-Up architecture for Zalando Assistant Conversation Starters.","summary_zh":"为 Zalando Assistant Conversation Starters 构建个性化链路和异步 Warm-Up 架构。","star_s_en":"Conversation Starters used static signals only, called the profile service on every request, and had noticeable cold-start latency under traffic spikes.","star_a_en":"(1) Rebuilt the input pipeline to fuse real-time conversation context, user profile, and behaviour history. (2) Added a TTL cache layer with field-level invalidation in front of the profile service. (3) Designed an async Warm-Up: a Redis registry tracks pending first-screen requests; a background worker pre-generates suggestions; in-memory fallback handles cache misses.","star_r_en":"Conversation Starter engagement +15%. Cold-start time –60%. Profile-service calls –70%; P99 latency –60% under high concurrency. Validated across 800+ real product-detail-page scenarios.","star_s_zh":"Conversation Starters 仅依赖静态信号，每次请求都调用画像服务，高峰期冷启动延迟明显。","star_a_zh":"(1) 重建输入链路，融合实时对话上下文、用户画像和历史行为。(2) 在画像服务前加 TTL 缓存层，支持字段级失效。(3) 设计异步 Warm-Up：Redis 注册表追踪待处理首屏请求，后台 Worker 提前生成建议，内存降级兜底。","star_r_zh":"推荐入口互动率 +15%，冷启动时间 -60%，画像服务调用量 -70%，高并发下 P99 延迟 -60%。基于 800+ 真实商品页面场景验证。","impact":["+15% engagement","-60% cold-start","-70% profile calls","-60% P99 latency"],"skills":["Personalization","Redis","Async Warm-Up","Caching","Eval-Driven"],"highlight":true},{"id":"product-comparison","title":"Product Comparison Skill","company":"Zalando","period":"2025–2026","summary_en":"Designed and shipped a multi-turn product comparison capability for Zalando Assistant.","summary_zh":"为 Zalando Assistant 设计并上线多轮商品对比能力。","star_s_en":"Users asked to compare browsed products, but free-form LLM output was unreliable: table layouts broke, discount fields went missing, and multi-turn references (\"compare the first two\") were frequently misresolved.","star_a_en":"Split responsibilities: the model handles intent, conversation-state tracking, and summary copy; deterministic code owns product-reference resolution, field selection, discount calculation, and layout rendering. This gave the frontend a stable contract independent of model version.","star_r_en":"Comparison-scenario engagement +20%. Eliminated LLM formatting instability; frontend rendering is stable across model updates.","star_s_zh":"用户要求对比已浏览商品，但 LLM 直接输出格式不稳定：布局错乱、折扣字段缺失，多轮引用频繁解析错误。","star_a_zh":"责任拆分：模型负责意图理解、对话状态追踪和总结文案；确定性代码负责商品引用解析、字段选择、折扣计算和布局渲染，向前端提供与模型版本无关的稳定契约。","star_r_zh":"对比场景互动率 +20%，消除 LLM 格式不稳定问题，前端渲染跨模型版本保持稳定。","impact":["+20% engagement","Stable rendering","Multi-turn references","Model/code split"],"skills":["Structured Output","Tool Calling","Multi-turn","Deterministic Rendering"],"highlight":true},{"id":"text2sql","title":"Text2SQL AI Agent — Enterprise Data Analysis","company":"Thoughtworks · Major Domestic Bank","period":"2021–2025","summary_en":"Built an enterprise data-analysis Agent for a major domestic bank, enabling natural-language querying of complex structured data.","summary_zh":"为国内知名银行构建企业数据分析 Agent，支持复杂结构化数据的自然语言查询。","star_s_en":"Non-technical pricing analysts needed self-service access to complex structured data. Naive LLM prompts failed on nested conditions and ambiguous schema fields, bad SQL could corrupt pricing decisions, and there was no evaluation baseline.","star_a_en":"Designed a multi-stage agent pipeline: intent clarification → SQL generation → automated SQL validation → exception retry → result summarisation with visualisations. Built dual-layer vector reranking (field + value) to reduce schema hallucination. Created a 1,000+ case evaluation suite from real business queries as a regression baseline for all prompt changes.","star_r_en":"End-to-end query accuracy +20%. SQL validation + retry loop eliminated silent failures. 1,000+ eval cases became the team's standard regression baseline.","star_s_zh":"非技术定价分析师需自助查询复杂结构化数据，但直接 prompt LLM 在嵌套条件和歧义字段上错误率高，且缺乏评估基线。","star_a_zh":"设计多阶段 Agent 流水线：意图澄清 → SQL 生成 → 自动 SQL 校验 → 异常重试 → 结果总结与可视化。构建字段+值双层向量 Rerank 减少 schema 幻觉。从真实业务查询积累 1,000+ 条评估用例作为回归基线。","star_r_zh":"端到端查询准确率 +20%，SQL 校验+重试消除静默失败，1,000+ 评估用例成为团队标准回归基线。","impact":["+20% accuracy","1,000+ eval cases","Dual-layer rerank","Auto SQL validation"],"skills":["Text2SQL","Multi-stage Agent","FAISS","Reranking","SQL Validation","Evaluation"],"highlight":false},{"id":"pricing-management","title":"Pricing Management System — Access Control & Data Pipeline","company":"Thoughtworks · Major Domestic Bank","period":"2021–2025","summary_en":"Backend module owner for a bank-wide interest-rate product pricing platform — access control, reporting, and database migration.","summary_zh":"负责国内知名银行利率类金融产品定价管理系统的权限模块、报表模块及数据库迁移等核心工作。","star_s_en":"The pricing platform needed fine-grained access control across complex role hierarchies and multiple business lines, high-performance in-memory multi-dimensional aggregation for reporting, and a MySQL architecture struggling under millions of daily pricing transactions.","star_a_en":"(1) Led access control module design and implementation using Hexagonal Architecture and DDD — modelled complex role hierarchies and fine-grained permissions as a reusable domain layer adopted across multiple sub-systems. (2) Designed a custom in-memory data processing pipeline (Tablesaw + custom toolchain) for the reporting module to replace external dependencies. (3) Spearheaded the database migration strategy, delivering a zero-downtime production switchover for large-scale business tables.","star_r_en":"Reporting module dev efficiency +40%; delivery cycle shortened by 2+ weeks. Database migration achieved zero business impact, sustaining stable operation under millions of daily pricing requests. Access control module reused across multiple sub-systems.","star_s_zh":"定价平台需跨多业务线支持复杂角色层级与细粒度权限管理；报表模块需内存中多维聚合与计算；原 MySQL 架构在海量业务数据下存在性能瓶颈。","star_a_zh":"(1) 基于六边形架构与 DDD 主导权限模块设计与落地，构建可复用领域模型，在多个子系统中复用。(2) 针对报表模块自研内存数据加工方案（Tablesaw + 自定义工具链），替代外部依赖。(3) 主导数据库迁移方案设计与实施，完成生产环境平滑切换。","star_r_zh":"报表模块开发效率提升约 40%，开发工期缩短 2 周以上。数据库迁移实现 0 业务感知，系统在每日数百万笔定价请求下稳定运行。权限模块在多个子系统中复用。","impact":["+40% dev efficiency","–2 weeks cycle","0-downtime DB migration","Multi-system reuse"],"skills":["Spring Cloud","Hexagonal Architecture","Tablesaw","MySQL","Redis","RabbitMQ"],"highlight":false},{"id":"rag-chatbot","title":"RAG Knowledge Q&A System","company":"Thoughtworks","period":"2021–2025","summary_en":"Built a production RAG pipeline for enterprise policy Q&A alongside the Text2SQL agent.","summary_zh":"与 Text2SQL Agent 并行，构建企业政策问答生产级 RAG 流水线。","star_s_en":"The bank needed a reliable Q&A system over internal policy documents, with no existing retrieval infrastructure or quality measurement.","star_a_en":"Built a full RAG pipeline with LlamaIndex and FAISS — chunking strategy, embedding, vector retrieval, and answer generation. Introduced RAGAS evaluation (faithfulness, relevance, context coverage) as the quality gate, creating a reusable eval harness the team adopted for all subsequent RAG work.","star_r_en":"RAGAS faithfulness 0.82 / context recall 0.78 on internal policy Q&A benchmark. Eval harness adopted by 3 downstream RAG projects; reusable pipeline template cut average onboarding ~40%.","star_s_zh":"银行需要基于内部政策文档的可靠问答系统，无现有检索基础设施，也没有质量度量方式。","star_a_zh":"基于 LlamaIndex + FAISS 构建完整 RAG 流水线——切片策略、Embedding、向量检索和答案生成。引入 RAGAS（忠实性、相关性、上下文覆盖率）作为质量门控，形成团队后续 RAG 工作的可复用评估框架。","star_r_zh":"RAGAS 忠实性评分 0.82，上下文召回率 0.78。评估框架被 3 个后续 RAG 项目复用，可复用流水线模板将平均上线周期缩短约 40%。","impact":["Faithfulness 0.82","Context recall 0.78","-40% onboarding","3 projects adopted"],"skills":["RAG","LlamaIndex","FAISS","Embedding","RAGAS"],"highlight":false}];


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

async function loadProjects() {
  cachedProjects = PROJECTS_DATA;
  renderProjects(cachedProjects);
}

function renderProjects(projects) {
  if (!projects) return;
  const grid = $("[data-projects-grid]");
  if (!grid) return;
  grid.innerHTML = projects.map((project) => {
    const s = lang === "zh" ? project.star_s_zh : project.star_s_en;
    const a = lang === "zh" ? project.star_a_zh : project.star_a_en;
    const r = lang === "zh" ? project.star_r_zh : project.star_r_en;
    const hasStar = s && a && r;
    const body = hasStar
      ? `<div class="star-block">
          <div class="star-row"><span class="star-label star-s">S</span><p>${escapeHtml(s)}</p></div>
          <div class="star-row"><span class="star-label star-a">A</span><p>${escapeHtml(a)}</p></div>
          <div class="star-row"><span class="star-label star-r">R</span><p>${escapeHtml(r)}</p></div>
        </div>`
      : `<p>${escapeHtml(lang === "zh" ? project.summary_zh : project.summary_en)}</p>`;
    return `
    <article class="project-card ${project.highlight ? "highlight" : ""}">
      <div class="project-header">
        <div>
          <div class="project-company">${escapeHtml(project.company)}</div>
          <h3>${escapeHtml(project.title)}</h3>
        </div>
        <div class="project-period">${escapeHtml(project.period)}</div>
      </div>
      ${body}
      <div class="impact-chips">${project.impact.map((item) => `<span>${escapeHtml(item)}</span>`).join("")}</div>
      <div class="skill-chips">${project.skills.map((item) => `<span>${escapeHtml(item)}</span>`).join("")}</div>
    </article>`;
  }).join("");
}

async function loadArchitecture() {
  try {
    const res = await fetch(`${API}/api/architecture`);
    if (!res.ok) throw new Error("architecture failed");
    cachedArch = await res.json();
    renderArchitecture(cachedArch);
  } catch {
    const diagram = $("[data-arch-diagram]");
    if (diagram) diagram.innerHTML = `<p class="console-muted">${escapeHtml(t("agentError"))}</p>`;
  }
}

function renderArchitecture(arch) {
  if (!arch) return;
  const diagram = $("[data-arch-diagram]");
  const summary = $("[data-arch-summary]");
  if (diagram) {
    diagram.innerHTML = `<div class="arch-nodes">${arch.nodes.map((node) => `
      <div class="arch-node type-${escapeHtml(node.type)}">
        <div class="arch-node-label">${escapeHtml(node.label)}</div>
        <div class="arch-node-desc">${escapeHtml(node.description)}</div>
        <span class="arch-node-type">${escapeHtml(node.type)}</span>
      </div>
    `).join("")}</div>`;
  }
  if (summary) summary.textContent = lang === "zh" ? arch.summary_zh : arch.summary_en;
}

function addToolMsg(toolName) {
  return addTerminalMessage("tool", `tool_call: ${toolName}`);
}

function addEvidence(parent, evidence) {
  parent.querySelector(".evidence-list")?.remove();
  if (!evidence?.length) return;
  const list = document.createElement("div");
  list.className = "evidence-list";
  evidence.forEach((item) => {
    const card = document.createElement("div");
    card.className = "evidence-card";
    card.innerHTML = `
      <strong>${escapeHtml(item.title)}</strong>
      <span class="ev-company">${escapeHtml(item.company)}</span>
      <div class="ev-chips">
        ${(item.evidence || []).slice(0, 4).map((chip) => `<span>${escapeHtml(chip)}</span>`).join("")}
      </div>`;
    list.append(card);
  });
  parent.append(list);
  const feed = $("[data-command-feed]");
  if (feed) feed.scrollTop = feed.scrollHeight;
}

function scrollTerminalToBottom() {
  const feed = $("[data-command-feed]");
  if (feed) feed.scrollTop = feed.scrollHeight;
}

function createTerminalTextStreamer(el, done) {
  let queue = "";
  let timer = null;
  let closed = false;
  let finished = false;

  function finish() {
    if (finished) return;
    finished = true;
    done?.();
  }

  function flush() {
    if (!queue) {
      timer = null;
      if (closed) finish();
      return;
    }
    el.textContent += queue.slice(0, TERMINAL_RENDER_CHARS);
    queue = queue.slice(TERMINAL_RENDER_CHARS);
    scrollTerminalToBottom();
    timer = window.setTimeout(flush, TERMINAL_RENDER_DELAY_MS);
  }

  return {
    push(text = "") {
      queue += text;
      if (!timer) flush();
    },
    close() {
      closed = true;
      if (!timer && !queue) finish();
    },
    cancel() {
      if (timer) window.clearTimeout(timer);
      timer = null;
      queue = "";
      closed = true;
      finished = true;
    },
  };
}

function revealText(el, text, done) {
  const streamer = createTerminalTextStreamer(el, done);
  streamer.push(text);
  streamer.close();
}

async function sendMessage(message) {
  if (!message) return;
  addTerminalMessage("user", message);

  const cacheKey = `${lang}|${message}`;
  if (warmupCache[cacheKey]) {
    const data = warmupCache[cacheKey];
    if (data.session_id && !sessionId) sessionId = data.session_id;
    const answer = addTerminalMessage("assistant", "");
    revealText(answer.querySelector("p"), sanitiseAnswer(data.answer), () => addEvidence(answer, data.evidence));
    return;
  }

  const loading = addTerminalMessage("assistant", t("agentThinking"));
  const toolMessages = [];
  try {
    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), STREAM_TIMEOUT_MS);
    const res = await fetch(`${API}/api/chat/stream`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      signal: controller.signal,
      body: JSON.stringify({ message, language: lang, session_id: sessionId }),
    });
    window.clearTimeout(timeout);
    if (!res.ok || !res.body) throw new Error("stream failed");
    loading.remove();
    const answer = addTerminalMessage("assistant", "");
    const textEl = answer.querySelector("p");
    let pendingEvidence = null;
    const streamer = createTerminalTextStreamer(textEl, () => {
      if (pendingEvidence) addEvidence(answer, pendingEvidence);
    });
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const parts = buffer.split("\n\n");
      buffer = parts.pop() || "";
      for (const part of parts) {
        const eventLine = part.split("\n").find((line) => line.startsWith("event:"));
        const dataLine = part.split("\n").find((line) => line.startsWith("data:"));
        if (!eventLine || !dataLine) continue;
        const event = eventLine.replace("event:", "").trim();
        const payload = JSON.parse(dataLine.replace("data:", "").trim());
        if (event === "metadata" && payload.session_id) sessionId = payload.session_id;
        if (event === "tool_call") toolMessages.push(addToolMsg(payload.name));
        if (event === "answer_delta") {
          streamer.push(payload.text || "");
        }
        if (event === "evidence") {
          toolMessages.forEach((msg) => msg.remove());
          pendingEvidence = payload;
          textEl.textContent = sanitiseAnswer(textEl.textContent);
          // Only show evidence if there's actual answer text
          if (!textEl.textContent.trim()) pendingEvidence = null;
          streamer.close();
        }
        if (event === "done" && payload.session_id) sessionId = payload.session_id;
        if (event === "error") {
          streamer.cancel();
          textEl.textContent = payload.message || t("agentError");
        }
      }
    }
    streamer.close();
  } catch {
    loading.remove();
    try {
      const res = await fetch(`${API}/api/chat`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ message, language: lang, session_id: sessionId }),
      });
      if (!res.ok) throw new Error("chat failed");
      const data = await res.json();
      if (data.session_id) sessionId = data.session_id;
      const answer = addTerminalMessage("assistant", "");
      const answerText = sanitiseAnswer(data.answer || "");
      if (answerText) {
        revealText(answer.querySelector("p"), answerText, () => addEvidence(answer, data.evidence));
      } else {
        answer.querySelector("p").textContent = t("agentError");
      }
    } catch {
      addTerminalMessage("assistant", t("agentError"));
    }
  }
}

function bindAgent() {
  // suggestion-btn clicks handled via data-run-command in bindCommandConsole
}

async function warmup() {
  // Mark already-cached pills as ready immediately (static cache populated above)
  const allQuestions = [
    ["What are Lu's strongest technical areas?", "en"],
    ["What's the biggest performance win Lu has shipped to production?", "en"],
    ["How did Lu build an LLM agent reliable enough for a real bank?", "en"],
    ["How has Lu's work spanned both e-commerce and financial AI?", "en"],
    ["汪露最擅长哪些技术方向？", "zh"],
    ["汪露交付过最大的性能优化是什么？", "zh"],
    ["汪露是怎么让 LLM Agent 在银行生产环境可靠运行的？", "zh"],
    ["汪露的经验是怎么覆盖电商和金融两个领域的？", "zh"],
  ];
  allQuestions.push(
    ["How does Lu match Senior AI Agent Engineer job requirements?", "en"],
    ["这个简历网站本身如何体现 AI Agent 工程能力？", "zh"],
  );
  allQuestions.forEach(([message, language]) => {
    const key = `${language}|${message}`;
    if (warmupCache[key]) markSuggestionReady(message, language);
  });

  // Fallback: only fetch current language questions that aren't cached yet
  try { await fetch(`${API}/health`); } catch {}
  const missing = allQuestions.filter(([message, language]) => {
    return language === lang && !warmupCache[`${language}|${message}`];
  });
  await Promise.allSettled(missing.map(async ([message, language]) => {
    const key = `${language}|${message}`;
    const res = await fetch(`${API}/api/chat`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ message, language, session_id: sessionId }),
    });
    if (!res.ok) return;
    warmupCache[key] = await res.json();
    markSuggestionReady(message, language);
  }));
}

function markSuggestionReady(question, language) {
  if (language !== lang) return;
  $$(".pill-q").forEach((btn) => {
    const value = language === "zh" ? btn.dataset.qZh : btn.dataset.qEn;
    if (value === question) btn.classList.add("warmed");
  });
}

function init() {
  $("#year").textContent = new Date().getFullYear();
  if (window.innerWidth <= 800) closeTerminal();
  else document.body.classList.add("terminal-open");
  $("[data-lang-toggle]")?.addEventListener("click", () => {
    lang = lang === "zh" ? "en" : "zh";
    applyLang();
  });
  bindBackground();
  bindCommandConsole();
  bindFab();
  bindMetricObserver();
  bindAgent();
  applyLang();
  loadMarketSignals();
  loadCapabilities();
  loadProjects();
  warmup();
}

init();
