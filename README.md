# MCP Ecosystem Tools Comparison

A comprehensive comparison of tools in the **MCP (Model Context Protocol)** ecosystem - from CLI clients to transport bridges to enterprise gateways.

## 🎯 Quick Navigation

| I want to... | Go here |
|--------------|---------|
| **Use a CLI with MCP servers** | [CLI Clients](#-cli-clients) |
| **Expose my MCP server as REST/HTTP** | [REST API Bridges](#-rest-api-bridges) |
| **Bridge MCP across transports** | [Transport Bridges](#-transport-bridges) |
| **Deploy enterprise MCP infrastructure** | [Enterprise Tools](#-enterprise--cloud) |
| **Convert gRPC/protobuf to MCP** | [gRPC Bridge](#-grpc-bridge) |
| **See security analysis** | [Security Analysis](comparisons/security.md) |
| **Browse all tools** | [Full Comparison](comparisons/auto-generated.md) |

## 📊 Ecosystem Overview

| Category | Projects | Description |
|----------|----------|-------------|
| CLI Clients | 10 | Command-line interfaces for MCP |
| Transport Bridges | 8 | stdio ↔ HTTP/SSE/WebSocket |
| REST API Bridges | 2 | Expose MCP as REST with OpenAPI |
| Enterprise Gateways | 2 | Production infrastructure |
| Specialized Adapters | 3 | CLI wrapping, command execution |
| Total | 27 | All tracked projects |

**Top projects:** 9,000+ combined GitHub stars • 8 reputable/official sources

## 💻 CLI Clients

Interactive command-line tools for working with MCP servers.

| Project | Stars | Language | Key Features |
|---------|------:|----------|--------------|
| [chrishayuk/mcp-cli](https://github.com/chrishayuk/mcp-cli) | 1.8k | Python | Chat, interactive shell, command-line |
| [f/mcptools](https://github.com/f/mcptools) | 1.4k | Go | Industrial-strength, discovery, management |
| [adhikasp/mcp-client-cli](https://github.com/adhikasp/mcp-client-cli) | 655 | Python | Simple, terminal alternative to Claude Desktop |
| [wong2/mcp-cli](https://github.com/wong2/mcp-cli) | 396 | JavaScript | Inspector, scriptable automation |
| [MladenSU/cli-mcp-server](https://github.com/MladenSU/cli-mcp-server) | 155 | Python | Secure CLI execution, command whitelisting |
| [mcp-use/mcp-use-cli](https://github.com/mcp-use/mcp-use-cli) | 48 | TypeScript | Chat-style, multi-provider LLM support |

**[View all CLI clients →](comparisons/auto-generated.md#cli-client)**

## 🔄 REST API Bridges

Expose MCP servers as REST APIs with OpenAPI/Swagger compatibility.

| Project | Stars | Language | Best For |
|---------|------:|----------|----------|
| [SecretiveShell/MCP-Bridge](https://github.com/SecretiveShell/MCP-Bridge) | 882 | Python | OpenAI-compatible endpoints |
| [acehoss/mcp-gateway](https://github.com/acehoss/mcp-gateway) | 128 | TypeScript | Custom GPTs, OpenAPI/Swagger |

**Key use cases:**

* Integrate MCP servers with GPT Actions and custom GPTs
* Provide OpenAPI-compatible REST endpoints
* Enable web applications to call MCP tools

## 🔌 Transport Bridges

Bridge between stdio MCP and HTTP/SSE/WebSocket transports.

| Project | Stars | Type | Transports |
|---------|------:|------|------------|
| [sparfenyuk/mcp-proxy](https://github.com/sparfenyuk/mcp-proxy) | 2.1k | Python | stdio ↔ HTTP/SSE |
| [TBXark/mcp-proxy](https://github.com/TBXark/mcp-proxy) | 592 | Go | Proxy aggregator + HTTP/SSE |
| [EvalsOne/MCP-connect](https://github.com/EvalsOne/MCP-connect) | 227 | TypeScript | stdio ↔ HTTP gateway |
| [ConechoAI/nchan-mcp-transport](https://github.com/ConechoAI/nchan-mcp-transport) | 28 | TypeScript | WebSocket/SSE high-performance |
| [nccgroup/http-mcp-bridge](https://github.com/nccgroup/http-mcp-bridge) | - | Python | HTTP/SSE (security testing) |
| [supercorp-ai/supergateway](https://github.com/supercorp-ai/supergateway) | - | TypeScript | Multi-protocol adapter |

**[Full Transport Details →](comparisons/transports.md)**

## 🏢 Enterprise & Cloud

Production-ready gateways from major organizations.

| Project | Organization | Features |
|---------|--------------|----------|
| [microsoft/mcp-gateway](https://github.com/microsoft/mcp-gateway) | Microsoft | K8s-native, session-aware routing, lifecycle management |
| [lasso-security/mcp-gateway](https://github.com/lasso-security/mcp-gateway) | Lasso Security | Security-first, guardrail plugins |
| [docker/mcp-gateway](https://github.com/docker/mcp-gateway) | Docker | Docker CLI plugin, container integration |

**Enterprise features:**

* Kubernetes integration and orchestration
* Security guardrails and policy enforcement
* Session management and routing
* Production observability

## ⚙️ gRPC Bridge

Convert between gRPC/protobuf and MCP.

| Project | Organization | Description |
|---------|--------------|-------------|
| [redpanda-data/protoc-gen-go-mcp](https://github.com/redpanda-data/protoc-gen-go-mcp) | Redpanda | protoc plugin: gRPC → MCP servers |

## 🔍 Specialized Adapters

Unique use cases and integrations.

| Project | Type | Description |
|---------|------|-------------|
| [eirikb/any-cli-mcp-server](https://github.com/eirikb/any-cli-mcp-server) | CLI wrapping | Auto-generate MCP tools from CLI help text |
| [g0t4/mcp-server-commands](https://github.com/g0t4/mcp-server-commands) | Command execution | Run arbitrary shell commands via MCP |
| [containers/kubernetes-mcp-server](https://github.com/containers/kubernetes-mcp-server) | K8s native | Native Go Kubernetes/OpenShift server |

## 📚 Detailed Comparisons

* **[Auto-generated tables](comparisons/auto-generated.md)** - Full comparison data with all projects
* **[Feature comparison](comparisons/features.md)** - Features by category, cross-cutting analysis
* **[Security analysis](comparisons/security.md)** - Code patterns, recommendations, per-project findings
* **[Transport support](comparisons/transports.md)** - Protocol matrix, implementation details

## 🔧 For Contributors

### Project Data Schema

Each project is documented in a YAML file under `projects/`:

```yaml
last-update: "2025-12-16"
repo-url: "https://github.com/owner/repo"
name: "Project Name"
stars: 1234
category: "cli-client"
transports:
  stdio: true
  http: true
```

See **[spec.yaml](spec.yaml)** for the full schema.

### Scripts

| Script | Purpose |
|--------|---------|
| `scripts/clone-all.sh` | Clone all tracked repos to `tmp/` |
| `scripts/check-yaml.py` | Validate YAML files against spec |
| `scripts/generate-tables.py` | Generate comparison tables |

### Generate Tables

```bash
# Generate all comparison tables
./scripts/generate-tables.py

# Specific views
./scripts/generate-tables.py --by-category
./scripts/generate-tables.py --by-transport
./scripts/generate-tables.py --reputable-only
```

### Repository Structure

```
├── README.md                    # This file
├── GUIDELINES.md                # Project guidelines
├── PROCESS.md                   # Research process
├── spec.yaml                    # YAML schema
├── projects/                    # Project YAML files
├── scripts/                     # Utility scripts
├── comparisons/                 # Detailed comparisons
├── ramblings/                   # Research notes
└── tmp/                         # Cloned repos (gitignored)
```

### Contributing

See **[CONTRIBUTING.md](CONTRIBUTING.md)** for detailed instructions.

Quick start:

1. Run `./scripts/clone-all.sh` to clone all repos
2. Analyze a project and update its YAML file
3. Run `./scripts/check-yaml.py` to validate
4. Regenerate tables: `./scripts/generate-tables.py > comparisons/auto-generated.md`
5. Submit a PR

## 🔒 Security Considerations

When evaluating these tools, we check for:

* **Network isolation**: Only connects to configured MCP servers?
* **Code execution**: Safe handling of `eval`, `exec`, subprocess calls?
* **Input validation**: Proper sanitization of user input?
* **Sandboxing**: Container/isolation support?

**[Full Security Analysis →](comparisons/security.md)**

## 📖 Research Resources

* [Perplexity: MCP Server Wrappers & REST Adapters](https://www.perplexity.ai/search/wrapping-mcp-servers-into-cli-0jIuIvdPSregFphOEGCWbw) - Initial research on wrapping MCP servers into CLI tools and exposing REST servers as MCP

## 📄 License

This research repository is released under MIT License.
