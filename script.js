const API = "https://resume-gent-api-vtugquposb.cn-hangzhou.fcapp.run";

// ── i18n ─────────────────────────────────────────────────
const T = {
  en: {
    eyebrow: "Senior AI Engineer", heroLabel: "AI Software Engineer · Zalando",
    heroName: "Lu Wang",
    heroLead: "Builds LLM applications that ship to millions of users. Specialises in Agent Runtime, Tool Calling, Streaming, and evaluation-driven delivery.",
    phone: "+86 13122038365", downloadResume: "PDF",
    badge1: "4+ yrs AI engineering", badge2: "Zalando · Thoughtworks", badge3: "Cardiff MSc Computing",
    navAgent: "Resume Agent", navImpact: "Impact", navProjects: "Projects",
    navArchitecture: "Architecture", navSkills: "Skills",
    impactLabel: "Delivered outcomes", impactTitle: "Impact at scale",
    metric1: "TTFT reduction — Agent Runtime latency improvement (avg + P95)",
    metric2: "Engagement lift — Personalized Conversation Starters",
    metric3: "Cold-start reduction via async Warm-Up cache",
    metric4: "SQL accuracy — Text2SQL Agent at leading domestic bank",
    metric5: "Evaluation cases built for Text2SQL regression testing",
    metric6: "Personalization scenarios covered end-to-end",
    agentLabel: "Live demo · powered by this repo's backend",
    agentTitle: "Ask my resume", agentStatusLive: "DeepSeek · Aliyun FC",
    agentPlaceholder: "Ask about Lu's AI engineering experience…",
    agentSend: "Ask", agentSuggestionsTitle: "Try asking",
    agentIntro: "Ask anything about Lu's AI engineering experience — Agent systems, Streaming, personalization, Text2SQL, or measurable outcomes. I'll cite evidence from the resume.",
    agentQ1: "What AI Agent systems has Lu built?",
    agentQ2: "Show Streaming and Tool Calling experience.",
    agentQ3: "What measurable impact?",
    agentQ4: "Explain Text2SQL experience.",
    agentThinking: "Calling tools…",
    agentError: "The resume agent is temporarily unavailable. Please try again later.",
    agentArchLabel: "How this agent works",
    agentInfo1: "Multi-turn session memory",
    agentInfo2: "Tool calling: search, detail, capabilities",
    agentInfo3: "SSE streaming with typed events",
    agentInfo4: "Pydantic-validated tool schemas",
    agentInfo5: "Evidence cards from resume data",
    projectsLabel: "Selected work", projectsTitle: "AI Projects",
    archLabel: "This site's own backend", archTitle: "System architecture",
    archLoading: "Loading architecture…",
    methodLabel: "How I build LLM applications", methodTitle: "Engineering principles",
    p1Title: "Separate reasoning from execution",
    p1Desc: "Model handles understanding and generation. Validation, routing, rendering, and safety controls stay deterministic.",
    p2Title: "Measure before tuning",
    p2Desc: "Latency benchmarks, eval sets, scenario replay, and regression checks before changing any prompt or workflow.",
    p3Title: "Design for failure paths",
    p3Desc: "Missing context, tool timeouts, empty values, service errors, and fallback behavior are first-class product flows.",
    p4Title: "Make output easy to consume",
    p4Desc: "Structured contracts, stable schemas, and frontend-friendly events over free-form output where reliability matters.",
    expLabel: "Career", expTitle: "Work Experience",
    zalandoRole: "AI Software Engineer",
    zalandoDesc: "Building customer-facing AI Agent capabilities: personalized shopping assistance, product decision support, real-time Streaming, and runtime reliability at scale.",
    twRole: "AI Software Engineer",
    twDesc: "Delivered AI and backend systems for enterprise clients: Text2SQL Agents, RAG Q&A, pricing platforms, and after-sales management.",
    present: "Present",
    skillsLabel: "Capabilities", skillsTitle: "Skills",
    skillAi: "AI / LLM Engineering", skillRetrieval: "Retrieval & Vectors",
    skillBackend: "Backend & Infrastructure", skillDeploy: "Deploy & Observability",
    eduLabel: "Education", eduTitle: "Degrees",
    cardiffDegree: "MSc in Computing", suesDegree: "BA in Marketing",
    footerStack: "Frontend: GitHub Pages · Backend: Aliyun FC · AI: DeepSeek",
  },
  zh: {
    eyebrow: "AI 软件工程师", heroLabel: "AI 软件工程师 · Zalando",
    heroName: "汪露",
    heroLead: "负责面向数百万用户的 LLM 应用建设，专注 Agent Runtime、Tool Calling、Streaming 和评估驱动的交付。",
    phone: "13122038365（微信同号）", downloadResume: "简历 PDF",
    badge1: "4 年以上 AI 工程经验", badge2: "Zalando · Thoughtworks", badge3: "英国卡迪夫大学 硕士",
    navAgent: "简历 Agent", navImpact: "量化成果", navProjects: "AI 项目",
    navArchitecture: "系统架构", navSkills: "技能",
    impactLabel: "可量化交付成果", impactTitle: "规模化影响",
    metric1: "TTFT 降低 — Agent Runtime 延迟优化（平均 + P95）",
    metric2: "互动率提升 — 个性化 Conversation Starters",
    metric3: "冷启动降低 — 异步 Warm-Up 缓存",
    metric4: "SQL 准确率提升 — Text2SQL Agent（国内知名银行）",
    metric5: "Text2SQL 回归测试评估用例",
    metric6: "个性化场景端到端覆盖",
    agentLabel: "实时演示 · 由本仓库后端驱动",
    agentTitle: "直接问我的简历", agentStatusLive: "DeepSeek · 阿里云 FC",
    agentPlaceholder: "输入你想了解的 AI 工程经历…",
    agentSend: "提问", agentSuggestionsTitle: "可以这样问",
    agentIntro: "可以询问汪露的 AI Agent 系统、Streaming、个性化、Text2SQL 或可量化成果，我会引用简历中的证据。",
    agentQ1: "汪露做过哪些 AI Agent 系统？",
    agentQ2: "展示 Streaming 和 Tool Calling 经验。",
    agentQ3: "有哪些可量化结果？",
    agentQ4: "介绍 Text2SQL 项目经验。",
    agentThinking: "正在调用工具…",
    agentError: "简历 Agent 暂时不可用，请稍后再试。",
    agentArchLabel: "Agent 工作原理",
    agentInfo1: "多轮对话会话记忆",
    agentInfo2: "工具调用：搜索、详情、能力列表",
    agentInfo3: "类型化 SSE 流式响应",
    agentInfo4: "Pydantic 工具 Schema 校验",
    agentInfo5: "简历结构化证据卡片",
    projectsLabel: "代表项目", projectsTitle: "AI 项目经验",
    archLabel: "本站后端架构", archTitle: "系统架构",
    archLoading: "加载架构图…",
    methodLabel: "我如何建设 LLM 应用", methodTitle: "工程原则",
    p1Title: "拆分推理与执行",
    p1Desc: "模型负责理解和生成，校验、路由、渲染和安全控制尽量由确定性逻辑承担。",
    p2Title: "先度量，再调优",
    p2Desc: "在修改 Prompt 或工作流前，先建立延迟基准、评估集、场景回放和回归检查。",
    p3Title: "把失败路径当成产品流程",
    p3Desc: "显式处理上下文缺失、工具超时、空值、服务异常和降级策略。",
    p4Title: "让输出易于消费",
    p4Desc: "在可靠性要求高的场景中，优先使用结构化契约、稳定 Schema 和前端友好的事件。",
    expLabel: "职业经历", expTitle: "工作经历",
    zalandoRole: "AI 软件工程师",
    zalandoDesc: "负责面向用户的 AI Agent 能力建设：个性化导购、商品决策辅助、实时 Streaming 优化和运行时稳定性。",
    twRole: "AI 软件工程师",
    twDesc: "为企业客户交付 AI 与后端系统：Text2SQL Agent、RAG 智能问答、定价平台和售后管理系统。",
    present: "至今",
    skillsLabel: "能力栈", skillsTitle: "技能",
    skillAi: "AI / LLM 应用开发", skillRetrieval: "检索与向量技术",
    skillBackend: "后端与基础设施", skillDeploy: "部署与可观测性",
    eduLabel: "教育背景", eduTitle: "学历",
    cardiffDegree: "英国卡迪夫大学 · Computing 硕士",
    suesDegree: "上海工程技术大学 · 市场营销 本科",
    footerStack: "前端：GitHub Pages · 后端：阿里云 FC · AI：DeepSeek",
  },
};

// ── Language ──────────────────────────────────────────────
let lang = localStorage.getItem("resume-lang") || "en";

function applyLang() {
  const d = T[lang];
  document.documentElement.lang = lang === "zh" ? "zh-CN" : "en";
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const k = el.dataset.i18n;
    if (d[k]) el.textContent = d[k];
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    const k = el.dataset.i18nPlaceholder;
    if (d[k]) el.placeholder = d[k];
  });
  const toggle = document.querySelector("[data-lang-toggle]");
  toggle.textContent = lang === "zh" ? "EN" : "中文";
  localStorage.setItem("resume-lang", lang);
}

document.querySelector("[data-lang-toggle]").addEventListener("click", () => {
  lang = lang === "zh" ? "en" : "zh";
  applyLang();
  renderProjects(cachedProjects);
  renderArchitecture(cachedArch);
});

function t(k) { return T[lang][k] || T.en[k] || k; }

// ── Counter animation ─────────────────────────────────────
function animateCounter(el) {
  const target = parseInt(el.dataset.count, 10);
  const prefix = el.dataset.prefix || "";
  const suffix = el.dataset.suffix || "";
  const duration = 1400;
  const start = performance.now();
  const ease = x => 1 - Math.pow(1 - x, 3);

  function step(now) {
    const p = Math.min((now - start) / duration, 1);
    const value = Math.round(ease(p) * target);
    el.textContent = prefix + value.toLocaleString() + suffix;
    if (p < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

const metricObserver = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting && !e.target.dataset.animated) {
      e.target.dataset.animated = "1";
      animateCounter(e.target);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll(".metric-num").forEach(el => metricObserver.observe(el));

// ── Projects from API ─────────────────────────────────────
let cachedProjects = null;

async function loadProjects() {
  try {
    const res = await fetch(`${API}/api/projects`);
    if (!res.ok) throw new Error("failed");
    cachedProjects = await res.json();
    renderProjects(cachedProjects);
  } catch {
    document.querySelector("[data-projects-grid]").innerHTML =
      `<p style="color:var(--muted);grid-column:1/-1">${t("agentError")}</p>`;
  }
}

function renderProjects(projects) {
  if (!projects) return;
  const grid = document.querySelector("[data-projects-grid]");
  grid.innerHTML = projects.map(p => `
    <article class="project-card ${p.highlight ? "highlight" : ""}">
      <div class="project-header">
        <div>
          <div class="project-company">${p.company}</div>
          <h3>${p.title}</h3>
        </div>
        <div class="project-period">${p.period}</div>
      </div>
      <p>${lang === "zh" ? p.summary_zh : p.summary_en}</p>
      <div class="impact-chips">
        ${p.impact.map(i => `<span>${i}</span>`).join("")}
      </div>
      <div class="skill-chips">
        ${p.skills.map(s => `<span>${s}</span>`).join("")}
      </div>
    </article>
  `).join("");
}

// ── Architecture from API ─────────────────────────────────
let cachedArch = null;

async function loadArchitecture() {
  try {
    const res = await fetch(`${API}/api/architecture`);
    if (!res.ok) throw new Error("failed");
    cachedArch = await res.json();
    renderArchitecture(cachedArch);
  } catch {
    document.querySelector("[data-arch-diagram]").innerHTML =
      `<p style="color:var(--muted)">${t("agentError")}</p>`;
  }
}

function renderArchitecture(arch) {
  if (!arch) return;
  const diag = document.querySelector("[data-arch-diagram]");
  diag.innerHTML = `
    <div class="arch-nodes">
      ${arch.nodes.map(n => `
        <div class="arch-node type-${n.type}">
          <div class="arch-node-label">${n.label}</div>
          <div class="arch-node-desc">${n.description}</div>
          <span class="arch-node-type">${n.type}</span>
        </div>
      `).join("")}
    </div>`;
  const summary = document.querySelector("[data-arch-summary]");
  summary.textContent = lang === "zh" ? arch.summary_zh : arch.summary_en;
}

// ── Agent chat ────────────────────────────────────────────
const messagesEl = document.querySelector("[data-agent-messages]");
const form = document.querySelector("[data-agent-form]");
const input = document.querySelector("[data-agent-input]");

let sessionId = null;

function addMsg(role, text) {
  const el = document.createElement("article");
  el.className = `msg msg-${role}`;
  const p = document.createElement("p");
  p.textContent = text;
  el.append(p);
  messagesEl.append(el);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return el;
}

function addToolMsg(toolName) {
  const el = document.createElement("article");
  el.className = "msg msg-tool";
  el.innerHTML = `→ <span class="tool-name">${toolName}</span>`;
  messagesEl.append(el);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return el;
}

function addEvidence(parent, evidence) {
  const existing = parent.querySelector(".evidence-list");
  if (existing) existing.remove();
  if (!evidence?.length) return;
  const list = document.createElement("div");
  list.className = "evidence-list";
  evidence.forEach(item => {
    const card = document.createElement("div");
    card.className = "evidence-card";
    card.innerHTML = `
      <strong>${item.title}</strong>
      <span class="ev-company">${item.company}</span>
      <p>${item.summary}</p>
      <div class="ev-chips">
        ${[...(item.evidence || []), ...(item.skills || []).slice(0, 3)].map(c => `<span>${c}</span>`).join("")}
      </div>`;
    list.append(card);
  });
  parent.append(list);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

form.addEventListener("submit", async e => {
  e.preventDefault();
  const msg = input.value.trim();
  if (!msg) return;
  input.value = "";
  addMsg("user", msg);
  const loading = addMsg("assistant", t("agentThinking"));
  const toolMsgs = [];

  try {
    const res = await fetch(`${API}/api/chat/stream`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ message: msg, language: lang, session_id: sessionId }),
    });
    if (!res.ok || !res.body) throw new Error(res.status);

    loading.remove();
    const answerEl = addMsg("assistant", "");
    const textEl = answerEl.querySelector("p");
    const reader = res.body.getReader();
    const dec = new TextDecoder();
    let buf = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += dec.decode(value, { stream: true });
      const parts = buf.split("\n\n");
      buf = parts.pop() || "";
      for (const part of parts) {
        const evLine = part.split("\n").find(l => l.startsWith("event:"));
        const dataLine = part.split("\n").find(l => l.startsWith("data:"));
        if (!evLine || !dataLine) continue;
        const ev = evLine.replace("event:", "").trim();
        const payload = JSON.parse(dataLine.replace("data:", "").trim());

        if (ev === "metadata") {
          if (payload.request_id) sessionId = payload.session_id || sessionId;
        }
        if (ev === "tool_call") {
          toolMsgs.push(addToolMsg(payload.name));
        }
        if (ev === "answer_delta") {
          textEl.textContent += payload.text || "";
          messagesEl.scrollTop = messagesEl.scrollHeight;
        }
        if (ev === "evidence") {
          toolMsgs.forEach(m => m.remove());
          addEvidence(answerEl, payload);
        }
        if (ev === "done" && payload.session_id) {
          sessionId = payload.session_id;
        }
        if (ev === "error") {
          textEl.textContent = payload.message || t("agentError");
        }
      }
    }
  } catch {
    loading.remove();
    try {
      const res = await fetch(`${API}/api/chat`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ message: msg, language: lang, session_id: sessionId }),
      });
      if (!res.ok) throw new Error(res.status);
      const data = await res.json();
      if (data.session_id) sessionId = data.session_id;
      const el = addMsg("assistant", data.answer);
      addEvidence(el, data.evidence);
    } catch {
      addMsg("assistant", t("agentError"));
    }
  }
});

document.querySelectorAll(".suggestion-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    input.value = lang === "zh" ? btn.dataset.qZh : btn.dataset.qEn;
    form.requestSubmit();
  });
});

// ── Init ──────────────────────────────────────────────────
document.getElementById("year").textContent = new Date().getFullYear();
applyLang();
loadProjects();
loadArchitecture();
