---
title: "Meow's CodeNote - SQLite Locking and SQLITE_BUSY / SQLite 锁机制与 SQLITE_BUSY 详解"
date: 2026-06-17 11:11:11 -0400
categories: [00CodeNote, SQL]
tags: [SQLite, concurrency, locking, SQLITE_BUSY, WAL, database, Python]
math: false
toc: true
image: ""
---

# SQLite Locking and SQLITE_BUSY / SQLite 锁机制与 SQLITE_BUSY 详解

---

## Overview 概述

SQLite 是一个嵌入式数据库，采用文件级别的锁机制来保证数据一致性。与 PostgreSQL 或 MySQL 不同，SQLite 的并发模型极为简单：同一时刻只允许一个写入者，这导致在多进程或多线程场景下容易出现 `SQLITE_BUSY`（错误码 5）或 `database is locked` 错误。

SQLite is an embedded database that uses file-level locking to guarantee data consistency. Unlike PostgreSQL or MySQL, SQLite has a very simple concurrency model: only one writer is allowed at a time. This leads to `SQLITE_BUSY` (error code 5) or `database is locked` errors in multi-process or multi-threaded scenarios.

理解 SQLite 的锁机制是排查这类错误、设计稳健应用的基础。本文从零开始，逐层深入讲解锁状态、错误类型、日志模式、WAL 模式及解决方案。

Understanding SQLite's locking model is the foundation for diagnosing these errors and designing resilient applications. This note builds from zero, covering lock states, error types, journal modes, WAL mode, and solutions in increasing depth.

---

## Part 1: The Mental Model 思维模型（入门）

### 图书馆类比 Library Analogy

把 SQLite 数据库想象成一座只有一本书的图书馆：

Think of a SQLite database as a library with only one copy of a book:

- **多人可以同时阅读** — 只读操作可以并发执行 / Multiple readers can read simultaneously — read-only operations are concurrent
- **只有一人可以写字** — 写入操作是独占的 / Only one writer can write — write operations are exclusive
- **有人在写字时，没有人能阅读** — 默认模式下，写入会阻塞所有读取 / While someone is writing, nobody can read — in default mode, writes block all reads
- **WAL 模式打破了最后一条规则** — 见 Part 4 / WAL mode breaks the last rule — see Part 4

### 为什么 SQLite 是这样设计的 Why SQLite Works This Way

SQLite 的设计目标是嵌入式场景：移动应用、桌面软件、单用户工具。它把整个数据库存储在一个文件里，通过操作系统的文件锁来实现并发控制，无需单独的服务进程。这种设计在单进程场景下非常高效，但在多进程并发写入时会产生锁竞争。

SQLite is designed for embedded scenarios: mobile apps, desktop software, single-user tools. It stores the entire database in one file and uses OS-level file locks for concurrency control, with no separate server process. This is highly efficient for single-process use, but creates lock contention when multiple processes write concurrently.

---

## Part 2: The Five Lock States 五种锁状态（核心概念）

SQLite 在内部维护一个精确的锁状态机。每个数据库连接在任意时刻处于以下五种状态之一：

SQLite maintains a precise lock state machine internally. Each database connection is in one of five states at any moment:

| 状态 State | 编号 | 含义 Meaning |
|---|---|---|
| `UNLOCKED` | 0 | 无锁，默认状态 / No lock held, default state |
| `SHARED` | 1 | 共享读锁，多连接可同时持有 / Shared read lock, multiple connections can hold simultaneously |
| `RESERVED` | 2 | 预留写锁，表达写入意图 / Reserved lock, signals intent to write |
| `PENDING` | 3 | 等待排他锁，不再接受新的共享锁 / Pending exclusive lock, no new shared locks accepted |
| `EXCLUSIVE` | 4 | 排他写锁，独占数据库 / Exclusive write lock, full ownership |

### 锁升级路径 Lock Escalation Path

```
UNLOCKED
  → SHARED      (开始读取 / begin read)
    → RESERVED  (开始写入事务 / begin write transaction)
      → PENDING (等待读取者离开 / waiting for readers to finish)
        → EXCLUSIVE (完成写入 / ready to write)
```

### 每种状态详解 State Details

**UNLOCKED** — 连接存在但不持有任何锁。数据库文件可被其他连接自由访问。
The connection exists but holds no lock. The database file is freely accessible to other connections.

**SHARED** — 执行 `SELECT` 时获取。多个连接可同时持有 SHARED 锁，因为并发读取是安全的。
Acquired when executing `SELECT`. Multiple connections can hold SHARED locks simultaneously since concurrent reads are safe.

**RESERVED** — 执行 `BEGIN` 或第一次 `INSERT`/`UPDATE`/`DELETE` 时获取。此时持有 SHARED 锁的其他连接仍可继续读取。每个数据库文件同一时刻只允许一个 RESERVED 锁存在。
Acquired on `BEGIN` or the first write statement. Other connections holding SHARED locks can still read. Only one RESERVED lock per database file is allowed at a time.

**PENDING** — 当连接准备提交，需要升级为 EXCLUSIVE 时进入此状态。SQLite 停止向其他连接发放新的 SHARED 锁，但等待已有的 SHARED 锁释放。
Entered when the connection is ready to commit and needs to escalate to EXCLUSIVE. SQLite stops issuing new SHARED locks to others, but waits for existing SHARED locks to be released.

**EXCLUSIVE** — 数据库完全独占，其他连接不能持有任何锁。这是实际写入磁盘的阶段。
The database is fully owned. No other connection can hold any lock. This is when actual disk writes happen.

---

## Part 3: SQLITE_BUSY vs SQLITE_LOCKED 两种不同的错误

### 错误码对比 Error Code Comparison

| 错误 Error | 错误码 Code | 触发场景 Trigger |
|---|---|---|
| `SQLITE_BUSY` | 5 | **跨进程**锁冲突 / Cross-process lock conflict |
| `SQLITE_LOCKED` | 6 | **同进程**内锁冲突（共享缓存模式） / Intra-process conflict (shared cache mode) |

### SQLITE_BUSY — 跨进程锁冲突

`SQLITE_BUSY` 表示另一个**操作系统进程**（或线程，取决于编译选项）持有冲突锁，导致当前操作无法立即获取所需的锁。

`SQLITE_BUSY` means another **OS process** (or thread, depending on compile options) holds a conflicting lock, preventing the current operation from acquiring the needed lock immediately.

**常见场景 Common Scenarios:**

- 进程 A 正在写入，进程 B 试图写入 / Process A is writing, Process B tries to write
- 进程 A 正在写入（持有 EXCLUSIVE），进程 B 试图读取 / Process A is writing (EXCLUSIVE), Process B tries to read
- 备份工具（如 `sqlite3 .backup`）持有锁时，应用试图写入 / A backup tool holds a lock while the app tries to write

**Python 中的表现 In Python:**

```python
import sqlite3

conn = sqlite3.connect("app.db")
try:
    conn.execute("INSERT INTO events VALUES (1, 'click')")
    conn.commit()
except sqlite3.OperationalError as e:
    # e.args[0] == "database is locked"
    print(f"Caught: {e}")
```

### SQLITE_LOCKED — 同进程内锁冲突

`SQLITE_LOCKED` 通常发生在同一进程内，当使用**共享缓存模式**（shared cache）时，同一进程内的多个连接共享页缓存，如果一个连接持有表级锁，另一个连接试图访问同一张表就会触发此错误。

`SQLITE_LOCKED` occurs within the same process, typically in **shared cache mode**, where multiple connections in the same process share a page cache. If one connection holds a table-level lock, another connection attempting to access the same table triggers this error.

```python
import sqlite3

# 共享缓存模式示例 / Shared cache mode example
conn1 = sqlite3.connect("file:app.db?cache=shared", uri=True)
conn2 = sqlite3.connect("file:app.db?cache=shared", uri=True)

conn1.execute("BEGIN EXCLUSIVE")
try:
    conn2.execute("SELECT * FROM users")  # raises sqlite3.OperationalError: database is locked
except sqlite3.OperationalError as e:
    print(f"SQLITE_LOCKED: {e}")
```

---

## Part 4: Journal Mode vs WAL Mode 日志模式 vs WAL 模式

理解两种持久化模式是解决锁争用的关键。

Understanding the two persistence modes is the key to solving lock contention.

### 默认日志模式（Rollback Journal）默认 Default Mode

默认情况下，SQLite 使用 **DELETE 日志模式**（也叫 rollback journal）：

By default, SQLite uses **DELETE journal mode** (also called rollback journal):

```
写入流程 Write Flow:
1. 获取 RESERVED 锁 / Acquire RESERVED lock
2. 将原始页面复制到 <db>.db-journal 文件 / Copy original pages to <db>.db-journal
3. 在数据库文件中修改页面 / Modify pages in database file
4. 升级到 EXCLUSIVE 锁（阻塞所有读取者！）/ Escalate to EXCLUSIVE (blocks ALL readers!)
5. 提交：删除 journal 文件 / Commit: delete journal file
6. 释放锁 / Release lock
```

**问题 Problem:** 步骤 4 升级到 EXCLUSIVE 锁时，所有持有 SHARED 锁的读取者必须等待锁释放，这会导致读取者看到 `SQLITE_BUSY`。

At step 4, escalating to EXCLUSIVE forces all readers holding SHARED locks to wait, causing them to see `SQLITE_BUSY`.

### WAL 模式（Write-Ahead Logging）

WAL 模式彻底改变了并发模型：

WAL mode fundamentally changes the concurrency model:

```
WAL 写入流程 WAL Write Flow:
1. 写入者将修改的页面追加到 <db>.db-wal 文件（不修改主数据库文件）
   Writer appends modified pages to <db>.db-wal (does NOT modify the main db file)
2. 写入者只需要一个较弱的 WAL 写锁，不阻塞读取者
   Writer holds only a weak WAL write lock, does NOT block readers
3. 读取者从主数据库文件读取，加上 WAL 中已提交的页面
   Readers read from main db file plus committed pages in WAL
4. Checkpoint（检查点）：定期将 WAL 合并回主数据库文件
   Checkpoint: periodically merges WAL back into the main database file
```

**WAL 模式的核心优势 Key Advantage:**

- 读取者和写入者可以**同时运行** / Readers and writers can **run concurrently**
- 读取者永远不会被写入者阻塞 / Readers are never blocked by writers
- 写入者等待的情况大幅减少 / Writer waits are significantly reduced

**启用 WAL 模式 Enable WAL Mode:**

```python
import sqlite3

conn = sqlite3.connect("app.db")
conn.execute("PRAGMA journal_mode=WAL")
conn.commit()
# 验证 / Verify
result = conn.execute("PRAGMA journal_mode").fetchone()
print(result)  # ('wal',)
```

```bash
# 或通过命令行 / or via CLI
sqlite3 app.db "PRAGMA journal_mode=WAL;"
```

**WAL 模式的注意事项 WAL Caveats:**

- WAL 模式不支持网络文件系统（NFS、SMB）/ WAL mode does not work on network filesystems (NFS, SMB)
- 会产生三个文件：`app.db`、`app.db-wal`、`app.db-shm` / Produces three files: `app.db`, `app.db-wal`, `app.db-shm`
- 仍然只允许一个写入者 / Still only one writer at a time

### 模式对比 Mode Comparison

| 特性 Feature | 默认 Journal 模式 | WAL 模式 |
|---|---|---|
| 并发读取 Concurrent reads | 是 Yes | 是 Yes |
| 读写并发 Read-write concurrent | 否 No | 是 Yes |
| 并发写入 Concurrent writes | 否 No | 否 No |
| 网络文件系统支持 NFS support | 是 Yes | 否 No |
| 文件数量 File count | 1-2 | 3 |
| 崩溃恢复 Crash recovery | 快 Fast | 稍慢 Slightly slower |

---

## Part 5: Practical Scenarios and Solutions 实战场景与解决方案

### 场景 1：多进程写入争用 Multi-Process Write Contention

**场景描述 Scenario:**
一个 Web 服务器（多个 worker 进程）同时写入 SQLite。

A web server with multiple worker processes writing to SQLite simultaneously.

**复现代码 Reproduction:**

```python
# process_a.py
import sqlite3, time

conn = sqlite3.connect("shared.db")
conn.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, msg TEXT)")
conn.execute("BEGIN")
conn.execute("INSERT INTO logs (msg) VALUES ('long transaction')")
time.sleep(5)  # 模拟慢操作 / simulate slow operation
conn.commit()
conn.close()
```

```python
# process_b.py — run while process_a.py is sleeping
import sqlite3

conn = sqlite3.connect("shared.db")
try:
    conn.execute("INSERT INTO logs (msg) VALUES ('fast insert')")
    conn.commit()
except sqlite3.OperationalError as e:
    print(f"Error: {e}")  # database is locked
conn.close()
```

**解决方案 Solution — busy_timeout:**

```python
import sqlite3

conn = sqlite3.connect("shared.db", timeout=10)  # wait up to 10 seconds
# or equivalently:
conn = sqlite3.connect("shared.db")
conn.execute("PRAGMA busy_timeout = 10000")  # 10000 milliseconds

conn.execute("INSERT INTO logs (msg) VALUES ('retried insert')")
conn.commit()
```

`busy_timeout` 告诉 SQLite：如果遇到锁，先等待指定毫秒数，期间不断重试，超时后才返回 `SQLITE_BUSY`。

`busy_timeout` tells SQLite: if a lock is encountered, wait up to the specified milliseconds, retrying continuously, and only return `SQLITE_BUSY` after timeout.

### 场景 2：多线程应用 Multi-Threaded Application

**场景描述 Scenario:**
Python 应用使用线程池并发写入同一 SQLite 数据库。

A Python app uses a thread pool to write concurrently to the same SQLite database.

**问题代码 Problematic Code:**

```python
import sqlite3
import threading

# 错误：每个线程创建独立连接，没有协调 / Wrong: each thread creates its own connection, no coordination
def worker(thread_id):
    conn = sqlite3.connect("app.db")
    conn.execute(f"INSERT INTO tasks VALUES ({thread_id}, 'done')")
    conn.commit()
    conn.close()

threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

**推荐方案 Recommended Solution — Single Connection with Lock:**

```python
import sqlite3
import threading

# 方案 A：使用单一连接 + 线程锁 / Option A: single connection + thread lock
db_lock = threading.Lock()
conn = sqlite3.connect("app.db", check_same_thread=False)

def worker(thread_id):
    with db_lock:
        conn.execute(f"INSERT INTO tasks VALUES ({thread_id}, 'done')")
        conn.commit()

threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

```python
# 方案 B：WAL 模式 + busy_timeout / Option B: WAL mode + busy_timeout
import sqlite3

def get_conn():
    conn = sqlite3.connect("app.db", timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn
```

### 场景 3：长事务导致锁持有 Long Transactions Holding Locks

**场景描述 Scenario:**
一个事务内部包含网络请求或用户交互，导致锁被长时间持有。

A transaction contains a network request or user interaction, causing the lock to be held for a long time.

**问题代码 Problematic Code:**

```python
import sqlite3, requests

conn = sqlite3.connect("app.db")
conn.execute("BEGIN")
conn.execute("UPDATE jobs SET status='running' WHERE id=1")

# 锁在这里被持有！/ Lock is held here!
response = requests.get("https://external-api.example.com/process")  # could take seconds

conn.execute(f"UPDATE jobs SET result='{response.text}' WHERE id=1")
conn.commit()
```

**修复方案 Fix:**

```python
import sqlite3, requests

# 在事务外执行慢操作 / Perform slow operations outside the transaction
response = requests.get("https://external-api.example.com/process")

conn = sqlite3.connect("app.db")
# 锁持有时间极短 / Lock held for minimal time
with conn:  # auto commit/rollback context manager
    conn.execute("UPDATE jobs SET status='done', result=? WHERE id=1", (response.text,))
```

### 场景 4：Django / Flask 中的 SQLite 锁 Web Framework SQLite Locks

**场景描述 Scenario:**
Django 开发环境使用 SQLite，部署了多个 Gunicorn worker，发生锁争用。

Django development environment uses SQLite with multiple Gunicorn workers, causing lock contention.

**Django 配置推荐 Django Config:**

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,         # busy_timeout in seconds
            'init_command': 'PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL;',
        },
    }
}
```

**重要提示 Important Note:**
SQLite 不适合多 worker 的生产部署。多进程写入场景应迁移到 PostgreSQL 或 MySQL。

SQLite is not suitable for multi-worker production deployments. Migrate to PostgreSQL or MySQL for multi-process write scenarios.

### 场景 5：带重试的指数退避 Exponential Backoff Retry

**场景描述 Scenario:**
需要在代码层实现细粒度的重试逻辑，而不依赖 `busy_timeout`。

Fine-grained retry logic in code, not relying on `busy_timeout`.

```python
import sqlite3
import time
import random

def execute_with_retry(conn, sql, params=(), max_retries=5, base_delay=0.1):
    """Execute SQL with exponential backoff on SQLITE_BUSY."""
    for attempt in range(max_retries):
        try:
            conn.execute(sql, params)
            conn.commit()
            return
        except sqlite3.OperationalError as e:
            if "database is locked" not in str(e):
                raise
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt) + random.uniform(0, 0.1)
            time.sleep(delay)

# 使用 / Usage
conn = sqlite3.connect("app.db")
execute_with_retry(conn, "INSERT INTO events (name) VALUES (?)", ("click",))
```

---

## Part 6: Advanced Topics 进阶主题

### WAL 检查点机制 WAL Checkpoint

WAL 文件随写入不断增长。SQLite 会自动触发检查点（默认阈值：1000 页），将 WAL 中的数据合并回主数据库文件。

The WAL file grows as writes accumulate. SQLite automatically triggers a checkpoint (default threshold: 1000 pages) to merge WAL data back into the main database file.

```python
# 手动触发检查点 / Manually trigger checkpoint
conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")

# 配置自动检查点阈值 / Configure auto-checkpoint threshold
conn.execute("PRAGMA wal_autocheckpoint=2000")  # trigger at 2000 pages
```

**检查点类型 Checkpoint Types:**

| 类型 Type | 行为 Behavior |
|---|---|
| `PASSIVE` | 不阻塞任何连接，尽力合并 / Non-blocking, best-effort merge |
| `FULL` | 等待读取者完成，再合并 / Waits for readers, then merges |
| `RESTART` | 合并后重置 WAL 写入位置 / Merges and resets WAL write position |
| `TRUNCATE` | 合并后截断 WAL 文件为零字节 / Merges and truncates WAL to zero bytes |

### PRAGMA 调优参数 PRAGMA Tuning Parameters

```python
import sqlite3

conn = sqlite3.connect("app.db")

# 核心调优 / Core tuning
conn.execute("PRAGMA journal_mode=WAL")       # 启用 WAL / enable WAL
conn.execute("PRAGMA synchronous=NORMAL")     # 性能与安全的平衡 / balance between perf and safety
conn.execute("PRAGMA busy_timeout=30000")     # 30 秒超时 / 30 second timeout
conn.execute("PRAGMA cache_size=-64000")      # 64 MB 页缓存 / 64 MB page cache
conn.execute("PRAGMA temp_store=MEMORY")      # 临时表存内存 / temp tables in memory
conn.execute("PRAGMA mmap_size=268435456")    # 256 MB 内存映射 / 256 MB memory-mapped I/O
```

### 共享缓存模式 Shared Cache Mode

共享缓存模式（`SQLITE_OPEN_SHAREDCACHE`）允许同一进程内多个连接共享页缓存，减少内存占用，但引入了表级锁，增加了 `SQLITE_LOCKED` 的风险。官方文档不推荐在新代码中使用。

Shared cache mode allows multiple connections within the same process to share a page cache, reducing memory usage, but introduces table-level locks and increases `SQLITE_LOCKED` risk. The official documentation discourages use in new code.

```python
# 不推荐 / Not recommended for new code
conn = sqlite3.connect("file:app.db?cache=shared", uri=True)
```

### 事务类型 Transaction Types

SQLite 支持三种显式事务类型，控制初始锁的获取策略：

SQLite supports three explicit transaction types controlling initial lock acquisition strategy:

```python
# DEFERRED（默认）: 延迟获取锁，直到第一次读写操作
# DEFERRED (default): defers lock acquisition until first read/write
conn.execute("BEGIN DEFERRED")

# IMMEDIATE: 立即获取 RESERVED 锁，阻止其他写入者
# IMMEDIATE: acquires RESERVED lock immediately, blocks other writers
conn.execute("BEGIN IMMEDIATE")

# EXCLUSIVE: 立即获取 EXCLUSIVE 锁，阻止所有其他连接
# EXCLUSIVE: acquires EXCLUSIVE lock immediately, blocks all other connections
conn.execute("BEGIN EXCLUSIVE")
```

| 事务类型 | 初始锁 | 适用场景 Use Case |
|---|---|---|
| `DEFERRED` | 无 None | 大多数读写混合场景 / Mixed read-write workloads |
| `IMMEDIATE` | RESERVED | 预期会写入，想减少升级冲突 / Expect writes, reduce upgrade conflicts |
| `EXCLUSIVE` | EXCLUSIVE | 需要独占访问，如批量迁移 / Need exclusive access, e.g., bulk migration |

### 诊断工具 Diagnostic Tools

```bash
# 查看数据库当前锁状态 / Check current lock state
sqlite3 app.db "PRAGMA locking_mode;"

# 查看 WAL 文件状态 / Check WAL file status
sqlite3 app.db "PRAGMA wal_checkpoint;"

# 查看当前 journal 模式 / Check current journal mode
sqlite3 app.db "PRAGMA journal_mode;"

# 查看 busy_timeout 设置 / Check busy_timeout setting
sqlite3 app.db "PRAGMA busy_timeout;"
```

```python
# Python: 检查数据库完整性 / Python: check database integrity
import sqlite3

conn = sqlite3.connect("app.db")
result = conn.execute("PRAGMA integrity_check").fetchone()
print(result)  # ('ok',) if no corruption
```

---

## Part 7: Decision Flowchart 决策流程图

```
遇到 "database is locked" 错误？
Encountered "database is locked" error?
         |
         v
  是单进程还是多进程？
  Single process or multi-process?
    /           \
单进程            多进程
Single           Multi-process
   |                 |
   v                 v
是多线程吗？       启用 WAL 模式
Multi-threaded?   Enable WAL mode
  /      \             |
是 Yes    否 No         v
 |         |      设置 busy_timeout >= 5000ms
 v         v      Set busy_timeout >= 5000ms
使用单一    使用      |
连接+线程锁  WAL模式   v
Single conn 即可    写入量大吗？
+ thread lock WAL  High write volume?
             is fine  /       \
                    是 Yes    否 No
                     |         |
                     v         v
                 考虑迁移到  SQLite WAL
                 PostgreSQL  足够了
                 Consider    SQLite WAL
                 migrating   is sufficient
                 to Postgres
```

---

## Key Takeaways 关键要点

- SQLite 使用五级锁状态机（UNLOCKED → SHARED → RESERVED → PENDING → EXCLUSIVE）控制并发访问 / SQLite uses a five-level lock state machine to control concurrent access
- `SQLITE_BUSY`（错误码 5）= 跨进程锁冲突；`SQLITE_LOCKED`（错误码 6）= 同进程内锁冲突 / `SQLITE_BUSY` = cross-process conflict; `SQLITE_LOCKED` = intra-process conflict
- 默认 Journal 模式：写入时阻塞所有读取者；WAL 模式：读写可以并发 / Default Journal mode blocks all readers during writes; WAL mode allows concurrent reads and writes
- `PRAGMA busy_timeout=N` 是解决 `SQLITE_BUSY` 最简单的第一步 / `PRAGMA busy_timeout=N` is the simplest first step to resolve `SQLITE_BUSY`
- 保持事务短小，不要在事务内执行 I/O 或等待操作 / Keep transactions short; never perform I/O or wait operations inside a transaction
- 多进程写入密集场景下，SQLite 不是正确的工具；应迁移至 PostgreSQL / For multi-process write-heavy workloads, SQLite is not the right tool; migrate to PostgreSQL
- `BEGIN IMMEDIATE` 比 `BEGIN DEFERRED` 更能减少写入时的锁升级冲突 / `BEGIN IMMEDIATE` reduces lock escalation conflicts compared to `BEGIN DEFERRED`

---

## References 参考资料

- [SQLite Locking and Concurrency](https://www.sqlite.org/lockingv3.html) — official spec
- [SQLite WAL Mode](https://www.sqlite.org/wal.html) — official WAL documentation
- [SQLite Shared Cache Mode](https://www.sqlite.org/sharedcache.html)
- [SQLite PRAGMA Reference](https://www.sqlite.org/pragma.html)
- [Python sqlite3 module docs](https://docs.python.org/3/library/sqlite3.html)
