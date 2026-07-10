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
