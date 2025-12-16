# Code Analysis Summary

**Date:** 2025-12-16
**Method:** Parallel subagents analyzing cloned repositories

## Key Security Findings

### Safe Projects (No dangerous patterns)

* **sparfenyuk--mcp-proxy**: No eval/exec, proper HTTP/SSE handling
* **chrishayuk--mcp-cli**: Safe LLM patterns, secure keyring storage
* **f--mcptools**: No injection vulnerabilities, guard mode for access control
* **adhikasp--mcp-client-cli**: LangChain-based, safe tool confirmation
* **TBXark--mcp-proxy**: Safe proxy patterns, config-based operation
* **wong2--mcp-cli**: URL sanitization, proper OAuth handling
* **microsoft--mcp-gateway**: Entra ID auth, RBAC, container isolation
* **redpanda-data--protoc-gen-go-mcp**: Type-safe code generation
* **MladenSU--cli-mcp-server**: Built-in whitelisting, path validation
* **docker--mcp-gateway**: Container isolation, secrets management
* **modelcontextprotocol--inspector**: Session tokens, auth by default
* **lasso-security--mcp-gateway**: Security-focused, PII detection

### Projects Requiring Careful Configuration

* **g0t4--mcp-server-commands**: Executes arbitrary commands (requires user approval)
* **eirikb--any-cli-mcp-server**: Wraps arbitrary CLIs (parses --help)
* **simon-ami--win-cli-mcp-server**: Windows shell execution (deprecated)

## Transport Support Summary

| Transport | Count | Projects |
|-----------|-------|----------|
| stdio | 27 | All projects |
| HTTP | 18 | Most bridges/gateways |
| SSE | 12 | sparfenyuk, wong2, supergateway, etc. |
| WebSocket | 3 | ConechoAI, supergateway, EvalsOne |
| gRPC | 1 | redpanda-data |

## Language Distribution

* **TypeScript/JavaScript**: 12 projects
* **Python**: 8 projects
* **Go**: 6 projects
* **C#/.NET**: 1 project (Microsoft)
* **R**: 1 project (Posit)

## Documentation Quality Ranking

1. **Excellent**: microsoft--mcp-gateway, containers--kubernetes-mcp-server, steipete--mcporter
2. **Very Good**: chrishayuk--mcp-cli, f--mcptools, modelcontextprotocol--inspector
3. **Good**: sparfenyuk--mcp-proxy, docker--mcp-gateway, ConechoAI--nchan-mcp-transport
4. **Adequate**: Most others
5. **Minimal**: Some CLI-wrapping servers

## Test Coverage

* **Best**: containers--kubernetes-mcp-server (64 test files), posit-dev--mcptools (full suite)
* **Good**: chrishayuk--mcp-cli (18 tests), sparfenyuk--mcp-proxy, eirikb--any-cli-mcp-server (12 tests)
* **Some**: f--mcptools (10 tests), supergateway (7 tests), lasso-security (7 tests)
* **Minimal**: Several CLI tools

## Recommendations

### For CLI Usage

* **General**: f/mcptools (Go, comprehensive)
* **LLM Integration**: chrishayuk/mcp-cli (Python, feature-rich)
* **Lightweight**: adhikasp/mcp-client-cli (Python, simple)
* **R Users**: posit-dev/mcptools

### For HTTP/API Exposure

* **Most Starred**: sparfenyuk/mcp-proxy (2.1k stars)
* **Multi-transport**: supercorp-ai/supergateway
* **WebSocket**: ConechoAI/nchan-mcp-transport

### For Enterprise

* **Kubernetes**: microsoft/mcp-gateway (C#, Azure integration)
* **Container**: docker/mcp-gateway (Official Docker)
* **Security**: lasso-security/mcp-gateway (Guardrails)

### For Development/Testing

* **Official**: modelcontextprotocol/inspector (Anthropic)
* **gRPC**: redpanda-data/protoc-gen-go-mcp
