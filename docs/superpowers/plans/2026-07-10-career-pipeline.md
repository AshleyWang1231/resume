# Career Pipeline Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a project-local `/career-pipeline` Claude Skill that produces a Markdown strategy pack from resume evidence, public LinkedIn input, AI/Agent job matching, and Mainland China + Hong Kong application strategy.

**Architecture:** Add a focused project skill under `.claude/skills/career-pipeline/` with one main `SKILL.md` and three reference files loaded progressively. The skill is documentation-driven: it orchestrates existing Claude capabilities and optional marketplace skills, applies strict privacy boundaries, and saves personal outputs under `.career/`, which remains git-ignored.

**Tech Stack:** Claude Code project skills, Markdown skill instructions, repository `.gitignore`, optional WebSearch/WebFetch/Read/Write tool usage during skill execution.

## Global Constraints

- Skill name: `career-pipeline`.
- Default target: `AI/Agent 工程`.
- Default market: `中国大陆 + 香港`.
- Default output: Markdown strategy pack.
- LinkedIn source: public URL when provided; resume-only fallback when public reading fails or `--no-linkedin` is used.
- Do not log in to LinkedIn.
- Do not bypass LinkedIn login walls or access controls.
- Do not store cookies, sessions, tokens, or credentials.
- Do not scrape non-public personal profiles.
- Do not automatically apply to jobs.
- Do not automatically send LinkedIn messages.
- Do not claim live job search is exhaustive.
- Ensure `.career/` is git-ignored.
- External marketplace skills are best-effort helpers, not hard dependencies.
- Do not run `git commit` unless the user explicitly asks for a commit in the current conversation.

---

## File Structure

Create or modify these files:

```text
.gitignore
.claude/skills/career-pipeline/SKILL.md
.claude/skills/career-pipeline/references/output-template.md
.claude/skills/career-pipeline/references/linkedin-checklist.md
.claude/skills/career-pipeline/references/job-search-queries.md
```

Responsibilities:

- `.gitignore`: keep local Claude settings and private career outputs out of git while allowing the project skill files to be tracked.
- `SKILL.md`: main slash-command instructions, argument handling, workflow phases, privacy rules, fallback behavior, and final response requirements.
- `output-template.md`: exact Markdown structure for the strategy pack.
- `linkedin-checklist.md`: LinkedIn profile audit and rewrite checklist.
- `job-search-queries.md`: Mainland China and Hong Kong AI/Agent job search query pack and JD intake fallback.

---

### Task 1: Add project skill entry point

**Files:**
- Modify: `.gitignore`
- Create: `.claude/skills/career-pipeline/SKILL.md`

**Interfaces:**
- Consumes: `docs/superpowers/specs/2026-07-10-career-pipeline-design.md` as the approved design source.
- Produces: A project skill named `career-pipeline` whose `SKILL.md` references `references/output-template.md`, `references/linkedin-checklist.md`, and `references/job-search-queries.md`.

- [ ] **Step 1: Run the failing validation**

Run this before creating files:

```bash
python3 - <<'PY'
from pathlib import Path
root = Path('.')
skill = root / '.claude/skills/career-pipeline/SKILL.md'
gitignore = (root / '.gitignore').read_text()
assert skill.exists(), 'missing .claude/skills/career-pipeline/SKILL.md'
assert '!.claude/skills/career-pipeline/**' in gitignore, 'career-pipeline skill is not unignored in .gitignore'
assert '.career/' in gitignore, '.career/ is not ignored'
text = skill.read_text()
assert 'name: career-pipeline' in text
assert 'user-invocable: true' in text
assert 'AI/Agent 工程' in text
assert '中国大陆 + 香港' in text
assert 'Do not log in to LinkedIn' in text
print('career-pipeline entrypoint validation passed')
PY
```

Expected: FAIL with `missing .claude/skills/career-pipeline/SKILL.md`.

- [ ] **Step 2: Update `.gitignore`**

Replace the existing line:

```gitignore
.claude
```

with this block:

```gitignore
# Claude Code local settings stay private, but project skills may be tracked
.claude/*
!.claude/skills/
!.claude/skills/career-pipeline/
!.claude/skills/career-pipeline/**

# Career pipeline — personal job-search data, never commit
.career/
```

Keep the existing interview-coach personal data ignore block unchanged.

- [ ] **Step 3: Create the skill directory**

Run:

```bash
mkdir -p .claude/skills/career-pipeline/references
```

Expected: command exits successfully.

- [ ] **Step 4: Write `.claude/skills/career-pipeline/SKILL.md`**

Create the file with this complete content:

```markdown
---
name: career-pipeline
description: Builds a career strategy pack from resume evidence, a public LinkedIn profile, AI/Agent role matching, and Mainland China plus Hong Kong job-search strategy. Use when the user asks for career pipeline, LinkedIn optimization, resume-to-LinkedIn updates, job matching, job search strategy, application strategy, AI Agent jobs, LLM Engineer roles, GenAI roles, or China/Hong Kong career planning.
user-invocable: true
---

# Career Pipeline

Build a repeatable career workflow:

```text
Resume / portfolio evidence
  -> LinkedIn optimization
  -> AI/Agent role matching
  -> Mainland China + Hong Kong application strategy pack
```

## Defaults

Use these defaults unless the user specifies otherwise:

- Target: `AI/Agent 工程`
- Market: `中国大陆 + 香港`
- Output: Markdown strategy pack
- LinkedIn source: public URL when provided
- Automation: no auto-apply, no auto-message, no account automation

## Privacy Boundaries

You may read public web pages, repository resume evidence, and user-provided job descriptions. You must not cross account or privacy boundaries.

Do not:

- Do not log in to LinkedIn.
- Do not bypass LinkedIn login walls or access controls.
- Do not ask for LinkedIn credentials.
- Do not store cookies, sessions, tokens, or credentials.
- Do not scrape non-public personal profiles.
- Do not automatically apply to jobs.
- Do not automatically send LinkedIn messages.
- Do not claim live job search is exhaustive.

Before saving output, ensure `.career/` is git-ignored. Save personal strategy packs under `.career/strategy-packs/` when file writes are appropriate for the session.

## Inputs

Accept any of these forms:

```text
/career-pipeline https://www.linkedin.com/in/sample-profile
/career-pipeline --no-linkedin
/career-pipeline --market "香港,深圳,上海" --target "AI Agent Engineer"
/career-pipeline --job "Senior AI Agent Engineer role requiring Python, RAG, tool calling, evaluation, and backend production experience."
```

Interpret arguments loosely:

- A LinkedIn URL sets `linkedin_source`.
- `--no-linkedin` disables LinkedIn reading.
- `--market` overrides the market.
- `--target` overrides the role family.
- `--job` means analyze the provided job description before or instead of live job search.
- If arguments are ambiguous, make a sensible assumption and list it in the final pack.

## Required Workflow

### Phase 1 — Profile Intake

1. Read relevant resume / portfolio evidence from the current repository.
2. If a public LinkedIn URL is provided and `--no-linkedin` is absent, try to read the public page with normal web access.
3. If public LinkedIn reading fails, continue with resume-only LinkedIn optimization and state the fallback.
4. Normalize the candidate context into:
   - current positioning
   - key projects
   - skills
   - metrics
   - target roles
   - market constraints
   - LinkedIn availability

### Phase 2 — LinkedIn Optimization

Use the checklist in `references/linkedin-checklist.md`.

When available, optionally use these external skills as helpers:

- `linkedin profile optimizer`
- `resume-ats-beater`

These external skills are best-effort helpers. If they are unavailable, continue with the built-in checklist.

Produce recommendations for:

- Headline
- About
- Experience
- Skills
- Featured
- Projects
- keyword coverage
- recruiter searchability
- proof and metrics density
- Mainland China + Hong Kong market phrasing

### Phase 3 — Market & Role Scan

Use the query pack in `references/job-search-queries.md`.

When available, optionally use these external skills as helpers:

- `job-search-strategist`
- `career-ops-job-search`
- `job-search`

These external skills are best-effort helpers. If they are unavailable or live results are thin, continue with search queries and a job-description intake workflow.

Default role families:

- AI Agent Engineer
- LLM Engineer
- GenAI Engineer
- AI Application Engineer
- Backend AI Engineer

### Phase 4 — Fit Matrix

Score roles or job descriptions with these dimensions:

| Dimension | Meaning |
|---|---|
| Skill Fit | Technical keyword and capability match. |
| Evidence Fit | Concrete resume proof or metrics. |
| Market Fit | Mainland China / Hong Kong phrasing and expectations. |
| Seniority Fit | Years, scope, and responsibility match. |
| Differentiation | Why this candidate stands out. |
| Risk | Gaps, weak evidence, location constraints, language mismatch, or domain mismatch. |

Use these priorities:

- `P0`: apply now; high match and strong differentiation
- `P1`: worth applying; light tailoring needed
- `P2`: watch or apply selectively; visible gaps
- `P3`: not recommended now; weak match or high risk

### Phase 5 — Strategy Pack

Read `references/output-template.md` and fill every section. The final response must include either the full strategy pack or a clear path to the saved strategy pack plus an executive summary.

## Fallback Messages

Use these exact fallback statements when the condition occurs.

Public LinkedIn read fails:

```markdown
LinkedIn profile could not be read from the public URL.
Fallback used: resume-only LinkedIn optimization.
Recommended next input: paste your LinkedIn About and Experience sections.
```

Live job search returns too few reliable results:

```markdown
Live job search returned too few reliable results.
Fallback used: search query pack + JD intake workflow.
Recommended next input: paste 5-10 job descriptions or links.
```

External skill unavailable:

```markdown
External skill unavailable: skill-name
Fallback used: built-in checklist and prompts.
```

Missing details:

```markdown
Missing information:
- Preferred cities
- Salary expectations
- Current LinkedIn About section
- Work authorization constraints

Assumptions used this run:
- Market: 中国大陆 + 香港
- Target: AI/Agent 工程
```

## Output Rules

- Ground claims in resume evidence, LinkedIn public content, user-provided job descriptions, or cited public job sources.
- Do not invent employers, metrics, dates, job postings, compensation, or work authorization facts.
- Clearly separate evidence-backed recommendations from assumptions.
- Prefer bilingual phrasing when useful for Mainland China + Hong Kong roles.
- Make the strategy actionable: prioritize, sequence, and explain what to do next.
- If saving a file, write it under `.career/strategy-packs/` and mention the path.
```

- [ ] **Step 5: Re-run validation**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
root = Path('.')
skill = root / '.claude/skills/career-pipeline/SKILL.md'
gitignore = (root / '.gitignore').read_text()
assert skill.exists(), 'missing .claude/skills/career-pipeline/SKILL.md'
assert '!.claude/skills/career-pipeline/**' in gitignore, 'career-pipeline skill is not unignored in .gitignore'
assert '.career/' in gitignore, '.career/ is not ignored'
text = skill.read_text()
assert 'name: career-pipeline' in text
assert 'user-invocable: true' in text
assert 'AI/Agent 工程' in text
assert '中国大陆 + 香港' in text
assert 'Do not log in to LinkedIn' in text
print('career-pipeline entrypoint validation passed')
PY
```

Expected: PASS and prints `career-pipeline entrypoint validation passed`.

- [ ] **Step 6: Review changed files**

Run:

```bash
git diff -- .gitignore .claude/skills/career-pipeline/SKILL.md
```

Expected: diff shows the `.gitignore` allowlist for `.claude/skills/career-pipeline/`, `.career/` ignored, and the new `SKILL.md`.

- [ ] **Step 7: Prepare commit only if explicitly authorized**

If the user explicitly asks for a commit, run:

```bash
git add .gitignore .claude/skills/career-pipeline/SKILL.md docs/superpowers/specs/2026-07-10-career-pipeline-design.md

git commit -m "Add career pipeline skill design and entrypoint

Co-Authored-By: Claude <noreply@anthropic.com>"
```

Expected: commit succeeds. If the user has not explicitly asked for a commit, do not run these commands.

---

### Task 2: Add output template and LinkedIn checklist references

**Files:**
- Create: `.claude/skills/career-pipeline/references/output-template.md`
- Create: `.claude/skills/career-pipeline/references/linkedin-checklist.md`

**Interfaces:**
- Consumes: `SKILL.md` references to `references/output-template.md` and `references/linkedin-checklist.md`.
- Produces: The strategy pack template and the LinkedIn audit checklist used by the skill workflow.

- [ ] **Step 1: Run the failing validation**

Run before creating the reference files:

```bash
python3 - <<'PY'
from pathlib import Path
base = Path('.claude/skills/career-pipeline/references')
output = base / 'output-template.md'
checklist = base / 'linkedin-checklist.md'
assert output.exists(), 'missing output-template.md'
assert checklist.exists(), 'missing linkedin-checklist.md'
output_text = output.read_text()
checklist_text = checklist.read_text()
for heading in ['Executive Summary', 'Resume -> LinkedIn Gap Analysis', 'Job Match Matrix', 'Application Strategy', 'Next Actions']:
    assert heading in output_text, f'missing output template heading: {heading}'
for item in ['Headline', 'About', 'Experience', 'Skills', 'Featured', 'Projects']:
    assert item in checklist_text, f'missing LinkedIn checklist item: {item}'
print('career-pipeline reference validation passed')
PY
```

Expected: FAIL with `missing output-template.md` or `missing linkedin-checklist.md`.

- [ ] **Step 2: Write `references/output-template.md`**

Create `.claude/skills/career-pipeline/references/output-template.md` with this complete content:

```markdown
# Career Pipeline Strategy Pack Template

Use this exact structure for the final strategy pack. Fill every section. If evidence is unavailable, state the assumption or fallback instead of leaving the section blank.

## 1. Executive Summary

- **Current positioning:** One sentence grounded in resume evidence.
- **Recommended direction:** The best-fit AI/Agent role family for this run.
- **Top 3 actions:** Three actions the user should take next.

## 2. Resume -> LinkedIn Gap Analysis

### LinkedIn Availability

State whether LinkedIn content was read from a public URL, skipped by `--no-linkedin`, or unavailable due to public-read failure.

### High-Impact Changes

List the three to seven LinkedIn changes most likely to improve recruiter searchability and role fit.

### Headline Options

Provide three headline options:

1. AI/Agent-focused headline.
2. Backend + AI systems headline.
3. Bilingual Mainland China / Hong Kong market headline.

### About Section Draft

Write a concise About draft. Include only facts supported by resume evidence, public LinkedIn content, or user-provided information.

### Experience Rewrite Recommendations

For each relevant role or project, provide:

- existing signal from resume evidence
- LinkedIn gap
- improved bullet or paragraph
- keywords covered

### Skills, Featured, and Projects

Recommend skills to add or reorder, projects to feature, and evidence to surface.

## 3. Target Role Profile

- **Target keywords:** Role and technical keywords to search for.
- **Common requirements:** Requirements seen in job descriptions or generated from the query pack.
- **Strong matches:** Candidate strengths with evidence.
- **Gaps or phrasing changes:** Missing evidence, weak language, or terms to reframe.

## 4. Job Match Matrix

Use this table. If live job search is unavailable, fill it with job families or user-provided job descriptions instead of fabricated postings.

| Priority | Role | Company | Location | Match | Best Evidence | Risks | Strategy |
|---|---|---|---|---|---|---|---|
| P0/P1/P2/P3 | Role title or role family | Company name or source type | City/region | High/Medium/Low with reason | Resume or LinkedIn evidence | Concrete risk | Next action |

## 5. Application Strategy

### Positioning

Write one positioning statement tailored to the selected market and target role.

### Top Roles to Apply

For each P0 or P1 role, include:

- why this role is attractive
- which resume evidence to emphasize
- which LinkedIn keywords to align
- outreach or referral angle

### Resume / LinkedIn Keywords

- **Must emphasize:** Keywords strongly supported by evidence.
- **Nice to include:** Keywords that are relevant but less central.
- **Avoid overclaiming:** Terms not sufficiently supported by evidence.

### Recommended Application Order

Give a clear order for applications and explain why.

## 6. Next Actions

### Today

List actions that can be completed in one working session.

### This Week

List actions for the next five working days.

### Next Inputs Needed

List the most useful information for the next run, such as LinkedIn About text, job descriptions, preferred cities, salary expectations, or work authorization constraints.

## Fallbacks Used

List every fallback used in this run. If none were used, write `No fallback was needed.`

## Sources and Evidence

List resume files, public URLs, job sources, and user-provided inputs used. Do not include private tokens, cookies, or credentials.
```

- [ ] **Step 3: Write `references/linkedin-checklist.md`**

Create `.claude/skills/career-pipeline/references/linkedin-checklist.md` with this complete content:

```markdown
# LinkedIn Optimization Checklist

Use this checklist to audit and rewrite a LinkedIn profile for AI/Agent engineering roles in Mainland China and Hong Kong.

## Evidence Rules

- Use only resume evidence, public LinkedIn content, user-provided information, or cited public sources.
- Do not invent employers, dates, metrics, projects, publications, certifications, compensation, or work authorization details.
- If evidence is missing, label the recommendation as an assumption or ask for that input in `Next Inputs Needed`.

## Headline

Check whether the headline communicates:

- target role family: AI Agent Engineer, LLM Engineer, GenAI Engineer, AI Application Engineer, or Backend AI Engineer
- differentiator: production AI systems, tool calling, RAG, evaluation, streaming, backend integration, or bilingual market fit
- seniority signal when supported by evidence
- searchable keywords for Mainland China and Hong Kong recruiters

Strong headline patterns:

```text
AI Agent / LLM Application Engineer | Tool Calling, RAG, Evaluation, Streaming | Backend Production Systems
Backend AI Engineer | AI Agent Workflows, FastAPI, Python, OpenAI-compatible Providers | EN/ZH
GenAI Engineer focused on Agentic Workflows, Retrieval, Tool Use, and Production Evaluation
```

## About

The About section should include:

1. role positioning in the first two lines
2. strongest AI/Agent evidence
3. production backend evidence
4. metrics or concrete outcomes
5. target market phrasing for Mainland China and Hong Kong
6. concise collaboration or communication signal when supported

Avoid:

- generic enthusiasm without proof
- unsupported claims about leadership, scale, or model training
- long paragraphs that hide keywords

## Experience

For each experience entry, check:

- Does the first bullet state the business or product context?
- Does the second bullet show technical depth?
- Does at least one bullet include a metric or concrete outcome?
- Are AI/Agent keywords explicit and searchable?
- Are tool names included only when supported by evidence?

Preferred bullet shape:

```text
Built or improved [system] for [user/business context], using [technical approach], resulting in [measurable or concrete outcome].
```

## Skills

Prioritize skills that match target roles and are supported by evidence.

Must-emphasize candidates:

- AI Agent
- LLM Application Engineering
- Tool Calling
- RAG
- Evaluation
- Streaming
- Python
- FastAPI
- Backend Systems
- OpenAI-compatible APIs
- Cloudflare or serverless deployment when supported

Use Chinese equivalents when helpful for Mainland China roles:

- 大模型应用
- AI 智能体
- 工具调用
- 检索增强生成
- 评估体系
- 后端工程

## Featured

Recommend featuring proof-heavy artifacts:

- portfolio or resume agent website
- AI chat or agent demo
- evaluation or benchmark write-up
- architecture diagram
- project post explaining tool calling, RAG, streaming, or evaluation

Each Featured item should answer:

- What does it prove?
- Which target role keyword does it support?
- What should a recruiter notice in ten seconds?

## Projects

For each project, capture:

- project title
- one-line impact
- technical stack
- target role keywords
- evidence or metric
- link when public

## Recruiter Searchability

Check whether the profile contains exact terms recruiters may search:

```text
AI Agent
LLM Engineer
GenAI Engineer
大模型应用
智能体
RAG
Tool Calling
Evaluation
Python
FastAPI
Backend
Hong Kong
香港
深圳
上海
北京
```

Only include locations that match the user's preferences or stated market.
```

- [ ] **Step 4: Re-run validation**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
base = Path('.claude/skills/career-pipeline/references')
output = base / 'output-template.md'
checklist = base / 'linkedin-checklist.md'
assert output.exists(), 'missing output-template.md'
assert checklist.exists(), 'missing linkedin-checklist.md'
output_text = output.read_text()
checklist_text = checklist.read_text()
for heading in ['Executive Summary', 'Resume -> LinkedIn Gap Analysis', 'Job Match Matrix', 'Application Strategy', 'Next Actions']:
    assert heading in output_text, f'missing output template heading: {heading}'
for item in ['Headline', 'About', 'Experience', 'Skills', 'Featured', 'Projects']:
    assert item in checklist_text, f'missing LinkedIn checklist item: {item}'
print('career-pipeline reference validation passed')
PY
```

Expected: PASS and prints `career-pipeline reference validation passed`.

- [ ] **Step 5: Review changed files**

Run:

```bash
git diff -- .claude/skills/career-pipeline/references/output-template.md .claude/skills/career-pipeline/references/linkedin-checklist.md
```

Expected: diff shows the two new reference files.

- [ ] **Step 6: Prepare commit only if explicitly authorized**

If the user explicitly asks for a commit, run:

```bash
git add .claude/skills/career-pipeline/references/output-template.md .claude/skills/career-pipeline/references/linkedin-checklist.md

git commit -m "Add career pipeline output and LinkedIn references

Co-Authored-By: Claude <noreply@anthropic.com>"
```

Expected: commit succeeds. If the user has not explicitly asked for a commit, do not run these commands.

---

### Task 3: Add job-search query pack and static skill validation

**Files:**
- Create: `.claude/skills/career-pipeline/references/job-search-queries.md`

**Interfaces:**
- Consumes: `SKILL.md` reference to `references/job-search-queries.md`.
- Produces: Search query templates and fallback instructions for Mainland China + Hong Kong AI/Agent role discovery.

- [ ] **Step 1: Run the failing validation**

Run before creating the query file:

```bash
python3 - <<'PY'
from pathlib import Path
query_file = Path('.claude/skills/career-pipeline/references/job-search-queries.md')
assert query_file.exists(), 'missing job-search-queries.md'
text = query_file.read_text()
for required in ['LinkedIn Jobs', 'Boss 直聘', '猎聘', 'JobsDB', 'AI Agent Engineer', '大模型应用', 'Hong Kong', '香港']:
    assert required in text, f'missing query reference: {required}'
print('career-pipeline job query validation passed')
PY
```

Expected: FAIL with `missing job-search-queries.md`.

- [ ] **Step 2: Write `references/job-search-queries.md`**

Create `.claude/skills/career-pipeline/references/job-search-queries.md` with this complete content:

```markdown
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
```

- [ ] **Step 3: Re-run query validation**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
query_file = Path('.claude/skills/career-pipeline/references/job-search-queries.md')
assert query_file.exists(), 'missing job-search-queries.md'
text = query_file.read_text()
for required in ['LinkedIn Jobs', 'Boss 直聘', '猎聘', 'JobsDB', 'AI Agent Engineer', '大模型应用', 'Hong Kong', '香港']:
    assert required in text, f'missing query reference: {required}'
print('career-pipeline job query validation passed')
PY
```

Expected: PASS and prints `career-pipeline job query validation passed`.

- [ ] **Step 4: Run full static validation**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
root = Path('.')
skill_dir = root / '.claude/skills/career-pipeline'
files = [
    skill_dir / 'SKILL.md',
    skill_dir / 'references/output-template.md',
    skill_dir / 'references/linkedin-checklist.md',
    skill_dir / 'references/job-search-queries.md',
]
for path in files:
    assert path.exists(), f'missing {path}'
    text = path.read_text()
    assert 'TBD' not in text, f'placeholder TBD found in {path}'
    assert 'TODO' not in text, f'placeholder TODO found in {path}'
    assert 'PLACEHOLDER' not in text, f'placeholder PLACEHOLDER found in {path}'

skill = (skill_dir / 'SKILL.md').read_text()
assert 'references/output-template.md' in skill
assert 'references/linkedin-checklist.md' in skill
assert 'references/job-search-queries.md' in skill
assert 'Do not automatically apply to jobs.' in skill
assert 'Do not automatically send LinkedIn messages.' in skill

gitignore = (root / '.gitignore').read_text()
assert '.career/' in gitignore
assert '!.claude/skills/career-pipeline/**' in gitignore
print('career-pipeline full static validation passed')
PY
```

Expected: PASS and prints `career-pipeline full static validation passed`.

- [ ] **Step 5: Review final changed files**

Run:

```bash
git status --short

git diff -- .gitignore .claude/skills/career-pipeline docs/superpowers/specs/2026-07-10-career-pipeline-design.md
```

Expected: status shows the new spec and skill files, plus `.gitignore` modified. Diff shows no personal `.career/` artifacts.

- [ ] **Step 6: Prepare commit only if explicitly authorized**

If the user explicitly asks for a commit, run:

```bash
git add .gitignore .claude/skills/career-pipeline docs/superpowers/specs/2026-07-10-career-pipeline-design.md docs/superpowers/plans/2026-07-10-career-pipeline.md

git commit -m "Add career pipeline skill

Co-Authored-By: Claude <noreply@anthropic.com>"
```

Expected: commit succeeds. If the user has not explicitly asked for a commit, do not run these commands.

---

### Task 4: Manually verify slash-command behavior

**Files:**
- No file changes expected after Task 3.

**Interfaces:**
- Consumes: `career-pipeline` project skill files from Tasks 1-3.
- Produces: Manual verification notes confirming the skill can guide resume-only, public LinkedIn, and pasted-JD workflows.

- [ ] **Step 1: Verify the skill appears or reload if needed**

In Claude Code, start a fresh session or reload available skills if the current session does not list project skills immediately. Then type:

```text
/career-pipeline --no-linkedin
```

Expected: the skill loads and follows the Career Pipeline workflow.

- [ ] **Step 2: Verify resume-only fallback behavior**

Run:

```text
/career-pipeline --no-linkedin
```

Expected output includes:

```text
LinkedIn was not read because --no-linkedin was used.
```

Expected strategy pack sections:

- Executive Summary
- Resume -> LinkedIn Gap Analysis
- Target Role Profile
- Job Match Matrix
- Application Strategy
- Next Actions

- [ ] **Step 3: Verify public LinkedIn URL fallback behavior**

Run with a harmless sample URL that may not expose useful public content:

```text
/career-pipeline https://www.linkedin.com/in/sample-profile
```

Expected: if public reading fails, output includes the exact fallback statement:

```markdown
LinkedIn profile could not be read from the public URL.
Fallback used: resume-only LinkedIn optimization.
Recommended next input: paste your LinkedIn About and Experience sections.
```

- [ ] **Step 4: Verify pasted JD behavior**

Run:

```text
/career-pipeline --job "Senior AI Agent Engineer role requiring Python, RAG, tool calling, LLM evaluation, backend API integration, and production monitoring for a Hong Kong-based product team."
```

Expected output includes:

- JD-specific fit analysis
- P0/P1/P2/P3 priority
- best resume evidence
- risks
- application strategy

- [ ] **Step 5: Verify no private artifacts are staged**

Run:

```bash
git status --short --ignored | grep -E '(^!! .career/|^\?\? \.career/)' || true
```

Expected: `.career/` appears only as ignored (`!! .career/`) if strategy packs were saved, or no output if no `.career/` files were created. It must not appear as untracked (`?? .career/`).

- [ ] **Step 6: Final implementation summary**

Report:

```text
Implemented /career-pipeline as a project skill.
Static validation passed.
Manual checks run: resume-only, public LinkedIn fallback, pasted JD.
No automatic application or messaging behavior was added.
.career/ remains git-ignored.
```

If any manual check could not run because the current session needs a reload to see the new skill, report that explicitly and give the exact command the user should try next:

```text
/career-pipeline --no-linkedin
```
