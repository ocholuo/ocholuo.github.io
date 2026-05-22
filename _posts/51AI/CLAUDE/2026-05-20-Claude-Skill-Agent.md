---
title: "LLM - Claude Skill vs Agent vs MCP"
date: 2026-05-20 11:11:11 -0400
categories: [51AI, CLAUDE]
tags: [AI, Claude, Skill, Agent, MCP, workflow, multi-agent]
math: false
toc: true
---

# Claude Skill vs Agent vs MCP

- [Claude Skill vs Agent vs MCP](#claude-skill-vs-agent-vs-mcp)
  - [Overview 概述](#overview-概述)
  - [概念定义 Concept Definitions](#概念定义-concept-definitions)
    - [Skill 技能](#skill-技能)
    - [Agent 代理](#agent-代理)
    - [MCP (Model Context Protocol)](#mcp-model-context-protocol)
  - [三层对比表 Three-Way Comparison](#三层对比表-three-way-comparison)
  - [用户场景 User Scenarios](#用户场景-user-scenarios)
    - [场景 1 — 只用 Skill：统一工作流 Scenario 1 — Skill only: standardize a workflow](#场景-1--只用-skill统一工作流-scenario-1--skill-only-standardize-a-workflow)
    - [场景 2 — 只用 Agent：大规模并行分析 Scenario 2 — Agent only: large-scale parallel analysis](#场景-2--只用-agent大规模并行分析-scenario-2--agent-only-large-scale-parallel-analysis)
    - [场景 3 — 只用 MCP：连接外部系统 Scenario 3 — MCP only: connect to an external system](#场景-3--只用-mcp连接外部系统-scenario-3--mcp-only-connect-to-an-external-system)
    - [场景 4 — Skill + Agent：专家编排并行子任务 Scenario 4 — Skill + Agent: expert orchestration of parallel subtasks](#场景-4--skill--agent专家编排并行子任务-scenario-4--skill--agent-expert-orchestration-of-parallel-subtasks)
    - [场景 5 — Skill + MCP：专业工作流使用外部工具 Scenario 5 — Skill + MCP: expert workflow using external tools](#场景-5--skill--mcp专业工作流使用外部工具-scenario-5--skill--mcp-expert-workflow-using-external-tools)
    - [场景 6 — Agent + MCP：子代理并行调用外部系统 Scenario 6 — Agent + MCP: subagents calling external systems in parallel](#场景-6--agent--mcp子代理并行调用外部系统-scenario-6--agent--mcp-subagents-calling-external-systems-in-parallel)
    - [场景 7 — 三者结合：全自动端到端安全扫描 Scenario 7 — All three: fully automated end-to-end security scan](#场景-7--三者结合全自动端到端安全扫描-scenario-7--all-three-fully-automated-end-to-end-security-scan)
  - [Agent vs 多个 Terminal Session Agent vs Multiple Terminal Sessions](#agent-vs-多个-terminal-session-agent-vs-multiple-terminal-sessions)
    - [相似之处 What They Share](#相似之处-what-they-share)
    - [核心差距：谁来协调 Core Difference: Who Coordinates](#核心差距谁来协调-core-difference-who-coordinates)
    - [更准确的类比 A Better Analogy](#更准确的类比-a-better-analogy)
    - [什么时候多开 Session 就够了 When Multiple Sessions Are Enough](#什么时候多开-session-就够了-when-multiple-sessions-are-enough)
    - [什么时候必须用 Agent When Agents Are Necessary](#什么时候必须用-agent-when-agents-are-necessary)
  - [Key Takeaways](#key-takeaways)
  - [References](#references)

---

## Overview 概述

在 Claude Code 生态中，有三种核心概念用于扩展 Claude 的能力，它们处于不同的层次，服务于不同的目的。

In the Claude Code ecosystem, three core concepts extend Claude's capabilities. Each operates at a different layer and serves a distinct purpose.

- **MCP**：给 Claude 一双手 — 连接外部系统，提供新能力
  **MCP**: gives Claude hands — connects to external systems, provides new capabilities

- **Skill 技能**：给 Claude 一本操作手册 — 告诉它如何高效完成特定工作流
  **Skill**: gives Claude an operating manual — tells it how to execute a workflow consistently

- **Agent 代理**：给 Claude 一支团队 — 并行运行多个独立的 Claude 子实例完成复杂任务
  **Agent**: gives Claude a team — runs multiple independent Claude sub-instances in parallel for complex tasks

---

## 概念定义 Concept Definitions

### Skill 技能

**技能**是一个存放在 `.claude/skills/` 目录下的 Markdown 文件（`SKILL.md`），通过 YAML 元数据中的 `description` 字段自动触发。技能在主 Claude 实例的同一上下文窗口中运行，提供工作流知识，而不增加新的系统能力。

A **Skill** is a Markdown file (`SKILL.md`) stored in `.claude/skills/`, auto-triggered by matching the `description` field against the user's request. It runs inside the main Claude instance's context window and provides workflow knowledge without adding new system capabilities.

- 触发方式 Triggering: `description` 字段关键词匹配 / description field keyword match
- 运行位置 Runs in: 主 Claude 上下文 / main Claude context window
- 编写方式 Authored in: Markdown，无需编程 / Markdown, no coding required
- 目的 Purpose: 让 Claude 的某类工作流始终一致、专业 / make a class of workflows consistent and expert

> **注意 Note:** 技能目录里可以有 `agents/` 子文件夹，但那只是存放子工作流指令文件的命名惯例，不是真正的进程。
> A skill directory may contain an `agents/` subfolder, but that is only a naming convention for sub-workflow instruction files — not real subprocesses.

---

### Agent 代理

**代理**（Subagent）是由主 Claude 通过 `Agent` 工具显式生成的一个全新的、独立的 Claude 子实例。每个 Agent 拥有自己的上下文窗口、工具访问权限，独立执行任务后将结果返回给编排它的主 Claude。多个 Agent 可以<font color=OrangeRed>并行运行</font>，这是处理大规模并发任务的关键能力。

An **Agent** (Subagent) is a brand-new, isolated Claude sub-instance explicitly spawned by the main Claude using the `Agent` tool. Each Agent has its own context window and tool access, executes a task independently, then returns a result to the orchestrating Claude. Multiple Agents can run <font color=OrangeRed>in parallel</font> — this is the key capability for large-scale concurrent work.

- 触发方式 Triggering: 主 Claude 显式调用 `Agent` 工具 / orchestrating Claude explicitly calls `Agent` tool
- 运行位置 Runs in: 独立上下文窗口（新 Claude 实例）/ isolated context window (new Claude instance)
- 编写方式 Authored in: 主 Claude 或技能中的编排逻辑 / orchestration logic in the main Claude or in a skill
- 目的 Purpose: 并行执行、任务隔离、分而治之 / parallel execution, task isolation, divide-and-conquer

---

### MCP (Model Context Protocol)

**MCP** 是一个基于 JSON-RPC 2.0 的开放协议，运行为独立的服务器进程。它向 Claude 暴露三种原语：工具（可调用函数）、资源（只读数据源）、提示模板。MCP 赋予 Claude 它本身不具备的外部能力，例如查询数据库、调用第三方 API、读写文件系统。

**MCP** is an open protocol (JSON-RPC 2.0) running as a separate server process. It exposes three primitives to Claude: Tools (callable functions), Resources (read-only data sources), and Prompts (pre-built templates). MCP gives Claude external capabilities it does not have natively — querying databases, calling third-party APIs, reading/writing file systems.

- 触发方式 Triggering: Claude 的工具调用机制 / Claude's tool-use mechanism
- 运行位置 Runs in: 独立服务器进程 / separate server process
- 编写方式 Authored in: Python、Node.js、Go 等 / Python, Node.js, Go, etc.
- 目的 Purpose: 连接 Claude 到外部系统 / connect Claude to external systems

---

## 三层对比表 Three-Way Comparison

| 维度 Dimension | Skill 技能 | Agent 代理 | MCP |
|---|---|---|---|
| 所处层级 Layer | 提示 / 指令层 Prompt / instruction | 执行 / 并发层 Execution / concurrency | 基础设施 / 连接层 Infrastructure / connectivity |
| 提供什么 Provides | 工作流知识 Workflow knowledge | 并行执行能力 Parallel execution | 新能力（工具、数据）New capabilities |
| 运行在哪 Runs in | 主上下文 Main context | 独立子上下文 Isolated sub-context | 独立服务器进程 Server process |
| 上下文共享 Context | 共享主上下文 Shares main context | 全新隔离上下文 Fresh isolated context | 在 Claude 上下文之外 External to context |
| 并行能力 Parallelism | 否 No | 是 Yes | N/A |
| 编写方式 Authored | Markdown | 编排逻辑 Orchestration logic | 编程语言 Programming language |
| 是否需要编程 Coding | 否 No | 取决于编排 Depends | 是 Yes |
| 独立工作 Works alone | 是 Yes | 是 Yes | 是 Yes |
| 触发机制 Triggering | description 字段 Field match | 显式调用 Explicit call | 工具调用机制 Tool-use |

---

## 用户场景 User Scenarios

### 场景 1 — 只用 Skill：统一工作流 Scenario 1 — Skill only: standardize a workflow

**情境 Situation:**
每次写 PR 描述，格式都不一样，团队审查效率低。

Every PR description looks different, slowing down code review.

**解决方案 Solution:**
创建 `pr-writer` 技能。每次说 "帮我写 PR 描述"，Claude 自动按团队模板（概述 → 变更类型 → 测试方式）生成规范内容。

Create a `pr-writer` skill. Every time the team says "write a PR description," Claude automatically follows the template (overview → change type → test plan).

**为什么不用 Agent / MCP Why not Agent/MCP:**
任务是单一的、顺序的，不需要并行，也不需要连接外部系统。

The task is single and sequential — no parallelism needed, no external system to connect.

---

### 场景 2 — 只用 Agent：大规模并行分析 Scenario 2 — Agent only: large-scale parallel analysis

**情境 Situation:**
一个代码仓库有 50 个文件，需要逐一检查是否有 SQL 注入漏洞。如果顺序执行，需要等很久。

A repo has 50 files, each needing SQL injection checks. Doing them sequentially takes too long.

**解决方案 Solution:**
主 Claude 把 50 个文件分成 10 组，同时生成 10 个子 Agent，每个 Agent 检查 5 个文件，最后主 Claude 汇总所有 Agent 的结果。

The main Claude splits 50 files into 10 groups, spawns 10 subagents simultaneously — each checks 5 files — then the main Claude aggregates all results.

**为什么不用 Skill / MCP Why not Skill/MCP:**
Skill 在主上下文中顺序运行，无法并行。MCP 提供工具，但不解决并发问题。

A skill runs sequentially in the main context — it cannot parallelize. MCP provides tools but doesn't solve concurrency.

---

### 场景 3 — 只用 MCP：连接外部系统 Scenario 3 — MCP only: connect to an external system

**情境 Situation:**
想让 Claude 能直接查询 Postgres 数据库，拉取报表数据。

The team wants Claude to query a Postgres database directly and pull report data.

**解决方案 Solution:**
搭建 Postgres MCP 服务器，暴露 `query_db` 工具。Claude 调用该工具执行 SQL，无需人工复制粘贴数据。

Set up a Postgres MCP server exposing a `query_db` tool. Claude calls the tool to run SQL — no manual copy-paste needed.

**为什么不用 Skill / Agent Why not Skill/Agent:**
Skill 和 Agent 都没有内置数据库连接能力，MCP 是唯一能赋予这种能力的层。

Neither skills nor agents have built-in database connectivity. MCP is the only layer that can grant this capability.

---

### 场景 4 — Skill + Agent：专家编排并行子任务 Scenario 4 — Skill + Agent: expert orchestration of parallel subtasks

**情境 Situation:**
安全审查工作流需要：读取每个模块的代码 → 按 OWASP 清单分析 → 汇总报告。模块很多，单线程太慢。

A security review workflow needs to: read each module → analyze against OWASP checklist → produce a consolidated report. Many modules, sequential is too slow.

**解决方案 Solution:**
创建 `security-reviewer` 技能，技能的工作流中编排多个 Agent：每个 Agent 负责一个模块，按技能内嵌的 OWASP 清单审查，完成后主 Claude 汇总所有发现。

Create a `security-reviewer` skill. The skill's workflow orchestrates multiple Agents: each Agent handles one module against the embedded OWASP checklist, then the main Claude consolidates all findings.

```
security-reviewer Skill
        ↓
为每个模块生成一个 Agent / Spawn one Agent per module
        ↓  ↓  ↓  ↓  ↓  (并行 parallel)
  [Agent A] [Agent B] [Agent C] [Agent D] [Agent E]
  模块1分析  模块2分析  模块3分析  模块4分析  模块5分析
        ↓
  主 Claude 汇总，生成最终安全报告
  Main Claude consolidates → final security report
```

---

### 场景 5 — Skill + MCP：专业工作流使用外部工具 Scenario 5 — Skill + MCP: expert workflow using external tools

**情境 Situation:**
已经有 GitHub MCP（可以调用 `create_pr`、`add_comment`），但 Claude 每次用这些工具的方式不一致，评论质量参差不齐。

GitHub MCP already exists (`create_pr`, `add_comment` tools). But Claude uses those tools inconsistently, producing variable-quality comments.

**解决方案 Solution:**
创建 `pr-review` 技能，内嵌标准化工作流：拉取 diff → 分类问题严重级别 → 按模板用 `add_comment` 写结构化评论。MCP 提供工具，Skill 提供使用这些工具的判断逻辑。

Create a `pr-review` skill with a standardized workflow: pull the diff → classify issue severity → write structured comments via `add_comment` following a template. MCP provides the tools; the Skill provides the judgment for using them.

---

### 场景 6 — Agent + MCP：子代理并行调用外部系统 Scenario 6 — Agent + MCP: subagents calling external systems in parallel

**情境 Situation:**
需要同时查询 5 个不同地区的数据库，每个数据库在不同的 MCP 服务器上，合并成一张全球报表。

5 regional databases (each on a different MCP server) need to be queried simultaneously and merged into a global report.

**解决方案 Solution:**
主 Claude 生成 5 个子 Agent，每个 Agent 连接对应地区的 MCP 服务器，查询后返回结果。主 Claude 合并 5 个结果。

The main Claude spawns 5 subagents — each connects to its region's MCP server, runs the query, returns the result. Main Claude merges all 5 results.

---

### 场景 7 — 三者结合：全自动端到端安全扫描 Scenario 7 — All three: fully automated end-to-end security scan

**情境 Situation:**
一个完整的仓库安全扫描：需要从 GitHub 拉代码、并行分析各模块、按标准工作流生成报告。

A full repo security scan: pull code from GitHub, analyze modules in parallel, generate a report following a standard workflow.

**解决方案 Solution:**

```
security-auto Skill (技能编排整个流程 / skill orchestrates the entire flow)
        ↓
为每个模块生成子 Agent / Spawn subagent per module
        ↓       ↓       ↓
  [Agent A]  [Agent B]  [Agent C]   (并行 parallel)
      ↓           ↓          ↓
  GitHub MCP  GitHub MCP  GitHub MCP  → 拉取模块代码 / pull module code
  SAST MCP    SAST MCP    SAST MCP    → 运行静态扫描 / run static analysis
      ↓           ↓          ↓
   返回发现 Return findings
        ↓
  主 Claude 汇总 / Main Claude consolidates
        ↓
  GitHub MCP create_pr → 提交安全报告 PR / submit security report PR
```

技能提供标准化工作流；Agent 提供并行执行；MCP 提供 GitHub 和扫描工具的访问权限。

The Skill provides the standardized workflow. Agents provide parallel execution. MCP provides access to GitHub and the SAST scanner.

---

## Agent vs 多个 Terminal Session Agent vs Multiple Terminal Sessions

这是一个很常见的认知误区：多开几个 Claude Code 终端窗口，不就和用 Agent 一样了吗？

A common misconception: opening multiple Claude Code terminal sessions does the same thing as using Agents. The conceptual similarity is real — but the operational difference is significant.

### 相似之处 What They Share

- 两者都是多个独立的 Claude 实例，各自有独立的上下文窗口
  Both involve multiple independent Claude instances, each with its own context window
- 两者都可以同时处理不同的任务
  Both can handle different tasks simultaneously

### 核心差距：谁来协调 Core Difference: Who Coordinates

| | 多个 Terminal Session | Agent 子代理 |
|---|---|---|
| 协调者 Coordinator | 你（人工）You (manual) | 主 Claude（程序化）Orchestrating Claude (programmatic) |
| 规模上限 Scale limit | ~5 个（人的注意力有限）~5 (human attention is the bottleneck) | 50+ 个（程序无此限制）50+ (no programmatic limit) |
| 结果汇总 Result aggregation | 手动复制粘贴 Manual copy-paste | 自动回流给主 Claude Automatically returned to orchestrator |
| 条件逻辑 Conditional logic | 你看结果再决定下一步 You decide next step after reading results | 主 Claude 自动分支、重试、组合 Orchestrator auto-branches, retries, combines |
| 嵌入工作流 Embeddable in workflow | 否 No | 是（Skill 可编排 Agent）Yes (Skills can orchestrate Agents) |
| 会话生命周期 Session lifecycle | 持续存在直到手动关闭 Persists until manually closed | 任务完成即结束（短暂）Ephemeral — ends when task is done |
| 交互模式 Interaction mode | 多轮对话 Multi-turn conversation | 单次任务 → 返回结果 Single task → return result |

### 更准确的类比 A Better Analogy

多个 terminal session = 你自己当项目经理，挨个打电话给几个外包，等对方回复，自己汇总报告。

Multiple terminal sessions = you acting as project manager — calling each contractor individually, waiting for replies, writing the summary report yourself.

Agent = 你雇了一个项目经理（主 Claude），它自动派活、追踪进度、收结果、写汇总，你只看最终输出。

Agents = you hired a project manager (the orchestrating Claude) — it assigns work, tracks progress, collects results, writes the summary. You only see the final output.

### 什么时候多开 Session 就够了 When Multiple Sessions Are Enough

如果满足以下所有条件，手动开多个 session 和用 Agent 的结果几乎一样：

If all of the following are true, multiple terminal sessions and Agents produce nearly identical results:

- 任务数量少（≤5 个）Task count is small (≤5)
- 任务之间相互独立，不需要结果汇总 Tasks are independent, no aggregation needed
- 不介意手动协调和复制结果 Manual coordination and copy-paste is acceptable
- 不需要条件逻辑（A 的结果决定是否执行 B）No conditional logic (A's result determines whether to run B)

### 什么时候必须用 Agent When Agents Are Necessary

- 需要并行处理 10 个以上的独立子任务 10+ independent subtasks need to run in parallel
- 结果需要自动汇总后再做决策 Results must be automatically aggregated before the next decision
- 任务编排有条件分支（基于中间结果动态派发更多任务）Orchestration has conditional branching (spawn more tasks based on intermediate results)
- 工作流需要嵌入 Skill 中自动触发 Workflow needs to be embedded in a Skill and triggered automatically

---

```
需要连接外部系统（数据库、API、文件系统）？
Need to connect to an external system (DB, API, filesystem)?
  → 用 MCP

任务是否可以被分解成多个独立的并行子任务？
Can the task be broken into independent parallel subtasks?
  → 用 Agent（可以在 Skill 内编排）
     Use Agent (can be orchestrated within a Skill)

需要 Claude 每次都用同一套专业流程处理某类工作？
Need Claude to follow the same expert process for a class of work every time?
  → 用 Skill

以上都有？
All of the above?
  → Skill 编排 Agent，Agent 调用 MCP
     Skill orchestrates Agents, Agents call MCP
```

---

## Key Takeaways

- **MCP** 是连接层，赋予 Claude 外部能力。MCP is the connectivity layer — gives Claude external capabilities.
- **Skill** 是指令层，嵌入领域专业知识，保证工作流一致。Skill is the instruction layer — embeds expertise and ensures workflow consistency.
- **Agent** 是执行层，用于并行和隔离。Agent is the execution layer — used for parallelism and isolation.
- 技能的 `agents/` 子文件夹只是命名惯例（存放子工作流 Markdown），不是真正的进程。The `agents/` subfolder inside a skill is only a naming convention for sub-workflow Markdown files — not real processes.
- 三者互补，最强大的系统将三者结合：Skill 编排 → Agent 并行 → MCP 连接。All three are complementary — the most powerful systems combine all three: Skill orchestrates → Agent parallelizes → MCP connects.

## References

- `_posts/51AI/CLAUDE/2023-04-24-Claude_skill.md` — Claude Skill internals
- `_posts/51AI/AIAttack/2021-08-11-MCPSecurity.md` — MCP security attack surface
- [Anthropic Claude Code Docs](https://docs.anthropic.com/claude-code)
