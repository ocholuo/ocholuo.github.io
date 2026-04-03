---
title: LLM - Claude Skill
date: 2023-04-24 11:11:11 -0400
description:
categories: [51AI, CNN]
# img: /assets/img/sample/rabbit.png
tags: [AI, ML, CNN]
---

# ALLM - Claude Skill

- [ALLM - Claude Skill](#allm---claude-skill)
  - [什么是技能 (Skill)？](#什么是技能-skill)
  - [技术要求与规范](#技术要求与规范)
    - [命名限制](#命名限制)
    - [File structure](#file-structure)
    - [YAML 元数据示例](#yaml-元数据示例)
  - [测试与优化](#测试与优化)
    - [Quantitative metrics](#quantitative-metrics)
    - [Qualitative metrics](#qualitative-metrics)
  - [Common skill use case categories](#common-skill-use-case-categories)
    - [Category 1: Document \& Asset Creation](#category-1-document--asset-creation)
    - [Category 2: Workflow Automation](#category-2-workflow-automation)
    - [Category 3: MCP Enhancement](#category-3-mcp-enhancement)
  - [Writing effective skills](#writing-effective-skills)
    - [The description field](#the-description-field)
    - [The main instructions](#the-main-instructions)
  - [Testing and iteration](#testing-and-iteration)
  - [Skill Structure](#skill-structure)
  - [agents](#agents)
  - [commands](#commands)
  - [scripts](#scripts)
  - [references](#references)
  - [assets](#assets)

ref:

- https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf

---

## 什么是技能 (Skill)？

- 一个“技能”是一个包含特定文件的文件夹，结构如下：
  - SKILL.md (必须)： 使用 Markdown 编写的核心指令，包含 YAML 元数据。
  - scripts/ (可选)： 可执行的代码（如 Python, Bash），用于处理数据或验证。
  - references/ (可选)： 供 Claude 按需读取的参考文档。
  - assets/ (可选)： 模板、图标或静态资源。

- 设计原则：渐进式披露 (Progressive Disclosure)

- 为了节省 Token 并保持高效，技能采用三层加载机制：
  - 第一层 (YAML 元数据)： 始终加载，让 Claude 知道什么时候该用这个技能。
  - 第二层 (SKILL.md 正文)： 仅在任务相关时加载，提供详细指令。
  - 第三层 (关联文件)： 仅在 Claude 认为需要时才会去读取 references/ 中的文件。

- most powerful ways to customize Claude for your specific needs.
- Instead of re-explaining your preferences, processes, and domain expertise in every conversation, skills let you teach Claude once and benefit every time.
- Skills are powerful when you have repeatable workflows: generating frontend designs from specs, conducting research with consistent methodology, creating documents that follow your team's style guide, or orchestrating multi-step processes.

With skills:

- Pre-built workflows activate automatically when needed
- Consistent, reliable tool usage
- Best practices embedded in every interaction
- Lower learning curve for your integration

技能与 MCP 的关系

- 如果你已经有了 MCP (Model Context Protocol) 服务器，技能就是它的“大脑”。
- MCP (连接性)： 提供了厨房和工具（如连接 Notion, GitHub 的能力）。
- 技能 (知识)： 提供了菜谱（教 Claude 如何高效、规范地使用这些工具）。

## 技术要求与规范

Core design principles:

- Progressive Disclosure
  - Skills use a three-level system:
    - First level (YAML frontmatter): Always loaded in Claude's system prompt. Provides just enough information for Claude to know when each skill should be used without loading all of it into context.
    - Second level (SKILL.md body): Loaded when Claude thinks the skill is relevant to the current task. Contains the full instructions and guidance.
    - Third level (Linked files): Additional files bundled within the skill directory that Claude can choose to navigate and discover only as needed. This progressive disclosure minimizes token usage while maintaining specialized expertise.

- Composability
  - Claude can load multiple skills simultaneously. Your skill should work well alongside others, not assume it's the only capability available.

- Portability
  - Skills work identically across Claude.ai, Claude Code, and API. Create a skill once and it works across all surfaces without modification, provided the environment supports any dependencies the skill requires.

### 命名限制

- 文件夹命名： 必须使用 kebab-case（如 my-new-skill），不能有空格、大写或下划线。
- SKILL.md： 文件名必须完全匹配，区分大小写。

### File structure

```bash
your-skill-name/
├── SKILL.md # Required - main skill file
├── scripts/ # Optional - executable code
│ ├── process_data.py # Example
│ └── validate.sh # Example
├── references/ # Optional - documentation
│ ├── api-guide.md # Example
│ └── examples/ # Example
└── assets/ # Optional - templates, etc.
  └── report-template.md # Example
```

### YAML 元数据示例

这是 SKILL.md 的开头，至关重要：

```YAML
---
name: project-setup
description: 用于初始化项目。当用户说“开始新项目”或“设置工作区”时触发。
---
```

## 测试与优化

### Quantitative metrics

- 触发测试 Triggering tests
  - Skill triggers on 90% of relevant queries
  - 确保它在相关请求时能自动加载，而在无关请求（如问天气）时不触发。
  - How to measure: Run 10-20 test queries that should trigger your skill. Track how many times it loads automatically vs. requires explicit invocation.

- 性能对比
  - 对比使用技能前后的对话轮数和 Token 消耗（通常技能可以大幅减少沟通成本）。
  - Completes workflow in X tool calls
  - How to measure: Compare the same task with and without the skill enabled.
  - Count tool calls and total tokens consumed.

- 迭代逻辑
  - 如果 Claude 经常“偷懒”或出错，建议将逻辑写成 Python 脚本 放在 scripts/ 中，因为代码比自然语言更具有确定性。
  - 0 failed API calls per workflow
  - How to measure: Monitor MCP server logs during test runs. Track retry rates and error codes.

### Qualitative metrics

- Users don't need to prompt Claude about next steps
  - How to assess: During testing, note how often you need to redirect or clarify. Ask beta users for feedback.

- Workflows complete without user correction
  - How to assess: Run the same request 3-5 times. Compare outputs for structural consistency and quality.

- Consistent results across sessions
  - How to assess: Can a new user accomplish the task on first try with minimal guidance?

---

## Common skill use case categories

### Category 1: Document & Asset Creation

Key techniques:

- Embedded style guides and brand standards
- Template structures for consistent output
- Quality checklists before finalizing
- No external tools required - uses Claude's built-in capabilities

### Category 2: Workflow Automation

Key techniques:

- Step-by-step workflow with validation gates
- Templates for common structures
- Built-in review and improvement suggestions
- Iterative refinement loops

### Category 3: MCP Enhancement

Key techniques:

- Coordinates multiple MCP calls in sequence
- Embeds domain expertise
- Provides context users would otherwise need to specify
- Error handling for common MCP issues

---

## Writing effective skills

### The description field

Structure: `[What it does] + [When to use it] + [Key capabilities]`

```bash
# Good - specific and actionable
description: Analyzes Figma design files and generates
developer handoff documentation. Use when user uploads .fig
files, asks for "design specs", "component documentation", or
"design-to-code handoff".

# Good - includes trigger phrases
description: Manages Linear project workflows including sprint
planning, task creation, and status tracking. Use when user
mentions "sprint", "Linear tasks", "project planning", or asks
to "create tickets".

# Good - clear value proposition
description: End-to-end customer onboarding workflow for
PayFlow. Handles account creation, payment setup, and
subscription management. Use when user says "onboard new
customer", "set up subscription", or "create PayFlow account".

# Too vague
description: Helps with projects.

# Missing triggers
description: Creates sophisticated multi-page documentation
systems.

# Too technical, no user triggers
description: Implements the Project entity model with
hierarchical relationships.
```

### The main instructions

Recommended structure:

```bash
---
name: your-skill
description: [--.]
---

# Your Skill Name

## Instructions

### Step 1: [First Major Step]
Clear explanation of what happens.

Example:
python scripts/fetch_data.py --project-id PROJECT_ID
Expected output: [describe what success looks like]

# Example 1: [common scenario]
User says: "Set up a new marketing campaign"
Actions:
1. Fetch existing campaigns via MCP
2. Create new campaign with provided parameters
Result: Campaign created with confirmation link
(Add more examples as needed)

#(Include error handling)
## Common Issues
### MCP Connection Failed
If you see "Connection refused":
1. Verify MCP server is running: Check Settings > Extensions
2. Confirm API key is valid
3. Try reconnecting: Settings > Extensions > [Your Service] > Reconnect

#(Reference bundled resources clearly)
Before writing queries, consult `references/api-patterns.md` for:
- Rate limiting guidance
- Pagination patterns
- Error codes and handling
```

Use progressive disclosure

---

## Testing and iteration

Skills can be tested at varying levels of rigor depending on your needs:

- Manual testing in Claude.ai
  - Run queries directly and observe behavior.
  - Fast iteration, no setup required.
- Scripted testing in Claude Code
  - Automate test cases for repeatable validation across changes.
- Programmatic testing via skills API
  - Build evaluation suites that run systematically against defined test sets.

---

## Skill Structure

```bash
SKILL.md             ← router + workflow
  agents/
    abc_worker.md    ← agent
  commands/
    a.md         ← /a command
    b.md         ← /b command
  references/          ← domain knowledge only
  scripts/             ← deterministic code
  assets/              ← report template


  ┌─────────────┬──────────────────────────────────┬─────────────────────────────────┬───────────────────────────────────────┐
  │   Folder    │           Content type           │       How Claude uses it        │                 When                  │
  ├─────────────┼──────────────────────────────────┼─────────────────────────────────┼───────────────────────────────────────┤
  │ scripts/    │ Python/bash executables          │ Runs via Bash tool              │ When SKILL.md says to run it          │
  ├─────────────┼──────────────────────────────────┼─────────────────────────────────┼───────────────────────────────────────┤
  │ references/ │ Knowledge docs (Markdown)        │ Reads into context              │ When SKILL.md says to load it         │
  ├─────────────┼──────────────────────────────────┼─────────────────────────────────┼───────────────────────────────────────┤
  │ agents/     │ Workflow instructions (Markdown) │ Reads and follows               │ When SKILL.md routes to it            │
  ├─────────────┼──────────────────────────────────┼─────────────────────────────────┼───────────────────────────────────────┤
  │ commands/   │ Slash command definitions        │ Reads + $ARGUMENTS substitution │ On /command invocation or when routed │
  ├─────────────┼──────────────────────────────────┼─────────────────────────────────┼───────────────────────────────────────┤
  │ assets/     │ Templates/static files           │ Reads to produce output         │ When generating a report/deliverable  │
  └─────────────┴──────────────────────────────────┴─────────────────────────────────┴───────────────────────────────────────┘

```

- Claude is the runtime. There's no framework executing these files
- Claude reads the instructions and decides what to do.
- Every folder is just an organizational convention that SKILL.md references explicitly.

## agents

- Instructions for a specialized persona or sub-workflow

- a convention the skill introduced (not a built-in Claude Code concept). These files contain detailed instructions for a distinct mode of operation — essentially a self-contained workflow that's too large or specialized to put in SKILL.md itself.

- The difference from references/:
  - references/ = facts and knowledge (what is a? what's b?)
  - agents/ = behavioral instructions (here's how to execute an action that do .....)

- When SKILL.md routes to agents/abc_worker.md, Claude reads the whole file and essentially becomes worker for that session, following its phases, its output format, its invocation modes.

## commands

- Slash command definitions

- When you type `/a xxxx` in a Claude Code session, Claude Code finds `commands/a.md`, substitutes `xxxx` for `$ARGUMENTS`, and executes the instructions.

- without slash command invocation, these files are just like agents/ files, SKILL.md can tell Claude to read them when routing.

## scripts

- Executable code Claude runs as shell commands
- These are Python scripts, bash scripts, etc. that Claude runs with the Bash tool.
- Claude doesn't need to read them to use them — it just executes them.

```bash
# Claude runs this, it produces output, Claude uses the output
python BASE_DIR/scripts/check_secrets.py myfile.py --save
```

- Use scripts when the task is `deterministic and repetitive`
- things where you want consistent behavior every time, not Claude reasoning through it fresh.
  - math is better by a script than by an LLM guessing.

## references

- Domain knowledge Claude reads on demand

- Markdown files with information Claude loads into its context when it needs them.

- Think of them as reference manuals, don't read the entire Python docs before writing code, you look up the specific section you need.

- SKILL.md says when to load each one:
  - If Phase 2 ... Load references/aaaa.md → xxx section

- Claude then reads that file and uses the knowledge.
  - This keeps context lean, don't load the entire reference for a call that has no related info.

## assets

- Output templates
- Static files used to produce output — report templates, HTML templates, icons.
- Claude reads these when generating a deliverable so the output has consistent structure.

```bash
# ---
User says "create my app at localhost:3000"
      ↓
SKILL.md triggers (description matches)
      ↓
SKILL.md routing logic → "read commands/create.md"
      ↓
Claude reads commands/create.md, $ARGUMENTS = "localhost:3000"
      ↓
Claude follows create phases, runs curl commands via Bash tool
      ↓
Create a web → offers "create doc?" → reads commands/doc-creator.md

# ---
User says "check this Dashboard.tsx for accessibility issues"
        ↓
SKILL.md triggers
(description: "audit component for a11y / accessibility / WCAG issues")
        ↓
SKILL.md routing → component audit workflow (stays in SKILL.md)
        ↓
Phase 2 reads Dashboard.tsx, finds:
    - <img> missing alt attribute  → WCAG 1.1.1
    - low-contrast text (#888 on white) → WCAG 1.4.3
    - button with no visible label → WCAG 4.1.2
        ↓
SKILL.md says "load references/wcag-criteria.md → 1.1.1, 1.4.3, 4.1.2"
        ↓
Claude reads those three sections, gets:
    - conformance level (A vs AA)
    - failure conditions
    - sufficient techniques (e.g. use aria-label, ensure 4.5:1 contrast ratio)
        ↓
Phase 2c: runs `node scripts/contrast_check.js Dashboard.tsx`
(deterministic color math — Claude executes, doesn't re-read the script)
        ↓
Phase 4: reads assets/a11y-report-template.md, writes report
```
