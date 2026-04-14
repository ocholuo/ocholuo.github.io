---
title: LLMApps - 养安全资产：用 LLM-KB 方法论驱动代码安全扫描器
date: 2026-04-13 12:00:00 -0400
description: Apply the "cultivate research assets" methodology to code security scanners and PR review — turning one-off findings into a compounding security knowledge base.
categories: [51AI, LLMApps]
tags: [AI, LLM, SecurityScanner, SAST, CodeReview, PRScanner, KnowledgeBase, DevSecOps]
---

# 养安全资产：用 LLM-KB 方法论驱动代码安全扫描器

**Table of contents:**

- [养安全资产：用 LLM-KB 方法论驱动代码安全扫描器](#养安全资产用-llm-kb-方法论驱动代码安全扫描器)
  - [The Core Problem](#the-core-problem)
  - [只做扫描 vs 养安全资产](#只做扫描-vs-养安全资产)
  - [5-Layer Framework Applied to Security Scanning](#5-layer-framework-applied-to-security-scanning)
    - [信息层 — Raw Scanner Output](#信息层--raw-scanner-output)
    - [论据层 — Evidence \& Triage](#论据层--evidence--triage)
    - [验证层 — Validation \& Trend Analysis](#验证层--validation--trend-analysis)
    - [执行层 — Remediation Playbook](#执行层--remediation-playbook)
    - [复盘层 — Retrospective](#复盘层--retrospective)
  - [Wiki Structure for a Security Scanning KB](#wiki-structure-for-a-security-scanning-kb)
    - [Per-Project Pages](#per-project-pages)
    - [Organization-Wide Pages](#organization-wide-pages)
  - [Ingest / Query / Lint Applied to Scanning](#ingest--query--lint-applied-to-scanning)
    - [Ingest (new scan results arrive)](#ingest-new-scan-results-arrive)
    - [Query (developer asks: "is this a real finding?")](#query-developer-asks-is-this-a-real-finding)
    - [Lint (weekly health check)](#lint-weekly-health-check)
  - [Practical Example: PR Scanner Workflow](#practical-example-pr-scanner-workflow)
  - [Key Takeaway](#key-takeaway)

---

## The Core Problem

Most teams run a scanner and process findings in isolation:

1. Scanner fires → developer sees alert → fix or dismiss → PR merges → done
2. Next PR: same pattern appears again
3. Same false positives misfire on every run
4. No memory of why a previous suppression was accepted
5. Onboarding a new project: start from zero

**The scanner produces information. It never produces knowledge.**

> 不要只做扫描，要养安全资产。
> Don't just run scans — cultivate security assets.

---

## 只做扫描 vs 养安全资产

| 只做扫描                       | 养安全资产                                           |
| ------------------------------ | ---------------------------------------------------- |
| 扫出来一堆 findings，逐个处理  | 每个 finding 类型都有对应的模式页，处理有据可查      |
| 同一个漏洞模式反复出现         | 建模式页：为什么反复出现，系统性根因在哪里           |
| 误报太多，开发不再信任扫描器   | 维护 false-positive 日志，持续调整规则 calibration   |
| PR 合并了，结束                | 复盘页：这个 PR 引入了什么风险，有没有遗漏           |
| 换一个项目，从头来             | 打开 codebase 安全页，历史债、规则库、已知反模式全在 |
| 漏洞被利用了，"怎么没扫出来？" | 检查 finding 是被抑制了还是规则覆盖不了              |
| 扫描器升级，不知道哪些规则变了 | 有 scanner config 版本页，变更有记录                 |

---

## 5-Layer Framework Applied to Security Scanning

### 信息层 — Raw Scanner Output

**原始信息：只读，永久保存为证据。**

Raw inputs that flow in continuously:

- SAST findings (Semgrep, CodeQL, Bandit, Checkmarx)
- SCA findings (Dependabot, Snyk, OWASP Dependency-Check) — CVE + affected version
- Secrets detection (Gitleaks, TruffleHog) — leaked credentials, API keys
- IaC scanning (Checkov, tfsec) — misconfigured Terraform, Kubernetes manifests
- PR diffs + commit history + author context
- CVE feeds and vendor security advisories

**Storage pattern:** raw findings land in `inbox/scans/` — immutable, timestamped, never edited.

```markdown
wiki/
└── inbox/
    └── scans/
        ├── 2026-04-01-semgrep-myapp.json
        ├── 2026-04-01-snyk-dependencies.json
        └── 2026-04-13-pr-4821-findings.md
```

---

### 论据层 — Evidence & Triage

**为什么这是真实漏洞？为什么这是误报？证据有没有过期？**

For every finding type, a wiki page captures the reasoning:

| Question                                | Answer (filed in wiki)                                                                  |
| --------------------------------------- | --------------------------------------------------------------------------------------- |
| Is this exploitable in our context?     | Attack vector, authentication required, data sensitivity                                |
| Is this a known false positive pattern? | Why this rule misfires on our codebase (e.g., ORM escapes input that Semgrep can't see) |
| Has this pattern appeared before?       | Link to historical findings page                                                        |
| What's the business impact?             | Which service, which data class, blast radius                                           |
| Is the CVE score accurate for us?       | CVSS is generic — our exploitability may differ                                         |

**Example wiki page:** `pages/vuln-patterns/SQL-Injection-Django-ORM.md`

```markdown
## Summary
Django ORM parameterizes queries by default. Raw string interpolation into
`.raw()` or `.extra()` calls is still dangerous. Semgrep rule `python.django.security.audit.raw-query`
fires on both safe and unsafe uses — needs manual triage.

## False Positive Pattern
`Model.objects.raw("SELECT * FROM table WHERE id = %s", [user_id])` — SAFE (parameterized).
`Model.objects.raw(f"SELECT * FROM table WHERE id = {user_id}")` — REAL finding.

## Evidence
- 3 confirmed FPs in myapp (2026-01 to 2026-04), 1 confirmed TP (2025-11 incident)
```

---

### 验证层 — Validation & Trend Analysis

**历史统计、误报率追踪、规则效力分析。**

The wiki accumulates quantitative validation over time:

| Metric                           | What it tells you                                                 |
| -------------------------------- | ----------------------------------------------------------------- |
| **False positive rate per rule** | Which rules need calibration or suppression                       |
| **Finding recurrence rate**      | Which vuln patterns keep coming back (systemic, not one-off)      |
| **Mean time to fix by severity** | Are SLAs being met? Which teams lag?                              |
| **Regression rate**              | "Fixed" findings that reappear — indicates incomplete remediation |
| **Coverage gaps**                | Finding types that led to incidents but weren't caught by scanner |
| **Developer risk profile**       | Which codebases/teams generate which finding types                |

**Example trend page:** `pages/trends/SAST-Finding-Trends-2026.md`

```markdown
## Q1 2026 Findings Summary
- Total: 847 findings across 12 repos
- True positives: 312 (37%)
- False positives: 535 (63%) — top offenders: rule A (240), rule B (180)
- Recurrent patterns: XSS in template engine (appeared in 4 PRs), hardcoded secrets in test fixtures
- SLA breach: 2 critical findings open >24h (both in repo X — team notified)
```

---

### 执行层 — Remediation Playbook

**在哪里修、怎么修、什么情况下接受风险。**

The wiki maintains actionable, stack-specific fix playbooks:

```markdown
pages/playbooks/
├── fix-sql-injection-django.md
├── fix-ssrf-requests-python.md
├── fix-xss-react-dangerouslysetinnerhtml.md
├── fix-hardcoded-secrets-env-pattern.md
├── accept-risk-template.md        ← formal risk acceptance with expiry date
└── escalation-criteria.md         ← when to page the security team
```

**Each playbook page includes:**

- The vulnerable pattern (copy-paste recognizable)
- The safe replacement (copy-paste ready)
- Why the fix works (attack vector neutralized)
- Stack-specific gotchas ("in Django, also check `.extra()`")
- Acceptance criteria: what a correct fix looks like in PR review

**PR blocking criteria page** (execution rules):

```markdown
## Block PR
- Any secrets detection finding (zero tolerance)
- Critical CVSS ≥ 9.0 with public exploit
- Regression: previously fixed pattern reappearing

## Warn (merge allowed, ticket required)
- High CVSS 7.0–8.9, no public exploit
- Dependency with fix available

## Accept Risk (formal approval required, 90-day expiry)
- Low/medium finding in non-sensitive code path
- No fix available yet (zero-day, waiting on upstream)
```

---

### 复盘层 — Retrospective

**事后追踪：判断有没有失真，规则有没有漏洞。**

After every significant event, file a retrospective page:

**Post-incident retrospective:**
```markdown
## 2026-03-15 | SQL Injection in /api/search Endpoint

### What happened
Finding appeared in Semgrep output on 2025-11-02 PR.
Was suppressed as false positive by developer. Exploited 2026-03-14.

### Why it was missed
Suppression comment said "ORM handles this" — but this code path used .raw().
The false-positive pattern page for this rule did NOT cover .raw() calls.

### Knowledge update
- Updated: pages/vuln-patterns/SQL-Injection-Django-ORM.md — added .raw() section
- Updated: pages/playbooks/fix-sql-injection-django.md — added .raw() examples
- New rule: suppressions on sql-injection rules require security team sign-off
```

**Post-PR retrospective (weekly, sampled):**
```markdown
## 2026-04-07 | PR #4821 — auth-service refactor

### Findings summary: 3 warnings, 0 blocks
### Were findings correctly triaged? Yes — 2 confirmed FP, 1 correctly fixed
### Anything scanner missed? Manual review found: JWT expiry not validated in new endpoint
### Knowledge update: added JWT validation pattern to pages/vuln-patterns/JWT-Validation.md
```

---

## Wiki Structure for a Security Scanning KB

### Per-Project Pages

```markdown
pages/projects/<project-name>/
├── security-profile.md      # Tech stack, risky areas, known debt, scanner config
├── finding-history.md        # Chronological log of significant findings
├── false-positive-registry.md # Rules that consistently misfire + why
└── open-risks.md             # Accepted risks with expiry dates
```

**`security-profile.md` template:**
```markdown
## Stack
Python 3.11 / Django 4.2 / PostgreSQL / React 18

## Scanners Active
- Semgrep (rules: python.django, secrets, OWASP-top-10)
- Snyk SCA (block on critical, warn on high)
- Gitleaks (pre-commit + PR gate)

## Known Risky Areas
- /api/search — raw query construction (2 historical TPs)
- file upload handler — no MIME validation (ticket #3421)

## Security Debt
- 14 accepted-risk findings (see open-risks.md)
- Dependency: lodash 4.17.19 — CVE-2021-23337, no upgrade path yet
```

---

### Organization-Wide Pages

```markdown
pages/org-security/
├── vuln-patterns/            # One page per recurring vulnerability pattern
│   ├── SQL-Injection-Django-ORM.md
│   ├── SSRF-Requests-Python.md
│   └── XSS-React-Templates.md
├── playbooks/                # Stack-specific fix instructions
├── trends/                   # Quarterly finding trend summaries
├── scanner-config/           # Scanner rule sets, suppressions, thresholds
├── incidents/                # Post-incident retrospectives
└── developer-risk-profile.md # Which teams/repos generate which finding types
```

---

## Ingest / Query / Lint Applied to Scanning

### Ingest (new scan results arrive)

1. Read raw scanner output from `inbox/scans/`
2. Identify finding types → check if a vuln-pattern page exists
3. Update existing pattern page OR create new stub
4. Update false-positive registry if applicable
5. Update project `finding-history.md`
6. Append to `log.md`

### Query (developer asks: "is this a real finding?")

1. LLM reads `index.md` → finds relevant vuln-pattern page
2. Reads pattern page → synthesizes triage decision with citations
3. Files answer back: if it reveals a new FP sub-pattern, update the pattern page

### Lint (weekly health check)

1. Find accepted-risk entries past their expiry date → flag for re-review
2. Find vuln patterns mentioned in incidents but missing a pattern page → create stub
3. Find rules with >80% FP rate → flag for suppression or calibration
4. Find projects with no recent scan → flag as coverage gap
5. Append lint entry to `log.md`

---

## Practical Example: PR Scanner Workflow

**Without the KB (one-off):**
```markdown
PR #4821 opens →
  Semgrep fires: "SQL injection risk" →
  Developer: "looks like a FP, ORM handles this" →
  Suppression added →
  PR merges →
  Knowledge: zero
```

**With the KB (compounding):**
```markdown
PR #4821 opens →
  Semgrep fires: "SQL injection risk" →
  LLM checks: pages/vuln-patterns/SQL-Injection-Django-ORM.md →
  Pattern page says: ".raw() calls are NOT covered by ORM — check if this is .raw()" →
  Developer checks → it IS .raw() → real finding →
  Fix applied → PR merges →
  KB update: finding logged to myapp/finding-history.md →
  Pattern page updated with this PR as a confirmed TP example
```

The second time this pattern appears, the KB answers the triage question instantly — without re-deriving it from scratch.

---

## Key Takeaway

The scanner tells you **what** it found. The KB tells you **what it means**.

```markdown
Scanner output (信息层)
  → Triage reasoning (论据层)     ← where most teams stop
    → Trend validation (验证层)
      → Fix playbook (执行层)
        → Retrospective (复盘层)  ← where knowledge compounds
```

> **让安全判断从"每次重新想"变成"可追踪、可校验、可迭代"的系统。让安全认知可以复利。**
> Transform security decisions from "re-derive every time" into a trackable, verifiable, iterating system — where security knowledge compounds.

The same finding, reviewed the fifth time, should take 10 seconds — not 10 minutes.
That's the difference between running a scanner and building a security asset.
