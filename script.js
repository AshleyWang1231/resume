const translations = {
  en: {
    navAgent: "Resume Agent",
    navSystems: "AI Systems",
    navMethod: "Method",
    navExperience: "Experience",
    navProjects: "AI Projects",
    navSkills: "Skills",
    navEducation: "Education",
    eyebrow: "AI Software Engineer",
    heroName: "Lu Wang",
    summary:
      "AI Software Engineer focused on building LLM applications and AI Agent systems for real business scenarios. Experienced in Python/Java backend development, Agent Workflows, Tool Calling, Streaming, personalization, product decision support, Text2SQL, and observability-driven performance diagnostics.",
    phone: "+86 13122038365",
    downloadResume: "Download resume",
    agentEyebrow: "Resume Agent",
    agentTitle: "Ask my resume",
    agentIntro:
      "Ask about Lu's AI Agent, Streaming, personalization, Product Comparison, or Text2SQL experience.",
    agentPlaceholder: "Ask about Lu's AI engineering experience...",
    agentSend: "Ask",
    agentSuggestionsTitle: "Try asking",
    agentThinking: "Reading resume evidence...",
    agentError: "The resume agent is temporarily unavailable. Please try again later.",
    agentQ1: "What AI Agent systems has Lu built?",
    agentQ2: "Show Lu's Streaming and Tool Calling experience.",
    agentQ3: "What measurable impact does Lu have?",
    agentQ4: "Explain Lu's Text2SQL experience.",
    heroVisual: "LLM applications built with product context, engineering controls, and measurable outcomes.",
    consoleLabel: "AI capability areas",
    consoleAgent: "Tool Calling · Streaming · Responses API",
    consolePersonalization: "Profiles · Context · Warm-Up · Cache",
    consoleDecision: "Product Comparison · Structured Output",
    consoleEnterprise: "Text2SQL · RAG · Evaluation",
    systemsEyebrow: "AI Systems Portfolio",
    systemsTitle: "From LLM capability to reliable product systems",
    coreEyebrow: "Core",
    coreDesc:
      "Turning model capabilities into tool-integrated, observable, testable, and user-facing systems.",
    capAgent:
      "Tool orchestration, Streaming, final-answer extraction, and real-time response reliability.",
    capRag:
      "Retrieval, reranking, SQL validation, evaluation datasets, and enterprise Q&A workflows.",
    capPersonalization:
      "User profile, behavior, conversation context, Warm-Up precompute, cache, and fallback paths.",
    capStructured:
      "Model reasoning separated from deterministic rendering contracts for stable product experiences.",
    capEvaluation: "Benchmarking latency, accuracy, coverage, fallback behavior, and regression quality.",
    workflowEyebrow: "Workflow Showcase",
    workflowTitle: "How the AI systems work",
    tabAgent: "Agent Runtime",
    tabPersonalization: "Personalization",
    tabComparison: "Product Comparison",
    tabText2sql: "Text2SQL",
    agentStep1: "User Intent",
    agentStep2: "Tool Calling",
    agentStep3: "Event Stream",
    agentStep4: "Final Answer",
    personalStep1: "Profile",
    personalStep2: "Context",
    personalStep3: "Warm-Up",
    personalStep4: "Starter Suggestions",
    comparisonStep1: "Natural Language",
    comparisonStep2: "Reference Parsing",
    comparisonStep3: "Criteria Selection",
    comparisonStep4: "Structured Table",
    text2sqlStep1: "Clarify",
    text2sqlStep2: "Schema Link",
    text2sqlStep3: "SQL Validate",
    text2sqlStep4: "Summarize",
    flowAgent:
      "Coordinated tool results, process states, business events, and final model output in one real-time flow to reduce duplicated display and latency.",
    flowPersonalization:
      "Combined profile signals, historical behavior, and conversation context with asynchronous precomputation to improve first-screen relevance and speed.",
    flowComparison:
      "Let the model understand shopping intent while deterministic code handles fields, discounts, layout, and rendering markers.",
    flowText2sql:
      "Built a multi-stage Agent workflow with prompt optimization, field/value reranking, SQL validation, retry logic, and evaluation cases.",
    methodEyebrow: "Engineering Method",
    methodTitle: "How I build LLM applications",
    principle1Title: "Separate reasoning from execution",
    principle1Desc:
      "Use the model for understanding and generation; keep validation, routing, rendering, and safety controls deterministic.",
    principle2Title: "Measure before tuning",
    principle2Desc:
      "Use latency benchmarks, evaluation sets, scenario replay, and regression checks before changing prompts or workflows.",
    principle3Title: "Design for failure paths",
    principle3Desc:
      "Handle missing context, tool timeouts, empty values, service errors, and fallback behavior as first-class product flows.",
    principle4Title: "Make output easy to consume",
    principle4Desc:
      "Prefer structured contracts, stable schemas, and frontend-friendly events over free-form model output where reliability matters.",
    sectionCurrent: "Current Focus",
    experienceTitle: "Work Experience",
    present: "Present",
    zalandoRole: "AI Software Engineer",
    zalandoRoleDesc:
      "Building customer-facing AI Agent capabilities for personalized shopping assistance, product decision support, real-time response optimization, and runtime reliability.",
    thoughtworksRole: "AI Software Engineer",
    thoughtworksRoleDesc:
      "Delivered AI and backend systems for enterprise clients, including Text2SQL Agents, RAG Q&A systems, pricing platforms, and after-sales management systems.",
    sectionSelected: "Selected Work",
    projectsTitle: "AI Projects",
    p1Title: "Personalized Conversation Starters",
    p1Desc:
      "Built personalized starter suggestions using user profile, behavior, conversation context, and product signals.",
    p1c1: "+15% engagement",
    p1c2: "-60% cold start",
    p1c3: "-70% profile calls",
    p1c4: "800+ scenarios",
    p2Title: "Agent Runtime Upgrade",
    p2Desc:
      "Upgraded Agent Runtime with product-detail Tool Calling, Streaming handling, and OpenAI Responses API migration.",
    p2c1: "-25% avg TTFT",
    p2c2: "-25% P95 TTFT",
    p2c3: "Streaming stability",
    p3Title: "Product Comparison Skill",
    p3Desc:
      "Launched natural-language product comparison with context-aware reference parsing and stable table rendering.",
    p3c1: "+20% engagement",
    p3c2: "Multi-turn references",
    p3c3: "Structured output",
    p4Title: "Text2SQL AI Agent",
    p4Meta: "Thoughtworks · Leading Domestic Bank",
    p4Desc:
      "Built an enterprise data-analysis Agent for natural-language query, SQL generation, validation, and visualization.",
    p4c1: "+20% accuracy",
    p4c2: "1,000+ cases",
    p4c3: "Field + value rerank",
    sectionCapabilities: "Capabilities",
    skillsTitle: "Skills & Technologies",
    skillAi: "AI / LLM Application Development",
    skillRetrieval: "Retrieval and Vector Technologies",
    skillBackend: "Programming and Backend",
    skillTools: "Engineering Tools",
    sectionEducation: "Education",
    educationTitle: "Education",
    cardiffDegree: "MSc in Computing",
    suesDegree: "BA in Marketing",
  },
  zh: {
    navAgent: "简历 Agent",
    navSystems: "AI 系统",
    navMethod: "工程方法",
    navExperience: "工作经历",
    navProjects: "AI 项目",
    navSkills: "技能",
    navEducation: "教育",
    eyebrow: "AI 软件工程师",
    heroName: "汪露",
    summary:
      "专注于面向真实业务场景的 LLM 应用与 AI Agent 系统建设，具备 Python/Java 后端研发、Agent Workflow、Tool Calling、Streaming、个性化推荐、商品决策辅助、Text2SQL 和可观测性驱动性能诊断经验。",
    phone: "13122038365（微信同号）",
    downloadResume: "下载简历",
    agentEyebrow: "简历 Agent",
    agentTitle: "直接问我的简历",
    agentIntro: "可以询问汪露的 AI Agent、Streaming、个性化、商品对比或 Text2SQL 经验。",
    agentPlaceholder: "输入你想了解的 AI 工程经历...",
    agentSend: "提问",
    agentSuggestionsTitle: "可以这样问",
    agentThinking: "正在读取简历证据...",
    agentError: "简历 Agent 暂时不可用，请稍后再试。",
    agentQ1: "汪露做过哪些 AI Agent 系统？",
    agentQ2: "展示 Streaming 和 Tool Calling 经验。",
    agentQ3: "有哪些可量化结果？",
    agentQ4: "介绍 Text2SQL 项目经验。",
    heroVisual: "将业务上下文、工程控制和可量化结果结合起来的 LLM 应用建设经验。",
    consoleLabel: "AI 能力方向",
    consoleAgent: "Tool Calling · Streaming · Responses API",
    consolePersonalization: "用户画像 · 上下文 · Warm-Up · 缓存",
    consoleDecision: "商品对比 · 结构化输出",
    consoleEnterprise: "Text2SQL · RAG · 评估",
    systemsEyebrow: "AI 系统作品集",
    systemsTitle: "从 LLM 能力到可靠产品系统",
    coreEyebrow: "核心能力",
    coreDesc: "将模型能力转化为可集成工具、可观测、可测试、可面向用户的真实系统。",
    capAgent: "工具编排、Streaming、最终答案提取和实时响应稳定性。",
    capRag: "检索、重排序、SQL 校验、评估数据集和企业问答工作流。",
    capPersonalization: "用户画像、行为、对话上下文、Warm-Up 预计算、缓存和降级路径。",
    capStructured: "将模型推理与确定性渲染契约拆分，保障产品体验稳定。",
    capEvaluation: "围绕延迟、准确率、覆盖率、降级行为和回归质量做评估。",
    workflowEyebrow: "工作流展示",
    workflowTitle: "AI 系统如何工作",
    tabAgent: "Agent Runtime",
    tabPersonalization: "个性化",
    tabComparison: "商品对比",
    tabText2sql: "Text2SQL",
    agentStep1: "用户意图",
    agentStep2: "工具调用",
    agentStep3: "事件流",
    agentStep4: "最终回答",
    personalStep1: "用户画像",
    personalStep2: "上下文",
    personalStep3: "Warm-Up",
    personalStep4: "对话入口",
    comparisonStep1: "自然语言",
    comparisonStep2: "引用解析",
    comparisonStep3: "维度选择",
    comparisonStep4: "结构化表格",
    text2sqlStep1: "意图澄清",
    text2sqlStep2: "Schema 关联",
    text2sqlStep3: "SQL 校验",
    text2sqlStep4: "结果总结",
    flowAgent:
      "在一条实时链路中协调工具结果、过程状态、业务事件和最终模型输出，减少重复展示和响应延迟。",
    flowPersonalization:
      "结合用户画像、历史行为和对话上下文，并通过异步预计算提升首屏相关性和响应速度。",
    flowComparison:
      "让模型负责理解购物意图，由确定性代码处理字段、折扣、布局和渲染标记。",
    flowText2sql:
      "构建多阶段 Agent 工作流，结合 Prompt 优化、字段和值重排序、SQL 校验、重试逻辑和评估用例。",
    methodEyebrow: "工程方法",
    methodTitle: "我如何建设 LLM 应用",
    principle1Title: "拆分推理与执行",
    principle1Desc: "模型负责理解和生成，校验、路由、渲染和安全控制尽量由确定性逻辑承担。",
    principle2Title: "先度量，再调优",
    principle2Desc: "在修改 Prompt 或工作流前，先建立延迟基准、评估集、场景回放和回归检查。",
    principle3Title: "把失败路径当成产品流程",
    principle3Desc: "显式处理上下文缺失、工具超时、空值、服务异常和降级策略。",
    principle4Title: "让输出易于消费",
    principle4Desc: "在可靠性要求高的场景中，优先使用结构化契约、稳定 Schema 和前端友好的事件。",
    sectionCurrent: "当前方向",
    experienceTitle: "工作经历",
    present: "至今",
    zalandoRole: "AI 软件工程师",
    zalandoRoleDesc:
      "负责面向用户的 AI Agent 能力建设，包括个性化导购、商品决策辅助、实时响应优化和运行时稳定性。",
    thoughtworksRole: "AI 软件工程师",
    thoughtworksRoleDesc:
      "为企业客户交付 AI 与后端系统，包括 Text2SQL Agent、RAG 智能问答、定价平台和售后管理系统。",
    sectionSelected: "代表项目",
    projectsTitle: "AI 项目经验",
    p1Title: "个性化 Conversation Starters",
    p1Desc:
      "结合用户画像、行为、对话上下文和商品信号，生成个性化对话入口。",
    p1c1: "+15% 互动率",
    p1c2: "-60% 冷启动",
    p1c3: "-70% 画像调用",
    p1c4: "800+ 场景",
    p2Title: "Agent Runtime 主链路升级",
    p2Desc:
      "升级商品详情 Tool Calling、Streaming 处理和 OpenAI Responses API 链路。",
    p2c1: "-25% 平均 TTFT",
    p2c2: "-25% P95 TTFT",
    p2c3: "Streaming 稳定性",
    p3Title: "Product Comparison Skill",
    p3Desc:
      "上线自然语言商品对比能力，支持多轮引用解析和稳定表格渲染。",
    p3c1: "+20% 互动率",
    p3c2: "多轮商品引用",
    p3c3: "结构化输出",
    p4Title: "Text2SQL AI Agent",
    p4Meta: "Thoughtworks · 国内知名银行",
    p4Desc:
      "建设企业数据分析 Agent，支持自然语言查询、SQL 生成、校验和可视化。",
    p4c1: "+20% 准确率",
    p4c2: "1,000+ 用例",
    p4c3: "字段+值重排序",
    sectionCapabilities: "能力栈",
    skillsTitle: "技能与技术",
    skillAi: "AI / LLM 应用开发",
    skillRetrieval: "检索与向量技术",
    skillBackend: "编程与后端",
    skillTools: "工程化工具",
    sectionEducation: "教育背景",
    educationTitle: "教育背景",
    cardiffDegree: "英国卡迪夫大学 · Computing 硕士",
    suesDegree: "上海工程技术大学 · 市场营销 本科",
  },
};

const toggle = document.querySelector("[data-lang-toggle]");
const translatable = document.querySelectorAll("[data-i18n]");
const placeholderTranslatable = document.querySelectorAll("[data-i18n-placeholder]");
const year = document.getElementById("year");
const workflowTabs = document.querySelectorAll("[data-workflow-tab]");
const workflowPanels = document.querySelectorAll("[data-workflow-panel]");
const agentForm = document.querySelector("[data-agent-form]");
const agentInput = document.querySelector("[data-agent-input]");
const agentMessages = document.querySelector("[data-agent-messages]");
const agentQuestionButtons = document.querySelectorAll("[data-agent-question-en]");
const API_BASE_URL = "https://resume-gent-api-vtugquposb.cn-hangzhou.fcapp.run";

function setLanguage(lang) {
  const dictionary = translations[lang] || translations.en;
  document.documentElement.lang = lang === "zh" ? "zh-CN" : "en";

  translatable.forEach((element) => {
    const key = element.dataset.i18n;
    if (dictionary[key]) {
      element.textContent = dictionary[key];
    }
  });

  placeholderTranslatable.forEach((element) => {
    const key = element.dataset.i18nPlaceholder;
    if (dictionary[key]) {
      element.setAttribute("placeholder", dictionary[key]);
    }
  });

  toggle.textContent = lang === "zh" ? "EN" : "中文";
  toggle.setAttribute("aria-label", lang === "zh" ? "Switch to English" : "切换到中文");
  localStorage.setItem("resume-lang", lang);
}

toggle.addEventListener("click", () => {
  const next = document.documentElement.lang === "zh-CN" ? "en" : "zh";
  setLanguage(next);
});

workflowTabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    const target = tab.dataset.workflowTab;
    workflowTabs.forEach((item) => item.classList.toggle("active", item === tab));
    workflowPanels.forEach((panel) => {
      panel.classList.toggle("active", panel.dataset.workflowPanel === target);
    });
  });
});

agentForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = agentInput.value.trim();
  if (!message) return;

  agentInput.value = "";
  appendMessage("user", message);
  const loading = appendMessage("assistant", getText("agentThinking"));

  try {
    loading.remove();
    await streamAgentResponse(message);
  } catch (error) {
    console.error(error);
    loading.remove();
    try {
      const payload = await fetchAgentResponse(message);
      appendAgentResponse(payload);
    } catch (fallbackError) {
      console.error(fallbackError);
      appendMessage("assistant", getText("agentError"));
    }
  }
});

agentQuestionButtons.forEach((button) => {
  button.addEventListener("click", () => {
    agentInput.value =
      getCurrentLanguage() === "zh" ? button.dataset.agentQuestionZh : button.dataset.agentQuestionEn;
    agentForm.requestSubmit();
  });
});

function getCurrentLanguage() {
  return document.documentElement.lang === "zh-CN" ? "zh" : "en";
}

function getText(key) {
  return translations[getCurrentLanguage()][key] || translations.en[key] || key;
}

async function fetchAgentResponse(message) {
  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      message,
      language: getCurrentLanguage(),
    }),
  });

  if (!response.ok) {
    throw new Error(`Resume agent request failed: ${response.status}`);
  }

  return response.json();
}

async function streamAgentResponse(message) {
  const response = await fetch(`${API_BASE_URL}/api/chat/stream`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      message,
      language: getCurrentLanguage(),
    }),
  });

  if (!response.ok || !response.body) {
    throw new Error(`Resume agent stream failed: ${response.status}`);
  }

  const streamedMessage = appendMessage("assistant", "");
  const streamedText = streamedMessage.querySelector("p");
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const events = buffer.split("\n\n");
    buffer = events.pop() || "";
    events.forEach((eventText) => handleStreamEvent(eventText, streamedMessage, streamedText));
  }

  if (buffer) {
    handleStreamEvent(buffer, streamedMessage, streamedText);
  }
}

function handleStreamEvent(eventText, message, textElement) {
  const lines = eventText.split("\n");
  const eventLine = lines.find((line) => line.startsWith("event:"));
  const dataLine = lines.find((line) => line.startsWith("data:"));
  if (!eventLine || !dataLine) return;

  const eventName = eventLine.replace("event:", "").trim();
  const rawData = dataLine.replace("data:", "").trim();
  const payload = JSON.parse(rawData);

  if (eventName === "answer_delta") {
    textElement.textContent += payload.text || "";
    agentMessages.scrollTop = agentMessages.scrollHeight;
  }

  if (eventName === "evidence" && Array.isArray(payload)) {
    appendEvidence(message, payload);
  }

  if (eventName === "error") {
    textElement.textContent = payload.message || getText("agentError");
  }
}

function appendMessage(role, text) {
  const message = document.createElement("article");
  message.className = `agent-message ${role}`;
  const paragraph = document.createElement("p");
  paragraph.textContent = text;
  message.append(paragraph);
  agentMessages.append(message);
  agentMessages.scrollTop = agentMessages.scrollHeight;
  return message;
}

function appendAgentResponse(payload) {
  const message = document.createElement("article");
  message.className = "agent-message assistant";

  const answer = document.createElement("p");
  answer.textContent = payload.answer;
  message.append(answer);

  if (Array.isArray(payload.evidence) && payload.evidence.length > 0) {
    appendEvidence(message, payload.evidence);
  }

  agentMessages.append(message);
  agentMessages.scrollTop = agentMessages.scrollHeight;
}

function appendEvidence(message, evidence) {
  const existing = message.querySelector(".evidence-list");
  if (existing) {
    existing.remove();
  }

  const evidenceList = document.createElement("div");
  evidenceList.className = "evidence-list";

  evidence.forEach((item) => {
    const card = document.createElement("section");
    card.className = "evidence-card";

    const title = document.createElement("strong");
    title.textContent = item.title;
    const meta = document.createElement("span");
    meta.textContent = item.company;
    const summary = document.createElement("p");
    summary.textContent = item.summary;

    const chips = document.createElement("div");
    chips.className = "result-chips";
    [...(item.evidence || []), ...(item.skills || []).slice(0, 3)].forEach((chipText) => {
      const chip = document.createElement("span");
      chip.textContent = chipText;
      chips.append(chip);
    });

    card.append(title, meta, summary, chips);
    evidenceList.append(card);
  });

  message.append(evidenceList);
  agentMessages.scrollTop = agentMessages.scrollHeight;
}

year.textContent = new Date().getFullYear();
setLanguage(localStorage.getItem("resume-lang") || "en");
