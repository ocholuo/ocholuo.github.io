---
title: "Meow's AIML - MCP Deployment"
date: 2021-08-11 11:11:11 -0400
description:
categories: [51AI, AIML]
img: /assets/img/sample/rabbit.png
tags: [AI, ML, MCP, protocol, LLM, agent, deployment, FastMCP, Python, Docker, AWS, serverless]
toc: true
---

# MCP Deployment

- [MCP Deployment](#mcp-deployment)
  - [Overview 概述](#overview-概述)
  - [Prerequisites 准备工作](#prerequisites-准备工作)
  - [Core Concepts 核心概念](#core-concepts-核心概念)
  - [Project Setup 项目搭建](#project-setup-项目搭建)
  - [FastMCP Quick Start 快速开始](#fastmcp-quick-start-快速开始)
    - [Define a Tool — @mcp.tool()](#define-a-tool--mcptool)
    - [Define a Resource — @mcp.resource()](#define-a-resource--mcpresource)
    - [Define a Prompt — @mcp.prompt()](#define-a-prompt--mcpprompt)
    - [Run the Server](#run-the-server)
  - [Traditional SDK: Resources and Tools](#traditional-sdk-resources-and-tools)
    - [Defining Resources](#defining-resources)
    - [Defining Tools](#defining-tools)
    - [Error Handling and Validation](#error-handling-and-validation)
  - [Debugging with MCP Inspector 调试工具](#debugging-with-mcp-inspector-调试工具)
  - [Client Development 客户端开发](#client-development-客户端开发)
    - [stdio Client](#stdio-client)
    - [SSE Client](#sse-client)
    - [Client with DeepSeek LLM](#client-with-deepseek-llm)
  - [Claude Desktop Configuration](#claude-desktop-configuration)
  - [Cline and Cursor Configuration](#cline-and-cursor-configuration)
  - [Sampling Callback 采样回调](#sampling-callback-采样回调)
  - [Advanced Features 高级特性](#advanced-features-高级特性)
    - [Lifecycle Management 生命周期管理](#lifecycle-management-生命周期管理)
    - [Prompt Primitives](#prompt-primitives)
    - [Resource Primitives](#resource-primitives)
  - [LangChain Integration LangChain 集成](#langchain-integration-langchain-集成)
  - [Remote Deployment 远程部署](#remote-deployment-远程部署)
    - [SSE Transport SSE 传输模式](#sse-transport-sse-传输模式)
    - [Docker Deployment](#docker-deployment)
    - [AWS Deployment (Lambda + ECS)](#aws-deployment-lambda--ecs)
    - [Aliyun Serverless 阿里云函数计算部署](#aliyun-serverless-阿里云函数计算部署)
  - [Security Best Practices 安全最佳实践](#security-best-practices-安全最佳实践)
  - [Key Takeaways](#key-takeaways)
  - [References](#references)

ref:
- [How to Build an MCP Server: A Step-by-Step Guide with Code Examples](https://blog.openreplay.com/how-to-build-an-mcp-server/)
- [5分钟上手MCP](https://mp.weixin.qq.com/s/ZFZ-MCP-tutorial)
- [MCP 编程极速上手](https://mp.weixin.qq.com/s/MCP-quick-start)

---

## Overview 概述

<font color=OrangeRed>MCP (Model Context Protocol)</font> is an open standard that lets AI models communicate with external tools, data sources, and services in a structured, secure way. Building an MCP server allows you to expose resources (readable data) and tools (callable actions) to any compliant LLM client — Claude, Cursor, Cline, or a custom agent.

This note covers the full lifecycle from local development to production deployment:

- Setting up a Python MCP server project (traditional SDK or FastMCP)
- Defining resources, tools, and prompts
- Debugging with MCP Inspector
- Writing MCP clients and connecting real LLMs
- Deploying via Docker, AWS Lambda/ECS, and Aliyun Serverless (FC 3.0)

---

## Prerequisites 准备工作

| Requirement | Notes |
|---|---|
| Python 3.8+ | 3.10+ recommended |
| MCP Python SDK | `pip install mcp` or `pip install fastmcp` |
| MCP Inspector | `npx @modelcontextprotocol/inspector` |
| Git | Version control |
| Docker | For containerized deployment |
| Node.js 16+ | For Inspector and some clients |

---

## Core Concepts 核心概念

An MCP system has three roles:

| Role | Responsibility |
|---|---|
| **Server** | Exposes resources and tools to LLMs |
| **Client** | Connects an LLM to one or more servers |
| **Protocol** | Governs message framing between client and server |

Three primitive types that a server can expose:

- <font color=OrangeRed>**Resource**</font> — Static or dynamic data the LLM can read (files, DB rows, API results)
- <font color=OrangeRed>**Tool**</font> — Callable functions the LLM can invoke to take actions
- <font color=OrangeRed>**Prompt**</font> — Reusable instruction templates the LLM can request

Communication flow:

```
LLM (via Client)
  → request resource or call tool
  → Server processes and returns standardized response
  → LLM uses result in its reasoning
```

Two transport modes:

| Transport | Use case |
|---|---|
| `stdio` | Local tools, CLI, desktop apps — subprocess communication |
| `SSE` (HTTP) | Remote servers, web services, multi-user environments |

---

## Project Setup 项目搭建

```bash
mkdir my_mcp_server
cd my_mcp_server

# Create virtual environment (use pyenv)
pyenv virtualenv 3.11.4 mcp-server-env
pyenv local mcp-server-env

# Project structure
mkdir -p src/resources src/tools tests
touch src/__init__.py src/resources/__init__.py src/tools/__init__.py
touch requirements.txt README.md
```

`requirements.txt`:

```
mcp>=1.0.0
fastmcp>=0.1.0
pydantic>=2.0.0
pytest>=7.0.0
httpx>=0.27.0
```

```bash
pip install -r requirements.txt
```

---

## FastMCP Quick Start 快速开始

<font color=OrangeRed>FastMCP</font> is the high-level wrapper over the official MCP SDK. It uses decorators (`@mcp.tool()`, `@mcp.resource()`, `@mcp.prompt()`) to define server capabilities with minimal boilerplate.

### Define a Tool — @mcp.tool()

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DemoServer")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.tool()
def get_weather(city: str) -> str:
    """Get weather for a city."""
    # In production: call a real weather API
    return f"The weather in {city} is sunny, 25°C."
```

Type hints are used automatically to build the JSON schema the client sends to the LLM.

### Define a Resource — @mcp.resource()

```python
@mcp.resource("config://app")
def get_app_config() -> str:
    """Return application config."""
    return "debug=true\nversion=1.0"

@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: str) -> str:
    """Return a user profile by ID."""
    return f"User {user_id}: Engineer, 5yr exp"
```

Resources are read-only — they never trigger side effects.

### Define a Prompt — @mcp.prompt()

```python
@mcp.prompt()
def review_code(code: str) -> str:
    """Generate a code review prompt."""
    return f"Please review the following code and identify bugs:\n\n{code}"
```

### Run the Server

```bash
# stdio mode (default)
mcp run server.py

# Or directly
python server.py
```

```python
if __name__ == "__main__":
    mcp.run()                        # stdio
    # mcp.run(transport="sse")       # SSE/HTTP
```

---

## Traditional SDK: Resources and Tools

When using the lower-level `mcp` SDK directly (not FastMCP), define resources and tools explicitly.

### Defining Resources

`src/resources/user_profiles.py`:

```python
from typing import List, Dict, Any
from pydantic import BaseModel
import logging

logger = logging.getLogger("mcp_server.resources")

class UserProfile(BaseModel):
    name: str
    role: str
    department: str = "General"
    years_experience: int = 0

def fetch_user_profiles() -> List[Dict[str, Any]]:
    users = [
        UserProfile(name="Alice", role="Engineer", department="Engineering", years_experience=5),
        UserProfile(name="Bob", role="Product Manager", department="Product", years_experience=3),
    ]
    logger.info(f"Fetched {len(users)} user profiles")
    return [u.model_dump() for u in users]
```

`src/server.py`:

```python
from mcp_server import MCPServer, Resource
import logging
from src.resources.user_profiles import fetch_user_profiles

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_server")

def main() -> None:
    server = MCPServer(
        name="MyMCPServer",
        version="0.1.0",
        description="A simple MCP server example"
    )

    user_profiles = Resource(
        name="user_profiles",
        description="List of user profiles from the company database.",
        fetch_fn=fetch_user_profiles
    )
    server.add_resource(user_profiles)

    logger.info("Starting MCP server...")
    server.start()

if __name__ == "__main__":
    main()
```

### Defining Tools

`src/tools/user_management.py`:

```python
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError
import logging

logger = logging.getLogger("mcp_server.tools")

class CreateUserRequest(BaseModel):
    name: str = Field(..., min_length=2)
    role: str = Field(..., min_length=2)
    department: Optional[str] = Field("General")
    years_experience: Optional[int] = Field(0, ge=0)

def create_user_profile(request_data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        user_data = CreateUserRequest(**request_data)
        logger.info(f"Creating user: {user_data.name}")
        return {
            "status": "success",
            "message": f"User {user_data.name} created successfully",
            "user": user_data.model_dump()
        }
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return {"status": "error", "message": "Invalid user data", "details": str(e)}
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return {"status": "error", "message": "Failed to create user", "details": str(e)}
```

Register the tool in `server.py`:

```python
from mcp_server import MCPServer, Resource, Tool
from src.tools.user_management import create_user_profile

# Inside main():
create_user = Tool(
    name="create_user_profile",
    description="Create a new user profile in the database.",
    parameters={
        "name": {"type": "string", "description": "User's full name"},
        "role": {"type": "string", "description": "User's job role"},
        "department": {"type": "string", "description": "User's department (optional)"},
        "years_experience": {"type": "integer", "description": "Years of experience (optional)"}
    },
    execute_fn=create_user_profile
)
server.add_tool(create_user)
```

### Error Handling and Validation

Centralize validation using Pydantic:

```python
# src/utils/validation.py
from typing import Dict, Any, Optional, Type, Tuple
from pydantic import BaseModel, ValidationError
import logging

logger = logging.getLogger("mcp_server.validation")

def validate_request(
    data: Dict[str, Any],
    model_class: Type[BaseModel]
) -> Tuple[Optional[BaseModel], Optional[Dict[str, Any]]]:
    try:
        return model_class(**data), None
    except ValidationError as e:
        error_dict = {
            "status": "error",
            "message": "Validation failed",
            "errors": e.errors()
        }
        logger.error(f"Validation error: {e.errors()}")
        return None, error_dict
```

---

## Debugging with MCP Inspector 调试工具

<font color=OrangeRed>MCP Inspector</font> is an interactive browser-based tool for testing MCP servers without a full LLM client.

```bash
# Method 1: npx (no install required)
npx @modelcontextprotocol/inspector python server.py

# Method 2: via mcp CLI
mcp dev server.py

# Method 3: with environment variables
npx @modelcontextprotocol/inspector \
  -e API_KEY=your_key \
  python server.py
```

After running, open `http://localhost:5173` in a browser. You will see:

- **Resources tab** — list and read all registered resources
- **Tools tab** — invoke tools with custom parameters
- **Prompts tab** — preview prompt templates
- **Console** — view all JSON-RPC messages in real time

Typical debug workflow:

1. Start the Inspector pointing at your server
2. Click a tool → fill parameters → click "Run"
3. Inspect the JSON request/response in the Console tab
4. Confirm the output matches expectations before connecting to a real client

---

## Client Development 客户端开发

### stdio Client

The stdio client launches the MCP server as a subprocess and communicates over stdin/stdout.

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print("Tools:", [t.name for t in tools.tools])

            # List resources
            resources = await session.list_resources()
            print("Resources:", [r.name for r in resources.resources])

            # Call a tool
            result = await session.call_tool("add", {"a": 3, "b": 5})
            print("3 + 5 =", result.content[0].text)

asyncio.run(main())
```

### SSE Client

For servers running over HTTP/SSE:

```python
import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    async with sse_client("http://localhost:8000/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("get_weather", {"city": "Beijing"})
            print(result.content[0].text)

asyncio.run(main())
```

### Client with DeepSeek LLM

Full agentic loop where the LLM decides which tools to call:

```python
import asyncio
import json
from openai import AsyncOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

client = AsyncOpenAI(
    api_key="your_deepseek_api_key",
    base_url="https://api.deepseek.com",
)

async def run_agent():
    server_params = StdioServerParameters(command="python", args=["server.py"])
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Get tool list and convert to OpenAI format
            tools_response = await session.list_tools()
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description,
                        "parameters": t.inputSchema,
                    }
                }
                for t in tools_response.tools
            ]

            messages = [
                {"role": "user", "content": "What is the weather in Shanghai?"}
            ]

            # LLM decides to call a tool
            response = await client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                tools=tools,
            )

            # Execute tool calls returned by the LLM
            assistant_msg = response.choices[0].message
            messages.append(assistant_msg)

            for tool_call in (assistant_msg.tool_calls or []):
                args = json.loads(tool_call.function.arguments)
                result = await session.call_tool(tool_call.function.name, args)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result.content[0].text,
                })

            # Final LLM response after tool results
            final = await client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
            )
            print(final.choices[0].message.content)

asyncio.run(run_agent())
```

---

## Claude Desktop Configuration

To register an MCP server with Claude Desktop, edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"],
      "env": {
        "API_KEY": "your_api_key"
      }
    }
  }
}
```

After saving, restart Claude Desktop. The registered server's tools and resources appear automatically in every conversation.

For a server installed as a package:

```json
{
  "mcpServers": {
    "weather": {
      "command": "uvx",
      "args": ["mcp-server-weather"]
    }
  }
}
```

---

## Cline and Cursor Configuration

**Cline** (VS Code extension) and **Cursor** both support MCP servers via a JSON config file.

Cline — `~/.cline/mcp_settings.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {
        "API_KEY": "your_key"
      }
    }
  }
}
```

Cursor — project `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["server.py"]
    }
  }
}
```

---

## Sampling Callback 采样回调

<font color=OrangeRed>Sampling</font> is an MCP feature that lets the server request the LLM to generate text — the reverse of the normal flow. This enables pre/post tool hooks and multi-step reasoning patterns.

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import CreateMessageRequest, CreateMessageResult, TextContent

async def handle_sampling(request: CreateMessageRequest) -> CreateMessageResult:
    """Called when the server wants the LLM to generate text."""
    print(f"[Sampling] Server requests generation: {request.messages[-1].content.text}")
    # In production: forward to a real LLM
    return CreateMessageResult(
        role="assistant",
        content=TextContent(type="text", text="Sampling response placeholder"),
        model="mock-model",
        stopReason="endTurn",
    )

async def main():
    server_params = StdioServerParameters(command="python", args=["server.py"])
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write,
            sampling_callback=handle_sampling
        ) as session:
            await session.initialize()
            result = await session.call_tool("tool_that_uses_sampling", {})
            print(result)

asyncio.run(main())
```

The `sampling_callback` is invoked whenever the server calls `create_message`. Use it to:
- Log every LLM interaction for auditing
- Route to different models per request
- Add safety filters before responses reach the server

---

## Advanced Features 高级特性

### Lifecycle Management 生命周期管理

Use the `lifespan` context manager to initialize and clean up shared resources (DB connections, HTTP clients, caches) that tools depend on.

```python
from contextlib import asynccontextmanager
from mcp.server.fastmcp import FastMCP
import httpx

@asynccontextmanager
async def lifespan(app):
    # Startup: initialize shared state
    app.state.http_client = httpx.AsyncClient()
    app.state.db_pool = await create_db_pool()
    print("Server started, resources initialized.")
    yield
    # Shutdown: clean up
    await app.state.http_client.aclose()
    await app.state.db_pool.close()
    print("Server shutting down, resources released.")

mcp = FastMCP("MyServer", lifespan=lifespan)

@mcp.tool()
async def fetch_data(url: str) -> str:
    # Access the shared client from app state
    response = await mcp.app.state.http_client.get(url)
    return response.text
```

### Prompt Primitives

Prompts are reusable instruction templates. They appear in MCP-aware editors as slash commands or context actions.

```python
from mcp.server.fastmcp import FastMCP
from mcp.types import GetPromptResult, PromptMessage, TextContent

mcp = FastMCP("PromptServer")

@mcp.prompt()
def debug_error(error: str, language: str = "Python") -> GetPromptResult:
    return GetPromptResult(
        description=f"Debug a {language} error",
        messages=[
            PromptMessage(
                role="user",
                content=TextContent(
                    type="text",
                    text=f"You are an expert {language} developer. Debug this error:\n\n{error}"
                )
            )
        ]
    )
```

### Resource Primitives

Resources support URI templates for dynamic data:

```python
@mcp.resource("file://{path}")
async def read_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()

@mcp.resource("db://users/{user_id}")
async def get_user(user_id: str) -> str:
    # Query database
    user = await db.get_user(user_id)
    return user.to_json()
```

Resources can also return binary data (images, PDFs) using `BlobResourceContents`:

```python
from mcp.types import BlobResourceContents
import base64

@mcp.resource("image://{filename}")
async def get_image(filename: str) -> BlobResourceContents:
    with open(f"images/{filename}", "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return BlobResourceContents(blob=data, mimeType="image/png")
```

---

## LangChain Integration LangChain 集成

The `langchain-mcp-adapters` library converts MCP tools into LangChain-compatible tools, making them usable in any LangChain agent.

```bash
pip install langchain-mcp-adapters langchain-openai langgraph
```

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o")

async def main():
    server_params = StdioServerParameters(command="python", args=["server.py"])
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Convert MCP tools to LangChain tools
            tools = await load_mcp_tools(session)

            # Create a ReAct agent with MCP tools
            agent = create_react_agent(model, tools)
            result = await agent.ainvoke({
                "messages": [{"role": "user", "content": "What is 15 + 27?"}]
            })
            print(result["messages"][-1].content)

asyncio.run(main())
```

For multi-server setups:

```python
from langchain_mcp_adapters.client import MultiServerMCPClient

async def main():
    async with MultiServerMCPClient({
        "math": {
            "command": "python",
            "args": ["math_server.py"],
            "transport": "stdio",
        },
        "weather": {
            "url": "http://localhost:8000/sse",
            "transport": "sse",
        }
    }) as client:
        tools = client.get_tools()
        agent = create_react_agent(model, tools)
        result = await agent.ainvoke({
            "messages": [{"role": "user", "content": "What's the weather in Beijing?"}]
        })
        print(result["messages"][-1].content)
```

---

## Remote Deployment 远程部署

### SSE Transport SSE 传输模式

To serve an MCP server over HTTP/SSE:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("RemoteServer")

@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8000)
```

The server exposes two endpoints:
- `GET /sse` — SSE stream for server-to-client events
- `POST /messages` — client-to-server messages

Test with curl:

```bash
curl -N http://localhost:8000/sse
```

### Docker Deployment

`Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY server.py .

EXPOSE 8000

CMD ["python", "server.py"]
```

`docker-compose.yml`:

```yaml
version: "3.8"
services:
  mcp-server:
    build: .
    ports:
      - "8000:8000"
    environment:
      - API_KEY=${API_KEY}
      - LOG_LEVEL=INFO
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

```bash
docker build -t my-mcp-server .
docker-compose up -d
```

### AWS Deployment (Lambda + ECS)

**Stateless — Lambda + API Gateway (stdio/HTTPS)**

`template.yaml` (SAM):

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Transform: AWS::Serverless-2016-10-31

Resources:
  MCPServerFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: lambda_handler.handler
      Runtime: python3.11
      MemorySize: 512
      Timeout: 30
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /mcp
            Method: post
```

`lambda_handler.py`:

```python
import json
from server import mcp  # your FastMCP app

def handler(event, context):
    body = json.loads(event.get("body", "{}"))
    # Process MCP request
    response = mcp.handle_request(body)
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(response)
    }
```

**Stateful — ECS Fargate (SSE)**

Use ECS Fargate with an Application Load Balancer for persistent SSE connections. Key configuration:

```yaml
# ECS Task Definition (excerpt)
ContainerDefinitions:
  - Name: mcp-server
    Image: !Sub "${AWS::AccountId}.dkr.ecr.${AWS::Region}.amazonaws.com/mcp-server:latest"
    PortMappings:
      - ContainerPort: 8000
    Environment:
      - Name: TRANSPORT
        Value: sse
```

ALB target group: set `deregistration_delay` to 60s and use sticky sessions (duration-based) to ensure SSE clients stay connected to the same container.

### Aliyun Serverless 阿里云函数计算部署

Aliyun Function Compute (FC 3.0) supports HTTP triggers with SSE for stateless MCP servers.

**Prerequisites**

```bash
# Install Serverless Devs
npm install -g @serverless-devs/s

# Configure credentials
s config add --AccessKeyID <id> --AccessKeySecret <secret> --alias default
```

`s.yaml`:

```yaml
edition: 3.0.0
name: mcp-server

resources:
  mcp-server:
    component: fc3

    props:
      region: cn-hangzhou
      functionName: mcp-server
      description: MCP Server via SSE
      runtime: python3.10
      code: ./
      handler: server.handler
      memorySize: 512
      timeout: 60
      environmentVariables:
        TRANSPORT: sse

      triggers:
        - triggerName: http-trigger
          triggerType: http
          triggerConfig:
            authType: anonymous
            methods:
              - GET
              - POST
```

Adapt `server.py` for FC's HTTP event format:

```python
from mcp.server.fastmcp import FastMCP
import json

mcp = FastMCP("AliyunMCPServer")

@mcp.tool()
def hello(name: str) -> str:
    return f"Hello from Aliyun, {name}!"

def handler(environ, start_response):
    """WSGI-compatible handler for Aliyun FC HTTP trigger."""
    # Route SSE vs POST
    path = environ.get("PATH_INFO", "")
    if environ.get("REQUEST_METHOD") == "GET" and path == "/sse":
        return mcp.handle_sse(environ, start_response)
    elif environ.get("REQUEST_METHOD") == "POST" and path == "/messages":
        return mcp.handle_post(environ, start_response)
    else:
        start_response("404 Not Found", [])
        return [b"Not Found"]
```

Deploy and test:

```bash
# Deploy
s deploy

# Get endpoint URL
s info

# Test with Inspector
npx @modelcontextprotocol/inspector --sse https://<fc-endpoint>/sse
```

---

## Security Best Practices 安全最佳实践

| Risk | Mitigation |
|---|---|
| Credential exposure | Use environment variables; never hardcode API keys in server code |
| Input injection | Validate all tool inputs with Pydantic before executing |
| Path traversal | Validate file paths; use `pathlib.Path.resolve()` and check against allowed roots |
| Privilege escalation | Follow least-privilege principle; tools should only access what they need |
| Logging sensitive data | Never log API keys, passwords, or PII; sanitize error messages |
| Unauthenticated SSE | Add auth middleware (API key header, OAuth token) before exposing SSE publicly |

Example — path validation in a file-access tool:

```python
from pathlib import Path

ALLOWED_ROOT = Path("/data/safe")

@mcp.tool()
def read_file(filename: str) -> str:
    target = (ALLOWED_ROOT / filename).resolve()
    if not str(target).startswith(str(ALLOWED_ROOT)):
        raise ValueError("Path traversal detected")
    return target.read_text()
```

Example — API key validation middleware:

```python
from mcp.server.fastmcp import FastMCP
import os

mcp = FastMCP("SecureServer")

@mcp.middleware()
async def auth_check(request, call_next):
    api_key = request.headers.get("X-API-Key")
    if api_key != os.environ["SERVER_API_KEY"]:
        raise PermissionError("Invalid API key")
    return await call_next(request)
```

---

## Key Takeaways

- FastMCP (`@mcp.tool()`, `@mcp.resource()`, `@mcp.prompt()`) is the fastest way to build an MCP server — minimal boilerplate, full type-hint-driven schemas.
- Use `stdio` transport for local/desktop integrations; use `SSE` for any remote or multi-user scenario.
- MCP Inspector (`npx @modelcontextprotocol/inspector`) is the primary debug tool — test resources and tools interactively before wiring to a real LLM.
- The client-side agentic loop: list tools → convert to LLM format → let LLM decide → execute tool → feed results back → final response.
- Sampling callbacks invert the flow: the server can request LLM generation, enabling pre/post hooks and multi-step server-side reasoning.
- For production: use Docker + ECS (SSE) for stateful connections, or Lambda + API Gateway for stateless request-per-call workloads.
- Always validate inputs at the tool boundary, restrict file paths, and keep credentials in environment variables.

## References

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [FastMCP Documentation](https://gofastmcp.com)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)
- [How to Build an MCP Server: Step-by-Step Guide — OpenReplay](https://blog.openreplay.com/how-to-build-an-mcp-server/)
- [LangChain MCP Adapters](https://github.com/langchain-ai/langchain-mcp-adapters)
- [Aliyun Function Compute FC 3.0 Docs](https://help.aliyun.com/product/50980.html)
- [MCP Protocol Specification](https://modelcontextprotocol.io/specification)
