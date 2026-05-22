---
title: "Meow's AI Tool - Langfuse LLM Observability"
date: 2026-05-14 11:11:11 -0400
categories: [51AI, Tool]
tags: [langfuse, llm, observability, tracing, mlops, open-source, prompt-management, evaluation]
math: false
toc: true
---

# Langfuse — LLM Observability Platform

---

## Overview

<font color=OrangeRed>Langfuse</font> is an open-source LLM engineering platform that provides tracing, prompt management, evaluations, and cost tracking for applications built on large language models. Think of it as **APM (Application Performance Monitoring) for LLM apps** — the same way Datadog traces a microservice call graph, Langfuse traces an LLM pipeline call graph.

It was founded in 2023 (YC W23). The cloud-hosted version runs at `cloud.langfuse.com`; the self-hosted version is fully open-source under MIT license.

### Why It Exists — The Core Problem

LLM applications are non-deterministic. Traditional logging (printing prompts to stdout) cannot answer:

- Which prompt version caused a quality regression?
- What is the latency breakdown across a multi-step chain?
- How much did this feature cost in tokens last week?
- Which users are getting the worst outputs?

Langfuse captures the **full execution tree** of an LLM pipeline — inputs, outputs, latency, token counts, cost, model name, and custom metadata — and makes all of it queryable, scoreable, and comparable across time.

---

## Core Data Model 核心数据模型

Langfuse uses a four-level hierarchy. Understanding this hierarchy is the key to using the SDK correctly.

```
Trace
  └── Observation (abstract)
        ├── Span     (non-LLM work: retrieval, tool call, preprocessing)
        └── Generation  (one LLM API call)
```

### Trace

The **top-level container** for one end-to-end user operation — e.g., "answer one user question" or "process one document". A Trace is NOT an LLM call itself.

Key fields:

| Field | Type | Purpose |
|---|---|---|
| `name` | string | Human-readable label (`"doc-qa-pipeline"`) |
| `user_id` | string | Links to a real application user |
| `session_id` | string | Groups traces across a multi-turn conversation |
| `tags` | list[str] | For filtering (`["rag", "v3"]`) |
| `release` | string | Deployment version (`"v2.1.0"`) |
| `input` / `output` | any | Overall request and final response |
| `metadata` | dict | Arbitrary key-value pairs |

### Span

An Observation that represents **non-LLM work** — a vector retrieval step, a tool call, a cache lookup, a preprocessing function. Class: `StatefulSpanClient`.

### Generation

An Observation that represents **exactly one LLM API call**. The richest node type because Langfuse auto-calculates cost from it.

Extra fields beyond Span:

| Field | Purpose |
|---|---|
| `model` | Model identifier (`"gpt-4o"`, `"claude-3-5-sonnet-20241022"`) |
| `model_parameters` | Dict of `temperature`, `max_tokens`, etc. |
| `usage` | `Usage(input=N, output=M)` — token counts |
| `prompt` | Optional link to a managed Langfuse Prompt object |

### Nesting Example — RAG Pipeline

```
Trace: "answer-question"
  Span: "retrieve-context"          ← vector DB search
    Generation: "rerank-llm"        ← optional LLM reranker
  Generation: "final-answer"        ← main chat completion
  Span: "write-to-cache"            ← post-processing
```

Each node captures its own latency and input/output. The UI shows a timing waterfall across all nodes.

---

## Key Features 核心功能

### Tracing

The primary feature. Every trace is stored with full input/output, latency breakdown, and token counts. The UI shows:

- Trace list with search/filter by `user_id`, `session_id`, `name`, `tags`, `metadata.*`, date range, and score value ranges
- Trace detail: tree of spans/generations with timing waterfall
- Full input/output at every node
- Cost breakdown per generation and rollup per trace

### Prompt Management

Langfuse stores prompt templates in a versioned registry. Each prompt has:

- A `name` key (e.g. `"system-prompt-v2"`)
- A prompt body (string or chat messages list)
- A `version` integer (auto-incremented on each push)
- A `label` — the special label `"production"` marks the active version fetched by default

Variables use Mustache syntax: `{{variable_name}}`.

```python
prompt_obj = langfuse.get_prompt("system-prompt-v2")
prompt_text = prompt_obj.compile(user_name="Alice")

# Linking generation to prompt enables per-prompt-version analytics
generation = trace.generation(name="chat", prompt=prompt_obj, ...)
```

When a generation is linked to a prompt object, Langfuse can show per-version quality, latency, and cost metrics — so you can compare prompt v3 vs v4 objectively.

### Evaluations

Evaluations attach a score to a Trace or Generation. They answer: "was this output good?"

**Score schema:**

```python
langfuse.score(
    trace_id="abc-123",
    observation_id="gen-456",   # optional — scope to a specific step
    name="faithfulness",
    value=0.9,                  # float, or string for CATEGORICAL
    comment="All claims verified",
    data_type="NUMERIC",        # "BOOLEAN" or "CATEGORICAL" also valid
)
```

**Three evaluation modes:**

| Mode | How |
|---|---|
| Manual / human annotation | Reviewers score traces in the Langfuse UI annotation queue |
| LLM-as-judge | Configure an eval template + judge model; Langfuse runs it automatically on filtered traces |
| Programmatic | Your own eval logic calls `langfuse.score()` via SDK or REST API |

### Cost Tracking

Langfuse maintains a model cost table (price per 1k input/output tokens) for hundreds of models from OpenAI, Anthropic, Google, Mistral, etc. When a Generation is logged with `model` and `usage`, cost is auto-calculated in USD.

Cost surfaces at:
- Per-generation (raw cost)
- Per-trace rollup (sum of all generations)
- Dashboard: daily/weekly cost charts, cost by model, cost by user, cost by feature

### Datasets

Collections of `(input, expected_output)` pairs for offline regression testing. Workflow:

1. Curate interesting/failing traces from production
2. Add to dataset: `langfuse.create_dataset_item(dataset_name="qa-eval", input=..., expected_output=...)`
3. Run experiments:

```python
dataset = langfuse.get_dataset("qa-eval")
for item in dataset.items:
    with item.observe(run_name="experiment-v2") as trace:
        output = my_pipeline(item.input)
    item.score(name="exact_match", value=1 if output == item.expected_output else 0)
```

4. Compare experiment runs in the UI (score distributions, latency, cost per run)

### User and Session Tracking

- `user_id` — any string; enables per-user cost, error rate, and quality score aggregation
- `session_id` — groups traces; UI shows all turns of a conversation as a unified thread

---

## Python SDK Patterns Python SDK 使用模式

Install:

```bash
pip install langfuse
```

Auth (set once via environment variables):

```bash
export LANGFUSE_PUBLIC_KEY="pk-lf-..."
export LANGFUSE_SECRET_KEY="sk-lf-..."
export LANGFUSE_HOST="https://cloud.langfuse.com"   # or self-hosted URL
```

### Pattern 1 — Manual Low-Level SDK

Most explicit control. Use when you need fine-grained span boundaries.

```python
from langfuse import Langfuse
from langfuse.model import Usage

langfuse = Langfuse()

trace = langfuse.trace(
    name="doc-qa",
    user_id="user-42",
    session_id="session-99",
    tags=["rag", "v3"],
)

# Span for non-LLM work
retrieval_span = trace.span(
    name="vector-retrieval",
    input={"query": "What is Langfuse?"},
)
docs = retrieve(query)
retrieval_span.end(output={"doc_count": len(docs)})

# Generation for LLM call
generation = trace.generation(
    name="final-answer",
    model="gpt-4o",
    model_parameters={"temperature": 0.2},
    input=[{"role": "user", "content": prompt}],
)
response = openai_client.chat.completions.create(...)
generation.end(
    output=response.choices[0].message.content,
    usage=Usage(
        input=response.usage.prompt_tokens,
        output=response.usage.completion_tokens,
    ),
)

langfuse.flush()  # CRITICAL: always flush before process exit
```

### Pattern 2 — `@observe` Decorator

Least code. The call tree of decorated functions maps directly to the Trace → Span tree.

```python
from langfuse.decorators import observe, langfuse_context

@observe()
def retrieve_docs(query: str) -> list[str]:
    # Automatically becomes a Span
    return vector_db.search(query)

@observe()
def generate_answer(docs: list[str], question: str) -> str:
    langfuse_context.update_current_observation(model="gpt-4o")
    return call_llm(docs, question)

@observe()   # top-level call becomes the Trace
def answer_question(question: str) -> str:
    docs = retrieve_docs(question)
    answer = generate_answer(docs, question)
    langfuse_context.update_current_trace(user_id="user-42", session_id="s-99")
    return answer
```

`langfuse_context` key methods:

| Method | Purpose |
|---|---|
| `.update_current_observation(**kwargs)` | Set metadata on the current span/generation |
| `.update_current_trace(**kwargs)` | Set metadata on the root trace |
| `.score_current_trace(name, value)` | Attach a score inline |

### Pattern 3 — OpenAI Drop-in Replacement

Zero code change for OpenAI calls. Just swap the import.

```python
from langfuse.openai import openai   # NOT: import openai

client = openai.OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
    # Langfuse-specific kwargs (all optional):
    name="my-generation",
    trace_id="abc-123",        # attach to an existing trace
    session_id="session-99",
    user_id="user-42",
    tags=["feature-x"],
)
# Generation is automatically created with input, output, model, usage, cost
```

### Pattern 4 — LangChain CallbackHandler

```python
from langfuse.callback import CallbackHandler

handler = CallbackHandler(
    public_key="pk-lf-...",
    secret_key="sk-lf-...",
    trace_name="langchain-run",
    user_id="user-42",
    session_id="session-99",
)

chain.invoke({"input": "..."}, config={"callbacks": [handler]})
```

Intercepts LangChain's `on_llm_start`, `on_llm_end`, `on_chain_start`, etc. and maps them to Langfuse spans/generations automatically.

---

## Key SDK Concepts 重要概念

### `flush()` — Why It Matters

Langfuse uses an **async background queue** to batch and send events. This avoids adding latency to LLM calls. The consequence: if the process exits before the queue drains, **events are silently lost**.

Rules:
- Always call `langfuse.flush()` before process exit
- Use a `try/finally` block when instrumenting handlers
- In serverless (AWS Lambda, Cloud Functions): call flush at the end of every handler invocation
- The `@observe` decorator does NOT auto-flush — caller is responsible

### Public Key vs Secret Key

| Key | Prefix | Safe in frontend? | Capabilities |
|---|---|---|---|
| Public key | `pk-lf-...` | Yes | Ingest traces only; cannot read data |
| Secret key | `sk-lf-...` | No — server-side only | Full read + write: fetch prompts, retrieve datasets, call scores API |

The SDK uses both: public key for ingestion, secret key for read operations.

---

## Deployment: Cloud vs Self-Hosted 云端 vs 自托管

### Cloud (cloud.langfuse.com)

Managed SaaS, hosted in EU. Free tier available. Paid plans add higher ingestion limits, SSO, and SLA. Data leaves your environment — not suitable for environments with strict data residency requirements.

### Self-Hosted Stack

```
Langfuse Server (Next.js)  ← web app + REST API
PostgreSQL                  ← primary datastore
ClickHouse (recommended)    ← analytics queries at scale
S3-compatible store         ← large payloads, media
Redis                       ← queue + cache
```

Minimum viable: Docker Compose with Langfuse Server + PostgreSQL only (ClickHouse optional for low volume).

ClickHouse becomes required at production scale because PostgreSQL cannot handle the analytical query patterns (GROUP BY model, time-series rollups) at high ingestion volume.

**Key env vars for self-hosted:**

```bash
DATABASE_URL=postgresql://user:pass@host:5432/langfuse
NEXTAUTH_SECRET=<random-32-char>
NEXTAUTH_URL=https://your-langfuse.example.com
SALT=<random>
```

Data residency: self-hosted means all trace data stays within your infrastructure — required for HIPAA, regulated finance, or any env where prompt content contains PII.

---

## Security Relevance 安全相关性

### Audit Trail

Every LLM call is logged with full input, output, timestamp, user ID, and session ID. This is a **compliance artifact**: you can answer "who asked what, when, and what did the model say?" — essential for GDPR data subject requests, internal audit, and incident response.

The raw input/output is immutable once written (append-only). Scores and metadata can be updated.

### Prompt Injection Detection

Langfuse enables detection pipelines for <font color=OrangeRed>LLM01: Prompt Injection</font> (OWASP LLM Top 10):

1. Log all user inputs as trace inputs
2. Run a model-based evaluator (LLM-as-judge) that checks inputs for injection patterns
3. Write a score `prompt_injection` with value 0 or 1
4. Alert or quarantine traces where `prompt_injection == 1`

Langfuse does not detect injection itself — it provides the infrastructure to operationalize a detection pipeline you build.

### Cost Runaway Prevention

Uncontrolled LLM API spend is an operational risk. Langfuse provides:
- Real-time cost per trace (visible immediately in the UI)
- Daily/weekly cost charts on the dashboard
- Per-user cost breakdown (identify which users or features drive spend)
- Cost alerts can be built on top of the API: `GET /api/public/metrics/usage`

Langfuse does not block or rate-limit LLM calls based on cost — that is done at the API gateway layer. Langfuse provides the visibility to make those decisions.

### Key Management Best Practices

- Never commit `LANGFUSE_SECRET_KEY` to source control — it grants full read access to all traces, including prompt inputs that may contain PII
- Use separate Langfuse projects (each with their own key pair) for production vs staging
- The public key alone cannot read trace data — safe in client-side contexts

---

## Comparison: Langfuse vs Alternatives

| Dimension | Langfuse | LangSmith | Helicone | Arize Phoenix |
|---|---|---|---|---|
| **License** | MIT (open source) | Proprietary | Proprietary | Apache 2.0 |
| **Self-host** | Yes, full stack | Enterprise only | No | Yes |
| **Prompt management** | Yes (versioned + labeled) | Yes | No | No |
| **Datasets & evals** | Yes (built-in runner) | Yes | Limited | Yes (strong) |
| **LangChain native** | CallbackHandler | Native (same company) | Via proxy | CallbackHandler |
| **Cost tracking** | Yes (auto, model table) | Yes | Yes (proxy-based) | Partial |
| **OTEL compatibility** | Partial | No | No | Yes (first-class) |
| **LLM-as-judge evals** | Yes (built-in templates) | Yes | No | Yes |
| **Pricing model** | Events-based | Events-based | Requests-based | Seats-based |

**When to use Langfuse over LangSmith:** self-hosting requirement, not using LangChain, or needing MIT license flexibility.

**When to use Helicone:** you want zero-code tracing via a proxy and don't need evaluations.

**When to use Arize Phoenix:** already using OpenTelemetry, need deep MLOps model performance evaluation, or want OTEL-native spans.

---

## Key Takeaways

- Langfuse is APM for LLM apps — traces, spans, generations form a call tree just like distributed tracing in microservices
- The hierarchy is: Trace (one user operation) → Span (non-LLM step) → Generation (one LLM call)
- `flush()` is non-optional — forget it and you lose events silently
- Two keys: public key for ingestion (safe anywhere), secret key for reads (server-side only)
- Self-hosted under MIT license — full data residency control, suitable for regulated environments
- Security value: audit trail for compliance, infrastructure for prompt injection detection pipelines, cost visibility to prevent runaway spend
- Closest competitor is LangSmith; Langfuse wins on self-hosting and licensing

## References

- Langfuse docs: `langfuse.com/docs`
- Python SDK: `github.com/langfuse/langfuse-python`
- OWASP LLM Top 10: `owasp.org/www-project-top-10-for-large-language-model-applications`
- Related wiki: [[AI/LLM]], [[RAG]], [[SecConcepts/OWASP]]
