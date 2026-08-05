---
title: "Meow's Docker - Layer Caching and Incremental Builds"
date: 2026-06-15 11:11:11 -0400
categories: [30System, Docker]
tags: [Docker, Dockerfile, build-cache, uv, buildx, python, incremental-build]
math: false
toc: true
image:
---

# Docker Layer Caching and Incremental Builds
# Docker 层级缓存与增量构建

---

## Overview 概述

Every `docker build` breaks a Dockerfile into a stack of layers. Docker caches each layer by a hash of its inputs. When a layer's hash matches what is already stored, Docker reuses the cached result and skips re-executing that step. Understanding which inputs go into each hash — and why the **order** of instructions in a Dockerfile determines whether expensive steps get cached — is the foundational skill behind fast Docker workflows.

每次 `docker build` 都会将 Dockerfile 分解为一组层级堆栈。Docker 通过对每层输入内容计算哈希值来缓存各层。当某层的哈希值与已存储的结果匹配时，Docker 会复用缓存并跳过重新执行该步骤。理解哪些输入参与哈希计算，以及为何 Dockerfile 中指令的**顺序**决定了耗时步骤能否被缓存，是实现快速 Docker 工作流的基础技能。

---

## 1. How Docker Builds Work — Layers and the Union Filesystem
## 1. Docker 构建原理 — 层级与联合文件系统

### What is a layer? 什么是层？

A Docker image is not a single flat archive. It is a **stack of read-only filesystem snapshots**, each called a layer. Every instruction in a Dockerfile (`FROM`, `RUN`, `COPY`, `ADD`, `ENV`, etc.) that changes the filesystem produces a new layer on top of the previous one.

Docker 镜像不是单一的扁平归档文件。它是一组**只读文件系统快照的堆栈**，每个快照称为一层（layer）。Dockerfile 中每条会改变文件系统的指令（`FROM`、`RUN`、`COPY`、`ADD`、`ENV` 等）都会在前一层之上生成一个新层。

```
Image layer stack (top = newest):
镜像层级堆栈（顶部 = 最新）：

  [ Layer 5 ] COPY main/ .          <-- service code
  [ Layer 4 ] RUN pip install ...   <-- installed packages
  [ Layer 3 ] COPY pyproject.toml . <-- manifest file
  [ Layer 2 ] RUN apt-get install   <-- OS packages
  [ Layer 1 ] FROM python:3.11      <-- base image
```

At runtime, Docker uses a **union filesystem** (OverlayFS on Linux) to merge all layers into a single coherent directory tree. The result looks like one flat filesystem to the running container, but each layer is stored separately on disk.

在运行时，Docker 使用**联合文件系统**（Linux 上为 OverlayFS）将所有层合并为一个连贯的目录树。对运行中的容器来说，结果看起来像一个扁平的文件系统，但每一层在磁盘上是单独存储的。

### Why layers matter for build speed 为何层级对构建速度至关重要

Each layer is identified by a **cache key** — a hash computed from:

每一层通过一个**缓存键**来标识，该键由以下内容的哈希值计算得出：

- The parent layer's cache key 父层的缓存键
- The Dockerfile instruction text 指令文本
- For `COPY`/`ADD`: the checksum of the files being copied 被复制文件的校验和
- For `RUN`: the exact command string 精确的命令字符串

If the cache key matches a stored layer, Docker prints `CACHED` and moves on instantly. If it does not match, Docker re-executes that instruction — and **all subsequent layers are also re-executed**, because each layer's key depends on its parent.

如果缓存键与已存储的层匹配，Docker 会打印 `CACHED` 并立即继续。如果不匹配，Docker 会重新执行该指令——**所有后续层也会重新执行**，因为每层的键都依赖于其父层。

```
If Layer 3 cache miss → Layer 4 re-runs → Layer 5 re-runs → ...
如果第 3 层缓存未命中 → 第 4 层重新执行 → 第 5 层重新执行 → ...
```

This cascading invalidation is the central mechanic. The goal of Dockerfile optimization is to arrange layers so that **frequently-changing inputs appear as late as possible**.

这种级联失效是核心机制。Dockerfile 优化的目标是合理排列层级，使**频繁变化的输入尽可能靠后出现**。

---

## 2. The Layer Cache: What Invalidates It and Why Order Matters
## 2. 层级缓存：何时失效及顺序为何重要

### Cache invalidation triggers 缓存失效触发条件

| Instruction | Cache invalidates when... |
|---|---|
| `FROM` | Base image digest changes |
| `RUN` | Command string changes |
| `COPY src dest` | Any file under `src` changes (checksum-based) |
| `ADD` | Source file or URL content changes |
| `ENV`, `ARG` | Value changes (and invalidates all `RUN` steps after it) |

| 指令 | 缓存失效时机 |
|---|---|
| `FROM` | 基础镜像摘要变更 |
| `RUN` | 命令字符串变更 |
| `COPY src dest` | `src` 下任意文件变更（基于校验和） |
| `ADD` | 源文件或 URL 内容变更 |
| `ENV`, `ARG` | 值变更（并使其后所有 `RUN` 步骤失效） |

### The mental model: a waterfall 心智模型：瀑布

Think of layers as a waterfall. Water flows from top to bottom. Once a layer is invalidated (the water changes), everything below it also gets new water. Cached layers above the invalidation point are unaffected.

将层级想象成一道瀑布。水从上往下流。一旦某层失效（水发生变化），其下方的所有内容也会获得新的水流。失效点上方的已缓存层不受影响。

```
Layer 1: FROM python:3.11           -> rarely changes -> CACHED almost always
Layer 2: RUN apt-get install curl   -> rarely changes -> CACHED almost always
Layer 3: COPY . /app                -> changes on EVERY .py edit -> CACHE MISS
Layer 4: RUN pip install -r req.txt -> always re-runs because Layer 3 missed
                                       even though req.txt itself didn't change
```

Layer 3 copies ALL source code. Any `.py` file change updates Layer 3's checksum, which misses the cache, which forces Layer 4 (the slow `pip install`) to re-run — even though the dependencies themselves did not change.

第 3 层复制了所有源代码。任何 `.py` 文件的更改都会更新第 3 层的校验和，导致缓存未命中，进而强制第 4 层（耗时的 `pip install`）重新执行——即使依赖项本身根本没有变化。

---

## 3. The "COPY-Before-Install" Anti-Pattern
## 3. "先 COPY 再安装"反模式

This is the exact bug that PR #2853 fixed in the code-guard project.

这正是 PR #2853 在 code-guard 项目中修复的问题。

### Bad order (before the fix) 错误顺序（修复前）

```dockerfile
FROM python:3.11
RUN apt-get install -y curl

# BAD: Copy ALL service code first
COPY main/ /app/main/
COPY common/ /app/common/
COPY pyproject.toml /app/

# This runs AFTER the code copy, so it re-runs on every .py change
RUN uv pip install -r pyproject.toml
```

**What happens on every `.py` file edit:**
**每次编辑 `.py` 文件时发生的情况：**

1. `COPY main/` detects changed files → cache miss on Layer 3
   `COPY main/` 检测到文件变更 → 第 3 层缓存未命中
2. `COPY common/` re-runs (cascade) — even if common/ unchanged
   `COPY common/` 重新执行（级联）— 即使 common/ 未变更
3. `COPY pyproject.toml` re-runs
   `COPY pyproject.toml` 重新执行
4. `RUN uv pip install` re-runs — **this takes 2-5 minutes**
   `RUN uv pip install` 重新执行 — **这需要 2-5 分钟**

A one-line Python change triggers a full dependency re-install on every build. Multiply by 5 images and this dominates build time.

一行 Python 代码的修改会在每次构建时触发完整的依赖重新安装。乘以 5 个镜像，这将主导构建时间。

### Good order (after the fix) 正确顺序（修复后）

```dockerfile
FROM python:3.11
RUN apt-get install -y curl

# GOOD: Copy only the manifest first
COPY pyproject.toml /app/

# Install deps — only re-runs when pyproject.toml changes
RUN uv pip install -r pyproject.toml

# Copy service code AFTER — cache miss here does NOT cascade up to pip install
COPY main/ /app/main/
COPY common/ /app/common/

# Editable install — re-runs on code changes, but it's fast (no downloads)
RUN uv pip install -e .
```

**What happens on every `.py` file edit now:**
**现在每次编辑 `.py` 文件时发生的情况：**

1. `COPY pyproject.toml` — file unchanged → **CACHED**
   `COPY pyproject.toml` — 文件未变更 → **缓存命中**
2. `RUN uv pip install -r pyproject.toml` — parent cached → **CACHED**
   `RUN uv pip install -r pyproject.toml` — 父层缓存命中 → **缓存命中**
3. `COPY main/` — detects changed `.py` → cache miss, re-runs (fast, just copy)
   `COPY main/` — 检测到 `.py` 变更 → 缓存未命中，重新执行（快速，仅复制）
4. `RUN uv pip install -e .` — re-runs (fast, no downloads, just symlinks)
   `RUN uv pip install -e .` — 重新执行（快速，无需下载，仅创建符号链接）

The 2-5 minute dependency install is now cached on code changes. Only `pyproject.toml` edits trigger it.

2-5 分钟的依赖安装现在在代码修改时会被缓存命中。只有编辑 `pyproject.toml` 才会触发它。

---

## 4. `pyproject.toml`-Based Caching — The Manifest as Cache Key
## 4. 基于 `pyproject.toml` 的缓存 — 清单文件作为缓存键

### What is `pyproject.toml`? 什么是 `pyproject.toml`？

`pyproject.toml` is the Python project manifest — it declares the project name, version, and most importantly, the list of **dependencies** (packages the project needs to run). It is the Python equivalent of `package.json` in Node.js or `pom.xml` in Maven.

`pyproject.toml` 是 Python 项目清单文件——它声明了项目名称、版本，以及最重要的**依赖项**列表（项目运行所需的包）。它相当于 Node.js 中的 `package.json` 或 Maven 中的 `pom.xml`。

```toml
# Example pyproject.toml
[project]
name = "code-guard-main"
version = "1.0.0"
dependencies = [
    "fastapi>=0.100.0",
    "pydantic>=2.0.0",
    "motor>=3.3.0",
]
```

### Why it makes the perfect cache key 为何它是完美的缓存键

The rule is: **dependencies should only be re-installed when the dependency list changes.** `pyproject.toml` is exactly that list. By copying only `pyproject.toml` before the install step, the Docker layer cache key becomes:

规则是：**只有当依赖项列表发生变化时，才应重新安装依赖项。** `pyproject.toml` 正是这个列表。通过在安装步骤之前仅复制 `pyproject.toml`，Docker 层级缓存键变为：

```
hash(parent_layer_key + "RUN uv pip install" + checksum(pyproject.toml))
```

This hash only changes when `pyproject.toml` changes — not when any `.py` file changes. Service code changes happen dozens of times per day; `pyproject.toml` changes perhaps once a week. The optimization eliminates the wasted install time on the 95%+ of builds where deps are unchanged.

这个哈希值只有在 `pyproject.toml` 变更时才会改变——而不是在任何 `.py` 文件变更时改变。服务代码每天可能修改数十次；`pyproject.toml` 可能每周只改一次。这项优化消除了在 95% 以上依赖项未变更的构建中浪费的安装时间。

---

## 5. `uv`, Wheels, and Buildx Daemon Cache Mounts
## 5. `uv`、Wheel 与 Buildx Daemon 缓存挂载

### What is `uv`? 什么是 `uv`？

<font color=OrangeRed>`uv`</font> is a fast Python package installer and resolver written in Rust (by Astral, the makers of `ruff`). It is a drop-in replacement for `pip` and `pip-tools`, but 10-100x faster because it uses a persistent local cache of downloaded wheels and resolves dependencies in parallel.

<font color=OrangeRed>`uv`</font> 是一个用 Rust 编写的快速 Python 包安装器和解析器（由 `ruff` 的开发者 Astral 出品）。它是 `pip` 和 `pip-tools` 的直接替代品，但速度快 10-100 倍，因为它使用持久化的本地 wheel 缓存并并行解析依赖项。

### What is a wheel? 什么是 wheel？

A <font color=OrangeRed>wheel</font> (`.whl` file) is a pre-built binary distribution format for Python packages. Think of it as a zip file containing the compiled package, ready to be extracted directly into `site-packages` without compilation. When `uv` (or `pip`) installs a package, it:

<font color=OrangeRed>Wheel</font>（`.whl` 文件）是 Python 包的预构建二进制发行格式。可以将其想象为一个包含已编译包的 zip 文件，可以直接解压到 `site-packages`，无需编译。当 `uv`（或 `pip`）安装一个包时，它会：

1. **Resolve**: figure out which version of each dependency to use
   **解析**：确定每个依赖项使用哪个版本
2. **Download**: fetch `.whl` files from PyPI (or a cache)
   **下载**：从 PyPI（或缓存）获取 `.whl` 文件
3. **Install**: extract wheel contents into `site-packages`
   **安装**：将 wheel 内容解压到 `site-packages`

Steps 1 and 2 are the slow parts (network-bound). Step 3 is fast (local disk IO). A wheel cache stores the downloaded `.whl` files so that re-installs skip the download step entirely.

步骤 1 和 2 是慢的部分（受网络限制）。步骤 3 很快（本地磁盘 IO）。Wheel 缓存存储已下载的 `.whl` 文件，使重新安装时完全跳过下载步骤。

### The problem: Docker layer cache vs. uv's local cache 问题：Docker 层级缓存 vs. uv 的本地缓存

By default, `uv` stores its wheel cache at `/root/.cache/uv` inside the container. But **Docker layer isolation means this cache directory disappears between builds** — each `RUN` step starts from a clean copy of the parent layer's filesystem. So every `RUN uv pip install` re-downloads everything from the network, even if the same packages were just installed yesterday.

默认情况下，`uv` 将其 wheel 缓存存储在容器内的 `/root/.cache/uv`。但**Docker 的层级隔离意味着这个缓存目录在构建间会消失**——每个 `RUN` 步骤都从父层文件系统的干净副本开始。因此每次 `RUN uv pip install` 都会从网络重新下载所有内容，即使相同的包昨天刚刚安装过。

### The solution: BuildKit cache mounts 解决方案：BuildKit 缓存挂载

<font color=OrangeRed>BuildKit</font> (Docker's build engine, enabled via `docker buildx`) introduced **cache mounts** — a special mount type that persists a directory across builds on the same build daemon, but is **never included in the final image**.

<font color=OrangeRed>BuildKit</font>（通过 `docker buildx` 启用的 Docker 构建引擎）引入了**缓存挂载**——一种特殊的挂载类型，可在同一构建守护进程上的多次构建间持久化某个目录，但**永远不会包含在最终镜像中**。

```dockerfile
# Without cache mount — re-downloads every time
RUN uv pip install -r pyproject.toml --no-cache

# With cache mount — reuses downloaded wheels across builds
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install -r pyproject.toml
```

The `--mount=type=cache,target=/root/.cache/uv` line tells BuildKit: "mount a persistent cache volume at `/root/.cache/uv` during this `RUN` step." The volume survives between builds. The final image does not contain it (zero size impact).

`--mount=type=cache,target=/root/.cache/uv` 这行告诉 BuildKit："在此 `RUN` 步骤期间，在 `/root/.cache/uv` 挂载一个持久化缓存卷。"该卷在构建间持续存在。最终镜像不包含它（零大小影响）。

### What "same buildx daemon" means "相同 buildx 守护进程"的含义

The cache mount is stored by the **buildx daemon** — the background process that actually runs builds. On a developer's machine, this is typically the Docker Desktop VM or a local `buildkitd` process. The cache persists as long as that daemon is running. If the daemon is restarted or the machine is rebooted, the cache may be cleared. On CI machines, the daemon persists for the lifetime of the build agent pod — subsequent builds on the same agent reuse the cache.

缓存挂载由 **buildx 守护进程**存储——即实际运行构建的后台进程。在开发者的机器上，这通常是 Docker Desktop VM 或本地的 `buildkitd` 进程。只要该守护进程在运行，缓存就会持续存在。如果守护进程重启或机器重启，缓存可能会被清除。在 CI 机器上，守护进程在构建 agent pod 的生命周期内持续存在——同一 agent 上的后续构建会复用缓存。

### Combined effect of both optimizations 两项优化的叠加效果

```
Scenario: Developer edits one .py file and rebuilds
场景：开发者编辑一个 .py 文件并重新构建

WITHOUT fixes (original):
  COPY main/ -> cache miss
  COPY pyproject.toml -> re-runs
  RUN uv pip install -> re-runs, re-downloads all wheels: ~3-5 min
  Total: 3-5 minutes

WITH layer reorder only:
  COPY pyproject.toml -> CACHED
  RUN uv pip install -> CACHED (layer cache hit)
  COPY main/ -> cache miss (fast)
  RUN uv pip install -e . -> re-runs (fast, no downloads)
  Total: ~10 seconds

WITH layer reorder + cache mount:
  Same as above, but even on a cold build where pyproject.toml changes:
  RUN uv pip install -> wheels already cached locally -> no downloads
  Total: ~10-20 seconds even for new dependency
```

---

## 6. Incremental vs Cold Rebuilds
## 6. 增量构建 vs 冷构建

### Cold build 冷构建

A build with **no cache available** — either first ever build, after `docker builder prune`, or on a fresh CI runner. Every layer executes from scratch. This is unavoidable for the first build but should be rare in practice.

**没有可用缓存**的构建——无论是首次构建、执行 `docker builder prune` 后，还是在全新的 CI runner 上。每一层都从头执行。对于首次构建这是不可避免的，但在实践中应该很少发生。

### Incremental build 增量构建

A build where **some layers are cached**. In a well-optimized Dockerfile, an incremental build after a single `.py` file change should only re-run the layers after the `COPY <service-code>` instruction. Everything above it (base image, OS packages, dependency install) should be `CACHED`.

**某些层被缓存**的构建。在优化良好的 Dockerfile 中，单个 `.py` 文件变更后的增量构建应该只重新执行 `COPY <service-code>` 指令之后的层。其上方的所有内容（基础镜像、OS 包、依赖安装）应为 `CACHED`。

### Layer reuse after a reorder 重排后首次构建的说明

When a Dockerfile's layer order changes (as in PR #2853), **every developer's first build after merging will be a full cold rebuild**. BuildKit sees different layer hashes because the instructions are in a different order. After that one cold build, subsequent incremental builds benefit from the better cache structure.

当 Dockerfile 的层级顺序改变时（如 PR #2853），**合并后每个开发者的第一次构建将是完整的冷构建**。BuildKit 看到不同的层级哈希值，因为指令的顺序不同。经过这次冷构建后，后续的增量构建将受益于更好的缓存结构。

---

## 7. Parallelizing Multi-Image Builds
## 7. 并行化多镜像构建

### The sequential problem 顺序构建的问题

The code-guard project has 5 service images: `main`, `archive_processor`, `results_processor`, `security_scanners`, `security_context_rag`. The original `build-and-bump.sh` script builds them **one by one**:

code-guard 项目有 5 个服务镜像。原始的 `build-and-bump.sh` 脚本**逐个**构建它们：

```
Build main          -> 4 min
Build archive_proc  -> 4 min
Build results_proc  -> 4 min
Build scanners      -> 4 min
Build security_rag  -> 4 min
Total: 20 minutes
```

The images are **independent** — none depends on the output of another. Sequential execution wastes all available CPU and network parallelism.

这些镜像是**相互独立的**——没有一个依赖另一个的输出。顺序执行浪费了所有可用的 CPU 和网络并行能力。

### The parallel solution 并行解决方案

A companion PR in `devsec-infra` adds a `--jobs N` flag to `build-and-bump.sh` that runs builds concurrently using shell job control (or `make -j`). With 5 images and enough CPU:

`devsec-infra` 中的配套 PR 为 `build-and-bump.sh` 添加了 `--jobs N` 标志，使用 shell 作业控制（或 `make -j`）并发运行构建。有 5 个镜像且 CPU 充足时：

```
Build main       \
Build archive     |
Build results     |-> all run in parallel
Build scanners    |
Build security_rag/
Total: ~4 min (dominated by slowest single image)
```

Wall-clock time drops from the sum of all build times to the maximum of any single build time — a 3-5x speedup for cold builds.

挂钟时间从所有构建时间之和降低到任意单个构建时间的最大值——冷构建速度提升 3-5 倍。

### Combined impact of both PRs 两个 PR 的综合效果

| Scenario | Before | After (both PRs) |
|---|---|---|
| Cold build, all images | ~20 min | ~4-5 min |
| Incremental build (1 .py change) | ~20 min | ~30-50 sec |
| `pyproject.toml` change | ~20 min | ~4-5 min |

| 场景 | 之前 | 之后（两个 PR） |
|---|---|---|
| 冷构建，全部镜像 | ~20 分钟 | ~4-5 分钟 |
| 增量构建（1 个 .py 变更） | ~20 分钟 | ~30-50 秒 |
| `pyproject.toml` 变更 | ~20 分钟 | ~4-5 分钟 |

---

## 8. `.dockerignore` and Build Context
## 8. `.dockerignore` 与构建上下文

### What is the build context? 什么是构建上下文？

When `docker build` runs, Docker first sends a **build context** — a directory snapshot — to the buildx daemon. Every file in the current directory (`.`) is included by default. This transfer happens before any layer executes and can be slow for large repos.

当 `docker build` 运行时，Docker 首先将**构建上下文**（目录快照）发送到 buildx 守护进程。默认情况下，当前目录（`.`）中的每个文件都会被包含。这个传输发生在任何层执行之前，对于大型仓库可能很慢。

### `.dockerignore` 的作用

`.dockerignore` works exactly like `.gitignore` but for the build context. Files matching patterns in `.dockerignore` are excluded from the context snapshot before it is sent to the daemon.

`.dockerignore` 的工作原理与 `.gitignore` 完全相同，但针对的是构建上下文。匹配 `.dockerignore` 中模式的文件在发送到守护进程之前会从上下文快照中排除。

```
# .dockerignore example from PR #2853
.git/
tests/
robot_integration_tests/
debug/
bruno_collection/
*.md
uv.lock
.venv/
__pycache__/
*.pyc
.DS_Store
.idea/
.vscode/
```

**Effect:** Build context shrinks from ~75MB to ~30-40MB. Smaller context = faster transfer to the daemon = faster build start. It also prevents accidental `COPY . .` instructions from including test data or secrets.

**效果：** 构建上下文从约 75MB 缩减至约 30-40MB。更小的上下文 = 更快地传输到守护进程 = 更快的构建启动。它还可以防止意外的 `COPY . .` 指令包含测试数据或机密文件。

---

## Key Takeaways 关键要点

- Docker images are stacks of cached layers. A cache miss on any layer re-executes all layers below it.
  Docker 镜像是缓存层的堆栈。任何层的缓存未命中都会重新执行其下方的所有层。

- Layer order is the primary Dockerfile optimization lever. Place slow, rarely-changing steps (dependency installs) before fast, frequently-changing steps (source code copies).
  层级顺序是 Dockerfile 最主要的优化手段。将慢速、不常变更的步骤（依赖安装）放在快速、频繁变更的步骤（源代码复制）之前。

- Copy only the dependency manifest (`pyproject.toml`, `requirements.txt`, `package.json`) before installing. Copy service code after. This ties the install cache key to the manifest, not to the code.
  在安装之前只复制依赖清单文件（`pyproject.toml`、`requirements.txt`、`package.json`）。之后再复制服务代码。这将安装缓存键绑定到清单文件，而不是代码。

- `--mount=type=cache` persists a directory across builds on the same buildx daemon without including it in the final image. Use it for package manager caches (`uv`, `pip`, `npm`, `cargo`).
  `--mount=type=cache` 在同一 buildx 守护进程的多次构建间持久化目录，而不将其包含在最终镜像中。将其用于包管理器缓存（`uv`、`pip`、`npm`、`cargo`）。

- A wheel (`.whl`) is a pre-built Python package archive. Caching it means re-installs skip the network download step entirely.
  Wheel（`.whl`）是预构建的 Python 包归档。缓存它意味着重新安装时完全跳过网络下载步骤。

- Independent images should be built in parallel. Wall-clock time equals the slowest single build, not the sum.
  独立的镜像应并行构建。挂钟时间等于最慢单个构建的时间，而非总和。

- `.dockerignore` reduces build context size and prevents accidental inclusion of large or sensitive files.
  `.dockerignore` 减少构建上下文大小，防止意外包含大文件或敏感文件。

- Reordering layers causes a one-time cold rebuild for everyone. After that single rebuild, all subsequent incremental builds are faster.
  重排层级会导致每个人都进行一次性冷构建。在那次冷构建之后，所有后续的增量构建都更快。

---

## References 参考资料

- Docker BuildKit documentation: cache mounts (`--mount=type=cache`)
- uv documentation: https://docs.astral.sh/uv/
- Python Packaging: pyproject.toml specification (PEP 517, PEP 621)
- BuildKit source: https://github.com/moby/buildkit
- PR #2853: Reorder Dockerfile layers + add .dockerignore for code-guard
