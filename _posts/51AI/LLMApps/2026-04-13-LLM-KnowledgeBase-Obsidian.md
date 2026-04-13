---
title: LLMApps - Karpathy LLM Knowledge Base with Obsidian
date: 2026-04-13 11:11:11 -0400
description: Build a compounding personal knowledge base where an LLM maintains a persistent wiki — replacing RAG with structured ingest, query, and lint operations inside an Obsidian vault.
categories: [51AI, LLMApps]
tags: [AI, LLM, KnowledgeBase, Obsidian, RAG, Karpathy, PKM, Workflow]
---

# Karpathy LLM Knowledge Base — Obsidian Implementation

**Table of contents:**

- [Karpathy LLM Knowledge Base — Obsidian Implementation](#karpathy-llm-knowledge-base--obsidian-implementation)
  - [Overview](#overview)
  - [Why Not RAG](#why-not-rag)
  - [3-Layer Architecture](#3-layer-architecture)
  - [3 Core Operations](#3-core-operations)
    - [Ingest 入库](#ingest-入库)
    - [Query 查询](#query-查询)
    - [Lint 健康检查](#lint-健康检查)
  - [Two Special Files](#two-special-files)
    - [`index.md` — Content Catalog](#indexmd--content-catalog)
    - [`log.md` — Activity Log](#logmd--activity-log)
  - [Obsidian Vault Implementation](#obsidian-vault-implementation)
    - [Directory Layout](#directory-layout)
    - [Page Format](#page-format)
    - [Schema File (SCHEMA.md)](#schema-file-schemamd)
  - [Real Vault Stats](#real-vault-stats)
  - [Obsidian Tips](#obsidian-tips)
  - [Key Takeaway](#key-takeaway)
  - [References](#references)

---

## Overview

**LLM-KB** is an architecture where the LLM incrementally builds and maintains a persistent wiki — rather than re-deriving answers from raw documents at query time (as in RAG). Knowledge accumulates and compounds over time.

> Coined/popularized by **Andrej Karpathy** (2026).
> Source: [GitHub Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

**Division of labor:**

| Role      | Job                                                                           |
| --------- | ----------------------------------------------------------------------------- |
| **Human** | Curate sources, ask questions, direct analysis                                |
| **LLM**   | Write wiki pages, update cross-references, maintain consistency, file answers |

不要只做研究，要养研究资产。

- "做研究"是一次性的——看了一份报告，做了一个判断，然后这个判断就埋在聊天记录里了。
- "养资产"是持续的——每一份报告都变成知识库的一部分，每一个判断都有证据链，每一次市场验证都更新了你对这家公司的理解。

Examples:

| 做研究                 | 养研究资产                           |
| ---------------------- | ------------------------------------ |
| 看完研报，记个要点     | 更新到公司页，关联到主题页           |
| 买入时心里有想法       | 写成thesis，列出证据和反证           |
| 跌了，"拿着吧"         | 检查论据是被强化了还是被削弱了       |
| 卖了，结束             | 复盘页：为什么买、为什么卖、学到什么 |
| 再看同一只股票，从头来 | 打开公司页，所有历史研究都在         |

把信息、论据、量化验证、风险管理和执行建议连成一个闭环。

- 信息层：新闻、财报、行情数据的结构化整理
- 论据层：为什么看多/看空，证据是什么，证据有没有过期
- 验证层：历史统计、因子回测、风险暴露分析
- 执行层：在什么位置买、仓位多大、什么条件退出
- 复盘层：事后追踪，判断有没有失真这不是一个"选股工具"。
- 让投资判断从"拍脑袋"变成"可追踪、可校验、可迭代"的系统。让认知可以复利。



---

## Why Not RAG

| RAG                                                   | LLM-KB                                             |
| ----------------------------------------------------- | -------------------------------------------------- |
| Re-discovers knowledge from scratch on every query    | Knowledge accumulates over time                    |
| Requires vector DB + embedding infrastructure         | Just markdown files in a folder                    |
| Passive — retrieval only                              | Active — LLM maintains the knowledge base          |
| Subtle cross-document synthesis re-queried every time | Synthesis filed once, referenced forever           |
| Not human-readable at the retrieval layer             | Everything is human-readable and directly editable |

> **RAG**: good for large, static document corpora you don't want to re-process.
> **LLM-KB**: better for knowledge that accumulates, evolves, and requires repeated synthesis.

---

## 3-Layer Architecture

```bash
Layer 1: Raw Sources (Immutable)
  ├── Articles, papers, web clips, PDFs
  ├── LLM reads — NEVER edits
  └── Source of truth

Layer 2: Wiki Pages (LLM-owned)
  ├── Summaries, concept pages, entity pages, comparisons
  ├── LLM writes and maintains everything here
  └── Human can read, browse, and correct

Layer 3: Schema (Co-evolved)
  ├── Config doc: wiki structure, conventions, operations
  ├── Evolved by human + LLM over time
  └── Lives as SCHEMA.md or CLAUDE.md in the wiki root
```

Karpathy的系统有三层，非常清晰：

- 第一层：原始资料
  - 财报、研报、新闻、电话会纪要、行情数据、聊天记录。
  - 这些是“只读"的—进来了就不改，永远当原始证据保存。

- 第二层：知识库（Wiki）
  - 这是核心。Al 读完原始资料后，不是简单做个摘要就完事。而是：
  - 给每家公司建一个"档案页"：基本面、看多逻辑、风险、催化剂、退出条件给每个投资主题建一个"主题页"：AI算力周期、存储景气度、港股高息、美联储政策
  - 给每个策略建一个"策略页"：动量策略适合什么市场、全天候组合怎么配
  - 给每个持仓建一个"论据页"：我为什么买的、证据是什么、什么情况下论据失效
  - 最关键的是——这些页面之间互相连美光的公司页链接到存储周期的主题页，存储周期链接到AI算力主题页，AI算力又链接到英伟达和台积电。新的财报出来，不只是更新一个页面，而是沿着这些连接，把相关的页面全部同步更新。
  - Karpathy自己的原话：
  - “一个新资料进来，可能要触及10-15个Wiki页面。"这才是“知识复利"的意思：不是存了多少，而是连接了多少。

- 第三层：规则文件
  - 一份告诉AI"怎么维护这个知识库"的说明书。
    - 什么格式
    - 什么命名规范
    - 新资料进来怎么处理
    - 多久做一次"健康检查"
    - 哪些矛盾需要标记
  - 相当于给AI立了一套投研纪律。

---

## 3 Core Operations

### Ingest 入库

Drop a new source → tell LLM to process it:

1. Read source file
2. Extract key information and entities
3. Write or update wiki pages in `pages/`
4. Update `pages/index.md` — add new pages with one-line summaries
5. Append to `log.md`:

```markdown
## [YYYY-MM-DD] ingest | Source Title
- Pages created: [[Page Name]]
- Pages updated: [[Other Page]]
```

> One source may touch **5–15 wiki pages** — entities, concepts, topics, and cross-references.
> Prefer updating existing pages over creating new ones for incremental additions.

举个例子：一份美光季报出来了。
AI 不只是写个"美光Q2收入beat"的摘要。它还会去检查—之前存储周期主题页里写的“库存正在去化"，和这份财报里的库存数据一致吗？之前的看多论据"DRAM价格趋势向上"，这次财报支持还是削弱了？

### Query 查询

Ask questions against the accumulated wiki:

1. LLM reads `index.md` → identifies relevant pages
2. Reads relevant pages
3. Synthesizes answer with citations (`[[wikilinks]]`)
4. **Files substantive answers back as new wiki pages** — comparisons, analyses, and connections should not disappear into chat history

Output formats: markdown page, comparison table, Marp slide deck, matplotlib chart, Obsidian canvas.

### Lint 健康检查

Periodic health check (on-demand or scheduled):

1. Find contradictions between pages
2. Find orphan pages (no inbound links) — flag or connect
3. Find concepts mentioned but lacking their own page — create stubs
4. Find stale claims superseded by newer sources
5. Suggest 2–3 new questions or sources to investigate
6. Append to `log.md`:

```markdown
## [YYYY-MM-DD] lint | Wiki Health Check
- Issues found: ...
- Pages created: ...
- Recommendations: ...
```

---

## Two Special Files

### `index.md` — Content Catalog

- Every wiki page listed with a `[[wikilink]]` and one-line summary
- Organized by category (Concepts, Security, Cloud, AI, etc.)
- **LLM reads this first on every query**
- Updated on every ingest — never let it go stale

```markdown
## AI & Machine Learning
| Page                   | Summary                                                       |
| ---------------------- | ------------------------------------------------------------- |
| [[AI/LLM]]             | LLMs: prompting, fine-tuning, OWASP LLM Top 10, RAG, security |
| [[LLM-Knowledge-Base]] | Karpathy's pattern: 3-layer wiki replacing RAG                |
```

### `log.md` — Activity Log

- Append-only chronological record
- Every ingest, query, and lint pass recorded
- Parse last 5 entries:

```bash
grep "^## \[" wiki/log.md | tail -5
```

---

## Obsidian Vault Implementation

### Directory Layout

```
wiki/
├── inbox/
│   └── Clippings/          # Layer 1: Raw sources — web clips, articles, PDFs
│                            # IMMUTABLE — LLM reads but NEVER modifies
├── pages/                  # Layer 2: LLM-maintained wiki pages
│   ├── concepts/           # Ideas, patterns, technologies, methods
│   ├── topics/             # Broad topic summaries / synthesis pages
│   └── index.md            # Content catalog — read this first on every query
├── _templates/
│   └── page.md             # Template for new wiki pages
├── log.md                  # Append-only activity log
└── SCHEMA.md               # Layer 3: Operating instructions for the LLM
```

### Page Format

Every wiki page uses this frontmatter:

```yaml
---
type: wiki-concept | wiki-entity | wiki-topic | wiki-summary
date: YYYY-MM-DD          # date first created
updated: YYYY-MM-DD       # date last updated
tags: [tag1, tag2]
sources: [filename.md]    # raw source files this page draws from
status: active | stub | needs-review
---
```

Heading structure:

```markdown
# Title
## Summary          — 2–4 sentence synthesis
## Key Points       — bulleted facts, claims, definitions
## Connections      — [[wikilinks]] to related pages
## Open Questions   — gaps, contradictions, things to investigate
## Sources          — links back to inbox/ raw files
```

### Schema File (SCHEMA.md)

The `SCHEMA.md` tells the LLM exactly how to operate:

- Directory structure and layer definitions
- Page format and frontmatter spec
- Step-by-step procedures for Ingest, Query, Lint
- Conventions: raw sources are immutable, good answers get filed, index stays current, log is append-only

> This file is co-evolved by human and LLM. As edge cases arise, add them here.
> Think of it as the LLM's "job description" for maintaining the wiki.

---

## Real Vault Stats

This ObsidianV vault runs the LLM-KB pattern with a cybersecurity focus:

| Metric               | Value                                                     |
| -------------------- | --------------------------------------------------------- |
| Total wiki pages     | 102                                                       |
| Raw sources ingested | 769                                                       |
| Top-level categories | 19                                                        |
| Largest subcategory  | AWS (~100+ files: IAM, EKS, boto3, CI/CD, ML)             |
| Richest AI category  | AI/LLM (OWASP LLM Top 10, RAG, fine-tuning, MCP security) |
| Init date            | 2026-04-08                                                |

**Batch ingest example** — 768 SecurityKB source files → 100 wiki pages in one pass:

```
## [2026-04-08] ingest | SecurityKB batch ingest — 768 source files → 100 wiki pages
- Source: wiki/reference/SecurityKB/_posts/ (768 .md files across 19 categories)
- Strategy: subcategory-level granularity — one wiki page per subfolder
- Pages created: 100 pages across wiki/pages/topics/
- Index updated: wiki/pages/index.md (101 total pages)
```

---

## Obsidian Tips

| Tip                         | Details                                                                                                                                |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **Web Clipper**             | Browser extension converts articles → markdown for `inbox/Clippings/`                                                                  |
| **Graph view**              | Visualize wiki topology — spot orphan pages and hub pages                                                                              |
| **Dataview**                | Add YAML frontmatter (`tags`, `date`, `source`) → render dynamic tables                                                                |
| **Marp**                    | Generate slide decks directly from wiki pages (Obsidian plugin available)                                                              |
| **Git**                     | Wiki is just markdown files → version history and branching are free                                                                   |
| **Download images locally** | Settings → Files and links → set attachment path; bind hotkey for "Download attachments"                                               |
| **qmd**                     | Local CLI + MCP server for hybrid BM25/vector search across markdown — useful when `index.md` alone isn't enough at scale (500+ pages) |

> *"Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."*
> — Keep LLM agent open on one side, Obsidian on the other. LLM edits, you browse in real time.

---

## Key Takeaway

The core insight: **maintenance cost is why wikis die**.

- Humans abandon wikis because bookkeeping grows faster than value
- LLMs don't get bored, don't forget to update cross-references, can touch 15 files in one pass
- The Memex vision (Vannevar Bush, 1945) — a private, curated knowledge store with associative trails — was always the right idea. The missing piece was who does the maintenance. The LLM handles that.

**The workflow in one line:**
> Spend your time curating sources and asking good questions. Let the LLM do everything else.

---

## References

- Andrej Karpathy — [LLM Wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [qmd](https://github.com/tobi/qmd) — local markdown search (BM25/vector hybrid, CLI + MCP)
- Obsidian Web Clipper — browser extension for markdown clipping
- Vannevar Bush — *As We May Think* (1945) — conceptual ancestor of LLM-KB
