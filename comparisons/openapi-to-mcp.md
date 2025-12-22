# OpenAPI → MCP Conversion

Make your REST API callable by AI agents.

## Overview

You have an existing REST API with an OpenAPI (Swagger) specification, and you want AI agents to be able to discover and call your API endpoints as tools. This guide helps you choose the right tool to convert your OpenAPI spec into an MCP (Model Context Protocol) server.

**Why convert OpenAPI to MCP?**

* **AI-Native Access:** LLMs can directly discover and invoke your API endpoints as strongly-typed tools
* **Type Safety:** JSON Schema validation ensures correct parameter types and structures
* **Auto-Documentation:** Tools are self-describing with names, descriptions, and parameter schemas
* **Authentication:** Built-in support for OAuth2, API keys, bearer tokens, and other auth methods
* **Ecosystem Integration:** Works with Claude Desktop, Open WebUI, and other MCP clients

## Quick Decision Guide

| Your Situation | Recommended Tool | Why |
|----------------|------------------|-----|
| Want fastest setup (.NET) | [openapi-to-mcp](#openapi-to-mcp-ouvreboite) | Single command, supports OAuth2, actively maintained |
| Python shop, need async | [FastMCP](#fastmcp-jlowin) | Production framework with enterprise auth, first-class OpenAPI support |
| Enterprise CI/CD | [openapi-mcp-codegen](#openapi-mcp-codegen-cnoe-io) | Code generation for customization, backed by CNOE/Cisco |
| Spring Boot application | [Spring AI Annotations](#spring-ai-mcp-annotations) | Native Java integration with @McpTool annotations |
| Just exploring/testing | [Swagger-MCP](#swagger-mcp-vizioz) | TypeScript, simple setup, good for experimentation |
| Docker deployment | [openapi-mcp (ckanthony)](#openapi-mcp-ckanthony) | Pre-built Docker images, v2 and v3 support |

## Tools Comparison

### Tier 1: Production-Ready

#### openapi-to-mcp (ouvreboite)

* **Language:** .NET/C#
* **Install:** `dotnet tool install -g openapi-to-mcp` or [releases page](https://github.com/ouvreboite/openapi-to-mcp/releases)
* **Repository:** [github.com/ouvreboite/openapi-to-mcp](https://github.com/ouvreboite/openapi-to-mcp)
* **License:** MIT
* **Best for:** Fastest path from OpenAPI to MCP with minimal configuration

**Features:**

* OpenAPI 2.0 and 3.0 support (3.1 pending upstream support)
* JSON/YAML formats
* Local files or remote URLs
* OAuth2 support (ClientCredentials, RefreshToken, Password flows)
* Bearer token and API key authentication
* Host override for development/staging environments
* Multiple tool naming strategies
* Strongly typed tools with full JSON Schema

**Quick Start:**

```bash
# Install
dotnet tool install -g openapi-to-mcp

# Use with Claude Desktop (add to config)
{
  "mcpServers": {
    "petstore": {
      "command": "openapi-to-mcp",
      "args": [
        "https://petstore3.swagger.io/api/v3/openapi.json"
      ]
    }
  }
}
```

**Authentication Examples:**

```bash
# Bearer token
openapi-to-mcp spec.yaml --bearer-token "your-token-here"

# OAuth2 (uses tokenUrl from spec)
openapi-to-mcp spec.yaml --oauth2-client-credentials \
  --client-id "your-client-id" \
  --client-secret "your-secret"
```

**Pros:**

* Single command deployment
* OAuth2 built-in
* Active maintenance
* Cross-platform (.NET Core)

**Cons:**

* Requires .NET runtime
* OpenAPI 3.1 not yet supported

---

#### FastMCP (jlowin)

* **Language:** Python
* **Install:** `pip install fastmcp`
* **Repository:** [github.com/jlowin/fastmcp](https://github.com/jlowin/fastmcp)
* **License:** Apache 2.0
* **Best for:** Python developers building production MCP applications with advanced patterns

**Features:**

* **FastMCP 2.0** with production-grade architecture
* OpenAPI spec → MCP server generation
* FastAPI app → MCP server conversion
* Enterprise authentication (Google, GitHub, WorkOS, Azure, Auth0)
* Server composition and proxying
* Tool transformation pipelines
* Async/await support throughout
* Comprehensive client libraries
* Testing utilities
* Deployment tools

**Quick Start:**

```python
from fastmcp import FastMCP

# Create MCP server from OpenAPI spec
mcp = FastMCP.from_openapi("https://api.example.com/openapi.json")

# Or from FastAPI app
from fastapi import FastAPI
app = FastAPI()
mcp = FastMCP.from_fastapi(app)
```

**Advanced Patterns:**

```python
# Server composition
composed = mcp1 + mcp2 + mcp3

# Server proxying
proxy = FastMCP.proxy("https://remote-mcp-server.com")

# Tool transformation
@mcp.tool(transform=preprocess_inputs)
async def my_tool(data: dict) -> dict:
    return await process(data)
```

**Pros:**

* Production-ready framework (2.0+)
* First-class OpenAPI/FastAPI integration
* Enterprise authentication built-in
* Powerful composition patterns
* Active development and community
* Core SDK adopted by official MCP Python SDK

**Cons:**

* Requires Python 3.8+
* More complex than simple wrappers
* Learning curve for advanced features

---

#### openapi-mcp-codegen (cnoe-io)

* **Language:** Python
* **Install:** `pip install openapi-mcp-codegen` or use `uv`
* **Repository:** [github.com/cnoe-io/openapi-mcp-codegen](https://github.com/cnoe-io/openapi-mcp-codegen)
* **Documentation:** [cnoe-io.github.io/openapi-mcp-codegen/](https://cnoe-io.github.io/openapi-mcp-codegen/)
* **Backed by:** CNOE (Cloud Native Operational Excellence) / Cisco CAIPE team
* **Best for:** Enterprise CI/CD pipelines requiring code generation and customization

**Features:**

* Generates production-ready Python MCP server code from OpenAPI specs
* LLM-enhanced documentation for better AI understanding
* Intelligent code generation with type hints
* httpx-based async HTTP client
* Configurable base URLs and headers
* uv package manager integration
* Designed for enterprise scale and governance

**Quick Start:**

```bash
# Install
pip install openapi-mcp-codegen

# Generate MCP server code
openapi-mcp-codegen generate \
  --spec openapi.yaml \
  --output ./my-mcp-server

# Run generated server
cd my-mcp-server
uv run mcp-server
```

**Generated Code Pattern:**

```python
# OpenAPI parameters → function arguments with type hints
async def operation_id(
    param1: str,
    param2: int,
    body: RequestModel
) -> ResponseModel:
    # httpx client with configured base URL
    async with httpx.AsyncClient() as client:
        response = await client.post(...)
        return response.json()
```

**Pros:**

* Enterprise-backed (CNOE/Cisco)
* Code generation allows full customization
* Built for CI/CD integration
* LLM-optimized documentation
* Active CAIPE community

**Cons:**

* Requires Python 3.8+
* More setup than runtime tools
* Generated code needs maintenance

**Use Cases:**

* Enterprise API governance: "One OpenAPI spec → one MCP Server → one AI-powered, access-controlled gateway"
* Role-based access control for AI agents
* Custom business logic in generated servers
* Meraki/Cisco API integration examples

---

### Tier 2: Framework Integration

#### Spring AI MCP Annotations

* **Language:** Java
* **Install:** Add Spring AI MCP dependency
* **Repository:** [github.com/spring-ai-community/mcp-annotations](https://github.com/spring-ai-community/mcp-annotations)
* **Documentation:** [Spring AI Reference](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-overview.html)
* **Best for:** Spring Boot developers wanting native Java MCP integration

**Features:**

* Annotation-based MCP server development
* `@McpTool`, `@McpResource`, `@McpPrompt` annotations
* Automatic JSON schema generation
* Spring component scanning integration
* AOT (Ahead-of-Time) compilation for native images
* Request context support (sync and async)
* Protocol version 2025-06-18 support

**Quick Start:**

```java
// Add dependency
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-mcp-annotations</artifactId>
</dependency>
```

```java
@Component
public class ApiTools {
    @McpTool(
        name = "create_user",
        description = "Create a new user in the system"
    )
    public User createUser(
        @McpToolParam(description = "Username", required = true) String username,
        @McpToolParam(description = "Email address", required = true) String email
    ) {
        return userService.createUser(username, email);
    }

    @McpResource(
        uri = "user://{id}",
        name = "User",
        description = "Get user by ID"
    )
    public User getUser(String id) {
        return userRepository.findById(id);
    }
}
```

**Advanced Features:**

```java
// Request context for progress updates
@McpTool(name = "long_operation")
public Result longOperation(McpSyncRequestContext ctx) {
    ctx.reportProgress(0.0, 100.0, "Starting...");
    // ... work ...
    ctx.reportProgress(50.0, 100.0, "Halfway...");
    // ... work ...
    return result;
}
```

**Pros:**

* Native Spring Boot integration
* Familiar Java annotations pattern
* Automatic type conversion
* Spring ecosystem benefits
* Active development (1.1.0-M2 released Sept 2025)

**Cons:**

* Java-only
* Requires Spring framework
* Not specifically OpenAPI-focused (general MCP tool building)

**Note:** While Spring AI annotations don't directly consume OpenAPI specs, they're excellent for exposing Spring Boot REST APIs (which often have OpenAPI docs) as MCP servers with minimal code changes.

---

### Tier 3: Exploration & Testing

#### Swagger-MCP (Vizioz)

* **Language:** TypeScript (97.9%)
* **Stars:** ~108
* **Repository:** [github.com/Vizioz/Swagger-MCP](https://github.com/Vizioz/Swagger-MCP)
* **Last Updated:** March 2025
* **Best for:** TypeScript developers exploring MCP, quick prototypes

**Features:**

* JSON and YAML Swagger/OpenAPI support
* Complete schema info including nested objects
* Auto-download and cache Swagger definitions
* TypeScript code generation for MCP tools
* `--swagger-url` argument for remote specs

**Quick Start:**

```bash
npm install swagger-mcp

swagger-mcp --swagger-url https://petstore3.swagger.io/api/v3/openapi.json
```

**Pros:**

* Simple TypeScript implementation
* Good for learning MCP concepts
* Caches definitions for offline use

**Cons:**

* Less actively maintained (last commit March 2025)
* Fewer features than production tools
* Limited authentication support

---

#### openapi-mcp (ckanthony)

* **Language:** Go
* **Stars:** ~79-131
* **Repository:** [github.com/ckanthony/openapi-mcp](https://github.com/ckanthony/openapi-mcp)
* **Docker Hub:** `ckanthony/openapi-mcp:latest`
* **Best for:** Docker deployments, containerized environments

**Features:**

* OpenAPI v2 (Swagger) & v3 support
* Local and remote spec support
* Automatic MCP tool generation from operations
* JSON Schema from parameters and request/response
* Secure API key handling
* Pre-built Docker images

**Quick Start:**

```bash
# Docker
docker run -v $(pwd)/spec.yaml:/spec.yaml \
  ckanthony/openapi-mcp:latest /spec.yaml

# With API key
docker run -e API_KEY=your-key \
  ckanthony/openapi-mcp:latest https://api.example.com/openapi.json
```

**Pros:**

* Docker-native deployment
* Go's performance and concurrency
* Pre-built images

**Cons:**

* Less flexible than Python/TypeScript options
* Limited documentation
* Uncertain maintenance status

---

## Other Notable Tools

### Research & Experimentation

* **danishjsheikh/swagger-mcp** - Node.js, dynamic tool generation, multiple auth types
* **matthewhand/mcp-openapi-proxy** - Python proxy for OpenAPI→MCP workflows
* **andersmandersen/mcp-swagger** - MCP server for Swagger doc access
* **LostInBrittany/swagger-to-mcp-generator** - Java/Quarkus code generator
* **dcolley/swagger-mcp** - Ingests and serves Swagger specs through MCP

These tools are less mature or documented than Tier 1/2 options, but may fit specific use cases.

---

## How It Works

### Conversion Process

```
┌─────────────────┐
│  OpenAPI Spec   │
│  (YAML/JSON)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Converter Tool │  ← openapi-to-mcp, FastMCP, codegen, etc.
│  - Parse spec   │
│  - Map routes   │
│  - Gen schemas  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   MCP Server    │
│  - Tools list   │
│  - JSON schemas │
│  - Auth config  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   MCP Client    │  ← Claude Desktop, Open WebUI, etc.
│  (AI Agent)     │
└─────────────────┘
```

### Example Mapping

**OpenAPI Endpoint:**

```yaml
paths:
  /users/{id}:
    get:
      operationId: getUser
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
```

**Generated MCP Tool:**

```json
{
  "name": "getUser",
  "description": "Get user by ID",
  "inputSchema": {
    "type": "object",
    "properties": {
      "id": {
        "type": "string",
        "description": "User ID"
      }
    },
    "required": ["id"]
  }
}
```

### Type Mapping

| OpenAPI Type | JSON Schema Type | Notes |
|-------------|-----------------|--------|
| `string` | `string` | With format hints (date, email, uri) |
| `integer` | `integer` | int32, int64 |
| `number` | `number` | float, double |
| `boolean` | `boolean` | |
| `array` | `array` | With items schema |
| `object` | `object` | Nested properties |
| `$ref` | `$ref` | Schema references |
| `oneOf/anyOf/allOf` | Preserved | Complex schemas |

---

## Authentication Considerations

### Supported Auth Methods

| Method | openapi-to-mcp | FastMCP | codegen | Swagger-MCP |
|--------|----------------|---------|---------|-------------|
| **OAuth2 ClientCredentials** | ✓ | ✓ | ✓ | ✗ |
| **OAuth2 RefreshToken** | ✓ | ✓ | ? | ✗ |
| **OAuth2 Password** | ✓ | ✓ | ? | ✗ |
| **Bearer Token** | ✓ | ✓ | ✓ | ✓ |
| **API Key** | ✓ | ✓ | ✓ | ✓ |
| **Basic Auth** | ? | ✓ | ✓ | ✓ |
| **Enterprise SSO** | ✗ | ✓ | Custom | ✗ |

### Security Best Practices

* **Never hardcode credentials** in MCP server configurations
* Use environment variables or secure secret stores
* Rotate API keys and tokens regularly
* Implement rate limiting at the MCP server level
* Use OAuth2 flows with short-lived tokens when possible
* Consider adding an auth proxy layer for enterprise deployments

### Example: Secure Configuration

```json
{
  "mcpServers": {
    "my-api": {
      "command": "openapi-to-mcp",
      "args": ["https://api.example.com/openapi.json"],
      "env": {
        "BEARER_TOKEN": "${MY_API_TOKEN}"
      }
    }
  }
}
```

---

## Limitations

### Common Challenges

**1. Authentication Complexity**

* Not all tools support all OAuth2 flows
* Some APIs use custom auth schemes not in OpenAPI spec
* Token refresh logic may need custom implementation

**2. OpenAPI 3.1 Support**

* Many tools only support 3.0 or earlier
* 3.1 features (like `$ref` improvements) may not work
* Check tool compatibility before upgrading specs

**3. Webhooks & Callbacks**

* OpenAPI webhooks don't map to MCP tools (tools are request/response)
* Callbacks require special handling or aren't supported

**4. Binary Data**

* File uploads/downloads may have limited support
* Base64 encoding can be inefficient for large files
* Check if tool supports multipart/form-data

**5. Complex Schemas**

* Deeply nested objects may exceed LLM context limits
* `oneOf`/`anyOf` can confuse AI agents
* Consider simplifying schemas for better LLM understanding

**6. Rate Limiting**

* OpenAPI specs rarely include rate limit info
* MCP servers may not enforce or communicate limits
* Add custom logic or use gateway tools

**7. API Versioning**

* Multiple API versions may need multiple MCP servers
* Version negotiation not standardized
* Consider version in tool names (`getUser_v2`)

### Workarounds

* **Auth issues:** Use FastMCP for complex enterprise auth, or add auth proxy
* **3.1 support:** Downgrade spec to 3.0, or wait for upstream library updates
* **Complex schemas:** Pre-process OpenAPI spec to flatten structures
* **Rate limits:** Wrap MCP server with rate-limiting proxy
* **Versioning:** Generate separate MCP servers per API version

---

## Quick Start Examples

### Using openapi-to-mcp

```bash
# 1. Install
dotnet tool install -g openapi-to-mcp

# 2. Test with public API
openapi-to-mcp https://petstore3.swagger.io/api/v3/openapi.json

# 3. Add to Claude Desktop config (~/.config/claude/config.json or similar)
{
  "mcpServers": {
    "petstore": {
      "command": "openapi-to-mcp",
      "args": ["https://petstore3.swagger.io/api/v3/openapi.json"]
    }
  }
}

# 4. Restart Claude Desktop, verify tools appear
```

---

### Using FastMCP

```python
# 1. Install
# pip install fastmcp

# 2. Create server (server.py)
from fastmcp import FastMCP

mcp = FastMCP.from_openapi(
    "https://api.github.com/openapi.json",
    name="GitHub API"
)

if __name__ == "__main__":
    mcp.run()

# 3. Configure MCP client
{
  "mcpServers": {
    "github": {
      "command": "python",
      "args": ["server.py"]
    }
  }
}
```

---

### Using openapi-mcp-codegen

```bash
# 1. Install
pip install openapi-mcp-codegen

# 2. Generate server code
openapi-mcp-codegen generate \
  --spec https://api.example.com/openapi.yaml \
  --output ./my-api-mcp

# 3. Review and customize generated code
cd my-api-mcp
cat mcp_server.py

# 4. Run server
uv run mcp-server

# 5. Configure client
{
  "mcpServers": {
    "my-api": {
      "command": "uv",
      "args": ["run", "mcp-server"],
      "cwd": "/path/to/my-api-mcp"
    }
  }
}
```

---

### Using Spring AI Annotations

```java
// 1. Add dependency to pom.xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-mcp-boot-starter</artifactId>
</dependency>

// 2. Create MCP tools from existing REST controllers
@Component
public class UserApiMcpTools {

    @Autowired
    private UserService userService;

    @McpTool(
        name = "create_user",
        description = "Create a new user"
    )
    public UserDto createUser(
        @McpToolParam(description = "Username", required = true) String username,
        @McpToolParam(description = "Email", required = true) String email
    ) {
        return userService.createUser(username, email);
    }
}

// 3. Spring Boot auto-configures MCP server
// 4. Connect MCP client to stdio transport
```

---

## Choosing the Right Tool

### Decision Tree

```
Do you have an existing Spring Boot app?
│
├─ YES → Spring AI Annotations
│         (Native Java integration)
│
└─ NO → Do you need enterprise-grade auth (SSO, RBAC)?
        │
        ├─ YES → FastMCP 2.0
        │         (Google, Azure, WorkOS, etc.)
        │
        └─ NO → Do you need to customize generated code?
                │
                ├─ YES → openapi-mcp-codegen
                │         (CI/CD, governance)
                │
                └─ NO → What runtime do you prefer?
                        │
                        ├─ .NET → openapi-to-mcp (ouvreboite)
                        ├─ Python → FastMCP
                        ├─ TypeScript → Swagger-MCP
                        └─ Docker → openapi-mcp (ckanthony)
```

### By Use Case

| Use Case | Recommended Tool | Reason |
|----------|------------------|--------|
| **Quick prototype** | openapi-to-mcp | Single command, no code |
| **Production Python** | FastMCP | Enterprise features, active development |
| **CI/CD pipeline** | openapi-mcp-codegen | Code generation, customization |
| **Spring Boot** | Spring AI Annotations | Native Java, annotation-based |
| **Docker deployment** | openapi-mcp (ckanthony) | Pre-built images |
| **Complex auth** | FastMCP | SSO, OAuth2, enterprise providers |
| **Cisco/Meraki** | openapi-mcp-codegen | Cisco backing, governance focus |
| **Learning MCP** | Swagger-MCP | Simple TypeScript, easy to understand |

---

## See Also

* [MCP → OpenAPI](mcp-to-openapi.md) - The reverse direction (expose MCP servers as REST APIs)
* [Full Comparison](auto-generated.md) - All MCP ecosystem tools
* [Transport Bridges](transports.md) - stdio, HTTP, SSE, WebSocket conversion
* [Enterprise Guide](enterprise.md) - Production deployment considerations (coming soon)
* [Security Analysis](security.md) - Security review of MCP tools

---

## Sources & Further Reading

* [FastMCP GitHub Repository](https://github.com/jlowin/fastmcp)
* [Introducing FastMCP 2.0](https://www.jlowin.dev/blog/fastmcp-2)
* [openapi-to-mcp GitHub Repository](https://github.com/ouvreboite/openapi-to-mcp)
* [Spring AI MCP Annotations Documentation](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-overview.html)
* [Spring AI MCP Blog Post](https://spring.io/blog/2025/09/16/spring-ai-mcp-intro-blog/)
* [CNOE openapi-mcp-codegen Documentation](https://cnoe-io.github.io/openapi-mcp-codegen/)
* [Cisco Blog: Wrangling the Wild West of MCP Servers](https://blogs.cisco.com/learning/wrangling-the-wild-west-of-mcp-servers)
* [Speakeasy: Generating MCP tools from OpenAPI](https://www.speakeasy.com/mcp/tool-design/generate-mcp-tools-from-openapi)
* [Spring AI 1.1.0-M2 Release Notes](https://spring.io/blog/2025/09/19/spring-ai-1-1-0-M2-mcp-focused/)
* [Creating Your First MCP Server in Java](https://www.danvega.dev/blog/creating-your-first-mcp-server-java)

---

**Last Updated:** 2025-12-22
**Contributions:** See [CONTRIBUTING.md](../CONTRIBUTING.md) for how to add or update tool information.
