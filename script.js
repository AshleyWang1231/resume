const VISITOR_BOARD_API = ""; // Set to the AWS Lambda Function URL before deploying to S3.

const T = {
  en: {
    eyebrow: "AI Software Engineer",
    navCapabilities: "Capabilities",
    navVisitorBoard: "Visitor Board",
    navProjects: "Projects",
    downloadResume: "PDF",
    heroKicker: "AI Software Engineer",
    heroTitle: "I ship AI Agent systems from design to production.",
    heroLead: "Focused on building production-grade LLM applications and AI Agent systems. Experienced in Python/Java backend development, Agent Workflows, Tool Calling, Streaming, personalization, product decision support, and Text2SQL. Led AI product capabilities across e-commerce and financial services — including personalized shopping assistance, real-time response optimization, and enterprise data analysis agents — with end-to-end experience from system design to production rollout.",
    heroWork: "Leave a public note",
    heroAgentPrefix: "Original resume agent experience:",
    heroAgentLink: "open the live site",

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


    projectsKicker: "Related experience",
    projectsTitle: "Each case: problem → approach → outcome.",


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
    visitorSubmitted: "Public note submitted. You can edit or delete it for 3 minutes.",
    visitorSubmitError: "Could not submit public note. Please try again later.",
    visitorEdit: "Edit",
    visitorDelete: "Delete",
    visitorSave: "Save",
    visitorCancel: "Cancel",
    visitorEditableUntil: "Editable for 3 minutes after posting.",
    visitorDeleteConfirm: "Delete this public note?",
    visitorUpdated: "Public note updated.",
    visitorDeleted: "Public note deleted.",
    visitorEditExpired: "The edit window has expired.",
  },
  zh: {
    eyebrow: "AI 软件工程师",
    navCapabilities: "核心能力",
    navVisitorBoard: "访客留言板",
    navProjects: "项目",
    downloadResume: "简历 PDF",
    heroKicker: "AI 软件工程师",
    heroTitle: "从设计到上线，我构建生产级 AI Agent 系统。",
    heroLead: "专注于生产级 LLM 应用与 AI Agent 系统建设。擅长基于 Python/Java 构建高可用后端服务，在 Agent Workflow、Tool Calling、Streaming、个性化推荐、商品决策辅助及 Text2SQL 等方向具备丰富实践经验。主导电商与金融领域 AI 产品研发，负责个性化导购、实时响应优化、企业级数据分析 Agent 等核心能力建设，具备从系统设计到生产落地的完整经验。",
    heroWork: "留下公开留言",
    heroAgentPrefix: "原始 AI 简历 Agent 体验：",
    heroAgentLink: "打开线上版本",

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


    projectsKicker: "相关项目经验",
    projectsTitle: "每个案例：问题 → 方案 → 结果。",


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
    visitorSubmitted: "公开留言已提交。3 分钟内可以编辑或删除。",
    visitorSubmitError: "暂时无法提交公开留言，请稍后再试。",
    visitorEdit: "编辑",
    visitorDelete: "删除",
    visitorSave: "保存",
    visitorCancel: "取消",
    visitorEditableUntil: "发布后 3 分钟内可编辑或删除。",
    visitorDeleteConfirm: "删除这条公开留言？",
    visitorUpdated: "公开留言已更新。",
    visitorDeleted: "公开留言已删除。",
    visitorEditExpired: "编辑时间已过。",
  },
};

let lang = localStorage.getItem("resume-lang") || "en";
let cachedProjects = null;

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
  loadVisitorMessages({ quiet: true });
}


function bindBackground() {
  const root = document.documentElement;
  window.addEventListener("pointermove", (event) => {
    root.style.setProperty("--mouse-x", `${event.clientX}px`);
    root.style.setProperty("--mouse-y", `${event.clientY}px`);
  }, { passive: true });
}



const PROJECTS_DATA = [{"id":"agent-runtime","title":"Agent Runtime & Streaming Architecture","company":"Zalando","period":"2025–2026","summary_en":"Redesigned the Zalando Assistant Agent Runtime — Streaming architecture, Tool Calling integration, OpenAI Responses API migration.","summary_zh":"重新设计 Zalando Assistant Agent Runtime，覆盖 Streaming 架构、Tool Calling 接入和 OpenAI Responses API 迁移。","star_s_en":"The assistant returned full responses only after all tool calls completed, giving users no visibility into agent progress and making interactions feel sluggish.","star_a_en":"Introduced a Streaming layer separating process states, business events, and user-visible text into typed SSE events. Integrated product-detail Tool Calling so answers are grounded in live catalogue data. Migrated the runtime from Chat Completions to OpenAI Responses API, unifying the Tool Calling + Streaming path.","star_r_en":"Average TTFT –25% (Suggestions API benchmark). P95 TTFT –25% in validated flows. Users see real-time tool progress instead of a blank wait.","star_s_zh":"助手需等所有工具调用完成后才整体输出，用户看不到任何进度，体验偏慢。","star_a_zh":"引入 Streaming 分发层，将过程状态、业务事件和用户可见文本拆分为类型化 SSE 事件。接入商品详情 Tool Calling，让回答基于实时商品数据。将主链路从 Chat Completions 迁移至 OpenAI Responses API，统一 Tool Calling + Streaming 路径。","star_r_zh":"平均 TTFT 降低 25%（Suggestions API 基准测试），P95 TTFT 降低 25%，用户实时可见工具调用进度。","impact":["-25% avg TTFT","-25% P95 TTFT","Typed SSE events","OpenAI Responses API"],"skills":["Agent Runtime","Tool Calling","Streaming","State Machine","OpenAI Responses API"],"highlight":true},{"id":"personalization","title":"Personalization & Warm-Up Architecture","company":"Zalando","period":"2025–2026","summary_en":"Built personalization pipeline and async Warm-Up architecture for Zalando Assistant Conversation Starters.","summary_zh":"为 Zalando Assistant Conversation Starters 构建个性化链路和异步 Warm-Up 架构。","star_s_en":"Conversation Starters used static signals only, called the profile service on every request, and had noticeable cold-start latency under traffic spikes.","star_a_en":"(1) Rebuilt the input pipeline to fuse real-time conversation context, user profile, and behaviour history. (2) Added a TTL cache layer with field-level invalidation in front of the profile service. (3) Designed an async Warm-Up: a Redis registry tracks pending first-screen requests; a background worker pre-generates suggestions; in-memory fallback handles cache misses.","star_r_en":"Conversation Starter engagement +15%. Cold-start time –60%. Profile-service calls –70%; P99 latency –60% under high concurrency. Validated across 800+ real product-detail-page scenarios.","star_s_zh":"Conversation Starters 仅依赖静态信号，每次请求都调用画像服务，高峰期冷启动延迟明显。","star_a_zh":"(1) 重建输入链路，融合实时对话上下文、用户画像和历史行为。(2) 在画像服务前加 TTL 缓存层，支持字段级失效。(3) 设计异步 Warm-Up：Redis 注册表追踪待处理首屏请求，后台 Worker 提前生成建议，内存降级兜底。","star_r_zh":"推荐入口互动率 +15%，冷启动时间 -60%，画像服务调用量 -70%，高并发下 P99 延迟 -60%。基于 800+ 真实商品页面场景验证。","impact":["+15% engagement","-60% cold-start","-70% profile calls","-60% P99 latency"],"skills":["Personalization","Redis","Async Warm-Up","Caching","Eval-Driven"],"highlight":true},{"id":"product-comparison","title":"Product Comparison Skill","company":"Zalando","period":"2025–2026","summary_en":"Designed and shipped a multi-turn product comparison capability for Zalando Assistant.","summary_zh":"为 Zalando Assistant 设计并上线多轮商品对比能力。","star_s_en":"Users asked to compare browsed products, but free-form LLM output was unreliable: table layouts broke, discount fields went missing, and multi-turn references (\"compare the first two\") were frequently misresolved.","star_a_en":"Split responsibilities: the model handles intent, conversation-state tracking, and summary copy; deterministic code owns product-reference resolution, field selection, discount calculation, and layout rendering. This gave the frontend a stable contract independent of model version.","star_r_en":"Comparison-scenario engagement +20%. Eliminated LLM formatting instability; frontend rendering is stable across model updates.","star_s_zh":"用户要求对比已浏览商品，但 LLM 直接输出格式不稳定：布局错乱、折扣字段缺失，多轮引用频繁解析错误。","star_a_zh":"责任拆分：模型负责意图理解、对话状态追踪和总结文案；确定性代码负责商品引用解析、字段选择、折扣计算和布局渲染，向前端提供与模型版本无关的稳定契约。","star_r_zh":"对比场景互动率 +20%，消除 LLM 格式不稳定问题，前端渲染跨模型版本保持稳定。","impact":["+20% engagement","Stable rendering","Multi-turn references","Model/code split"],"skills":["Structured Output","Tool Calling","Multi-turn","Deterministic Rendering"],"highlight":true},{"id":"text2sql","title":"Text2SQL AI Agent — Enterprise Data Analysis","company":"Thoughtworks · Major Domestic Bank","period":"2021–2025","summary_en":"Built an enterprise data-analysis Agent for a major domestic bank, enabling natural-language querying of complex structured data.","summary_zh":"为国内知名银行构建企业数据分析 Agent，支持复杂结构化数据的自然语言查询。","star_s_en":"Non-technical pricing analysts needed self-service access to complex structured data. Naive LLM prompts failed on nested conditions and ambiguous schema fields, bad SQL could corrupt pricing decisions, and there was no evaluation baseline.","star_a_en":"Designed a multi-stage agent pipeline: intent clarification → SQL generation → automated SQL validation → exception retry → result summarisation with visualisations. Built dual-layer vector reranking (field + value) to reduce schema hallucination. Created a 1,000+ case evaluation suite from real business queries as a regression baseline for all prompt changes.","star_r_en":"End-to-end query accuracy +20%. SQL validation + retry loop eliminated silent failures. 1,000+ eval cases became the team's standard regression baseline.","star_s_zh":"非技术定价分析师需自助查询复杂结构化数据，但直接 prompt LLM 在嵌套条件和歧义字段上错误率高，且缺乏评估基线。","star_a_zh":"设计多阶段 Agent 流水线：意图澄清 → SQL 生成 → 自动 SQL 校验 → 异常重试 → 结果总结与可视化。构建字段+值双层向量 Rerank 减少 schema 幻觉。从真实业务查询积累 1,000+ 条评估用例作为回归基线。","star_r_zh":"端到端查询准确率 +20%，SQL 校验+重试消除静默失败，1,000+ 评估用例成为团队标准回归基线。","impact":["+20% accuracy","1,000+ eval cases","Dual-layer rerank","Auto SQL validation"],"skills":["Text2SQL","Multi-stage Agent","FAISS","Reranking","SQL Validation","Evaluation"],"highlight":false},{"id":"pricing-management","title":"Pricing Management System — Access Control & Data Pipeline","company":"Thoughtworks · Major Domestic Bank","period":"2021–2025","summary_en":"Backend module owner for a bank-wide interest-rate product pricing platform — access control, reporting, and database migration.","summary_zh":"负责国内知名银行利率类金融产品定价管理系统的权限模块、报表模块及数据库迁移等核心工作。","star_s_en":"The pricing platform needed fine-grained access control across complex role hierarchies and multiple business lines, high-performance in-memory multi-dimensional aggregation for reporting, and a MySQL architecture struggling under millions of daily pricing transactions.","star_a_en":"(1) Led access control module design and implementation using Hexagonal Architecture and DDD — modelled complex role hierarchies and fine-grained permissions as a reusable domain layer adopted across multiple sub-systems. (2) Designed a custom in-memory data processing pipeline (Tablesaw + custom toolchain) for the reporting module to replace external dependencies. (3) Spearheaded the database migration strategy, delivering a zero-downtime production switchover for large-scale business tables.","star_r_en":"Reporting module dev efficiency +40%; delivery cycle shortened by 2+ weeks. Database migration achieved zero business impact, sustaining stable operation under millions of daily pricing requests. Access control module reused across multiple sub-systems.","star_s_zh":"定价平台需跨多业务线支持复杂角色层级与细粒度权限管理；报表模块需内存中多维聚合与计算；原 MySQL 架构在海量业务数据下存在性能瓶颈。","star_a_zh":"(1) 基于六边形架构与 DDD 主导权限模块设计与落地，构建可复用领域模型，在多个子系统中复用。(2) 针对报表模块自研内存数据加工方案（Tablesaw + 自定义工具链），替代外部依赖。(3) 主导数据库迁移方案设计与实施，完成生产环境平滑切换。","star_r_zh":"报表模块开发效率提升约 40%，开发工期缩短 2 周以上。数据库迁移实现 0 业务感知，系统在每日数百万笔定价请求下稳定运行。权限模块在多个子系统中复用。","impact":["+40% dev efficiency","–2 weeks cycle","0-downtime DB migration","Multi-system reuse"],"skills":["Spring Cloud","Hexagonal Architecture","Tablesaw","MySQL","Redis","RabbitMQ"],"highlight":false},{"id":"rag-chatbot","title":"RAG Knowledge Q&A System","company":"Thoughtworks","period":"2021–2025","summary_en":"Built a production RAG pipeline for enterprise policy Q&A alongside the Text2SQL agent.","summary_zh":"与 Text2SQL Agent 并行，构建企业政策问答生产级 RAG 流水线。","star_s_en":"The bank needed a reliable Q&A system over internal policy documents, with no existing retrieval infrastructure or quality measurement.","star_a_en":"Built a full RAG pipeline with LlamaIndex and FAISS — chunking strategy, embedding, vector retrieval, and answer generation. Introduced RAGAS evaluation (faithfulness, relevance, context coverage) as the quality gate, creating a reusable eval harness the team adopted for all subsequent RAG work.","star_r_en":"RAGAS faithfulness 0.82 / context recall 0.78 on internal policy Q&A benchmark. Eval harness adopted by 3 downstream RAG projects; reusable pipeline template cut average onboarding ~40%.","star_s_zh":"银行需要基于内部政策文档的可靠问答系统，无现有检索基础设施，也没有质量度量方式。","star_a_zh":"基于 LlamaIndex + FAISS 构建完整 RAG 流水线——切片策略、Embedding、向量检索和答案生成。引入 RAGAS（忠实性、相关性、上下文覆盖率）作为质量门控，形成团队后续 RAG 工作的可复用评估框架。","star_r_zh":"RAGAS 忠实性评分 0.82，上下文召回率 0.78。评估框架被 3 个后续 RAG 项目复用，可复用流水线模板将平均上线周期缩短约 40%。","impact":["Faithfulness 0.82","Context recall 0.78","-40% onboarding","3 projects adopted"],"skills":["RAG","LlamaIndex","FAISS","Embedding","RAGAS"],"highlight":false}];

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


function visitorBoardUrl(path) {
  return `${VISITOR_BOARD_API.replace(/\/$/, "")}${path}`;
}

const tokenKey = (id) => `visitor-board-token-${id}`;

function storeEditToken(id, editToken, editExpiresAt) {
  if (!id || !editToken || !editExpiresAt) return;
  sessionStorage.setItem(tokenKey(id), JSON.stringify({ editToken, editExpiresAt }));
}

function getEditToken(id) {
  try {
    const raw = sessionStorage.getItem(tokenKey(id));
    if (!raw) return null;
    const token = JSON.parse(raw);
    if (!token.editToken || !token.editExpiresAt || new Date(token.editExpiresAt).getTime() <= Date.now()) {
      sessionStorage.removeItem(tokenKey(id));
      return null;
    }
    return token;
  } catch {
    sessionStorage.removeItem(tokenKey(id));
    return null;
  }
}

function clearEditToken(id) {
  sessionStorage.removeItem(tokenKey(id));
}

function setVisitorStatus(message = "", type = "") {
  const status = $("#visitor-status");
  if (!status) return;
  status.textContent = message;
  status.dataset.status = type;
}

async function updateVisitorMessage(id, message, editToken) {
  const res = await fetch(visitorBoardUrl(`/messages/${encodeURIComponent(id)}`), {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, editToken }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || t("visitorSubmitError"));
  return data.item;
}

async function deleteVisitorMessage(id, editToken) {
  const res = await fetch(visitorBoardUrl(`/messages/${encodeURIComponent(id)}`), {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ editToken }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || t("visitorSubmitError"));
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

    const token = getEditToken(item.id);
    if (token) {
      const note = document.createElement("p");
      note.className = "visitor-edit-note";
      note.textContent = t("visitorEditableUntil");

      const actions = document.createElement("div");
      actions.className = "visitor-message-actions";

      const edit = document.createElement("button");
      edit.type = "button";
      edit.textContent = t("visitorEdit");
      edit.addEventListener("click", () => renderEditForm(article, item, token));

      const remove = document.createElement("button");
      remove.type = "button";
      remove.textContent = t("visitorDelete");
      remove.addEventListener("click", async () => {
        if (!window.confirm(t("visitorDeleteConfirm"))) return;
        try {
          await deleteVisitorMessage(item.id, token.editToken);
          clearEditToken(item.id);
          await loadVisitorMessages({ quiet: true });
          setVisitorStatus(t("visitorDeleted"), "success");
        } catch (error) {
          setVisitorStatus(error.message || t("visitorSubmitError"), "error");
        }
      });

      actions.append(edit, remove);
      article.append(note, actions);
    }

    container.append(article);
  });
}

function renderEditForm(article, item, token) {
  article.replaceChildren();

  const textarea = document.createElement("textarea");
  textarea.className = "visitor-edit-textarea";
  textarea.maxLength = 500;
  textarea.value = item.message || "";

  const actions = document.createElement("div");
  actions.className = "visitor-message-actions";

  const save = document.createElement("button");
  save.type = "button";
  save.textContent = t("visitorSave");
  save.addEventListener("click", async () => {
    const message = textarea.value.trim();
    if (!message) {
      setVisitorStatus(t("visitorRequired"), "error");
      return;
    }
    try {
      await updateVisitorMessage(item.id, message, token.editToken);
      await loadVisitorMessages({ quiet: true });
      setVisitorStatus(t("visitorUpdated"), "success");
    } catch (error) {
      setVisitorStatus(error.message || t("visitorSubmitError"), "error");
    }
  });

  const cancel = document.createElement("button");
  cancel.type = "button";
  cancel.textContent = t("visitorCancel");
  cancel.addEventListener("click", () => loadVisitorMessages({ quiet: true }));

  actions.append(save, cancel);
  article.append(textarea, actions);
  textarea.focus();
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
    storeEditToken(data.item?.id, data.editToken, data.editExpiresAt);
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


function init() {
  $("#year").textContent = new Date().getFullYear();
  $("[data-lang-toggle]")?.addEventListener("click", () => {
    lang = lang === "zh" ? "en" : "zh";
    applyLang();
  });
  bindBackground();
  bindVisitorBoard();
  applyLang();
  loadProjects();
}

init();
