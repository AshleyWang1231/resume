# Job Search Queries for Mainland China and Hong Kong AI/Agent Roles

Use these query templates for market scan and fallback search guidance. Do not claim results are exhaustive. Prefer cited public sources or user-provided job descriptions for role-specific claims.

## Default Role Families

- AI Agent Engineer
- LLM Engineer
- GenAI Engineer
- AI Application Engineer
- Backend AI Engineer
- 大模型应用工程师
- AI 智能体工程师
- RAG 工程师
- AIGC 应用工程师

## Mainland China Platforms

Use these platforms when live search is available or when generating user-facing search instructions:

- LinkedIn Jobs
- Boss 直聘
- 猎聘
- 拉勾
- 脉脉
- Company career pages

Query examples:

```text
site:linkedin.com/jobs "AI Agent Engineer" "China"
site:linkedin.com/jobs "LLM Engineer" "Shanghai"
site:zhipin.com "AI Agent" "大模型应用"
site:zhipin.com "智能体" "Python"
site:liepin.com "大模型应用" "后端"
site:liepin.com "LLM" "RAG" "北京"
site:lagou.com "GenAI" "Python"
site:maimai.cn "AI Agent" "招聘"
```

## Hong Kong Platforms

Use these platforms when live search is available or when generating user-facing search instructions:

- LinkedIn Jobs
- JobsDB
- CTgoodjobs
- eFinancialCareers
- Company career pages

Query examples:

```text
site:linkedin.com/jobs "AI Agent Engineer" "Hong Kong"
site:linkedin.com/jobs "LLM Engineer" "Hong Kong"
site:linkedin.com/jobs "AI Engineer" "香港"
site:jobsdb.com "GenAI Engineer" "Hong Kong"
site:jobsdb.com "AI Engineer" "RAG" "Hong Kong"
site:ctgoodjobs.hk "AI Engineer" "LLM"
site:efinancialcareers.hk "GenAI" "Hong Kong"
```

## Keyword Clusters

### Core AI/Agent Keywords

```text
AI Agent
Agentic Workflow
LLM Application
Tool Calling
Function Calling
RAG
Retrieval Augmented Generation
Evaluation
LLM Evaluation
Streaming
Multi-agent
Workflow Automation
```

### Chinese Keywords

```text
大模型应用
AI 智能体
智能体工作流
工具调用
函数调用
检索增强生成
知识库问答
评估体系
模型评测
流式输出
多智能体
```

### Backend Keywords

```text
Python
FastAPI
Backend Engineer
API Integration
Serverless
Cloudflare
OpenAI-compatible API
Observability
Production AI System
```

## JD Intake Fallback

When live search returns too few reliable results, ask the user for job descriptions or links using this message:

```markdown
Live job search returned too few reliable results.
Fallback used: search query pack + JD intake workflow.
Recommended next input: paste 5-10 job descriptions or links.
```

Then analyze each pasted JD with:

- target role family
- core technical requirements
- required evidence from the resume
- matching resume evidence
- missing or weak evidence
- P0/P1/P2/P3 priority
- tailored application angle

## Fit Signals

Strong positive signals:

- production AI/LLM application ownership
- tool calling or function calling experience
- RAG or retrieval systems
- evaluation datasets or quality measurement
- streaming UX or latency optimization
- backend integration and deployment experience
- measurable outcomes

Risk signals:

- requires model pretraining or deep ML research not shown in evidence
- requires domain-specific finance, healthcare, or autonomous-driving expertise not shown in evidence
- requires local work authorization that is unknown
- requires management scope not shown in evidence
- vague AI role with no concrete product or engineering ownership
