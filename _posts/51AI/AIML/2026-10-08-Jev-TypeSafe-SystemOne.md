---
title: "Meow's AI - Jev (TypeSafe) System One Model"
date: 2026-10-08 11:11:11 -0400
description: Definition, design, limits, and usage of Jev, the TypeSafe AI System One model that answers with typed choices and confidence instead of text, with a section on SOC use.
categories: [51AI, AIML]
tags: [AI, ML, Jev, TypeSafe, SystemOne, Classification, ConfidenceScore, SOC]
math: false
toc: true
---

# Jev (TypeSafe) System One Model

**Table of contents:**

- [Jev (TypeSafe) System One Model](#jev-typesafe-system-one-model)
  - [Overview 概述](#overview-概述)
  - [Definition 定义](#definition-定义)
    - [Name origin 名称来源](#name-origin-名称来源)
    - [System One vs System Two 系统一与系统二](#system-one-vs-system-two-系统一与系统二)
    - [Jev vs LLM](#jev-vs-llm)
  - [Design 设计](#design-设计)
    - [Input: state and questions 输入：状态与问题](#input-state-and-questions-输入状态与问题)
    - [Question types 问题类型](#question-types-问题类型)
    - [Output 输出](#output-输出)
    - [Speed, price, and limits 速度、价格与限制](#speed-price-and-limits-速度价格与限制)
  - [Claims vs Reality 声明与现实](#claims-vs-reality-声明与现实)
    - [Self-reported benchmarks 自报基准](#self-reported-benchmarks-自报基准)
    - [Can Jev hallucinate? Jev 会幻觉吗？](#can-jev-hallucinate-jev-会幻觉吗)
    - [Known limits 已知局限](#known-limits-已知局限)
  - [Implementation Patterns 实现模式](#implementation-patterns-实现模式)
    - [Confidence-gated routing 置信度门控路由](#confidence-gated-routing-置信度门控路由)
    - [Input preparation 输入准备](#input-preparation-输入准备)
    - [Untrusted input 不可信输入](#untrusted-input-不可信输入)
    - [Version pinning and data terms 版本固定与数据条款](#version-pinning-and-data-terms-版本固定与数据条款)
  - [Usage 使用场景](#usage-使用场景)
    - [General usage 通用场景](#general-usage-通用场景)
    - [Jev for SOC 安全运营中心中的 Jev](#jev-for-soc-安全运营中心中的-jev)
  - [Key Takeaways](#key-takeaways)
  - [References](#references)

---

## Overview 概述

<font color=OrangeRed>Jev</font> is an AI model from TypeSafe AI, released on 2026-09-15. It answers a question by choosing from a fixed set of answers and reporting how confident it is. It writes no text. TypeSafe calls it the first <font color=OrangeRed>System One model</font>: a model for fast, structured decisions that software acts on directly.

Jev 是 TypeSafe AI 于 2026-09-15 发布的 AI 模型。它从一组固定答案中选择答案，并报告置信度，不生成任何文字。TypeSafe 称它为第一个"系统一"模型：用于软件可以直接执行的快速、结构化决策。

---

## Definition 定义

### Name origin 名称来源

The name comes from William Stanley Jevons. In 1865, Jevons argued that more efficient steam engines would make Britain burn more coal, because cheaper power gets put to more uses. This is the <font color=OrangeRed>Jevons paradox</font>.

TypeSafe chose the name as a forecast: "We expect machine intelligence to follow a similar path to coal." When a decision gets cheaper, people make far more of them.

名称来自经济学家 William Stanley Jevons。1865 年他提出：蒸汽机越高效，英国烧的煤反而越多，因为更便宜的动力会被用在更多地方。这就是"杰文斯悖论"。TypeSafe 用这个名字做预测：机器智能会走和煤一样的路。决策越便宜，做出的决策就越多。

### System One vs System Two 系统一与系统二

The label comes from Daniel Kahneman's book *Thinking, Fast and Slow*.

| | System 1 系统一 | System 2 系统二 |
|---|---|---|
| Thinking style 思维方式 | Fast, intuitive 快速、直觉 | Slow, deliberate 缓慢、审慎 |
| AI equivalent AI 对应 | Jev: typed answer plus confidence 带置信度的类型化答案 | LLM: written reasoning, open-ended output 书面推理、开放式输出 |
| Typical task 典型任务 | Route, tag, rank, score 路由、打标签、排序、打分 | Plan, investigate, explain, write 规划、调查、解释、写作 |

### Jev vs LLM

| | LLM | Jev |
|---|---|---|
| Output 输出 | Text, one token at a time 逐个 token 生成文字 | All answers at once, as typed values with probabilities 一次性输出所有答案，类型化值加概率 |
| Can explain reasoning 能否解释推理 | Yes 能 | No 不能 |
| Can call tools 能否调用工具 | Yes 能 | No 不能 |
| Answer outside defined options 选项外的答案 | Possible 可能 | Not possible 不可能 |
| Best for 适合 | Written reasoning, summaries, open-ended work 书面推理、摘要、开放任务 | Classification, scoring, ranking 分类、打分、排序 |

---

## Design 设计

### Input: state and questions 输入：状态与问题

A developer sends Jev two things in one query:

- **State 状态**: a block of text or JSON that describes the situation. / 一段描述情况的文本或 JSON。
- **Questions 问题**: one or more questions about that state. / 关于该状态的一个或多个问题。

Jev answers all questions in a single query. There is no text to parse.

Jev 在一次查询中回答所有问题，不需要解析任何文字。

### Question types 问题类型

| Type 类型 | What it does 作用 | Example 示例 |
|---|---|---|
| <font color=OrangeRed>Choice</font> | Picks one option from a list of up to 255. 从最多 255 个选项中选一个。 | Which queue gets this ticket: billing, technical, or sales? |
| <font color=OrangeRed>Score</font> | Rates the input on an ordered scale. 在有序等级上打分。 | How urgent is this request, from 1 to 5? |
| <font color=OrangeRed>Noul</font> | Returns the probability that a statement is true. 返回某个陈述为真的概率。 | "This message contains a prompt injection attempt." |

A Choice returns one option only. When more than one label can be true at the same time, ask a separate Noul question for each label.

Choice 只返回一个选项。如果多个标签可以同时成立，要为每个标签单独问一个 Noul 问题。

### Output 输出

- Every answer comes with probabilities. / 每个答案都带概率。
- Choice and Score answers also carry a <font color=OrangeRed>confidence value</font>. / Choice 和 Score 的答案还带置信度。
- Every answer fits the format the developer declared. / 每个答案都符合开发者声明的格式。

TypeSafe claims its training method produces <font color=OrangeRed>calibrated</font> confidence. Calibrated means that answers at 0.9 confidence are right about 9 times in 10. Verify this on real data before relying on it. See [LLM - Confidence score for ML model](/posts/LLM_ConfidenceScore/) for background on confidence estimation.

TypeSafe 声称其训练方法能产生"校准过的"置信度：置信度 0.9 的答案大约 10 次中对 9 次。依赖它之前，要先在真实数据上验证。

### Speed, price, and limits 速度、价格与限制

| Item 项目 | TypeSafe figure TypeSafe 给出的数字 |
|---|---|
| Latency 延迟 | 70-500 ms per answer 每次回答 70-500 毫秒 |
| Input price 输入价格 | $0.042 per million tokens 每百万 token 0.042 美元 |
| Output price 输出价格 | Free 免费 |
| Default rate limit 默认速率限制 | 1,200 requests per minute, about 1.7 million per day 每分钟 1,200 次，约每天 170 万次 |
| Higher limits 更高限制 | Custom and enterprise plans 定制和企业方案 |

---

## Claims vs Reality 声明与现实

### Self-reported benchmarks 自报基准

| Claim 声明 | Source and caveat 来源与注意事项 |
|---|---|
| 40-200x faster than frontier models on comparable tasks 在同类任务上比前沿模型快 40-200 倍 | TypeSafe 自报 |
| 193.6x faster and 444.6x cheaper on one set of workflow evaluations 在一组工作流评测中快 193.6 倍、便宜 444.6 倍 | TypeSafe's own team wrote the workflows. TypeSafe says "some bias could exist" and that the figures sit "on the higher end of real world gains." 工作流由 TypeSafe 团队自己编写，公司承认可能有偏差，且数字处于实际收益的高端。 |

TrueFoundry's review lists these figures as "self-reported and not yet independently reproduced."

TrueFoundry 的评测指出，这些数字是自报的，尚未被独立复现。

### Can Jev hallucinate? Jev 会幻觉吗？

TypeSafe says Jev "can't hallucinate." This claim covers the **format** of the answer, not its **correctness**.

| Failure type 失败类型 | Possible with Jev? Jev 会不会出现？ |
|---|---|
| Invented tool name, hostname, or citation 编造的工具名、主机名或引用 | No. Jev writes no free text. 不会，Jev 不写自由文本。 |
| Answer outside the defined options 选项外的答案 | No 不会 |
| Wrong option with high confidence 高置信度地选错 | **Yes 会** |

TrueFoundry: "what's been eliminated is the malformed answer, not the mistaken judgment."

TrueFoundry："消除的是格式错误的答案，而不是错误的判断。"所以仍然要用已确认的结果来衡量准确率。

### Known limits 已知局限

TypeSafe's documentation lists these weak points:

- It "answers the question you wrote, not the one you meant." Write each question precisely. / 它只回答写下来的问题，而不是想问的问题。问题要写准确。
- It does not count reliably. / 计数不可靠。
- It reads dates as text, not as ordered values. / 把日期当作文本，而不是有序的值。
- Accuracy drops as the input fills with content unrelated to the decision. / 输入中无关内容越多，准确率越低。
- It accepts text only, with no images. / 只接受文本，不接受图片。
- It does not treat the state as hostile by default. Text written to steer the model "can move the answer." / 默认不把输入当作恶意内容，刻意引导的文字可以改变答案。

---

## Implementation Patterns 实现模式

### Confidence-gated routing 置信度门控路由

TypeSafe documents this as the main design pattern:

1. Ask Jev the question. / 向 Jev 提问。
2. When confidence is above a threshold, accept the answer and act on it. / 置信度高于阈值时，接受答案并执行。
3. When confidence is below the threshold, send the item to a slower reasoning model or a person. / 置信度低于阈值时，交给较慢的推理模型或人工处理。

```text
            +---------+   confidence >= threshold   +-------------------+
 state ---> |   Jev   | --------------------------> | act automatically |
            +---------+                             +-------------------+
                 |
                 |  confidence < threshold
                 v
        +---------------------------+
        | reasoning model or person |
        +---------------------------+
```

Set each threshold by the cost of acting on a wrong answer. Even with calibrated scores, 0.9 confidence means 1 wrong answer in 10.

每个阈值要根据"按错误答案执行"的代价来设定。即使置信度已校准，0.9 也意味着每 10 次错 1 次。

To check calibration:

1. Group answers by confidence band, for example 0.8-0.9 and 0.9-1.0. / 按置信度区间分组。
2. Measure accuracy in each band against confirmed outcomes. / 在每个区间内用已确认的结果衡量准确率。
3. When accuracy is lower than the band, raise the threshold or change the design. / 准确率低于区间值时，提高阈值或修改设计。
4. Count the high-cost misses that land in the auto-accept band. / 统计落在自动接受区间内的高代价错误。

Grade against confirmed outcomes, not against another model's labels. Agreement with a frontier model only measures agreement. When two models disagree, either one can be wrong.

要用已确认的结果评分，而不是用另一个模型的标签评分。与前沿模型一致只说明两者一致；两者不一致时，任何一方都可能错。

### Input preparation 输入准备

- **Compute numbers in code. 用代码计算数值。** Counts, time gaps, and speeds go through code first. Send Jev the result, not the raw records. / 计数、时间差、速度先用代码算好，再把结果交给 Jev。
- **Send named fields. 发送命名字段。** Pass only the fields the decision depends on. Accuracy falls as unrelated content grows, and cost rises with every input token. / 只传决策需要的字段。无关内容越多准确率越低，每个输入 token 都会增加成本。
- **Gather context first. 先收集上下文。** Jev does not query anything. Put all the evidence it needs into the state before the call. / Jev 不会自己查询，调用前要把所需证据放进状态里。
- **Use another tool for images. 图片用其他工具处理。** Jev accepts text only. / Jev 只接受文本。

### Untrusted input 不可信输入

When any field in the state comes from an outside party, treat it as hostile. Test two cases:

- Can injected text raise the score of a benign item? / 注入的文字能否提高良性条目的分数？
- Can injected text lower the score of a bad item, for example a forged "approved" note? / 注入的文字能否降低恶意条目的分数，例如伪造的"已批准"字样？

When either case works, clean those fields before scoring. Remove comments and decode encoded content, but keep the core field the decision depends on.

任一情况成立时，打分前要清理这些字段。删除注释、解码编码内容，但保留决策所依赖的核心字段。

### Version pinning and data terms 版本固定与数据条款

- The `jev-latest` alias moves to each new release, so answers can change with no change to the code. Pin a versioned model name, retest thresholds on each new version, and log the model version with each result. / `jev-latest` 别名会随每次发布变化，代码不变答案也可能变。要固定带版本号的模型名，每个新版本都重测阈值，并在每条结果中记录模型版本。
- TypeSafe commits not to train on user data and offers zero data retention to enterprise customers through its sales team. Confirm which terms apply to the account and sign a data processing agreement before sending production data. / TypeSafe 承诺不用用户数据训练模型，并通过销售团队为企业客户提供零数据留存。发送生产数据前，要确认账户适用的条款并签署数据处理协议。

---

## Usage 使用场景

### General usage 通用场景

Jev suits <font color=OrangeRed>bounded decisions</font>: the answer is one item from a known list, or a number on a known scale.

Jev 适合"范围有限的决策"：答案是已知列表中的一项，或已知等级上的一个数值。

| Use 用途 | Description 说明 |
|---|---|
| Routing 路由 | Send an item to the queue, team, or workflow that matches its type. 把条目发送到匹配类型的队列、团队或流程。 |
| Tagging 打标签 | Label an item with a category for grouping and reporting. 给条目加类别标签，便于分组和报告。 |
| Ranking 排序 | Order candidates by relevance. 按相关性排列候选项。 |
| First-pass scoring 初筛打分 | Score high-volume input before a slower step looks at it. 在较慢的步骤之前，先给大量输入打分。 |
| Guardrails 护栏 | Screen prompts, tool outputs, and responses of an LLM agent for prompt injection before another model acts on them. TypeSafe publishes a guardrails recipe. 在其他模型执行之前，检查 LLM 智能体的提示、工具输出和响应中是否有提示注入。 |

Jev is the wrong tool for work that needs written reasoning, multi-step planning, tool calls, or open-ended output. Use an LLM for that work.

需要书面推理、多步规划、工具调用或开放式输出的工作，Jev 不适合，应使用 LLM。

### Jev for SOC 安全运营中心中的 Jev

A SOC collects far more process events, emails, and logins than it can afford to score with a frontier model. At Jev's price, a team can score a much larger share of that data, not only the items that fire an alert. If the Jevons pattern holds, the SOC will make far more automated judgments, and each suspicious result still needs an analyst or an AI SOC agent to find out what happened.

SOC 收集的进程事件、邮件和登录记录，远多于用前沿模型能负担得起打分的数量。按 Jev 的价格，团队可以给更大比例的数据打分，而不只是触发告警的部分。如果杰文斯规律成立，SOC 会做出多得多的自动判断，而每个可疑结果仍然需要分析师或 AI SOC 智能体去调查。

#### SOC use cases SOC 用例

| Use 用途 | SOC example SOC 示例 |
|---|---|
| Routing 路由 | Send an alert to the investigation plan, queue, or team that matches its type. 把告警发送到匹配类型的调查方案、队列或团队。 |
| Tagging 打标签 | Label raw events or untagged alerts with a MITRE ATT&CK tactic. Many detection rules already carry tags (for example the Sigma `tags` field), so the value is in untagged data. One technique can map to more than one tactic (Valid Accounts maps to four), so ask one Noul question per tactic. 给原始事件或未打标签的告警标注 ATT&CK 战术。一个技术可能对应多个战术，所以每个战术问一个 Noul 问题。 |
| Ranking 排序 | Order knowledge-base articles, related alerts, or asset owners to pull into an investigation. 给要纳入调查的知识库文章、相关告警或资产负责人排序。 |
| First-pass scoring 初筛打分 | Score EDR process events before they become alerts. A single process event is rarely enough: malware abuses Office apps to start child processes, but legitimate business apps also start PowerShell. Add the parent process chain and the host role to the state. 在 EDR 进程事件变成告警前打分。单个进程事件通常不够判断，要把父进程链和主机角色加入状态。 |
| Guardrails 护栏 | Screen inputs and outputs of an LLM-based SOC agent for prompt injection. 检查基于 LLM 的 SOC 智能体的输入和输出中是否有提示注入。 |

#### Scale and false positives 规模与误报

Price is not the main ceiling. False positives are. A team that scores 10 million events a day with a 0.1% false-positive rate gets 10,000 flags a day to work.

价格不是主要上限，误报才是。每天给 1,000 万个事件打分、误报率 0.1%，每天就有 10,000 条标记要处理。

#### What Jev cannot do in a SOC Jev 在 SOC 中做不到的事

- **No investigation planning. 不能规划调查。** In an investigation, each question depends on the last answer. Example: an Okta alert for a login from a new country. The analyst checks MFA, then the session activity after login, then whether the user can confirm the trip. Jev can answer each question quickly, but it does not choose them. / 调查中每个问题都取决于上一个答案。Jev 能快速回答每个问题，但不会自己选问题。
- **No evidence gathering. 不收集证据。** Jev does not run SIEM, EDR, or identity queries. / Jev 不执行 SIEM、EDR 或身份系统的查询。
- **No explanation. 不能解释。** A reviewer looks for what was checked, what came back, and why it supports the call. A score of 0.91 gives the reviewer nothing to verify. / 审核人要看查了什么、结果是什么、为什么支持结论。0.91 这个分数无从核实。
- **No counts or time math. 不做计数和时间计算。** Impossible-travel speed, failed attempts in a window, and minutes between email delivery and first click must be computed in code first. / 不可能旅行的速度、时间窗口内的失败次数、邮件送达到首次点击的分钟数，都要先用代码计算。
- **No images. 不处理图片。** Phishing cases that depend on a screenshot, QR code, or image attachment need another tool. / 依赖截图、二维码或图片附件的钓鱼案例需要其他工具。

#### SOC pre-production checklist SOC 上线前检查清单

1. **Include malicious activity in the test set. 测试集要包含恶意活动。** A quiet tenant can hold weeks of events with nothing confirmed malicious. Results on that data say nothing about the alerts that matter most. / 平静的租户可能几周都没有确认的恶意事件，在这种数据上的结果无法说明最重要的告警。
2. **Grade against confirmed outcomes. 用已确认的结果评分。** See [Confidence-gated routing](#confidence-gated-routing-置信度门控路由).
3. **Check calibration by confidence band. 按置信度区间检查校准。** 0.9 confidence is still too many errors for alerts closed with no analyst. Count the confirmed-malicious items in the auto-accept band. / 对于无人审核就关闭的告警，0.9 置信度的错误率仍然太高。要统计自动接受区间内已确认的恶意条目。
4. **Send named fields. 发送命名字段。** Pass the command line, parent process, and user, not the full alert payload. / 传命令行、父进程和用户，而不是完整告警。
5. **Treat attacker-written text as hostile. 把攻击者写的文本当作恶意输入。** The attacker writes command lines, email subjects, file names, and script comments. Test whether a comment that names a credential-dumping tool raises a benign command's score, and whether a forged "approved by security" note lowers a malicious one. Remove comments and decode encoded commands, but keep the command line. / 测试注释和伪造的"安全团队已批准"字样能否改变分数。删除注释、解码编码命令，但保留命令行本身。
6. **Pin the model version. 固定模型版本。**
7. **Read the data terms. 阅读数据条款。** Alerts carry usernames, hostnames, and email content. / 告警包含用户名、主机名和邮件内容。

#### SOC conclusion SOC 结论

When scoring costs almost nothing, SOC capacity depends on how many flagged items the team can investigate and document. Jev can clear the easy items from the queue. An analyst, or an agent built to plan investigations, still has to work the rest. See [LLM - LLMs in Cybersecurity](/posts/LLM_Security_Cybersecurity/) for LLM-based SOC work.

当打分几乎不花钱时，SOC 的能力取决于团队能调查和记录多少被标记的条目。Jev 能清掉队列中简单的条目，剩下的仍然要由分析师或专门规划调查的智能体处理。

---

## Key Takeaways

- Jev is a System One model: it returns typed answers with probabilities and confidence, and writes no text. / Jev 是系统一模型：返回带概率和置信度的类型化答案，不写文字。
- Three question types: Choice (one of up to 255), Score (ordered scale), Noul (probability a statement is true). / 三种问题类型：Choice、Score、Noul。
- "Can't hallucinate" means no malformed output. It does not mean no wrong answers. / "不会幻觉"指没有格式错误，不代表没有错误答案。
- Speed and cost figures are self-reported and not independently reproduced. / 速度和成本数字是自报的，未被独立复现。
- Main pattern: confidence-gated routing. It only works when confidence is calibrated on real data. / 核心模式是置信度门控路由，前提是置信度在真实数据上校准。
- Compute counts and dates in code, send only needed fields, treat outside text as hostile, and pin the model version. / 计数和日期用代码算，只发需要的字段，外部文本视为恶意，固定模型版本。
- In a SOC, Jev moves the bottleneck from scoring to investigation. / 在 SOC 中，Jev 把瓶颈从打分转移到调查。

## References

- Ajmal Kohgadai, "What Jev (TypeSafe) Means for Security Operations", Prophet Security blog, 2026-09-29. The author works in product marketing at Prophet Security, a vendor of AI SOC products.
- TypeSafe AI documentation on Jev, confidence-gated routing, and the guardrails recipe, as quoted in the article above.
- TrueFoundry review of Jev, as quoted in the article above.
- Daniel Kahneman, *Thinking, Fast and Slow*.
- [LLM - Confidence score for ML model](/posts/LLM_ConfidenceScore/)
- [LLM - LLMs in Cybersecurity](/posts/LLM_Security_Cybersecurity/)
