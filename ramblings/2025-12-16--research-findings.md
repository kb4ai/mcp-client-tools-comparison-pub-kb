# MCP Wrapper Tools Research Findings

**Date:** 2025-12-16

## Summary

Comprehensive research identified **70+ tools** in the MCP ecosystem that wrap, bridge, or expose Model Context Protocol servers through various interfaces.

## Key Categories

### 1. CLI Clients

* **f/mcptools** (Go, ~1.4k stars): Industrial-strength CLI with Homebrew distribution, supports stdio+HTTP, provides web UI
* **chrishayuk/mcp-cli** (Python, ~1.8k stars): LLM-integrated CLI, defaults to Ollama for privacy-centric local operation
* **adhikasp/mcp-client-cli** (Python, ~655 stars): Minimalist alternative to Claude Desktop
* **wong2/mcp-cli** (JavaScript, ~396 stars): Scriptable CLI inspector with automation support

### 2. HTTP/SSE Bridges

* **sparfenyuk/mcp-proxy** (Python, ~2.1k stars): Bidirectional Streamable HTTP↔stdio bridge (most starred community project)
* **supercorp-ai/supergateway**: Multi-protocol support (stdio↔SSE, stdio↔WS, SSE↔stdio)
* **brrock/mcp-bridge** (TypeScript): Serverless-optimized (Vercel)
* **nccgroup/http-mcp-bridge** (Python): Security testing focused

### 3. REST API & OpenAPI Wrappers

* **Vizioz/Swagger-MCP** (TypeScript, ~108 stars): Generates TypeScript MCP tools from OpenAPI specs
* **ckanthony/openapi-mcp** (Go, ~79-131 stars): Dockerized solution for OpenAPI v2+v3

### 4. Enterprise Gateways

* **microsoft/mcp-gateway** (C#, ~386 stars): K8s-native reverse proxy with lifecycle management
* **lasso-security/mcp-gateway**: Security-first with PII masking, prompt injection detection
* **TBXark/mcp-proxy** (Go, ~592 stars): Aggregator proxy for multiple MCP servers

### 5. gRPC/Protobuf Converters

* **redpanda-data/protoc-gen-go-mcp** (Go, ~177 stars): Official protoc plugin from Redpanda
* **adiom-data/grpcmcp** (Go): MCP server proxying to gRPC backend

### 6. WebSocket Transports

* **ConechoAI/nchan-mcp-transport** (TypeScript/Python): High-performance WebSocket/SSE layer
* **yonaka15/mcp-server-runner**: WebSocket server for running MCP servers

### 7. Docker & Kubernetes

* **docker/mcp-gateway**: Official Docker integration with container isolation
* **containers/kubernetes-mcp-server**: Native Go K8s implementation (not a kubectl wrapper)

## Language Distribution

* TypeScript/JavaScript: 15+ projects
* Python: 8+ projects
* Go: 5+ projects
* C#/.NET: 1 project (Microsoft)
* Rust: 1 project (enterprise proxy)

## Official/Reputable Sources

* Anthropic: @modelcontextprotocol/inspector
* Microsoft: mcp-gateway
* Docker: mcp-gateway, mcp-registry
* GitHub: github-mcp-server
* Redpanda: protoc-gen-go-mcp
* Security firms: NCC Group, Lasso Security, Pangea Cyber

## Security Considerations for Analysis

When analyzing these tools, check for:

1. **Network behavior**: Only connects to configured MCP servers?
2. **Code execution**: Presence of `eval`, `exec`, `subprocess` with user input?
3. **Command injection**: Input sanitization before shell execution?
4. **Transport support**: stdio, SSE, HTTP, WebSocket?
5. **Authentication**: OAuth, API keys, bearer tokens?
6. **Isolation**: Docker/container support, sandboxing?

## Priority Projects for YAML Files

Based on stars, reputation, and relevance:

1. sparfenyuk/mcp-proxy (~2.1k stars)
2. chrishayuk/mcp-cli (~1.8k stars)
3. f/mcptools (~1.4k stars)
4. adhikasp/mcp-client-cli (~655 stars)
5. TBXark/mcp-proxy (~592 stars)
6. wong2/mcp-cli (~396 stars)
7. microsoft/mcp-gateway (~386 stars)
8. MCP-connect/EvalsOne (~227 stars)
9. redpanda-data/protoc-gen-go-mcp (~177 stars)
10. cli-mcp-server/MladenSU (~155 stars)

## Transport Categories

* **stdio↔HTTP/SSE**: 10+ bridges
* **WebSocket**: 5+ implementations
* **gRPC/Protobuf**: 6+ converters
* **REST API**: 5+ bridges
