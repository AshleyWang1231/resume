const API = "https://resume-gent-api-vtugquposb.cn-hangzhou.fcapp.run";
const VISITOR_BOARD_API = ""; // Set to the AWS Lambda Function URL before deploying to S3.
const STREAM_TIMEOUT_MS = 30000;
const TERMINAL_RENDER_DELAY_MS = 35;
const TERMINAL_RENDER_CHARS = 5;

const T = {
  en: {
    eyebrow: "AI Software Engineer",
    navCapabilities: "Capabilities",
    navVisitorBoard: "Visitor Board",
    navSystem: "System",
    downloadResume: "PDF",
    heroKicker: "AI Software Engineer",
    heroTitle: "I ship AI Agent systems from design to production.",
    heroLead: "Focused on building production-grade LLM applications and AI Agent systems. Experienced in Python/Java backend development, Agent Workflows, Tool Calling, Streaming, personalization, product decision support, and Text2SQL. Led AI product capabilities across e-commerce and financial services — including personalized shopping assistance, real-time response optimization, and enterprise data analysis agents — with end-to-end experience from system design to production rollout.",
    heroAsk: "Ask the resume agent",
    heroWork: "Leave a public note",
    consoleLine1: "Profile loaded: Zalando · Thoughtworks · Agent Runtime · Streaming · Text2SQL",
    consoleLine2: "Ready. Ask naturally, or use commands like /projects.",
    commandPlaceholder: "Ask about Streaming, or type /projects",

    capKicker: "What I bring",
    capTitle: "Production AI engineering across the full stack.",
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
    visitorKicker: "Visitor Board",
    visitorTitle: "Ask me about my experience",
    visitorLead: "Leave a public note or question. Messages are stored in DynamoDB and shown below.",
    visitorPrivacy: "Messages are public. Please do not submit private contact information.",
    visitorNamePlaceholder: "Your name or organization",
    visitorMessagePlaceholder: "Your question or note",
    visitorSubmit: "Submit public note",
    visitorApiMissing: "Visitor Board API is not configured yet.",
    visitorEmpty: "No public notes yet.",
    visitorLoading: "Loading public notes…",
    visitorLoadError: "Could not load public notes. Please try again later.",
    visitorSubmitting: "Submitting public note…",
    visitorRequired: "Name and message are required.",
    visitorSubmitted: "Public note submitted.",
    visitorSubmitError: "Could not submit public note. Please try again later.",
  },
  zh: {
    eyebrow: "AI 软件工程师",
    navCapabilities: "核心能力",
    navVisitorBoard: "访客留言板",
    navSystem: "系统",
    downloadResume: "简历 PDF",
    heroKicker: "AI 软件工程师",
    heroTitle: "从设计到上线，我构建生产级 AI Agent 系统。",
    heroLead: "专注于生产级 LLM 应用与 AI Agent 系统建设。擅长基于 Python/Java 构建高可用后端服务，在 Agent Workflow、Tool Calling、Streaming、个性化推荐、商品决策辅助及 Text2SQL 等方向具备丰富实践经验。主导电商与金融领域 AI 产品研发，负责个性化导购、实时响应优化、企业级数据分析 Agent 等核心能力建设，具备从系统设计到生产落地的完整经验。",
    heroAsk: "询问简历 Agent",
    heroWork: "留下公开留言",
    consoleLine1: "Profile loaded: Zalando · Thoughtworks · Agent Runtime · Streaming · Text2SQL",
    consoleLine2: "Ready. 可以直接提问，也可以使用 /projects 这类命令。",
    commandPlaceholder: "询问 Streaming 架构，或输入 /projects",

    capKicker: "我能带来什么",
    capTitle: "覆盖全链路的生产级 AI 工程能力。",
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
    visitorKicker: "访客留言板",
    visitorTitle: "想了解我的经历？",
    visitorLead: "留下公开问题或留言。内容会存储在 DynamoDB 中，并显示在下方。",
    visitorPrivacy: "留言是公开的，请不要提交私人联系方式。",
    visitorNamePlaceholder: "你的姓名或机构",
    visitorMessagePlaceholder: "你的问题或留言",
    visitorSubmit: "提交公开留言",
    visitorApiMissing: "访客留言板 API 尚未配置。",
    visitorEmpty: "还没有公开留言。",
    visitorLoading: "正在加载公开留言…",
    visitorLoadError: "暂时无法加载公开留言，请稍后再试。",
    visitorSubmitting: "正在提交公开留言…",
    visitorRequired: "姓名和留言内容均为必填。",
    visitorSubmitted: "公开留言已提交。",
    visitorSubmitError: "暂时无法提交公开留言，请稍后再试。",
  },
};

let lang = localStorage.getItem("resume-lang") || "en";
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
    "/visitor-board": "visitor-board",
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

function visitorBoardUrl(path) {
  return `${VISITOR_BOARD_API.replace(/\/$/, "")}${path}`;
}

function setVisitorStatus(message = "", type = "") {
  const status = $("#visitor-status");
  if (!status) return;
  status.textContent = message;
  status.dataset.status = type;
}

function renderVisitorMessages(items = []) {
  const container = $("#visitor-messages");
  if (!container) return;
  container.replaceChildren();

  if (!VISITOR_BOARD_API) {
    const empty = document.createElement("p");
    empty.className = "visitor-empty";
    empty.textContent = t("visitorApiMissing");
    container.append(empty);
    return;
  }

  if (!items.length) {
    const empty = document.createElement("p");
    empty.className = "visitor-empty";
    empty.textContent = t("visitorEmpty");
    container.append(empty);
    return;
  }

  items.forEach((item) => {
    const article = document.createElement("article");
    article.className = "visitor-message-card";

    const header = document.createElement("div");
    header.className = "visitor-message-head";

    const name = document.createElement("strong");
    name.textContent = item.name || "Visitor";

    const time = document.createElement("time");
    time.dateTime = item.createdAt || "";
    time.textContent = item.createdAt ? new Date(item.createdAt).toLocaleString() : "Just now";

    const message = document.createElement("p");
    message.textContent = item.message || "";

    header.append(name, time);
    article.append(header, message);
    container.append(article);
  });
}

async function loadVisitorMessages({ quiet = false } = {}) {
  const container = $("#visitor-messages");
  if (!container) return;
  if (!VISITOR_BOARD_API) {
    renderVisitorMessages([]);
    return;
  }

  if (!quiet) setVisitorStatus(t("visitorLoading"), "loading");
  try {
    const res = await fetch(visitorBoardUrl("/messages"));
    if (!res.ok) throw new Error("Failed to load visitor messages");
    const data = await res.json();
    renderVisitorMessages(Array.isArray(data.items) ? data.items : []);
    if (!quiet) setVisitorStatus("", "");
  } catch {
    setVisitorStatus(t("visitorLoadError"), "error");
  }
}

async function submitVisitorMessage(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const button = $("#visitor-submit-button");
  const nameInput = $("#visitor-name");
  const messageInput = $("#visitor-message");
  const name = nameInput?.value.trim() || "";
  const message = messageInput?.value.trim() || "";

  if (!VISITOR_BOARD_API) {
    setVisitorStatus(t("visitorApiMissing"), "error");
    return;
  }
  if (!name || !message) {
    setVisitorStatus(t("visitorRequired"), "error");
    return;
  }

  if (button) button.disabled = true;
  setVisitorStatus(t("visitorSubmitting"), "loading");
  try {
    const res = await fetch(visitorBoardUrl("/messages"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, message }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.error || "Failed to submit visitor message");
    form.reset();
    await loadVisitorMessages({ quiet: true });
    setVisitorStatus(t("visitorSubmitted"), "success");
  } catch (error) {
    setVisitorStatus(error.message || t("visitorSubmitError"), "error");
  } finally {
    if (button) button.disabled = false;
  }
}

function bindVisitorBoard() {
  $("#visitor-message-form")?.addEventListener("submit", submitVisitorMessage);
  loadVisitorMessages();
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
  bindAgent();
  bindVisitorBoard();
  applyLang();
  warmup();
}

init();
