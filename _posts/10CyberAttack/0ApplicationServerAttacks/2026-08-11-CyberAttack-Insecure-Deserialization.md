---
title: "Meow's CyberAttack - Application/Server Attacks - Insecure Deserialization (CWE-502) / 不安全反序列化"
date: 2026-08-11 11:11:11 -0400
categories: [10CyberAttack, Deserialization]
tags: [CyberAttack, deserialization, CWE-502, OWASP, RCE, gadget-chain, pickle, Jackson, ysoserial, java-serialization]
math: false
toc: true
image:
---

# Insecure Deserialization 不安全反序列化

- [Insecure Deserialization 不安全反序列化](#insecure-deserialization-不安全反序列化)
  - [Overview 概述](#overview-概述)
  - [Mental Model Flat-Pack Furniture Analogy 心智模型 组装家具类比](#mental-model-flat-pack-furniture-analogy-心智模型-组装家具类比)
    - [The Basic Picture 基本场景](#the-basic-picture-基本场景)
    - [Where the Danger Comes From 危险来源](#where-the-danger-comes-from-危险来源)
    - [Mapping Terminology onto the Analogy](#mapping-terminology-onto-the-analogy)
  - [Serialization Basics 序列化基础](#serialization-basics-序列化基础)
    - [Common Formats and Magic Bytes 常见格式与特征字节](#common-formats-and-magic-bytes-常见格式与特征字节)
    - [Native Formats vs Data Only Formats 原生格式与纯数据格式](#native-formats-vs-data-only-formats-原生格式与纯数据格式)
  - [Why Deserialization Becomes Code Execution 为什么反序列化会变成代码执行](#why-deserialization-becomes-code-execution-为什么反序列化会变成代码执行)
    - [The Core Flaw 核心缺陷](#the-core-flaw-核心缺陷)
    - [Lifecycle Methods 生命周期方法](#lifecycle-methods-生命周期方法)
  - [Gadget Chain](#gadget-chain)
  - [Java Ecosystem Java 生态](#java-ecosystem-java-生态)
    - [Native Serialization 原生序列化](#native-serialization-原生序列化)
    - [ysoserial and Gadget Libraries ysoserial 与小工具库](#ysoserial-and-gadget-libraries-ysoserial-与小工具库)
    - [Jackson and Polymorphic Typing Jackson 与多态类型](#jackson-and-polymorphic-typing-jackson-与多态类型)
    - [Other Java Libraries 其他 Java 库](#other-java-libraries-其他-java-库)
  - [PHP Ecosystem PHP 生态](#php-ecosystem-php-生态)
    - [unserialize and Magic Methods unserialize 与魔术方法](#unserialize-and-magic-methods-unserialize-与魔术方法)
    - [POP Chains POP 链](#pop-chains-pop-链)
    - [Phar Deserialization Phar 反序列化](#phar-deserialization-phar-反序列化)
  - [Python Ecosystem Python 生态](#python-ecosystem-python-生态)
    - [pickle Code Execution pickle 代码执行](#pickle-code-execution-pickle-代码执行)
    - [Other Unsafe Loaders 其他不安全的加载器](#other-unsafe-loaders-其他不安全的加载器)
  - [Other Ecosystems 其他生态](#other-ecosystems-其他生态)
  - [Detection 检测识别](#detection-检测识别)
    - [Traffic and Log Indicators 流量与日志特征](#traffic-and-log-indicators-流量与日志特征)
    - [Code Review Patterns 代码审计模式](#code-review-patterns-代码审计模式)
  - [Defenses 防御措施](#defenses-防御措施)
    - [Do Not Deserialize Untrusted Data 不要反序列化不可信数据](#do-not-deserialize-untrusted-data-不要反序列化不可信数据)
    - [Allowlist Filtering with JEP 290 使用 JEP 290 白名单过滤](#allowlist-filtering-with-jep-290-使用-jep-290-白名单过滤)
    - [Integrity Protection 完整性保护](#integrity-protection-完整性保护)
    - [Language Specific Hardening 各语言加固要点](#language-specific-hardening-各语言加固要点)
    - [Defense Summary Table 防御汇总表](#defense-summary-table-防御汇总表)
  - [Case Studies in This Knowledge Base 本库中的案例](#case-studies-in-this-knowledge-base-本库中的案例)
  - [Key Takeaways](#key-takeaways)
  - [References](#references)

---

## Overview 概述

<font color=OrangeRed>Insecure deserialization</font>

- 不安全反序列化
- occurs when an application converts `attacker-controlled bytes` back into `in-memory objects` without constraining which types may be instantiated 没有限制允许实例化的类型.
- The vulnerability is not that the attacker injects code into the data stream. It is that the deserializer itself is a general-purpose object factory, and reconstructing an object graph invokes real methods on real classes already present in the application's classpath.
- 危险之处不在于攻击者往数据里塞了代码，而在于<font color=OrangeRed>反序列化器本身就是一个通用的对象工厂</font>：还原对象图的过程会真实调用类路径中已存在的类的方法。攻击者不需要上传代码，只需要用应用自己已有的代码拼出一条执行路径。

Mapped as <font color=OrangeRed>CWE-502: Deserialization of Untrusted Data</font>.

- Tracked by OWASP as A8:2017 Insecure Deserialization, which was folded into <font color=OrangeRed>A08:2021 Software and Data Integrity Failures</font>.
- Typically reached through `MITRE ATTCK T1190 Exploit Public-Facing Application`, leading to `T1059 Command and Scripting Interpreter`.

**Key insight 核心认知:**

- The payload carries no shellcode. It carries a *description of an object graph*.
- 载荷里没有 shellcode，只有一份「对象图的描述」。
- Impact is usually <font color=OrangeRed>pre-authentication remote code execution</font>, because deserialization happens while parsing the request, before any authorization check runs.
- 影响通常是<font color=OrangeRed>未授权的远程代码执行</font>，因为反序列化发生在解析请求阶段，早于任何鉴权逻辑。
- The vulnerable code is often a single line, and the exploitability depends on which libraries happen to be on the classpath.
- 漏洞代码常常只有一行，能否利用取决于类路径里恰好有哪些库。

---

## Mental Model Flat-Pack Furniture Analogy 心智模型 组装家具类比

The formats and CVEs above are easier to hold onto once the mechanism is mapped onto a physical, non-technical scene. This section builds that intuition once, then the rest of the note reuses the same vocabulary.

上面的格式与 CVE 一旦被映射到一个具体的、非技术的场景上，就更容易理解和记住。本节先建立这个直觉，后续章节沿用同一套词汇。

### The Basic Picture 基本场景

> Ordering a cabinet online does not deliver an assembled cabinet. It delivers a flat box containing boards and screws, plus an assembly manual. Following the manual turns the flat parts into a standing, usable cabinet.

| Computing 计算机世界 | Real-world analogy 现实类比 |
| --- | --- |
| Serialization 序列化 | Flattening the cabinet into boards and writing a manual for it 把柜子拆成板材并写一份说明书 |
| Transport 传输 | Shipping the box 把盒子寄出去 |
| Deserialization 反序列化 | Assembling the cabinet by following the manual 照说明书把柜子组起来 |

Systems exchange data the same way:

- one side flattens a live object into a string (JSON, XML, YAML) and sends it;
- the other side receives it and reconstructs a live object.

### Where the Danger Comes From 危险来源

The manual is written by whoever sent the package, not by whoever receives it.

- Suppose a hostile sender's manual looks entirely normal, except that step seven reads "open the gas valve in the kitchen."
- An assembly worker who follows written steps without judgment carries that step out along with the rest, because nothing in the process distinguishes a legitimate assembly instruction from an injected one.
- 假设一份来自恶意寄件人的说明书看起来完全正常，只是第七步写着「去厨房把煤气阀门打开」。一个只会照做、不做判断的装配工人会把这一步和其他步骤一样执行下去 —— 因为整个流程里没有任何环节能区分「合法的组装指令」和「被插入的指令」。

<font color=OrangeRed>Reconstructing the object is not the risky part. Executing instructions authored by an untrusted party during that reconstruction is.</font> The "open the gas valve" step, translated back into computing terms, is <font color=OrangeRed>RCE</font>: arbitrary code execution on infrastructure the attacker does not own.

<font color=OrangeRed>还原对象本身不是风险所在，风险在于还原过程中执行了不可信一方编写的指令。</font>「开煤气阀门」这一步翻译回计算机语言，就是<font color=OrangeRed>RCE</font>：在攻击者并不拥有的基础设施上执行任意代码。

### Mapping Terminology onto the Analogy

- <font color=OrangeRed>Serialization / Deserialization 序列化／反序列化</font>
  flattening a cabinet into a shippable box, and assembling it back from the manual.
  把柜子拆成可寄送的盒子，以及照说明书把它组装回来。

  ```java
  // serialize: live object -> string
  String json = mapper.writeValueAsString(order);
  // deserialize: string -> live object
  Order restored = mapper.readValue(json, Order.class);
  ```

- <font color=OrangeRed>RCE 远程代码执行</font>
  the manual's hidden step gets carried out on real infrastructure.
  说明书里藏的指令在真实基础设施上被执行。

  ```java
  // what the "hidden step" ultimately resolves to once a gadget chain fires
  Runtime.getRuntime().exec("id");   // <-- attacker-influenced, not application code
  ```

- <font color=OrangeRed>Type metadata / discriminator 型别标记／判别字段</font>
  the line on the manual's cover page declaring what it assembles, e.g. "this is a cabinet manual." The receiver does not verify that line; it is simply the sender's claim. This is the analogy for Jackson's `@type` field or a PHP serialized string's class name.
  说明书封面上声明「这是柜子说明书」的那一行字。收件方并不验证这行字，它只是寄件人的一面之词
  对应 Jackson 的 `@type` 字段或 PHP 序列化字符串里的类名。

  ```json
  { "@type": "com.example.dto.Cabinet", "shelves": 3 }
  ```

- <font color=OrangeRed>Polymorphic handling 多态处理</font>
  one shared intake counter accepts manuals for any furniture type, and the cover page self-declares which type it is. Convenient for the receiver, but it also means an attacker's manual is accepted at the same counter, self-declaring whatever type it wants.
  一个共享的收件口可以接收任何家具的说明书，具体是哪一种由封面自行声明。这对接收方很方便，但同样意味着攻击者的说明书也能从这个口进来，自行声明成任何类型。

  ```java
  mapper.enableDefaultTyping();               // "one counter, any furniture type"
  Object thing = mapper.readValue(json, Object.class);
  ```

- <font color=OrangeRed>Concrete type 具体型别</font>
  narrowing that counter so it only ever accepts cabinet manuals. The cover page is not read at all, so there is nothing left for an attacker to spoof.
  把收件口收窄成只接收柜子说明书。封面那行字完全不读，攻击者也就没有可伪造的对象。

  ```java
  Cabinet cabinet = mapper.readValue(json, Cabinet.class);  // "@type" is never consulted
  ```

- <font color=OrangeRed>Closed mapping / allowlist 封闭映射／白名单</font>
  a gatekeeper stands at the still-shared counter holding a list of exactly three approved words (cabinet, table, chair) and rejects anything else. The counter itself is unchanged and the self-declaring mechanism is still switched on; a check has simply been added in front of it.
  在仍然共享的收件口加一位门房，手持一张只写着三个词（柜子、桌子、椅子）的名单，凡不在名单上的一律退回。收件口本身没变，自我声明的机制依然在运转，只是前面多了一道检查。

  ```java
  PolymorphicTypeValidator ptv = BasicPolymorphicTypeValidator.builder()
      .allowIfSubType("com.example.dto.")   // the gatekeeper's list: cabinet, table, chair
      .build();
  ```

- <font color=OrangeRed>Fail closed 失败时关闭</font>
  the gatekeeper's default action on an unrecognized item is to refuse it, not to let it through and hope it turns out fine. The opposite, fail open, lets unrecognized items in by default.
  门房遇到不认识的东西，默认动作是拒收，而不是先放进来再看情况。
  反面是失败时打开，即默认放行未识别的项目。

  ```bash
  -Djdk.serialFilter='com.example.dto.*;!*'   # unlisted classes are rejected, not admitted
  ```

- <font color=OrangeRed>Nested attacker-selected type 嵌套的攻击者可选型别</font>
  the approved list includes "a box" as a valid item, which is entirely legitimate. An attacker then submits a box whose contents are a manual for something else. The outer layer is a legitimate, allowlisted type; the inner layer is whatever the attacker chooses, because the list never inspected what is inside the box. This is why an allowlist has to close every nested field capable of naming its own type, not just the top-level type.
  名单里允许「一个箱子」作为合法项目，这本身完全正当。攻击者随后提交一个箱子，里面装的却是别的东西的说明书。
  外层是合法且在名单上的类型，内层是攻击者任意选择的内容，因为名单从未检查箱子里装了什么。
  这正是为什么白名单必须封住每一个能够自行声明类型的嵌套字段，而不只是最外层的类型。

  ```java
  class Shipment {
      String trackingId;
      Object contents;   // <-- "a box": legitimate at the top level, unchecked inside
  }
  ```

- <font color=OrangeRed>Gadget chain / sink 小工具链／汇点</font>
  even when every item on the gatekeeper's list is an ordinary, harmless furniture part, an attacker can request a specific combination of allowed parts and assemble them into a working catapult. No individual part is disallowed; it is the combination, and the point where it finally does damage, that causes harm.
  即便门房名单上的每一项都是普通、无害的家具零件，攻击者仍可以指定一种特定的合法零件组合，把它们拼装成一台能用的投石机。没有任何一个零件本身被禁止，造成伤害的是这种组合，以及它最终触发伤害的那一点。

  ```java
  // three ordinary, individually harmless methods, chained by an attacker
  class Lookup  { Object get(String key)       { return registry.get(key); } }   // kick-off
  class Wrapper { Object transform(Object o)    { return invoke(o); } }          // chain
  class Sink    { void invoke(Object cmd)       { Runtime.getRuntime().exec((String) cmd); } } // sink
  ```

---

## Serialization Basics 序列化基础

Serialization converts an `in-memory object` into a `byte stream` for **storage or transport**.

- Deserialization reverses it.
- The security properties depend entirely on:
  - how much type information the format carries
  - how much of it the receiver trusts.

### Common Formats and Magic Bytes 常见格式与特征字节

Recognizing a serialized blob on the wire is the first step in both attack and defense. 识别流量中的序列化数据是攻防双方的第一步。

| Format 格式 | Raw prefix 原始前缀 | Base64 prefix | Notes 说明 |
| --- | --- | --- | --- |
| Java native | `AC ED 00 05` | `rO0AB` | `STREAM_MAGIC` 0xACED + version 5 |
| Java HTTP | — | — | `Content-Type: application/x-java-serialized-object` |
| .NET `BinaryFormatter` | `00 01 00 00 00 FF FF FF FF` | `AAEAAAD/////` | Also `LosFormatter`, `ObjectStateFormatter` |
| ASP.NET ViewState | — | `/wEP` | `__VIEWSTATE` parameter |
| PHP `serialize` | `O:8:"ClassName"` | — | `a:` array, `O:` object, `s:` string |
| Python pickle | `80 04` (proto 4) | `gASV` | Proto 0 is printable ASCII |
| Ruby `Marshal` | `04 08` | `BAg` | |
| Node `node-serialize` | — | — | `_$$ND_FUNC$$_` marker |

```python
MAGIC = {
    b"\xac\xed\x00\x05": "Java native serialization",
    b"\x00\x01\x00\x00\x00\xff\xff\xff\xff": ".NET BinaryFormatter",
    b"\x80\x04": "Python pickle (protocol 4)",
}

def sniff(blob: bytes) -> str | None:
    for prefix, name in MAGIC.items():
        if blob.startswith(prefix):
            return name
    return None
```

### Native Formats vs Data Only Formats 原生格式与纯数据格式

This distinction is the single most important design decision. 这一区分是最关键的设计决策。

| | Native / object formats 原生对象格式 | Data-only formats 纯数据格式 |
| --- | --- | --- |
| Examples | Java serialization, PHP `serialize`, pickle, `BinaryFormatter`, `Marshal` | JSON, Protobuf, Avro, Thrift, MessagePack, CSV |
| Carries type info 携带类型信息 | Yes — names the classes to instantiate | No — only scalars, lists, maps |
| Runs code on load 加载时执行代码 | <font color=OrangeRed>Yes, by design</font> | No, unless a layer bolts typing on top |
| Safe on untrusted input | Never 绝不安全 | Safe to *parse*, still must validate values |

<font color=OrangeRed>Critical caveat</font>: a data-only format becomes dangerous the moment a library adds polymorphic type resolution on top of it. JSON is safe; JSON plus "instantiate whatever class the `@type` field names" is not. This is exactly how Jackson and fastjson vulnerabilities arise.

<font color=OrangeRed>重要例外</font>：纯数据格式一旦被库加上多态类型解析就不再安全。

- JSON 本身安全，但「按 `@type` 字段实例化任意类」的 JSON 不安全
- Jackson 与 fastjson 的漏洞正是这样产生的。

```python
# Safe: data-only, bound to a known shape — nothing is instantiated from the bytes
data = json.loads(blob)                 # dict of scalars/lists
cabinet = Cabinet(shelves=data["shelves"])

# Unsafe: a layer that instantiates whatever class the bytes name
data = json.loads(blob)
cls = import_class(data["@type"])       # attacker-controlled class name
obj = cls(**data)                       # <-- arbitrary instantiation
```

> 组装家具类比 Analogy: a data-only format is a fill-in-the-blank order form; a native format is the full assembly manual. A library that adds `@type` resolution hands the order form a manual after all.
> 纯数据格式是一张只需填空的订购单；原生格式则是完整的组装说明书。一旦库为其加上 `@type` 解析，那张订购单也就等于拿到了一份说明书。

---

## Why Deserialization Becomes Code Execution 为什么反序列化会变成代码执行

### The Core Flaw 核心缺陷

A deserializer performs three steps, and step two is where trust is lost.

反序列化器执行三个步骤，信任在第二步失守。

```text
  attacker-controlled bytes
            |
            v
  1. parse the stream structure          <- attacker controls layout
            |
            v
  2. resolve and instantiate classes     <- attacker controls WHICH classes
            |                                (no allowlist = arbitrary types)
            v
  3. populate fields, invoke lifecycle   <- application code now RUNS
            |                                on attacker-chosen objects
            v
     object graph handed to the app
      (validation happens HERE - too late)
```

Application-level validation runs at step three's end. By then the damage is done, because reconstructing the graph already executed code. 应用层校验发生在第三步之后，但那时代码已经跑完了 —— 还原对象图的过程本身就是执行。

```python
# The same three steps a deserializer performs, made explicit
raw = read_bytes(request)               # 1. parse structure   (attacker controls layout)
cls = resolve_class(raw.type_name)      # 2. resolve class     (attacker controls WHICH class)
obj = cls.__new__(cls)
obj.__setstate__(raw.fields)            # 3. populate + lifecycle hooks run HERE
validate(obj)                            # <-- too late: object already reconstructed
```

> 组装家具类比 Analogy: step 1 is reading the manual's page layout, step 2 is picking which furniture part the cover page names, step 3 is physically assembling it and running whatever built-in setup step the manual specifies — including "open the gas valve."
> 类比：第一步是读懂说明书的页面排版，第二步是按封面声明去挑选家具零件，第三步是实际组装并执行说明书里指定的内建设置步骤 —— 包括「打开煤气阀」那一步。

### Lifecycle Methods 生命周期方法

Deserializers call methods automatically so that objects can restore invariants. Those callbacks are the attacker's entry points.

反序列化器会自动调用一些方法，让对象恢复自身不变量。这些回调就是攻击者的入口。

| Language | Automatically invoked 自动调用 |
| --- | --- |
| Java | `readObject`, `readObjectNoData`, `readResolve`, `validateObject`, `finalize`; plus `hashCode` / `equals` / `compareTo` when a `HashMap`, `HashSet`, or `TreeMap` rebuilds its internal layout |
| PHP | `__wakeup`, `__unserialize` (7.4+), `__destruct`, `__toString`, `__get`, `__set`, `__call`, `__invoke` |
| Python | whatever callable `__reduce__` / `__reduce_ex__` designates, plus `__setstate__` |
| .NET | `OnDeserialized` / `OnDeserializing` callbacks, `ISerializable` constructor, setters during type resolution |

`HashMap.readObject` is the classic Java kick-off: rebuilding the table requires hashing every key, so `hashCode()` is called on attacker-chosen objects. Java 中最经典的起点是 `HashMap.readObject`：重建哈希表必须对每个 key 求哈希，于是 `hashCode()` 被调用在攻击者指定的对象上。

```java
class Session implements Serializable {
    private void readObject(ObjectInputStream in) throws IOException, ClassNotFoundException {
        in.defaultReadObject();   // <-- called automatically; attacker-chosen state is already set
    }
}
```

```php
class LogWriter {
    public function __wakeup() {
        // called automatically right after unserialize() rebuilds this object
        $this->open($this->file);
    }
}
```

> 组装家具类比 Analogy: lifecycle methods are the manual's final setup checklist that the assembler runs automatically after the last screw — no one asked for it to run, it simply always does.
> 类比：生命周期方法就是说明书最后一步「自动执行的收尾检查清单」—— 没有人特意要求它运行，装配工人组装完最后一颗螺丝后就会自动执行。

---

## Gadget Chain

A <font color=OrangeRed>gadget</font> is a method in a legitimate library that does something useful to an attacker when invoked with controlled state.

A <font color=OrangeRed>gadget chain</font> stitches gadgets together so that an automatic lifecycle call cascades into a dangerous sink.

<font color=OrangeRed>小工具（gadget）</font>是合法库中的一个方法，在状态可控时会做出对攻击者有用的行为。<font color=OrangeRed>小工具链</font>把多个小工具串起来，使一次自动的生命周期调用最终级联到危险的汇聚点。

```text
  kick-off gadget          chain gadgets              sink gadget
  (auto-invoked)     ->    (pass control along)  ->   (does the damage)

  HashMap.readObject       LazyMap.get                Runtime.exec
  __destruct               ChainedTransformer         eval / include
  __reduce__               InvokerTransformer         defineClass
                           reflection wrappers        JDBC / JNDI lookup
                                                      file write
```

Three properties 推论 follow from this model, and they explain most of the confusion around this bug class:

- <font color=OrangeRed>The vulnerable application contains no malicious code.</font> Every gadget is ordinary library code doing what it was written to do. 应用里没有任何恶意代码，每个小工具都是库的正常功能。
- <font color=OrangeRed>Exploitability is a property of the dependency set, not of the sink alone.</font> The same one-line flaw is unexploitable with a bare classpath and trivially exploitable once a gadget-bearing library is added. 可利用性取决于依赖集合，而非单看汇聚点。同一行代码，类路径干净时打不动，加入某个含小工具的库后就一击必中。
- <font color=OrangeRed>Blacklisting gadgets is a losing race.</font> Denylists enumerate known chains; researchers keep finding new ones in new libraries. 黑名单只能枚举已知链条，研究者会不断在新库中发现新链条，因此黑名单必然滞后。

> 组装家具类比 Analogy: every method above is an ordinary library method doing its job; see [Mapping Terminology onto the Analogy](#mapping-terminology-onto-the-analogy) — the danger is the combination, like harmless furniture parts assembled into a catapult.
> 类比：上面每一个方法都是库中一个正常在履行职责的方法；参见前文「组装家具类比」的术语对照 —— 危险来自组合方式，就像无害的家具零件被拼装成一台投石机。

---

## Java Ecosystem Java 生态

### Native Serialization 原生序列化

The sink is `ObjectInputStream.readObject()` reading bytes the attacker influences.

```java
// Vulnerable: the stream decides which classes get instantiated.
ObjectInputStream ois = new ObjectInputStream(request.getInputStream());
Object obj = ois.readObject();   // <-- gadget chain fires here
```

> 组装家具类比 Analogy: `readObject()` is the shared intake counter that accepts a manual for any furniture type — see [Polymorphic handling](#mapping-terminology-onto-the-analogy) above.
> 类比：`readObject()` 就是那个能接收任何家具说明书的共享收件口 —— 对应前文的「多态处理」。

Common places serialized Java objects cross a trust boundary: RMI and JMX endpoints, JNDI, HTTP session persistence and session replication, message queues, caches such as Memcached or Redis, cookies, hidden form fields, and proprietary protocols such as WebLogic T3.

Java 序列化数据穿越信任边界的常见位置：RMI 与 JMX 端点、JNDI、HTTP 会话持久化与会话复制、消息队列、Memcached / Redis 之类的缓存、Cookie、隐藏表单字段，以及 WebLogic T3 等私有协议。

### ysoserial and Gadget Libraries ysoserial 与小工具库

`ysoserial` (Chris Frohoff) generates ready-made payloads for known chains. It turns a research problem into a one-liner, which is why an unfiltered `readObject` should be treated as immediately exploitable.

```bash
# Generate a payload using the commons-collections gadget chain.
java -jar ysoserial.jar CommonsCollections2 "touch /tmp/pwned" > payload.ser
```

| Gadget source 小工具来源 | Mechanism 机制 |
| --- | --- |
| `commons-collections` | `InvokerTransformer` + `ChainedTransformer` reach reflective `Runtime.exec` |
| `commons-beanutils` | Property-getter invocation via comparators |
| `TemplatesImpl` (JDK/Xalan) | `newTransformer()` calls `defineClass` on attacker bytecode |
| `Spring`, `Groovy`, `ROME`, `C3P0`, `Hibernate` | Assorted reflection and JNDI-reaching chains |

Notable CVEs: <font color=OrangeRed>CVE-2015-4852</font> (WebLogic T3), <font color=OrangeRed>CVE-2017-9805</font> (Struts2 REST plugin via XStream), <font color=OrangeRed>CVE-2017-10271</font> (WebLogic `wls-wsat` XMLDecoder), <font color=OrangeRed>CVE-2019-2725</font> (WebLogic), <font color=OrangeRed>CVE-2020-9484</font> (Tomcat session persistence).

### Jackson and Polymorphic Typing Jackson 与多态类型

Jackson parses JSON, so it looks safe. It becomes unsafe when configured to record and honour concrete types.

Jackson 解析的是 JSON，看起来很安全。一旦被配置为记录并信任具体类型，它就不安全了。

```java
// Dangerous: the JSON payload now names the class to instantiate.
ObjectMapper mapper = new ObjectMapper();
mapper.enableDefaultTyping();   // deprecated; activateDefaultTyping is no better without a validator
```

Preconditions for exploitation: polymorphic typing is enabled, the declared field type is broad enough (`Object`, `Serializable`, an interface, or an abstract class), a gadget class sits on the classpath, and the attacker controls the JSON body. 利用条件：启用了多态类型、声明字段类型足够宽（`Object`、`Serializable`、接口或抽象类）、类路径中存在小工具类、且攻击者可控 JSON 内容。

Jackson ships a denylist of known dangerous types, which lags behind published research by design. Use `activateDefaultTyping` with a strict `PolymorphicTypeValidator`, or avoid polymorphic typing and bind to explicit DTOs. Jackson 自带已知危险类型的黑名单，其本质上滞后于公开研究。应使用带严格 `PolymorphicTypeValidator` 的 `activateDefaultTyping`，或干脆放弃多态类型、绑定到明确的 DTO。

> 组装家具类比 Analogy: `enableDefaultTyping()` is the cover page being read and trusted; a `PolymorphicTypeValidator` is the gatekeeper's list — see [Type metadata](#mapping-terminology-onto-the-analogy) and [Closed mapping / allowlist](#mapping-terminology-onto-the-analogy) above.
> 类比：`enableDefaultTyping()` 相当于封面那行字被读取并被信任；`PolymorphicTypeValidator` 相当于门房手里的名单 —— 对应前文的「型别标记」与「封闭映射／白名单」。

Notable CVEs: <font color=OrangeRed>CVE-2017-7525</font>, <font color=OrangeRed>CVE-2019-12384</font>.

### Other Java Libraries 其他 Java 库

| Library | Trigger 触发点 |
| --- | --- |
| `fastjson` | `@type` AutoType field names an arbitrary class |
| `XStream` | XML directly encodes types; many chains, e.g. CVE-2021-39144 |
| `SnakeYAML` | `yaml.load` honours tags such as `!!javax.script.ScriptEngineManager` |
| `Kryo`, `Hessian`, `Castor`, `JYaml` | Registration-optional or type-carrying modes |

```java
// fastjson: @type in the JSON body directly names the class to instantiate
String json = "{\"@type\":\"org.apache.commons.collections.functors.InvokerTransformer\"}";
JSON.parseObject(json, Object.class);
```

```java
// SnakeYAML: a YAML tag can construct arbitrary objects, including scripting engines
Yaml yaml = new Yaml();
yaml.load("!!javax.script.ScriptEngineManager [!!java.net.URLClassLoader [[]]]");
```

---

## PHP Ecosystem PHP 生态

### unserialize and Magic Methods unserialize 与魔术方法

`unserialize()` on user input reconstructs objects and then triggers magic methods, most reliably `__destruct()` at script shutdown.

对用户输入调用 `unserialize()` 会重建对象，随后触发魔术方法，其中最可靠的是脚本结束时的 `__destruct()`。

```php
<?php
// Vulnerable: the serialized string names the class and sets its properties.
$data = unserialize($_COOKIE['prefs']);   // <-- __wakeup / __destruct fire
```

```text
O:8:"LogWriter":2:{s:4:"file";s:14:"/var/www/x.php";s:4:"data";s:20:"<?php system($_GET);"}
 |  |     |       |  |                                    ^
 |  |     |       |  +- property name                      +- attacker-controlled value
 |  |     |       +- property count
 |  |     +- class name to instantiate
 |  +- class name length
 +- object
```

`__wakeup()` could be used to reject a bad state, but <font color=OrangeRed>CVE-2016-7124</font> showed that declaring a property count larger than the actual number of properties skips `__wakeup()` entirely on affected versions.

### POP Chains POP 链

<font color=OrangeRed>Property Oriented Programming</font>  

- the PHP equivalent of a Java gadget chain
- the attacker sets object properties so that one magic method calls into another object's method, walking toward a sink such as `system`, `eval`, `include`, or a file write.
- 攻击者设置对象属性，使一个魔术方法调用到另一个对象的方法，逐步走向 `system`、`eval`、`include` 或文件写入等汇聚点。

`phpggc` is the PHP counterpart to `ysoserial`, carrying prebuilt chains for Laravel, Symfony, Monolog, WordPress, Drupal, and others.

```php
class FileLogger {
    public $file;
    public function __destruct() { $this->write("closed"); }              // kick-off
    public function write($msg) { file_put_contents($this->file, $msg); } // sink: arbitrary file write
}
// attacker sets $file to a path they control before the object is unserialized
```

### Phar Deserialization Phar 反序列化

The subtle one. A `.phar` archive stores serialized metadata, and the `phar://` stream wrapper deserializes that metadata during <font color=OrangeRed>any</font> file operation on the path — no call to `unserialize()` is needed at all.

最隐蔽的一种。`.phar` 归档中存有序列化的元数据，而 `phar://` 流包装器会在对该路径执行<font color=OrangeRed>任何</font>文件操作时反序列化这些元数据 —— 完全不需要调用 `unserialize()`。

```php
<?php
// Every one of these can trigger deserialization if the path is attacker-controlled.
file_exists("phar://uploaded.jpg/x");
md5_file($path);
filesize($path);
getimagesize($path);
```

This converts a benign-looking file-existence check plus an upload primitive into remote code execution. It also means a polyglot upload with an image extension can carry a payload. 这把一个看似无害的文件存在性检查加上任意上传能力，组合成了远程代码执行；带图片后缀的多格式文件同样可以携带载荷。

---

## Python Ecosystem Python 生态

### pickle Code Execution pickle 代码执行

`pickle` is not a data format with a security weakness. It is a virtual machine whose instruction set includes "call this callable". Arbitrary code execution is documented behaviour, not a bug.

`pickle` 不是「有安全弱点的数据格式」，而是一台指令集中包含「调用某个可调用对象」的虚拟机。任意代码执行是它被记录在案的既定行为，不是缺陷。

```python
import os
import pickle

class Exploit:
    def __reduce__(self):
        # pickle honours this on load: callable + args
        return (os.system, ("echo pwned",))

payload = pickle.dumps(Exploit())
pickle.loads(payload)   # executes: echo pwned
```

There is no safe subset, no sandbox flag, and no validation that helps. The only control is refusing to unpickle untrusted bytes.

不存在安全子集、沙箱开关或有效的校验手段。唯一的控制措施就是拒绝反序列化不可信字节。

### Other Unsafe Loaders 其他不安全的加载器

Many Python APIs use pickle internally or otherwise execute on load, which surprises people who thought they were only loading data.

许多 Python API 内部使用 pickle 或在加载时执行代码，这常常出乎「我只是在读数据」的预期。

| API | Note 说明 |
| --- | --- |
| `yaml.load` without `SafeLoader` | Tags can construct arbitrary objects; use `yaml.safe_load` |
| `numpy.load(allow_pickle=True)` | Defaults to `False` for this reason — keep it that way |
| `pandas.read_pickle` | Pickle under the hood |
| `joblib.load` | Common in ML pipelines and model registries |
| `torch.load` | Historically pickle-based; prefer `weights_only=True` |
| `dill`, `cloudpickle` | Broader-than-pickle capabilities |
| `shelve`, `marshal` | Pickle-backed or interpreter-internal formats |

```python
import yaml

yaml.safe_load(blob)                    # safe: only builds plain Python types (dict, list, str, int)
yaml.load(blob, Loader=yaml.Loader)     # unsafe: honours tags that construct arbitrary objects
```

<font color=OrangeRed>Model files are executables.</font> Downloading a `.pkl`, `.pt`, or `.joblib` artifact from an untrusted registry and loading it is equivalent to running an untrusted binary. <font color=OrangeRed>模型文件就是可执行文件</font>：从不可信仓库下载 `.pkl`、`.pt`、`.joblib` 并加载，等同于运行一个不可信的二进制程序。

---

## Other Ecosystems 其他生态

| Runtime | Dangerous sinks 危险汇聚点 | Notes 说明 |
| --- | --- | --- |
| .NET | `BinaryFormatter`, `LosFormatter`, `ObjectStateFormatter`, `NetDataContractSerializer`, `SoapFormatter`, `Newtonsoft.Json` with `TypeNameHandling` | `BinaryFormatter` is obsoleted and removed in .NET 9; tooling is `ysoserial.net`. ViewState without a valid MAC is a classic entry point, as in <font color=OrangeRed>CVE-2020-0688</font> where a static Exchange `machineKey` made payloads universally valid |
| Ruby | `Marshal.load`, unsafe `YAML.load` / `Psych.load` | Universal gadget chains exist for common gem sets |
| Node.js | `node-serialize`, `funcster`, `eval`-based revivers | `node-serialize` executes an IIFE marked `_$$ND_FUNC$$_` |

```csharp
// .NET: BinaryFormatter resolves and instantiates the type named in the stream
var formatter = new BinaryFormatter();
object obj = formatter.Deserialize(stream);
```

```ruby
# Ruby: Marshal.load reconstructs objects and can invoke arbitrary methods via gadgets
obj = Marshal.load(data)
```

```javascript
// Node.js: node-serialize revives functions marked with a special prefix
var obj = serialize.unserialize(data);   // executes _$$ND_FUNC$$_ payloads
```

---

## Detection 检测识别

### Traffic and Log Indicators 流量与日志特征

- Search request bodies, query parameters, cookies, and headers for the magic-byte prefixes in the table above, especially base64 `rO0`, `AAEAAAD/////`, `gASV`, and raw `O:` followed by a digit and a quoted class name.
  在请求体、查询参数、Cookie 与请求头中搜索上文表格中的特征字节前缀，尤其是 base64 的 `rO0`、`AAEAAAD/////`、`gASV`，以及裸的 `O:` 后跟数字与带引号的类名。
- Flag `Content-Type: application/x-java-serialized-object` on any externally reachable endpoint.
  对任何可从外部访问的端点，标记 `Content-Type: application/x-java-serialized-object`。
- Deserialization failures are noisy. Stack traces naming `ObjectInputStream`, `com.fasterxml.jackson.databind`, `InvokerTransformer`, `TemplatesImpl`, `_PyUnpickler`, or `unserialize()` in error logs often indicate probing that has not yet succeeded.
  反序列化失败会产生大量噪声。错误日志中出现 `ObjectInputStream`、`com.fasterxml.jackson.databind`、`InvokerTransformer`、`TemplatesImpl`、`_PyUnpickler` 或 `unserialize()` 的堆栈，往往说明探测正在进行但尚未成功。
- Watch for child-process spawns and outbound DNS or LDAP lookups originating from an application server that has no legitimate reason to make them.
  关注应用服务器上无正当理由的子进程创建与出站 DNS / LDAP 查询。
- The `sniff()` helper under [Common Formats and Magic Bytes](#common-formats-and-magic-bytes-常见格式与特征字节) above can be run directly against captured request bodies, cookies, and header values.
  上文「常见格式与特征字节」小节里的 `sniff()` 函数，可直接用于扫描抓取到的请求体、Cookie 与请求头。

### Code Review Patterns 代码审计模式

```bash
# Java
grep -rn "readObject\|ObjectInputStream\|enableDefaultTyping\|activateDefaultTyping\|readUnshared" .
# PHP
grep -rn "unserialize(\|phar://" .
# Python
grep -rn "pickle.load\|pickle.loads\|yaml.load(\|allow_pickle=True\|read_pickle\|joblib.load\|torch.load" .
# .NET
grep -rn "BinaryFormatter\|LosFormatter\|ObjectStateFormatter\|TypeNameHandling" .
```

For each hit, the question is not "is the input validated" but <font color=OrangeRed>"can an untrusted party influence these bytes at all"</font>. If yes, treat it as exploitable until a type allowlist or an integrity check is proven to sit in front of it.

对每处命中，要问的不是「输入是否经过校验」，而是<font color=OrangeRed>「不可信方能否影响这些字节」</font>。若能，则在证明其前方存在类型白名单或完整性校验之前，一律视为可利用。

Dependency scanning matters as much as code review here: an inventory of gadget-bearing libraries determines whether a sink is reachable in practice. 依赖扫描与代码审计同等重要：含小工具的库清单决定了汇聚点在实际中是否可达。

---

## Defenses 防御措施

### Do Not Deserialize Untrusted Data 不要反序列化不可信数据

The only complete fix. Replace `native object serialization` at trust boundaries with a <font color=OrangeRed>data-only format plus an explicit schema</font>: `JSON, Protobuf, or Avro` bound to concrete DTO types, with no polymorphic type resolution.

唯一彻底的修复。在信任边界上用<font color=OrangeRed>纯数据格式加明确 schema</font>替换原生对象序列化：JSON、Protobuf 或 Avro，绑定到具体的 DTO 类型，且不启用多态类型解析。

State that must round-trip through a client should be replaced by an opaque identifier, with the real state held server-side. 需要经客户端往返的状态，应改为不透明标识符，真实状态保存在服务端。

```java
// Before: native serialization, unconstrained
ObjectInputStream ois = new ObjectInputStream(in);
Object obj = ois.readObject();

// After: data-only format bound to an explicit, concrete DTO
OrderDto order = mapper.readValue(json, OrderDto.class);   // no polymorphic typing
```

> 组装家具类比 Analogy: this is the counter narrowing from "any furniture type" to "cabinets only" — see [Concrete type](#mapping-terminology-onto-the-analogy) above.
> 类比：这就是收件口从「任何家具类型」收窄为「只收柜子」—— 对应前文的「具体型别」。

### Allowlist Filtering with JEP 290 使用 JEP 290 白名单过滤

When native Java serialization cannot be removed, constrain which classes may be resolved. <font color=OrangeRed>JEP 290</font> added serialization filters in Java 9 and backported them to 8u121, 7u131, and 6u141.

无法移除 Java 原生序列化时，应限制可解析的类。<font color=OrangeRed>JEP 290</font> 在 Java 9 引入序列化过滤器，并向后移植到 8u121、7u131、6u141。

```java
// Allowlist: permit only expected types, reject everything else.
ObjectInputFilter filter = ObjectInputFilter.Config.createFilter(
    "com.example.dto.*;java.base/java.lang.String;!*");
ObjectInputStream ois = new ObjectInputStream(in);
ois.setObjectInputFilter(filter);
```

```bash
# Process-wide filter, plus depth and size limits to blunt DoS payloads.
java -Djdk.serialFilter='com.example.dto.*;!*;maxdepth=10;maxarray=1000' -jar app.jar
```

Allowlist (`com.example.*;!*`), never denylist. JEP 415 in Java 17 adds context-specific filter factories for finer scoping. 使用白名单（`com.example.*;!*`），绝不使用黑名单。Java 17 的 JEP 415 增加了上下文相关的过滤器工厂，可实现更细粒度的作用域控制。

> 组装家具类比 Analogy: the trailing `!*` is the gatekeeper's default action on an unrecognized item — see [Closed mapping / allowlist](#mapping-terminology-onto-the-analogy) and [Fail closed](#mapping-terminology-onto-the-analogy) above.
> 类比：末尾的 `!*` 就是门房对未识别项目的默认动作 —— 对应前文的「封闭映射／白名单」与「失败时关闭」。

### Integrity Protection 完整性保护

If a serialized blob must cross a trust boundary, authenticate it so tampering is detected before parsing.

若序列化数据必须穿越信任边界，应对其做认证，使篡改在解析前即被发现。

```python
import hmac, hashlib

def sign(data: bytes, key: bytes) -> bytes:
    return hmac.new(key, data, hashlib.sha256).digest()

def verify_and_load(data: bytes, mac: bytes, key: bytes):
    if not hmac.compare_digest(sign(data, key), mac):   # verify first
        raise ValueError("tampered")
    return deserialize(data)                              # parse second
```

> 组装家具类比 Analogy: the HMAC is a tamper-evident seal on the box, checked before the box is ever opened — a broken seal means the box is refused outright, not opened cautiously.
> 类比：HMAC 就是贴在盒子上的防拆封条，在盒子被打开之前先检查。封条破损，盒子就直接拒收，而不是「小心地」打开看看。

- Attach an <font color=OrangeRed>HMAC</font> over the serialized bytes using a server-held key, and verify it before deserializing. Verify first, parse second. 用服务端持有的密钥对序列化字节计算 <font color=OrangeRed>HMAC</font>，并在反序列化之前验证。先验证，后解析。
- Use a constant-time comparison for the MAC. 使用恒定时间比较验证 MAC。
- Signing proves integrity and origin, not confidentiality — signed data is still readable, so secrets do not belong in it. 签名只保证完整性与来源，不保证机密性 —— 已签名的数据仍可被读取，因此不应在其中放置敏感信息。
- Keys must be per-deployment, rotatable, and never shipped as a default. A hardcoded or shared key reduces the control to decoration, which is precisely what made CVE-2020-0688 exploitable at scale. 密钥必须按部署实例生成、可轮换、且绝不作为默认值分发。硬编码或共享密钥会让该控制措施形同虚设，CVE-2020-0688 正因如此被大规模利用。

### Language Specific Hardening 各语言加固要点

| Language | Action 措施 |
| --- | --- |
| Java | Apply `jdk.serialFilter` allowlists; remove `commons-collections` style gadgets where possible; for Jackson use explicit DTOs or a strict `PolymorphicTypeValidator`; disable fastjson AutoType |
| PHP | Never `unserialize()` user input — use `json_decode`; set `allowed_classes` if `unserialize()` is unavoidable; block `phar://` via `phar.readonly` and validate upload paths |
| Python | Never unpickle untrusted bytes; use `json` or `yaml.safe_load`; keep `allow_pickle=False`; set `torch.load(weights_only=True)`; treat model artifacts as untrusted executables |
| .NET | Remove `BinaryFormatter` and friends; avoid `TypeNameHandling` other than `None`; enforce ViewState MAC with a per-deployment `machineKey` |

Defense in depth, applied regardless of language: run deserialization in a <font color=OrangeRed>low-privilege, network-restricted</font> context so a successful chain lands somewhere with nothing worth reaching; enforce egress filtering to break the download-and-execute second stage; alert on child processes spawned by application servers; and patch dependencies promptly, since new gadget chains are discovered in already-installed libraries.

各语言通用的纵深防御：在<font color=OrangeRed>低权限、受限网络</font>的上下文中执行反序列化，使成功的利用链落在无价值的位置；实施出站流量过滤以打断「下载并执行」的第二阶段；对应用服务器创建子进程的行为告警；及时更新依赖，因为新的小工具链会在已安装的库中被发现。

### Defense Summary Table 防御汇总表

| # | Control 控制措施 | Effectiveness 有效性 | CWE / Reference |
| --- | --- | --- | --- |
| 1 | Replace native serialization with data-only format + schema | Eliminates the class 根除该问题 | CWE-502 |
| 2 | Allowlist filtering (`jdk.serialFilter`, `allowed_classes`) | Strong 强 | JEP 290 / JEP 415 |
| 3 | HMAC integrity check before parsing | Strong, key management dependent 强，依赖密钥管理 | CWE-345, CWE-347 |
| 4 | Disable polymorphic typing (Jackson, fastjson, `TypeNameHandling`) | Strong for JSON layers 对 JSON 层有效 | CWE-502 |
| 5 | Remove or update gadget-bearing dependencies | Partial, raises cost 部分，提高攻击成本 | CWE-1104 |
| 6 | Low-privilege sandbox + egress filtering | Limits impact 限制影响 | MITRE T1190 |
| 7 | Denylist of known gadget classes | <font color=OrangeRed>Weak — always lags</font> 弱，必然滞后 | — |

---

## Case Studies in This Knowledge Base 本库中的案例

Two CVE analyses in this repo demonstrate the model end to end. Both are Java, both reach RCE, and both are worth reading after the theory above.

本库中有两篇 CVE 分析完整演示了上述模型，均为 Java 且都达成 RCE，建议在理解上述理论后阅读。

> Jackson polymorphic typing, CVE-2019-12384 and CVE-2017-7525, including the H2 JDBC SSRF-to-RCE step:
> `_posts/Lab/htb/time/2020-10-10-CVE-Jackson反序列化漏洞分析.md`

> Tomcat `PersistentManager` / `FileStore` session deserialization, CVE-2020-9484, driven with `ysoserial`:
> `_posts/Lab/htb/hard-feline/2021-01-09-CVE-2020-9484.md`

> Operational exploitation logs for the same two vectors:
> `_posts/Lab/htb/time/2020-11-13-HTB-Time.md` and `_posts/Lab/htb/hard-feline/2021-01-09-HTB-Feline.md`

> Framework mapping context:
> `_posts/10SecConcepts/Attack/2019-12-16-OWASP10andCWE25.md`

---

## Key Takeaways

- <font color=OrangeRed>The payload is an object graph, not code.</font> Exploitation reuses classes already on the classpath, so the vulnerable application contains nothing that looks malicious.
  <font color=OrangeRed>载荷是对象图而非代码。</font>利用过程复用类路径中已有的类，因此漏洞应用里找不到任何看起来恶意的东西。
- <font color=OrangeRed>Deserialization executes before authorization.</font> That is why impact is typically pre-authentication remote code execution rather than a lesser data-integrity issue.
  <font color=OrangeRed>反序列化发生在鉴权之前。</font>这正是其影响通常为未授权远程代码执行，而非较轻的数据完整性问题的原因。
- <font color=OrangeRed>Native object formats are unsafe by design; data-only formats are safe until a library adds type resolution.</font> JSON is fine, JSON with `@type` is not.
  <font color=OrangeRed>原生对象格式在设计上就不安全；纯数据格式在库为其加上类型解析之前是安全的。</font>JSON 没问题，带 `@type` 的 JSON 有问题。
- <font color=OrangeRed>Exploitability is a property of the dependency set.</font> The same one-line sink flips from unexploitable to trivially exploitable when a gadget-bearing library is added.
  <font color=OrangeRed>可利用性取决于依赖集合。</font>同一处一行代码的汇聚点，在引入含小工具的库后会从打不动变为一击必中。
- <font color=OrangeRed>Allowlist, never denylist.</font> Denylists enumerate known chains and are permanently behind current research; `jdk.serialFilter` with `!*` as the terminal rule inverts that.
  <font color=OrangeRed>用白名单，不用黑名单。</font>黑名单只能枚举已知链条并永远落后于最新研究；以 `!*` 结尾的 `jdk.serialFilter` 白名单反转了这一劣势。
- <font color=OrangeRed>Signing is not a substitute for not deserializing.</font> An HMAC is only as strong as its key management, and a shared or hardcoded key makes the control cosmetic.
  <font color=OrangeRed>签名不能替代「不反序列化」。</font>HMAC 的强度取决于密钥管理，共享或硬编码的密钥会让该控制措施沦为装饰。
- <font color=OrangeRed>Machine-learning model files are executables.</font> `pickle`-backed artifacts such as `.pkl`, `.pt`, and `.joblib` run code on load, so loading one from an untrusted registry is running an untrusted binary.
  <font color=OrangeRed>机器学习模型文件就是可执行文件。</font>`.pkl`、`.pt`、`.joblib` 等基于 `pickle` 的产物在加载时执行代码，从不可信仓库加载等同于运行不可信二进制。

---

## References

- CWE-502: Deserialization of Untrusted Data
- OWASP Top 10 — A8:2017 Insecure Deserialization, merged into A08:2021 Software and Data Integrity Failures
- OWASP Deserialization Cheat Sheet
- JEP 290: Filter Incoming Serialization Data
- JEP 415: Context-Specific Deserialization Filters
- MITRE ATT\&CK — T1190 Exploit Public-Facing Application, T1059 Command and Scripting Interpreter
- `ysoserial` — Java gadget chain payload generator (Chris Frohoff)
- `ysoserial.net` — .NET equivalent
- `phpggc` — PHP gadget chain generator
- Sam Thomas, "It's a PHP Unserialization Vulnerability Jim, but Not as We Know It" — phar deserialization research
- Python `pickle` module documentation — explicit warning that pickle is not secure against maliciously constructed data
- CVE-2015-4852, CVE-2017-7525, CVE-2017-9805, CVE-2017-10271, CVE-2019-2725, CVE-2019-12384, CVE-2020-9484, CVE-2016-7124, CVE-2020-0688
