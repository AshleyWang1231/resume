const API = "https://resume-gent-api-vtugquposb.cn-hangzhou.fcapp.run";
const STREAM_TIMEOUT_MS = 4000;

const T = {
  en: {
    eyebrow: "AI Software Engineer",
    navCapabilities: "Capabilities",
    navAgent: "Agent",
    navProjects: "Projects",
    navSystem: "System",
    downloadResume: "PDF",
    heroKicker: "AI Software Engineer · Zalando",
    heroTitle: "I build LLM agents that make product decisions easier.",
    heroLead: "Focused on Agent Runtime, Tool Calling, Streaming UX, personalization, and Text2SQL systems that can be measured, tested, and shipped.",
    heroAsk: "Ask the resume agent",
    heroWork: "View selected work",
    consoleLine1: "Profile loaded: Agent Runtime, Streaming, Tool Calling, Personalization, Text2SQL.",
    consoleLine2: "Ready. Ask naturally, or use commands like /projects.",
    commandPlaceholder: "Ask about Streaming, or type /projects",
    capKicker: "Core capabilities",
    capTitle: "AI engineering, kept close to product outcomes.",
    cap1: "Tool orchestration, state handling, and grounded responses for shopping and enterprise workflows.",
    cap2: "Typed event streams that separate process state, business actions, and final user-facing text.",
    cap3: "Context-aware recommendations driven by user profile, history, conversation context, and product signals.",
    cap4: "Scenario replay, latency baselines, SQL validation, and regression checks before prompt or workflow changes.",
    agentKicker: "Resume agent",
    agentTitle: "One terminal for navigation, questions, and evidence.",
    agentProof1Title: "Live backend",
    agentProof1: "The hero terminal calls the Resume Agent API and falls back gracefully when streaming is unavailable.",
    agentProof2Title: "Evidence first",
    agentProof2: "Answers cite project evidence instead of repeating generic profile copy.",
    agentSuggestionsTitle: "Useful prompts",
    agentQ1: "What AI Agent systems has Lu built?",
    agentQ2: "Show Streaming and Tool Calling experience.",
    agentQ3: "What measurable impact?",
    agentQ4: "Explain Text2SQL experience.",
    agentThinking: "Calling tools...",
    agentError: "The resume agent is temporarily unavailable. Please try again later.",
    impactKicker: "Selected metrics",
    impactTitle: "Measured improvements across latency, engagement, and reliability.",
    metric1: "average TTFT reduction in Suggestions API benchmark",
    metric2: "first-screen cold-start reduction via Warm-Up",
    metric3: "profile-service calls after cache layer",
    metric4: "product-comparison engagement lift",
    projectsKicker: "Selected AI work",
    projectsTitle: "Project cases with concrete outcomes.",
    systemKicker: "This site's backend",
    systemTitle: "A small agent stack behind the portfolio.",
    archLoading: "Loading architecture...",
    skillsKicker: "Stack",
    skillsTitle: "Tools I use to ship AI systems.",
    skillAi: "AI / LLM",
    skillBackend: "Backend",
    skillRetrieval: "Retrieval",
    contactKicker: "Contact",
    contactTitle: "Available for AI software engineering roles.",
    phone: "+86 13122038365",
    cmdUnknown: "Unknown command. Try /capabilities, /agent, /projects, /system, or /ask ...",
    cmdScrolled: "Navigated to",
    cmdAsking: "Forwarding question to Resume Agent",
    pillsCommands: "Commands",
    pillsQuestions: "Questions",
  },
  zh: {
    eyebrow: "AI 软件工程师",
    navCapabilities: "核心能力",
    navAgent: "简历 Agent",
    navProjects: "项目",
    navSystem: "系统",
    downloadResume: "简历 PDF",
    heroKicker: "AI 软件工程师 · Zalando",
    heroTitle: "我构建能辅助真实业务决策的 LLM Agent。",
    heroLead: "专注 Agent Runtime、Tool Calling、Streaming 体验、个性化推荐和 Text2SQL 系统，强调可度量、可测试、可上线。",
    heroAsk: "询问简历 Agent",
    heroWork: "查看项目",
    consoleLine1: "Profile loaded: Agent Runtime, Streaming, Tool Calling, Personalization, Text2SQL.",
    consoleLine2: "Ready. 可以直接提问，也可以使用 /projects 这类命令。",
    commandPlaceholder: "询问 Streaming，或输入 /projects",
    capKicker: "核心能力",
    capTitle: "围绕产品结果构建 AI 工程能力。",
    cap1: "为导购和企业工作流设计工具编排、状态处理和基于证据的回答链路。",
    cap2: "用类型化事件流拆分过程状态、业务动作和最终用户可见文本。",
    cap3: "基于用户画像、历史行为、对话上下文和商品信号生成个性化推荐。",
    cap4: "在修改 Prompt 或工作流前建立场景回放、延迟基线、SQL 校验和回归检查。",
    agentKicker: "简历 Agent",
    agentTitle: "一个终端完成导航、提问和证据展示。",
    agentProof1Title: "真实后端",
    agentProof1: "首屏 terminal 会调用 Resume Agent API；当流式接口不可用时自动降级。",
    agentProof2Title: "证据优先",
    agentProof2: "回答引用项目证据，而不是重复泛泛的个人简介。",
    agentSuggestionsTitle: "可以这样问",
    agentQ1: "汪露做过哪些 AI Agent 系统？",
    agentQ2: "展示 Streaming 和 Tool Calling 经验。",
    agentQ3: "有哪些可量化结果？",
    agentQ4: "介绍 Text2SQL 项目经验。",
    agentThinking: "正在调用工具...",
    agentError: "简历 Agent 暂时不可用，请稍后再试。",
    impactKicker: "关键指标",
    impactTitle: "围绕延迟、互动率和稳定性的可量化改进。",
    metric1: "Suggestions API 基准测试平均 TTFT 降低",
    metric2: "Warm-Up 架构降低首屏冷启动",
    metric3: "缓存层减少画像服务调用",
    metric4: "商品对比场景互动率提升",
    projectsKicker: "AI 项目",
    projectsTitle: "有明确结果支撑的项目案例。",
    systemKicker: "本站后端",
    systemTitle: "支撑这个作品集的小型 Agent 系统。",
    archLoading: "加载架构图...",
    skillsKicker: "技术栈",
    skillsTitle: "用于交付 AI 系统的工具。",
    skillAi: "AI / LLM",
    skillBackend: "后端",
    skillRetrieval: "检索",
    contactKicker: "联系",
    contactTitle: "正在寻找 AI 软件工程相关机会。",
    phone: "13122038365（微信同号）",
    cmdUnknown: "未知命令。可以试试 /capabilities、/agent、/projects、/system 或 /ask ...",
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

async function loadProjects() {
  try {
    const res = await fetch(`${API}/api/projects`);
    if (!res.ok) throw new Error("projects failed");
    cachedProjects = await res.json();
    renderProjects(cachedProjects);
  } catch {
    const grid = $("[data-projects-grid]");
    if (grid) grid.innerHTML = `<p class="console-muted">${escapeHtml(t("agentError"))}</p>`;
  }
}

function renderProjects(projects) {
  if (!projects) return;
  const grid = $("[data-projects-grid]");
  if (!grid) return;
  grid.innerHTML = projects.map((project) => `
    <article class="project-card ${project.highlight ? "highlight" : ""}">
      <div class="project-header">
        <div>
          <div class="project-company">${escapeHtml(project.company)}</div>
          <h3>${escapeHtml(project.title)}</h3>
        </div>
        <div class="project-period">${escapeHtml(project.period)}</div>
      </div>
      <p>${escapeHtml(lang === "zh" ? project.summary_zh : project.summary_en)}</p>
      <div class="impact-chips">${project.impact.map((item) => `<span>${escapeHtml(item)}</span>`).join("")}</div>
      <div class="skill-chips">${project.skills.map((item) => `<span>${escapeHtml(item)}</span>`).join("")}</div>
    </article>
  `).join("");
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
      <p>${escapeHtml(item.summary)}</p>
      <div class="ev-chips">
        ${[...(item.evidence || []), ...(item.skills || []).slice(0, 3)].map((chip) => `<span>${escapeHtml(chip)}</span>`).join("")}
      </div>`;
    list.append(card);
  });
  parent.append(list);
  const feed = $("[data-command-feed]");
  if (feed) feed.scrollTop = feed.scrollHeight;
}

function revealText(el, text, done) {
  let index = 0;
  function frame() {
    if (index >= text.length) {
      done?.();
      return;
    }
    el.textContent += text.slice(index, index + 16);
    index += 16;
    const feed = $("[data-command-feed]");
    if (feed) feed.scrollTop = feed.scrollHeight;
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}

async function sendMessage(message) {
  if (!message) return;
  addTerminalMessage("user", message);

  const cacheKey = `${lang}|${message}`;
  if (warmupCache[cacheKey]) {
    const data = warmupCache[cacheKey];
    if (data.session_id && !sessionId) sessionId = data.session_id;
    const answer = addTerminalMessage("assistant", "");
    revealText(answer.querySelector("p"), data.answer, () => addEvidence(answer, data.evidence));
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
          textEl.textContent += payload.text || "";
          const feed = $("[data-command-feed]");
          if (feed) feed.scrollTop = feed.scrollHeight;
        }
        if (event === "evidence") {
          toolMessages.forEach((msg) => msg.remove());
          addEvidence(answer, payload);
        }
        if (event === "done" && payload.session_id) sessionId = payload.session_id;
        if (event === "error") textEl.textContent = payload.message || t("agentError");
      }
    }
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
      const answer = addTerminalMessage("assistant", data.answer);
      addEvidence(answer, data.evidence);
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
    ["What AI Agent systems has Lu built?", "en"],
    ["Show Lu's Streaming and Tool Calling experience.", "en"],
    ["What measurable impact does Lu have?", "en"],
    ["Explain Lu's Text2SQL experience.", "en"],
    ["汪露做过哪些 AI Agent 系统？", "zh"],
    ["展示 Streaming 和 Tool Calling 经验。", "zh"],
    ["有哪些可量化结果？", "zh"],
    ["介绍 Text2SQL 项目经验。", "zh"],
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
  loadArchitecture();
  setTimeout(warmup, 900);
}

init();
