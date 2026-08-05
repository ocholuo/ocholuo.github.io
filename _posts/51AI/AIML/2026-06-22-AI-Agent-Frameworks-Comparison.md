---
title: "Meow's AIML - AI Agent Frameworks Comparison / AI Agent 主流框架对比"
date: 2026-06-22 11:11:11 -0400
categories: [51AI, AIML]
tags: [AI, agent, LLM, AutoGPT, LangGraph, Dify, CrewAI, AutoGen, framework, multi-agent, workflow]
math: false
toc: true
image:
---

# AI Agent Frameworks Comparison / AI Agent 主流框架对比

- [AI Agent Frameworks Comparison / AI Agent 主流框架对比](#ai-agent-frameworks-comparison--ai-agent-主流框架对比)
  - [Overview 概述](#overview-概述)
  - [1. Workflow 与 Agent 的区别 / Workflow vs Agent](#1-workflow-与-agent-的区别--workflow-vs-agent)
  - [2. 何时使用 Agent 框架 / When to Use an Agent Framework](#2-何时使用-agent-框架--when-to-use-an-agent-framework)
  - [3. 各框架对比总结 / Framework Comparison](#3-各框架对比总结--framework-comparison)
  - [4. AutoGPT](#4-autogpt)
  - [5. LangGraph](#5-langgraph)
  - [6. Dify](#6-dify)
  - [7. CrewAI](#7-crewai)
  - [8. AutoGen](#8-autogen)
  - [Key Takeaways 核心要点](#key-takeaways-核心要点)
  - [References](#references)

---

## Overview 概述

Agent 框架选择是 AI 应用落地的核心决策之一。本文对比五种主流框架：AutoGPT、LangGraph、Dify、CrewAI 和 AutoGen，帮助开发者快速判断适合自身场景的技术路径。

Choosing an Agent framework is a core architectural decision when deploying AI applications. This note compares five mainstream frameworks — AutoGPT, LangGraph, Dify, CrewAI, and AutoGen — to help developers quickly identify the right tool for their scenario.

![Agent 主流框架介绍 — 五种框架概览](./assets/img/post/agent-frameworks-overview-title.jpg)

---

## 1. Workflow 与 Agent 的区别 / Workflow vs Agent

![Workflow 与 Agent 的区别及框架选择](./assets/img/post/agent-frameworks-workflow-vs-agent-selection.jpg)

| 类型         | 定义                                                      |
| ------------ | --------------------------------------------------------- |
| **Workflow** | 在预定义的链路中加入 LLM，或由 LLM 控制预定义流程中的流转 |
| **Agent**    | LLM 根据环境自行选取工具并执行，具备反馈循环              |

Workflow 分为三类模式：

- **Prompt Chaining** — 顺序调用 LLM，每步输出作为下一步输入
- **Orchestrator-Worker / Evaluator-optimizer / Routing** — 由 LLM 在预定义路径中控制流转
- **Agent** — LLM call → action → Tool → feedback，LLM 自主决策

The key distinction: in a Workflow the control flow is predetermined; in an Agent, the LLM autonomously selects tools and decides the next action based on environment feedback.

---

## 2. 何时使用 Agent 框架 / When to Use an Agent Framework

![Agent 框架解决的核心问题 — 以客服场景为例](./assets/img/post/agent-frameworks-when-to-use-agent-vs-workflow.jpg)

只要"问题不可完全穷举、要跨多系统查证、并且需要在对话中澄清/协商/决策"，就更应该用 Agent 框架，而不是纯 Workflow。

Use an Agent framework (not pure Workflow) when:

- The problem space cannot be fully enumerated in advance
- Cross-system evidence gathering is required
- The solution requires in-conversation clarification, negotiation, or decision-making

**纯 Workflow 的局限 / Limitations of pure Workflow:**

Workflow（Dify 可视化编排、LangGraph 状态机）非常适合步骤确定 + 条件有限的流程，例如：

1. 查询订单 → 格式化答复
2. 退货 → 生成标签 → 发通知
3. FAQ 检索 → 返回片段

一旦进入长尾问题，Workflow 就会遇到"分支爆炸"。Agent 框架通过动态规划与调用工具解决这个问题。

**Agent 框架典型场景示例（客服）/ Agent in action (customer service):**

用户场景：用户说"我 8 月 1 号下的单今天还没到，收件地址其实要换，而且我被重复扣费了。"

| 步骤               | Agent 行为                                                                     |
| ------------------ | ------------------------------------------------------------------------------ |
| 1. 意图识别 + 澄清 | Planner Agent 拆出多意图，先问关键信息（订单号/新地址/扣费凭证）               |
| 2. 跨系统取证      | OMS/物流工具查轨迹与 SLA；计费/支付工具核对重复扣款；CRM 看 VIP 状态           |
| 3. 政策推理与合规  | Policy/Critic Agent 套用假期延误 + VIP + 改址组合条款，评估补偿区间            |
| 4. 方案生成与协商  | 提出可行方案并按用户反馈实时调整                                               |
| 5. 执行与闭环      | 调用工单/票据工具落账，写入 CRM 备注；若任一步失败，自动选择备选策略或升级人工 |

---

## 3. 各框架对比总结 / Framework Comparison

![五种框架对比 — Venn 图、排名与汇总表](./assets/img/post/agent-frameworks-comparison-venn-rankings.jpg)

**定位 Venn 图：**

- **纯 AI Agent**：AutoGPT（高自主性，LLM 驱动）
- **交叉区（Agent + Workflow）**：AutoGen、LangGraph、CrewAI
- **纯 Workflow**：Dify（低代码可视化，偏确定性流程）

**内置工具数排名（低→高）：**
AutoGPT / AutoGen < Dify < LangGraph / CrewAI

**灵活性排名（低→高）：**
AutoGPT < Dify < CrewAI / LangGraph / AutoGen

**汇总对比表 / Summary Table:**

| Agent 框架    | 适合场景                                           | 优势                                                       | 不足                                                           |
| ------------- | -------------------------------------------------- | ---------------------------------------------------------- | -------------------------------------------------------------- |
| **AutoGPT**   | 各类通用任务                                       | 完全自主执行；任务分解与多步推理；记忆和持续学习           | 复杂任务场景前后文一致性问题；高成本和效率问题；操作可控性较低 |
| **LangGraph** | 可明确拆解任务步骤                                 | 灵活的多步骤控制；原生支持短长期记忆；易调试和全链路可观测 | 自主性有限；Agent 模式不成熟                                   |
| **Dify**      | 可明确拆解任务步骤                                 | 低代码，易用性与低门槛；强大的模型与工具能力               | 功能广而不精；需在简单和复杂场景之间找到平衡                   |
| **CrewAI**    | 任务步骤不固定，需让 Agent 自己探索                | 工具和生态集成；灵活性与深度定制                           | 特定功能支持有限（如代码沙盒）                                 |
| **AutoGen**   | 原生多代理支持；灵活的对话流程控制；可观察调试支持 | 微软开源；原生多 Agent；灵活对话控制                       | 社区生态尚处于起步阶段                                         |

---

## 4. AutoGPT

![AutoGPT 主要特点、优势与不足及使用示例](./assets/img/post/agent-autogpt-features-example.jpg)

**简介：** AutoGPT 是第一个爆火的自主 AI Agent 框架，提供一系列工具让用户构建和使用自治代理。功能涵盖代理创建模块"Forge"、性能评测基准 agbenchmark、排行榜以及易用的 UI 和 CLI 接口。

AutoGPT is the first viral autonomous AI Agent framework. It provides tools for building and using self-governing agents, covering agent creation (Forge), performance benchmarking (agbenchmark), a leaderboard, and both UI and CLI interfaces.

**主要特点：**

AutoGPT 支持"思考→行动→反馈→学习"的循环，让代理不断生成子任务并执行。拥有丰富的插件和工具接口，允许代理访问浏览器、文件系统、API 等资源，从而完成复杂的链式任务。

**典型应用场景：** 需要让 Agent 自动拆解目标并执行的任务，如市场调研、行程规划、代码编写等。

**优势 / Strengths:**

| 优势               | 说明                                                                                                |
| ------------------ | --------------------------------------------------------------------------------------------------- |
| 自主性与少人干预   | 只需给定最终目标，便能自主规划步骤并循环执行，无需逐步指导                                          |
| 任务分解与多步推理 | 内置 ReAct 机制，能将复杂目标拆分为可执行子任务并逐一完成，集成了文件操作、网络搜索、代码执行等能力 |
| 记忆机制与持续学习 | 结合短期与长期记忆模块，在长任务执行中能保留上下文，将每步的结果添加到记忆，并以此调整后续执行策略  |

**不足 / Weaknesses:**

| 不足               | 说明                                                                                                                                                                                                                     |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 对话和上下文一致性 | 随着任务执行步骤的增多，Agent 可能逐渐偏离原始目标，产生与任务无关的输出                                                                                                                                                 |
| 高成本和效率问题   | 每次决策都需要频繁调用大型模型 API；AutoGPT 采取链式探试的方法执行任务，相对于人类亲自主导的处理方式可能低效，一些简单任务由 AutoGPT 执行时间过长                                                                        |
| 操作可控性较低     | 由于用户只设定初始目标，过程中 Agent 的具体操作对用户不透明。可能无法搜索到相关信息或尝试执行不当操作而不自知；虽然 AutoGPT 提供了步骤执行前让用户确认的链路监控模式，但在开放的选链模式下，缺乏监控可能导致错误链条蔓延 |

**使用示例：** 基于 AutoGPT 让 Agent 帮写一篇介绍 AutoGPT 的文章，通过 CLI 配置 Agent 名称、角色以及目标后自动执行。

---

## 5. LangGraph

![LangGraph Graph 模式与预构建模式示意图及主要特点](./assets/img/post/agent-langgraph-graph-patterns-features.jpg)

![LangGraph 优势与不足及代码示例](./assets/img/post/agent-langgraph-pros-cons-code-example.jpg)

**简介：** LangGraph 是由 LangChain 团队推出的有状态、持久运行、多智能体应用的编排框架。核心将 Agent 建模成一个图（Graph）：每个节点是计算步骤（LLM 调用、工具函数、任意 Python 代码等），边控制流转（含条件与循环），并最终实现既定目标。

LangGraph, built by the LangChain team, is a stateful, persistent, multi-agent orchestration framework. It models agents as a graph where each node is a computation step (LLM call, tool function, or arbitrary Python code), and edges control flow — including conditionals and loops.

**多智能体拓扑模式：**

- **Custom** — 自定义有向图，灵活拓扑
- **Network** — 全连接网络，Agent 间可互相通信
- **Supervisor** — 主控 Agent 分配子任务给 Worker Agent

**主要特点：** 支持图式编排、可人工干预、可中断/续跑。LangGraph 可形成可控的分支/循环流程，可在每个节点中加入人工干预环节，适合需要人工审批/修订的业务场景，并且基于持久化状态可方便中断、续跑、回溯。

**典型应用场景：** 可明确拆解任务步骤的场景，如 RAG 类、文章生成、日程助手等。

**优势 / Strengths:**

| 优势                 | 说明                                                                                                                                                                                                                                    |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 灵活的多步骤流程控制 | 最大优势在于高度灵活的工作流编排能力，通过图结构的逻辑，使开发者可以针对特定需求定制非线性的执行路径，实现从对话流到复杂工具调用再到错误重试等各种流程                                                                                  |
| 共享状态与记忆       | 引入了共享 State（状态）的概念，在工作流的各个节点间持久共享输入和输出都都存储在状态中，后续节点能够访问先前步骤的信息，通过这种内存共享机制，Agent 可携带短期记忆（当前任务进展的记忆）以及通过外部数据库实现的长期记忆                |
| 易调试和高可观察性   | 采用显式的图结构，开发者可以方便地插入日志、检查点，观察数据在各节点的流动，并利用调试工具定位问题路径；LangChain 与 LangSmith 等监控/调试工具深度集成，能够对每次 LLM 调用、工具使用进行详尽的跟踪和可视化，帮助开发者迅速调调复杂链路 |

**不足 / Weaknesses:**

| 不足             | 说明                                                                                                                                                                                                                             |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 自主性有限       | LangGraph 强调的是由开发者显式控制的 Agent 流程（Workflow），在一定程度上限制了 Agent 的自主性                                                                                                                                   |
| 预构建模式不成熟 | 目前预构建模式内部组件对用户不透明，难以在框架外精确插入自定义逻辑或中间步骤；预构建模式缺乏某些特殊处理或并行执行多个任务的能力，预构建模式目前没有内置的重试、降级或显示机制，需要开发者在外部捕获并处理，否则对话中断或不一致 |

**代码示例 / Code Example:**

```python
def _build_workflow(self) -> StateGraph:
    """构建LangGraph工作流"""
    workflow = StateGraph(ArticleState)

    # 添加节点
    workflow.add_node("analyze_topic", self._analyze_topic)
    workflow.add_node("create_outline", self._create_outline)
    workflow.add_node("write_content", self._write_content)
    workflow.add_node("review_content", self._review_content)

    # 设置边
    workflow.set_entry_point("analyze_topic")
    workflow.add_edge("analyze_topic", "create_outline")
    workflow.add_edge("create_outline", "write_content")
    workflow.add_edge("write_content", "review_content")
    workflow.add_edge("review_content", END)
```

---

## 6. Dify

![Dify 主要特点、优势与不足及可视化 UI 示例](./assets/img/post/agent-dify-features-pros-cons-ui.jpg)

**简介：** Dify (Do It For You) 是一个开源的低代码平台，旨在简化大模型（LLM）驱动的 AI 应用开发与部署。它融合了"后端即服务（BaaS）"与 LLMOps 概念，提供涵盖模型接入、提示设计、知识库检索、智能代理、数据监控等在内的一站式解决方案。通过直观的可视化界面和预构建组件，开发者和非技术人员都可以快速构建如聊天机器人、内容生成、数据分析等各类生成式 AI 应用。

Dify is an open-source low-code platform that simplifies LLM-powered AI application development and deployment. It combines BaaS and LLMOps concepts, providing an all-in-one solution covering model integration, prompt design, knowledge base retrieval, intelligent agents, and data monitoring.

**主要特点：** 低代码、可视化工作流构建、检索增强生成（RAG）管道、开放工具市场。

**典型应用场景：** 可明确拆解任务步骤的场景，如 RAG 类、文章生成、日程助手等。

**优势 / Strengths:**

| 优势                     | 说明                                                                                                                                                                                                      |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 易用性与低门槛           | 最大亮点之一是上手非常简单，可视化操作界面让用户几乎不需要编程技能就能搭建 AI 应用；预构建的节点和模板减少了大量繁琐配置，几小时内即可完成过去需要数周开发的原型                                          |
| 强大的模型与工具集成能力 | Dify 生来强调"模型中立"和灵活扩展开箱即支持上百家模型提供商的上百种 LLM，涵盖 OpenAI、Anthropic、Mistral 以及各类本地运行模型等，在工具方面，涵盖了常见的网络服务和 AI 模型，可以借助外部能力完成复杂任务 |

**不足 / Weaknesses:**

| 不足               | 说明                                                                                                                                                  |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| 功能广而不精       | 某些专业领域的深度上可能比不上专门化工具，例如 Dify 内置了知识库 RAG 功能，但在复杂文档理解、细粒度检索参数方面不及专注于 RAG 的框架（如 RAGFlow 等） |
| "重量级"工具的取舍 | 如果只是做一个很简单的问答 Bot 或单一功能，用 Dify 会感觉"大材小用"；企业如果有很多特殊功能需求，往往也需要对 Dify 进行二次开发来满足                 |

---

## 7. CrewAI

![CrewAI 主要特点、优势与不足及代码示例](./assets/img/post/agent-crewai-features-pros-cons-code.jpg)

**简介：** CrewAI 是一个多智能体（multi-agent）编排框架，其核心理念是让多个具备特定角色的 AI 代理协同合作（组成"crew"团队）来完成复杂任务。每个代理被赋予特定的角色、目标和背景知识，通过相互分工与配合，自动地进行任务委派和问询，最终以团队形式完成用户交给的工作。

CrewAI is a multi-agent orchestration framework. Its core idea is to have multiple AI agents with specific roles collaborate as a "crew" to complete complex tasks. Each agent is assigned a role, goal, and background knowledge, enabling autonomous task delegation and inquiry.

**主要特点：** 多工具及生态集成、支持 Workflow 和 AI Agent 两种模式。

**典型应用场景：** 任务步骤不固定，需让 Agent 自己探索的场景。

**优势 / Strengths:**

| 优势             | 说明                                                                                                                                                                                                                                                                                                      |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 工具和生态集成   | CrewAI 起初借鉴并构建在 LangChain 生态之上，因而天然支持使用 LangChain 提供的大量工具集合（如搜索、数据库查询、API 接口等），同时 CrewAI 自身及社区提供了超过 40 种工具接口（包括常用的 LLM、云服务、数据库等）以供理直接使用                                                                             |
| 灵活性与深度定制 | 在 CrewAI 的高层模式下，依然保留了很大的灵活性，开发者可以填入定制每个代理的提示（prompt）、工具和内部行为，基至可以自定义低层级的代理模板和代理行为；CrewAI 支持同时结合自主代理（Crews）和精确流程（Flows）两种形式，允许在同一应用中既有自主探索的部分，也有确定顺序的流程，从而无缝融合自治与精确控制 |

**不足 / Weaknesses:** 特定功能支持有限，相较于某些专用框架（如代码沙盒），CrewAI 在特定能力上可能如何不够完善。

**代码示例 / Code Example:**

```yaml
researcher:
  role: >
    {topic} 资深研究员
  goal: >
    {topic} 领域内最新研究成果
  backstory: >
    你是一名资深研究员，擅长{topic}领域内的最新研究成果。
    你能够找到最相关的信息，并将其以清晰明了的方式呈现。

reporting_analyst:
  role: >
    {topic} 报告分析师
  goal: >
    {topic} 领域内最新研究成果
  backstory: >
    你是一名报告分析师，擅长{topic}领域内的最新研究成果。
    你能够将复杂的研究成果转化为清晰明了的报告，使其他人能够轻松理解和采用信息。
```

---

## 8. AutoGen

![AutoGen 主要特点、优势与不足及 Swarm 模式示例](./assets/img/post/agent-autogen-features-pros-cons-swarm-example.jpg)

**简介：** AutoGen 是微软开源的一个面向 Agentic AI（代理式人工智能）的编程框架，用于构建 AI 智能体并促进多个智能体协作完成复杂任务。AutoGen 支持事件驱动的分布式架构，具有良好的可扩展性和弹性，可用于搭建可自主行动或在人类监督下运行的多代理 AI 系统。

AutoGen is Microsoft's open-source programming framework for Agentic AI, used to build AI agents and facilitate multi-agent collaboration on complex tasks. It supports event-driven distributed architecture with high scalability and elasticity, suitable for both autonomous and human-supervised multi-agent systems.

**主要特点：** 微软开源、原生多 Agent 支持、灵活对话控制。

**优势 / Strengths:**

| 优势               | 说明                                                                                                                                                                                                                                                |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 原生多代理支持     | 作为一款专为多智能体协作设计的框架，AutoGen 天生支持多个 Agent 之间的通信与并行工作，它不拘泥于固定顺序，这意味着开发者可以实现高度灵活控制的对话流程：代理们可以灵活调用、并行运行、双向自由交流，甚至在人工干预下下达新规划                       |
| 灵活的对话流程控制 | AutoGen 采用异步消息驱动，代理之间的通信可以异步进行，不拘泥于固定顺序；这意味着开发者可以实现高度灵活控制的对话流程；代理们可以灵活调用、并行运行、双向自由交流，甚至在人工干预下下达新规划                                                        |
| 可观察性和调试工具 | 框架内置了可观察性和调试工具，AutoGen 提供消息跟踪、日志记录以及 OpenTelemetry 集成等功能，方便开发者监控代理间的交互过程、排查问题；此外，AutoGen 允许代理将生成的代码提交到沙盒（如 Docker 容器）安全执行，并支持实时查看代理行为、可视化消息流等 |

**不足 / Weaknesses:** 社区生态尚处于起步阶段，作为近年才推出的框架（2024 年末发布重构版 v0.4），AutoGen 的生态系统相对其他成熟框架而言仍在成长中；文档详细文字并不够社区区较快，但由于版本更新较快，文档与实际功能不一致的情况出现；第三方针对 AutoGen 的教程、案例和工具库目前数量有限，大部分资源来自官方及微软团队；这意味着在遇到非常规问题时，开发者能够借鉴的社区经验相对较少。

**使用示例 — Swarm 模式的机票退订助手:**

```
AutoGen Swarm 退票助手 — 输入 'quit' 或 'exit' 退出程序

我要退订机票
[FunctionCall(transfer_to_travel_agent)]
Transferred to user, adopting the role of user immediately.
[HandoffMessage(travel_agent)]
User: CA1123
[FunctionCall(name='transfer_to_flights_refunder')]
Transferred to flights_refunder, adopting the role of flights_refunder immediately.
```

---

## Key Takeaways 核心要点

- **Workflow vs Agent**：Workflow 适合步骤确定、分支有限的流程；Agent 适合问题空间无法穷举、需要跨系统动态决策的场景。
- **AutoGPT**：自主性最强，适合通用任务，但可控性低、成本高。
- **LangGraph**：开发者控制最精细，适合需要明确步骤、可审计和可中断的工作流。
- **Dify**：门槛最低，低代码上手，适合快速原型和中等复杂度应用，深度定制受限。
- **CrewAI**：角色化多 Agent 协作，工具生态丰富，适合步骤不固定的探索型任务。
- **AutoGen**：微软原生多 Agent，异步消息驱动，适合分布式、可观测的复杂多 Agent 系统，生态尚在成长。

## References

- Xiaohongshu (rednote) article ID: 4356821527
- LangChain / LangGraph official documentation
- Microsoft AutoGen documentation
- Dify official documentation
- CrewAI official documentation
