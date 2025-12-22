# MCP → OpenAPI/REST

Expose your MCP server as a REST API.

## Overview

Why expose MCP as REST:

* **Integration with non-MCP systems** - Connect MCP tools to existing REST-based infrastructure
* **Testing with standard HTTP tools** - Use curl, Postman, or any HTTP client for testing
* **Gateway/proxy deployments** - Create centralized access points for multiple MCP servers
* **Swagger UI for exploration** - Interactive documentation and testing interface
* **Legacy system integration** - Bridge MCP capabilities to systems that only support REST
* **Public API exposure** - Make MCP tools available to external developers

## Tools Comparison

| Tool | Type | Best For | Auth | OpenAPI Spec | Deployment |
|------|------|----------|------|--------------|------------|
| MCPO | Self-hosted | General use, Open WebUI | Bearer | Auto-generated | Docker/pip |
| Azure APIM | Cloud | Enterprise, governance | Entra ID | Manual config | Azure cloud |
| Custom wrapper | DIY | Full control, specific needs | Any | Custom | Your choice |

## Recommended: MCPO

The official recommendation from the Open WebUI team for exposing MCP servers as REST APIs.

### Features

* **Swagger UI included** - Interactive API documentation out of the box
* **Auto-generates OpenAPI spec** - Automatically creates OpenAPI 3.0 spec from MCP tool definitions
* **Easy deployment** - Single command to start serving
* **Bearer token authentication** - Simple token-based security
* **CORS support** - Configure cross-origin requests
* **Multiple server support** - Expose multiple MCP servers through one REST endpoint

### Quick Start

```bash
# Install MCPO
pip install mcpo

# Basic usage - expose a local MCP server
mcpo --port 8000 -- npx -y @modelcontextprotocol/server-filesystem /tmp

# With authentication
export MCPO_API_KEY=your-secret-token
mcpo --port 8000 --auth bearer -- your-mcp-server

# With CORS enabled
mcpo --port 8000 --cors-origin "https://your-app.com" -- your-mcp-server

# Multiple servers (advanced)
mcpo --port 8000 --config servers.json
```

### Example: Filesystem Server via REST

```bash
# Start MCPO with filesystem server
mcpo --port 8000 -- npx -y @modelcontextprotocol/server-filesystem /tmp

# Access Swagger UI
# Open http://localhost:8000/docs

# Test with curl
curl -X POST http://localhost:8000/api/tools/read_file \
  -H "Content-Type: application/json" \
  -d '{"path": "/tmp/test.txt"}'

# List available tools
curl http://localhost:8000/api/tools

# Get OpenAPI spec
curl http://localhost:8000/openapi.json
```

### Configuration File Format

```json
{
  "servers": [
    {
      "name": "filesystem",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
      "prefix": "/fs"
    },
    {
      "name": "github",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxx"
      },
      "prefix": "/gh"
    }
  ]
}
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

RUN pip install mcpo

# Install Node.js for MCP servers that need it
RUN apt-get update && apt-get install -y nodejs npm

ENV MCPO_API_KEY=change-me-in-production

EXPOSE 8000

CMD ["mcpo", "--port", "8000", "--auth", "bearer", "--", \
     "npx", "-y", "@modelcontextprotocol/server-filesystem", "/data"]
```

```yaml
# docker-compose.yml
services:
  mcpo:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MCPO_API_KEY=${MCPO_API_KEY}
    volumes:
      - ./data:/data
```

### Integration with Open WebUI

MCPO was specifically designed for Open WebUI integration:

```yaml
# Open WebUI configuration
openai:
  api_base: http://mcpo:8000/api
  api_key: ${MCPO_API_KEY}

tools:
  mcp_tools:
    enabled: true
    endpoint: http://mcpo:8000
```

## Enterprise: Azure API Management

For organizations already using Azure infrastructure and requiring enterprise governance.

### Features

* **No-code configuration** - Set up MCP → REST bridging through Azure Portal
* **Enterprise governance** - Rate limiting, quotas, analytics
* **Entra ID authentication** - Integrate with Microsoft identity platform
* **Built-in monitoring** - Azure Monitor, Application Insights integration
* **Developer portal** - Auto-generated documentation for API consumers
* **Global distribution** - Multi-region deployments with CDN

### Setup

#### 1. Deploy MCP Server to Azure

```bash
# Option A: Container Apps
az containerapp create \
  --name mcp-server \
  --resource-group mcp-rg \
  --environment mcp-env \
  --image your-mcp-server:latest \
  --target-port 3000 \
  --ingress internal

# Option B: App Service
az webapp create \
  --name mcp-server \
  --resource-group mcp-rg \
  --plan mcp-plan \
  --deployment-container-image your-mcp-server:latest
```

#### 2. Create API Management Instance

```bash
az apim create \
  --name mcp-apim \
  --resource-group mcp-rg \
  --publisher-email admin@example.com \
  --publisher-name "Your Org" \
  --sku-name Developer
```

#### 3. Configure API from OpenAPI Spec

```bash
# Generate OpenAPI spec from your MCP server's tool definitions
# Then import to APIM
az apim api import \
  --path /mcp \
  --resource-group mcp-rg \
  --service-name mcp-apim \
  --specification-format OpenApi \
  --specification-path mcp-openapi.json
```

#### 4. Add Authentication Policy

```xml
<policies>
  <inbound>
    <validate-jwt header-name="Authorization" failed-validation-httpcode="401">
      <openid-config url="https://login.microsoftonline.com/{tenant}/.well-known/openid-configuration" />
      <audiences>
        <audience>api://mcp-server</audience>
      </audiences>
    </validate-jwt>
    <rate-limit calls="100" renewal-period="60" />
  </inbound>
  <backend>
    <base />
  </backend>
  <outbound>
    <base />
  </outbound>
</policies>
```

### Example: GitHub MCP Server via Azure APIM

```bash
# 1. Deploy GitHub MCP server
az containerapp create \
  --name mcp-github \
  --resource-group mcp-rg \
  --environment mcp-env \
  --image ghcr.io/modelcontextprotocol/server-github:latest \
  --env-vars GITHUB_TOKEN=secretref:github-token \
  --secrets github-token=${GITHUB_TOKEN} \
  --target-port 3000

# 2. Configure APIM backend
az apim backend create \
  --resource-group mcp-rg \
  --service-name mcp-apim \
  --backend-id mcp-github-backend \
  --url https://mcp-github.internal.example.com \
  --protocol http

# 3. Test via APIM
curl -X POST https://mcp-apim.azure-api.net/mcp/tools/search_repositories \
  -H "Authorization: Bearer ${ENTRA_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"query": "model context protocol"}'
```

## DIY: Custom FastAPI Wrapper

When you need full control over the REST API design, authentication, or business logic.

### Basic FastAPI Wrapper

```python
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import asyncio
import json
from typing import Any, Dict

app = FastAPI(
    title="MCP REST Bridge",
    description="REST API wrapper for MCP servers",
    version="1.0.0"
)

security = HTTPBearer()

# MCP client setup (using mcp Python SDK)
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class ToolRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]

class ToolResponse(BaseModel):
    content: list[Any]
    isError: bool = False

# Global MCP session
mcp_session = None

async def get_mcp_session():
    """Initialize and return MCP session."""
    global mcp_session
    if mcp_session is None:
        server_params = StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
        )
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                mcp_session = session
    return mcp_session

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify bearer token."""
    import os
    expected_token = os.getenv("API_TOKEN", "secret-token")
    if credentials.credentials != expected_token:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return credentials.credentials

@app.get("/")
async def root():
    """API information."""
    return {
        "name": "MCP REST Bridge",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/api/tools")
async def list_tools(token: str = Depends(verify_token)):
    """List all available MCP tools."""
    session = await get_mcp_session()
    tools_result = await session.list_tools()
    return {
        "tools": [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.inputSchema
            }
            for tool in tools_result.tools
        ]
    }

@app.post("/api/tools/execute", response_model=ToolResponse)
async def execute_tool(
    request: ToolRequest,
    token: str = Depends(verify_token)
):
    """Execute an MCP tool by name."""
    session = await get_mcp_session()

    try:
        result = await session.call_tool(request.tool_name, request.arguments)
        return ToolResponse(
            content=result.content,
            isError=result.isError if hasattr(result, 'isError') else False
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tools/{tool_name}")
async def execute_tool_direct(
    tool_name: str,
    arguments: Dict[str, Any],
    token: str = Depends(verify_token)
):
    """Execute an MCP tool via path parameter."""
    session = await get_mcp_session()

    try:
        result = await session.call_tool(tool_name, arguments)
        return {
            "content": result.content,
            "isError": result.isError if hasattr(result, 'isError') else False
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Running the Custom Wrapper

```bash
# Install dependencies
pip install fastapi uvicorn mcp

# Set authentication token
export API_TOKEN=your-secret-token

# Run the server
python mcp_rest_bridge.py

# Test endpoints
curl http://localhost:8000/api/tools \
  -H "Authorization: Bearer your-secret-token"

curl -X POST http://localhost:8000/api/tools/execute \
  -H "Authorization: Bearer your-secret-token" \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "read_file",
    "arguments": {"path": "/tmp/test.txt"}
  }'
```

### Advanced: Multi-Server Router

```python
from fastapi import FastAPI, Path
from typing import Dict
from mcp import ClientSession

app = FastAPI()

# Multiple MCP server configurations
MCP_SERVERS = {
    "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
    },
    "github": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "env": {"GITHUB_TOKEN": "ghp_xxx"}
    },
    "postgres": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-postgres"],
        "env": {"DATABASE_URL": "postgresql://..."}
    }
}

sessions: Dict[str, ClientSession] = {}

@app.post("/api/{server_name}/tools/{tool_name}")
async def execute_server_tool(
    server_name: str = Path(..., description="MCP server name"),
    tool_name: str = Path(..., description="Tool name"),
    arguments: Dict[str, Any] = {}
):
    """Execute tool on specific MCP server."""
    if server_name not in MCP_SERVERS:
        raise HTTPException(status_code=404, detail=f"Server {server_name} not found")

    # Get or create session for this server
    if server_name not in sessions:
        # Initialize session (simplified - needs proper async context)
        pass

    session = sessions[server_name]
    result = await session.call_tool(tool_name, arguments)

    return {"content": result.content}
```

## Architecture Patterns

### Direct Proxy

Simple one-to-one mapping:

```
┌─────────────┐      ┌──────┐      ┌─────────────┐
│ REST Client │─────▶│ MCPO │─────▶│ MCP Server  │
└─────────────┘      └──────┘      └─────────────┘
                    HTTP/REST      MCP Protocol
```

**Use case:** Single MCP server, simple testing, development

**Implementation:** `mcpo --port 8000 -- your-mcp-server`

### Gateway Pattern

Multiple MCP servers behind single REST endpoint:

```
                      ┌─────────────────┐
                      │   REST Gateway  │
                      │   (MCPO/Custom) │
                      └────────┬────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ MCP Server 1 │      │ MCP Server 2 │      │ MCP Server 3 │
│ (Filesystem) │      │  (GitHub)    │      │  (Postgres)  │
└──────────────┘      └──────────────┘      └──────────────┘
```

**Use case:** Centralized tool access, unified authentication, load balancing

**Implementation:** MCPO with config file or custom FastAPI router

### Cloud Integration

Enterprise deployment with managed services:

```
┌─────────────────┐
│ External Apps   │
│ (Web/Mobile)    │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│  Azure APIM     │
│  - Auth (Entra) │
│  - Rate Limit   │
│  - Monitoring   │
└────────┬────────┘
         │ Internal
         ▼
┌─────────────────┐      ┌─────────────────┐
│ Container Apps  │      │   Key Vault     │
│  - MCP Servers  │─────▶│   (Secrets)     │
│  - Auto-scale   │      └─────────────────┘
└─────────────────┘
```

**Use case:** Production deployments, compliance requirements, global distribution

**Implementation:** Azure APIM + Container Apps/App Service

### Hybrid: On-Prem + Cloud

Bridge on-premises MCP servers to cloud consumers:

```
┌─────────────┐
│ Cloud Apps  │
└──────┬──────┘
       │ Internet
       ▼
┌─────────────┐
│   APIM      │
│   (Cloud)   │
└──────┬──────┘
       │ VPN/ExpressRoute
       ▼
┌─────────────┐      ┌──────────────┐
│   MCPO      │─────▶│ MCP Servers  │
│ (On-Prem)   │      │ (On-Prem)    │
└─────────────┘      └──────────────┘
```

**Use case:** Sensitive data that must stay on-premises, gradual cloud migration

## Security Considerations

### Authentication Forwarding

When exposing MCP tools via REST, properly forward authentication:

```python
# Bad - No authentication passed to MCP
@app.post("/api/tools/{tool_name}")
async def execute_tool(tool_name: str, args: dict):
    return await mcp_session.call_tool(tool_name, args)

# Good - Pass user context to MCP server
@app.post("/api/tools/{tool_name}")
async def execute_tool(
    tool_name: str,
    args: dict,
    user: User = Depends(get_current_user)
):
    # Include user context in MCP request
    args["_user_context"] = {
        "user_id": user.id,
        "permissions": user.permissions
    }
    return await mcp_session.call_tool(tool_name, args)
```

### Rate Limiting

Protect your MCP servers from abuse:

```python
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

@app.post("/api/tools/{tool_name}")
@limiter.limit("10/minute")  # 10 requests per minute
async def execute_tool(
    tool_name: str,
    args: dict,
    request: Request
):
    return await mcp_session.call_tool(tool_name, args)
```

Or in Azure APIM:

```xml
<rate-limit calls="100" renewal-period="60" />
<quota calls="10000" renewal-period="86400" />
```

### Audit Logging

Track all MCP tool executions:

```python
import logging
from datetime import datetime

audit_logger = logging.getLogger("audit")

@app.post("/api/tools/{tool_name}")
async def execute_tool(
    tool_name: str,
    args: dict,
    user: User = Depends(get_current_user)
):
    audit_logger.info(
        "MCP tool execution",
        extra={
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user.id,
            "tool_name": tool_name,
            "arguments": args,
            "ip_address": request.client.host
        }
    )

    result = await mcp_session.call_tool(tool_name, args)

    audit_logger.info(
        "MCP tool result",
        extra={
            "tool_name": tool_name,
            "success": not result.isError,
            "response_size": len(str(result.content))
        }
    )

    return result
```

### Input Validation

Sanitize inputs before passing to MCP servers:

```python
from pydantic import BaseModel, validator, Field

class FileReadRequest(BaseModel):
    path: str = Field(..., max_length=1000)

    @validator('path')
    def validate_path(cls, v):
        # Prevent directory traversal
        if '..' in v or v.startswith('/etc'):
            raise ValueError('Invalid path')
        return v

@app.post("/api/tools/read_file")
async def read_file(request: FileReadRequest):
    return await mcp_session.call_tool("read_file", {"path": request.path})
```

### CORS Configuration

Properly configure CORS for web client access:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-app.com",
        "https://staging.your-app.com"
    ],  # Never use ["*"] in production
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)
```

### Secret Management

Never hardcode secrets in your REST bridge:

```python
# Bad
GITHUB_TOKEN = "ghp_1234567890abcdef"

# Good - Environment variables
import os
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Better - Secret management service
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://myvault.vault.azure.net/", credential=credential)
GITHUB_TOKEN = client.get_secret("github-token").value
```

## Performance Optimization

### Connection Pooling

Reuse MCP connections instead of creating new ones per request:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize MCP connections
    await init_mcp_sessions()
    yield
    # Shutdown: Close MCP connections
    await close_mcp_sessions()

app = FastAPI(lifespan=lifespan)
```

### Caching

Cache expensive MCP tool results:

```python
from functools import lru_cache
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

@app.post("/api/tools/search")
@cache(expire=300)  # Cache for 5 minutes
async def search_repositories(query: str):
    return await mcp_session.call_tool("search_repositories", {"query": query})
```

### Async Processing

For long-running MCP tools, use async task queues:

```python
from fastapi import BackgroundTasks

@app.post("/api/tools/long-running/{tool_name}")
async def execute_long_running_tool(
    tool_name: str,
    args: dict,
    background_tasks: BackgroundTasks
):
    task_id = str(uuid.uuid4())
    background_tasks.add_task(execute_mcp_tool_async, task_id, tool_name, args)
    return {"task_id": task_id, "status": "processing"}

@app.get("/api/tasks/{task_id}")
async def get_task_status(task_id: str):
    # Check task status in Redis/DB
    return {"task_id": task_id, "status": "completed", "result": {...}}
```

## See Also

* [OpenAPI → MCP](openapi-to-mcp.md) - The reverse direction: exposing REST APIs as MCP tools
* [MCP Transport Protocols](../transports.md) - Understanding MCP's native communication methods
* [MCP Security Best Practices](../security.md) - Securing MCP servers and clients
* [Open WebUI Integration](../integrations/open-webui.md) - Using MCPO with Open WebUI
* [Azure APIM Documentation](https://learn.microsoft.com/azure/api-management/) - Microsoft's official APIM guide
