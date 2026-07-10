# Career Pipeline Skill Design

Date: 2026-07-10

## Goal

Create a Claude Skill / slash command named `/career-pipeline` that turns Lu Wang's existing resume and portfolio evidence into a repeatable career workflow:

```text
Resume / portfolio evidence
  -> LinkedIn optimization
  -> AI/Agent role matching
  -> Mainland China + Hong Kong application strategy pack
```

The first version should produce a high-quality Markdown strategy pack. It should not automate applications, send messages, log in to LinkedIn, bypass access controls, or store sensitive career materials in git.

## Recommended Approach

Use one main skill with internal phases:

```text
/career-pipeline
  Phase 1. Profile Intake
  Phase 2. LinkedIn Optimization
  Phase 3. Market & Role Scan
  Phase 4. Fit Matrix
  Phase 5. Application Strategy Pack
```

This keeps the user experience simple while keeping the internal workflow modular and debuggable. External marketplace skills can enhance the workflow, but the main skill must still produce a useful output if any external skill is unavailable.

## User Entry Point

### Skill name

```text
/career-pipeline
```

### Common invocations

Run with a public LinkedIn URL:

```text
/career-pipeline https://www.linkedin.com/in/<profile>
```

Run with explicit preferences:

```text
/career-pipeline https://www.linkedin.com/in/<profile> --market "中国大陆,香港" --target "AI Agent Engineer"
```

Run without reading LinkedIn:

```text
/career-pipeline --no-linkedin
```

Run against a pasted job description:

```text
/career-pipeline --job "<paste JD here>"
```

## Defaults

If the user does not specify options, use these defaults:

```text
target: AI/Agent 工程
market: 中国大陆 + 香港
output: strategy pack
automation: no auto-apply, no auto-message, no account automation
linkedin_source: public URL when provided; otherwise resume-only fallback
```

## Output Contract

Every successful run should produce a Markdown strategy pack with this structure:

```markdown
# Career Pipeline Strategy Pack

## 1. Executive Summary
- Current positioning
- Most recommended application direction
- Top 3 actions for this run

## 2. Resume -> LinkedIn Gap Analysis
- LinkedIn headline recommendations
- About section recommendations
- Experience rewrite recommendations
- Skills / Featured / Projects recommendations
- Missing or under-emphasized evidence compared with the resume

## 3. Target Role Profile
- Target role keywords
- Common job description requirements
- Strong current matches
- Gaps or phrasing changes needed

## 4. Job Match Matrix
| Role | Company | Location | Match | Why | Risk | Priority |
|---|---|---|---|---|---|---|

## 5. Application Strategy
- Top priority roles
- Positioning angle for each role
- Resume / LinkedIn keywords to emphasize
- Recommended application order

## 6. Next Actions
- What to do today
- What to do this week
- What to provide next time
```

## Output Storage

The skill should save personal career artifacts under a git-ignored local directory:

```text
.career/
  strategy-packs/
    2026-07-10-career-pipeline.md
  linkedin-snapshots/
  job-shortlists/
```

Implementation should ensure `.career/` is present in `.gitignore` before writing personal strategy packs there.

## Internal Phase Design

### Phase 1 — Profile Intake

Purpose: collect and normalize candidate context.

Inputs:

1. Current repository resume / portfolio data.
2. Public LinkedIn URL, when provided.
3. User options such as `--market`, `--target`, `--job`, `--no-linkedin`, and `--language`.

Preferred LinkedIn behavior:

- Try `linkedin-reader` when available.
- Read only public content visible from the provided URL.
- If public reading fails, continue with resume-only LinkedIn optimization.
- Do not ask for or store LinkedIn credentials.

Profile context output:

```markdown
## Candidate Profile Context
- Current positioning
- Key projects
- Skills
- Metrics
- Target roles
- Market constraints
- LinkedIn availability
```

### Phase 2 — LinkedIn Optimization

Purpose: compare resume evidence with LinkedIn content and produce actionable LinkedIn edits.

External skills to use when available:

- `linkedin profile optimizer`
- `resume-ats-beater`

Analysis dimensions:

```text
Headline
About
Experience
Skills
Featured
Projects
Keyword coverage
Recruiter searchability
Proof / metrics density
Market-specific phrasing
```

Market-specific emphasis for AI/Agent engineering roles in Mainland China and Hong Kong:

- AI Agent
- LLM application engineering
- GenAI engineering
- Tool Calling
- RAG
- Evaluation
- Streaming
- Backend integration
- Python
- FastAPI
- Cloudflare
- OpenAI-compatible providers
- Bilingual Chinese / English communication where supported by evidence

Output:

```markdown
## LinkedIn Optimization Plan
### High-impact changes
### Headline options
### About rewrite draft
### Experience bullet rewrites
### Skills to add or reorder
### Featured section recommendations
```

### Phase 3 — Market & Role Scan

Purpose: identify target role families and candidate opportunities.

External skills to use when available:

- `job-search-strategist`
- `career-ops-job-search`
- `job-search`

Default search scope:

```text
中国大陆 + 香港
AI Agent Engineer
LLM Engineer
GenAI Engineer
AI Application Engineer
Backend AI Engineer
```

The first version should produce an auditable shortlist rather than claiming exhaustive coverage of the market.

Market scan output:

```markdown
## Market Scan
- Search queries used
- Role families found
- Companies / sectors appearing repeatedly
- Common requirements
- Common compensation / seniority signals if available
- Links or source snippets when available
```

If live job search is weak or unavailable, fallback to a query pack and JD intake workflow. Suggested platforms include:

- LinkedIn Jobs
- Boss 直聘
- 猎聘
- 拉勾
- 脉脉
- JobsDB
- CTgoodjobs
- eFinancialCareers
- Company career pages

### Phase 4 — Fit Matrix

Purpose: score roles against Lu's resume evidence and produce a prioritized shortlist.

Scoring dimensions:

| Dimension | Meaning |
|---|---|
| Skill Fit | Technical keyword and capability match. |
| Evidence Fit | Whether resume evidence includes concrete proof or metrics. |
| Market Fit | Whether the candidate positioning fits Mainland China / Hong Kong phrasing and expectations. |
| Seniority Fit | Whether role seniority matches years, scope, and responsibility. |
| Differentiation | What makes the candidate stand out for this role. |
| Risk | Gaps, weak evidence, location constraints, language mismatch, or domain mismatch. |

Priority definitions:

```text
P0 = apply now; high match and strong differentiation
P1 = worth applying; light tailoring needed
P2 = watch or apply selectively; visible gaps
P3 = not recommended now; weak match or high risk
```

Fit matrix output:

```markdown
| Priority | Role | Company | Location | Match | Best Evidence | Risks | Strategy |
|---|---|---|---|---|---|---|---|
```

### Phase 5 — Application Strategy Pack

Purpose: turn the analysis into a concrete action plan.

Required sections:

```markdown
## Application Strategy

### Positioning
A concise positioning statement.

### Top Roles to Apply
- Why this role
- Which resume evidence to emphasize
- LinkedIn keywords to align
- Suggested outreach angle

### Resume / LinkedIn Keywords
- Must emphasize
- Nice to include
- Avoid overclaiming

### This Week Action Plan
- Day 1: update LinkedIn headline and About
- Day 2: add or reorder Featured projects
- Day 3: shortlist target jobs
- Day 4: customize top applications
- Day 5: outreach or referral requests

### Follow-up Inputs Needed
- Missing LinkedIn sections
- Job descriptions to paste next time
- Preferred cities / salary / remote constraints
```

## External Skill Policy

The main skill should use external marketplace skills as best-effort helpers, not hard dependencies.

```text
Try external skill if available
  -> use the output if useful
  -> otherwise continue with built-in checklists and prompts
  -> always produce a final strategy pack
```

This policy applies to LinkedIn reading, LinkedIn optimization, resume ATS review, and job search.

## Privacy and Safety Boundaries

The skill must not:

- Log in to LinkedIn.
- Bypass LinkedIn login walls or access controls.
- Store cookies, sessions, tokens, or credentials.
- Scrape non-public personal profiles.
- Automatically apply to jobs.
- Automatically send LinkedIn messages.
- Commit `.career/` artifacts to git.
- Claim that a live market scan is exhaustive.

The skill may:

- Read publicly visible LinkedIn profile content from a user-provided URL.
- Ask the user to paste LinkedIn sections if public reading fails.
- Read resume / portfolio evidence already present in this repository.
- Search public job information.
- Analyze user-provided job descriptions.
- Generate LinkedIn edits, job shortlists, and application strategy.

## Failure Handling

### Public LinkedIn read fails

Continue and include:

```markdown
LinkedIn profile could not be read from the public URL.
Fallback used: resume-only LinkedIn optimization.
Recommended next input: paste your LinkedIn About and Experience sections.
```

### Live job search returns too few reliable results

Continue and include:

```markdown
Live job search returned too few reliable results.
Fallback used: search query pack + JD intake workflow.
Recommended next input: paste 5-10 job descriptions or links.
```

### External skill unavailable

Continue and include:

```markdown
External skill unavailable: <skill-name>
Fallback used: built-in checklist and prompts.
```

### Required details are missing

Continue with assumptions and include:

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

## Suggested Files

```text
.claude/
  skills/
    career-pipeline/
      SKILL.md
      references/
        output-template.md
        linkedin-checklist.md
        job-search-queries.md
```

### `SKILL.md`

Defines the trigger conditions, arguments, workflow phases, privacy boundaries, fallback rules, and final output requirements.

### `references/output-template.md`

Holds the Markdown strategy pack template so output remains consistent between runs.

### `references/linkedin-checklist.md`

Holds LinkedIn optimization checks for Headline, About, Experience, Skills, Featured, Projects, metrics, and recruiter searchability.

### `references/job-search-queries.md`

Holds Mainland China and Hong Kong AI/Agent job search query templates, including examples such as:

```text
site:linkedin.com/jobs "AI Agent Engineer" "Hong Kong"
site:linkedin.com/jobs "LLM Engineer" 香港
site:zhipin.com "AI Agent" "大模型应用"
site:liepin.com "智能体" "LLM"
site:jobsdb.com "GenAI Engineer" "Hong Kong"
```

## Acceptance Criteria

1. `/career-pipeline` is available as a Claude Skill / slash command.
2. It supports a public LinkedIn URL input.
3. It defaults to AI/Agent engineering roles.
4. It defaults to Mainland China and Hong Kong.
5. It outputs a complete Markdown strategy pack.
6. LinkedIn read failure still produces resume-only LinkedIn optimization.
7. Weak job search results still produce search queries and a JD intake next step.
8. It does not auto-apply or send messages.
9. `.career/` is git-ignored.
10. The skill documentation clearly states privacy boundaries and fallback behavior.

## Manual Test Plan

### Test 1 — Resume-only fallback

```text
/career-pipeline --no-linkedin
```

Expected:

- Produces LinkedIn optimization recommendations.
- Produces a target role profile.
- Does not fail because LinkedIn is absent.
- States that LinkedIn was not read.

### Test 2 — Public LinkedIn URL

```text
/career-pipeline https://www.linkedin.com/in/<profile>
```

Expected:

- Attempts public LinkedIn reading.
- If reading fails, states the fallback clearly.
- Produces a complete strategy pack.

### Test 3 — Pasted JD

```text
/career-pipeline --job "<paste JD>"
```

Expected:

- Produces role-specific fit analysis.
- Assigns a P0/P1/P2/P3 priority.
- Gives a role-specific application strategy.

## Non-goals for V1

- No browser automation.
- No account login.
- No private LinkedIn scraping.
- No automatic applications.
- No automatic outreach messages.
- No public web app UI.
- No persistent database for job tracking.

These can be reconsidered only after the strategy-pack workflow is stable and after the user explicitly approves a separate design.
