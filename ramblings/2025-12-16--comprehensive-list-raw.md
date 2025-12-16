# MCP (Model Context Protocol) Wrappers, Bridges & CLI Tools - Comprehensive List

**Research Date:** 2025-12-16
**Focus:** Tools that wrap MCP servers and expose them as CLI tools, REST APIs, HTTP/SSE bridges, and other interfaces

## Table of Contents

* [Official Anthropic Tools](#official-anthropic-tools)
* [CLI Clients & Interactive Tools](#cli-clients--interactive-tools)
* [HTTP/SSE/WebSocket Bridges](#httpssewebsocket-bridges)
* [REST API & OpenAPI Wrappers](#rest-api--openapi-wrappers)
* [Enterprise Gateways & Proxies](#enterprise-gateways--proxies)
* [Transport Protocol Adapters](#transport-protocol-adapters)
* [Specialized Bridges](#specialized-bridges)

---

## Official Anthropic Tools

### @modelcontextprotocol/inspector

* **Repository:** https://github.com/modelcontextprotocol/inspector
* **Stars:** ~7,900
* **Language:** TypeScript/JavaScript (Node.js + React)
* **Status:** Official Anthropic project ✓
* **Description:** Visual testing tool for MCP servers with both web UI and CLI mode. Includes MCP Proxy (MCPP) that bridges protocol transports (stdio, SSE, streamable-http) and MCP Inspector Client (MCPI) for interactive testing
* **Key Features:**
  * Browser-based UI at localhost:6274
  * CLI mode for scripting: `npx @modelcontextprotocol/inspector --cli`
  * Configuration file support for multiple servers
  * Docker support
* **npm:** [@modelcontextprotocol/inspector](https://www.npmjs.com/package/@modelcontextprotocol/inspector)

---

## CLI Clients & Interactive Tools

### f/mcptools

* **Repository:** https://github.com/f/mcptools
* **Stars:** ~1,400
* **Language:** Go
* **Last Commit:** March 25, 2025
* **Description:** Comprehensive Go-based CLI for discovering and interacting with MCP servers. Supports both stdio and HTTP transport
* **Key Features:**
  * Commands: tools, resources, prompts, call, shell, web, mock, proxy, alias, configs
  * Multiple output formats (table, JSON, pretty-print)
  * Interactive shell mode
  * Web interface
  * Project scaffolding for TypeScript servers
  * Homebrew installation: `brew tap f/mcptools && brew install mcp`

### chrishayuk/mcp-cli

* **Repository:** https://github.com/chrishayuk/mcp-cli
* **Stars:** ~1,800
* **Language:** Python
* **Last Commit:** November 30, 2024
* **Description:** Feature-rich Python CLI for MCP servers with integrated LLM support
* **Key Features:**
  * Multiple modes: Chat (streaming), Interactive (command shell), Command (Unix pipeable)
  * Defaults to Ollama with gpt-oss for local privacy-focused operation
  * Supports cloud providers (OpenAI, Anthropic, Azure)
  * CHUK Tool Processor integration
  * No API keys required for local mode

### adhikasp/mcp-client-cli

* **Repository:** https://github.com/adhikasp/mcp-client-cli
* **Stars:** ~635
* **Language:** Python
* **Description:** Simple CLI to run LLM prompts with MCP client implementation. Alternative to Claude Desktop
* **Key Features:**
  * Works with any LLM provider (OpenAI, Groq, local models via llama)
  * MCP server config via JSON
  * Terminal-based interface

### moritalous/mcp-tools-cli

* **Repository:** https://github.com/moritalous/mcp-tools-cli
* **Stars:** ~2
* **Language:** Python (100%)
* **Last Commit:** March 23, 2025
* **Description:** Command-line client for interacting with MCP servers
* **Key Features:**
  * list-tools: Lists available tools on MCP server
  * call-tool: Calls specific tool on MCP server
  * Install via pip
  * Configuration via mcp_config.json

### mcp-use/mcp-use-cli

* **Repository:** https://github.com/mcp-use/mcp-use-cli
* **Stars:** ~48
* **Language:** TypeScript (99.2%)
* **Last Commit:** November 24, 2025 (archived)
* **Status:** Archived - successor: [@mcp-use/cli](https://www.npmjs.com/package/@mcp-use/cli)
* **Description:** Terminal interface for MCP servers using natural language with multiple LLM providers

### johnlindquist/mcp-list-tools

* **Repository:** https://github.com/johnlindquist/mcp-list-tools
* **Description:** Simplified command-line wrapper around official @modelcontextprotocol/inspector
* **Key Features:**
  * Simplifies complex inspector commands
  * List tools: `npx mcp-list-tools node build/index.js`
  * Options: --resources, --prompts, --transport
  * Supports Node.js, Python, NPM packages, remote servers

---

## HTTP/SSE/WebSocket Bridges

### sparfenyuk/mcp-proxy

* **Repository:** https://github.com/sparfenyuk/mcp-proxy
* **Stars:** ~2,100
* **Language:** Python
* **Last Commit:** December 26, 2024
* **Description:** Bidirectional bridge between Streamable HTTP and stdio MCP transports
* **Key Features:**
  * Client mode: Connect stdio to remote SSE/StreamableHTTP servers
  * Server mode: Expose local stdio servers via HTTP for remote access
  * SSE server with configurable port
  * MIT licensed, 95 commits

### brrock/mcp-bridge

* **Repository:** https://github.com/brrock/mcp-bridge
* **Stars:** ~8
* **Language:** TypeScript (94.5%)
* **Last Commit:** June 1, 2025
* **Description:** Converts STDIO MCP servers to SSE/HTTP for serverless environments
* **Key Features:**
  * SSE and streamable HTTP transport
  * Management interface
  * Configuration generator
  * PostgreSQL database support
  * Redis session management
  * One-command deployment
  * Vercel-optimized

### StanNieuwmans/mcp-bridge

* **Repository:** https://github.com/StanNieuwmans/mcp-bridge
* **Description:** Lightweight STDIO to SSE bridge for Claude Desktop
* **Key Features:**
  * Connects Claude Desktop (STDIO) to MCP backends (SSE)
  * POSTs to /messages endpoint
  * Opens SSE connection to /sse endpoint
  * Node.js v18+ required
  * Configuration via Claude Desktop config.json

### nccgroup/http-mcp-bridge

* **Repository:** https://github.com/nccgroup/http-mcp-bridge
* **Language:** Python
* **Last Commit:** November 13, 2025
* **Source:** NCC Group (cybersecurity firm)
* **Description:** HTTP/1.1 to SSE bridge specifically for security testing MCP servers
* **Key Features:**
  * Designed for HTTP security tool integration
  * Multi-session support with session IDs
  * Configurable timeout parameters
  * Run: `python3 main.py --remote-url="http://127.0.0.1:8787/sse"`
  * HTTP server on localhost:8000
  * MIT licensed

### sidharthrajaram/mcp-sse

* **Repository:** https://github.com/sidharthrajaram/mcp-sse
* **Description:** Working pattern for SSE-based MCP servers and standalone clients
* **Key Features:**
  * Demonstrates decoupled processes
  * Agents connect/disconnect dynamically
  * Server as running process, not stdio subprocess
  * Node-to-node distribution capable

### supercorp-ai/supergateway

* **Repository:** https://github.com/supercorp-ai/supergateway
* **Description:** Bidirectional MCP gateway for stdio↔SSE and stdio↔WebSocket
* **Key Features:**
  * stdio→SSE mode: Convert stdio server to SSE endpoint
  * SSE→stdio mode: Connect to remote SSE, expose local stdio
  * WebSocket support
  * Automatic JSON-RPC versioning
  * Package metadata retransmission
  * Docker images: supercorp/supergateway, ghcr.io/supercorp-ai/supergateway
  * --minConcurrency/--maxConcurrency for process control
  * Streamable HTTP to stdio support
  * Claude Desktop and Cursor integration

---

## REST API & OpenAPI Wrappers

### Vizioz/Swagger-MCP

* **Repository:** https://github.com/Vizioz/Swagger-MCP
* **Stars:** ~108
* **Language:** TypeScript (97.9%)
* **Last Commit:** March 8, 2025
* **Description:** MCP server generator from Swagger/OpenAPI specifications
* **Key Features:**
  * JSON and YAML Swagger support
  * Complete schema info including nested objects
  * Auto-download and cache Swagger definitions
  * TypeScript code generation for MCP tools
  * `--swagger-url` argument for remote specs

### ckanthony/openapi-mcp

* **Repository:** https://github.com/ckanthony/openapi-mcp
* **Stars:** ~79-131 (varies by source)
* **Language:** Go
* **Description:** Dockerized MCP server for any API with OpenAPI docs
* **Key Features:**
  * OpenAPI v2 (Swagger) & v3 support
  * Local and remote spec support
  * Automatic MCP tool generation from operations
  * JSON Schema from parameters and request/response
  * Secure API key handling
  * Docker Hub: ckanthony/openapi-mcp:latest

### danishjsheikh/swagger-mcp

* **Repository:** https://github.com/danishjsheikh/swagger-mcp
* **Description:** Dynamically defines MCP tools from Swagger specs
* **Key Features:**
  * Run: `swagger-mcp --specUrl=https://your_swagger_api_docs.json`
  * Base URL override support
  * Multiple auth types: basic, apiKey, bearer

### matthewhand/mcp-openapi-proxy

* **Repository:** https://github.com/matthewhand/mcp-openapi-proxy
* **Language:** Python
* **Description:** Python MCP server exposing OpenAPI REST APIs as MCP tools
* **Key Features:**
  * Dynamic tool generation from OpenAPI endpoints
  * Seamless OpenAPI→MCP workflow integration

### andersmandersen/mcp-swagger

* **Repository:** https://github.com/andersmandersen/mcp-swagger
* **Description:** MCP server for Swagger/OpenAPI documentation access and API requests

### LostInBrittany/swagger-to-mcp-generator

* **Repository:** https://github.com/LostInBrittany/swagger-to-mcp-generator
* **Language:** Java
* **Description:** Java program generating Quarkus MCP servers from OpenAPI/Swagger
* **Key Features:**
  * Quarkus framework
  * Auto-generates MCP handlers from .proto services
  * LLM↔REST API interaction

### dcolley/swagger-mcp

* **Repository:** https://github.com/dcolley/swagger-mcp
* **Description:** Ingests and serves Swagger/OpenAPI specs through MCP

---

## Enterprise Gateways & Proxies

### microsoft/mcp-gateway

* **Repository:** https://github.com/microsoft/mcp-gateway
* **Stars:** ~386
* **Language:** .NET/C#
* **Source:** Microsoft ✓
* **Description:** Reverse proxy and management layer for MCP servers in Kubernetes
* **Key Features:**
  * Session-aware stateful routing
  * Lifecycle management (deploy, update, delete)
  * Data gateway with session affinity
  * Control plane for server management
  * Enterprise telemetry and access control
  * Observability integration
  * Dynamic tool routing via tool gateway router
  * Kubernetes-optimized

### acehoss/mcp-gateway

* **Repository:** https://github.com/acehoss/mcp-gateway
* **Stars:** ~128
* **Language:** TypeScript (100%)
* **Last Commit:** December 18, 2024
* **Description:** Flexible gateway bridging MCP STDIO to HTTP+SSE and REST API
* **Key Features:**
  * Multi-instance MCP server support
  * REST API interface (OpenAPI/Swagger compatible)
  * OpenAI custom GPTs integration
  * HTTP client access for containerized environments (LibreChat)
  * Remote machine MCP server exposure

### lasso-security/mcp-gateway

* **Repository:** https://github.com/lasso-security/mcp-gateway
* **Source:** Lasso Security (cybersecurity firm) ✓
* **Description:** Plugin-based security gateway orchestrating multiple MCPs
* **Key Features:**
  * Guardrail plugins: basic, presidio (PII masking), lasso (full features)
  * Token/Secret masking
  * PII masking
  * Custom policy enforcement
  * Prompt injection detection
  * Harmful content filtering
  * Security scanner (v1.1.0) for malicious server detection
  * MCP risk scoring
  * Unified dashboard
  * Real-time monitoring
  * Central router and management

### hyprmcp/mcp-gateway

* **Repository:** https://github.com/hyprmcp/mcp-gateway
* **Source:** Hypr MCP
* **Description:** OAuth proxy with dynamic client registration for streamable HTTP MCP servers
* **Key Features:**
  * 1-click OAuth authorization
  * Dynamic Client Registration (DCR)
  * MCP prompt analytics
  * MCP firewall
  * OAuth2.1 compliance
  * Authorization Server Metadata (ASM)
  * Zero-code OAuth for MCP servers
  * Enterprise-grade security
* **Related:** [hyprmcp/jetski](https://github.com/hyprmcp/jetski) - Authentication, analytics, prompt visibility with zero code changes

### TBXark/mcp-proxy

* **Repository:** https://github.com/TBXark/mcp-proxy
* **Stars:** ~590
* **Language:** Go
* **Description:** MCP proxy aggregating multiple servers through single HTTP endpoint
* **Key Features:**
  * Aggregate tools, prompts, resources from many servers
  * SSE and streamable HTTP support
  * Flexible config: stdio, sse, streamable-http
  * Install: `go install github.com/TBXark/mcp-proxy@latest`
  * Docker: `docker run ghcr.io/tbxark/mcp-proxy:latest`
  * MIT licensed

### matthisholleville/mcp-gateway

* **Repository:** https://github.com/matthisholleville/mcp-gateway
* **Description:** Flexible proxy gateway with enterprise middleware
* **Key Features:**
  * Authentication and authorization
  * Rate limiting
  * Observability
  * Middleware system

### lucky-aeon/mcp-gateway

* **Repository:** https://github.com/lucky-aeon/mcp-gateway
* **Description:** Reverse proxy forwarding client requests to MCP servers
* **Key Features:**
  * Unified portal for all MCP servers
  * Request forwarding

---

## Transport Protocol Adapters

### mcp-remote (npm)

* **Package:** [mcp-remote](https://www.npmjs.com/package/mcp-remote)
* **Version:** 0.1.31
* **Used by:** 20+ npm projects
* **Description:** Remote proxy adapter for stdio-only MCP clients to access HTTP+SSE servers with OAuth
* **Key Features:**
  * OAuth 2.0 and Bearer token auth
  * Forwards STDIO traffic to remote HTTP+SSE servers
  * `--allow-http` flag for trusted networks
  * `--transport sse-only` for SSE-only mode
  * `--ignore-tool` for filtering tools
  * `--enable-proxy` for HTTP(S) proxy via environment variables
  * Run: `npx -p mcp-remote@latest mcp-remote-client https://remote.mcp.server/sse`
* **Usage Example:**
  ```json
  {
    "command": "npx",
    "args": ["-y", "mcp-remote", "https://remote.mcp.server/sse"]
  }
  ```

### @pyroprompts/mcp-stdio-to-streamable-http-adapter

* **Package:** [@pyroprompts/mcp-stdio-to-streamable-http-adapter](https://www.npmjs.com/package/@pyroprompts/mcp-stdio-to-streamable-http-adapter)
* **Description:** MCP server wrapping Streamable HTTP servers for stdio clients
* **Key Features:**
  * Runs as stdio process
  * Wraps Streamable HTTP servers
  * Enables any stdio-supporting client to use Streamable HTTP MCP servers

### @langchain/mcp-adapters

* **Package:** [@langchain/mcp-adapters](https://www.npmjs.com/package/@langchain/mcp-adapters)
* **Description:** LangChain adapters for MCP servers
* **Key Features:**
  * Connect via stdio (local) or Streamable HTTP (remote)
  * Automatic fallback from Streamable HTTP to SSE
  * Custom headers for authentication in SSE

### @vercel/mcp-adapter

* **Package:** [@vercel/mcp-adapter](https://www.npmjs.com/package/@vercel/mcp-adapter)
* **Description:** Vercel adapter for MCP enabling real-time AI model communication
* **Key Features:**
  * Next.js support (more frameworks coming)
  * Real-time communication

### supergateway (npm)

* **Package:** [supergateway](https://www.npmjs.com/package/supergateway)
* **Description:** Converts MCP stdio servers to SSE or WS services
* **Key Features:**
  * `--sse` for SSE URL connections
  * `--streamableHttp` for Streamable HTTP URLs
  * `--outputTransport` options: stdio, sse, ws, streamableHttp
  * Simplifies web client integration and debugging

---

## Specialized Bridges

### GongRzhe/ACP-MCP-Server

* **Repository:** https://github.com/GongRzhe/ACP-MCP-Server
* **Description:** Bridge between Agent Communication Protocol (ACP) and MCP
* **Key Features:**
  * ACP agent ↔ MCP client integration
  * Multiple transports: STDIO, SSE, Streamable HTTP
  * Enables ACP-based AI agents with MCP tools (Claude Desktop)

### iflow-mcp/http-oauth-mcp-server-1

* **Repository:** https://github.com/iflow-mcp/http-oauth-mcp-server-1
* **Description:** Remote MCP server implementing OAuth authorization extension
* **Key Features:**
  * SSE + Streamable HTTP
  * OAuth 2.0 based on MCP spec (added March 25, 2025)
  * Direct agent usage or via mcp-remote from Cursor/Claude
  * OAuth spec implementation in TypeScript SDK (as of May 1, 2025)

### Leantime/leantime-mcp

* **Repository:** https://github.com/Leantime/leantime-mcp
* **Description:** MCP client bridge to Leantime MCP Server
* **Key Features:**
  * HTTP/HTTPS transport
  * Server-Sent Events (SSE)
  * Streaming responses
  * MCP protocol version 2025-03-26 (latest)
  * Backward compatibility

### tuannvm/codex-mcp-server

* **Repository:** https://github.com/tuannvm/codex-mcp-server
* **Description:** MCP wrapper for OpenAI Codex CLI enabling Claude Code integration
* **Key Features:**
  * Codex CLI v0.50.0+ support
  * Session management
  * Model selection
  * Native resume support

### LanceVCS/codex-mcp

* **Repository:** https://github.com/LanceVCS/codex-mcp
* **Description:** Stateful MCP server for Codex CLI
* **Key Features:**
  * Claude Code ↔ Codex interaction
  * JSON-RPC protocol translation
  * Translates MCP codex tool calls to `codex exec --json` commands

### conorluddy/xc-mcp

* **Repository:** https://github.com/conorluddy/xc-mcp
* **Description:** XCode CLI MCP wrapper for iOS Simulator
* **Key Features:**
  * Convenience wrapper for Xcode CLI tools
  * Progressive disclosure of responses
  * `--mini` param for build-only with tiny context
  * Reduces context usage
  * AI agent accessibility

### Oliver0804/arduino-cli-mcp

* **Repository:** https://github.com/Oliver0804/arduino-cli-mcp
* **Description:** MCP wrapper for Arduino CLI
* **Key Features:**
  * Auto-approval of repetitive operations
  * Simplified Arduino workflows
  * Useful for developers and educators

---

## Additional Bridge Projects

### Apache APISIX mcp-bridge Plugin

* **Source:** Apache APISIX API Gateway
* **Documentation:** [Host MCP Server with APISIX](https://apisix.apache.org/blog/2025/04/21/host-mcp-server-with-api-gateway/)
* **Description:** Bridges stdio-based MCP services with modern API architectures
* **Key Features:**
  * Converts stdio to HTTP SSE streaming interfaces
  * API gateway routing and traffic management
  * Enterprise integration

### Azure API Management MCP Adapter

* **Source:** Microsoft Azure
* **Documentation:** [Expose REST API as MCP Server](https://learn.microsoft.com/en-us/azure/api-management/export-rest-mcp-server)
* **Description:** Exposes REST APIs managed in API Management as remote MCP servers
* **Key Features:**
  * Built-in AI gateway
  * One or more API operations as MCP tools
  * No rebuilding or rehosting required
  * Enterprise Azure integration

### Gravitee MCP Gateway

* **Source:** Gravitee.io
* **Description:** Gateway between AI clients and MCP servers
* **Key Features:**
  * Routing, authentication, caching
  * Transport adaptation
  * stdio and HTTP/SSE support
  * Local and remote integration

### GPT-MCP-Proxy (Skywork AI)

* **Source:** Skywork AI
* **Description:** RESTful bridge aggregating backend MCP servers
* **Key Features:**
  * Define all MCP servers in mcp_settings.json
  * Proxy aggregates tools
  * Single unified REST API

---

## Related Security & Testing Tools

### slowmist/MCP-Security-Checklist

* **Repository:** https://github.com/slowmist/MCP-Security-Checklist
* **Source:** SlowMist (blockchain security firm)
* **Description:** Comprehensive security checklist for MCP-based AI tools
* **Purpose:** Safeguard LLM plugin ecosystems

### cyproxio/mcp-for-security

* **Repository:** https://github.com/cyproxio/mcp-for-security
* **Description:** Collection of MCP servers for security tools
* **Tools:** SQLMap, FFUF, NMAP, Masscan, and more
* **Purpose:** Integrate security testing and penetration testing into AI workflows

### cisco-ai-defense/mcp-scanner

* **Repository:** https://github.com/cisco-ai-defense/mcp-scanner
* **Source:** Cisco AI Defense
* **Description:** Scan MCP servers for potential threats and security findings

---

## Summary Statistics

### By Category

* **CLI Clients:** 7 tools
* **HTTP/SSE/WebSocket Bridges:** 9 tools
* **REST API/OpenAPI Wrappers:** 8 tools
* **Enterprise Gateways:** 6 tools
* **Transport Adapters:** 6 npm packages
* **Specialized Bridges:** 9 tools
* **Security Tools:** 3 tools

### By Language

* **TypeScript/JavaScript:** 15+ projects
* **Python:** 8+ projects
* **Go:** 3 projects
* **C#/.NET:** 1 project (Microsoft)
* **Java:** 1 project

### By Source Reputation

* **Official Anthropic:** 1 (@modelcontextprotocol/inspector)
* **Major Companies:** Microsoft, Azure, Apache, Vercel, Gravitee
* **Security Firms:** NCC Group, Lasso Security, SlowMist, Cisco
* **Active Community:** 30+ independent developers and organizations

### Most Starred Projects

1. @modelcontextprotocol/inspector: ~7,900 stars (Official)
2. sparfenyuk/mcp-proxy: ~2,100 stars
3. chrishayuk/mcp-cli: ~1,800 stars
4. f/mcptools: ~1,400 stars
5. adhikasp/mcp-client-cli: ~635 stars
6. TBXark/mcp-proxy: ~590 stars
7. microsoft/mcp-gateway: ~386 stars

---

## Research Methodology

This research was conducted on December 16, 2025, using:

* Web search queries targeting MCP CLI wrappers, REST gateways, HTTP bridges, transport adapters
* GitHub repository analysis for stars, languages, commit dates, descriptions
* npm package registry searches
* Official documentation from Anthropic, Microsoft, Apache, Azure
* Community resources: LobeHub, MCP Servers directory, PulseMCP, MCPHub

---

## Sources

* [GitHub - chrishayuk/mcp-cli](https://github.com/chrishayuk/mcp-cli)
* [GitHub - f/mcptools](https://github.com/f/mcptools)
* [GitHub - modelcontextprotocol/inspector](https://github.com/modelcontextprotocol/inspector)
* [GitHub - acehoss/mcp-gateway](https://github.com/acehoss/mcp-gateway)
* [GitHub - microsoft/mcp-gateway](https://github.com/microsoft/mcp-gateway)
* [GitHub - sparfenyuk/mcp-proxy](https://github.com/sparfenyuk/mcp-proxy)
* [GitHub - TBXark/mcp-proxy](https://github.com/TBXark/mcp-proxy)
* [GitHub - Vizioz/Swagger-MCP](https://github.com/Vizioz/Swagger-MCP)
* [GitHub - ckanthony/openapi-mcp](https://github.com/ckanthony/openapi-mcp)
* [GitHub - lasso-security/mcp-gateway](https://github.com/lasso-security/mcp-gateway)
* [GitHub - hyprmcp/mcp-gateway](https://github.com/hyprmcp/mcp-gateway)
* [GitHub - supercorp-ai/supergateway](https://github.com/supercorp-ai/supergateway)
* [npm - mcp-remote](https://www.npmjs.com/package/mcp-remote)
* [MCP Tools CLI - fka.dev blog](https://blog.fka.dev/blog/2025-03-26-introducing-mcp-tools-cli/)
* [Azure API Management MCP Integration](https://learn.microsoft.com/en-us/azure/api-management/export-rest-mcp-server)
* [Apache APISIX MCP Bridge](https://apisix.apache.org/blog/2025/04/21/host-mcp-server-with-api-gateway/)
* [NCC Group http-mcp-bridge](https://github.com/nccgroup/http-mcp-bridge)
* [Lasso Security MCP Gateway Announcement](https://www.lasso.security/resources/lasso-releases-first-open-source-security-gateway-for-mcp)

---

## Notes

* Star counts are approximate as of research date and may have changed
* Last commit dates are based on repository metadata when available
* Some projects have multiple forks and variations; primary repositories are listed
* OAuth support in MCP was added to specification on March 25, 2025
* Many tools support both stdio and HTTP/SSE transports for flexibility
* Enterprise gateways focus on Kubernetes, security, observability, and multi-tenant scenarios
* Community is very active with new tools emerging regularly
