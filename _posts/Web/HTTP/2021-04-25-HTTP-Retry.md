---
title: HTTP - Retry and Circuit Breaker
# author: Grace JyL
date: 2021-04-25 11:11:11 -0400
description:
excerpt_separator:
categories: [Web, HTTP]
tags: [Web, HTTP, Retry, CircuitBreaker, Resilience]
math: true
# pin: true
toc: true
# image: /assets/img/sample/devices-mockup.png
---

- [HTTP - Retry and Circuit Breaker 重试与断路器](#http---retry-and-circuit-breaker-重试与断路器)
  - [这篇笔记讲什么 What This Note Covers](#这篇笔记讲什么-what-this-note-covers)
  - [先搞懂四个词 Four Words to Understand First](#先搞懂四个词-four-words-to-understand-first)
    - [幂等 Idempotency](#幂等-idempotency)
  - [什么情况下要 retry When to Retry](#什么情况下要-retry-when-to-retry)
    - [状态码对照表 Status Codes and the Correct Action](#状态码对照表-status-codes-and-the-correct-action)
    - [429 Code and the Retry-After Header](#429-code-and-the-retry-after-header)
    - [读超时的歧义 The Ambiguity of a Read Timeout](#读超时的歧义-the-ambiguity-of-a-read-timeout)
  - [Retry处理步骤 Retry Handling Steps](#retry处理步骤-retry-handling-steps)
    - [简单的立即retry Simple Immediate Retry](#简单的立即retry-simple-immediate-retry)
      - [立即retry的算术 The arithmetic of immediate retry](#立即retry的算术-the-arithmetic-of-immediate-retry)
    - [重试风暴 Retry Storm and Retry Amplification](#重试风暴-retry-storm-and-retry-amplification)
    - [有延迟的retry Delayed Retry](#有延迟的retry-delayed-retry)
      - [固定间隔的 delay Fixed-Interval Delay](#固定间隔的-delay-fixed-interval-delay)
      - [随机 delay 的方式 Randomised Delay](#随机-delay-的方式-randomised-delay)
      - [四种 backoff 策略对比 Four Backoff Strategies Compared](#四种-backoff-策略对比-four-backoff-strategies-compared)
      - [抖动 jitter 到底解决什么问题 What Jitter Actually Fixes](#抖动-jitter-到底解决什么问题-what-jitter-actually-fixes)
      - [可运行的调度模拟 A Runnable Schedule Simulation](#可运行的调度模拟-a-runnable-schedule-simulation)
      - [必须给重试设上限 Always Bound the Retries](#必须给重试设上限-always-bound-the-retries)
      - [重试预算 Retry Budgets](#重试预算-retry-budgets)
    - [Circuit Breaker(断路器) Circuit Breaker](#circuit-breaker断路器-circuit-breaker)
      - [断路器到底是什么 What a Circuit Breaker Actually Is](#断路器到底是什么-what-a-circuit-breaker-actually-is)
      - [一次完整的跳闸时间线 A Complete Trip Timeline](#一次完整的跳闸时间线-a-complete-trip-timeline)
      - [断路器和重试的分工 How Retry and the Breaker Divide the Work](#断路器和重试的分工-how-retry-and-the-breaker-divide-the-work)
      - [自己动手写一个断路器 Building a Circuit Breaker From Scratch](#自己动手写一个断路器-building-a-circuit-breaker-from-scratch)
        - [完整实现 The Complete Implementation](#完整实现-the-complete-implementation)
        - [逐条拆解决策逻辑 Dissecting the Decision Logic](#逐条拆解决策逻辑-dissecting-the-decision-logic)
        - [让状态机跑起来 Watching the State Machine Move](#让状态机跑起来-watching-the-state-machine-move)
        - [两种失败计数方式 Two Ways to Count Failures](#两种失败计数方式-two-ways-to-count-failures)
        - [慢调用也是一种失败 Slow Calls Count as Failures](#慢调用也是一种失败-slow-calls-count-as-failures)
        - [这个玩具版故意省略了什么 What This Toy Deliberately Omits](#这个玩具版故意省略了什么-what-this-toy-deliberately-omits)
      - [生产环境中真实的实现 Real Implementations in Production](#生产环境中真实的实现-real-implementations-in-production)
        - [五种实现横向对比 Cross-Library Comparison](#五种实现横向对比-cross-library-comparison)
        - [什么算失败 What Counts as a Failure](#什么算失败-what-counts-as-a-failure)
        - [服务网格层面的断路 Circuit Breaking at the Service-Mesh Layer](#服务网格层面的断路-circuit-breaking-at-the-service-mesh-layer)
        - [网关层也能断路 The Gateway Layer Can Also Break Circuits](#网关层也能断路-the-gateway-layer-can-also-break-circuits)
      - [生产环境中的常见应用模式 Common Production Usage Patterns](#生产环境中的常见应用模式-common-production-usage-patterns)
        - [重试和断路器的组合顺序 Composition Order: Retry Inside or Outside the Breaker](#重试和断路器的组合顺序-composition-order-retry-inside-or-outside-the-breaker)
        - [韧性四件套 The Four Resilience Primitives](#韧性四件套-the-four-resilience-primitives)
        - [参数怎么定 How to Choose the Numbers](#参数怎么定-how-to-choose-the-numbers)
        - [每个实例各有一个断路器 Breaker State Is Per Instance](#每个实例各有一个断路器-breaker-state-is-per-instance)
        - [恢复时的二次冲击 The Recovery Stampede](#恢复时的二次冲击-the-recovery-stampede)
        - [反模式 Anti-Patterns](#反模式-anti-patterns)
        - [怎么测试断路器 How to Test a Breaker](#怎么测试断路器-how-to-test-a-breaker)
        - [该看哪些指标 Metrics and Alerts Worth Having](#该看哪些指标-metrics-and-alerts-worth-having)
  - [Retry 设计模式在客户端的应用与实现 Applying and Implementing the Retry Pattern on the Client](#retry-设计模式在客户端的应用与实现-applying-and-implementing-the-retry-pattern-on-the-client)
    - [原始实现 The Original Implementation](#原始实现-the-original-implementation)
    - [客户端特有的约束 Constraints Unique to Clients](#客户端特有的约束-constraints-unique-to-clients)
  - [监控：更好地在运行时了解你的系统 Monitoring: Understanding the System at Runtime](#监控更好地在运行时了解你的系统-monitoring-understanding-the-system-at-runtime)
    - [一条重试日志该记录什么 What Belongs in a Retry Log Line](#一条重试日志该记录什么-what-belongs-in-a-retry-log-line)
    - [与熔断器指标的关系 How This Relates to Circuit Breaker Metrics](#与熔断器指标的关系-how-this-relates-to-circuit-breaker-metrics)
  - [Example 实例](#example-实例)
    - [go-resty 重试机制的实现 go-resty's Retry Implementation](#go-resty-重试机制的实现-go-restys-retry-implementation)
    - [Backoff函数 The Backoff Function](#backoff函数-the-backoff-function)
    - [Demo 实战调用](#demo-实战调用)
    - [一些其他重试机制的实现 A Few Other Retry Implementations](#一些其他重试机制的实现-a-few-other-retry-implementations)
    - [上手清单 A Practical Checklist](#上手清单-a-practical-checklist)

---

# HTTP - Retry and Circuit Breaker 重试与断路器

- ref
  - [浅谈Retry设计模式及在前端的应用与实现](https://segmentfault.com/a/1190000022418493)
  - [重试机制的实现](https://segmentfault.com/a/1190000025181043)
  - [如何正确地实现重试 (Retry)](https://www.infoq.cn/article/7z0wpahuh9euxqiq5xzx)

---

## 这篇笔记讲什么 What This Note Covers

> **大白话:** 打电话没人接，是该马上再打、隔一会儿再打、还是干脆别打了？这篇笔记就是这三个决定的说明书。

| 读者想问的问题 Reader's question | 回答它的章节 Section that answers it |
| --- | --- |
| 这次失败到底该不该重试？ Should this particular failure be retried at all? | 什么情况下要 retry — When to retry |
| 两次重试之间要等多久？ How long should the gap between attempts be? | Retry处理步骤 与退避策略 — Retry steps and backoff strategies |
| 什么时候应该彻底停止重试？ When should retrying stop completely? | 断路器 Circuit Breaker |
| 成熟的库是怎么做的？ How do production libraries actually implement this? | 各语言实现 — Library implementations |

<font color=OrangeRed>Retry</font>:

- Retry means sending the same request again after a failure;
- a circuit breaker means deliberately stopping further sends once failures pile up.
- The two belong together, because retrying alone will push an already-overloaded service further down.

---

## 先搞懂四个词 Four Words to Understand First

> **大白话:** 把这件事想成在餐厅点菜：顾客是客户端，厨房是服务端，写在纸条上递进去的那句"一份牛肉面"就是请求。

| 词 Term | 中文解释 Chinese | English |
| --- | --- | --- |
| 客户端 client | 主动发起要求的一方，比如浏览器、手机 App、或另一个后端服务。 | The side that initiates the ask: a browser, a phone app, or another backend service. |
| 服务端 server | 收到要求、干活、然后回话的一方。 | The side that receives the ask, does the work, and answers. |
| 请求 request | 客户端发给服务端的那一条具体消息，包含方法、地址和数据。 | The one concrete message sent from client to server, carrying a method, an address, and data. |
| 响应 response | 服务端回过来的消息，最重要的部分是状态码。 | The message coming back, whose most important part is the status code. |

请注意：一次失败的请求，可能是"厨房听懂了但做坏了"，也可能是"纸条根本没递进去"，两者处理方式完全不同。
Note that a failed request may mean "the kitchen understood the order but botched it", or "the slip never reached the kitchen", and the two are handled differently.

### 幂等 Idempotency

> **大白话:** 按电梯按钮按十下，电梯还是只来一次，这就是幂等；往购物车里点十下"加入"，就真的加了十件，这就不幂等。  

<font color=OrangeRed>幂等 idempotency</font> 的定义：

- performing the same operation once and performing it many times `leave the system in exactly the same final state`.
- This is the precondition for retrying.

| 操作 Operation | 幂等？ Idempotent? | 重试安全吗 Safe to retry? |
| --- | --- | --- |
| 查询账户余额 Read an account balance | 是 Yes | 安全，查十次余额也不会变 Safe, ten reads do not change the balance |
| 转账 100 元 Transfer 100 dollars | 否 No | 危险，重试可能扣两次钱 Dangerous, a retry may debit twice |
| 删除 ID 为 7 的记录 Delete record with ID 7 | 是 Yes | 安全，第二次删除只是"已经没有了" Safe, the second delete just finds it already gone |
| 新增一条订单 Create a new order | 否 No | 危险，会产生重复订单 Dangerous, it produces duplicate orders |

HTTP 方法本身就带有幂等约定：GET、HEAD、PUT、DELETE 按规范是幂等的，POST 不是。

对不幂等的写操作，正确做法不是"不重试"，而是让它变成幂等的：客户端为每次业务操作生成一个唯一的幂等键（idempotency key），服务端见到重复的键就直接返回第一次的结果。
For a non-idempotent write, the right move is not "never retry" but "make it idempotent": the caller generates a unique idempotency key for each business operation, sends it in a header such as `Idempotency-Key`, and the server returns the first result whenever it sees a repeated key.

---

## 什么情况下要 retry When to Retry

> **大白话:** 水管突然没水，可能是全市停水（等等就好），也可能是水龙头装反了（等一万年也不会好）。只有前一种值得再拧一次。

认识 Transient fault（短暂故障）
Recognising a transient fault, meaning a fault that is temporary by nature.

- 短暂存在，并且在一段时间后会被修复的故障。
  A fault that exists only briefly and repairs itself after some period.
- 这个时间可以短到几毫秒也可以长达几小时。
  That period may be as short as a few milliseconds or as long as several hours.
- 如果的请求是因为一个这样的故障而失败的，那在适当的时候重试就可以了。
  If a request failed because of such a fault, retrying at an appropriate moment is enough.

- Many possible causes of a failed request.
  - a bug in the server's own internal logic,
  - a bad request sent by the client,
  - infrastructure issue, such as a temporary load spike, a single machine going down, or a network problem.
- `Retrying` is meaningful only in the **transient-fault case**.

> 在前端应用中，短暂故障往往发生在你向服务端请求资源时。比如你向一个API发送一个AJAX请求，对面返回一个 “5XX” 的响应。

鉴别 Transient fault（短暂故障）
Identifying a transient fault.

- 最简单的方法是运用 HTTP 请求的响应码。根据规范，
- 400-499 之间是客户端造成的问题，没有必要重试了, problem caused by the client, so there is no point retrying,
  - 4xx 默认不重试，但 408 和 429 例外
- 500-599 之间是服务端的故障, server-side failure.
  - 5xx 默认可重试，但 501 Not Implemented 和 505 例外，因为它们不会自己好起来。
  - to pick the transient faults out of the 5xx family.
  - 如果服务端对错误响应码有标准的定义，就可以通过不同的号码得知错误的原因，从而决定是进行retry还是做别的处理。
    If the server defines its error codes in a standard way, the cause can be read off the number, and the caller can decide between retrying and handling it some other way.
  - 服务端开发中标准并清晰的定义错误码和给与错误信息的重要性。
    This is why defining error codes clearly, and returning informative error messages, matters so much in server development.

### 状态码对照表 Status Codes and the Correct Action

> **大白话:** 这张表就是一份"回话对照卡"：厨房回的每句话，对应该不该再递一次纸条。  

| 状态码 Code | 含义 Meaning | 重试 Retry | 原因 Why in one clause |
| --- | --- | --- | --- |
| 400 Bad Request | 请求格式错误 Malformed request | 否 No | 重发同样的坏请求还是坏的 The same malformed bytes fail again |
| 401 Unauthorized | 未认证 Missing or expired credentials | 否 No | 需要换新凭证，不是等一等 New credentials are needed, not time |
| 403 Forbidden | 无权限 Authenticated but not permitted | 否 No | 权限不会因为重试而出现 Permission does not appear on a second try |
| 404 Not Found | 资源不存在 Resource absent | 否 No | 资源不会因为重试而被创建 The resource is not created by asking again |
| 408 Request Timeout | 服务端等请求等超时 Server timed out waiting for the request | 是 Yes | 请求根本没被处理过，重发是安全的 The request was never processed, so resending is safe |
| 409 Conflict | 状态冲突 State conflict, e.g. version mismatch | 视情况 Conditional | 需先读取最新状态再重试 Only after re-reading the current state |
| 422 Unprocessable Entity | 语法对但语义错 Syntactically valid, semantically invalid | 否 No | 业务数据本身不合法 The business payload itself is invalid |
| 429 Too Many Requests | 触发限流 Rate limit reached | 是 Yes | 等待配额恢复即可 The quota refills after waiting |
| 500 Internal Server Error | 服务端未预期错误 Unexpected server error | 是 Yes | 可能是偶发异常 It may be a one-off exception |
| 501 Not Implemented | 服务端不支持该方法 The method is not supported at all | 否 No | 重新部署之前不会改变 It cannot change before a redeploy |
| 502 Bad Gateway | 上游回了坏响应 Upstream returned garbage | 是 Yes | 常在上游重启期间出现 Common while an upstream restarts |
| 503 Service Unavailable | 服务暂时不可用 Temporarily unavailable | 是 Yes | 定义上就是短暂的 Transient by definition |
| 504 Gateway Timeout | 网关等上游超时 Gateway timed out on upstream | 仅幂等 Idempotent only | 上游可能已经做完了 The upstream may already have finished |
| 505 HTTP Version Not Supported | 不支持该 HTTP 版本 The HTTP version is not supported | 否 No | 应该降级协议，而不是等待 Downgrade the protocol rather than wait |
| 连接被拒 Connection refused | 端口上没有进程监听 Nothing listening on the port | 是 Yes | 进程可能正在重启 The process may be mid-restart |
| DNS 解析失败 DNS failure | 域名解析不出 IP Name cannot be resolved | 是 Yes | 解析器故障常是短暂的 Resolver glitches are usually brief |
| TLS 握手失败 TLS handshake failure | 加密协商失败 Encryption negotiation failed | 视情况 Conditional | 证书过期不该重试，网络中断该重试 Expired certificates no, network blips yes |
| 读超时 Read timeout | 发出去了但没等到回话 Sent but no answer arrived | 仅幂等 Idempotent only | 服务端可能已经执行成功 The server may already have succeeded |

### 429 Code and the Retry-After Header

> **大白话:** 银行柜员说"三十分钟后再来"，还偏要每分钟去问一次，这不是勤奋，是插队。  

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Retry-After: 30
X-RateLimit-Remaining: 0

{"error": "rate_limit_exceeded", "message": "quota resets in 30 seconds"}
```

服务端返回 429 时，通常会带上 <font color=OrangeRed>Retry-After</font> 响应头，明确告诉调用方"请等这么久"。

- 它的值可以是秒数，也可以是一个 HTTP 日期。
- 忽略 Retry-After 是一个常见且不礼貌的 bug：它把服务端明确表达的背压（backpressure，即"我扛不住了，慢一点"）当成噪音，结果是限流窗口不断被刷新，双方都恢复得更慢。Ignoring Retry-After is a common and rude bug: it treats an explicit statement of backpressure, meaning "this side is saturated, slow down", as noise, so the rate-limit window keeps resetting and both sides recover more slowly.

> 下面这段代码依赖 requests 库，安装命令 `pip install requests==2.32.3`。

```python
# pip install requests==2.32.3
from __future__ import annotations

import random
import time
import requests

MAX_ATTEMPTS = 4
FALLBACK_BASE_SECONDS = 2.0
MIN_WAIT_SECONDS = 0.5
MAX_WAIT_SECONDS = 60.0
JITTER_RATIO = 0.2

def parse_retry_after_seconds(header: str) -> float | None:
    # 只接受非负秒数；"30.0"、" 30" 能过，"-1" 和 HTTP 日期一律退回退避
    # Accept a non-negative number of seconds only: "30.0" and " 30" pass, while "-1" and an HTTP date fall back.
    try:
        seconds = float(header.strip())
    except ValueError:
        return None
    return seconds if seconds >= 0 else None

def get_honouring_retry_after(url: str, timeout: float = 5.0) -> requests.Response:
    for attempt in range(1, MAX_ATTEMPTS + 1):
        response = requests.get(url, timeout=timeout)
        if response.status_code != 429:
            return response

        # 最后一次尝试之后没有下一次了，不再白等一轮
        # No attempt follows the last one, so no full wait is spent for nothing.
        if attempt == MAX_ATTEMPTS:
            break

        server_seconds = parse_retry_after_seconds(response.headers.get("Retry-After", ""))
        # 服务端说了等多久就等多久，没说才退回指数退避
        # Honour the server's number when present, fall back to exponential backoff otherwise.
        if server_seconds is None:
            wait_seconds = FALLBACK_BASE_SECONDS * (2 ** (attempt - 1))
        else:
            wait_seconds = server_seconds

        # 夹到 [MIN, MAX]，既挡住 Retry-After: 86400，也挡住 Retry-After: 0 造成的忙等
        # Clamp into [MIN, MAX], blocking both Retry-After: 86400 and the busy loop from Retry-After: 0.
        wait_seconds = min(max(wait_seconds, MIN_WAIT_SECONDS), MAX_WAIT_SECONDS)
        # 加抖动，避免所有客户端在同一毫秒一起回来
        # Add jitter so that every client does not come back in the same millisecond.
        time.sleep(wait_seconds * (1.0 + random.uniform(0.0, JITTER_RATIO)))
    raise RuntimeError(f"still rate limited after {MAX_ATTEMPTS} attempts")
```

相对最初的写法，上面修掉了五处缺陷：
Relative to the first draft, five defects above are now fixed:

- 最后一次尝试前不再 sleep，省掉一整轮无意义的等待。 / The final attempt no longer sleeps before raising, which removes one entirely pointless wait.
- 退避改成 `FALLBACK_BASE_SECONDS * (2 ** (attempt - 1))`，秒数常量不再被误当成指数的底数。 / Backoff became `FALLBACK_BASE_SECONDS * (2 ** (attempt - 1))`, so a seconds-valued constant is no longer misused as the exponent base.
- 服务端给的值先夹进 `[MIN_WAIT_SECONDS, MAX_WAIT_SECONDS]`，`Retry-After: 86400` 不会睡满 24 小时，`Retry-After: 0` 也不会退化成忙等。 / The server-supplied value is clamped into `[MIN_WAIT_SECONDS, MAX_WAIT_SECONDS]`, so `Retry-After: 86400` does not sleep for a full day and `Retry-After: 0` does not degrade into a busy loop.
- 加入抖动，与本文后面的 checklist 保持一致。 / Jitter is present, which keeps the snippet consistent with the checklist later in this note.
- 解析不再用 `header.isdigit()`：`"30.0"`、`" 30"` 现在能正确解析，`"-1"` 和 HTTP 日期则明确退回退避而不是静默变成 0。 / Parsing no longer relies on `header.isdigit()`: `"30.0"` and `" 30"` now parse correctly, while `"-1"` and HTTP dates fall back to backoff explicitly instead of silently becoming zero.

上面这段只覆盖了秒数形式；若服务端返回 HTTP 日期，需改用 `email.utils.parsedate_to_datetime` 解析。
The snippet covers only the seconds form; an HTTP date requires `email.utils.parsedate_to_datetime` instead.

---

### 读超时的歧义 The Ambiguity of a Read Timeout

> **大白话:** 纸条递进厨房后就再没消息，可能菜根本没做，也可能菜已经做好了只是没人端出来。

读超时（read timeout）

- 意味着请求已经发出，但在限定时间内没有收到响应。
- 它<font color=OrangeRed>不代表操作失败</font>，只代表结果未知。
- the request was sent but no response arrived within the allotted time. I

幂等的写操作

- 对不幂等的写操作 (non-idempotent write) 在超时后重试，可能让客户被扣两次款、或者收到两份订单。
- 解决办法正是前面提到的幂等键：带同一个 `Idempotency-Key` 重试，服务端就能识别这是同一笔业务，从而只执行一次。retry with the same Idempotency-Key and the server recognises one single business operation, executing it exactly once.

---

## Retry处理步骤 Retry Handling Steps

> **大白话:** 打电话没人接的时候，先判断是"对方正在通话中"还是"号码根本不存在"，后者再打一万次也没用。

| 术语 Term | 中文解释 Chinese | English explanation |
| --- | --- | --- |
| request 请求 | 客户端发给服务端的一次询问，例如"把用户 42 的资料给我" | One question sent from a caller to a service, for example "return the profile of user 42" |
| transient fault 瞬时故障 | 只持续很短时间、原因不在请求本身的失败，例如网络抖动、服务端刚好在重启 | A failure that lasts only briefly and is not caused by the request itself, such as a network hiccup or a service restarting at that instant |

当请求失败时可以有一个基本的处理步骤：
When a request fails, a basic three-step procedure applies:

- 鉴别是不是 transient fault
  Determine whether the failure is a transient fault.
  - 判断这次失败是不是"过一会儿自己会好"的那一类。
  - Decide whether this failure belongs to the class that heals by itself after a short wait.
- 如果是，启动retry机制，进行一定次数的retry
  If it is, start the retry mechanism and carry out a bounded number of retries.
  - 是瞬时故障就再发一次同样的请求，重复的上限必须事先写死。
  - If it is transient, send the same request again, with a hard upper bound on the number of attempts fixed in advance.
- 当retry达到最大次数还没有成功，报错并说明原因：服务端暂时无法响应。
  When the retry budget is used up without success, raise an error and state the reason: the service is temporarily unable to respond.
  - 用尽次数后必须停下来并明确告知调用方原因，而不是无声地继续或返回一个假的成功。
  - Once the budget is exhausted the loop must stop and report the reason explicitly, rather than looping silently or returning a fabricated success.

基本的retry设计模式。
These three steps are the skeleton of every retry design pattern that follows.

其中第一步是整个模式的地基。如果把"用户名密码错误"这种<font color=OrangeRed>永久性故障 permanent fault</font>误判成瞬时故障，重试只会把同一个注定失败的请求发送多次，浪费两端的资源。
Step one is the foundation of the whole pattern. If a <font color=OrangeRed>permanent fault</font> such as a wrong password is misclassified as transient, retrying merely sends the same doomed request several times and wastes resources on both ends.

| 类别 Category | 例子 Example | 该不该重试 Retry? |
| --- | --- | --- |
| 瞬时 Transient | 连接超时、503 服务暂时不可用、连接被重置 Connection timeout, 503 temporarily unavailable, connection reset | 可以 Yes |
| 永久 Permanent | 400 请求格式错误、401 未认证、404 资源不存在 400 malformed request, 401 unauthenticated, 404 resource absent | 不可以 No |
| 不确定 Ambiguous | 写操作超时，不知道服务端是否已经落库 A write times out and it is unknown whether the service already persisted it | 仅当操作幂等时 Only if idempotent |

"幂等 idempotent"的定义见前文 [幂等 Idempotency](#幂等-idempotency) 一节。 / The definition of "idempotent" is given earlier, in the [幂等 Idempotency](#幂等-idempotency) section.

### 简单的立即retry Simple Immediate Retry

> **大白话:** 水管堵了，立刻把水龙头开到最大再冲一次——偶尔真能冲开，但如果堵的原因是下游水管本来就满了，这样只会更快地把水压爆。

- 当请求失败，立即retry，
  When a request fails, retry it immediately.
  - 失败返回之后不等待任何时间，马上发出第二次请求。
  - The second request leaves as soon as the first failure returns, with no waiting period in between.
- 用于一些不常见的失败原因，因为原因罕见，立刻retry也许就修复了。
  This fits uncommon failure causes: because the cause is rare, an immediate retry may already resolve it.
  - 例如一个丢掉的网络数据包，重发时它极不可能再次丢失。
  - A single dropped network packet is the classic case: the resend is very unlikely to be dropped again.
- 但当碰到一些常见的失败原因如服务端负载过高，不断的立即retry只会让服务端更加不堪重负。
  But for a common cause such as excessive server load, relentless immediate retries only push the service further past its limit.
  - 服务端失败的原因正是"请求太多"，而重试的动作是"发出更多请求"。
  - The reason the service failed is "too many requests", and the retry action is "send more requests".
- 试想如果有多个客户端instance在同时发送请求，那越是retry情况就越糟糕。
  Consider several client instances sending requests at the same moment: the more they retry, the worse the situation becomes.
  - 每个客户端实例都在独立地放大流量，彼此互不知情，总放大倍数是相乘的。
  - Each client instance amplifies traffic independently and without knowledge of the others, so the multipliers combine.
- **不带 backoff 的重试，对于下游来说会在失败发生时进一步遇到更多的请求压力，进一步恶化**。
  **Retrying without backoff means the downstream side meets even more request pressure at the exact moment it is already failing, which makes matters worse.**
  - 这里的 backoff 指"每次重试之前主动等待一段时间"，下一节会展开。
  - "Backoff" here means deliberately waiting before each retry; the next section develops it.

```java
public static <T> T retryNoDelay(final callable<T> callable, final int maxAttempts){
  for (int i = 0; i < maxAttempts; i++) {
    try {
      final T t = callable.call();
      if (isExpected(t)){ return t};
    }
    try {
      insertMessageInboxResult = messageInboxManager.insertMessage(messageInbox);
      if (insertMessageInboxResult) {
        break;
      }
    }
    catch (Exception e) {
      log.error(
        "insertMessageInbox exception retry {}, messageInbox={}", i, messageInbox)
    }
  }
  // return default t or error
  return null;
}
```

上面的代码块保持原样，它是一次真实的复制粘贴事故。问题清单如下。
The block above is kept verbatim; it is a genuine copy-paste accident. The defects are listed below.

- 类型名 `callable` 首字母小写，Java 标准库里的类型是 `java.util.concurrent.Callable`，原样无法编译。
  - The type is spelled `callable`; the JDK type is `java.util.concurrent.Callable`, so the source does not compile.
- `if (isExpected(t)){ return t};` 里分号位置错了，应该是 `return t;` 写在花括号内。
  - In `if (isExpected(t)){ return t};` the semicolon sits outside the brace instead of terminating the `return t;` statement.
- 第一个 `try` 块后面没有 `catch` 也没有 `finally`，Java 不允许孤立的 `try`。
  - The first `try` block has neither `catch` nor `finally`; Java forbids a bare `try`.
- 中间混进了一段与泛型重试助手完全无关的 `messageInbox` / `insertMessageInboxResult` 业务代码，这两个变量从未声明。
  - An unrelated `messageInbox` / `insertMessageInboxResult` business snippet was pasted into a generic helper, and neither variable is ever declared.
- `log.error(...)` 结尾缺少分号。
  - The `log.error(...)` call is missing its terminating semicolon.
- 捕获到异常后无条件继续循环，没有区分瞬时故障与永久故障，违反了上一节的第一步。
  - The catch block continues the loop unconditionally, without separating transient from permanent faults, which violates step one above.

**修正版 Corrected version**

```java
// 修正版：通用的立即重试助手 / Corrected: a generic immediate-retry helper.
// 依赖 Java 8+ 标准库,日志用 SLF4J 1.7.x / Java 8+ standard library, logging via SLF4J 1.7.x.
// Maven: org.slf4j:slf4j-api:1.7.36
import java.util.concurrent.Callable;
import java.util.function.Predicate;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public final class ImmediateRetry {

  private static final Logger log = LoggerFactory.getLogger(ImmediateRetry.class);

  private ImmediateRetry() {
  }

  // isExpected: 结果是否算成功 / decides whether a returned value counts as success.
  // isTransient: 异常是否值得重试 / decides whether a thrown exception is worth retrying.
  public static <T> T retryNoDelay(
      final Callable<T> callable,
      final int maxAttempts,
      final Predicate<T> isExpected,
      final Predicate<Exception> isTransient) throws Exception {

    if (maxAttempts < 1) {
      throw new IllegalArgumentException("maxAttempts must be at least 1");
    }

    Exception lastFailure = null;

    for (int attempt = 1; attempt <= maxAttempts; attempt++) {
      try {
        final T result = callable.call();
        if (isExpected.test(result)) {
          return result;
        }
        log.info("attempt {} of {} returned an unexpected result", attempt, maxAttempts);
      } catch (Exception e) {
        // 永久性故障立刻上抛,不浪费剩余次数 / a permanent fault is rethrown at once.
        if (!isTransient.test(e)) {
          log.info("attempt {} hit a permanent fault, not retrying", attempt);
          throw e;
        }
        lastFailure = e;
        log.info("attempt {} of {} hit a transient fault", attempt, maxAttempts, e);
      }
    }

    // 次数用尽,明确报错而不是返回 null / the budget is exhausted, so fail loudly.
    throw new IllegalStateException("all " + maxAttempts + " attempts failed", lastFailure);
  }
}
```

#### 立即retry的算术 The arithmetic of immediate retry

> **大白话:** 门铃没人应，一个客人就连按四下；四十个客人都这么做，门口就响了一百六十下——而铃声最密的那一刻，恰好是屋里最忙、最应不过来的那一刻。 / When nobody answers the doorbell, one visitor presses four times; forty visitors doing the same produce one hundred and sixty rings, and the ringing peaks at exactly the moment the household is least able to answer.

假设一个服务正常每秒处理 1000 个请求(1000 requests per second,简称 QPS)，现在它开始失败，而每个客户端在失败后立即重试 3 次。
Suppose a service normally handles 1000 requests per second (QPS) and now begins to fail, while every client retries three times immediately after a failure.

| 每个请求的总尝试次数 Total attempts per request | 放大倍数 Multiplier | 服务端实际承受的 QPS Offered load |
| --- | --- | --- |
| 1 次，不重试 1, no retry | 1x | 1000 |
| 1 次 + 1 次重试 1 + 1 retry | 2x | 2000 |
| 1 次 + 2 次重试 1 + 2 retries | 3x | 3000 |
| 1 次 + 3 次重试 1 + 3 retries | 4x | 4000 |

关键不在于 4000 这个数字，而在于它出现的时刻:恰好是服务最虚弱、最需要流量下降的那一秒。这就是所谓的<font color=OrangeRed>重试放大 retry amplification</font>。
The number 4000 matters less than its timing: it arrives in exactly the second when the service is weakest and most needs traffic to drop. This effect is called <font color=OrangeRed>retry amplification</font>.

### 重试风暴 Retry Storm and Retry Amplification

> **大白话:** 一个客人在餐厅催了 3 次菜，服务员就去催了厨师 3 次，厨师每次又去催了备菜工 3 次——传到最里面的那个人，已经被催了几十次。 / When one diner asks three times, the waiter asks the cook three times per ask, and the cook asks the prep station three times per ask — the person at the far end is chased dozens of times for a single original question.

现代系统的一次调用往往穿过多层服务，每层都独立地实现了自己的重试。这些倍数不是相加，而是相乘。
A single call in a modern system typically passes through several layers of services, each with its own independent retry logic. These multipliers do not add; they multiply.

设每一层对一次失败都发出总共 3 次尝试，则第 n 跳收到的调用数是 3 的 (n-1) 次方。第 1 跳只收到 1 次调用，因为一次用户点击本身只发出一次请求。
If each layer makes a total of three attempts per failure, then the number of calls arriving at hop n is three raised to the power of n minus one. Hop 1 receives exactly one call, because a single user click sends exactly one request.

| 第 n 跳 Hop n | 第 n 跳收到 = 3^(n-1) Calls received = 3^(n-1) | 调用数 Call count |
| --- | --- | --- |
| 1 | 3^0 | 1 |
| 2 | 3^1 | 3 |
| 3 | 3^2 | 9 |
| 4 | 3^3 | 27 |

一次用户点击，在第 4 跳变成了 27 次后端调用。如果每层改成 4 次尝试，第 4 跳就是 64 次。
One user click becomes 27 backend calls at the fourth hop. Raising every layer to four attempts makes the fourth hop 64 calls.

```text
        one user click
              |
              v                1 call into hop 1
        +-----------+
        |  Hop 1    |  API gateway
        +-----------+
         /    |    \           3 attempts
        v     v     v
      +---+ +---+ +---+
      | H2| | H2| | H2|        3 calls into hop 2: order service
      +---+ +---+ +---+
      /|\   /|\   /|\          3 attempts each
     v v v v v v v v v
     [ 9 calls into hop 3: inventory service ]
              |
              v               3 attempts each
     [ 27 calls into hop 4: the database ]
```

缓解办法有三条，通常一起使用。第一，只在一层重试，通常是最靠近用户的那一层或最靠近故障的那一层，其余各层失败即上抛。第二，使用重试预算(retry budget):规定重试流量不得超过正常流量的某个比例，例如 10%,超出即停止重试，这样放大倍数有上限而与层数无关。第三，把"不要重试"的信号随响应向下游传递，例如一个自定义响应头或 gRPC 的元数据，让下游看到该信号后直接失败，不再自行重试。
Three mitigations exist and are normally combined. First, retry at only one layer — usually the layer closest to the user or the layer closest to the fault — and let every other layer propagate the failure immediately. Second, apply a retry budget: cap retry traffic at a fixed fraction of normal traffic, for example ten percent, and stop retrying once the cap is reached, which bounds the multiplier independently of hop depth. Third, forward an explicit "do not retry" signal alongside the response, such as a custom response header or gRPC metadata, so that a downstream service seeing that signal fails fast instead of starting a retry loop of its own.

---

### 有延迟的retry Delayed Retry

> **大白话:** 电话占线时马上按重播，只会再听到一次占线音；隔一会儿再打，对方才有机会挂断上一通电话。 / When a phone line is busy, pressing redial instantly only produces another busy tone; waiting first gives the other side a chance to hang up.

<font color=OrangeRed>retry（重试）</font>指一次请求失败后程序自动把同一个请求再发一遍；delay（延迟）指在两次发送之间故意空等一段时间。 / <font color=OrangeRed>Retry</font> means the program automatically sends the same request again after a failure; delay means deliberately doing nothing between two sends.

- 与其立即retry, 倒不如等待一会，也许那时服务端的负载就降下来了。 / Rather than retrying immediately it is better to wait, because by then the load on the server may have dropped. Here "load" means how much work the remote machine is already handling.
- 这个 delay（延迟）的时间可以是一个常量，也可以是根据一定数学公式变化的变量。 / The delay can be a constant, or a variable computed from a formula.
  - 逐次增加delay算法。 / An algorithm that increases the delay on every successive attempt.
  - Exponential Backoff (指数后退算法): 以指数的方式来增加delay。 / Exponential backoff: each wait is a fixed multiple of the previous one rather than a fixed amount larger.
    - such as 第一次失败等待1秒，第二次再失败等待2秒，接下去4秒，8秒...。 / For example wait 1 second after the first failure, then 2, then 4, then 8.

> 根据自己系统的特性和业务的需求，设计更适合更优化的算法。 / Design a more suitable algorithm according to the characteristics of the system in question and the needs of the business.

#### 固定间隔的 delay Fixed-Interval Delay

> **大白话:** 像每隔 5 秒敲一次门，节奏完全一样；若整栋楼的人都在同一秒敲同一扇门，那扇门每 5 秒挨一次集体撞击。 / It is like knocking every 5 seconds; if everyone in the building knocks on the same door at the same second, that door takes one collective impact every 5 seconds.

- delay 的方式按照是方法本身是异步还是同步的，可以通过定时器或则简单的 `Thread.sleep` 实现 / The delay uses a timer or a simple `Thread.sleep` depending on whether the method is asynchronous (the thread continues and work resumes later) or synchronous (the thread stops and waits).
- 虽然这次带了固定间隔的 backoff，但是**每次重试的间隔固定** / Although this version adds a fixed-interval backoff, **the gap between retries is always identical**.
- 此时对于下游资源的冲击将会变成间歇性的脉冲； / The pressure on the downstream resource then becomes an intermittent pulse, meaning traffic arrives in sharp bursts instead of spreading out.
- 特别是当集群都遇到类似的问题时，步调一致的脉冲，将会最终对资源造成很大的冲击，并陷入失败的循环中。 / Especially when every machine in the cluster hits a similar problem the pulses become synchronised, straining the resource and trapping the system in a loop of failures.

```java
public static <T> T retry(
  final Callable<T> callable, final int maxAttempts, final int fixedBackOff){
    for (int i = 0; i < maxAttempts; i++) {
      try {
        final T t = callable.call();
        if (isExpected(t)){ return t};
      }
      catch (Exception e) {
        log.error("error")
        try {
          Thread.sleep(fixedBackOff);
        }
        catch (Exception ee) {}
      }
    }
    // return default t or error
    return null;
  }
```

```java
private T retry(Supplier<T> function) throws RuntimeException {
    log.error("1st command failed, will be retired " + maxRetires + "times.");
    invokeCnt = 0;
    Exception exception = null;

    while ( invokeCnt < maxRetires) {
      try {
        if (sleepTime > MIN_SLEEP_TIME && sleepTime <= MAX_SLEEP_TIME) {
          Thread,sleep(sleepTime);
        }
        return function.get();
      }
      catch (InterrunptedException ex) {...}
      catch (Exception ex) {
        exception = ex;
        invokeCnt++;
        log.error(invokeCnt + " times return failed of " + maxRetires + " error: " + ex);
        if ( invokeCnt > maxRetires) {...}
      }
    }
    throw new RuntimeException(maxRetires + " retires all fails", exception);
  }
```

| 缺陷 Defect, 第二段代码 second block | 原文 As written | 为什么坏掉 What breaks |
| --- | --- | --- |
| (a) 逗号写成点 Comma instead of dot | `Thread,sleep(sleepTime)` | 逗号不是成员访问符，编译器读成两个表达式，直接编译失败。 / A comma is not the member-access operator, so the compiler reads two expressions and the file does not compile. |
| (b) 异常类名拼错 Exception misspelled | `catch (InterrunptedException ex)` | 正确类名是 `InterruptedException`，多了一个 n 的类并不存在。 / The correct name is `InterruptedException`; the extra "n" names a class that does not exist. |
| (c) 循环条件与内部判断矛盾 Contradictory guard | `while (invokeCnt < maxRetires)` 内又判断 `if (invokeCnt > maxRetires)` | 进入循环即证明计数小于上限，加一后最多等于上限，永不大于，该 if 是死代码；`maxRetires` 也是 `maxRetries` 的拼写错误。 / Entering the loop proves the counter is below the limit and one increment can at most reach it, so the inner branch is unreachable dead code; `maxRetires` also misspells `maxRetries`. |

**修正版 Corrected version**

```java
// 修正: 点号 Thread.sleep, 正确的 InterruptedException, 删除死代码, maxRetries 拼写
// Corrected: dot operator, correct exception name, dead branch removed, spelling fixed.
private T retry(Supplier<T> function) {
    int invokeCnt = 0;
    Exception last = null;
    while (invokeCnt < maxRetries) {
      try {
        if (sleepTime > MIN_SLEEP_TIME && sleepTime <= MAX_SLEEP_TIME) { Thread.sleep(sleepTime); }
        return function.get();
      }
      catch (InterruptedException ex) {
        Thread.currentThread().interrupt();
        throw new RuntimeException("interrupted while retrying", ex);
      }
      catch (Exception ex) { last = ex; invokeCnt++; log.error("attempt {} failed", invokeCnt, ex); }
    }
    throw new RuntimeException(maxRetries + " retries all failed", last);
  }
```

#### 随机 delay 的方式 Randomised Delay

> **大白话:** 一群人同时冲向同一个银行窗口会堵死；给每人随机分配一个略有不同的到达时刻，队伍就自然散开。 / A crowd rushing one bank counter at the same instant jams it; giving each person a randomly shifted arrival time spreads the queue out.

- 采用随机 backoff 的方式，即具体的 delay 时间在一个最小值和最大值之间浮动 / With randomised backoff the actual delay floats between a minimum and a maximum.
- 虽然解决了 backoff 的时间集中的问题，对时间进行了随机打散，但是依然存在下面的问题： / This spreads the wait times out, but the following issues remain.
- 如果依赖的底层服务持续地失败，改方法依然会进行固定次数的尝试，并不能起到很好的保护作用 / If the dependency keeps failing this method still performs a fixed number of attempts, so it offers little real protection.
- 对结果是否符合预期，是否需要进行重试依赖于异常 / Deciding whether the result is acceptable, and therefore whether to retry, depends entirely on exceptions being thrown.
- 无法针对异常进行精细化的控制，如只针部分异常进行重试。 / There is no per-exception control, such as retrying only a subset of exception types.

```java

public static <T> T retryWithRandomDelay(
  final Callable<T> callable,
  final int maxAttempts,
  final int minBackOff,
  final int maxBackOff,
  // randomFactor, 0.0 - 1.0
  final double randomFactor) {
    for (int i = 0; i < maxAttempts; i++) {
      try {
        final T t = callable.call();
        if (isExpected(t)) {
          return t
        };
      }
      catch (Exception e) {
        log.error("error")
        try {
          final double rnd = 1.0 + ThreadLocalRandom.current().nextDouble() * randomFactor;
          long backOffTime;
          try {
            backOffTime = (long)(Math.min(maxBackoff, minBackoff * Math.pow(2, i)) * rnd);
          }
          catch (Exception ee) {
            backOffTime = maxBackoff;
          }
          Thread.sleep(backOffTime);
        }
        catch (Exception ee) {}
      }
    }
    // return default t or error
    return null;
  }
```

```java
public static <V> V retryWithRandomDelay(
  final Callable<V> callable,
  final int maxRetryTime,
  final int sleepInMills) throws Exception {
    if (maxRetryTime >= 10) {...}
    if (sleepInMills <= 0) {...}

    try {
      return callable.call();
    }
    catch (Throwable e) {
      if (maxRetryTime <= 0) {...}
      else {
        try {
          LOGGGER.error(
            "retry with maxRetryTime:{}, sleepInMills:{}, error:{}",
            maxRetryTime,sleepInMills,e
          )
          Thread.sleep(sleepInMills);
          return retryWithBackoff(
            callable,
            maxRetryTime: maxRetryTime-1,
            sleepInMills: sleepInMills * ThreadLocalRandom.current().nextDouble(origin:1, bound: 3));
        }
        catch (InterrunptedException ex) {
          Thread.currentThread().interrupt();
          throw e;
        }
      }
    }
  }
```

| 缺陷 Defect, 上面两段代码 the two blocks above | 原文 As written | 为什么坏掉 What breaks |
| --- | --- | --- |
| (d1) 递归调用不存在的方法 Call to an undefined method | `return retryWithBackoff(...)` | 笔记里从未定义 `retryWithBackoff`，名字也与自身 `retryWithRandomDelay` 不一致，符号无法解析。 / `retryWithBackoff` is never defined in the note and does not match the enclosing method name, so the symbol cannot be resolved. |
| (d2) double 传给 int 形参 A double passed into an int parameter | `sleepInMills: sleepInMills * ...nextDouble(...)` | `nextDouble` 返回 double，乘积也是 double，而形参是 `int`；Java 不做隐式窄化，必须显式取整。 / The product is a double while the parameter is `int`, and Java performs no implicit narrowing, so an explicit cast or rounding is required. |
| (e) 变量名大小写不一致 Inconsistent capitalisation | 形参 `minBackOff`/`maxBackOff`，方法体写 `minBackoff`/`maxBackoff` | Java 区分大小写，方法体引用了从未声明的标识符，报 cannot find symbol。 / Java is case sensitive, so the body refers to identifiers that were never declared and the compiler reports "cannot find symbol". |
| (b) 同一异常拼写错误再现 Same misspelling recurs | `catch (InterrunptedException ex)` | 与上一节同一个错误，正确写法 `InterruptedException`。 / The same defect as in the previous subsection; the correct spelling is `InterruptedException`. |

**修正版 Corrected version**

```java
// 修正: 名称统一, 递归调用自身, 显式取整, 异常拼写正确 / Corrected: consistent names,
// self-recursive call, explicit rounding, correct exception spelling.
public static <V> V retryWithRandomDelay(
  final Callable<V> callable, final int remainingRetries, final int sleepInMillis)
  throws Exception {
    try { return callable.call(); }
    catch (Exception e) {
      if (remainingRetries <= 0) { throw e; }
      try {
        Thread.sleep(sleepInMillis);
        final int next = (int) Math.round(
          sleepInMillis * ThreadLocalRandom.current().nextDouble(1.0, 3.0));
        return retryWithRandomDelay(callable, remainingRetries - 1, next);
      }
      catch (InterruptedException ex) { Thread.currentThread().interrupt(); throw e; }
    }
  }
```

#### 四种 backoff 策略对比 Four Backoff Strategies Compared

> **大白话:** 四种策略就是四种敲门节奏：一直猛敲、每 5 秒敲一次、越敲越慢、越敲越慢且每人节奏都不同。 / The four strategies are four knocking rhythms: hammer non-stop, knock every 5 seconds, slow down progressively, or slow down progressively with a different rhythm per person.

下表中 base = 1 秒，倍数 2，<font color=OrangeRed>cap</font>（单次等待上限）= 30 秒，用于阻止指数增长变成几小时。 / Below, base = 1 second, the multiplier is 2, and the <font color=OrangeRed>cap</font>, the maximum single wait, is 30 seconds, which stops exponential growth from reaching hours.

| 策略 Strategy | 公式 Formula | 第1至第5次等待秒数 Waits 1-5 (s) | 未解决的失败模式 Failure mode not solved |
| --- | --- | --- | --- |
| 无延迟 No delay | `0` | 0, 0, 0, 0, 0 | 立刻放大流量，把过载的服务彻底压死。 / Instantly amplifies traffic and finishes off an overloaded service. |
| 固定间隔 Fixed delay | `base` | 1, 1, 1, 1, 1 | 所有客户端节奏一致形成周期脉冲，长故障时压力不下降。 / All clients share one rhythm, producing periodic pulses, and pressure never drops during a long outage. |
| 指数无抖动 Exponential, no jitter | `min(cap, base * 2^(n-1))` | 1, 2, 4, 8, 16 | 总量下降了，但同时失败的客户端仍在同一秒集中醒来。 / Volume drops, yet clients that failed together still wake in the same second. |
| 指数加全抖动 Exponential, full jitter | `uniform(0, min(cap, base * 2^(n-1)))` | 0.4, 1.7, 2.2, 5.9, 11.3（随机样例 one sample） | 仍无法停止对永久故障的持续重试，那需要熔断器与重试预算。 / It still cannot stop endless retries against a permanent fault; that needs a circuit breaker and a retry budget. |

#### 抖动 jitter 到底解决什么问题 What Jitter Actually Fixes

> **大白话:** 一千个人的闹钟都设在同一秒响，于是一千个人同时冲进同一个洗手间；把每个闹钟随机挪几分钟，同一个洗手间就够用了。 / A thousand alarm clocks set to the same second send a thousand people into one bathroom at once; shifting each alarm randomly makes the same bathroom sufficient.

这个现象叫 <font color=OrangeRed>thundering herd（惊群效应）</font>：共享依赖短暂宕机时，所有调用方在同一时刻收到失败，第一次重试也落在同一时刻；只要公式是确定性的，即使等待按指数增长，大家的时刻表依然完全相同，依赖刚恢复的瞬间又被重试洪峰打垮。 / This is the <font color=OrangeRed>thundering herd</font>: when a shared dependency fails briefly, every caller receives its failure at the same instant, so every first retry lands at the same instant; a deterministic formula gives everyone an identical timetable even with exponential growth, and the dependency is knocked over again the moment it recovers.

jitter（抖动）就是往等待时间里注入随机数把时刻表打散；实践中有三个有名公式，下面每个都是可运行的 python 函数，只用标准库，`random` 是 Python 3 自带模块，无需安装。 / Jitter injects randomness into the wait so the timetables diverge; three named formulas are used in practice, each shown below as a runnable python function using only the standard library, since `random` ships with Python 3.

```python
import random

BASE, CAP = 1.0, 30.0  # 中文: 基础秒数与单次上限 / English: base seconds and per-attempt cap

def full_jitter(attempt: int) -> float:
    """完全抖动: 0 到指数上界均匀取值 / Full jitter: uniform over the whole interval."""
    return random.uniform(0.0, min(CAP, BASE * (2 ** (attempt - 1))))

def equal_jitter(attempt: int) -> float:
    """等量抖动: 一半固定一半随机 / Equal jitter: half fixed, half random."""
    half = min(CAP, BASE * (2 ** (attempt - 1))) / 2.0
    return half + random.uniform(0.0, half)

def decorrelated_jitter(previous: float) -> float:
    """去相关抖动: 以上一次实际等待为种子 / Decorrelated: seeded by the previous wait."""
    return min(CAP, random.uniform(BASE, previous * 3.0))
```

| 公式 Formula | 何时优先选择 When to prefer it |
| --- | --- |
| full jitter | 默认推荐；公式最简单，方差最大，打散效果最好。 / The default; simplest formula, widest spread, best dispersion. |
| equal jitter | 过早重试代价很高、需要保证一个最小等待时间时。 / When retrying too soon is expensive and a guaranteed minimum wait is required. |
| decorrelated jitter | 长故障中等待仍需持续增长，同时要避免时刻表相关性时。 / When waits must keep growing during long outages while avoiding correlated timetables. |

明确一点：**没有特殊理由就选 full jitter**，它公式最简单、打散效果好，也是 AWS 架构博客给出的默认建议；不过在该博客自己的模拟里，full jitter 与 decorrelated jitter 表现相当，其中 decorrelated jitter 发出的调用次数更少，博客作者本人也表示会选 decorrelated jitter。 / To state it plainly: **choose full jitter unless there is a specific reason not to**; it is the simplest formula, it spreads well, and it is the default suggested in the AWS architecture blog. In that blog's own simulation, however, full jitter and decorrelated jitter perform comparably, with decorrelated jitter issuing fewer calls, and the post's author states a preference for decorrelated jitter.

#### 可运行的调度模拟 A Runnable Schedule Simulation

> **大白话:** 与其相信文字里的秒数，不如自己跑一遍脚本把真实等待表打印出来。 / Rather than trusting the numbers in prose, run the script and print the real wait table.

存成 `backoff_demo.py` 后执行 `python3 backoff_demo.py`，仅用标准库，无需 pip 安装。 / Save as `backoff_demo.py` and run `python3 backoff_demo.py`; standard library only, so no pip install is needed.

```python
import random

BASE, CAP, ATTEMPTS = 1.0, 30.0, 5

def expo(n: int) -> float:
    return min(CAP, BASE * (2 ** (n - 1)))

STRATEGIES = {
    "no delay": lambda n: 0.0,
    "fixed delay": lambda n: BASE,
    "exp no jitter": expo,
    "exp full jitter": lambda n: random.uniform(0.0, expo(n)),
    "exp equal jitter": lambda n: expo(n) / 2 + random.uniform(0.0, expo(n) / 2),
}

def decorrelated(count: int) -> list:
    out, prev = [], BASE  # 中文: 依赖上一次结果 / English: depends on the previous wait
    for _ in range(count):
        prev = min(CAP, random.uniform(BASE, prev * 3.0))
        out.append(prev)
    return out

if __name__ == "__main__":
    random.seed(42)  # 中文: 固定种子便于复现 / English: reproducible output
    span = range(1, ATTEMPTS + 1)
    print("strategy".ljust(18) + "".join(f"a{i:<7}" for i in span) + "total")
    rows = {name: [fn(i) for i in span] for name, fn in STRATEGIES.items()}
    rows["exp decorrelated"] = decorrelated(ATTEMPTS)
    for name, waits in rows.items():
        print(name.ljust(18) + "".join(f"{w:<8.2f}" for w in waits) + f"{sum(waits):.2f}")
```

最后一列 total 是关键：它是所有等待之和，也就是这条策略最少会把一个用户请求挂住多久。 / The final `total` column matters most: it is the sum of all waits, the minimum time this policy holds a user request open.

#### 必须给重试设上限 Always Bound the Retries

> **大白话:** 餐厅催菜有三个上限：最多催几次、每次等厨房回话多久、整桌最晚几点必须吃到饭；前两个合理并不代表第三个不会爆。 / Chasing a dish has three limits: how many times to ask, how long to wait for each answer, and the latest moment the table must be fed. The first two being reasonable does not mean the third holds.

| 上限 Bound | 含义 Meaning | 不设会怎样 Consequence of omitting it |
| --- | --- | --- |
| 最大尝试次数 Max attempt count | 含首次调用在内总共允许发出几次请求。 / The total number of requests permitted, counting the first call. | 对永久故障无限重试，把下游流量放大数倍。 / Unbounded retries against a permanent fault multiply downstream traffic. |
| 单次超时 Per-attempt timeout | 一次请求最多等多久回应，超过即算失败。 / The maximum time one request may wait for a response before counting as failed. | 卡住的连接永久占用线程和连接池，导致资源耗尽。 / A stalled connection holds a thread and a pool slot forever, exhausting resources. |
| 总截止时间 Total deadline | 从最初调用算起，整个重试过程最晚必须结束的时刻。 / The absolute moment by which the whole retry process must finish, measured from the original call. | 次数与单次超时都正常，端到端耗时仍会失控。 / Attempt count and per-attempt timeout can both look fine while end-to-end latency runs away. |

- <font color=OrangeRed>总截止时间 total deadline</font> 最重要。设最大尝试 5 次、单次超时 30 秒、指数等待 1+2+4+8 秒，单看每一项都合理：30 秒是常见默认值，5 次听起来很保守。 / The <font color=OrangeRed>total deadline</font> matters most. Assume 5 attempts, a 30-second per-attempt timeout, and waits of 1+2+4+8 seconds; each number looks reasonable alone, since 30 seconds is a common default and 5 attempts sounds conservative.
- 最坏情况是 5 次全部超时，5 x 30 = 150 秒，加上 15 秒等待共 165 秒。面向用户的请求被挂住近三分钟，而浏览器和负载均衡器通常在 60 秒左右就已断开连接。 / The worst case is all 5 attempts timing out: 5 x 30 = 150 seconds plus 15 seconds of waiting gives 165 seconds. A user-facing request is held open for nearly three minutes, while browsers and load balancers typically drop the connection around 60 seconds.
- 结论是必须设一个总截止时间（例如 3 秒），每次重试前检查剩余预算；剩余时间不足就立即放弃，而不是再发一个注定被上层丢弃的请求。 / The conclusion is that a total deadline such as 3 seconds must exist and the remaining budget must be checked before every retry; when too little time remains the operation gives up rather than sending one more request whose answer will be discarded.

#### 重试预算 Retry Budgets

> **大白话:** 给整个服务发一叠有限的重试券，用完就不能再重试，这样重试流量永远只占正常流量的一小部分。 / Issue the service a limited stack of retry tickets; once spent no further retries are allowed, so retry traffic stays a small fraction of normal traffic.

即使每个请求都遵守上面三个上限，成千上万个请求同时重试仍能把下游流量翻倍。<font color=OrangeRed>retry budget（重试预算）</font>把重试量限制为总流量的一个小比例，业界常用约 10%，通常用 token bucket（令牌桶）实现：正常请求按比例投放令牌，每次重试消耗一个，桶空则拒绝重试。 / Even when every request honours the three bounds above, thousands of simultaneous retries can double downstream traffic. A <font color=OrangeRed>retry budget</font> caps retries at a small percentage of total traffic, commonly around 10 percent, usually via a token bucket: normal traffic deposits tokens at a fixed ratio, each retry spends one, and retries are refused when the bucket is empty.

```python
import threading

class RetryBudget:
    """令牌桶: 每 1/ratio 次正常请求换 1 张重试券 / One ticket per 1/ratio requests."""
    def __init__(self, ratio: float = 0.1, capacity: int = 100) -> None:
        # 中文: 必须用整数计数。0.1 没有精确的二进制表示, 若直接累加浮点数,
        # 十次之后只得到 0.9999999999999999, 每十张券就凭空少一张。
        # English: count in integers. 0.1 has no exact binary form, so adding
        # floats leaves 0.9999999999999999 after ten calls and loses one
        # ticket in every ten.
        self._per_retry = round(1 / ratio)
        self._capacity, self._credits, self._tokens = capacity, 0, 0
        self._lock = threading.Lock()

    def record_request(self) -> None:
        with self._lock:
            self._credits += 1
            if self._credits >= self._per_retry:
                self._credits -= self._per_retry
                self._tokens = min(self._capacity, self._tokens + 1)

    def try_retry(self) -> bool:
        with self._lock:
            if self._tokens < 1:
                return False
            self._tokens -= 1
            return True
```

- ratio 设为 0.1 意味着每 10 次正常请求换来 1 张券，100 次正常请求正好换来 10 次重试；实测 100 次 `record_request()` 之后 `try_retry()` 恰好成功 10 次。 / A ratio of 0.1 mints one ticket per 10 normal requests, so 100 normal requests fund exactly 10 retries; running the class above, 100 calls to `record_request()` are followed by exactly 10 successful `try_retry()` calls.
- 这里的 10% 是**长期平均**的天花板，不是瞬时上限。上面的实现没有时间衰减，早先健康流量攒下的令牌会一直留在桶里，故障瞬间可以被一次性花光：capacity 设为 100 就意味着允许一次接近 100 次重试的突发。 / The 10 percent figure is a **long-run average** ceiling, not an instantaneous one. The implementation above has no time decay, so tokens minted by earlier healthy traffic stay in the bucket and can all be spent the moment a fault appears: a capacity of 100 permits a burst of nearly 100 retries.
- 生产实现通常改用衰减窗口并加一个最小并发下限：Envoy 的 retry_budget 和 Finagle 的重试预算都是衰减窗口加最小并发下限。 / Production implementations normally use a decaying window plus a minimum-concurrency floor: both Envoy's retry_budget and Finagle's retry budget are built as a decaying window with a minimum-concurrency floor.
- 预算应按下游依赖分别统计，否则一个坏依赖会耗尽其他所有依赖的重试券。 / Budgets should be tracked per dependency, otherwise one broken dependency drains the tickets the others rely on.

---

### Circuit Breaker(断路器) Circuit Breaker

> **大白话:** 重试就像对着一个已经关门的餐厅反复敲门，敲一百次门也不会开；断路器的作用是在门上挂一张"暂停营业"的牌子，让后面来的人看一眼牌子就直接走，不用再排队敲门。 / Retrying is like knocking again and again on a restaurant door that is already locked; a hundred knocks will not open it. A circuit breaker hangs a "closed" sign on the door so that everyone arriving afterwards reads the sign and leaves immediately, instead of queueing up to knock.

`Transient fault(瞬时故障)` 的定义见前面的 "什么情况下要 retry When to Retry" 一节。
The definition of a transient fault appears earlier, in the "什么情况下要 retry When to Retry" section.

- 如果 `Transient fault` 修复的时间特别长, 比如长时间的网络问题，那就算有再好的retry机制，也免不了是徒劳。
  If the transient fault takes a very long time to heal, for example a network outage that lasts minutes, then even the best retry mechanism is wasted effort.
  - 只会一次又一次地retry, 失败，再retry, 直到达到上限。
    The client simply retries, fails, retries again, and keeps going until the retry limit is reached.
  - 一来浪费资源，二来或许又会干扰服务端的自我修复。
    First this wastes resources on both sides; second the extra load can actively interfere with the server's own recovery.
  - 断路器模式 一般用在当下游资源失败后，但是失败恢复的时间不固定时，自动地进行探索式地恢复尝试，并且在遇到较多失败时，能够快速自动地断开，从而避免失败蔓延的一种模式。
    The circuit breaker pattern is used when a downstream resource has failed and the recovery time is unpredictable. It probes for recovery automatically, and when failures pile up it disconnects automatically and quickly, so that the failure does not spread.
  - 当断路器处于开断状态时，所有的请求都会直接失败，不再会对下游资源造成冲击，并能够在一段时间后，进行探索式的尝试，如果没有达到条件，可以自动地恢复到之前的闭合状态。
    While the breaker is in the disconnected state, every request fails immediately and no traffic hits the downstream resource. After a while the breaker sends a probe, and once the probe indicates health it returns to the previous connected state automatically.

- Circuit Breaker (断路器)的设计模式: 原意其实就是电路中的开关
  The circuit breaker design pattern borrows its name from a literal switch in an electrical circuit.
  - 在电路里一旦开关断开，电流就别想通过了。
    Once the switch in a circuit is open, no current can pass through it.
  - 一旦开关断开，就不会再发送任何请求了。
    Once the software breaker is open, no request is sent any more.

- Circuit Breaker在retry机制中的应用是一个状态机
  Inside a retry mechanism the circuit breaker is implemented as a state machine, meaning an object that is always in exactly one named state and moves between states on defined events.
  - 有三种状态：**OPEN, HALF-OPEN, CLOSE**。
    There are three states: **OPEN**, **HALF-OPEN**, and **CLOSE**.
  - 设定一个 `threshold(阈值)` 和一个 `timeout`，
    Two settings are required: a `threshold`, meaning how many failures are tolerated before tripping, and a `timeout`, meaning how long the breaker stays open before probing again.
  - 当retry的次数超过 `threshold` 时，认为服务端进入一个较长的`Trasient fault`。
    When the number of failed attempts exceeds the `threshold`, the breaker concludes that the server has entered a long transient fault rather than a momentary blip.
    - 那么就开关断开，进入 **OPEN** 状态。
      The switch opens and the breaker enters the **OPEN** state.
    - 这时将不再向服务端发送任何请求，就像开关断开了，电流（请求）怎么也不会从客户端流向服务端。
      No request reaches the server in this state, exactly as no current can flow across an open switch, where the current stands for the requests travelling from client to server.
  - 当过了一段时间到了 `timeout`，就将状态设为 **HALF-OPEN**
    Once the `timeout` has elapsed, the state changes to **HALF-OPEN**.
    - 这时会尝试把客户端的请求发往服务端去试探它是否已经恢复。
      In this state one request is allowed through to the server as a probe, to test whether the server has recovered.
    - 如果是就进入 **CLOSE** 状态，回到正常的机制中
      If the probe succeeds, the breaker moves to **CLOSE** and normal operation resumes.
    - 如果不是，就再次进入 **OPEN** 状态。
      If the probe fails, the breaker returns to **OPEN**.

> 既节约了资源，防止了无休止的无用的尝试，
> 又保证了在修复后，客户端能知晓，并恢复的正常的运行。

上面这段引文的英文含义 The English meaning of the quotation above:

> Resources are conserved and endless useless attempts are prevented,
> while the client is still guaranteed to notice the recovery and return to normal operation.

![Circuit breaker state machine showing Closed, Open and Half-Open states, with Trip Breaker, Attempt Reset and Reset Breaker transitions](/assets/img/post/circuit-breaker-state-machine-closed-open-halfopen.png)

图中每条箭头的含义 What each labelled arrow in the diagram means:

- **Success（Closed 上的自环）**：请求成功后，断路器留在 Closed 状态，失败计数被清零。
  **Success (the self-loop on Closed)**: after a successful call the breaker stays in Closed and the failure counter is reset to zero.
- **Trip Breaker（Closed → Open）**：连续失败次数达到 `threshold`，开关跳闸，进入 Open。
  **Trip Breaker (Closed to Open)**: the consecutive failure count reaches the `threshold`, the switch trips, and the breaker enters Open.
- **Calls failing fast（Open 上的自环）**：Open 期间的每一个请求都被立刻拒绝，根本不发出网络调用。
  **Calls failing fast (the self-loop on Open)**: every request during Open is rejected immediately and no network call is issued at all.
- **Attempt Reset（Open → Half-Open）**：等待时间到了 `timeout`，断路器主动进入 Half-Open，准备放一个探测请求。
  **Attempt Reset (Open to Half-Open)**: once the wait reaches the `timeout`, the breaker moves itself into Half-Open and prepares to let one probe request through.
- **Reset Breaker（Half-Open → Closed）**：探测请求成功，说明下游已恢复，断路器合上，流量全量恢复。
  **Reset Breaker (Half-Open to Closed)**: the probe succeeds, which shows the downstream service has recovered, so the breaker closes and full traffic resumes.
- **Trip Breaker（Half-Open → Open）**：探测请求仍然失败，立刻重新跳闸，再等一个完整的 `timeout`。
  **Trip Breaker (Half-Open to Open)**: the probe still fails, so the breaker trips again immediately and waits another full `timeout`.

命名提示 A note on naming: 图里写的是 **Closed**，上面的文字写的是 **CLOSE**，两者指的是同一个状态——开关合上、请求正常通过。
The diagram spells the state **Closed** while the surrounding prose writes **CLOSE**; these are the same state, meaning the switch is shut and requests flow normally.

在应用断路器时，需要对下游资源的每次调用都通过断路器，对代码具备一定的结构侵入性。常见的有 Hystrix 或 resilience4j.
Adopting a breaker requires every call to the downstream resource to be routed through the breaker object, so the pattern is somewhat intrusive to the structure of the code. The commonly used libraries are Hystrix and resilience4j.

---

#### 断路器到底是什么 What a Circuit Breaker Actually Is

> **大白话:** 家里电器开太多会跳闸，跳闸是为了不让电线烧起来。软件里的断路器就是同一个开关，只不过它切断的是请求，而不是电流。 / Running too many appliances at home trips the breaker, and the trip exists so that the wiring does not catch fire. A software breaker is the same switch, except that what it cuts off is requests rather than electric current.

家里的电路板上有一个**保险开关（空气开关）**。
A household distribution board contains a **safety switch**, also called a miniature circuit breaker.

- 平时家电正常用电，开关就是合上的，电流哗哗地流过去，电视、冰箱都能用。可是如果家里同时开了太多电器，电流一下子变得特别大，继续这样下去电线会发热甚至起火——这时**保险开关**会自动"跳闸"，啪地一声把电路断开，不让电流再往下走了。
  Normally the switch is closed, current flows freely, and the television and the refrigerator both work. If too many appliances run at once the current spikes, and if that continued the wiring would overheat or even catch fire, so the safety switch <font color=OrangeRed>trips</font> automatically, snapping the circuit open and stopping the current from going any further.
- 跳闸之后，家里没电了，看起来很不方便，但其实这是在保护整个房子不被烧掉。
  After the trip the home has no power, which looks inconvenient, but the inconvenience is what protects the whole house from burning down.
- 等电工检查过线路、把问题解决了，再把开关重新合上，家里就又有电了。
  Once an electrician has inspected the wiring and fixed the problem, flipping the switch back on restores power.
- 软件里的"断路器"用的就是同一个道理，只不过流过去的不是电流，而是一次次向服务器发出的请求。
  A software circuit breaker works on exactly the same principle, except that what flows through it is not current but the stream of requests being sent to a server.

对照表 The Analogy Mapping Table:

| 家里的电路 Household Electrical Analogy | 软件里的断路器 Software Circuit Breaker |
| --- | --- |
| 保险开关合上，电流正常通过 The switch is closed, current flows normally | **CLOSE(闭合)** 状态：请求正常发往服务端 Requests are sent to the server normally |
| 用电太多，线路过载 Too many appliances draw too much current, the wiring overloads | 失败次数超过 `threshold`（阈值）Failures exceed the configured `threshold` |
| 啪！跳闸，断电保护房子 The breaker trips, cutting power to protect the house | **OPEN(断开)** 状态：请求被直接拒绝，根本不会打到服务端，避免火烧连营 Requests are rejected immediately, never reaching the server, preventing a cascading failure |
| 过一会儿，电工试探性地合上开关看看修好没有 After a while, an electrician tentatively flips the switch to test whether the wiring is fixed | **HALF-OPEN(半开)** 状态：过了 `timeout` 后放一小部分请求去试探服务端是否恢复 After the `timeout`, a small number of test requests are let through to probe whether the server has recovered |
| 电修好了，正式恢复供电 The wiring is fixed, power is fully restored | 试探请求成功 → 回到 **CLOSE** 状态 The probe succeeds → back to **CLOSE** |
| 电还没修好，再次跳闸 The wiring is still broken, the breaker trips again | 试探请求失败 → 回到 **OPEN** 状态，再等一个 `timeout` The probe fails → back to **OPEN**, wait another `timeout` |

Retry 和断路器的区别 The difference between Retry and a circuit breaker:

- Retry 就像打电话占线了就一直重打
  A retry is like redialling a phone number over and over because the line is busy.
- 而断路器是发现对方压根没人接、已经打了好多次都没用，干脆先别打了，等一会儿再打一次探探路，省得白白浪费电话费。
  A breaker notices that nobody is picking up at all and that many attempts have already been useless, so it stops dialling entirely, waits a while, then places a single call to test the line, rather than burning through call charges for nothing.

以下是断路器状态机的简单示意图 A simple diagram of the circuit breaker state machine:

```bash
        失败次数 >= threshold
   ┌──────────────────────────────┐
   │                              ▼
 CLOSE(闭合，正常放行请求)      OPEN(断开，直接拒绝请求)
   ▲                              │
   │                       过了 timeout 时间
   │ 试探请求成功                  ▼
   └───────────────────  HALF-OPEN(半开，放一小部分探测请求)
                                  │
                          试探请求失败，回到 OPEN
```

同一张图的纯 ASCII 版本，方便在不支持制表符的终端里查看 The same diagram in plain ASCII, for terminals that do not render box-drawing characters:

```text
             failures >= threshold  (Trip Breaker)
   +---------------------------------------------------+
   |                                                   v
CLOSE  (switch shut, requests pass through)      OPEN (switch open, requests rejected instantly)
   ^                                                   |
   |                                        timeout elapsed (Attempt Reset)
   |  probe succeeded (Reset Breaker)                   v
   +----------------------------------  HALF-OPEN (exactly one probe request allowed)
                                                       |
                                          probe failed -> back to OPEN
```

---

#### 一次完整的跳闸时间线 A Complete Trip Timeline

> **大白话:** 下面这张表就像餐厅门口的监控录像回放，一分钟一分钟地看清楚"敲门—贴牌子—撕牌子"整个过程。 / The table below plays back the whole episode like security-camera footage at the restaurant door, second by second, from knocking to hanging the sign to taking it down again.

配置 The configuration used in this walkthrough:

| 参数 Setting | 取值 Value | 含义 Meaning |
| --- | --- | --- |
| `failureThreshold` | 5 | 连续失败 5 次就跳闸 Five consecutive failures trip the breaker |
| `openTimeout` | 30s | 跳闸后保持 OPEN 30 秒，然后才允许探测 The breaker stays OPEN for 30 seconds before a probe is allowed |
| `callTimeout` | 2s | 单次调用最多等 2 秒 A single call waits at most 2 seconds for a response |

关键概念 <font color=OrangeRed>fail fast(快速失败)</font>：在 OPEN 状态下请求不会走网络，断路器立刻抛错，耗时通常不到 1 毫秒。
The key concept here is <font color=OrangeRed>fail fast</font>: while the breaker is OPEN no network call happens at all, the breaker raises an error immediately, and the whole attempt typically costs under one millisecond.

| 时间 Time | 事件 Event | 失败计数 Failure counter | 断路器状态 Breaker state | 调用方拿到什么 What the caller receives |
| --- | --- | --- | --- | --- |
| T+0.0s | 正常请求，服务端返回成功 A normal request, the server answers successfully | 0 | CLOSE | HTTP 200，耗时约 30ms HTTP 200 in roughly 30ms |
| T+0.1s | 第 1 次失败，服务端超时 First failure, the server times out | 1 | CLOSE | 错误，等满 2 秒才返回 An error, returned only after the full 2 seconds |
| T+2.5s | 第 2 次失败 Second failure | 2 | CLOSE | 错误，又等了 2 秒 An error after another 2 seconds |
| T+5.0s | 第 3 次失败 Third failure | 3 | CLOSE | 错误 An error |
| T+7.5s | 第 4 次失败 Fourth failure | 4 | CLOSE | 错误 An error |
| T+10.0s | 第 5 次失败，达到阈值，触发 Trip Breaker Fifth failure, the threshold is reached, Trip Breaker fires | 5 → 0（跳闸时清零 zeroed at the trip） | CLOSE → OPEN | 错误；同时断路器跳闸 An error, and the breaker trips at the same moment |
| T+10.001s | 下一个请求被断路器直接拦下，没有发出网络调用 The next request is blocked by the breaker itself, no network call is issued | 0 | OPEN | `CircuitBreakerOpenException`，不到 1ms 返回 `CircuitBreakerOpenException` returned in under 1ms |
| T+11s ~ T+39s | 这 28 秒内成千上万个请求全部被瞬间拒绝，服务端一个请求也没收到 Over these 28 seconds thousands of requests are rejected instantly and the server receives none of them | 0（被拒绝的请求不累加 rejected calls do not add to it） | OPEN | 立即报错，线程不被占用 An immediate error, and no thread is tied up waiting |
| T+40.0s | 跳闸后满 30 秒，Attempt Reset 触发 Thirty seconds after the trip, Attempt Reset fires | 0 | OPEN → HALF-OPEN | 尚无返回，下一个请求将成为探测请求 Nothing returned yet, the next request becomes the probe |
| T+40.1s | 唯一一个探测请求真正发往服务端，其余并发请求仍被拒绝 The single probe request is genuinely sent to the server while other concurrent requests are still rejected | 0 | HALF-OPEN | 探测方正常等待响应，其余调用方仍立即报错 The probing caller waits for a real response, all other callers still get an immediate error |
| T+40.3s | 结局甲：探测成功，Reset Breaker 触发 Ending A: the probe succeeds and Reset Breaker fires | 0（保持清零 stays at zero） | HALF-OPEN → CLOSE | HTTP 200，全部流量恢复正常 HTTP 200, and full traffic resumes |
| T+40.3s | 结局乙：探测仍失败，Trip Breaker 再次触发 Ending B: the probe still fails and Trip Breaker fires again | 0（再次跳闸时清零 zeroed again at the trip） | HALF-OPEN → OPEN | 错误；新的 30 秒等待重新开始，下次探测在 T+70.3s An error, a fresh 30-second wait begins, and the next probe happens at T+70.3s |

从这张表里可以读出三个容易被忽略的事实 Three easily missed facts can be read straight off this table:

- 跳闸前后调用方的体验完全不同：跳闸前每次失败都要白等 2 秒，跳闸后失败在 1 毫秒内返回，快了约两千倍。
  The caller's experience before and after the trip is completely different: before the trip each failure wastes a full 2 seconds, and after the trip each failure returns within one millisecond, roughly two thousand times faster.
- HALF-OPEN 只放一个请求过去，因为目的是"试探"而不是"恢复流量"；如果放全量请求过去，刚要缓过来的服务端会被再次压垮。
  HALF-OPEN lets exactly one request through, because the goal is to probe rather than to restore traffic. Sending the full load at a server that is only just recovering would knock it down again.
- 计数器在跳闸的那一刻就被清零，之后 OPEN 期间被拒绝的请求也不会往上累加；所谓"冻结"只是在描述后半个效果，并不是说计数值一直停在阈值上。
  The counter is zeroed at the moment of the trip, and the requests rejected during OPEN afterwards do not add to it either. The word "frozen" describes only that second effect, not a counter parked at the threshold value.

什么才算"一次失败" What actually counts as a failure: 完整的判定表见后面的 "什么算失败 What Counts as a Failure" 一节。
The full decision table appears later, in the "什么算失败 What Counts as a Failure" section.

连续计数与滑动窗口 Consecutive counting versus a rolling window: 两种计数方式的取舍见后面的 "两种失败计数方式 Two Ways to Count Failures" 一节。
The trade-off between the two counting schemes is covered later, in the "两种失败计数方式 Two Ways to Count Failures" section.

---

#### 断路器和重试的分工 How Retry and the Breaker Divide the Work

> **大白话:** 重试是"这一通电话没打通，马上再拨一次"；断路器是"这个号码今天一直打不通，先从通话列表里划掉，过半小时再试一次"。两件事管的时间尺度不一样。 / A retry says "this one call did not connect, so dial again right now". A breaker says "this number has been unreachable all day, so cross it off the call list and try once in half an hour". The two operate on different time scales.

| 对比维度 Dimension | Retry(重试) | Circuit Breaker(断路器) |
| --- | --- | --- |
| 解决什么问题 Problem solved | 单次调用偶发抖动，下一次很可能就成功 A one-off blip on a single call, where the next attempt will very likely succeed | 依赖方持续不可用，短期内再试也没用 A dependency that is persistently down, where trying again soon is pointless |
| 时间尺度 Time scale | 毫秒到秒级，通常在一次请求内部完成 Milliseconds to seconds, usually completed inside a single request | 秒到分钟级，跨越成千上万次请求 Seconds to minutes, spanning many thousands of requests |
| 保存什么状态 State kept | 不保存跨请求状态，每次调用独立判断 No cross-request state, each call decides on its own | 保存共享计数器和状态机，被所有调用方共同读写 Shared counters and a state machine, read and written by every caller |
| 作用对象 Scope of effect | 只影响发起重试的那一个调用 Affects only the one call that is being retried | 影响所有走同一个断路器的调用 Affects every call routed through the same breaker |
| 只用它会怎样 What happens if used alone | 依赖长时间宕机时，重试会把负载放大数倍，把濒死的服务彻底压死 When the dependency is down for a long time, retries multiply the load several times over and finish off a service that was barely alive | 遇到真正的瞬时抖动时，本来重试一次就能成功的请求被直接判为失败，可用性反而下降 A genuine momentary blip that a single retry would have fixed is reported as a failure instead, which lowers availability |
| 与另一个的关系 Relationship to the other | 需要断路器给它设上限，防止无休止放大 Needs the breaker to cap it, so that amplification cannot continue indefinitely | 需要重试来吸收真正短暂的抖动，避免过早跳闸 Needs retries to absorb genuinely brief blips, so that it does not trip prematurely |

两者是互补关系，不是二选一：重试处理"一瞬间的问题"，断路器处理"一段时间的问题"，正确的做法是在同一个调用链上同时配置。
The two are complements, not alternatives. Retry handles a problem that lasts an instant, the breaker handles a problem that lasts a while, and the correct approach is to configure both on the same call path.

嵌套顺序 The nesting order: 两者的组合顺序及其取舍见后面的 "重试和断路器的组合顺序 Composition Order: Retry Inside or Outside the Breaker" 一节。
The order in which the two are composed, and the trade-off involved, is covered later in the "重试和断路器的组合顺序 Composition Order: Retry Inside or Outside the Breaker" section.

一条实用建议 One practical rule: 每个下游依赖用独立的断路器实例，不要共用。共用会让一个慢依赖的跳闸把访问其他健康依赖的请求也一起拒绝。
Each downstream dependency deserves its own breaker instance rather than a shared one. Sharing means that a trip caused by one slow dependency also rejects the requests aimed at other healthy dependencies.

没有断路器的代价 The cost of having no breaker: 下游彻底挂掉时，干等超时的调用会占满线程池，最终把一个本来健康的服务也拖垮，这种失败沿调用链向上蔓延的现象叫做 <font color=OrangeRed>cascading failure(级联故障)</font>；具体的线程池算术见后面的 "韧性四件套 The Four Resilience Primitives" 一节。
When a dependency dies completely, calls that sit waiting for a timeout consume the whole thread pool and eventually drag down an otherwise healthy service; this spreading of failure up the call chain is called <font color=OrangeRed>cascading failure</font>. The concrete thread-pool arithmetic appears later, in the "韧性四件套 The Four Resilience Primitives" section.

---

#### 自己动手写一个断路器 Building a Circuit Breaker From Scratch

> **大白话:** 断路器就是家里电闸的软件版，而电闸内部并不神秘——一根会跳的开关、一个数跳闸次数的小计数器、一块表看过了多久，就这三样东西。 / A circuit breaker is the software version of the fuse switch in a house, and the inside of that switch is not mysterious: one lever that can flip, one small counter that tallies problems, and one clock that says how long it has been since the flip.

前面的章节直接跳到了 Hystrix、resilience4j、pybreaker 这些现成的库，读者看到的是"怎么用"，却从来没看到"里面是什么"。这一节把它从零拆开来。断路器的全部内容只有 **三个状态、两个计数器、一个时钟**：
The earlier sections jump straight to ready-made libraries such as Hystrix, resilience4j and pybreaker, so the reader is shown how to call one but never what is inside one. This section takes it apart from nothing. The entire mechanism is **three states, two counters, one clock**:

| 组成部分 Ingredient | 它是什么 What it is | 为什么需要它 Why it is needed |
| --- | --- | --- |
| 三个状态 Three states | `CLOSED` 闭合放行、`OPEN` 断开拒绝、`HALF_OPEN` 半开试探 / `CLOSED` lets calls through, `OPEN` rejects them, `HALF_OPEN` lets a trickle through | 决定"这一次调用到底发不发出去" Decides whether a given call is actually sent |
| 计数器一：连续失败数 Counter one: the failure streak | 一个整数，连续失败就加一，成功就归零 An integer that increments on each consecutive failure and resets to zero on success | 判断"坏得够不够严重，值不值得跳闸" Decides whether things are bad enough to trip |
| 计数器二：在途探测数 Counter two: probes in flight | 半开状态下已经放出去、还没回来的试探请求个数 The number of probe calls already released in `HALF_OPEN` and not yet finished | 半开时只允许极少量请求，防止一开闸就把刚喘上气的服务再压垮 Keeps `HALF_OPEN` down to a trickle so a barely-recovered server is not flattened again |
| 一个时钟 One clock | 最后一次状态切换的时间戳 The timestamp of the most recent state change | 用来算"断开够久了吗，可以去试探了吗" Used to answer: has the cooldown elapsed, is it time to probe |

这里唯一真正的抽象是 <font color=OrangeRed>状态机 state machine</font>：一个任何时刻只处于一种状态、并且只按固定规则在状态之间跳的东西。
The one genuine abstraction here is the <font color=OrangeRed>状态机 state machine</font>: a thing that sits in exactly one state at a time and moves between states only along fixed, declared rules.

##### 完整实现 The Complete Implementation

> **大白话:** 下面这段代码就是一个"门卫"。每次要打电话给下游服务之前，先问门卫一句"现在能打吗"，门卫要么放行、要么当场拦下来。 / The code below is a doorman. Before every call to a downstream service the caller asks the doorman whether calls are allowed right now, and the doorman either waves the call through or turns it away on the spot.

这段代码 <font color=OrangeRed>零依赖 zero dependencies</font>，只用到 Python 标准库里的 `enum`、`threading`、`time`，所以不需要任何 `pip install` 命令；目标版本是 Python 3.8 及以上。
This implementation has <font color=OrangeRed>零依赖 zero dependencies</font> and uses only `enum`, `threading` and `time` from the Python standard library, so no `pip install` command is required. It targets Python 3.8 and above.

```python
# -*- coding: utf-8 -*-
# 纯标准库断路器 A circuit breaker using only the Python standard library.
# 运行方式 How to run: python breaker.py   (Python 3.8+)

import enum
import threading
import time

class State(enum.Enum):
    CLOSED = "CLOSED"        # 闭合，正常放行 pass calls through
    OPEN = "OPEN"            # 断开，直接拒绝 reject every call
    HALF_OPEN = "HALF_OPEN"  # 半开，只放极少量探测 allow a trickle of probes

class CircuitOpenError(Exception):
    """断路器已断开，调用被拒绝 Raised when the breaker refuses a call."""

class CircuitBreaker:
    def __init__(self, failure_threshold=3, open_timeout=5.0,
                 half_open_probes=1, half_open_timeout=5.0):
        self._failure_threshold = failure_threshold   # 阈值 trip after N failures in a row
        self._open_timeout = open_timeout             # 冷却秒数 seconds to stay OPEN
        self._half_open_probes = half_open_probes     # 半开名额 probe slots in HALF_OPEN
        self._half_open_timeout = half_open_timeout   # 半开最长停留 max seconds in HALF_OPEN

        self._state = State.CLOSED
        self._consecutive_failures = 0                # 计数器一 counter one
        self._probes_in_flight = 0                    # 计数器二 counter two
        self._changed_at = time.monotonic()           # 唯一的时钟 the one clock
        self._lock = threading.Lock()                 # 保证多线程下计数不错乱 thread safety

    @property
    def state(self):
        # 纯读取，绝不改状态 a pure read that never mutates the state machine
        with self._lock:
            return self._state

    def tick(self):
        # 显式推进时间相关的状态迁移 explicitly apply the time-driven transitions
        with self._lock:
            self._maybe_expire()
            return self._state

    def _transition(self, new_state):
        # 改状态的唯一入口，顺手清空两个计数器 the only place state and counters change
        self._state = new_state
        self._changed_at = time.monotonic()
        self._consecutive_failures = 0
        self._probes_in_flight = 0

    def _maybe_expire(self):
        # 调用方必须已持有锁 the caller must already hold the lock
        elapsed = time.monotonic() - self._changed_at
        if self._state is State.OPEN:
            # OPEN 待够时间就自动变 HALF_OPEN cooldown elapsed -> start probing
            if elapsed >= self._open_timeout:
                self._transition(State.HALF_OPEN)
        elif self._state is State.HALF_OPEN:
            # 探测迟迟不回来就退回 OPEN 重新武装 a stuck probe re-arms the breaker
            if elapsed >= self._half_open_timeout:
                self._transition(State.OPEN)

    def _allow(self):
        # 返回 (是否放行, 当时的状态名) returns (allowed, state name at decision time)
        with self._lock:
            self._maybe_expire()
            if self._state is State.CLOSED:
                return True, self._state.value
            if self._state is State.OPEN:
                return False, self._state.value
            # HALF_OPEN: 名额有限，先到先得 limited slots, first come first served
            if self._probes_in_flight < self._half_open_probes:
                self._probes_in_flight += 1
                return True, self._state.value
            return False, self._state.value

    def _abandon_probe(self):
        # 没记账就退出时归还名额 give the slot back when no outcome was recorded
        with self._lock:
            if self._probes_in_flight > 0:
                self._probes_in_flight -= 1

    def _on_success(self):
        with self._lock:
            if self._state is State.HALF_OPEN:
                self._transition(State.CLOSED)     # 探测成功，正式恢复 probe ok -> recover
            else:
                self._consecutive_failures = 0     # 连续失败链断了 the streak is broken

    def _on_failure(self):
        with self._lock:
            if self._state is State.OPEN:
                return                             # 闸已跳过，这是迟到的在途结果 stale result
            if self._state is State.HALF_OPEN:
                self._transition(State.OPEN)       # 探测失败，重新跳闸 probe failed -> trip
                return
            self._consecutive_failures += 1
            if self._consecutive_failures >= self._failure_threshold:
                self._transition(State.OPEN)       # 连续失败够多，跳闸 streak long enough

    def _record_result(self, result, elapsed):
        # 可覆写的记账钩子 the overridable recording hook
        self._on_success()

    def call(self, func, *args, **kwargs):
        allowed, snapshot = self._allow()
        if not allowed:
            raise CircuitOpenError("circuit is " + snapshot + ", call rejected")
        recorded = False
        started = time.monotonic()
        try:
            result = func(*args, **kwargs)
        except Exception:
            recorded = True
            self._on_failure()
            raise                                  # 原始异常照旧抛出 re-raise untouched
        else:
            recorded = True
            self._record_result(result, time.monotonic() - started)
            return result
        finally:
            if not recorded:
                self._abandon_probe()              # BaseException 也不能吞掉名额 slot returned
```

##### 逐条拆解决策逻辑 Dissecting the Decision Logic

> **大白话:** 下面把门卫脑子里的每一个"如果"单独摊开来讲，重点不是这行代码写了什么，而是这一个分支到底在防什么事。 / Each branch in the doorman's head is unpacked below one at a time, and the point is not what the line of code says but which specific disaster that branch exists to prevent.

1. **`CLOSED` 且调用成功 → 计数器归零。** 关键词是"连续"。服务偶尔抖一下是正常的，只要中间成功过一次，之前的失败就不该继续记在账上。
   **`CLOSED` and the call succeeded, so the counter resets to zero.** The key word is *consecutive*. Occasional single failures are normal, and once a success happens in between, earlier failures should no longer be held against the dependency.

2. **`CLOSED` 且调用失败 → 计数器加一，还没到阈值就继续放行。** 这一支防止的是"过度敏感"：如果一次失败就跳闸，那么每天几次正常的网络抖动都会让整个功能不可用，断路器本身就成了故障源。
   **`CLOSED` and the call failed, so the counter increments but calls still go through until the threshold is reached.** This branch guards against over-sensitivity. If a single failure tripped the breaker, ordinary daily network jitter would take the feature offline, and the breaker itself would become the outage.

3. **`CLOSED` 且连续失败数达到阈值 → 切到 `OPEN`。** 这是整个模式存在的理由。它防止的是<font color=OrangeRed>雪崩 cascading failure</font>：下游已经躺平了，上游还在死命重试，每个重试都占着一个线程和一条连接，最后上游自己先被拖死，再拖死上游的上游。
   **`CLOSED` and the failure streak reached the threshold, so the state becomes `OPEN`.** This is the reason the whole pattern exists. It prevents a <font color=OrangeRed>雪崩 cascading failure</font>: the dependency is already flat on its back, the caller keeps retrying, every retry holds a thread and a connection, and eventually the caller dies first and takes its own callers down with it.

4. **`OPEN` 且冷却时间还没到 → 立刻拒绝，连网络都不碰。** 拒绝必须是"快"的，这才是断路器和超时的根本区别：超时要等满超时时间才失败，断路器是零耗时失败。它防止的是资源被无谓占用。
   **`OPEN` and the cooldown has not elapsed, so the call is rejected immediately without touching the network.** The rejection must be fast, and that is the essential difference from a timeout: a timeout still burns the full timeout duration before failing, whereas the breaker fails in zero time. This branch protects finite resources from being tied up for nothing.

5. **`OPEN` 且冷却时间已到 → 切到 `HALF_OPEN`；反过来，`HALF_OPEN` 停留超过 `half_open_timeout` → 退回 `OPEN` 重新武装。** 两个方向都由 `_maybe_expire` 处理，而 `_maybe_expire` 只在放行判断和显式的 `tick()` 里被调用，代码里没有任何后台线程或定时器。第一个方向防止的是复杂度：一个需要自己起线程的断路器，会带来线程泄漏和关闭顺序的新问题。第二个方向防止的是永久性拒绝：探测请求如果永远不返回，在途探测数就永远停在 1，若没有这条超时，断路器会在 `HALF_OPEN` 上钉死一辈子，此后每一次调用都被拒绝。
   **`OPEN` with the cooldown elapsed becomes `HALF_OPEN`, and conversely a `HALF_OPEN` that has lasted longer than `half_open_timeout` falls back to `OPEN` to re-arm.** Both directions live in `_maybe_expire`, which is reached only from the admission check and from an explicit `tick()`, so there is no background thread or timer anywhere in the code. The first direction guards against complexity: a breaker that spawns its own thread introduces thread leaks and shutdown-ordering problems of its own. The second guards against a permanent outage: if a probe never returns, the in-flight probe count stays at one forever, and without this deadline the breaker would be pinned at `HALF_OPEN` for the life of the process, rejecting every later call.

6. **`HALF_OPEN` 且探测名额还有 → 放行，同时占掉一个名额。** 这一支防止的是"惊群"：如果冷却一结束就把积压的全部请求一起放出去，刚刚缓过来的服务会被瞬间再次打死，然后无限循环。
   **`HALF_OPEN` with a probe slot still free, so the call goes through and consumes that slot.** This branch prevents a thundering herd. If every queued request were released the instant the cooldown ended, the barely-recovered dependency would be flattened again immediately, and the cycle would repeat forever.

7. **`HALF_OPEN` 且名额已被占满 → 拒绝。** 探测期间绝大多数调用仍然是失败的，这是有意的取舍：宁可多拒绝几个请求，也不要为了这几个请求赌上整个下游。
   **`HALF_OPEN` with all slots taken, so the call is rejected.** During probing the vast majority of calls still fail fast, and that is a deliberate trade: rejecting a few extra requests is cheaper than gambling the whole dependency on them.

8. **`HALF_OPEN` 且探测成功 → 切回 `CLOSED`，两个计数器一起清零。** 清零非常重要。如果只改状态不清 `_consecutive_failures`，那么恢复之后只要再失败一次就会立刻凑够阈值又跳闸，表现出来就是"断路器抖动 flapping"。
   **`HALF_OPEN` and the probe succeeded, so the state returns to `CLOSED` and both counters are cleared.** The clearing matters. Changing the state without resetting `_consecutive_failures` would mean one single failure after recovery is enough to hit the threshold again, which shows up in production as breaker flapping.

9. **`HALF_OPEN` 且探测失败 → 立刻回到 `OPEN`，重新开始计时。** 这里不需要再累积阈值。半开状态下的这一次失败已经是一次专门设计的体检，体检不合格就没有讨论的必要。
   **`HALF_OPEN` and the probe failed, so the state returns to `OPEN` and the clock restarts.** No further accumulation toward the threshold is needed here. That single call was a purpose-built health check, and a failed health check needs no second opinion.

10. **所有读写都在同一把锁里 → 计数不会错乱。** 这里用普通的 `Lock` 就够了：没有任何路径会在持锁期间再次申请这把锁。`state`、`tick()` 和放行判断各自加一次锁，`_maybe_expire` 与 `_transition` 都是私有的，并且只在调用方已经持锁时才被调用。
    **Every read and write happens inside one lock, so the counters cannot be corrupted.** A plain `Lock` suffices, because no path re-acquires the lock while already holding it. The `state` property, `tick()` and the admission check each acquire it exactly once, while `_maybe_expire` and `_transition` are private and are only ever called with the lock already held.

11. **被包裹的原始异常原样抛出 → 上层的错误处理不受影响。** `_on_failure()` 之后紧跟裸 `raise`，断路器只做记账，绝不吞掉或改写业务异常。`finally` 里的 `_abandon_probe()` 负责收尾：连 `except Exception` 都抓不到的 `BaseException` 逃出去时，半开名额也会被归还。
    **The wrapped function's original exception is re-raised untouched, so upper-layer error handling is unaffected.** A bare `raise` follows `_on_failure()`, which keeps the breaker purely a bookkeeper that never swallows or rewrites a business exception. The `_abandon_probe()` call in the `finally` block handles the remainder: when a `BaseException` that even `except Exception` cannot catch escapes, the half-open slot is still returned.

##### 让状态机跑起来 Watching the State Machine Move

> **大白话:** 把下面这段接在上面那段后面，存成同一个文件运行，就能亲眼看到状态从"闭合"一路跳到"断开"、再"半开"试探、最后恢复。 / Pasting the block below directly after the previous one into a single file makes the state visibly walk from closed, to open, into a probe, and back to normal.

注意 `state` 只是纯读取，它自己不会推进状态机；示例里那句"冷却结束"的日志之所以能看到 `HALF_OPEN`，是因为它显式调用了 `tick()`。这一点很重要：观测代码不应该悄悄改变被观测对象的行为。
Note that `state` is a pure read and does not advance the state machine on its own; the cooldown log line below can report `HALF_OPEN` only because it calls `tick()` explicitly. That separation matters, because observation code must not quietly change the behaviour of the thing being observed.

```python
# 接在上一段代码后面 Append this to the same file as the class above.

if __name__ == "__main__":
    breaker = CircuitBreaker(failure_threshold=2, open_timeout=1.0, half_open_probes=1)

    def always_fails():
        raise RuntimeError("downstream is down")

    def always_works():
        return "ok"

    def attempt(label, func):
        try:
            result = breaker.call(func)
            print("%-22s -> success(%s)   state=%s" % (label, result, breaker.state.value))
        except CircuitOpenError:
            print("%-22s -> REJECTED       state=%s" % (label, breaker.state.value))
        except RuntimeError as exc:
            print("%-22s -> failed(%s) state=%s" % (label, exc, breaker.state.value))

    attempt("call 1 (fail)", always_fails)
    attempt("call 2 (fail)", always_fails)
    attempt("call 3 (blocked)", always_fails)

    time.sleep(1.1)  # 等过冷却期 wait out the open_timeout
    print("--- cooldown elapsed, state=%s" % breaker.tick().value)

    attempt("call 4 (probe fail)", always_fails)
    attempt("call 5 (blocked)", always_works)

    time.sleep(1.1)  # 再等一轮 wait out the second cooldown
    attempt("call 6 (probe ok)", always_works)
    attempt("call 7 (normal)", always_works)
```

预期输出 Expected console output:

```text
call 1 (fail)          -> failed(downstream is down) state=CLOSED
call 2 (fail)          -> failed(downstream is down) state=OPEN
call 3 (blocked)       -> REJECTED       state=OPEN
--- cooldown elapsed, state=HALF_OPEN
call 4 (probe fail)    -> failed(downstream is down) state=OPEN
call 5 (blocked)       -> REJECTED       state=OPEN
call 6 (probe ok)      -> success(ok)   state=CLOSED
call 7 (normal)        -> success(ok)   state=CLOSED
```

值得注意的是 call 5 调用的是 `always_works`，本来会成功，却仍然被拒绝了——这正是断路器的代价：断开期间它会连正常请求一起挡掉。
Note that call 5 wraps `always_works` and would have succeeded, yet it is still rejected. That is precisely the cost of the pattern: while open, a breaker blocks healthy requests along with the sick ones.

##### 两种失败计数方式 Two Ways to Count Failures

> **大白话:** 一种数法是"连着摔了三跤才算病了"，另一种是"最近一百步里摔了四十跤就算病了"。第一种简单，但对一个总是摔四十跤、却从不连摔三跤的人完全无感。 / One way of counting says a runner is only unwell after three stumbles in a row; the other says a runner is unwell if forty of the last hundred steps were stumbles. The first is simpler, but it is completely blind to a runner who always stumbles forty percent of the time yet never three times consecutively.

上面手写的实现用的是最简单的 <font color=OrangeRed>连续失败计数 consecutive-failure counting</font>。生产库通常提供另一种：<font color=OrangeRed>滑动窗口失败率 sliding-window failure rate</font>。库的文档往往假设读者已经知道这个区别，所以这里明确说清。
The from-scratch implementation above uses the simplest scheme, <font color=OrangeRed>连续失败计数 consecutive-failure counting</font>. Production libraries usually offer a second scheme, <font color=OrangeRed>滑动窗口失败率 sliding-window failure rate</font>. Library documentation tends to assume the difference is already understood, so it is spelled out here.

| 对比维度 Dimension | 连续失败计数 Consecutive-failure counting | 滑动窗口失败率 Sliding-window failure rate |
| --- | --- | --- |
| 什么条件下跳闸 What trips it | 连续 N 次失败，中间一次成功就清零 N failures in an unbroken row; a single success resets the count | 最近一段样本里失败比例超过某个百分比，通常还要求样本数达到最小值 The failure proportion within a recent sample exceeds a percentage, usually with a minimum-sample requirement as well |
| 低流量下的表现 Behaviour under low traffic | 表现稳定，一天只有几次调用也照样能凑够连续失败 Stable; even a handful of calls per day can still form a streak | 容易误判，样本太少时一两次失败就能算出 50% 甚至 100% 的失败率，因此必须配最小样本数 Prone to false trips, because one or two failures out of a tiny sample compute to 50 percent or even 100 percent, so a minimum-sample setting is mandatory |
| 稳定 40% 失败时的表现 Behaviour when 40 percent of calls fail steadily | 很可能永远不跳闸。失败随机分布时，连续 3 次失败的概率只有 6.4%，而其间任何一次成功都会清零 Very likely never trips. With randomly distributed failures the chance of three in a row is only 6.4 percent, and any success in between wipes the count | 只要阈值低于 40%，就能稳定跳闸，因为它直接测量失败比例，不依赖失败是否连续 Trips reliably provided the threshold is set below 40 percent, because the failure rate is measured directly and does not depend on failures being consecutive |
| 内存开销 Memory cost | 一个整数，常数级 A single integer, constant | 需要保存最近 N 个结果或最近若干秒的桶，占用随窗口大小增长 Must retain the last N outcomes or a set of per-second buckets, so cost grows with the window size |
| 实现复杂度 Implementation complexity | 十行以内 Under ten lines | 需要环形缓冲或时间分桶，还要处理窗口滚动 Needs a ring buffer or time buckets plus window-rolling logic |

滑动窗口本身又分两种，选哪种取决于流量形态：
A sliding window itself comes in two flavours, and the choice depends on the traffic shape:

| 窗口类型 Window type | 定义 Definition | 适合什么场景 When it fits |
| --- | --- | --- |
| 计数窗口 Count-based | 只看最近 N 次调用，比如最近 100 次里失败了几次 Considers only the last N calls, for example how many of the last 100 failed | 流量稳定持续，窗口能被快速填满 Traffic is steady and continuous, so the window fills quickly |
| 时间窗口 Time-based | 只看最近 T 秒内的调用，比如最近 60 秒的失败率 Considers only calls within the last T seconds, for example the failure rate over the last 60 seconds | 流量忽高忽低，需要"陈旧数据必须过期"的保证 Traffic is bursty, and stale data must be guaranteed to expire |

关键结论：连续计数简单可靠，但它对"一个永远稳定失败 40% 的服务"完全无能为力，而这种半死不活的状态在生产环境里比彻底宕机常见得多。
The key conclusion: consecutive counting is simple and dependable, but it is powerless against a dependency that steadily fails 40 percent of the time forever, and that half-dead condition is far more common in production than a total outage.

##### 慢调用也是一种失败 Slow Calls Count as Failures

> **大白话:** 一个 30 秒才回话的下游，比一个立刻说"我不行"的下游破坏力更大——因为在这 30 秒里，一个线程和一条连接被死死占着，什么也干不了。 / A dependency that answers after thirty seconds does more damage than one that instantly says no, because for those thirty seconds a thread and a connection are pinned down and useless.

原因在于资源是有限的：慢调用会把工作线程和连接一直占住，最终导致 <font color=OrangeRed>线程池耗尽 thread pool exhaustion</font>，完整算例见后面"韧性四件套 The Four Resilience Primitives"一节。
The reason is that resources are finite: a slow call pins a worker thread and a connection until it returns, which ends in <font color=OrangeRed>线程池耗尽 thread pool exhaustion</font>, and the full calculation appears in the later section 韧性四件套 The Four Resilience Primitives.

成熟的库把"耗时超过阈值但成功了的调用"单独记为一类结果，作为独立于失败率的第二个维度来评估。resilience4j 用 `slowCallDurationThreshold` 判定一次调用是否算慢，把它记成 `SLOW_SUCCESS`，再用独立的 `slowCallRateThreshold` 衡量慢调用比例；失败率和慢调用比例中任意一个越线，断路器就跳闸。Sentinel 的慢调用比例规则是同一个思路。下面是把这个概念加到上面手写实现里的最小改动：
Mature libraries record a successful-but-slow call as its own outcome class and evaluate it as a second dimension alongside the failure rate. resilience4j decides whether a call counts as slow using `slowCallDurationThreshold`, records it as `SLOW_SUCCESS`, and measures the proportion of such calls against a separate `slowCallRateThreshold`; the breaker trips when either the failure rate or the slow-call rate crosses its own threshold. Sentinel's slow-call-ratio rule follows the same idea. Below is the minimal change that adds the concept to the from-scratch implementation:

```python
# 继承上面的 CircuitBreaker Extends the class defined earlier; still standard library only.

class SlowAwareCircuitBreaker(CircuitBreaker):
    # slow_call_threshold 只能按关键字传，免得挤掉 failure_threshold 的位置
    # slow_call_threshold is keyword-only so it cannot occupy the failure_threshold slot
    def __init__(self, *args, slow_call_threshold=2.0, **kwargs):
        super().__init__(*args, **kwargs)
        self._slow_call_threshold = slow_call_threshold  # 超过几秒算慢 seconds

    # 只覆写记账钩子，call 完全复用父类 only the recording hook is overridden
    def _record_result(self, result, elapsed):
        if elapsed > self._slow_call_threshold:
            # 拿到结果了，但太慢，照样记一次失败 got an answer, but too slow to count as healthy
            self._on_failure()
        else:
            self._on_success()
```

注意这里仍然把 `result` 返回给调用方——慢调用对业务是成功的，只对断路器是失败的。这两件事必须分开看待。
Note that `result` is still returned to the caller: a slow call succeeded as far as the business logic is concerned, and failed only as far as the breaker is concerned. Those two judgements must stay separate.

##### 这个玩具版故意省略了什么 What This Toy Deliberately Omits

> **大白话:** 上面这一百行足够讲清原理，但不该拿去上线。少掉的那些东西不是装饰，而是出事那天唯一能救命的部分。 / The hundred lines above are enough to explain the mechanism but should not be shipped. The missing pieces are not decoration; they are the parts that matter on the day something actually breaks.

- **指标上报 Metrics emission** — 没有任何计数被暴露给监控系统；该上报哪几个信号、哪些该配告警，见后面"该看哪些指标 Metrics and Alerts Worth Having"一节。
  Not a single counter is exposed to a monitoring system; which signals to publish and which of them deserve alerts are covered in the later section 该看哪些指标 Metrics and Alerts Worth Having.
- **事件监听 Event listeners** — 状态切换是静默发生的。生产库允许注册回调，用于打日志、发告警、切换到降级数据源。这里连一行日志都没有。
  State transitions happen silently. Production libraries allow callbacks to be registered for logging, alerting, or switching to a fallback data source. Here there is not even a log line.
- **按端点隔离 Per-endpoint instances** — 这一个实例包住了所有调用。真实场景需要每个下游、甚至每个接口一个独立断路器，否则订单查询接口挂掉会连带把健康的支付接口也拒绝掉。
  A single instance wraps every call. Real systems need one breaker per dependency, or even per endpoint, otherwise a broken order-lookup endpoint also blocks a perfectly healthy payment endpoint.
- **半开并发控制 Half-open concurrency limiting** — 这里只有一个朴素的计数器加一句 `finally`。顺便纠正一个常见误解：普通异常并不会漏掉名额，因为跳闸时两个计数器一起清零；真正会漏的是 `except Exception` 抓不到的 `BaseException`，例如 `KeyboardInterrupt`、`SystemExit`、`asyncio.CancelledError`——它们既不会被记成失败，又会白白占掉一个名额，所以上面才必须在 `finally` 里把名额还回去。生产库使用带许可归还的信号量，并支持"连续成功 N 次才恢复"。
  Only a naive counter plus one `finally` clause exists here. A common misreading is worth correcting: an ordinary exception does not leak a slot, because tripping clears both counters. The real leak comes from a `BaseException` that `except Exception` cannot catch, such as `KeyboardInterrupt`, `SystemExit` or `asyncio.CancelledError`, which is neither recorded as a failure nor charged back, which is exactly why the slot has to be returned in a `finally` block above. Production libraries use a semaphore with proper permit release and support requiring N consecutive successes before recovery.
- **异常分类 Exception classification** — 当前实现把所有 `Exception` 一律算作失败。这是错的：HTTP 400 参数错误是调用方自己的问题，重试一万次也不会好，不该计入跳闸；完整的判定规则见后面"什么算失败 What Counts as a Failure"一节。
  The current implementation counts every `Exception` as a failure. That is wrong: an HTTP 400 caused by a bad parameter is the caller's own mistake, will never improve with retries, and should not count toward tripping. The complete classification rule appears in the later section 什么算失败 What Counts as a Failure.
- **配置热更新 Configuration reload** — 阈值和超时在构造时固定。生产环境需要在不重启进程的情况下调整它们，因为合适的阈值往往只有在真实故障发生时才被发现。
  The threshold and timeout are fixed at construction time. Production environments need to adjust them without restarting the process, because the right threshold is usually only discovered during a real incident.

---

#### 生产环境中真实的实现 Real Implementations in Production

> **大白话:** 断路器不用自己造，就像厨房里不用自己拉铁丝做打蛋器——每种语言都有别人已经用了十年、摔打过无数次的成品，拿来接上就行。 / A breaker does not need to be hand-built, the same way a kitchen does not need a whisk bent out of wire: every language already ships a battle-tested part, and the job is to bolt it on correctly.

不同语言里都有现成的、经过生产环境验证的断路器库，不需要从零手写状态机。

Every mainstream language already has a production-proven <font color=OrangeRed>circuit breaker library</font>, so there is no need to hand-write the state machine. "State machine" here means the small piece of bookkeeping that remembers whether the breaker is currently CLOSE (traffic allowed), OPEN (traffic blocked), or HALF-OPEN (a few probe requests allowed through to test recovery).

**Python — [pybreaker](https://github.com/danielfm/pybreaker)**

> **大白话:** pybreaker 就像给一个函数套上一个保险丝盒，函数连续烧断五次，盒子就把线路切断，之后的调用连电都不通。 / pybreaker wraps a fuse box around one function: after the function blows five times in a row the box cuts the line, and later calls do not even get electricity.

安装 Install（本节示例针对 pybreaker 1.x — the examples target pybreaker 1.x）:

```bash
pip install pybreaker
```

```python
import pybreaker
import requests

# fail_max: 连续失败几次后跳闸进入 OPEN
# reset_timeout: 跳闸后等待多少秒，才进入 HALF-OPEN 去探测
breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60)

@breaker
def call_downstream_service():
    response = requests.get("https://api.example.com/data", timeout=3)
    response.raise_for_status()
    return response.json()

try:
    data = call_downstream_service()
except pybreaker.CircuitBreakerError:
    # 断路器处于 OPEN 状态时会直接抛这个异常，请求根本没有真的发出去
    data = get_cached_fallback_data()
```

| 参数 Knob | 含义 Plain meaning | 起始值 Starting value |
| --- | --- | --- |
| `fail_max` | 连续失败多少次就跳闸；注意是"连续"，成功一次就清零 / How many failures in a row trip the breaker; the counter resets to zero on any success | `5` |
| `reset_timeout` | 跳闸后冷静多少秒再放一个探测请求 / Seconds to stay quiet before one probe request is allowed | `60`（秒 seconds） |
| `exclude` | 哪些异常"不算"失败，可以填异常类型也可以填判断函数 / Which exceptions do not count as failures; accepts exception classes or predicate functions | 见下文"什么算失败" / see "What Counts as a Failure" |
| `listeners` | 状态变化时的回调，用来打日志或上报指标 / Callbacks fired on state change, used for logging or metrics | 至少挂一个记状态切换 / at least one that records transitions |
| `state_storage` | 状态存在哪里；默认存在进程内存里 / Where breaker state lives; defaults to process memory | `CircuitMemoryStorage('closed')`（`state` 是必填参数 / `state` is a required argument），多进程时换 Redis / swap in Redis for multi-process |
| `name` | 断路器的名字，出现在日志和指标里 / A label for the breaker, shown in logs and metrics | 下游服务名 / the downstream service name |

它唯一比别人强的地方 What it does better：pybreaker 支持 `CircuitRedisStorage`，把状态放进 Redis，于是 gunicorn 起的 16 个 worker 进程共享同一个断路器，而不是各自跳闸 16 次。 / pybreaker can store state in Redis via `CircuitRedisStorage`, so sixteen gunicorn worker processes share one breaker instead of each tripping independently.

**Go — [sony/gobreaker](https://github.com/sony/gobreaker)**

> **大白话:** gobreaker 不替使用者定政策，它只递给使用者一张最近的成绩单，由使用者自己写一行判断"这算不算该跳闸"。 / gobreaker does not decide the policy; it hands over a recent scorecard and the caller writes one line deciding whether that scorecard deserves a trip.

安装 Install:

```bash
go get github.com/sony/gobreaker
```

```go
import (
    "net/http"
    "time"

    "github.com/sony/gobreaker"
)

var cb *gobreaker.CircuitBreaker

// httpClient: 全局复用一个带超时的客户端，否则请求可能永远挂住
// httpClient: one shared client carrying a timeout, otherwise a request can hang forever
var httpClient = &http.Client{Timeout: 3 * time.Second}

func init() {
    settings := gobreaker.Settings{
        Name:        "downstream-api",
        MaxRequests: 3,                // HALF-OPEN 状态下最多放行几个探测请求
        Interval:    60 * time.Second, // CLOSE 状态下每隔这么久把计数整体清零；是周期性重置，不是滑动窗口 / counters are wholly reset every interval, a periodic reset rather than a sliding window
        Timeout:     30 * time.Second, // OPEN 状态维持多久后转入 HALF-OPEN
        ReadyToTrip: func(counts gobreaker.Counts) bool {
            failureRatio := float64(counts.TotalFailures) / float64(counts.Requests)
            return counts.Requests >= 10 && failureRatio >= 0.6
        },
    }
    cb = gobreaker.NewCircuitBreaker(settings)
}

func callDownstream() (interface{}, error) {
    return cb.Execute(func() (interface{}, error) {
        return httpClient.Get("https://api.example.com/data")
    })
}
```

| 参数 Knob | 含义 Plain meaning | 起始值 Starting value |
| --- | --- | --- |
| `Name` | 断路器名字，会出现在状态变更回调里 / Breaker label, surfaces in the state-change callback | 下游服务名 / the downstream service name |
| `MaxRequests` | HALF-OPEN 时允许通过的探测请求数上限 / Maximum probe requests allowed while HALF-OPEN | `3` |
| `Interval` | CLOSE 状态下多久把计数清一次零 / How often the counters are cleared while CLOSE | `60s` |
| `Timeout` | OPEN 状态维持多久 / How long the breaker stays OPEN | `30s` |
| `ReadyToTrip` | 一个函数，拿到计数后返回 true 就跳闸 / A function that receives the counts and returns true to trip | 至少 10 次调用且失败率 >= 60% / at least 10 calls and a 60% failure rate |
| `IsSuccessful` | 一个函数，决定某个 error 到底算不算失败 / A function deciding whether a given error counts as a failure | 把 4xx 判为"成功" / classify 4xx as success |
| `OnStateChange` | 状态切换回调，指标和告警从这里出去 / State-transition callback, the hook for metrics and alerts | 记日志并打点 / log and emit a counter |

它唯一比别人强的地方 What it does better：`ReadyToTrip` 是一个普通函数，任何跳闸策略都能表达——比如"只在 QPS 高于 50 时才允许跳闸"，别的库靠固定参数写不出来。 / `ReadyToTrip` is an ordinary function, so any trip policy is expressible, for example "only allow tripping when throughput exceeds 50 requests per interval", which fixed-knob libraries cannot express.

**Java — [resilience4j](https://resilience4j.readme.io/)（修正并补全上面残缺的示例 — a corrected, complete version of the incomplete example above）**

> **大白话:** resilience4j 不只看"打不通电话"，还看"电话通了但对方半分钟不说话"——慢也算故障。 / resilience4j does not only watch for calls that fail to connect, it also watches for calls that connect and then go silent for thirty seconds: slow counts as broken.

安装 Install（Maven 与 Gradle 坐标，示例针对 resilience4j 2.x — coordinates for Maven and Gradle, examples target resilience4j 2.x）:

```bash
# Maven: 加到 pom.xml 的 <dependencies> 里 / add to <dependencies> in pom.xml
#   <dependency>
#     <groupId>io.github.resilience4j</groupId>
#     <artifactId>resilience4j-circuitbreaker</artifactId>
#     <version>2.2.0</version>
#   </dependency>
#   resilience4j 2.x 的核心模块已经不再依赖 Vavr，要用 Try.recover 必须额外加下面这个坐标
#   resilience4j 2.x core modules no longer depend on Vavr, so Try.recover needs this extra artifact
#   <dependency>
#     <groupId>io.github.resilience4j</groupId>
#     <artifactId>resilience4j-vavr</artifactId>
#     <version>2.2.0</version>
#   </dependency>

# Gradle: 加到 build.gradle / add to build.gradle
#   implementation 'io.github.resilience4j:resilience4j-circuitbreaker:2.2.0'
#   implementation 'io.github.resilience4j:resilience4j-vavr:2.2.0'
```

```java
import java.time.Duration;
import java.util.function.Supplier;

import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig;
// Try 来自 Vavr，由 resilience4j-vavr 引入，核心模块里没有
// Try comes from Vavr, pulled in by resilience4j-vavr; the core module does not ship it
import io.vavr.control.Try;

CircuitBreakerConfig config = CircuitBreakerConfig.custom()
    .failureRateThreshold(50)                          // 失败率超过 50% 就跳闸
    .waitDurationInOpenState(Duration.ofSeconds(30))   // OPEN 状态维持 30 秒
    .slidingWindowSize(10)                              // 统计最近 10 次调用的结果
    .permittedNumberOfCallsInHalfOpenState(3)           // HALF-OPEN 时放行 3 次探测请求
    .build();

CircuitBreaker circuitBreaker = CircuitBreaker.of("downstreamApi", config);

Supplier<String> decoratedSupplier = CircuitBreaker
    .decorateSupplier(circuitBreaker, () -> downstreamClient.fetchData());

String result = Try.ofSupplier(decoratedSupplier)
    .recover(throwable -> getFallbackData())
    .get();
```

不想引入 Vavr 时，用纯 JDK 的 try/catch 表达同一件事 When Vavr is not wanted, plain JDK try/catch expresses the same thing:

```java
String result;
try {
    result = decoratedSupplier.get();
} catch (Exception e) {
    // 跳闸或调用失败都走到这里，返回兜底值
    // Both a tripped breaker and a failed call land here, and the fallback is returned
    result = getFallbackData();
}
```

| 参数 Knob | 含义 Plain meaning | 起始值 Starting value |
| --- | --- | --- |
| `slidingWindowType` | 按"最近 N 次调用"统计，还是按"最近 N 秒"统计 / Count over the last N calls, or over the last N seconds | `COUNT_BASED` |
| `slidingWindowSize` | 窗口大小，配合上一项理解 / Window size, read together with the row above | `100`（次 calls） |
| `minimumNumberOfCalls` | 样本不足这个数就一律不跳闸，防止前 2 次失败就误判 / Below this sample size the breaker never trips, which stops two early failures from causing a false trip | `20` |
| `failureRateThreshold` | 失败率百分比阈值 / Failure-rate percentage threshold | `50` |
| `slowCallDurationThreshold` | 超过多久就算一次"慢调用" / Above this duration a call is labelled slow | `2s` |
| `slowCallRateThreshold` | 慢调用占比超过多少就跳闸 / Percentage of slow calls that trips the breaker | `60` |
| `waitDurationInOpenState` | OPEN 状态维持多久 / How long the breaker stays OPEN | `30s` |
| `permittedNumberOfCallsInHalfOpenState` | HALF-OPEN 放几个探测请求 / Probe requests allowed while HALF-OPEN | `3` |
| `recordExceptions` | 白名单：只有这些异常算失败 / Allow-list: only these exception types count as failures | 见下文 / see below |
| `ignoreExceptions` | 黑名单：这些异常永远不算失败，优先级高于白名单 / Deny-list: these never count, and it wins over the allow-list | 见下文 / see below |

它唯一比别人强的地方 What it does better：只有 resilience4j 内置"慢调用率"这一维度。真实故障最常见的形态不是报错，而是变慢——依赖还在返回 200，只是每次要 8 秒，把调用方的线程全占满。 / Only resilience4j ships a slow-call rate dimension. The most common shape of a real outage is not errors but sluggishness: the dependency still returns 200, it just takes eight seconds and exhausts every thread on the calling side.

**Node.js — [opossum](https://github.com/nodeshift/opossum)**

> **大白话:** opossum 自带"备用答案"这个位置——跳闸时它不是抛错，而是直接把事先准备好的替代结果递出去，像餐厅招牌菜卖完时直接上今日特餐。 / opossum has a dedicated slot for a backup answer: when tripped it does not throw, it hands back a prepared substitute, the way a restaurant serves the daily special once the signature dish sells out.

安装 Install（示例针对 opossum 8.x — the example targets opossum 8.x）:

```bash
npm install opossum
```

```javascript
const CircuitBreaker = require('opossum');

const options = {
  timeout: 3000,                 // 单次调用超过 3 秒就算失败
  errorThresholdPercentage: 50,  // 失败率超过 50% 跳闸
  resetTimeout: 30000,           // OPEN 状态维持 30 秒后进入 HALF-OPEN
};

const breaker = new CircuitBreaker(callDownstreamApi, options);
breaker.fallback(() => getCachedFallbackData());

breaker.on('open', () => console.log('断路器跳闸，进入 OPEN'));
breaker.on('halfOpen', () => console.log('断路器进入探测状态 HALF-OPEN'));
breaker.on('close', () => console.log('断路器恢复正常，进入 CLOSE'));

breaker.fire().then(console.log).catch(console.error);
```

| 参数 Knob | 含义 Plain meaning | 起始值 Starting value |
| --- | --- | --- |
| `timeout` | 单次调用超时毫秒数，超时直接判失败 / Per-call timeout in milliseconds; a timeout is counted as a failure | `3000` |
| `errorThresholdPercentage` | 失败率百分比阈值 / Failure-rate percentage threshold | `50` |
| `resetTimeout` | OPEN 状态维持的毫秒数 / Milliseconds the breaker stays OPEN | `30000` |
| `rollingCountTimeout` | 统计窗口总长度（毫秒） / Total length of the statistics window in milliseconds | `10000` |
| `rollingCountBuckets` | 窗口切成几段，段数越多曲线越平滑 / How many buckets the window is split into; more buckets means a smoother curve | `10` |
| `volumeThreshold` | 窗口内样本少于这个数就不跳闸 / Below this sample count in the window the breaker will not trip | `10` |
| `errorFilter` | 返回 true 表示"这个错误不算失败" / Returning true marks an error as not-a-failure | 过滤掉 4xx / filter out 4xx |
| `capacity` | 同时允许并发进行的调用数上限 / Upper bound on concurrent in-flight calls | 依线程池预算而定 / sized to the connection budget |

它唯一比别人强的地方 What it does better：`fallback()` 与事件流 (`open`/`halfOpen`/`close`/`fallback`/`timeout`) 是一等公民，接上 `opossum-prometheus` 就能直接出指标，不需要自己写回调胶水。 / `fallback()` and the event stream (`open`, `halfOpen`, `close`, `fallback`, `timeout`) are first-class, and pairing it with `opossum-prometheus` yields metrics without hand-written callback glue.

---

##### 五种实现横向对比 Cross-Library Comparison

> **大白话:** 这张表回答一个采购问题：手上这门语言，能拿到哪些能力，缺哪些得自己补。 / This table answers a procurement question: given one language, which capabilities come for free and which must be added by hand.

| 实现 Implementation | 语言或层次 Language / layer | 计数方式 Counting strategy | 慢调用检测 Slow-call detection | 内置兜底 Built-in fallback | 指标输出 Metrics | 维护状态 Maintenance |
| --- | --- | --- | --- | --- | --- | --- |
| pybreaker | Python，进程内 / Python, in-process | 连续失败计数 / consecutive failures | 无 / no | 无，由调用方 catch 异常 / no, the caller catches the exception | 靠 listeners 自己接 / only through listeners | 维护中，节奏慢 / maintained, low activity |
| sony/gobreaker | Go，进程内 / Go, in-process | 固定间隔清零的计数 + 自定义 `ReadyToTrip` / interval-reset counters plus a custom `ReadyToTrip` | 无；`IsSuccessful` 的签名是 `func(err error) bool`，只拿到 error，拿不到耗时，因此必须在传给 `Execute` 的函数里自己计时，超阈值时返回一个哨兵 error，再由 `IsSuccessful` 识别它 / no; `IsSuccessful` is `func(err error) bool` and receives only the error, never the elapsed time, so latency must be timed inside the function passed to `Execute`, which returns a sentinel error above the threshold that `IsSuccessful` then recognises | 无 / no | 靠 `OnStateChange` 自己接 / only through `OnStateChange` | 维护中，已发布 v2 / maintained, v2 released |
| resilience4j | Java / JVM，进程内 / Java / JVM, in-process | 按次数或按时间的滑动窗口 / count-based or time-based sliding window | 有，`slowCallRateThreshold` / yes, `slowCallRateThreshold` | 有，`Try.recover` 或注解 `fallbackMethod` / yes, `Try.recover` or the annotation's `fallbackMethod` | 有，原生对接 Micrometer / yes, native Micrometer integration | 活跃维护 / actively maintained |
| opossum | Node.js，进程内 / Node.js, in-process | 分桶滚动百分比 / rolling percentage over buckets | 部分，超时算失败但没有独立慢调用率 / partial, timeouts count as failures but there is no separate slow-call rate | 有，`breaker.fallback()` / yes, `breaker.fallback()` | 有，配 `opossum-prometheus` / yes, with `opossum-prometheus` | 活跃维护 / actively maintained |
| Istio / Envoy | 网络层 sidecar，与语言无关 / network-layer sidecar, language agnostic | 按上游主机统计连续 5xx 或错误率 / consecutive 5xx or error rate, counted per upstream host | 无基于延迟的弹出 / no latency-based ejection | 无，只能踢掉主机 / no, it can only eject hosts | 有，Envoy 原生暴露 Prometheus 指标 / yes, Envoy exposes Prometheus metrics natively | 活跃维护 / actively maintained |

---

##### 什么算失败 What Counts as a Failure

> **大白话:** 打电话时对方说"这个号码不存在"，那是拨错了号，不是电话线断了；可是很多断路器默认把这两件事都记成"线路故障"，于是自己填错表单也能把整条线掐掉。 / When the other end says "no such number", the dialling was wrong, the line is not broken; yet many breakers record both cases as line faults, so a badly filled form can cut the whole line.

这是生产环境中最常见、也最容易被忽略的一个配置错误：绝大多数包装库默认把**任何异常**都记成一次断路器失败。

This is the most common and most easily missed misconfiguration in production: most wrapper libraries count <font color=OrangeRed>every exception</font> as a breaker failure by default.

后果非常具体。假设某个接口用 `raise_for_status()` 这类写法，那么下游返回 `404 Not Found`（资源不存在）或 `422 Unprocessable Entity`（提交的数据校验没通过）都会抛异常。这两种响应说明下游**完全健康**——它正确地读懂了请求并明确拒绝了它。但断路器只看到"又失败一次"，连续几次之后就跳闸，把一个健康的依赖整体切断。真正的用户随后看到的是"服务不可用"，而根因只是某个客户端在反复提交一个错误的表单。

The consequence is concrete. If an endpoint is wrapped with something like `raise_for_status()`, then a downstream `404 Not Found` (the resource does not exist) or `422 Unprocessable Entity` (the submitted data failed validation) raises an exception. Both of those responses prove the downstream is perfectly healthy: it parsed the request correctly and deliberately refused it. The breaker only sees another failure, trips after a few of them, and cuts off a healthy dependency entirely. Real users then see "service unavailable", while the root cause was one client resubmitting one malformed form.

判断规则很短 The rule is short:

| 类别 Category | 例子 Example | 算失败吗 Counts as failure |
| --- | --- | --- |
| 传输层故障 Transport-level failure | 连接被拒、DNS 解析失败、TLS 握手失败、读超时 / connection refused, DNS failure, TLS handshake failure, read timeout | 算 Yes |
| 服务端错误 Server-side error | `500`、`502`、`503`、`504`（`501` 与 `505` 不算，它们不会自行恢复 / `501` and `505` do not count, since they will not heal on their own） | 算 Yes |
| 请求超时 Request timeout | `408 Request Timeout` | 算；状态码落在 4xx 段，但语义是服务端没能在时限内读完请求，属于服务端侧的时间问题 / Yes; the code sits in the 4xx range, but the semantics are that the server did not finish reading the request in time, which is a server-side timing fault |
| 限流信号 Throttling signal | `429 Too Many Requests` | 算，但应优先尊重 `Retry-After` / Yes, but honour `Retry-After` first |
| 客户端错误 Client-side error | `400`、`401`、`403`、`404`、`409`、`422` | 不算 No |
| 业务性拒绝 Business rejection | 下游返回 `200` 且 body 里写着"余额不足" / downstream returns `200` with "insufficient balance" in the body | 不算 No |

`401` 和 `403` 有一个例外需要留意：如果整个服务的凭证过期，所有请求都会变成 `401`，这时它其实是一次真实的故障。处理办法不是让断路器去管，而是单独告警凭证状态。

One caveat applies to `401` and `403`: if a whole service's credentials expire, every request becomes `401`, and that genuinely is an outage. The right handling is not to delegate it to the breaker but to alert on credential state separately.

**修正版 Corrected version — pybreaker**

原始示例的问题：`response.raise_for_status()` 会对 4xx 抛 `requests.HTTPError`，而 `CircuitBreaker(fail_max=5, reset_timeout=60)` 没有配 `exclude`，因此 5 个 404 就足以让断路器跳闸。原始代码保留在上方未改动。

What was wrong in the original example: `response.raise_for_status()` raises `requests.HTTPError` for 4xx, and `CircuitBreaker(fail_max=5, reset_timeout=60)` sets no `exclude`, so five 404 responses are enough to trip the breaker. The original code above is left untouched.

```python
import pybreaker
import requests

def is_client_error(exc: BaseException) -> bool:
    # 返回 True 表示"这个异常不算断路器失败"
    # Returning True marks the exception as not-a-breaker-failure
    if not isinstance(exc, requests.HTTPError) or exc.response is None:
        return False
    # 429 是限流，属于真实的服务端压力信号，仍然算失败
    # 429 is throttling, a genuine server-pressure signal, so it still counts
    if exc.response.status_code == 429:
        return False
    return 400 <= exc.response.status_code < 500

breaker = pybreaker.CircuitBreaker(
    fail_max=5,
    reset_timeout=60,
    exclude=[is_client_error],  # 也可以直接填异常类型 / exception classes are accepted here too
)
```

**修正版 Corrected version — resilience4j**

`recordExceptions` 是白名单，`ignoreExceptions` 是黑名单，黑名单优先级更高。两者都不配时，默认所有异常都算失败。

`recordExceptions` is an allow-list and `ignoreExceptions` is a deny-list, with the deny-list taking priority. When neither is set, every exception counts as a failure by default.

```java
CircuitBreakerConfig config = CircuitBreakerConfig.custom()
    .failureRateThreshold(50)
    .slidingWindowType(CircuitBreakerConfig.SlidingWindowType.COUNT_BASED)
    .slidingWindowSize(100)
    .minimumNumberOfCalls(20)
    // 只有传输层和服务端故障才计入失败
    // Only transport-level and server-side faults are recorded as failures
    .recordExceptions(java.io.IOException.class, java.util.concurrent.TimeoutException.class)
    // 业务校验类异常永远不计入，优先级高于上面的白名单
    // Validation exceptions never count; this wins over the allow-list above
    .ignoreExceptions(ClientValidationException.class, ResourceNotFoundException.class)
    .build();
```

对应地，gobreaker 用 `IsSuccessful`、opossum 用 `errorFilter` 达到同一目的，两者都是"返回 true 表示不算失败"。 / The equivalents are `IsSuccessful` in gobreaker and `errorFilter` in opossum, both following the convention that returning true means the error is not counted.

---

##### 服务网格层面的断路 Circuit Breaking at the Service-Mesh Layer

> **大白话:** 进程内断路器像是餐厅前台决定"今天不再向这家供应商下单"；服务网格像是仓库把一箱发霉的货从货架上撤下来，别的箱子照卖。 / An in-process breaker is the front desk deciding to stop ordering from one supplier; a service mesh is the warehouse pulling one mouldy crate off the shelf while the other crates keep selling.

服务网格 (service mesh) 指的是在每个应用容器旁边再跑一个代理进程（sidecar），所有进出流量都先经过它。Istio 是控制面，Envoy 是那个代理。断路能力在 Istio 里通过 `DestinationRule` 配置，与应用代码完全无关。

A service mesh means running a proxy process (a sidecar) beside every application container so that all inbound and outbound traffic passes through it first. Istio is the control plane and Envoy is that proxy. Breaking behaviour is configured in Istio through a `DestinationRule`, entirely outside application code.

```yaml
# 需要 Istio 1.22 及以上；更早版本把 apiVersion 改成 networking.istio.io/v1beta1
# Requires Istio 1.22+; on earlier versions use apiVersion networking.istio.io/v1beta1
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: payment-api-outlier
  namespace: prod
spec:
  # host: 这条规则作用于哪个上游服务 / which upstream service this rule governs
  host: payment-api.prod.svc.cluster.local
  trafficPolicy:
    connectionPool:
      tcp:
        # maxConnections: 到该服务的 TCP 连接总上限，防止连接数打爆下游
        # maxConnections: hard cap on TCP connections to that service, so the downstream is not flooded
        maxConnections: 100
        # connectTimeout: 建立连接的超时，超过就算一次失败
        # connectTimeout: connection-establishment timeout; exceeding it counts as a failure
        connectTimeout: 3s
      http:
        # http1MaxPendingRequests: 排队等连接的请求上限，超出的立刻被拒（这就是舱壁隔离）
        # http1MaxPendingRequests: cap on requests queued waiting for a connection; the excess is rejected immediately, which is bulkheading
        http1MaxPendingRequests: 64
        # http2MaxRequests: 该服务上允许的并发请求总数
        # http2MaxRequests: total concurrent requests allowed against that service
        http2MaxRequests: 200
        # maxRequestsPerConnection: 一条连接复用多少次后关闭，帮助负载重新均衡
        # maxRequestsPerConnection: how many times one connection is reused before closing, which helps rebalance load
        maxRequestsPerConnection: 100
        # maxRetries: 整个集群同时"在途"的重试数量上限（默认 2^32-1），是并发天花板，不是单个请求的重试次数
        # maxRetries: cluster-wide ceiling on retries outstanding to all hosts at one time (default 2^32-1); it is a concurrency cap, not a per-request attempt count
        # 配得太小（例如 2）会让繁忙服务上多余的重试被直接丢弃，Envoy 的 upstream_rq_retry_overflow 上涨并对外表现为 503
        # Setting it too low (2, say) makes a busy service drop surplus retries, raising Envoy's upstream_rq_retry_overflow and surfacing as spurious 503s
        # 单个请求允许重试几次由 VirtualService.spec.http[].retries.attempts 决定
        # Per-request attempt counts live in VirtualService.spec.http[].retries.attempts
        maxRetries: 32
    outlierDetection:
      # consecutive5xxErrors: 某个后端实例连续返回几次 5xx 就把它踢出负载池
      # consecutive5xxErrors: how many 5xx responses in a row eject one backend instance from the load-balancing pool
      consecutive5xxErrors: 5
      # interval: 每隔多久扫描一次各实例的健康状况
      # interval: how often the health of each instance is scanned
      interval: 10s
      # baseEjectionTime: 基础隔离时长；反复被踢的实例，隔离时间会成倍延长
      # baseEjectionTime: base ejection duration; repeatedly ejected instances are ejected for multiples of it
      baseEjectionTime: 30s
      # maxEjectionPercent: 最多允许踢掉多少百分比的实例，防止把整个集群踢空
      # maxEjectionPercent: the largest share of instances that may be ejected, so the whole pool is never emptied
      maxEjectionPercent: 50
      # minHealthPercent: 健康实例低于这个比例时，停止继续弹出
      # minHealthPercent: ejection stops once healthy instances fall below this share
      minHealthPercent: 50
```

这里有一个必须讲清楚的语义差别，否则很容易误以为"上了网格就不用写断路器了"。网格做的是<font color=OrangeRed>把不健康的上游主机从负载均衡池里弹出</font> (host ejection)：它统计的对象是"某个后端实例"，处理动作是"这个实例先别用了，流量转给同服务的其他实例"。它并不包裹"一次逻辑依赖调用"，因此它不知道调用方在业务上想要什么，也就无法在跳闸时返回一个应用级的兜底值——它只能返回 `503`。相反，进程内断路器知道"这次调用是为了取用户头像"，于是可以返回默认头像。

There is one semantic difference that must be stated plainly, otherwise it is easy to conclude that adopting a mesh removes the need for a breaker. What the mesh performs is <font color=OrangeRed>ejecting unhealthy upstream hosts from the load-balancing pool</font>. Its unit of accounting is a single backend instance, and its remedy is to stop sending traffic to that instance and redistribute it to the other instances of the same service. It does not wrap one logical dependency call, so it has no idea what the caller wanted in business terms and cannot return an application-level fallback value when it trips: all it can return is `503`. An in-process breaker, by contrast, knows that the call was fetching a user avatar and can therefore return a default avatar.

还有一个盲区：如果整个下游服务的**所有**实例都同样地慢或同样地返回 5xx，弹出机制无处可弹（`maxEjectionPercent` 会挡住），流量照旧打进去。此时只有应用层断路器能停止发送请求。

There is also a blind spot: if every instance of the downstream service is uniformly slow or uniformly returning 5xx, there is nowhere to eject to, `maxEjectionPercent` blocks further ejection, and traffic keeps flowing. Only an application-level breaker can stop sending requests in that situation.

结论是两层互补，而不是二选一：网格负责"哪台机器不能用"，应用负责"这次调用失败了给用户看什么"。采用服务网格并不能免除写应用层兜底逻辑的责任。

The conclusion is that the two layers are complementary rather than alternatives: the mesh decides which machine is unusable, and the application decides what a user sees when one call fails. Adopting a service mesh does not remove the responsibility of writing an application-level fallback.

---

##### 网关层也能断路 The Gateway Layer Can Also Break Circuits

> **大白话:** 网关、网格、应用三处都装了同一个总闸，一次小抖动可能被三个闸门同时放大成一次全站故障。 / When the gateway, the mesh, and the application all install the same master switch, one small blip can be amplified by three switches at once into a site-wide outage.

API 网关 (Kong、APISIX、Nginx、Spring Cloud Gateway 等) 同样提供断路或熔断插件，本知识库的网关相关笔记里已经覆盖了这些配置，此处不重复。需要强调的只有一点：断路职责必须显式分配，否则三层各自跳闸会造成级联放大和极难定位的故障。

API gateways such as Kong, APISIX, Nginx, and Spring Cloud Gateway also ship breaker plugins, and the gateway notes elsewhere in this knowledge base already cover that configuration, so it is not repeated here. Only one point needs emphasis: breaking responsibility must be assigned explicitly, otherwise three layers tripping independently produce cascading amplification and outages that are extremely hard to localise.

| 层次 Layer | 建议承担的职责 Suggested responsibility |
| --- | --- |
| 网关 Gateway | 面向外部调用方的限流与粗粒度保护 / rate limiting and coarse protection facing external callers |
| 服务网格 Service mesh | 剔除不健康实例、限制连接与并发 / ejecting unhealthy instances, capping connections and concurrency |
| 应用 Application | 单个逻辑依赖的跳闸判定与业务兜底值 / trip decisions for one logical dependency, plus the business fallback value |

---

#### 生产环境中的常见应用模式 Common Production Usage Patterns

> **大白话:** 断路器不是贴在业务代码里的一句孤立的 if 判断，它更像大楼里的空气开关——可以装在插座上、装在楼层配电箱里、也可以装在整栋楼的进线上；装在哪一层，决定了跳闸的时候谁会被断电。/ A circuit breaker is not an isolated if-statement glued into business code; it is closer to the trip switches in a building, which can sit at the outlet, in the floor distribution box, or on the main incoming line, and the level at which it sits decides who loses power when it trips.

在往下看具体模式之前，先把两个词说清楚，因为后面每一段都会用到。 Before the specific patterns, two words need a plain definition, because every paragraph below relies on them.

| 词 Term | 中文解释 | English explanation |
| --- | --- | --- |
| 依赖 dependency | 本服务为了完成一次请求而必须去调用的另一个东西：另一个 HTTP 服务、一个数据库、一个缓存、一个第三方支付接口。 | Anything the service must call in order to finish one request: another HTTP service, a database, a cache, a third-party payment API. |
| 跳闸 trip | 断路器从"放行"状态切换到"直接拒绝"状态的那个瞬间动作，和家里电闸跳掉是同一个意思。 | The instant at which the breaker switches from letting calls through to rejecting them outright, exactly as a household trip switch cuts the circuit. |

本小节的核心概念是 <font color=OrangeRed>断路器的安装层级 breaker placement layer</font>：同一个模式，装在应用代码里、装在数据库连接池外面、还是装在服务网格的 sidecar 里，运维含义完全不同。 The core idea of this subsection is the <font color=OrangeRed>breaker placement layer</font>: the same pattern placed in application code, around a database connection pool, or inside a service-mesh sidecar carries completely different operational consequences.

- **历史起点 Historical origin**：Netflix 的 Hystrix 是第一个把断路器模式在微服务圈里真正普及开的库（2012 年开源，目前只做维护、不再加新功能）；后来的 resilience4j 基本继承了它的设计哲学，只是换成了更轻量的函数式写法。Netflix's Hystrix was the library that first popularized the circuit breaker pattern in microservice architectures (released in 2012, now in maintenance mode); resilience4j largely inherited its design philosophy.

- **服务网格层面 Service-mesh level**：断路可以完全放在基础设施层做，一行业务代码都不用改——例如 Istio 的 `DestinationRule.outlierDetection`，或者 Envoy 自己的 circuit breaker 配置：每个 Pod 旁边的 sidecar 代理会替所有服务自动执行这套逻辑。Circuit breaking can also happen at the infrastructure layer without touching application code, for example Istio's `DestinationRule.outlierDetection` or Envoy's circuit breaker configuration, where a sidecar proxy enforces the logic on behalf of every service automatically.

  **补充说明 Clarification**：Istio 文档把两组配置都归在"circuit breaking"这个标题下，但它们管的事不一样，值得分清：`outlierDetection` 做的是"异常点摘除"，即把连续报错的某个后端实例暂时从负载均衡池里踢出去；`connectionPool` 做的才是"并发与排队上限"，即限制同时在飞的连接数和请求数。原文的说法在 Istio 官方术语下没有错，这里只是补一句区别。Istio's own documentation files both groups of settings under the heading "circuit breaking", but they do different jobs: `outlierDetection` ejects an individual failing backend instance from the load-balancing pool for a while, whereas `connectionPool` caps concurrency and queue depth. The original bullet matches Istio's own terminology; this note only separates the two mechanisms.

- **数据库连接层面 Database connection level**：断路器同样可以套在数据库连接池外面（例如和 HikariCP 搭配使用），这样当数据库持续超时或者干脆拒绝新连接时，请求会立刻失败返回，而不是每个请求都卡在等连接上、最终把整个应用的线程池耗尽、把毫不相关的接口一起拖死。A circuit breaker can also wrap a database connection pool (e.g. alongside HikariCP) so that when the database keeps timing out or refusing connections, calls fail fast instead of exhausting every request thread and dragging down the whole application.

- **降级策略 Fallback strategies**：断路器跳闸之后不能什么都不做，常见的降级方式有：返回缓存里的旧数据、返回一个安全的默认值、关闭某个非核心功能但保留主流程、把请求放进队列稍后异步重试。When the breaker trips, the call still needs to return something — common fallback strategies include serving stale cached data, returning a safe default value, disabling a non-critical feature while keeping the main flow intact, or queueing the request for an asynchronous retry later.

- **配合监控 Pairing with monitoring**：该暴露哪几个信号、哪一个值得配告警，见后面"该看哪些指标 Metrics and Alerts Worth Having"一节。Which signals to expose and which one deserves an alert are covered in the later section 该看哪些指标 Metrics and Alerts Worth Having.

##### 重试和断路器的组合顺序 Composition Order: Retry Inside or Outside the Breaker

> **大白话:** 想象给客服打电话，占线就再拨两次。如果"三次连拨"算一次通话尝试，经理只会记下"这个客户今天打通了没有"；如果每一次拨号都单独记账，经理会以为今天来了三倍的电话量。/ Consider phoning a support line and redialling twice when it is busy. If all three dials count as one attempt, the supervisor records only whether the customer got through today; if each dial is logged separately, the supervisor believes three times as many calls arrived.

重试和断路器都是"包在调用外面的一层"，所以必然有嵌套顺序问题：到底是断路器包着重试，还是重试包着断路器。这个顺序不是风格问题，它直接改变断路器统计出来的失败率。 Retry and the circuit breaker are both wrappers around a call, so a nesting order is unavoidable: either the breaker wraps the retry, or the retry wraps the breaker. The order is not a matter of taste; it directly changes the failure rate the breaker computes.

```text
方案 A（推荐）：重试在里面，断路器在外面
Option A (recommended): retry INSIDE, breaker OUTSIDE

  caller -> +--------------- CIRCUIT BREAKER ----------------+
            |  +----------- RETRY ------------+           |
            |  | attempt 1 -> timeout         |           |
            |  | attempt 2 -> 503             |           |
            |  | attempt 3 -> 200 OK          |           |
            |  +------------------------------+           |
            |  breaker records: 1 success 记一次结果      |
            +-----------------------------------------------+

方案 B（常见，需附加条件）：断路器在里面，重试在外面
Option B (common, but requires an extra condition): breaker INSIDE, retry OUTSIDE

  caller -> +------------------- RETRY ---------------------+
            | attempt 1 -> [BREAKER] -> timeout  += failure |
            | attempt 2 -> [BREAKER] -> 503      += failure |
            | attempt 3 -> [BREAKER] -> 200 OK   += success |
            +-----------------------------------------------+

   breaker records: 3 outcomes for 1 logical call (67% failure)
```

流传最广的说法是"重试必须放在断路器内层"，但这个结论并不是无条件成立的，"常见但错"这种绝对化的标签把话说得过重，上图因此改标为"常见，需附加条件"。两种嵌套各有代价，而主流库的默认顺序恰恰是重试在最外层，所以这里先把事实摆清楚，再给出取舍。 The most widely repeated formulation is that the retry must sit inside the breaker, yet that conclusion does not hold unconditionally, and an absolute label such as "common but wrong" overstates the case, so the diagram above reads "common, but requires an extra condition" instead. Both nestings carry a cost, and the mainstream libraries in fact default to retry-outermost, so the facts come first and the trade-off after them.

先纠正一个流传很广的错误理由：有人说重试放在外层会把打向依赖的流量成倍放大。这个说法是反的。跳闸之前两种嵌套的放大倍数完全一样，都等于尝试次数 N；而跳闸所需的请求数不一样。以 `fail_max=5`、N=3、依赖彻底死掉为例：重试在内层时断路器每次逻辑调用只记一次失败，需要 5 次逻辑调用、也就是 15 个真实请求才跳闸；重试在外层时每次尝试都记一次失败，5 个请求就跳闸了。也就是说，重试在内层给这个已经死掉的依赖多发了三倍的请求，它更晚才把压力降到零。 One widely repeated reason has to be corrected first: the claim that placing the retry outside multiplies the traffic aimed at the dependency. That claim is backwards. Before the trip both nestings amplify by the same factor, namely the attempt count N; what differs is how many requests the trip itself needs. With `fail_max=5`, N=3, and a completely dead dependency: retry-inside records one failure per logical call, so five logical calls, meaning 15 real requests, are needed to trip, whereas retry-outside records one failure per attempt and trips after 5 requests. Retry-inside therefore sends three times more traffic to an already-dead dependency and reaches zero pressure later.

真正站得住脚的理由只有一条：<font color=OrangeRed>断路器计数器的统计有效性 statistical integrity of the breaker's counters</font>。同一次逻辑调用里的三次尝试针对的是同一个故障，它们不是三个独立样本；把它们当成三个独立样本，失败率就被人为抬高，断路器会比设计意图更早、更容易跳闸，而且跳闸依据是失真的。如果"失败率"这个数字还要用来定阈值、画看板、发告警，那它就必须是可信的，此时应当让重试在内层，让断路器对每一次逻辑调用只记录一个结果。 Only one reason genuinely holds: the <font color=OrangeRed>statistical integrity of the breaker's counters</font>. Three attempts inside one logical call all observe the same fault and are not three independent samples; treating them as such pushes the measured failure rate up artificially, so the breaker trips earlier and more easily than intended, on a distorted signal. If that failure-rate number is also used to set thresholds, draw dashboards, and raise alerts, then it has to be trustworthy, and in that case the retry belongs inside so the breaker records exactly one outcome per logical call.

所以本文的取舍是：<font color=OrangeRed>为了计数器可信而首选重试在内层，而不是因为它流量更少</font>；如果沿用库的默认顺序（重试在外层），那也是可以接受的，条件是显式排除 open-circuit 拒绝，并且清楚失败率这个指标已经被非独立样本抬高了。 The trade-off taken in this note is therefore: <font color=OrangeRed>retry-inside is preferred for trustworthy counters, not because it sends less traffic</font>; keeping a library's default order, with the retry outside, is also acceptable provided the open-circuit rejection is excluded explicitly and it is understood that the failure-rate metric has been inflated by non-independent samples.

| 嵌套方式 Nesting | 断路器观测到什么 What the breaker observes | 对依赖的压力 Load on the dependency | 结论 Verdict |
| --- | --- | --- | --- |
| 重试在内、断路器在外 retry inside, breaker outside | 每次逻辑调用一个结果，样本独立 one independent outcome per logical call | 跳闸前放大 N 倍；跳闸需要 fail_max x N 个请求（5 x 3 = 15），因此更晚才降到零 amplified N times before the trip, and the trip needs fail_max x N requests (5 x 3 = 15), so pressure reaches zero later | 本文首选，理由是计数器统计有效，不是流量更少 preferred here for counter integrity, not for lower traffic |
| 断路器在内、重试在外 breaker inside, retry outside | 每次逻辑调用 N 个结果，样本不独立，失败率被抬高 N non-independent outcomes per logical call, inflating the failure rate | 跳闸前同样放大 N 倍；跳闸只需 fail_max 个请求（5），因此更早降到零 amplified N times before the trip as well, but the trip needs only fail_max requests (5), so pressure reaches zero sooner | resilience4j 与 Polly 的默认顺序；可接受，但必须排除 open-circuit 拒绝 the default in resilience4j and Polly; acceptable, provided the open-circuit rejection is excluded |

**推论：断路器 OPEN 时的拒绝不是可重试的错误 Corollary: an open-circuit rejection is not a retryable error**：断路器在 OPEN 状态下必须立刻失败返回（fail fast），一微秒都不该等；同时，任何位于断路器外层的重试逻辑都绝对不能重试这个"电路已断开"的拒绝。原因很直白：这个拒绝不是网络抖动，它是本进程内部一个确定性的、在整个 open 窗口内都不会改变的判断，重试它只是白白烧掉重试预算，还会给外层调用方增加毫无意义的延迟。 While OPEN, the breaker must fail fast immediately, without waiting a microsecond; and any retry layer that happens to sit outside the breaker must never retry that open-circuit rejection. The reason is direct: the rejection is not a network blip, it is a deterministic in-process decision that will not change for the whole duration of the open window, so retrying it merely burns the retry budget and adds pointless latency for the caller.

```python
# pip install pybreaker==1.2.0 tenacity==8.5.0
# 方案 A：重试在内层，断路器在外层
# Option A: retry is the inner wrapper, breaker is the outer wrapper
import pybreaker
import requests
from tenacity import (retry, stop_after_attempt, wait_exponential_jitter,
                      retry_if_exception, retry_if_not_exception_type)

# 只有这些结果值得重试：根本没拿到响应，或者拿到一个明确的临时状态码
# Only these outcomes deserve a retry: no response at all, or an explicitly transient status
# 504 与读超时只在操作幂等时才重试，因为请求可能已经被处理过 / retry 504 and read timeouts only when the operation is idempotent, because the request may already have been processed
RETRYABLE_STATUS = frozenset({408, 429, 500, 502, 503, 504})

def _is_retryable(exc: BaseException) -> bool:
    if not isinstance(exc, requests.exceptions.RequestException):
        return False
    resp = getattr(exc, "response", None)
    if resp is None:
        return True  # 连接失败或超时 transport failure or timeout
    return resp.status_code in RETRYABLE_STATUS

def _is_client_error(exc: BaseException) -> bool:
    # 返回 True 表示"这个异常不算断路器失败"，否则 5 个 404 就能切断健康依赖
    # Returning True marks the exception as not-a-breaker-failure; without this,
    # five 404 responses are enough to cut off a perfectly healthy dependency
    resp = getattr(exc, "response", None)
    if resp is None:
        return False
    return 400 <= resp.status_code < 500 and resp.status_code not in RETRYABLE_STATUS

breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=20,
                                   exclude=[_is_client_error])
session = requests.Session()

# 内层：只重试真正可重试的结果，每次尝试都有超时
# Inner layer: retry only genuinely retryable outcomes, and every attempt has a timeout
@retry(stop=stop_after_attempt(3),
       wait=wait_exponential_jitter(initial=0.1, max=2.0),
       retry=retry_if_exception(_is_retryable),
       reraise=True)
def _fetch_price_with_retry(sku: str) -> dict:
    resp = session.get(f"https://pricing.internal/api/price/{sku}",
                       timeout=0.35)  # 单次超时 per-attempt timeout, seconds
    resp.raise_for_status()
    return resp.json()

# 外层：断路器只看到"这次逻辑调用成功还是失败"
# Outer layer: the breaker only sees whether this logical call succeeded
def fetch_price(sku: str) -> dict:
    return breaker.call(_fetch_price_with_retry, sku)

# 若框架强制把重试放在断路器外层，必须显式排除 open-circuit 拒绝
# When a framework forces the retry outside, exclude the open-circuit rejection
@retry(stop=stop_after_attempt(3),
       wait=wait_exponential_jitter(initial=0.1, max=2.0),
       retry=retry_if_not_exception_type(pybreaker.CircuitBreakerError),
       reraise=True)
def fetch_price_outer_retry(sku: str) -> dict:
    return breaker.call(_fetch_price_with_retry, sku)
```

##### 韧性四件套 The Four Resilience Primitives

> **大白话:** 餐厅厨房要不崩，靠四件事：每道菜有最长出菜时间、菜炒糊了可以重炒一次、某个灶台一直出事就先封掉、以及热菜冷菜各用各的灶不互相抢。/ A restaurant kitchen stays functional through four things: a maximum time per dish, permission to re-cook one ruined dish, shutting down a stove that keeps failing, and keeping hot and cold stations on separate equipment so they cannot starve each other.

断路器从来不是单独工作的。工程上真正有效的组合是四个原语一起用，每一个只负责限制一件事。这里最关键的一个是 <font color=OrangeRed>超时 timeout</font>，因为它是其余三个能正常工作的前提。 A breaker never works alone. The combination that actually holds up in production is four primitives together, each bounding exactly one thing. The critical one is the <font color=OrangeRed>timeout</font>, because the other three depend on it.

| 原语 Primitive | 它限制什么 What it bounds | 缺了它会怎样 What goes wrong if it is missing |
| --- | --- | --- |
| 超时 timeout：单次调用最多等多久 | 一次调用占用调用方资源的时间上限 The maximum time one call may hold caller-side resources | 线程/连接被永久占住，故障不会被"记录"为失败，只会表现为整个服务变慢直到卡死 Threads and connections are held forever; the fault is never recorded as a failure, it simply shows up as the whole service slowing to a halt |
| 重试 retry：失败后再试几次 | 单次瞬时故障的影响范围 The blast radius of one transient fault | 本可自愈的抖动（一次丢包、一次实例重启）直接变成用户可见的错误 A self-healing blip such as one dropped packet or one instance restart becomes a user-visible error |
| 断路器 circuit breaker：持续失败就停止调用 | 对一个已经确认坏掉的依赖持续施加的压力 The sustained pressure applied to a dependency already known to be broken | 故障期间调用方持续打满请求，既拖慢自己也阻碍依赖恢复 The caller keeps hammering during the outage, slowing itself down and blocking the dependency's recovery |
| 隔板 bulkhead：为每个依赖单独划定资源额度 | 单个依赖最多能占用多少并发资源 The maximum share of concurrency one dependency may consume | 一个慢依赖吃光全部线程或连接，与它无关的接口一起挂掉（连带故障） One slow dependency consumes every thread or connection and unrelated endpoints fail with it |

**没有单次超时的断路器几乎是无用的 A breaker without a per-call timeout is nearly useless**：这一句必须单独强调：断路器是靠"数失败次数"工作的，而一个永远不返回的调用永远不会被记为失败——它只是挂在那里占着线程，断路器的计数器一动不动，跳闸永远不会发生；线程被这样耗尽之后会发生什么，见下面隔板那一段里的算例。 This point deserves to stand alone: a breaker works by counting failures, and a call that never returns never registers as a failure — it simply hangs, holding a thread, while the breaker's counters stay frozen and the trip never happens; what follows once threads are exhausted this way is worked through in the bulkhead paragraph below.

**隔板到底是什么 What a bulkhead actually is**：隔板这个词来自船舶：船体内部用横向隔墙分成若干互不连通的舱室，撞破一个舱，进水只淹那一舱，船不会整体沉掉。 The word comes from shipbuilding: a hull is divided by transverse walls into compartments that do not connect, so a breach floods one compartment and the ship stays afloat.

放到服务里最具体的形态就是<font color=OrangeRed>每个依赖一个独立连接池 a separate connection pool per dependency</font>。假设某服务要调用推荐服务、库存服务、发票服务三个依赖，一共有 200 个工作线程。如果三者共用一个池，发票服务变慢到每次要 5 秒，用户请求会源源不断地卡在发票调用上，200 个线程很快全被占满，此时首页的推荐和库存查询也一起 503——尽管它们的依赖完全健康。 In service terms the most concrete form is a <font color=OrangeRed>separate connection pool per dependency</font>. Suppose a service calls recommendations, inventory, and invoicing, with 200 worker threads in total. If all three share one pool and invoicing slows to five seconds per call, requests pile up on invoicing, all 200 threads are consumed, and recommendations and inventory start returning 503 as well — even though their own dependencies are perfectly healthy.

改成隔板之后：发票服务最多只能占用 20 个线程，第 21 个打向发票的请求立刻被拒绝并走降级，另外 180 个线程完全不受影响，首页照常工作。 With a bulkhead in place, invoicing may occupy at most 20 threads; the twenty-first invoicing request is rejected immediately and falls back, the other 180 threads are untouched, and the home page keeps working.

##### 参数怎么定 How to Choose the Numbers

> **大白话:** 定断路器的参数不是抽签，它像给水管选阀门口径——先量清楚平时水流多大、水压多高，再挑阀门，而不是随手拧一个。/ Choosing breaker settings is not a lottery; it resembles sizing a valve for a pipe, where the normal flow rate and pressure are measured first and the valve chosen afterwards, rather than picking one at random.

网上抄来的 `failureRateThreshold: 50`、`waitDuration: 60s` 之所以经常不好用，是因为这些数字本来应该是从依赖的实测数据里推出来的。四个参数各有各的推导方法。这里最容易被搞错的是 <font color=OrangeRed>滑动窗口 sliding window</font> 的大小。 Copied-from-the-internet values such as `failureRateThreshold: 50` and `waitDuration: 60s` often behave badly because each number is supposed to be derived from measured data about the dependency. Each of the four settings has its own derivation. The one most often set wrongly is the size of the <font color=OrangeRed>sliding window</font>.

先解释三个统计词，后面要用。 Three statistical terms first, since the derivations use them.

| 词 Term | 中文解释 | English explanation |
| --- | --- | --- |
| p99 延迟 p99 latency | 把最近所有请求的耗时排序，第 99 百分位的那个值；意思是 99% 的请求都比它快。 | The 99th percentile of recent request durations, meaning 99 percent of requests complete faster than this value. |
| 滑动窗口 sliding window | 断路器用来算失败率的那一段最近历史，可以按"最近 N 次调用"算，也可以按"最近 T 秒"算。 | The slice of recent history over which the breaker computes its failure rate, counted either as the last N calls or the last T seconds. |
| 背景错误率 background error rate | 系统完全健康时本来就存在的那一点点失败比例，不是零。 | The small proportion of failures present even when the system is entirely healthy; it is never exactly zero. |

**推导方法 The derivation rules**

| 参数 Setting | 从哪里推出来 How it is derived | 理由 Why |
| --- | --- | --- |
| 单次超时 per-call timeout | 依赖的 p99 延迟乘 1.5 到 2 倍 the dependency's p99 latency times 1.5 to 2 | 既不会把正常的慢尾请求误杀，也不会让一个真正卡住的调用长期占资源 It neither kills legitimately slow tail requests nor lets a genuinely stuck call hold resources for long |
| 滑动窗口 sliding window | 由请求速率反推，保证窗口内样本数足够多（经验值：至少 50 到 100 个样本） derived from the request rate so the window holds enough samples, empirically at least 50 to 100 | 样本太少时失败率的统计噪声极大：只有 5 个样本时，一次失败就是 20% Too few samples make the failure rate extremely noisy: with only five samples, one failure is already 20 percent |
| 失败率阈值 failure-rate threshold | 取背景错误率的 3 到 5 倍，并且至少比它高 20 个百分点 three to five times the background error rate, and at least 20 percentage points above it | 留出余量，避免正常波动就跳闸 Headroom prevents ordinary fluctuation from tripping the breaker |
| OPEN 持续时长 open duration | 约等于该依赖的典型恢复时间（实例重启、主从切换、扩容完成所需时间） roughly the dependency's typical recovery time, such as a restart, a failover, or a scale-out | 太短会在依赖还没好时就放流量进去，太长会让已经恢复的依赖白白闲置 Too short lets traffic in before recovery, too long leaves a recovered dependency idle |

**低流量场景的特殊处理 The low-traffic special case**：窗口大小这条规则在低流量服务上尤其重要。假设某内部服务只有 2 QPS，用一个"最近 10 秒"的时间窗口，窗口里只有约 20 次调用，其中 1 次失败就是 5%，3 次失败就是 15%——单次网络抖动就能把失败率推到阈值附近。低流量服务应该改用基于次数的窗口（例如"最近 100 次调用"），并且设置最小样本数（`minimumNumberOfCalls`），在样本不足时断路器根本不参与判断。 This rule matters most for low-traffic services. Consider an internal service at 2 requests per second with a ten-second time window: the window holds roughly 20 calls, so one failure is 5 percent and three failures are 15 percent — a single network blip can push the rate close to the threshold. Low-traffic services should use a count-based window instead, for example the last 100 calls, together with a minimum sample count (`minimumNumberOfCalls`) below which the breaker does not evaluate anything at all.

**一个完整算例 A worked example**：已知条件：某订单服务调用定价服务，稳定流量 200 QPS，定价服务 p99 延迟 180 毫秒，健康期背景错误率约 0.5%，定价服务单个 Pod 滚动重启大约需要 20 秒恢复。 Given: an order service calls a pricing service at a steady 200 requests per second, the pricing service has a p99 latency of 180 milliseconds, the healthy background error rate is about 0.5 percent, and one pricing pod takes roughly 20 seconds to recover during a rolling restart.

| 参数 Setting | 推导过程 Derivation | 取值 Value |
| --- | --- | --- |
| 单次超时 per-call timeout | 180 ms x 2 = 360 ms，向下取整到一个好记的值 rounded to a memorable value | 350 ms |
| 滑动窗口 sliding window | 200 QPS 下，100 次调用只需 0.5 秒即可攒满，样本量足够且反应快 at 200 rps, 100 calls accumulate in 0.5 s, giving both enough samples and fast reaction | 基于次数 100 次 count-based, 100 |
| 最小样本数 minimum calls | 窗口的一半，避免服务刚启动时用 3 个样本就判死刑 half the window, so a just-started service is not judged on three samples | 50 |
| 失败率阈值 failure-rate threshold | 背景 0.5%：3 到 5 倍只给出 1.5% 到 2.5%，太贴近噪声；"至少高出 20 个百分点"这条更严的规则给出 20.5%，向上取整到一个好记的值 the 3-to-5x rule gives only 1.5 to 2.5 percent, too close to noise, so the stricter 20-point rule binds at 20.5 percent, rounded up to a memorable value | 25% |
| 慢调用也算失败 slow-call threshold | 取超时值的约 0.7 倍，这样慢调用能在被超时掐断之前先被记成慢调用 roughly 0.7 times the timeout, so a slow call is recorded as slow before the timeout aborts it | 250 ms，比例阈值 50% ratio 50% |
| OPEN 持续时长 open duration | 约等于 Pod 恢复时间 20 秒 approximately the 20-second pod recovery time | 20 s，带 ±20% 抖动 with plus or minus 20 percent jitter |
| HALF-OPEN 探测次数 half-open probes | 足够判断趋势又不至于压垮刚恢复的依赖 enough to judge the trend without crushing a just-recovered dependency | 10 |

对应的 resilience4j 配置（Spring Boot 里放在 `application.yml`，依赖 `io.github.resilience4j:resilience4j-spring-boot2` 或 `resilience4j-spring-boot3`，示例针对 resilience4j 2.x）： The corresponding resilience4j configuration, placed in `application.yml` in a Spring Boot application using `io.github.resilience4j:resilience4j-spring-boot2` or `resilience4j-spring-boot3`, targeting resilience4j 2.x:

```yaml
resilience4j:
  circuitbreaker:
    instances:
      pricingService:
        slidingWindowType: COUNT_BASED
        slidingWindowSize: 100
        minimumNumberOfCalls: 50
        failureRateThreshold: 25
        slowCallDurationThreshold: 250ms
        slowCallRateThreshold: 50
        # waitDurationInOpenState 只接受固定值：上下浮动 20% 的抖动在 yml 里无法表达，
        # 必须在代码里用 wait-interval 函数配置，见下面的 Java 片段
        # waitDurationInOpenState only takes a fixed value: the plus-or-minus 20 percent
        # jitter cannot be expressed in yml and must be configured in code with a
        # wait-interval function, as shown in the Java snippet below
        waitDurationInOpenState: 20s
        permittedNumberOfCallsInHalfOpenState: 10
  timelimiter:
    instances:
      pricingService:
        timeoutDuration: 350ms
  retry:
    instances:
      pricingService:
        maxAttempts: 3
        waitDuration: 100ms
        enableExponentialBackoff: true
```

上面表格里的"带上下浮动 20% 抖动"这一条，resilience4j 2.x 的 `application.yml` 里没有对应的键，只能在代码里配： The table entry asking for plus-or-minus 20 percent jitter has no corresponding key in `application.yml` under resilience4j 2.x and can only be configured in code:

```java
// resilience4j 2.x：OPEN 时长的抖动只能通过 wait-interval 函数表达
// resilience4j 2.x expresses jitter on the open duration through a wait-interval function
// import io.github.resilience4j.core.IntervalFunction;
// import java.time.Duration;
CircuitBreakerConfig config = CircuitBreakerConfig.custom()
    // 基准 20 秒，实际取值在 16 到 24 秒之间随机 base 20 s, drawn from 16 to 24 s
    .waitIntervalFunctionInOpenState(
        IntervalFunction.ofRandomized(Duration.ofSeconds(20), 0.2))
    .build();
```

需要注意两点。 Two caveats apply.

第一，resilience4j 的配置文件本身不表达嵌套顺序，顺序由代码里装饰器的组合方式决定。上面这份配置只有在断路器包住重试时才符合前一小节的首选。 First, a resilience4j configuration file does not itself express nesting order, which is decided by how the decorators are composed in code. The configuration above only matches the preference stated in the previous subsection if the breaker wraps the retry.

第二，默认顺序和这个首选是反的，必须刻意覆盖。resilience4j 官方 `Decorators` 的组合顺序是 Retry 包住 CircuitBreaker、CircuitBreaker 包住 RateLimiter、再往里是 TimeLimiter 和 Bulkhead，也就是<font color=OrangeRed>重试在最外层 retry outermost</font>；Polly 的官方指引同样把断路器放在重试内层。因此想按前一小节的首选来做，就必须在代码里显式反过来组合，而不是沿用默认值；如果决定沿用默认值，那就必须显式排除 open-circuit 拒绝，不要让外层重试去重试它。 Second, the default order is the opposite of that preference and has to be overridden deliberately. resilience4j's own `Decorators` composition order is Retry wrapping CircuitBreaker wrapping RateLimiter wrapping TimeLimiter wrapping Bulkhead, that is <font color=OrangeRed>retry outermost</font>, and Polly's guidance likewise places the breaker inside the retry. Following the preference of the previous subsection therefore requires composing the decorators the other way round explicitly rather than relying on the default; keeping the default instead requires excluding the open-circuit rejection explicitly, so the outer retry never retries it.

##### 每个实例各有一个断路器 Breaker State Is Per Instance

> **大白话:** 每个 Pod 里的断路器就像每户人家自己的电闸——邻居家跳闸不会连带把整栋楼断电，这通常正是想要的效果。/ The breaker inside each pod behaves like the trip switch in a single apartment: a neighbour's switch tripping does not cut power to the whole building, which is usually the desired behaviour.

一个常被忽略的事实：断路器状态默认是<font color=OrangeRed>进程内的 in-process</font>。如果一个服务部署了 50 个 Pod，那就有 50 个彼此独立的断路器，各自维护自己的滑动窗口和状态机。 An easily overlooked fact: breaker state is <font color=OrangeRed>in-process</font> by default. A deployment of 50 pods therefore contains 50 independent breakers, each maintaining its own sliding window and state machine.

这带来的直接后果是：跳闸是逐步发生的，不是全局瞬间发生的。哪些 Pod 恰好把请求路由到了坏掉的后端实例，哪些 Pod 就先跳闸；其他 Pod 的窗口里失败还没攒够，仍在正常放行。 The direct consequence is that trips are staggered rather than global. Pods whose requests happened to land on the broken backend instances trip first, while other pods have not yet accumulated enough failures in their windows and keep letting traffic through.

这种错开通常是好事，理由有三条。 This staggering is usually beneficial, for three reasons.

| 好处 Benefit | 中文说明 | English explanation |
| --- | --- | --- |
| 局部故障局部处理 局部性 locality | 如果只有部分后端实例坏了，只有打到它们的那部分 Pod 需要跳闸，全站没必要一起降级。 | When only some backend instances are broken, only the pods routed to them need to trip, and the whole service need not degrade. |
| 天然的渐进探测 natural gradual probing | 50 个断路器的 OPEN 计时起点各不相同，恢复时探测流量天然是分散的，不会所有 Pod 在同一秒一起冲上去。 | The 50 breakers start their open timers at different instants, so probe traffic during recovery is naturally spread out instead of every pod probing in the same second. |
| 没有额外故障点 no extra failure point | 状态存在本地内存里，读写是纳秒级，且不依赖任何外部组件。 | State lives in local memory, reads and writes take nanoseconds, and nothing external is involved. |

**为什么不建议把状态共享到 Redis Why sharing breaker state through Redis is normally a bad trade**：一个很自然的想法是：把断路器状态放进 Redis，让 50 个 Pod 共享，这样跳闸就是全局一致的。这个想法在绝大多数场景下是亏的。 A natural idea is to store breaker state in Redis so that all 50 pods share it and trips become globally consistent. In most situations the trade is a losing one.

| 代价 Cost | 中文说明 | English explanation |
| --- | --- | --- |
| 在故障路径上引入新依赖 a new dependency in the failure path | 断路器的全部意义是在依赖故障时保护自己；如果判断"要不要放行"这件事本身需要一次网络调用，那么 Redis 抖动的时候，连"快速失败"都做不到了。 | The entire point of the breaker is self-protection during a dependency outage; if deciding whether to allow a call itself requires a network round trip, then a Redis blip removes even the ability to fail fast. |
| 每次调用增加延迟 latency on every call | 本地内存判断是纳秒级，Redis 往返是毫秒级，而这个开销加在每一次调用上，包括系统完全健康的时候。 | An in-memory check costs nanoseconds while a Redis round trip costs milliseconds, and that overhead applies to every call, including when everything is healthy. |
| 放大误判 amplified misjudgement | 状态全局共享意味着一次错误的跳闸判断会立刻让全部 50 个 Pod 同时停止调用，故障半径从局部变成全局。 | Globally shared state means one incorrect trip decision immediately stops all 50 pods, expanding the blast radius from local to global. |
| Redis 本身也需要断路器 Redis needs a breaker too | 于是问题变成"谁来保护保护者"，逻辑上开始循环。 | The question becomes who protects the protector, and the reasoning starts to loop. |

真正需要全局视角的场合，正确做法不是共享断路器状态，而是在基础设施层做：服务网格的 sidecar 本身就在每个 Pod 里执行摘除逻辑，而控制平面掌握全局健康信息，两者分工明确。 Where a global view is genuinely required, the correct approach is not shared breaker state but infrastructure-level enforcement: the service-mesh sidecar performs ejection locally in each pod while the control plane holds the global health picture, keeping the two roles separate.

##### 恢复时的二次冲击 The Recovery Stampede

> **大白话:** 商场停电后重新供电，如果全楼几百台空调在同一秒一起启动，电闸会立刻再跳一次；分批启动才能真正恢复。/ When power returns to a shopping centre, hundreds of air conditioners starting in the same second trip the main breaker again; only a staged start-up actually restores service.

断路器闭合的那一瞬间是整个生命周期里最危险的时刻，这件事很反直觉。跳闸期间被拦下的流量并没有消失，它一直在积压：上游还在发请求，用户还在刷新，队列还在增长。断路器一闭合，这些被压制的流量在同一瞬间全部涌向那个刚刚才勉强站起来的依赖，很可能把它当场再打死一次，于是断路器再跳闸，形成 OPEN 与 CLOSE 之间的反复循环。 The instant the breaker closes is the most dangerous moment in its whole lifecycle, which is counter-intuitive. The traffic suppressed during the open window did not disappear, it accumulated: upstream callers kept sending, users kept refreshing, queues kept growing. The moment the breaker closes, all of that suppressed traffic hits a dependency that has only just barely recovered, quite possibly killing it again on the spot, tripping the breaker once more and producing a loop between OPEN and CLOSE.

这个现象的名字叫 <font color=OrangeRed>恢复踩踏 recovery stampede</font>，它和缓存领域的"缓存雪崩"是同一类问题：一群独立的客户端在同一时刻做同一件事。 The name for this is the <font color=OrangeRed>recovery stampede</font>, and it belongs to the same family as a cache stampede: a crowd of independent clients all doing the same thing at the same instant.

三种缓解手段，通常一起用。 Three mitigations, normally applied together.

| 手段 Mitigation | 做法 What it does | 效果 Effect |
| --- | --- | --- |
| 半开限流探测 limited probes in half-open | HALF-OPEN 状态只放行固定的少量调用（例如 10 次），其余照旧拒绝，等这批探测出结果再决定关闭还是重新打开。 | 用最小代价试探依赖是否真的好了，探测失败时依赖只多承受了 10 次请求。 It tests recovery at minimal cost, and a failed probe costs the dependency only ten extra requests. |
| 渐进放量 gradual ramp-up | 闭合之后不要立刻恢复 100% 流量，先放 10%，观察一个窗口再放 25%、50%、100%；实现上可以在断路器外面再叠一个限流器（rate limiter）。 | 让依赖有时间预热连接池、填充缓存、完成 JIT 编译，而不是一上来就满负荷。 It gives the dependency time to warm connection pools, refill caches, and finish JIT compilation instead of arriving at full load. |
| OPEN 时长加抖动 jitter on the open timeout | 把固定的 20 秒改成 20 秒上下浮动 20%（即 16 到 24 秒之间随机取值），让 50 个 Pod 的探测时刻自然错开。 | 避免整个集群在同一秒一起探测，把一次集体冲击变成一串小请求。 It prevents the whole fleet from probing in the same second, turning one collective surge into a spread-out trickle. |

抖动这一条最容易被忽略但成本最低。如果所有 Pod 都在依赖挂掉的同一时刻跳闸，且 OPEN 时长是一个固定常数，那么它们必然在同一秒结束 OPEN 状态、同一秒发出探测请求——把一个固定值改成一个随机区间就能消掉这个同步效应。 The jitter mitigation is the most often forgotten and the cheapest. If every pod trips at the same instant the dependency fails and the open duration is a fixed constant, then all of them necessarily leave the open state in the same second and probe in the same second; replacing the fixed value with a random range removes that synchronisation.

```python
# 给 OPEN 时长加抖动：基准 20 秒，实际在 16 到 24 秒之间随机取值
# Jitter on the open duration: base 20 s, actual value drawn from 16 to 24 s
import random

BASE_OPEN_SECONDS, JITTER_RATIO = 20.0, 0.2

def next_open_duration() -> float:
    return random.uniform(BASE_OPEN_SECONDS * (1 - JITTER_RATIO),
                          BASE_OPEN_SECONDS * (1 + JITTER_RATIO))
```

##### 反模式 Anti-Patterns

> **大白话:** 装电闸装错位置，比不装更危险——因为它会让人误以为已经安全了。/ A trip switch installed in the wrong place is more dangerous than none at all, because it creates a false sense of safety.

下面这些做法在代码评审里出现的频率相当高，且都有明确的替代方案。其中最危险的一条是把断路器套在<font color=OrangeRed>非幂等写操作 non-idempotent write</font>上。 The practices below appear regularly in code review and each has a clear alternative. The most dangerous is placing a breaker around a <font color=OrangeRed>non-idempotent write</font>.

"幂等"的定义和判断表见本文前面的"幂等 Idempotency"一节。 The definition of idempotency, together with the table for judging it, is in the earlier section "幂等 Idempotency".

| 反模式 Anti-pattern | 为什么有害 Why it is harmful | 应该怎么做 What to do instead |
| --- | --- | --- |
| 给非幂等写操作套断路器却不带幂等键 a breaker around a non-idempotent write with no idempotency key | 断路器只知道调用失败了，不知道"失败"是请求没发出去，还是请求已经到达服务端并成功执行、只是响应在回来的路上超时了。后一种情况下降级或重试会造成重复扣款、重复下单。 The breaker only knows the call failed; it cannot tell whether the request never left or whether it arrived, succeeded, and merely lost its response on the way back. In the second case a fallback or retry produces a duplicate charge or a duplicate order. | 由调用方生成幂等键（例如 UUID）随请求发送，服务端用它去重；只有具备幂等性之后，失败处理才是安全的。 The caller generates an idempotency key such as a UUID and sends it with the request so the server can deduplicate; only once idempotency exists is failure handling safe. |
| 把客户端 4xx 当成失败计入统计 counting client 4xx errors as failures | 依赖其实完全健康，却因为调用方自己的请求有问题而被整体切断。 The dependency is perfectly healthy yet gets cut off entirely because the caller's own requests are wrong. | 判定规则见前面的"什么算失败 What Counts as a Failure"一节。 The rule is in the earlier section "什么算失败 What Counts as a Failure". |
| 窗口太小导致状态来回抖动 a window so small the breaker flaps | 窗口里只有几个样本时，一次失败就能突破阈值，跳闸；探测一次成功又立刻闭合；下一次失败再跳闸。状态在 CLOSE 与 OPEN 之间高频震荡，既保护不了依赖，也让指标和告警完全不可读。 With only a handful of samples, one failure crosses the threshold and trips, one successful probe closes it again, and the next failure trips it once more. The state oscillates rapidly between CLOSE and OPEN, protecting nothing and making metrics and alerts unreadable. | 按上一节的方法从请求速率反推窗口大小，并设置 `minimumNumberOfCalls`；低流量服务改用基于次数的窗口。 Derive the window size from the request rate as described above and set `minimumNumberOfCalls`; low-traffic services should use a count-based window. |
| 用断路器掩盖一个稳定存在的 bug using a breaker to paper over a persistent bug | 断路器处理的是"临时性故障"。如果某个依赖每天固定跳闸三次，那不是韧性问题而是缺陷：断路器让系统表面上还能跑，于是根因永远没人去查，问题被制度化了。 A breaker addresses transient faults. A dependency that trips three times every day is a defect, not a resilience gap: the breaker keeps the system superficially working, so nobody investigates the root cause and the problem becomes institutionalised. | 把每次跳闸都当成一条需要归因的事件记录下来；反复跳闸应当直接进入故障复盘流程，而不是被当作正常噪声。 Record every trip as an event requiring attribution; repeated trips should enter the incident review process rather than being accepted as normal noise. |
| 降级时静默返回空数据 a fallback that silently returns empty data | `catch (Exception e) { return Collections.emptyList(); }` 这类写法会让下游业务逻辑把"依赖挂了"误读成"确实没有数据"，从而做出错误决策：优惠券列表为空于是不打折、库存为空于是标记缺货下架、风控名单为空于是全部放行。数据没坏，业务结论坏了。 Code of the form `catch (Exception e) { return Collections.emptyList(); }` lets downstream logic read "the dependency is down" as "there genuinely is no data", producing wrong decisions: an empty coupon list means no discount, empty inventory means the item is marked out of stock, an empty risk list means everything is approved. The data is intact but the business conclusion is wrong. | 降级结果必须带上"这是降级数据"的标记，让下游能区分空与未知；对于不能容忍未知的场景，宁可返回明确错误，也不要返回一个看起来正常的空值。 A fallback result must carry a marker saying it is degraded so downstream code can distinguish empty from unknown; where unknown cannot be tolerated, returning an explicit error beats returning a plausible-looking empty value. |
| 跳闸不告警，没人知道它发生过 no alert on the trip | 断路器比用户投诉更早知道依赖坏了，只写一行日志就把这个最早的信号浪费掉了。 The breaker learns of a broken dependency before users complain, and a single log line wastes that earliest signal. | 该上报哪些指标、对哪一个告警，见后面的"该看哪些指标 Metrics and Alerts Worth Having"一节。 Which signals to export and which one to alert on are covered in the later section "该看哪些指标 Metrics and Alerts Worth Having". |

##### 怎么测试断路器 How to Test a Breaker

> **大白话:** 消防演习不能等真着火那天才做第一次；断路器也一样，必须在平时人为制造故障，确认它真的会跳、真的会恢复。/ A fire drill cannot wait for the first real fire; a breaker likewise needs faults injected deliberately in advance to confirm that it truly trips and truly recovers.

断路器的代码路径有一个尴尬的特点：它平时永远不执行。只有依赖出问题时那几行才会被走到，而那正是最不希望第一次发现 bug 的时刻。所以它必须被主动测试，测试要分三层。这里最关键的技巧是 <font color=OrangeRed>注入时钟 injected clock</font>。 Breaker code has an awkward property: it never runs in normal operation. Those lines execute only when a dependency fails, which is the worst possible moment to discover a bug in them. It therefore has to be tested deliberately, at three levels. The essential technique is the <font color=OrangeRed>injected clock</font>.

| 层级 Level | 测什么 What it verifies | 工具 Tooling |
| --- | --- | --- |
| 单元测试 unit test | 状态机的每一次跃迁：CLOSE 到 OPEN、OPEN 到 HALF-OPEN、HALF-OPEN 到 CLOSE、HALF-OPEN 回到 OPEN。 Every state transition: CLOSE to OPEN, OPEN to HALF-OPEN, HALF-OPEN to CLOSE, and HALF-OPEN back to OPEN. | 注入时钟 + 打桩的依赖 an injected clock plus a stubbed dependency |
| 集成测试 integration test | 断路器、重试、超时三者组合起来的实际行为，以及降级路径返回的东西对不对。 The combined behaviour of breaker, retry, and timeout, and whether the fallback path returns something correct. | 打桩服务返回固定错误 a stub service returning fixed errors |
| 故障注入 fault injection | 在接近生产的环境里制造真实的网络级故障：延迟、丢包、连接重置、带宽限制。 Real network-level faults in a production-like environment: latency, packet loss, connection resets, bandwidth limits. | toxiproxy、服务网格的 fault injection toxiproxy, service-mesh fault injection |

**为什么必须注入时钟 Why the clock must be injected**：断路器的状态机里有时间条件："OPEN 满 20 秒之后转入 HALF-OPEN"。如果测试代码直接 `time.sleep(20)`，那么一个测试就要跑 20 秒，一套测试跑几分钟，开发者很快就会跳过它们；而且真实睡眠在 CI 上会因为机器负载而不稳定，产生随机失败的脆弱测试。把"现在几点"抽象成一个可替换的对象，测试里就能瞬间把时间推进 20 秒。 The breaker's state machine contains a time condition: after 20 seconds in OPEN, move to HALF-OPEN. If the test calls `time.sleep(20)` directly, one test takes 20 seconds and a suite takes minutes, so developers soon skip it; worse, real sleeps are sensitive to CI machine load and produce flaky failures. Abstracting "what time is it" into a replaceable object lets a test advance the clock by 20 seconds instantly.

```python
# breaker.py
# 一个最小断路器：时间来源通过构造函数注入，因此可被测试替换
# A minimal breaker whose time source is injected via the constructor
# clock 只需实现 now() -> float（单调递增的秒数）
# clock only needs now() -> float, returning monotonically increasing seconds
import threading
from typing import Callable

class BreakerRejection(Exception):
    """断路器自己拒绝的调用。它继承 Exception，所以裸 except Exception 照样会抓住它，
    保护只能来自重试层显式排除这个基类，类型本身挡不住任何人
    A call refused by the breaker itself. It derives from Exception, so a bare
    except Exception still catches it; the protection has to come from the retry
    layer excluding this base explicitly, since the type itself stops nobody."""

class OpenCircuitError(BreakerRejection):
    pass

class Breaker:
    CLOSED, OPEN, HALF_OPEN = "CLOSED", "OPEN", "HALF_OPEN"

    def __init__(self, clock, fail_max: int = 3, open_seconds: float = 20.0,
                 half_open_probes: int = 1):
        self._clock, self._fail_max, self._open_seconds = clock, fail_max, open_seconds
        self._half_open_probes = half_open_probes
        self._state, self._failures, self._opened_at = self.CLOSED, 0, 0.0
        self._probes = 0                 # 半开状态下在飞的探测数 probes in flight
        self._lock = threading.Lock()    # 状态与计数只在锁内改动 state and counters mutate here

    @property
    def state(self) -> str:
        with self._lock:
            self._expire_open()
            return self._state

    def _expire_open(self) -> None:
        # 调用方必须已经持锁 the caller must already hold the lock
        # 读状态时先看 OPEN 窗口是否到期 check whether the open window expired
        if self._state == self.OPEN and self._clock.now() - self._opened_at >= self._open_seconds:
            self._state, self._probes = self.HALF_OPEN, 0

    def _trip(self) -> None:
        # 跳闸时把失败计数清零，否则它会一直累加下去
        # Tripping resets the failure count, which would otherwise grow without bound
        self._state, self._opened_at = self.OPEN, self._clock.now()
        self._failures, self._probes = 0, 0

    def _admit(self) -> None:
        with self._lock:
            self._expire_open()
            if self._state == self.OPEN:
                # OPEN 状态立刻失败，不发起任何调用 fail fast, issue no call
                raise OpenCircuitError("circuit is open")
            if self._state == self.HALF_OPEN:
                # 半开只发固定数量的探测名额，名额用完照旧拒绝
                # Half-open hands out a fixed number of probe slots and rejects the rest
                if self._probes >= self._half_open_probes:
                    raise OpenCircuitError("half-open probe slots are taken")
                self._probes += 1

    def call(self, fn: Callable[[], object]) -> object:
        self._admit()
        try:
            result = fn()
        except Exception:
            with self._lock:
                self._failures += 1
                if self._state == self.HALF_OPEN or self._failures >= self._fail_max:
                    self._trip()
            raise
        with self._lock:
            self._state, self._failures, self._probes = self.CLOSED, 0, 0
        return result
```

**`BreakerRejection` 挡不住 `except Exception` Why `BreakerRejection` does not stop `except Exception`**：这个异常类型本身不提供任何保护。在 Python 里，只要异常继承自 `Exception`，一个裸的 `except Exception:` 就一定会捕获它，熔断器的 open-circuit 拒绝也不例外——一个默认写法的重试循环会照样抓住这个拒绝并重试三次，正好违反"open-circuit 拒绝绝不能被重试"这条规则。因此这条规则只能由重试层显式排除该类型来保证，继承关系保证不了。唯一能躲开 `except Exception` 的做法是改成继承 `BaseException`，但并不推荐：那样它同时也会逃出普通的错误处理，把该记日志、该收尾的地方一起跳过。 / The exception type itself provides no protection. In Python, any exception deriving from `Exception` will be caught by a bare `except Exception:`, and the breaker's open-circuit rejection is no exception, so a default-shaped retry loop catches that rejection and retries it three times, breaking the very rule that an open-circuit rejection must never be retried. The rule can therefore only be enforced by the retry layer excluding the type explicitly; the class hierarchy cannot enforce it. The only way to become uncatchable by `except Exception` would be to derive from `BaseException`, which is not recommended, because it would also escape ordinary error handling and skip the places that should log and clean up.

正确的顺序是把拒绝类型放在通用处理之前 The correct ordering places the rejection type ahead of the generic handler:

```python
import time

# 先接住熔断器的拒绝并原样上抛，再让真正可重试的失败落到通用分支
# Catch the breaker's rejection and re-raise it first, then let genuinely retryable failures reach the generic branch
def fetch_price_with_retry(breaker, fetch_price, attempts: int = 3):
    for attempt in range(attempts):
        try:
            return breaker.call(fetch_price)
        except BreakerRejection:
            # 电路已断开，重试没有意义，立刻向上抛
            # The circuit is open, retrying is pointless, so propagate at once
            raise
        except Exception:
            # 只有落到这里的失败才是真正可重试的
            # Only failures reaching this branch are genuinely retryable
            if attempt == attempts - 1:
                raise
            time.sleep(0.1 * 2 ** attempt)
```

```python
# test_breaker.py  ->  pip install pytest==8.3.3 && pytest -q test_breaker.py
import sys
import threading

import pytest

from breaker import Breaker, OpenCircuitError

class FakeClock:
    """可手动推进的假时钟 A fake clock that can be advanced by hand."""

    def __init__(self) -> None:
        self._t = 0.0

    def now(self) -> float:
        return self._t

    def advance(self, seconds: float) -> None:
        self._t += seconds  # 瞬间推进，不真的睡 advance instantly, never sleep

def boom():
    raise ConnectionError("dependency unreachable")

def ok():
    return "200 OK"

def test_open_to_half_open_after_timeout():
    clock = FakeClock()
    breaker = Breaker(clock, fail_max=3, open_seconds=20.0)

    # 连续三次失败之后应当跳闸 three consecutive failures must trip the breaker
    for _ in range(3):
        with pytest.raises(ConnectionError):
            breaker.call(boom)
    assert breaker.state == Breaker.OPEN

    # OPEN 期间必须立刻拒绝，且不调用依赖
    # While OPEN the call is rejected immediately, without touching the dependency
    with pytest.raises(OpenCircuitError):
        breaker.call(ok)

    # 推进到 19.9 秒：未到期，仍然 OPEN
    # Advance to 19.9 s: the window has not expired, the state is still OPEN
    clock.advance(19.9)
    assert breaker.state == Breaker.OPEN

    # 再推进 0.2 秒跨过边界：转入 HALF-OPEN，全过程零真实等待
    # Cross the boundary: the state becomes HALF-OPEN, with no real waiting at all
    clock.advance(0.2)
    assert breaker.state == Breaker.HALF_OPEN

def test_half_open_probe_decides_next_state():
    clock = FakeClock()
    breaker = Breaker(clock, fail_max=3, open_seconds=20.0)
    for _ in range(3):
        with pytest.raises(ConnectionError):
            breaker.call(boom)

    # 半开状态下探测失败，立刻回到 OPEN 并重置计时
    # A failed probe in half-open returns to OPEN and restarts the timer
    clock.advance(20.1)
    with pytest.raises(ConnectionError):
        breaker.call(boom)
    assert breaker.state == Breaker.OPEN

    # 再等一个窗口，这次探测成功，应当闭合
    # After another window a successful probe closes the breaker
    clock.advance(20.1)
    assert breaker.call(ok) == "200 OK"
    assert breaker.state == Breaker.CLOSED

def test_half_open_admits_only_the_permitted_number_of_probes():
    clock = FakeClock()
    breaker = Breaker(clock, fail_max=3, open_seconds=20.0, half_open_probes=1)
    for _ in range(3):
        with pytest.raises(ConnectionError):
            breaker.call(boom)
    clock.advance(20.1)
    assert breaker.state == Breaker.HALF_OPEN

    entered, release = threading.Event(), threading.Event()

    def slow_probe():
        entered.set()
        release.wait(5.0)
        return "200 OK"

    prober = threading.Thread(target=lambda: breaker.call(slow_probe))
    prober.start()
    assert entered.wait(5.0)

    # 唯一的探测名额已被占用，第二个调用方必须被立刻拒绝
    # The single probe slot is taken, so a second caller must be rejected at once
    with pytest.raises(OpenCircuitError):
        breaker.call(ok)

    release.set()
    prober.join(5.0)
    assert breaker.state == Breaker.CLOSED

def test_failure_counter_is_reset_when_the_breaker_trips():
    clock = FakeClock()
    breaker = Breaker(clock, fail_max=3, open_seconds=20.0)
    for _ in range(3):
        with pytest.raises(ConnectionError):
            breaker.call(boom)

    # 跳闸之后计数器必须归零，否则它会无界增长
    # After a trip the counter must be back to zero, otherwise it grows without bound
    assert breaker.state == Breaker.OPEN
    assert breaker._failures == 0

def test_concurrent_failures_are_all_counted():
    clock = FakeClock()
    workers, per_worker = 32, 5000
    breaker = Breaker(clock, fail_max=workers * per_worker + 1, open_seconds=20.0)

    def hammer():
        for _ in range(per_worker):
            with pytest.raises(ConnectionError):
                breaker.call(boom)

    # 把线程切换间隔调到极小，让缺锁时的读改写竞态几乎必然发生
    # A tiny switch interval makes the lock-free read-modify-write race almost certain to appear
    previous_interval = sys.getswitchinterval()
    sys.setswitchinterval(1e-6)
    try:
        threads = [threading.Thread(target=hammer) for _ in range(workers)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(120.0)
    finally:
        sys.setswitchinterval(previous_interval)

    # 没有锁的话这个数会偏小，而丢掉的每一个增量都是丢掉的一个失败样本
    # Without a lock this count comes out short, and every lost increment is a lost failure
    assert breaker._failures == workers * per_worker
```

**网络层故障注入 Fault injection at the network level**：单元测试证明状态机对，但证明不了整条链路对——真正的超时行为、连接池行为、TLS 握手行为都只有真流量才能暴露。toxiproxy 是一个放在应用和依赖之间的代理，可以按需注入延迟、断连、限带宽。 Unit tests prove the state machine is correct but cannot prove the whole path is: real timeout behaviour, connection-pool behaviour, and TLS handshake behaviour only appear under real traffic. toxiproxy is a proxy placed between the application and the dependency that injects latency, connection cuts, and bandwidth limits on demand.

```bash
# 启动 toxiproxy Start toxiproxy (image from Shopify's official repository)
docker run -d --name toxiproxy -p 8474:8474 -p 26379:26379 \
  ghcr.io/shopify/toxiproxy:2.9.0

# 建代理：本地 26379 转发到真实依赖 Proxy local 26379 to the real dependency
toxiproxy-cli create -l 0.0.0.0:26379 -u pricing.internal:443 pricing

# 注入 2 秒延迟，远超 350 ms 超时，应当跳闸
# Inject 2 s of latency, far beyond the 350 ms timeout, tripping the breaker
toxiproxy-cli toxic add pricing -t latency -a latency=2000

# 移除故障，观察恢复 Remove the fault and watch the recovery
toxiproxy-cli toxic remove pricing -n latency_downstream
```

如果服务跑在服务网格上，同样的实验可以不改任何部署、直接用网格自带的 fault injection 完成：Istio 在 `VirtualService.spec.http[].fault` 下提供 `delay`（注入固定延迟）和 `abort`（按比例返回指定 HTTP 状态码）两种故障，按百分比生效，实验做完删掉这段配置即可。 For a service running on a service mesh the same experiment needs no deployment change: Istio exposes `delay` for injecting fixed latency and `abort` for returning a chosen HTTP status to a percentage of traffic, both under `VirtualService.spec.http[].fault`, and the configuration is simply removed once the experiment ends.

##### 该看哪些指标 Metrics and Alerts Worth Having

> **大白话:** 断路器不上报指标，就等于家里的电闸装在了没人去的地下室——它可能已经跳了一个星期，而全家人只是在猜为什么灯不亮。/ A breaker that reports no metrics is like a trip switch in a basement nobody visits: it may have been open for a week while the household merely guesses why the lights are off.

断路器应当暴露四个信号。名称参考 resilience4j 的 micrometer 集成（依赖 `io.github.resilience4j:resilience4j-micrometer`），其他库的命名会不同但语义一致。 A breaker should export four signals. The names below follow resilience4j's micrometer integration, provided by `io.github.resilience4j:resilience4j-micrometer`; other libraries use different names with the same semantics.

| 信号 Signal | 类型 Type | 含义 Meaning | 告警还是看板 Alert or dashboard |
| --- | --- | --- | --- |
| 断路器状态 breaker state（`resilience4j_circuitbreaker_state`） | 仪表 gauge | 当前处于 CLOSED / OPEN / HALF-OPEN 中的哪一个，通常按状态打标签、值为 0 或 1。 Which of CLOSED, OPEN, or HALF-OPEN is current, usually labelled by state with a value of 0 or 1. | 告警 alert：持续 OPEN 超过一个 OPEN 时长就应该有人被叫醒 an OPEN state lasting longer than one open duration should wake somebody |
| 跳闸次数 trip count（状态迁移计数 state-transition counter） | 计数器 counter | 累计跳闸了多少次，是"这个依赖是否稳定"最直接的证据。 How many times the breaker has tripped in total, the most direct evidence of whether a dependency is stable. | 告警 alert：单位时间内跳闸次数上升，说明依赖在反复抖动 a rising trip rate means the dependency is flapping |
| 被拒调用数 rejected calls（`resilience4j_circuitbreaker_not_permitted_calls_total`） | 计数器 counter | 因为断路器处于 OPEN 而根本没发出去的调用数，直接等于"被牺牲掉的请求量"。 The number of calls never issued because the breaker was OPEN, which equals the volume of sacrificed requests. | 看板 dashboard，可加二级告警 dashboard, with a secondary alert：用来评估用户影响面 it quantifies user impact |
| 降级执行次数 fallback invocations（自行埋点 custom counter） | 计数器 counter | 降级路径被走了多少次；如果这个数长期不为零，说明系统实际上一直在降级运行。 How often the fallback path ran; a persistently non-zero value means the system has effectively been running degraded. | 看板 dashboard：并按降级类型分标签 dashboard, labelled by fallback type |

附带两个通常已经存在但值得一起看的指标：调用延迟分布（用来重新校准超时值）和失败率本身（用来验证阈值设得合不合理）。 Two further signals usually already exist and deserve to be viewed alongside: the latency distribution, used to recalibrate the timeout, and the failure rate itself, used to check whether the threshold is set sensibly.

**为什么要对跳闸本身告警 Why the trip itself deserves the alert**：对跳闸告警，而不是等下游用户错误率上升再告警，买到的是时间。跳闸发生在依赖刚开始持续失败的那一刻，而此时降级还在生效，用户看到的可能只是"推荐位空了"这种轻微异常，错误率指标可能完全没动；等到用户可见错误率涨上来，往往已经过去几分钟、影响面已经扩大。对跳闸告警意味着工程师是在降级还兜得住的时候介入，而不是在兜不住之后。 Alerting on the trip rather than waiting for downstream user error rates to rise buys time. The trip happens at the moment the dependency begins failing persistently, while the fallback is still working, so users may see only a mild anomaly such as an empty recommendation slot and the error-rate metric may not have moved at all; by the time user-visible errors climb, minutes have passed and the affected surface has grown. Alerting on the trip means engineers intervene while the fallback still holds, rather than after it has stopped holding.

一条具体的 Prometheus 告警规则示例（针对 Prometheus 2.x 的 `alerting_rules` 格式）： A concrete Prometheus alerting rule, in the `alerting_rules` format of Prometheus 2.x:

```yaml
groups:
  - name: circuitbreaker
    rules:
      # 断路器持续 OPEN 超过 1 分钟（远大于 20s 的 OPEN 时长）
      # A breaker stayed OPEN for over a minute, well beyond the 20 s duration
      # 这里必须用原始指标配 for: 1m：max_over_time 只要窗口里出现过一次 1 就为真，
      # 于是 15 秒的抖动也会触发，而且断路器闭合之后它还会继续为真整整一分钟
      # The raw metric with for: 1m is required: max_over_time is true if the series hit 1
      # anywhere in the window, so a 15-second blip fires it and it stays true for a full
      # minute after the breaker has already closed
      - alert: CircuitBreakerStuckOpen
        expr: resilience4j_circuitbreaker_state{state="open"} == 1
        for: 1m
        labels: {severity: warning}
        annotations: {summary: "breaker {{ $labels.name }} is stuck open"}
```

---

## Retry 设计模式在客户端的应用与实现 Applying and Implementing the Retry Pattern on the Client

> **大白话:** 服务端像酒店里的总台，有专人帮各个部门重打电话；客户端就像客人自己房间里的电话机，没人代打，得自己学会"占线就过一会儿再拨"。 / A server sits inside a hotel where the front desk redials on behalf of every department; a client is the phone in a guest room, where nobody redials for it, so it must learn to wait a moment and dial again itself.

- 在服务端，Retry 的机制被大量运用，尤其是在云端微服务的架构上。很多云平台本身就提供了主体（比如服务，节点等）之间的retry机制从而提高整个系统的稳定性。
  - On the server side the retry mechanism is used heavily, especially in cloud microservice architectures. Many cloud platforms already provide retry between participants such as services and nodes, which raises the stability of the whole system. 名词解释 Term: 微服务 microservice 指把一个大程序拆成许多小程序，各自独立部署、通过网络互相调用。 / A microservice means one large program split into many small programs, each deployed independently and calling the others over the network.

- 而客户端，作为一个独立于服务端系统之外，运行在用户手机或电脑上的一个App, 并没有办法享受到平台的这个功能。
  - A client is an App running on a user phone or computer, outside the server system, so it cannot benefit from that platform feature. 客户端 client 在这里就是使用者直接看得见、摸得到的那一层程序。 / Here the client simply means the layer of software the end user can see and touch.

  - 这时，就需要为App加入retry机制, 从而使整个产品更加强壮。
    - The App therefore needs its own retry mechanism so that the product as a whole becomes more robust.

npm 有一个 retry 的包可以帮助我们快速加入retry机制: <https://www.npmjs.com/package/retry>

- npm 是 JavaScript 世界的软件仓库，一条命令就能把别人写好的库装进项目。 / npm is the package registry of the JavaScript world; one command installs a library written by somebody else into a project.
- 安装命令 Install command: `npm install retry`（本节示例针对 `retry` 0.13.x，该包在 npm 上的最新版本即 0.13.1，并不存在 4.x）。 / `npm install retry` (the examples in this subsection target `retry` 0.13.x; 0.13.1 is the latest version published on npm and no 4.x line exists).

retry的实现并不复杂 / Implementing retry is not complicated.

- 完全可以自己写一个这样的工具供一个或多个产品使用。 / Writing such a utility in-house, then sharing it across one or several products, is entirely feasible.
- 更容易更改其中的算法来适应产品的需求。 / An in-house version is easier to modify so the algorithm fits the needs of the product.

下面是我写的一个简单的retry小工具，由于我们向服务端做请求的函数常常是返回promise的，比如 fetch 函数 。这个工具可以为任何一个返回promise的函数注入retry机制。 / The following is a small retry utility. Because functions that call a server usually return a promise, `fetch` being the classic example, this utility can inject retry into any promise-returning function.

- 名词解释 Term: <font color=OrangeRed>promise</font> 相当于一张取货单：先把凭据交出去，货到了再回来通知，代表一个还没完成的异步结果。 / A promise is like a collection ticket handed over before the goods arrive: the ticket is issued first, notification follows once the goods land, and it represents an asynchronous result that has not finished yet.

### 原始实现 The Original Implementation

> **大白话:** 这段代码就是一个包装纸：把原来的函数包起来，外面再套一层"失败就等一会儿再试"的循环。 / This code is wrapping paper: it wraps the original function and adds an outer loop that waits a moment and tries again after a failure.

```javascript
// 这个函数会为你的 promiseFunction (一个返回promise的函数) 注入retry的机制。
// 比如 retryPromiseFunctionGenerator(myPromiseFunction, 4, 1000, true, 4000)
// 会返回一个函数，它的用法和功能与 myPromiseFunction 一样。但如果 Promise reject 了，
// 它就会进行retry, 最多retry 4 次
// 每次时间间隔指数增加，最初是1秒，随后2秒，4秒，
// 由于设定最大delay是4秒，那么之后就会持续delay4秒，直到达到最大retry次数 4 次。
// 如果 enableExponentialBackoff 设为 false, delay就会是一个常量1秒。
const retryPromiseFunctionGenerator = (
  promiseFunction, // 需要被retry的function
  numRetries = defaultNumRetries, // 最多retry几次
  retryDelayMs = defaultRetryDelayMs, // 两次retry间的delay
  enableExponentialBackoff = false, // 是否启动指数增加delay
  maxRetryDelayMs // 最大delay时间
) => async (...args) => {
  for (
    let numRetriesLeft = numRetries;
    numRetriesLeft >= 0;
    numRetriesLeft -= 1
  ) {
    try {
      return await promiseFunction(...args);
    } catch (error) {
      if (numRetriesLeft === 0 || !isTransientFault(error)) {
        throw error;
      }

      const delay = enableExponentialBackoff
        ? Math.min(
            retryDelayMs * 2 ** (numRetries - numRetriesLeft),
            maxRetryDelayMs || Number.MAX_SAFE_INTEGER
          )
        : retryDelayMs;

      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }
};
```

上面的代码原文保留不动，但有两处值得指出的问题。 / The block above is preserved verbatim, and two issues in it are worth pointing out.

| 问题 Issue | 说明 What is wrong | 后果 Consequence |
| --- | --- | --- |
| 代码块语言标注错误 Wrong fence language | 原文围栏写的是 `java`，内容却是 JavaScript；上方围栏已改标为 `javascript`，代码本身未作任何改动。 / The original fence declared `java` while the body is JavaScript; the fence above has been retagged `javascript` and the code itself is untouched. | 语法高亮错乱，读者可能误以为这是 Java 代码。 / Syntax highlighting breaks and a reader may mistake the sample for Java. |
| `isTransientFault` 没有定义 `isTransientFault` is undefined | 代码调用了它，但笔记中从未给出定义或引入。 / The code calls it, yet no definition or import appears anywhere in the note. | 直接照抄会抛 `ReferenceError`，而瞬时/永久故障的判定恰恰是整个模式的地基。 / Copying the block as-is throws a `ReferenceError`, and transient-versus-permanent classification is precisely the foundation of the whole pattern. |
| 可能隐式返回 undefined May implicitly return undefined | `throw` 只在 `catch` 里 `numRetriesLeft === 0` 时发生；如果循环条件先结束，函数会走到末尾并隐式返回 `undefined`。 / The `throw` happens only inside `catch` when `numRetriesLeft === 0`; if the loop condition ends first, control reaches the end of the function and `undefined` is implicitly returned. | 调用方拿到 `undefined` 却没有异常，失败被静默吞掉，非常难排查。 / The caller receives `undefined` with no exception, so the failure is swallowed silently and is very hard to diagnose. |
| 缺少抖动 No jitter | 所有客户端用同一套确定性延迟。 / Every client uses the same deterministic delay. | 大量客户端会在同一毫秒一起重试，形成新的流量尖峰。 / Many clients retry in the same millisecond and create a fresh traffic spike. |
| 无法取消 Not cancellable | 用户离开页面时，`setTimeout` 仍在等待。 / When the user leaves the page the `setTimeout` is still pending. | 浪费电量与流量，且回调可能操作已销毁的界面。 / Battery and data are wasted, and the callback may touch a destroyed view. |

**修正版 Corrected version**

一句话说明改了什么：补上 `isTransientFault` 的完整定义、改用 full jitter 并把上限放在最后截断（因此 `maxRetryDelayMs` 是真正的上限）、让已取消的信号始终抛出取消错误，并保证函数只有"返回值"或"抛异常"两种出口。 / In one line: a complete definition of `isTransientFault` is supplied, jitter becomes full jitter with the cap clamped last so `maxRetryDelayMs` is a real ceiling, an aborted signal always throws the abort error, and the function is guaranteed to either return a value or throw.

```javascript
// 依赖 Dependency: 无第三方库，纯浏览器/Node 18+ 原生 API (AbortSignal, DOMException)。
// No third-party library; native browser or Node 18+ APIs only (AbortSignal, DOMException).
// 用法 Usage: const safeFetch = retryPromiseFunctionGenerator(fetch, 4, 1000, true, 4000);
//            await safeFetch(url, { signal: controller.signal });

// 可重试的 HTTP 状态码：请求超时、被限流、以及服务端的临时性错误。
// Retryable HTTP status codes: request timeout, rate limiting, and temporary server-side errors.
// 504 与读超时只在操作幂等时才重试，因为请求可能已经被处理过 / retry 504 and read timeouts only when the operation is idempotent, because the request may already have been processed
const RETRYABLE_STATUS = new Set([408, 429, 500, 502, 503, 504]);

// 瞬时故障判定是整个模式的地基：判错一次，就会去重试根本不该重试的请求。
// Transient-fault classification is the foundation of the whole pattern: one wrong verdict retries a request that must never be retried.
const isTransientFault = (error) => {
  // fetch 的网络层失败（DNS 解析失败、连接中断）抛出 TypeError，视为瞬时故障。
  // A fetch network-layer failure (DNS failure, dropped connection) throws TypeError, treated as transient.
  if (error instanceof TypeError) return true;
  // 取消不是故障，绝不重试。
  // Cancellation is not a fault and is never retried.
  if (error?.name === 'AbortError') return false;
  // 其余情况按状态码判断；4xx 里只有 408 与 429 值得再试。
  // Otherwise decide by status code; within 4xx only 408 and 429 are worth another attempt.
  const status = error?.status ?? error?.response?.status;
  return typeof status === 'number' && RETRYABLE_STATUS.has(status);
};

// 统一的取消异常，保证两条取消路径抛出完全相同的错误类型。
// One shared cancellation error so both cancellation paths throw exactly the same error type.
const toAbortError = (signal) =>
  signal?.reason ?? new DOMException('Aborted', 'AbortError');

const sleep = (ms, signal) =>
  new Promise((resolve, reject) => {
    // 已经取消就立刻失败 Fail immediately if already aborted
    if (signal?.aborted) {
      reject(toAbortError(signal));
      return;
    }
    const timer = setTimeout(resolve, ms);
    signal?.addEventListener('abort', () => {
      clearTimeout(timer);
      reject(toAbortError(signal));
    }, { once: true });
  });

const retryPromiseFunctionGenerator = (
  promiseFunction,
  numRetries = 3,
  retryDelayMs = 1000,
  enableExponentialBackoff = false,
  maxRetryDelayMs = 30000,
  { signal } = {}
) => async (...args) => {
  let lastError; // 记录最后一次错误，保证出口一定有异常可抛
  for (let attempt = 0; attempt <= numRetries; attempt += 1) {
    try {
      return await promiseFunction(...args);
    } catch (error) {
      lastError = error;

      // 取消优先于一切：只要信号已取消就抛出取消错误，调用方才能把"被取消"和"彻底失败"分开。
      // Cancellation wins over everything: an aborted signal always throws the abort error, so a caller can separate cancelled from permanently failed.
      if (signal?.aborted) {
        throw toAbortError(signal);
      }

      // 不可重试、或次数用尽 -> 立刻抛出，绝不静默返回
      // Not retryable, or budget exhausted -> throw at once, never return silently
      const isLastAttempt = attempt === numRetries;
      if (isLastAttempt || !isTransientFault(error)) {
        throw error;
      }

      // 顺序很关键：先算指数基数，再做 full jitter，最后才截断上限。
      // 上限放最后，maxRetryDelayMs 才是真正的天花板；若先截断再抖动，延迟会突破上限。
      // Order matters: compute the exponential base, then apply full jitter, then clamp last.
      // Clamping last makes maxRetryDelayMs a genuine ceiling; clamping before jitter lets the delay exceed the cap.
      const base = enableExponentialBackoff
        ? retryDelayMs * 2 ** attempt
        : retryDelayMs;
      const delay = Math.min(Math.random() * base, maxRetryDelayMs);

      await sleep(delay, signal);
    }
  }
  // 理论上不可达；仍显式抛出，杜绝隐式 undefined
  // Unreachable in theory; still throws explicitly so undefined can never leak
  throw lastError ?? new Error('retry exhausted with no recorded error');
};
```

### 客户端特有的约束 Constraints Unique to Clients

> **大白话:** 服务端重试像后厨慢慢重做一道菜，客人看不到；客户端重试时客人就坐在桌边盯着表，等太久比这道菜做失败更让人生气。 / A server retry is like a kitchen quietly remaking a dish out of sight; a client retry happens while the guest sits at the table watching the clock, and waiting too long annoys them more than a failed dish would.

| 约束 Constraint | 服务端 Server | 客户端 Client | 应对 What to do |
| --- | --- | --- | --- |
| 谁在等 Who waits | 通常是另一台机器，可容忍数秒。 / Usually another machine, tolerant of several seconds. | 是真人，超过约 2 到 3 秒就感觉卡住。 / A real person, who feels stuck after roughly 2 to 3 seconds. | 设总截止时间而非只设次数。 / Set a total deadline, not only an attempt count. |
| 网络状态 Network state | 机房内网基本常在。 / Data-centre networking is essentially always present. | 可能完全断网（地铁、电梯、飞行模式）。 / May be fully offline: subway, lift, aeroplane mode. | 断网不是瞬时故障，应暂停而非猛冲。 / Being offline is not a transient fault, so pause instead of hammering. |
| 成本 Cost | 成本记在服务器账单上。 / The cost lands on the server bill. | 耗电量与移动流量由用户承担。 / Battery drain and mobile data are paid by the user. | 限制次数，指数退避加抖动。 / Cap the attempts, use exponential backoff with jitter. |
| 生命周期 Lifecycle | 进程长期存活。 / The process lives for a long time. | 页面会被关闭，App 会切到后台。 / Pages get closed and Apps move to the background. | 用 `AbortSignal` 让调用方能取消。 / Expose an `AbortSignal` so the caller can cancel. |

- 总截止时间比"最终一定成功"更重要：宁可 3 秒后给出一个明确的错误提示和"重试"按钮，也不要让界面转圈 30 秒。 / A total deadline matters more than eventual success: a clear error message plus a retry button after 3 seconds beats a spinner that turns for 30 seconds.
- 检测离线状态并暂停：浏览器可用 `navigator.onLine` 与 `online` 事件，恢复联网后再继续，而不是每秒盲目重试。 / Detect the offline state and pause: a browser can use `navigator.onLine` plus the `online` event and resume once connectivity returns, rather than blindly retrying every second.

```javascript
// 离线时挂起，联网后再继续；原生 API，无需安装
// Suspend while offline and resume when back online; native API, nothing to install
const waitUntilOnline = (signal) =>
  navigator.onLine
    ? Promise.resolve()
    : new Promise((resolve, reject) => {
        const onOnline = () => resolve();
        window.addEventListener('online', onOnline, { once: true });
        signal?.addEventListener('abort', () => {
          window.removeEventListener('online', onOnline);
          reject(signal.reason ?? new Error('Aborted'));
        }, { once: true });
      });
```

---

## 监控：更好地在运行时了解你的系统 Monitoring: Understanding the System at Runtime

> **大白话:** 重试就像水管里的暗流，水最后流出来了，但没人知道中间堵了几次；监控就是在管子上装几个透明观察窗。 / Retries are like a hidden current inside plumbing: the water does come out, but nobody knows how many blockages happened on the way, and monitoring installs a few transparent inspection windows along the pipe.

App拥有了retry机制，在客户端运行时，它变得更强壮了，一些失败的服务端请求并不能打到它。 / Once the App has a retry mechanism it becomes more robust at runtime, and some failed server requests can no longer knock it over.

但想知道它在用户手上retry了几次，什么时候retry的，最终失败了没有。 / Still, it is valuable to know how many retries happened on the user device, when they happened, and whether the operation eventually failed.

- 这些信息不仅让我更好的了解用户的实际体验，它们也可以作为服务端性能的指标之一。 / This information gives a clearer picture of the real user experience and doubles as one indicator of server performance.
- 实时对这些信息进行监控可以**尽早的发现服务端的故障** 以减少损失 / Monitoring it in real time makes it possible to **detect server faults early** and reduce the damage.

客户端的监控是一个很大的话题，Retry信息的收集只是其中一个应用场景。 / Client monitoring is a large topic, and collecting retry information is only one use case within it.

- 实现呢很简单。 / The implementation is simple.
- 在每一次执行retry时发送一条log(日志)其中包含你想了解的信息。然后运用第三方或公司内部的日志浏览工具去分析这些日志，从而获得许多有意思的指标。
  - Emit one log line on every retry containing the fields of interest, then analyse those logs with a third-party or in-house log viewer to derive many interesting metrics. 名词解释 Term: <font color=OrangeRed>log</font>（日志）就是程序在运行时写下的一行行"记事本"，事后可以翻查。 / A log is the line-by-line notebook a program writes while running, readable after the fact.
- 例子，我们可以简单地监控retry log 的数量，如果突然激增，那就说明服务端也许出现了一些故障，这时候开发团队可以在第一时间做出反应修复故障，以免对大面积的客户造成影响。
  - For example, simply watching the count of retry logs works well: a sudden spike suggests the server may be faulting, and the development team can react immediately before a large share of customers is affected.
- 当然这不仅仅可以通过监控retry实现，我们也可以监控服务端的http请求失败的数量， / Retry monitoring is not the only route; the count of failed HTTP requests observed on the server can be monitored too.

### 一条重试日志该记录什么 What Belongs in a Retry Log Line

> **大白话:** 就像银行排队叫号：光记"有人重排了队"没用，得记清是几号票、第几次重排、在哪个窗口、等了多久。 / It is like a numbered queue at a bank: recording that somebody re-queued is useless without the ticket number, which attempt it was, which counter, and how long the wait had been.

| 字段 Field | 为什么重要 Why it matters |
| --- | --- |
| `correlation_id` / `request_id`（关联 ID） | 把同一次业务操作的多次尝试串成一条链，也能和服务端日志对上。 / Ties every attempt of one logical operation into a single chain and joins up with server-side logs. |
| `endpoint`（目标接口） | 定位是哪个接口在抖，而不是笼统说"网络不好"。 / Pinpoints which endpoint is flapping instead of blaming the network in general. |
| `attempt`（第几次尝试） | 区分"偶发一次"和"连续四次都失败"，后者严重得多。 / Separates a one-off blip from four consecutive failures, which is far more serious. |
| `elapsed_ms`（累计耗时） | 反映用户真实等待时长，是判断是否该放弃的依据。 / Reflects the real waiting time and drives the decision to give up. |
| `error_class`（错误类别） | 超时、503、DNS 失败的处理方式完全不同。 / A timeout, a 503, and a DNS failure each call for different handling. |
| `outcome`（最终结果） | 只有它能算出"重试挽救率"这个关键指标。 / Only this field allows the key metric, the share of operations rescued by retrying, to be computed. |
| `delay_ms`（本次计算出的延迟） | 验证退避与抖动是否按预期生效。 / Verifies that backoff and jitter behave as intended. |

一条结构化日志的样子 An example structured log line:

```json
{
  "ts": "2021-04-25T09:14:02.481Z",
  "level": "warn",
  "event": "http_retry",
  "correlation_id": "c1f8a2e4-6b90-4d3e-9a11-7c5de0f3b842",
  "endpoint": "POST /api/v2/orders",
  "attempt": 3,
  "max_attempts": 5,
  "elapsed_ms": 3120,
  "delay_ms": 1740,
  "error_class": "HttpTimeout",
  "http_status": null,
  "outcome": "retrying",
  "network": "cellular",
  "app_version": "4.12.0"
}
```

- 注意 `outcome` 取值应枚举化，例如 `retrying` / `succeeded` / `gave_up` / `aborted`，便于聚合统计。 / Note that `outcome` should be an enumeration such as `retrying`, `succeeded`, `gave_up`, or `aborted` so it aggregates cleanly.
- 不要把请求体、token、手机号写进日志。 / Request bodies, tokens, and phone numbers must never appear in these logs.

### 与熔断器指标的关系 How This Relates to Circuit Breaker Metrics

> **大白话:** 重试日志记的是"我又敲了一次门"，熔断器指标记的是"这扇门现在还让不让敲"；两份记录合起来才看得懂整件事。 / A retry log records that the door was knocked on again, while breaker metrics record whether knocking is currently allowed at all, and only both records together explain the full story.

熔断器自身的指标（当前状态、状态切换时刻、被直接拒绝的请求数）已在前面"该看哪些指标 Metrics and Alerts Worth Having"一节统一定义，此处不再重复，只需记住这两组数据互为补充。 / The breaker's own metrics, namely current state, transition timestamps, and the count of requests rejected outright, are defined once in the earlier section 该看哪些指标 Metrics and Alerts Worth Having and are not repeated here; the two sets of data simply complement each other.

---

## Example 实例

> **大白话:** 前面讲的都是道理，这一节是拆开一台真车的引擎盖看里面的零件——一个成熟的库到底怎么写重试循环。

- 服务在请求资源，如果遇到网络异常等情况，导致请求失败，这时需要有个重试机制来继续请求。  
- 常见的做法是重试3次，并随机 sleep 几秒。
- In an application scaffold, the HTTP client normally already wraps a retry method, so a failed request is retried automatically according to configuration.
- 下面以一个常见的 HTTP Client 为例， 看下它是如何实现请求重试。
- 最后整理其他一些重试机制的实现。

| 术语 Term | 白话解释 Plain meaning（术语速查 quick glossary） |
| --- | --- |
| HTTP Client | 一段帮程序去别的服务器"取东西"的代码。 / Code that fetches things from another server on behalf of a program. |
| 重试 Retry / Backoff 退避 | 失败了再打一次同样的电话，而且每次重打前多等一会儿。 / Placing the same call again after it failed, waiting longer before each redial. |
| Jitter 抖动 | 在等待时间上加一点随机，避免所有人同时重打。 / Adding randomness to the wait so that not everyone redials at the same instant. |
| Context 上下文 | 一张"这次任务还算不算数"的通行证，调用方可以随时作废它。 / A permission slip saying whether the task still counts; the caller can void it at any time. |

### go-resty 重试机制的实现 go-resty's Retry Implementation

> **大白话:** go-resty 就是 Go 语言里一个"帮忙打电话取数据"的小助手；reading its source to see that a production retry loop has the same shape as the short examples earlier in the note, only with more guards bolted on.

阅读前的定位说明：

- go-resty 是 Go 语言里最常用的第三方 HTTP 客户端库
- 一行 `client.R().Get(url)` 就能发一个请求
- 安装命令是 `go get github.com/go-resty/resty/v2`，下面的源码对应 v2 分支；
- 读库源码的意义在于，一个真实的重试循环并没有魔法，骨架仍是"尝试 -> 判断要不要再来 -> 等一会儿 -> 再尝试"
- 多出来的部分全是<font color=OrangeRed>护栏 guards</font>——上下文取消、不可重试错误标记、自定义重试条件、等待时间上限。
- a real retry loop contains no magic, its skeleton is still "attempt, decide whether another round is warranted, wait, attempt again", and everything extra is a <font color=OrangeRed>guard</font>: context cancellation, a marker for non-retryable errors, a customizable retry condition, and an upper bound on the wait.

先看下 go-resty 在发送 HTTP 请求时， 请求重试的实现： / First, here is how go-resty implements request retry when sending an HTTP request:

```go
// Execute method performs the HTTP request with given HTTP method and URL

// for current `Request`.
//   resp, err := client.R().Execute(resty.GET, "http://httpbin.org/get")
func (r *Request) Execute(method, url string) (*Response, error) {
    var addrs []*net.SRV
    var resp *Response
    var err error

    if r.isMultiPart && !(method == MethodPost || method == MethodPut || method == MethodPatch) {
        return nil, fmt.Errorf("multipart content is not allowed in HTTP verb [%v]", method)
    }

    if r.SRV != nil {
        _, addrs, err = net.LookupSRV(r.SRV.Service, "tcp", r.SRV.Domain)
        if err != nil {
            return nil, err
        }
    }

    r.Method = method
    r.URL = r.selectAddr(addrs, url, 0)

    if r.client.RetryCount == 0 {
        resp, err = r.client.execute(r)
        return resp, unwrapNoRetryErr(err)
    }
    // 如果 r.client.RetryCount 不等于0 ，执行 Backoff() 函数
    // EN: if RetryCount is not zero, hand the work to Backoff()

    // Backoff() 方法接收一个处理函数参数
    // EN: Backoff() takes the operation to run as its first argument
    // 根据重试策略，进行 attempt 次网络请求，同时接收 Retries()、WaitTime()等函数参数
    // EN: it performs `attempt` calls per the retry policy and accepts options such as Retries()
    attempt := 0
    err = Backoff(
        func() (*Response, error) {
            attempt++

            r.URL = r.selectAddr(addrs, url, attempt)

            resp, err = r.client.execute(r)
            // 如果没有设置重试次数，执行 r.client.execute(r) ：
            // 直接请求 Request ， 返回 Response 和 error。
            // EN: r.client.execute(r) issues the request and returns Response and error

            if err != nil {
                r.client.log.Errorf("%v, Attempt %v", err, attempt)
            }

            return resp, err
        },
        Retries(r.client.RetryCount),
        WaitTime(r.client.RetryWaitTime),
        MaxWaitTime(r.client.RetryMaxWaitTime),
        RetryConditions(r.client.RetryConditions),
    )
    return resp, unwrapNoRetryErr(err)
}
```

三个值得注意的设计点：

- `RetryCount == 0` 时完全绕过 Backoff，没有额外开销；
- `r.selectAddr(addrs, url, attempt)` 每轮重算地址，让重试可以换一台后端，避免反复打同一台坏机器；
- `unwrapNoRetryErr(err)` 在两处 return 都出现，把内部的"不要重试"包装剥掉，调用方看到的是原始错误。 /
- Three design points worth noticing: when `RetryCount == 0` Backoff is bypassed entirely, so there is no extra overhead; `r.selectAddr(addrs, url, attempt)` recomputes the address each round so a retry may hit a different backend instead of the same sick machine; and `unwrapNoRetryErr(err)` appears at both return sites, stripping the internal "do not retry" wrapper so the caller sees the original error.

### Backoff函数 The Backoff Function

> **大白话:** 这个函数就是餐厅后厨的传菜员：菜没做好就回头等一会儿再来问，但只要经理喊"这单取消了"，他立刻停下不再问。

```go
// Backoff retries with increasing timeout duration up until X amount of retries
// (Default is 3 attempts, Override with option Retries(n))
func Backoff(operation func() (*Response, error), options ...Option) error {
    // Defaults
    opts := Options{
        maxRetries:      defaultMaxRetries,
        waitTime:        defaultWaitTime,
        maxWaitTime:     defaultMaxWaitTime,
        retryConditions: []RetryConditionFunc{},
    }

    for _, o := range options {
        o(&opts)
    }

    var (
        resp *Response
        err  error
    )

    // 开始进行 opts.maxRetries 次 HTTP 请求
    // EN: begin the loop of HTTP calls bounded by opts.maxRetries
    for attempt := 0; attempt <= opts.maxRetries; attempt++ {
        // 执行处理函数 (发起 HTTP 请求)
        // EN: run the operation, which issues the HTTP request
        resp, err = operation()
        ctx := context.Background()

        // 如果返回结果不为空并且 context 不为空，
        // 保持 response 的请求上下文。
        // EN: if a response and its context exist, keep that request context
        if resp != nil && resp.Request.ctx != nil {
            ctx = resp.Request.ctx
        }
        // 如果上下文出错， 退出 Backoff() 流程
        // EN: if the context is already broken, leave the Backoff flow
        if ctx.Err() != nil {
            return err
        }

        err1 := unwrapNoRetryErr(err)
        // raw error, it used for return users callback.

        needsRetry := err != nil && err == err1
        // retry on a few operation errors by default

        // 执行 retryConditions(), 设置检查重试的条件。
        // EN: run retryConditions() to let the caller define what is retryable
        for _, condition := range opts.retryConditions {
            needsRetry = condition(resp, err1)
            if needsRetry {
                break
            }
        }

        if !needsRetry { //根据 needsRetry 判断是否退出流程
            // EN: needsRetry decides whether the loop stops here
            return err
        }

        // 通过 sleepDuration()计算 Duration
        // （根据此次请求resp, 等待时间配置，最大超时时间和重试次数算出 sleepDuration。
        // 时间算法相对复杂， 具体参考： Exponential Backoff And Jitter）
        // EN: sleepDuration() derives the wait from resp, waitTime, maxWaitTime and attempt
        waitTime, err2 := sleepDuration(resp, opts.waitTime, opts.maxWaitTime, attempt)
        if err2 != nil {
            if err == nil {
                err = err2
            }
            return err
        }

        // 等待 waitTime 进行下个重试。 如果请求完成退出流程
        // EN: wait for waitTime, but abandon the wait if the context is cancelled
        select {
        case <-time.After(waitTime):
        case <-ctx.Done():
            return ctx.Err()
        }
    }

    return err
}
```

控制流逐步拆解。 / Step-by-step walkthrough of the control flow.

1. 尝试循环 `for attempt := 0; attempt <= opts.maxRetries; attempt++` 把"再试一次"变成一个有上界的循环；缺了它循环无界，一个持续故障的下游会让调用方永远卡住。 / The attempt loop turns "try again" into a loop with an upper bound; without it the loop is unbounded and a persistently broken downstream would hang the caller forever.
2. 上下文取消检查 `if ctx.Err() != nil` 在每轮开头确认这次任务是否还算数；缺了它，用户已关掉页面、上游已超时，重试仍在烧下游容量。 / The context cancellation check confirms at the top of each round whether the task still counts; without it, retries keep burning downstream capacity after the user has closed the page or the upstream has timed out.
3. `unwrapNoRetryErr(err)` 把库内部标记为"永久不可重试"的错误拆开拿到原始错误，并用 `err != nil && err == err1` 判断它是否被包装过；缺了它，像 400 参数错误、证书错误这类重试一万次也不会变的失败会被反复重试。注意这一层保护只在<font color=OrangeRed>没有配置任何 `retryConditions`</font> 时才真正生效，原因见下一条。 / unwrapNoRetryErr unwraps an error the library marked as permanently non-retryable and the comparison `err != nil && err == err1` reveals whether wrapping was applied; without it, failures that never change, such as a 400 argument error or a certificate error, would be retried endlessly. This protection only takes real effect when <font color=OrangeRed>no `retryConditions` is configured</font>, for the reason given in the next item.
4. `retryConditions` 钩子把"什么算失败"的判断权交给调用方，因为库无法知道业务语义；缺了它，HTTP 200 但响应体写着 `"code": 503` 的情况无法被识别为需要重试。 / The retryConditions hook hands the definition of failure to the caller, because the library cannot know application semantics; without it, a response that is HTTP 200 yet carries `"code": 503` in the body could not be recognized as retryable.
    - **易错点：这个循环是赋值而不是"或" A trap: the loop assigns rather than ORs.** 循环体写的是 `needsRetry = condition(resp, err1)` 而不是 `needsRetry = needsRetry || condition(...)`，所以只要配置了任意一个条件函数，上一步由 `unwrapNoRetryErr` 得出的"不可重试"结论就被<font color=OrangeRed>直接丢弃</font>；条件函数返回 `true` 会让库明确标记为不可重试的错误照样被重试，返回 `false` 也会把真实的传输层错误压制成不重试。也就是说条件函数拥有<font color=OrangeRed>最终裁决权</font>，必须自己处理好那些永久性失败的分支。这也正是下面的 Demo 明明有库内部的标记，却仍然会重试 400、401、404 的原因。 / The loop body is `needsRetry = condition(resp, err1)` rather than `needsRetry = needsRetry || condition(...)`, so as soon as any condition function is configured, the non-retryable verdict computed a moment earlier by unwrapNoRetryErr is <font color=OrangeRed>discarded outright</font>; a condition returning `true` will retry an error the library explicitly marked as non-retryable, and a condition returning `false` will suppress retries even for a genuine transport error. The condition function therefore holds <font color=OrangeRed>final authority</font> and must handle the permanently failing branches itself. This is also exactly why the demo below still retries 400, 401 and 404 despite the library's internal marker.
5. `sleepDuration(...)` 根据本轮 attempt、基础等待与最大等待算出这次睡多久，内含指数增长与抖动；缺了它，固定间隔会让所有失败的调用方同步敲门，把恢复中的服务再打趴一次。 / sleepDuration derives this round's wait from the attempt number, the base wait and the maximum wait, including exponential growth and jitter; without it, a fixed interval would make every failing caller knock in lockstep and flatten a recovering service again.
6. `select` 在 `time.After(waitTime)` 与 `ctx.Done()` 之间二选一，等待期间仍可被取消；若只写 `time.Sleep(waitTime)`，一个已被取消的请求还要死等完整的睡眠时间才退出。 / The select chooses between time.After(waitTime) and ctx.Done, so the wait itself stays cancellable; a plain `time.Sleep(waitTime)` would force an already-cancelled request to sit through the full sleep before exiting.

**次数的坑 The off-by-one trap.** 循环条件是 `attempt <= opts.maxRetries`，所以配置 `Retries(3)` 时实际发起 <font color=OrangeRed>4 次调用</font>：1 次首发加 3 次重试；接手任何重试库，第一件事都是读文档确认这个数字是"总次数"还是"额外次数"，并用一次故障演练数一下真实的请求条数。 / The loop condition is `attempt <= opts.maxRetries`, so configuring `Retries(3)` produces four calls in total, one initial call plus three retries; when adopting any retry library, the first step is to confirm from the documentation whether the number means total attempts or extra attempts, then count the real number of requests in a single fault drill.

| 库的语义 Library semantics | 配置 3 意味着 Configuring 3 means | 常见误解 Common misreading |
| --- | --- | --- |
| maxRetries 型（go-resty） | 总共 4 次调用 / four calls in total | 以为只有 3 次，容量规划少算三分之一 / assumed to be three calls, under-counting load by a third |
| maxAttempts 型（如 Resilience4j 的 `maxAttempts`） | 总共 3 次调用 / three calls in total | 以为还会额外重试 3 次 / assumed to add three retries on top |

### Demo 实战调用

> **大白话:** 这段是"点菜单"，前面两段是"厨房怎么做"；调用方只填三个旋钮——重试几次、每次等多久、什么算失败。

看具体 HTTP Client （有做过简单封装）的请求: / Here is a call through a concrete HTTP client that has been lightly wrapped:

```go
func getInfo() {
  request := client.DefaultClient().NewRestyRequest(
    ctx, "", client.RequestOptions{
      MaxTries:      3,
      RetryWaitTime: 500 * time.Millisecond,
      RetryConditionFunc: func(response *resty.Response) (b bool, err error) {
        if !response.IsSuccess() { return true, nil }
        return
      },
    }).SetAuthToken(args.Token)

    // 然后 request.Get(url) 进入到 Backoff() 流程，
    // 此时重试的边界条件是： !response.IsSuccess(), 直到请求成功。
    // EN: request.Get(url) then enters the Backoff() flow, where the retry
    // EN: predicate is !response.IsSuccess(), so retries continue until success
    resp, err := request.Get(url)

    if err != nil {
        logger.Error(ctx, err)
    return
    }

    body := resp.Body()
    if resp.StatusCode() != 200 {
    logger.Error(
      ctx, fmt.Sprintf("Request keycloak access token failed, messages:%s, body:%s","message", resp.Status(),string(body))),
        )
    return
    }
  ...
}
```

- `RetryConditionFunc` 返回 `true` 表示"这次要重试"；这里的条件是 `!response.IsSuccess()`，即任何非 2xx 都重试，包含 400、401、404，而重试这些是没有意义的，更安全的条件应只覆盖 408、429、500、502、503、504 与网络层错误，并且把 401 也重试还可能因凭据错误触发下游的账户锁定。 / Returning `true` from RetryConditionFunc means this round should be retried; the predicate here is `!response.IsSuccess()`, so every non-2xx is retried, including 400, 401 and 404, which is pointless, whereas a safer predicate covers only 408, 429, 500, 502, 503, 504 and transport-level errors, and retrying 401 can additionally trigger account lockout downstream because of bad credentials.
- 上面这段原文除了重试条件过宽，`logger.Error` 那一处还有<font color=OrangeRed>三个无法通过编译</font>的问题：`fmt.Sprintf(...)` 之后多写了一个右括号，导致括号不配对；紧接着还有一个多余的尾逗号；格式串里只有两个 `%s` 占位符，却传入了 `"message"`、`resp.Status()`、`string(body)` 三个参数，多出来的参数会以 `%!(EXTRA ...)` 形式出现在日志里。 / Beyond the over-broad retry predicate, the `logger.Error` call above has <font color=OrangeRed>three problems that stop it from compiling</font>: an extra closing parenthesis after `fmt.Sprintf(...)` leaves the parentheses unbalanced; a stray trailing comma follows it; and the format string carries only two `%s` verbs while three arguments are passed, namely `"message"`, `resp.Status()` and `string(body)`, so the surplus argument would surface in the log as `%!(EXTRA ...)`.
- `response` 参数被直接解引用调用 `response.IsSuccess()`，一旦是连接被拒、DNS 失败这类没有响应的情况，`response` 为 `nil`，这里会直接 panic。 / The `response` parameter is dereferenced straight away by calling `response.IsSuccess()`, so when there is no response at all, such as a refused connection or a DNS failure, `response` is `nil` and this line panics.

**修正版 Corrected version** — 原 Demo 的重试条件过宽，会重试永久性的 4xx，日志调用还存在编译错误；下面保持调用方式不变，收窄条件、补齐真实签名并修好日志语句。 / The original demo's retry predicate is too broad and retries permanent 4xx errors, and its logging call does not compile; the version below keeps the same calling style while narrowing the predicate, restoring the real signature and repairing the log statement.

```go
// 只对"等一会儿可能就好了"的状态码重试
// EN: retry only on status codes that may succeed after a wait
func isTransient(code int) bool {
    // 504 与读超时只在操作幂等时才重试，因为请求可能已经被处理过 / retry 504 and read timeouts only when the operation is idempotent, because the request may already have been processed
    switch code {
    case 408, 429, 500, 502, 503, 504:
        return true
    }
    return false
}

// 真实的 resty.RetryConditionFunc 签名是 func(*resty.Response, error) (bool, error)
// EN: the real resty.RetryConditionFunc signature is func(*resty.Response, error) (bool, error)
// 由于 Backoff 是赋值而非取或，这个函数的返回值就是最终裁决，
// 所以永久性失败必须在这里显式返回 false
// EN: because Backoff assigns instead of OR-ing, this return value is the final verdict,
// EN: so permanent failures must be answered with false right here
RetryConditionFunc: func(response *resty.Response, err error) (bool, error) {
    if err != nil { // 传输层失败：连接被拒、超时、DNS 解析失败
        // EN: transport failure: refused connection, timeout, DNS resolution failure
        return true, nil
    }
    if response == nil {
        return false, nil
    }
    return isTransient(response.StatusCode()), nil
},
```

```go
// 修好原 Demo 中的日志调用：括号配对、去掉尾逗号、占位符与参数数量一致
// EN: the repaired logging call: parentheses balanced, trailing comma removed,
// EN: and the number of verbs matching the number of arguments
logger.Error(ctx, fmt.Sprintf(
    "Request keycloak access token failed, status:%s, body:%s",
    resp.Status(), string(body),
))
```

---

### 一些其他重试机制的实现 A Few Other Retry Implementations

> **大白话:** 下面两段是"手写版"重试，像自己拿水管和胶带修水龙头——能用，但少了几个阀门，得清楚它们漏在哪。 / The two snippets below are hand-rolled retries, comparable to fixing a tap with a length of pipe and tape; they work, but several valves are missing and it pays to know where they leak.

可以看出其实 go-resty 的 重试策略不是很简单， 这是一个完善，可定制化， 充分考虑 HTTP 请求场景下的一个机制， 它的业务属性相对比较重。 / As can be seen, go-resty's retry strategy is not simple; it is a complete, customizable mechanism designed with the realities of HTTP requests in mind, and it carries a fair amount of application-specific behaviour.

**格式修正说明 Formatting fix note:** 原文中"实现二"的代码块以四个反引号开始、三个反引号结束，导致其后的所有 Markdown 都被吞进代码块无法渲染；本节改成正常的三反引号 `go` 围栏，代码内容一字未改。 / In the original, the "实现二" block opened with four backticks and closed with three, which swallowed all following Markdown into the code block; this section emits it as a normal three-backtick `go` fence, with the code content unchanged.

实现一 / Implementation one

每次重试等待随机延长的时间， 直到 f() 执行完成 或不再重试。 / Each retry waits a randomly lengthening interval, until f() completes or signals that no further retry is warranted.

```go
// retry retries ephemeral errors from f up to an arbitrary timeout
func retry(f func() (err error, mayRetry bool)) error {
    var (
        bestErr     error
        lowestErrno syscall.Errno
        start       time.Time
        nextSleep   time.Duration = 1 * time.Millisecond
    )

    for {
        err, mayRetry := f()
        if err == nil || !mayRetry {
            return err
        }

        if errno, ok := err.(syscall.Errno); ok && (lowestErrno == 0 || errno < lowestErrno) {
            bestErr = err
            lowestErrno = errno
        } else if bestErr == nil {
            bestErr = err
        }

        if start.IsZero() {
            start = time.Now()
        } else if d := time.Since(start) + nextSleep; d >= arbitraryTimeout {
            break
        }
        time.Sleep(nextSleep)
        nextSleep += time.Duration(rand.Int63n(int64(nextSleep)))
    }

    return bestErr
}
```

关于实现一：`nextSleep += rand.Int63n(nextSleep)` 是一种真正的去相关抖动，期望值每轮约乘 1.5 倍且无上界；它没有最大睡眠上限，只靠 `arbitraryTimeout` 总时限兜底，这是个隐患，因为某一轮可能一口气睡掉剩余的全部预算。 / On implementation one: `nextSleep += rand.Int63n(nextSleep)` is genuine decorrelated-style jitter whose expected value grows by roughly 1.5x per round with no ceiling; there is no maximum sleep cap, only the overall `arbitraryTimeout` as a backstop, which is a hazard because a single round can consume the entire remaining budget in one sleep.

实现二 / Implementation two

对函数重试 attempts 次，每次等待 sleep 时间， 直到 f() 执行完成。 / Retries the function up to `attempts` times, waiting `sleep` between rounds, until f() completes.

```go
func Retry(attempts int, sleep time.Duration, f func() error) (err error) {
    for i := 0; ; i++ {
        err = f()
        if err == nil {
            return
        }

        if i >= (attempts - 1) {
            break
        }

        time.Sleep(sleep)

    }
    return fmt.Errorf("after %d attempts, last error: %v", attempts, err)
}
```

关于实现二：它没有抖动也没有 context 取消，因此只适合短小、非用户直面的后台工作；它的最终错误信息 `after %d attempts, last error: %v` 只保留最后一个错误，前几轮的失败原因全部丢失，排查时看不到"第一次为什么失败"。三种实现的取舍对照如下。 / On implementation two: it has neither jitter nor context cancellation, so it suits only short, non-user-facing work; its final message `after %d attempts, last error: %v` keeps only the last error, discarding every earlier failure reason, which hides why the first attempt failed during investigation. The three implementations compare as follows.

| 能力 Capability | go-resty Backoff | 实现一 Impl. 1 | 实现二 Impl. 2 |
| --- | --- | --- | --- |
| 次数上限 Attempt cap | 有 / yes | 靠总时限 / via total deadline | 有 / yes |
| 指数增长 Exponential growth | 有 / yes | 有 / yes | 无，固定间隔 / no, fixed interval |
| 抖动 Jitter | 有 / yes | 有 / yes | 无 / no |
| 睡眠上限 Max sleep cap | 有 `maxWaitTime` / yes | 无 / no | 不适用 / not applicable |
| 取消 Cancellation | 有 context / yes | 无 / no | 无 / no |
| 自定义重试条件 Custom predicate | 有 / yes | 有 `mayRetry` / yes | 无 / no |
| 保留全部错误 Keeps all errors | 否 / no | 保留最有价值的一个 / keeps the most informative one | 否，仅最后一个 / no, last only |

### 上手清单 A Practical Checklist

> **大白话:** 加重试和熔断之前先过一遍这十个问题，像出门前检查钥匙、钱包、门锁；漏一项，事故往往就从那一项来。

1. <font color=OrangeRed>幂等性 Idempotency</font>：这个操作重复执行会不会产生第二笔订单、第二封邮件？不幂等就先加幂等键，再谈重试。 / Would repeating this operation create a second order or a second email? If it is not idempotent, add an idempotency key before considering retry.
2. 可重试错误：明确写下白名单，通常是连接失败、超时、408、429、500、502、503、504；4xx 参数错误一律不重试（其中 504 与读超时只在操作幂等时才重试，因为请求可能已经被处理过）。 / Retryable errors: write down an explicit allowlist, typically connection failure, timeout, 408, 429, 500, 502, 503 and 504; 4xx argument errors are never retried (within that list, 504 and read timeouts are retried only when the operation is idempotent, because the request may already have been processed).
3. 单次尝试超时：每一次调用都必须有自己的超时，否则一个挂死的连接会吃掉全部重试预算。 / Per-attempt timeout: every single call needs its own timeout, otherwise one hung connection consumes the whole retry budget.
4. 总截止时间：为整个操作设一个 deadline，并随请求向下游传递，让重试在预算内停止。 / Total deadline: set one deadline for the whole operation and propagate it downstream so retries stop inside the budget.
5. 尝试次数：确认配置的数字是"总次数"还是"额外次数"，多数场景 3 次总调用已经够。 / Attempt count: confirm whether the configured number means total or extra attempts; three total calls is enough for most cases.
6. 抖动策略：至少要有抖动，优先 full jitter 或去相关抖动，并设一个最大睡眠上限。 / Jitter policy: jitter is mandatory; prefer full jitter or decorrelated jitter, and set a maximum sleep cap.
7. 前置熔断：高扇出或强依赖的调用点前面放熔断器，让持续故障时快速失败而不是排队重试。 / Breaker in front: place a circuit breaker ahead of high-fan-out or hard-dependency call sites so persistent faults fail fast instead of queueing retries.
8. 降级方案：熔断打开时返回什么——缓存副本、默认值、空列表，还是明确的错误？必须提前决定。 / Fallback: decide in advance what an open breaker returns, whether a cached copy, a default value, an empty list or an explicit error.
9. 日志内容：记录每一次尝试的序号、错误、实际等待时长和最终结果，不要只记最后一条错误。 / Logging: record each attempt's index, error, actual wait and final outcome, not only the last error.
10. 告警条件：对重试率、熔断开启次数和总耗时 P99 设阈值告警，重试量突增通常是故障的最早信号。 / Alerting: set thresholds on retry rate, breaker-open count and end-to-end P99 latency, since a jump in retry volume is usually the earliest signal of a fault.
