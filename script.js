const API = "https://resume-gent-api-vtugquposb.cn-hangzhou.fcapp.run";
const STREAM_TIMEOUT_MS = 15000;
const TERMINAL_RENDER_DELAY_MS = 35;
const TERMINAL_RENDER_CHARS = 5;

const T = {
  en: {
    eyebrow: "AI Software Engineer",
    navCapabilities: "Capabilities",
    navProjects: "Projects",
    navSystem: "System",
    downloadResume: "PDF",
    heroKicker: "AI Software Engineer",
    heroTitle: "I ship AI Agent systems from design to production.",
    heroLead: "Focused on building production-grade LLM applications and AI Agent systems. Experienced in Python/Java backend development, Agent Workflows, Tool Calling, Streaming, personalization, product decision support, and Text2SQL. Led AI product capabilities across e-commerce and financial services — including personalized shopping assistance, real-time response optimization, and enterprise data analysis agents — with end-to-end experience from system design to production rollout.",
    heroAsk: "Ask the resume agent",
    heroWork: "View selected work",
    consoleLine1: "Profile loaded: Zalando · Thoughtworks · Agent Runtime · Streaming · Text2SQL",
    consoleLine2: "Ready. Ask naturally, or use commands like /projects.",
    commandPlaceholder: "Ask about Streaming, or type /projects",

    capKicker: "What I bring",
    capTitle: "Production AI engineering across the full stack.",
    cap1Title: "Agent Runtime & Tool Orchestration",
    cap1: "I design the runtime loop that makes agents reliable: tool dispatch with Pydantic-validated schemas, state-machine Streaming that separates process events from user-visible text, and multi-turn session management. Built at Zalando for a live shopping assistant handling real user traffic.",
    cap2Title: "Streaming UX & Real-Time Performance",
    cap2: "Typed SSE event streams that give users instant feedback: tool progress, intermediate states, and final text each arrive as distinct events. Reduced TTFT by ~25% on Zalando's Suggestions API. Solved FC-specific streaming termination bugs in production.",
    cap3Title: "Personalization & Recommendation Systems",
    cap3: "End-to-end personalization pipelines combining conversation context, user profiles, and behavioural signals. Designed async Warm-Up (Redis registry + in-memory fallback) to decouple LLM generation from request latency. Evaluation-driven iteration across 800+ real product scenarios.",
    cap4Title: "Text2SQL & Enterprise RAG",
    cap4: "Multi-stage agent workflows for structured data access: intent clarification → SQL generation → validation + retry → result summarisation. Dual-layer vector reranking (field + value) to reduce schema hallucination. Built 1,000+ case eval suites as regression baselines.",

    agentQ1: "How did Lu cut TTFT by 25% at Zalando?",
    agentQ2: "What's the Agent Runtime architecture Lu built?",
    agentQ3: "How does Lu prevent LLM output from being unreliable in production?",
    agentQ4: "What made Lu's Text2SQL agent accurate enough for a real bank?",
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
    evalTitle: "Three test layers, zero manual checking.",
    evalLayer1Title: "Retrieval quality",
    evalLayer1Desc: "19 gold-standard queries with expected doc IDs. BM25 + FAISS scores are measured at every change. Current: 100% hit rate, MRR 0.947.",
    evalLayer1Code: "test_retrieval_eval.py · Precision@3 / Recall@3 / MRR",
    evalLayer2Title: "Agent end-to-end",
    evalLayer2Desc: "4 full-pipeline cases. Each asserts the correct evidence card is retrieved AND the answer contains required keywords (project names, metrics). No LLM mocking — runs against the real agent.",
    evalLayer2Code: "test_agent_eval.py · evidence hit + keyword match",
    evalLayer3Title: "Component contracts",
    evalLayer3Desc: "Guard (32 cases): injection patterns, off-topic, length limits. Output sanitiser (13 cases): XML tags, markdown headers, bold, lists. Provider factory and Pydantic tool schemas.",
    evalLayer3Code: "test_guard.py · test_sanitise.py · 78 cases total",
    evalMetric1: "19/19",
    evalMetric1Label: "retrieval hit rate",
    evalMetric2: "0.947",
    evalMetric2Label: "MRR across 19 queries",
    evalMetric3: "78",
    evalMetric3Label: "automated test cases",

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
    eyebrow: "AI 软件工程师",
    navCapabilities: "核心能力",
    navProjects: "项目",
    navSystem: "系统",
    downloadResume: "简历 PDF",
    heroKicker: "AI 软件工程师",
    heroTitle: "从设计到上线，我构建生产级 AI Agent 系统。",
    heroLead: "专注于生产级 LLM 应用与 AI Agent 系统建设。擅长基于 Python/Java 构建高可用后端服务，在 Agent Workflow、Tool Calling、Streaming、个性化推荐、商品决策辅助及 Text2SQL 等方向具备丰富实践经验。主导电商与金融领域 AI 产品研发，负责个性化导购、实时响应优化、企业级数据分析 Agent 等核心能力建设，具备从系统设计到生产落地的完整经验。",
    heroAsk: "询问简历 Agent",
    heroWork: "查看项目",
    consoleLine1: "Profile loaded: Zalando · Thoughtworks · Agent Runtime · Streaming · Text2SQL",
    consoleLine2: "Ready. 可以直接提问，也可以使用 /projects 这类命令。",
    commandPlaceholder: "询问 Streaming 架构，或输入 /projects",

    capKicker: "我能带来什么",
    capTitle: "覆盖全链路的生产级 AI 工程能力。",
    cap1Title: "Agent Runtime 与工具编排",
    cap1: "设计让 Agent 可靠运行的 Runtime 循环：Pydantic 校验工具 Schema、状态机 Streaming（过程事件与用户可见文本分离）、多轮会话管理。在 Zalando 面向真实用户流量的购物助手上落地。",
    cap2Title: "Streaming 体验与实时性能",
    cap2: "类型化 SSE 事件流让用户即时获得反馈：工具进度、中间状态和最终文本各自独立到达。在 Zalando Suggestions API 上将 TTFT 降低约 25%。在生产环境解决了函数计算特有的 Streaming 终止问题。",
    cap3Title: "个性化与推荐系统",
    cap3: "融合对话上下文、用户画像和行为信号的端到端个性化链路。设计基于 Redis 注册表的异步 Warm-Up 架构，将 LLM 生成从请求关键路径解耦。基于 800+ 真实商品场景的评估驱动迭代。",
    cap4Title: "Text2SQL 与企业级 RAG",
    cap4: "面向结构化数据访问的多阶段 Agent 流水线：意图澄清 → SQL 生成 → 校验重试 → 结果总结。字段+值双层向量 Rerank 降低 schema 幻觉。构建 1,000+ 用例评估集作为回归基线。",

    agentQ1: "Zalando 的 TTFT 是怎么降了 25% 的？",
    agentQ2: "汪露设计的 Agent Runtime 架构是什么样的？",
    agentQ3: "汪露如何确保 LLM 输出在生产环境可靠？",
    agentQ4: "Text2SQL Agent 是怎么做到银行级准确率的？",
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
    evalTitle: "三层测试，零人工检查。",
    evalLayer1Title: "检索质量",
    evalLayer1Desc: "19 条 gold-standard 查询，每条预设期望文档 ID。每次变更后自动计算 BM25 + FAISS 评分。当前：命中率 100%，MRR 0.947。",
    evalLayer1Code: "test_retrieval_eval.py · Precision@3 / Recall@3 / MRR",
    evalLayer2Title: "Agent 端到端",
    evalLayer2Desc: "4 条完整链路用例，每条断言：正确的 evidence card 被检索到，且回答中包含必要关键词（项目名、指标数字）。不 mock LLM，直接跑真实 agent。",
    evalLayer2Code: "test_agent_eval.py · evidence 命中 + 关键词断言",
    evalLayer3Title: "组件契约",
    evalLayer3Desc: "Guard（32 条）：注入模式、偏题、长度限制。输出清洗（13 条）：XML 标签、Markdown 标题、加粗、列表。Provider factory 和 Pydantic 工具 Schema。",
    evalLayer3Code: "test_guard.py · test_sanitise.py · 共 78 条",
    evalMetric1: "19/19",
    evalMetric1Label: "检索命中率",
    evalMetric2: "0.947",
    evalMetric2Label: "19 条查询的 MRR",
    evalMetric3: "78",
    evalMetric3Label: "自动化测试用例",

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

let lang = localStorage.getItem("resume-lang") || "en";
let cachedProjects = null;
let cachedArch = null;
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
  text = text.replace(/^[\-\*]\s+/gm, "");                        // - list items
  text = text.replace(/^\d+\.\s+/gm, "");                         // 1. numbered lists
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
  $$("[data-i18n-placeholder]").forEach((el) => {
    const key = el.dataset.i18nPlaceholder;
    if (dictionary[key]) el.placeholder = dictionary[key];
  });
  const toggle = $("[data-lang-toggle]");
  if (toggle) toggle.textContent = lang === "zh" ? "EN" : "中文";
  localStorage.setItem("resume-lang", lang);
  renderProjects(cachedProjects);
  renderArchitecture(cachedArch);
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
    "/capabilities": "capabilities",
    "/projects": "projects",
    "/impact": "impact",
    "/system": "system",
    "/skills": "skills",
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

const PROJECTS_DATA = [{"id":"agent-runtime","title":"Agent Runtime & Streaming Architecture","company":"Zalando","period":"2025–2026","summary_en":"Redesigned the Zalando Assistant Agent Runtime — Streaming architecture, Tool Calling integration, OpenAI Responses API migration.","summary_zh":"重新设计 Zalando Assistant Agent Runtime，覆盖 Streaming 架构、Tool Calling 接入和 OpenAI Responses API 迁移。","star_s_en":"The assistant returned full responses only after all tool calls completed, giving users no visibility into agent progress and making interactions feel sluggish.","star_a_en":"Introduced a state-machine Streaming layer separating process states, business events, and user-visible text into typed SSE events. Integrated product-detail Tool Calling so answers are grounded in live catalogue data. Migrated the runtime from Chat Completions to OpenAI Responses API, unifying the Tool Calling + Streaming path.","star_r_en":"Average TTFT –25% (Suggestions API benchmark). P95 TTFT –25% in validated flows. Users see real-time tool progress instead of a blank wait.","star_s_zh":"助手需等所有工具调用完成后才整体输出，用户看不到任何进度，体验偏慢。","star_a_zh":"引入状态机 Streaming 层，将过程状态、业务事件和用户可见文本拆分为类型化 SSE 事件。接入商品详情 Tool Calling，让回答基于实时商品数据。将主链路从 Chat Completions 迁移至 OpenAI Responses API，统一 Tool Calling + Streaming 路径。","star_r_zh":"平均 TTFT 降低 25%（Suggestions API 基准测试），P95 TTFT 降低 25%，用户实时可见工具调用进度。","impact":["-25% avg TTFT","-25% P95 TTFT","Typed SSE events","OpenAI Responses API"],"skills":["Agent Runtime","Tool Calling","Streaming","State Machine","OpenAI Responses API"],"highlight":true},{"id":"personalization","title":"Personalization & Warm-Up Architecture","company":"Zalando","period":"2025–2026","summary_en":"Built personalization pipeline and async Warm-Up architecture for Zalando Assistant Conversation Starters.","summary_zh":"为 Zalando Assistant Conversation Starters 构建个性化链路和异步 Warm-Up 架构。","star_s_en":"Conversation Starters used static signals only, called the profile service on every request, and had noticeable cold-start latency under traffic spikes.","star_a_en":"(1) Rebuilt the input pipeline to fuse real-time conversation context, user profile, and behaviour history. (2) Added a TTL cache layer with field-level invalidation in front of the profile service. (3) Designed an async Warm-Up: a Redis registry tracks pending first-screen requests; a background worker pre-generates suggestions; in-memory fallback handles cache misses.","star_r_en":"Conversation Starter engagement +15%. Cold-start time –60%. Profile-service calls –70%; P99 latency –60% under high concurrency. Validated across 800+ real product-detail-page scenarios.","star_s_zh":"Conversation Starters 仅依赖静态信号，每次请求都调用画像服务，高峰期冷启动延迟明显。","star_a_zh":"(1) 重建输入链路，融合实时对话上下文、用户画像和历史行为。(2) 在画像服务前加 TTL 缓存层，支持字段级失效。(3) 设计异步 Warm-Up：Redis 注册表追踪待处理首屏请求，后台 Worker 提前生成建议，内存降级兜底。","star_r_zh":"推荐入口互动率 +15%，冷启动时间 -60%，画像服务调用量 -70%，高并发下 P99 延迟 -60%。基于 800+ 真实商品页面场景验证。","impact":["+15% engagement","-60% cold-start","-70% profile calls","-60% P99 latency"],"skills":["Personalization","Redis","Async Warm-Up","Caching","Eval-Driven"],"highlight":true},{"id":"product-comparison","title":"Product Comparison Skill","company":"Zalando","period":"2025–2026","summary_en":"Designed and shipped a multi-turn product comparison capability for Zalando Assistant.","summary_zh":"为 Zalando Assistant 设计并上线多轮商品对比能力。","star_s_en":"Users asked to compare browsed products, but free-form LLM output was unreliable: table layouts broke, discount fields went missing, and multi-turn references (\"compare the first two\") were frequently misresolved.","star_a_en":"Split responsibilities: the model handles intent, conversation-state tracking, and summary copy; deterministic code owns product-reference resolution, field selection, discount calculation, and layout rendering. This gave the frontend a stable contract independent of model version.","star_r_en":"Comparison-scenario engagement +20%. Eliminated LLM formatting instability; frontend rendering is stable across model updates.","star_s_zh":"用户要求对比已浏览商品，但 LLM 直接输出格式不稳定：布局错乱、折扣字段缺失，多轮引用频繁解析错误。","star_a_zh":"责任拆分：模型负责意图理解、对话状态追踪和总结文案；确定性代码负责商品引用解析、字段选择、折扣计算和布局渲染，向前端提供与模型版本无关的稳定契约。","star_r_zh":"对比场景互动率 +20%，消除 LLM 格式不稳定问题，前端渲染跨模型版本保持稳定。","impact":["+20% engagement","Stable rendering","Multi-turn references","Model/code split"],"skills":["Structured Output","Tool Calling","Multi-turn","Deterministic Rendering"],"highlight":true},{"id":"text2sql","title":"Text2SQL AI Agent — Enterprise Data Analysis","company":"Thoughtworks · Major Domestic Bank","period":"2021–2025","summary_en":"Built an enterprise data-analysis Agent for a major domestic bank, enabling natural-language querying of complex structured data.","summary_zh":"为国内知名银行构建企业数据分析 Agent，支持复杂结构化数据的自然语言查询。","star_s_en":"Non-technical pricing analysts needed self-service access to complex structured data. Naive LLM prompts failed on nested conditions and ambiguous schema fields, bad SQL could corrupt pricing decisions, and there was no evaluation baseline.","star_a_en":"Designed a multi-stage agent pipeline: intent clarification → SQL generation → automated SQL validation → exception retry → result summarisation with visualisations. Built dual-layer vector reranking (field + value) to reduce schema hallucination. Created a 1,000+ case evaluation suite from real business queries as a regression baseline for all prompt changes.","star_r_en":"End-to-end query accuracy +20%. SQL validation + retry loop eliminated silent failures. 1,000+ eval cases became the team's standard regression baseline.","star_s_zh":"非技术定价分析师需自助查询复杂结构化数据，但直接 prompt LLM 在嵌套条件和歧义字段上错误率高，且缺乏评估基线。","star_a_zh":"设计多阶段 Agent 流水线：意图澄清 → SQL 生成 → 自动 SQL 校验 → 异常重试 → 结果总结与可视化。构建字段+值双层向量 Rerank 减少 schema 幻觉。从真实业务查询积累 1,000+ 条评估用例作为回归基线。","star_r_zh":"端到端查询准确率 +20%，SQL 校验+重试消除静默失败，1,000+ 评估用例成为团队标准回归基线。","impact":["+20% accuracy","1,000+ eval cases","Dual-layer rerank","Auto SQL validation"],"skills":["Text2SQL","Multi-stage Agent","FAISS","Reranking","SQL Validation","Evaluation"],"highlight":false},{"id":"pricing-management","title":"Pricing Management System — Access Control & Data Pipeline","company":"Thoughtworks · Major Domestic Bank","period":"2021–2025","summary_en":"Backend module owner for a bank-wide interest-rate product pricing platform — access control, reporting, and database migration.","summary_zh":"负责国内知名银行利率类金融产品定价管理系统的权限模块、报表模块及数据库迁移等核心工作。","star_s_en":"The pricing platform needed fine-grained access control across complex role hierarchies and multiple business lines, high-performance in-memory multi-dimensional aggregation for reporting, and a MySQL architecture struggling under millions of daily pricing transactions.","star_a_en":"(1) Led access control module design and implementation using Hexagonal Architecture and DDD — modelled complex role hierarchies and fine-grained permissions as a reusable domain layer adopted across multiple sub-systems. (2) Designed a custom in-memory data processing pipeline (Tablesaw + custom toolchain) for the reporting module to replace external dependencies. (3) Spearheaded the database migration strategy, delivering a zero-downtime production switchover for large-scale business tables.","star_r_en":"Reporting module dev efficiency +40%; delivery cycle shortened by 2+ weeks. Database migration achieved zero business impact, sustaining stable operation under millions of daily pricing requests. Access control module reused across multiple sub-systems.","star_s_zh":"定价平台需跨多业务线支持复杂角色层级与细粒度权限管理；报表模块需内存中多维聚合与计算；原 MySQL 架构在海量业务数据下存在性能瓶颈。","star_a_zh":"(1) 基于六边形架构与 DDD 主导权限模块设计与落地，构建可复用领域模型，在多个子系统中复用。(2) 针对报表模块自研内存数据加工方案（Tablesaw + 自定义工具链），替代外部依赖。(3) 主导数据库迁移方案设计与实施，完成生产环境平滑切换。","star_r_zh":"报表模块开发效率提升约 40%，开发工期缩短 2 周以上。数据库迁移实现 0 业务感知，系统在每日数百万笔定价请求下稳定运行。权限模块在多个子系统中复用。","impact":["+40% dev efficiency","–2 weeks cycle","0-downtime DB migration","Multi-system reuse"],"skills":["Spring Cloud","Hexagonal Architecture","Tablesaw","MySQL","Redis","RabbitMQ"],"highlight":false},{"id":"rag-chatbot","title":"RAG Knowledge Q&A System","company":"Thoughtworks","period":"2021–2025","summary_en":"Built a production RAG pipeline for enterprise policy Q&A alongside the Text2SQL agent.","summary_zh":"与 Text2SQL Agent 并行，构建企业政策问答生产级 RAG 流水线。","star_s_en":"The bank needed a reliable Q&A system over internal policy documents, with no existing retrieval infrastructure or quality measurement.","star_a_en":"Built a full RAG pipeline with LlamaIndex and FAISS — chunking strategy, embedding, vector retrieval, and answer generation. Introduced RAGAS evaluation (faithfulness, relevance, context coverage) as the quality gate, creating a reusable eval harness the team adopted for all subsequent RAG work.","star_r_en":"RAGAS faithfulness 0.82 / context recall 0.78 on internal policy Q&A benchmark. Eval harness adopted by 3 downstream RAG projects; reusable pipeline template cut average onboarding ~40%.","star_s_zh":"银行需要基于内部政策文档的可靠问答系统，无现有检索基础设施，也没有质量度量方式。","star_a_zh":"基于 LlamaIndex + FAISS 构建完整 RAG 流水线——切片策略、Embedding、向量检索和答案生成。引入 RAGAS（忠实性、相关性、上下文覆盖率）作为质量门控，形成团队后续 RAG 工作的可复用评估框架。","star_r_zh":"RAGAS 忠实性评分 0.82，上下文召回率 0.78。评估框架被 3 个后续 RAG 项目复用，可复用流水线模板将平均上线周期缩短约 40%。","impact":["Faithfulness 0.82","Context recall 0.78","-40% onboarding","3 projects adopted"],"skills":["RAG","LlamaIndex","FAISS","Embedding","RAGAS"],"highlight":false}];

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
  const item = evidence[0];
  const list = document.createElement("div");
  list.className = "evidence-list";
  const card = document.createElement("div");
  card.className = "evidence-card";
  card.innerHTML = `
    <strong>${escapeHtml(item.title)}</strong>
    <span class="ev-company">${escapeHtml(item.company)}</span>
    <div class="ev-chips">
      ${(item.evidence || []).slice(0, 4).map((chip) => `<span>${escapeHtml(chip)}</span>`).join("")}
    </div>`;
  list.append(card);
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
          // Sanitise the fully-streamed text before closing (replaces any leaked tags/markdown)
          textEl.textContent = sanitiseAnswer(textEl.textContent);
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
      revealText(answer.querySelector("p"), data.answer, () => addEvidence(answer, data.evidence));
    } catch {
      addTerminalMessage("assistant", t("agentError"));
    }
  }
}

function bindAgent() {
  // suggestion-btn clicks handled via data-run-command in bindCommandConsole
}

async function warmup() {
  try { await fetch(`${API}/health`); } catch {}
  const questions = [
    ["How did Lu cut TTFT by 25% at Zalando?", "en"],
    ["What's the Agent Runtime architecture Lu built?", "en"],
    ["How does Lu prevent LLM output from being unreliable in production?", "en"],
    ["What made Lu's Text2SQL agent accurate enough for a real bank?", "en"],
    ["Zalando 的 TTFT 是怎么降了 25% 的？", "zh"],
    ["汪露设计的 Agent Runtime 架构是什么样的？", "zh"],
    ["汪露如何确保 LLM 输出在生产环境可靠？", "zh"],
    ["Text2SQL Agent 是怎么做到银行级准确率的？", "zh"],
  ];
  await Promise.allSettled(questions.map(async ([message, language]) => {
    const key = `${language}|${message}`;
    if (warmupCache[key]) return;
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
  loadProjects();
  warmup();
}

init();
