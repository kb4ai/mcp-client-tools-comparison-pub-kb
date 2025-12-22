# Transport Support Details

## Overview

MCP (Model Context Protocol) defines several transport mechanisms for communication between clients and servers. This document provides a comprehensive analysis of which tools support which transports, transport combinations, bridge directions, and implementation patterns.

**Key insight:** While stdio is the universal baseline (96.3% adoption), many tools extend support to HTTP/SSE for remote access, with emerging support for WebSocket and gRPC for specialized use cases.

## Transport Statistics

| Transport | Projects | Percentage | Use Case |
|-----------|----------|------------|----------|
| stdio | 26 | 96.3% | Universal baseline, local process communication |
| HTTP | 13 | 48.1% | Remote access, REST APIs, web integration |
| SSE | 8 | 29.6% | Server-Sent Events for streaming responses |
| WebSocket | 2 | 7.4% | Bidirectional real-time communication |
| gRPC | 1 | 3.7% | High-performance RPC, service mesh integration |

**Total projects analyzed:** 27

## Transport Matrix

Full matrix of all projects and their transport support:

| Project | stdio | SSE | HTTP | WebSocket | gRPC |
|---------|:-----:|:---:|:----:|:---------:|:----:|
| [mcp-proxy](https://github.com/sparfenyuk/mcp-proxy) | ✓ | ✓ | ✓ |  |  |
| [mcp-cli](https://github.com/chrishayuk/mcp-cli) | ✓ |  |  |  |  |
| [mcptools](https://github.com/f/mcptools) | ✓ | ✓ | ✓ |  |  |
| [MCP-Bridge](https://github.com/SecretiveShell/MCP-Bridge) | ✓ |  | ✓ |  |  |
| [mcp-client-cli](https://github.com/adhikasp/mcp-client-cli) | ✓ |  |  |  |  |
| [mcp-proxy (TBXark)](https://github.com/TBXark/mcp-proxy) | ✓ | ✓ | ✓ |  |  |
| [mcp-cli (wong2)](https://github.com/wong2/mcp-cli) | ✓ | ✓ | ✓ |  |  |
| [mcp-gateway](https://github.com/microsoft/mcp-gateway) | ✓ |  | ✓ |  |  |
| [MCP-connect](https://github.com/EvalsOne/MCP-connect) | ✓ |  | ✓ |  |  |
| [protoc-gen-go-mcp](https://github.com/redpanda-data/protoc-gen-go-mcp) | ✓ |  |  |  | ✓ |
| [cli-mcp-server](https://github.com/MladenSU/cli-mcp-server) | ✓ |  |  |  |  |
| [mcp-gateway (acehoss)](https://github.com/acehoss/mcp-gateway) | ✓ |  | ✓ |  |  |
| [mcp-use-cli](https://github.com/mcp-use/mcp-use-cli) | ✓ |  |  |  |  |
| [nchan-mcp-transport](https://github.com/ConechoAI/nchan-mcp-transport) |  | ✓ | ✓ | ✓ |  |
| [mcp-cli (Deniscartin)](https://github.com/Deniscartin/mcp-cli) | ✓ |  |  |  |  |
| [kubernetes-mcp-server](https://github.com/containers/kubernetes-mcp-server) | ✓ |  |  |  |  |
| [Docker MCP Gateway](https://github.com/docker/mcp-gateway) | ✓ |  | ✓ |  |  |
| [any-cli-mcp-server](https://github.com/eirikb/any-cli-mcp-server) | ✓ |  |  |  |  |
| [mcp-server-commands](https://github.com/g0t4/mcp-server-commands) | ✓ |  |  |  |  |
| [Lasso MCP Gateway](https://github.com/lasso-security/mcp-gateway) | ✓ |  | ✓ |  |  |
| [MCP Inspector](https://github.com/modelcontextprotocol/inspector) | ✓ | ✓ | ✓ |  |  |
| [http-mcp-bridge](https://github.com/nccgroup/http-mcp-bridge) | ✓ | ✓ | ✓ |  |  |
| [mcptools (R)](https://github.com/posit-dev/mcptools) | ✓ |  |  |  |  |
| [win-cli-mcp-server](https://github.com/simon-ami/win-cli-mcp-server) | ✓ |  |  |  |  |
| [mcporter](https://github.com/steipete/mcporter) | ✓ |  |  |  |  |
| [supergateway](https://github.com/supercorp-ai/supergateway) | ✓ | ✓ |  | ✓ |  |
| [mcpcli](https://github.com/winterfx/mcpcli) | ✓ |  |  |  |  |

## By Transport Type

### stdio (Standard I/O)

**Adoption:** 26/27 projects (96.3%)

Universal baseline transport for MCP. Nearly all tools support stdio as it's the foundational transport mechanism defined in the MCP specification.

**Typical use cases:**

* Local process-to-process communication
* CLI tools and command-line automation
* Docker container communication
* Kubernetes pod-to-pod communication
* Development and testing environments

**stdio-only projects (12 total):**

* **CLI clients:** mcp-cli (chrishayuk), mcp-client-cli, mcp-use-cli, mcptools (R), mcporter, mcpcli, mcp-cli (Deniscartin)
* **Specialized adapters:** any-cli-mcp-server, mcp-server-commands, win-cli-mcp-server, cli-mcp-server
* **Platform integrations:** kubernetes-mcp-server

These tools focus on local, secure, process-isolated communication without network exposure.

### HTTP/Streamable HTTP

**Adoption:** 13/27 projects (48.1%)

Projects that bridge stdio to HTTP or provide HTTP-based access to MCP servers.

| Project | Direction | Category | Auth Support | Stars |
|---------|-----------|----------|--------------|-------|
| [mcp-proxy](https://github.com/sparfenyuk/mcp-proxy) | bidirectional | http-bridge | OAuth, Bearer | 2100 |
| [mcp-gateway](https://github.com/microsoft/mcp-gateway) | not specified | enterprise-gateway | OAuth, Bearer | 386 |
| [MCP-Bridge](https://github.com/SecretiveShell/MCP-Bridge) | not specified | rest-api-bridge | None | 882 |
| [MCP-connect](https://github.com/EvalsOne/MCP-connect) | stdio→http | http-bridge | None | 227 |
| [mcp-gateway (acehoss)](https://github.com/acehoss/mcp-gateway) | not specified | rest-api-bridge | None | 128 |
| [Docker MCP Gateway](https://github.com/docker/mcp-gateway) | not specified | docker-integration | None | ? |
| [Lasso MCP Gateway](https://github.com/lasso-security/mcp-gateway) | not specified | enterprise-gateway | None | ? |
| [http-mcp-bridge](https://github.com/nccgroup/http-mcp-bridge) | not specified | http-bridge | None | ? |
| [nchan-mcp-transport](https://github.com/ConechoAI/nchan-mcp-transport) | not specified | websocket-bridge | None | 28 |
| [mcptools](https://github.com/f/mcptools) | not specified | cli-client | None | 1400 |
| [mcp-proxy (TBXark)](https://github.com/TBXark/mcp-proxy) | aggregator | proxy-aggregator | None | 592 |
| [mcp-cli (wong2)](https://github.com/wong2/mcp-cli) | not specified | cli-client | OAuth | 396 |
| [MCP Inspector](https://github.com/modelcontextprotocol/inspector) | not specified | official-tool | None | ? |

**Key capabilities:**

* **Remote access:** Expose local MCP servers over HTTP for remote clients
* **Web integration:** Enable browser-based and web API access
* **Load balancing:** Distribute requests across multiple MCP servers
* **Authentication:** OAuth2, bearer tokens, API keys for secure access
* **Dual-mode operation:** Both Streamable HTTP and classic request/response

### SSE (Server-Sent Events)

**Adoption:** 8/27 projects (29.6%)

Projects supporting real-time streaming via Server-Sent Events, enabling efficient push-based communication.

**Projects with SSE support:**

| Project | Additional Transports | Category | Stars |
|---------|---------------------|----------|-------|
| [mcp-proxy](https://github.com/sparfenyuk/mcp-proxy) | stdio, http | http-bridge | 2100 |
| [mcptools](https://github.com/f/mcptools) | stdio, http | cli-client | 1400 |
| [mcp-proxy (TBXark)](https://github.com/TBXark/mcp-proxy) | stdio, http | proxy-aggregator | 592 |
| [mcp-cli (wong2)](https://github.com/wong2/mcp-cli) | stdio, http | cli-client | 396 |
| [MCP Inspector](https://github.com/modelcontextprotocol/inspector) | stdio, http | official-tool | ? |
| [http-mcp-bridge](https://github.com/nccgroup/http-mcp-bridge) | stdio, http | http-bridge | ? |
| [supergateway](https://github.com/supercorp-ai/supergateway) | stdio, websocket | http-bridge | ? |
| [nchan-mcp-transport](https://github.com/ConechoAI/nchan-mcp-transport) | http, websocket | websocket-bridge | 28 |

**Use cases:**

* Streaming LLM responses in real-time
* Long-running task progress updates
* Event notifications from MCP servers
* Reduced latency for interactive applications

**Notable:** All SSE implementations also support HTTP, indicating SSE is typically added as an enhancement to HTTP-based transports rather than a standalone transport.

### WebSocket

**Adoption:** 2/27 projects (7.4%)

Projects with WebSocket support for bidirectional real-time communication.

**Projects:**

1. **[nchan-mcp-transport](https://github.com/ConechoAI/nchan-mcp-transport)** (28 stars)
   * Category: websocket-bridge
   * Additional transports: SSE, HTTP
   * Built on: Nginx + Nchan + FastAPI
   * Purpose: High-performance real-time communication, addresses HTTP+SSE limitations for long tasks
   * Languages: TypeScript, Python, JavaScript

2. **[supergateway](https://github.com/supercorp-ai/supergateway)** (? stars)
   * Category: http-bridge
   * Additional transports: stdio, SSE
   * Purpose: Multi-protocol transport adapter (stdio↔SSE, stdio↔WS, SSE↔stdio)
   * Docker-first design

**Why WebSocket?**

* Bidirectional streaming for interactive sessions
* Lower overhead than HTTP polling or SSE for high-frequency updates
* Better support for complex stateful interactions
* Addressing limitations of HTTP+SSE for long-running tasks

### gRPC/Protobuf

**Adoption:** 1/27 projects (3.7%)

**Project:**

**[protoc-gen-go-mcp](https://github.com/redpanda-data/protoc-gen-go-mcp)** (177 stars)

* Organization: Redpanda (reputable source)
* Category: grpc-bridge
* Language: Go
* License: Apache-2.0
* Additional transport: stdio

**Key features:**

* protoc plugin generating MCP servers from gRPC/ConnectRPC APIs
* Auto-generates JSON Schema for tool inputs from method descriptors
* Generates `*.pb.mcp.go` files per protobuf service
* Direct forwarding of MCP tool calls to gRPC clients
* Runtime LLM provider selection
* Uses mark3labs/mcp-go as MCP server runtime

**Use cases:**

* Exposing existing gRPC services as MCP tools
* Service mesh integration
* High-performance enterprise environments
* Microservices architecture with MCP interface

## Transport Combinations

Analysis of common transport combinations and their use cases:

| Combination | Count | Use Case | Example Projects |
|-------------|-------|----------|------------------|
| **stdio only** | 12 | Pure CLI tools, local operation | mcp-client-cli, cli-mcp-server, kubernetes-mcp-server |
| **stdio + HTTP** | 6 | Basic HTTP bridges | MCP-connect, MCP-Bridge, Docker MCP Gateway |
| **stdio + HTTP + SSE** | 6 | Full-featured bridges with streaming | mcp-proxy, mcptools, MCP Inspector, http-mcp-bridge |
| **HTTP + SSE + WebSocket** | 1 | Multi-protocol real-time gateway | nchan-mcp-transport |
| **stdio + SSE + WebSocket** | 1 | Multi-protocol adapter | supergateway |
| **stdio + gRPC** | 1 | Service mesh / microservices | protoc-gen-go-mcp |

**Patterns observed:**

* **Progressive enhancement:** Projects start with stdio, add HTTP for remote access, then SSE for streaming
* **Protocol stacking:** SSE always appears with HTTP (SSE requires HTTP as underlying transport)
* **Specialization:** WebSocket and gRPC are used for specific performance or architectural requirements

## Bridge Directions

Some projects explicitly specify their bridging direction:

| Direction | Count | Description | Projects |
|-----------|-------|-------------|----------|
| **bidirectional** | 2 | Full proxy capability, converts in both directions | mcp-proxy (sparfenyuk), supergateway |
| **stdio→http** | 1 | Expose local stdio MCP servers via HTTP | MCP-connect |
| **aggregator** | 1 | Combines multiple MCP servers behind single endpoint | mcp-proxy (TBXark) |
| **not specified** | 23 | Direction not explicitly documented | (various) |

**Bidirectional bridges:**

* **mcp-proxy (sparfenyuk):** Most starred (2100), supports dual-mode operation (stdio→HTTP and HTTP→stdio), OAuth2 support
* **supergateway:** Docker-first design, multiple protocol conversions (stdio↔SSE, stdio↔WS, SSE↔stdio)

**Aggregator pattern:**

* **mcp-proxy (TBXark):** Consolidates tools/prompts/resources from multiple MCP servers into single HTTP endpoint
* Useful for: Multi-server orchestration, unified API surface, simplified client configuration

## Implementation Notes

### Authentication Mechanisms

Projects supporting HTTP transports often implement authentication:

| Project | OAuth | Bearer Token | Notes |
|---------|:-----:|:------------:|-------|
| mcp-proxy (sparfenyuk) | ✓ | ✓ | OAuth2 client credentials support |
| mcp-gateway (Microsoft) | ✓ | ✓ | Enterprise-grade auth |
| mcp-cli (wong2) | ✓ |  | OAuth integration |

### Port Configuration

HTTP-based projects typically support configurable ports:

* **MCP Inspector:** Default 6274 (UI), 6277 (proxy), configurable
* **Most bridges:** Environment variable configuration (e.g., `PORT`, `MCP_PORT`)
* **Best practice:** Non-standard ports to avoid conflicts (see CLAUDE.md guidelines)

### Docker Support

Transport implementations with Docker support:

* **mcp-proxy (sparfenyuk):** Docker support from v0.3.2+
* **supergateway:** Docker-first design
* **Docker MCP Gateway:** Container-based isolation by design
* **MCP Inspector:** Docker deployment available

### Performance Considerations

**stdio:**

* Lowest latency for local communication
* No network overhead
* Limited to single-machine deployments

**HTTP:**

* Network latency overhead
* Stateless, easy to load balance
* Firewall-friendly (standard ports)

**SSE:**

* Efficient for server-to-client streaming
* Lower overhead than polling
* One-directional (server → client)

**WebSocket:**

* Bidirectional streaming
* Lower overhead than HTTP for high-frequency updates
* Requires connection state management

**gRPC:**

* High performance with Protocol Buffers
* Efficient for microservices
* Strong typing and code generation

### Security Patterns

**Enterprise gateways** emphasize security features:

* **Lasso MCP Gateway:** PII masking, token filtering, prompt injection detection, harmful content blocking
* **Microsoft mcp-gateway:** Session-aware routing, lifecycle management
* **Docker MCP Gateway:** Container isolation, minimal host privileges

**CLI security:**

* **cli-mcp-server:** Command whitelisting, path validation
* **win-cli-mcp-server:** Blocking rules for Windows environments

### Language Implementation Distribution

Transport support by implementation language:

* **Python:** Strong stdio + HTTP/SSE support (mcp-proxy, http-mcp-bridge)
* **Go:** Diverse transport support, gRPC specialty (protoc-gen-go-mcp, mcptools)
* **TypeScript/JavaScript:** HTTP/WebSocket focus (nchan-mcp-transport, supergateway)
* **C#:** Enterprise gateway (Microsoft mcp-gateway)

## Recommendations

**For developers choosing transports:**

* **Local development/testing:** Use stdio for simplicity and security
* **Remote access needed:** Add HTTP/SSE for web integration
* **Real-time bidirectional:** Consider WebSocket (nchan-mcp-transport, supergateway)
* **Microservices/service mesh:** Use gRPC bridge (protoc-gen-go-mcp)
* **Multi-server orchestration:** Use aggregator pattern (TBXark/mcp-proxy)
* **Enterprise deployment:** Choose enterprise gateways with auth/security (Microsoft, Lasso)

**For new MCP tool developers:**

1. **Start with stdio** - universal compatibility
2. **Add HTTP if needed** - for remote access, web APIs
3. **Add SSE with HTTP** - for streaming responses
4. **Consider WebSocket** - only if bidirectional real-time needed
5. **Consider gRPC** - for high-performance enterprise use cases

## Future Trends

Based on current ecosystem analysis:

* **WebSocket adoption likely to grow** for interactive AI applications
* **gRPC integration expanding** as enterprises adopt MCP
* **Security features becoming standard** (auth, filtering, isolation)
* **Multi-protocol gateways** (like supergateway) address diverse deployment needs
* **Container-based deployments** increasing (Docker, Kubernetes native support)
